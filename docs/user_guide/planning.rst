#########
 Planning
#########

PyEPLAN provides two main planning modules: Investment Planning and Operation Planning. These modules can be used independently or in combination to provide comprehensive microgrid analysis.

Investment Planning
==================

The Investment Planning module addresses long-term capacity expansion decisions (1-20 years) with the objective of minimizing total system costs while meeting reliability constraints.

Mathematical Formulation
------------------------

The investment planning problem is formulated as a mixed-integer linear programming (MILP) model:

**Objective Function**:

Minimize total system cost = Investment costs + Operation costs + Maintenance costs

**Constraints**:

* Power balance constraints
* Capacity constraints for generators and storage
* Network flow constraints
* Reliability constraints (loss of load probability)
* Budget constraints
* Technology-specific constraints

Key Features
-----------

* **Technology Selection**: Optimal choice of renewable generators, energy storage, and conventional units
* **Capacity Sizing**: Determination of optimal installed capacity for each technology
* **Geographic Siting**: Optimal placement of generation and storage facilities
* **Network Expansion**: Integration with feeder routing for optimal network design
* **Scenario Analysis**: Handling of uncertainty through representative days

Usage Example
------------

.. code-block:: python

    from pyeplan import inosys

    # Initialize investment planning system
    inv_system = inosys()

    # Load input data
    inv_system.load_data('input_data.csv')

    # Run investment planning
    results = inv_system.investment_planning(
        planning_horizon=10,  # years
        discount_rate=0.08,
        reliability_target=0.99
    )

    # Analyze results
    inv_system.analyze_results(results)

Operation Planning
=================

The Operation Planning module addresses short-term dispatch decisions (hourly to daily) to minimize operational costs while maintaining system reliability.

Mathematical Formulation
------------------------

The operation planning problem is formulated as a linear programming (LP) model:

**Objective Function**:

Minimize operation cost = Fuel costs + Variable O&M costs + Grid exchange costs

**Constraints**:

* Power balance at each bus
* Generator capacity and ramping constraints
* Storage charge/discharge constraints
* Network capacity constraints
* Reserve requirements

Key Features
-----------

* **Economic Dispatch**: Optimal power generation scheduling
* **Unit Commitment**: Start-up/shut-down decisions for conventional units
* **Storage Management**: Optimal charge/discharge scheduling
* **Reserve Allocation**: Spinning and non-spinning reserve management
* **Grid Integration**: Power exchange with main grid

Usage Example
------------

.. code-block:: python

    from pyeplan import inosys

    # Initialize operation planning system
    op_system = inosys()

    # Load input data
    op_system.load_data('operation_data.csv')

    # Run operation planning
    results = op_system.operation_planning(
        time_horizon=24,  # hours
        reserve_margin=0.15
    )

    # Analyze results
    op_system.analyze_operation(results)

Integrated Planning
==================

PyEPLAN allows for integrated investment and operation planning, where long-term investment decisions are optimized considering detailed operational constraints.

Benefits:

* More accurate cost estimates
* Better technology selection
* Improved system reliability
* Comprehensive financial analysis

The integrated approach ensures that investment decisions are made with full consideration of operational implications, leading to more robust and cost-effective solutions.


