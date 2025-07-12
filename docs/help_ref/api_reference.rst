######################
API Reference
######################

This section provides detailed API documentation for all PyEPLAN modules and classes.

Core Modules
============

Data Processing Module
---------------------

The data processing module handles historical weather data extraction and representative day clustering.

.. autoclass:: pyeplan.datsys
    :members:
    :undoc-members:
    :show-inheritance:

**Key Methods**:

* `extract_weather_data()`: Extract historical weather data from satellite sources
* `create_daily_profiles()`: Generate 24-hour daily profiles for renewable generation
* `cluster_representative_days()`: Apply machine learning algorithms for scenario reduction
* `validate_data()`: Check data quality and consistency

**Example Usage**:
```python
from pyeplan import datsys

# Initialize data processing system
data_system = datsys()

# Extract weather data for a location
weather_data = data_system.extract_weather_data(
    latitude=1.2921,
    longitude=36.8219,
    start_date='2020-01-01',
    end_date='2020-12-31'
)

# Create representative days
rep_days = data_system.cluster_representative_days(
    data=weather_data,
    n_clusters=5,
    method='kmeans'
)
```

Routing Module
--------------

The routing module performs optimal network design using minimum spanning tree algorithms.

.. autoclass:: pyeplan.rousys
    :members:
    :undoc-members:
    :show-inheritance:

**Key Methods**:

* `load_coordinates()`: Load geographic coordinates of nodes
* `calculate_distances()`: Compute distances between all node pairs
* `optimize_network()`: Find optimal network topology
* `analyze_network()`: Evaluate network performance metrics

**Example Usage**:
```python
from pyeplan import rousys

# Initialize routing system
routing_system = rousys()

# Load node coordinates
routing_system.load_coordinates('coordinates.csv')

# Optimize network design
network = routing_system.optimize_network(
    method='mst',
    cost_function='distance'
)

# Analyze results
results = routing_system.analyze_network(network)
```

Investment and Operation Planning Module
---------------------------------------

The investment and operation planning module handles both long-term capacity expansion and short-term dispatch optimization.

.. autoclass:: pyeplan.inosys
    :members:
    :undoc-members:
    :show-inheritance:

**Key Methods**:

Investment Planning:
* `investment_planning()`: Long-term capacity expansion optimization
* `analyze_investment()`: Investment cost and performance analysis
* `sensitivity_analysis()`: Parameter sensitivity evaluation

Operation Planning:
* `operation_planning()`: Short-term dispatch optimization
* `analyze_operation()`: Operation cost and performance analysis
* `unit_commitment()`: Generator start-up/shut-down decisions

**Example Usage**:
```python
from pyeplan import inosys

# Initialize planning system
planning_system = inosys()

# Load input data
planning_system.load_data('input_data.csv')

# Run investment planning
inv_results = planning_system.investment_planning(
    horizon=10,
    discount_rate=0.08,
    reliability_target=0.99
)

# Run operation planning
op_results = planning_system.operation_planning(
    horizon=24,
    reserve_margin=0.15
)

# Analyze results
planning_system.analyze_results(inv_results, op_results)
```

Data Structures
==============

Input Data Format
----------------

PyEPLAN uses standardized CSV formats for input data:

**Component Data**:
* Generator characteristics (capacity, costs, efficiency)
* Storage system parameters (capacity, efficiency, lifetime)
* Network line parameters (resistance, reactance, capacity)

**Time Series Data**:
* Load profiles (hourly/daily demand)
* Renewable generation profiles (solar, wind)
* Fuel prices and grid tariffs

**Geographic Data**:
* Node coordinates (latitude, longitude)
* Terrain and accessibility information
* Climate zone classifications

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

**General Parameters**:
* `planning_horizon`: Time horizon for investment planning (years)
* `discount_rate`: Discount rate for financial calculations
* `reliability_target`: Target system reliability level

**Technical Parameters**:
* `reserve_margin`: Reserve capacity requirement
* `voltage_limits`: Acceptable voltage deviation range
* `line_capacity`: Maximum line loading limits

**Economic Parameters**:
* `fuel_prices`: Fuel cost projections
* `technology_costs`: Capital cost assumptions
* `grid_tariffs`: Grid exchange price structure

Error Handling
==============

PyEPLAN includes comprehensive error handling for:

* **Data Validation**: Input data format and range checking
* **Solver Issues**: Optimization solver failures and timeouts
* **Convergence Problems**: Non-convergent optimization problems
* **Memory Issues**: Large-scale problem memory management

**Example Error Handling**:
```python
try:
    results = planning_system.investment_planning()
except ValueError as e:
    print(f"Data validation error: {e}")
except RuntimeError as e:
    print(f"Optimization error: {e}")
except MemoryError as e:
    print(f"Memory limit exceeded: {e}")
```

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
