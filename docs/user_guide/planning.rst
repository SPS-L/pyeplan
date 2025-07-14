#########
 Planning
#########

PyEPlan provides a unified Investment and Operation Planning module (inosys) that addresses both long-term capacity expansion decisions and short-term dispatch optimization in a single optimization framework using mixed-integer linear programming (MILP).

Unified Investment and Operation Planning
=========================================

The inosys module combines investment and operation planning in a single optimization problem, allowing for comprehensive microgrid analysis that considers both long-term investment decisions and short-term operational constraints simultaneously.

Mathematical Formulation
------------------------

The unified planning problem is formulated as a mixed-integer linear programming (MILP) model:

**Objective Function**:

Minimize total system cost = Investment costs + Operation costs + Shedding costs

Where:
* Investment costs = Capital costs for generators, storage, and renewables
* Operation costs = Fuel costs + Variable O&M costs + Grid exchange costs
* Shedding costs = Demand shedding + Renewable curtailment costs

**Constraints**:

* **Power Balance**: Active and reactive power balance at each bus
* **Generator Constraints**: Capacity limits, ramping constraints for conventional generators
* **Renewable Constraints**: Maximum available power from solar and wind
* **Storage Constraints**: Charge/discharge limits, state of charge constraints
* **Network Constraints**: Line capacity limits, voltage limits
* **Investment Constraints**: Binary variables for technology selection
* **Operational Constraints**: Minimum up/down times, start-up costs

Key Features
-----------

* **Technology Selection**: Optimal choice of renewable generators, energy storage, and conventional units
* **Capacity Sizing**: Determination of optimal installed capacity for each technology
* **Geographic Siting**: Optimal placement of generation and storage facilities
* **Economic Dispatch**: Optimal power generation scheduling
* **Storage Management**: Optimal charge/discharge scheduling with state of charge tracking
* **Demand Management**: Load shedding and renewable curtailment optimization
* **Network Integration**: Power flow and voltage constraints
* **Scenario Analysis**: Handling of uncertainty through representative days

Usage Example
------------

.. code-block:: python

    from pyeplan import inosys

    # Initialize investment and operation planning system
    planning_system = inosys(
        inp_folder="input_folder",
        ref_bus=0,
        dshed_cost=1000000,  # High cost to discourage load shedding
        rshed_cost=500,      # Cost for renewable curtailment
        phase=3,             # Three-phase system
        vmin=0.85,           # Minimum voltage limit
        vmax=1.15,           # Maximum voltage limit
        sbase=1,             # Base apparent power
        sc_fa=1              # Scaling factor
    )

    # Solve the unified optimization problem
    planning_system.solve(
        solver='glpk',       # Optimization solver
        neos=False,          # Not using NEOS server
        invest=True,         # Include investment decisions
        onlyopr=False,       # Not operation-only mode
        commit=False,        # Not committing to NEOS
        solemail='',         # Solver email (for NEOS)
        verbose=False        # Verbose output
    )

    # Get optimization results
    costs = planning_system.resCost()
    wind_results = planning_system.resWind()
    battery_results = planning_system.resBat()
    solar_results = planning_system.resSolar()
    conventional_results = planning_system.resConv()
    curtailment_results = planning_system.resCurt()

Supported Technologies
=====================

**Conventional Generators**:
* Diesel generators
* Gas turbines
* Combined heat and power (CHP) units
* Grid connection (import/export)

**Renewable Energy Sources**:
* Solar photovoltaic (PV) systems
* Wind turbines
* Hybrid renewable systems

**Energy Storage**:
* Battery energy storage systems (BESS)
* Pumped hydro storage
* Thermal storage

**Network Components**:
* Distribution lines and cables
* Transformers
* Switchgear and protection devices

Optimization Modes
==================

**Investment and Operation Mode** (`invest=True`, `onlyopr=False`):
* Optimizes both investment decisions and operational dispatch
* Determines optimal technology mix and sizing
* Provides comprehensive cost analysis

**Operation-Only Mode** (`invest=False`, `onlyopr=True`):
* Optimizes only operational dispatch for existing infrastructure
* Useful for operational analysis and cost assessment
* Faster computation for large systems

**Investment-Only Mode** (`invest=True`, `onlyopr=False` with simplified operational constraints):
* Focuses on long-term investment decisions
* Uses simplified operational representation
* Suitable for strategic planning

Solver Options
==============

PyEPlan supports multiple optimization solvers through Pyomo:

**Open-Source Solvers**:
* GLPK (GNU Linear Programming Kit) - Default
* CBC (COIN-OR Branch and Cut)
* IPOPT (Interior Point Optimizer)

**Commercial Solvers**:
* Gurobi
* CPLEX
* MOSEK

**Solver Selection Guidelines**:
* GLPK: Good for small to medium problems
* CBC: Better for larger MILP problems
* Gurobi/CPLEX: Best performance for large-scale problems
* IPOPT: Suitable for continuous optimization problems

Results Analysis
===============

The optimization results provide comprehensive information about:

**Cost Analysis**:
* Total system cost breakdown
* Investment costs by technology
* Operational costs by component
* Levelized cost of energy (LCOE)

**Technology Mix**:
* Optimal installed capacity
* Technology selection decisions
* Geographic distribution

**Operational Performance**:
* Hourly dispatch schedules
* Storage state of charge profiles
* Network power flows
* Voltage profiles

**Reliability Metrics**:
* Loss of load probability
* Energy not served
* System adequacy indicators

Integration with Other Modules
=============================

The planning module integrates seamlessly with other PyEPlan modules:

**Data Processing Integration**:
* Uses representative days from datsys module
* Incorporates renewable generation profiles
* Handles load demand scenarios

**Network Integration**:
* Incorporates network topology from rousys module
* Considers line parameters and constraints
* Optimizes power flow distribution

This integrated approach ensures that all aspects of microgrid planning are considered in a unified optimization framework, leading to more robust and cost-effective solutions.


