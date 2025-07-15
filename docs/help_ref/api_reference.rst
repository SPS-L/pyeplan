######################
API Reference
######################

This section provides detailed API documentation for all PyEPlan modules and classes.

Core Modules
============

Data Processing Module (datsys)
-------------------------------

The data processing module handles historical weather data extraction and representative day clustering using PVGIS API.

.. autoclass:: pyeplan.datsys
    :members:
    :undoc-members:
    :show-inheritance: 

**Key Methods**:

* `data_extract()`: Extract historical weather data from PVGIS API
* `kmeans_clust()`: Apply K-means clustering for scenario reduction
* `_validate_output_format()`: Validate PVGIS API output format
* `_normalize_column_names()`: Normalize data column names

**Example Usage**:

.. code-block:: python

    from pyeplan import datsys

    # Initialize data processing system
    data_system = datsys(
        inp_folder="input_folder",
        lat=0.25,
        lon=32.40,
        year=2016,
        pvcalc=1,
        pp=50,
        sys_loss=14,
        n_clust=5
    )

    # Extract weather data from PVGIS
    data_system.data_extract()

    # Create representative days using K-means clustering
    data_system.kmeans_clust()

Routing Module (rousys)
-----------------------

The routing module performs optimal network design using minimum spanning tree algorithms.

.. autoclass:: pyeplan.rousys
    :members:
    :undoc-members:
    :show-inheritance:

**Key Methods**:

* `min_spn_tre()`: Generate minimum spanning tree network topology
* `distance()`: Calculate geographical distance between two points using Haversine formula

**Example Usage**:

.. code-block:: python

    from pyeplan import rousys

    # Initialize routing system
    routing_system = rousys(
        inp_folder="input_folder",
        crs=35,
        typ=7,
        vbase=415,
        sbase=1
    )

    # Generate optimal network topology
    routing_system.min_spn_tre()

Investment and Operation Module (inosys)
----------------------------------------

The investment and operation module handles both long-term capacity expansion and short-term dispatch optimization using mixed-integer linear programming.

.. autoclass:: pyeplan.inosys
    :members:
    :undoc-members:
    :show-inheritance:

**Key Methods**:

Optimization:

* `solve()`: Solve the investment and operation optimization problem

Results Analysis:

* `resCost()`: Get optimization results - costs
* `resWind()`: Get optimization results - wind generation
* `resBat()`: Get optimization results - battery operation
* `resSolar()`: Get optimization results - solar generation
* `resConv()`: Get optimization results - conventional generation
* `resCurt()`: Get optimization results - curtailment

**Example Usage**:

.. code-block:: python

    from pyeplan import inosys

    # Initialize planning system
    planning_system = inosys(
        inp_folder="input_folder",
        ref_bus=0,
        dshed_cost=1000000,
        rshed_cost=500,
        phase=3,
        vmin=0.85,
        vmax=1.15,
        sbase=1,
        sc_fa=1
    )

    # Solve investment and operation optimization
    planning_system.solve(
        solver='glpk',
        neos=False,
        invest=True,
        onlyopr=False,
        commit=False,
        solemail='',
        verbose=False
    )

    # Get results
    costs = planning_system.resCost()
    wind_results = planning_system.resWind()
    battery_results = planning_system.resBat()

Utility Functions
=================

Data Conversion Functions
-------------------------

* `pyomo2dfinv()`: Convert Pyomo investment variables to pandas DataFrame
* `pyomo2dfopr()`: Convert Pyomo operation variables to pandas DataFrame
* `pyomo2dfoprm()`: Convert Pyomo operation variables to pandas DataFrame (modified)

Data Structures
==============

Input Data Format
----------------

PyEPlan uses standardized CSV and Excel formats for input data:

**Component Data**:

* Generator characteristics (capacity, costs, efficiency)
* Storage system parameters (capacity, efficiency, lifetime)
* Network line parameters (resistance, reactance, capacity)
* Cable specifications (cross-section, resistance, current rating)

**Time Series Data**:

* Load profiles (hourly/daily demand)
* Renewable generation profiles (solar, wind)
* Fuel prices and grid tariffs

**Geographic Data**:

* Node coordinates (latitude, longitude)
* Terrain and accessibility information
* Climate zone classifications

**Required Input Files**:

Data Processing (datsys):

* `mgpc_dist.xlsx`: Load point and load level data

Routing (rousys):

* `geol_dist.csv`: Geographical coordinates of nodes
* `cblt_dist.csv`: Cable parameters and specifications

Investment & Operation (inosys):

* `cgen_dist.csv`: Conventional generator candidate data
* `egen_dist.csv`: Existing conventional generator data
* `csol_dist.csv`: Solar PV candidate data
* `esol_dist.csv`: Existing solar PV data
* `cwin_dist.csv`: Wind turbine candidate data
* `ewin_dist.csv`: Existing wind turbine data
* `cbat_dist.csv`: Battery storage candidate data
* `elin_dist.csv`: Electrical line data
* `pdem_dist.csv`: Active power demand profiles
* `qdem_dist.csv`: Reactive power demand profiles
* `prep_dist.csv`: Renewable active power profiles
* `qrep_dist.csv`: Renewable reactive power profiles
* `psol_dist.csv`: Solar power scenarios
* `qsol_dist.csv`: Solar reactive power scenarios
* `pwin_dist.csv`: Wind power scenarios
* `qwin_dist.csv`: Wind reactive power scenarios
* `dtim_dist.csv`: Time duration for each scenario

Output Data Format
-----------------

**Results Summary**:

* Optimal technology mix and sizing
* Total system costs and performance metrics
* Financial indicators (NPV, IRR, LCOE)

**Detailed Results**:

* Hourly dispatch schedules
* Network flows and losses
* Reliability and adequacy metrics

Configuration Parameters
========================

**Data Processing Parameters**:

* `lat`, `lon`: Geographic coordinates
* `year`: Data collection year
* `pvcalc`: PV calculation method (0=radiation only, 1=power+radiation)
* `pp`: Nominal power of PV system in kW
* `sys_loss`: System losses in %
* `n_clust`: Number of clusters for time series clustering

**Routing Parameters**:

* `crs`: Cross section of cables in mm²
* `typ`: Type of cables
* `vbase`: Line-to-line voltage in V
* `sbase`: Base apparent power in kW

**Optimization Parameters**:

* `ref_bus`: Reference bus number
* `dshed_cost`: Demand shedding cost
* `rshed_cost`: Renewable shedding cost
* `vmin`, `vmax`: Voltage limits in p.u.
* `phase`: Number of phases

Error Handling
==============

PyEPlan includes comprehensive error handling for:

* **Data Validation**: Input data format and range checking
* **Solver Issues**: Optimization solver failures and timeouts
* **Convergence Problems**: Non-convergent optimization problems
* **Memory Issues**: Large-scale problem memory management
* **API Communication**: PVGIS API connection and data retrieval issues

**Example Error Handling**:

.. code-block:: python

    try:
        results = planning_system.solve(solver='glpk')
    except ValueError as e:
        print(f"Data validation error: {e}")
    except RuntimeError as e:
        print(f"Optimization error: {e}")
    except MemoryError as e:
        print(f"Memory limit exceeded: {e}")

Performance Considerations
=========================

**Large-Scale Problems**:

* Use representative day clustering to reduce problem size
* Implement decomposition techniques for multi-year planning
* Consider parallel processing for scenario analysis

**Memory Management**:

* Monitor memory usage for large networks
* Use sparse matrix representations where possible
* Implement data streaming for large time series

**Solver Selection**:

* Commercial solvers (Gurobi, CPLEX) for large problems
* Open-source solvers (GLPK, CBC) for smaller problems
* Consider solver-specific parameter tuning

**PVGIS API Optimization**:

* Cache API responses for repeated queries
* Use appropriate radiation database for geographic region
* Handle API rate limits and timeouts gracefully
