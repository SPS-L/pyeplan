#######
 Output
#######

PyEPlan generates comprehensive output through various result methods that provide detailed analysis results for investment planning, operation planning, and system performance evaluation.

Output Structure
================

PyEPlan produces results through dedicated methods that return pandas DataFrames containing detailed analysis information:

1. **Cost Analysis Results**: Total system costs and breakdowns
2. **Technology Results**: Generation and storage operation details
3. **Network Results**: Power flows and voltage profiles
4. **Curtailment Results**: Load shedding and renewable curtailment

Cost Analysis Outputs
====================

**Cost Results** (`resCost()` method)

Returns a pandas DataFrame containing:

* Total system cost breakdown
* Investment costs by technology type
* Operational costs by component
* Shedding costs (demand and renewable)
* Cost per scenario and time period

Example output structure:

.. code-block:: python

    costs = inv_sys.resCost()
    print(costs.head())
    
    # Typical columns:
    # - scenario: Representative day scenario
    # - time_period: Hour of the day
    # - investment_cost: Capital costs
    # - operation_cost: Fuel and O&M costs
    # - shedding_cost: Load shedding and curtailment costs
    # - total_cost: Sum of all costs

Technology Operation Results
===========================

**Wind Generation Results** (`resWind()` method)

Returns detailed wind turbine operation:
* Power generation by wind turbine
* Capacity utilization
* Curtailment levels
* Operation by scenario and time period

**Solar Generation Results** (`resSolar()` method)

Returns detailed solar PV operation:

* Power generation by solar system
* Capacity utilization
* Curtailment levels
* Operation by scenario and time period

**Conventional Generation Results** (`resConv()` method)

Returns conventional generator operation:

* Power generation by generator
* Start-up/shut-down decisions
* Fuel consumption
* Operation costs

**Battery Storage Results** (`resBat()` method)

Returns battery energy storage operation:

* Charge/discharge power
* State of charge profiles
* Energy storage levels
* Battery utilization

Curtailment Analysis
====================

**Curtailment Results** (`resCurt()` method)

Returns information about:

* Load shedding by bus and time period
* Renewable energy curtailment
* Shedding costs and penalties
* System adequacy indicators

Network Analysis Outputs
========================

**Network Configuration Files**

The routing module (rousys) generates:

* `path.png`: Network topology visualization
* `rou_dist.csv`: Routing distances between connected nodes
* `elin_dist.csv`: Electrical line parameters and specifications

**Network Parameters**:

* Line resistances and reactances
* Current carrying capacities
* Voltage drop calculations
* Power flow limits

Data Processing Outputs
======================

**Representative Days**

The data processing module (datsys) generates:

* Clustered representative days
* Renewable generation profiles
* Load demand scenarios
* Time duration weights for each scenario

**PVGIS Data**:

* Solar irradiance profiles
* Wind speed data
* Temperature profiles
* Geographic and temporal data

Output File Formats
==================

PyEPlan generates outputs in multiple formats:

* **Pandas DataFrames**: Structured data for analysis and visualization
* **CSV Files**: Network configuration and routing data
* **PNG Files**: Network topology visualizations
* **Excel Files**: Input data and configuration files

Example Output Structure
========================

.. code-block:: text

    input_folder/
    ├── mgpc_dist.xlsx              # Load and generation data
    ├── geol_dist.csv               # Geographic coordinates
    ├── cblt_dist.csv               # Cable parameters
    ├── cgen_dist.csv               # Conventional generator data
    ├── csol_dist.csv               # Solar PV data
    ├── cwin_dist.csv               # Wind turbine data
    ├── cbat_dist.csv               # Battery storage data
    ├── elin_dist.csv               # Electrical line data
    ├── pdem_dist.csv               # Active power demand
    ├── qdem_dist.csv               # Reactive power demand
    ├── prep_dist.csv               # Renewable power profiles
    ├── qrep_dist.csv               # Renewable reactive power
    ├── psol_dist.csv               # Solar power scenarios
    ├── qsol_dist.csv               # Solar reactive scenarios
    ├── pwin_dist.csv               # Wind power scenarios
    ├── qwin_dist.csv               # Wind reactive scenarios
    ├── dtim_dist.csv               # Time duration weights
    ├── rou_dist.csv                # Routing distances (generated)
    ├── elin_dist.csv               # Electrical lines (generated)
    └── path.png                    # Network visualization (generated)

Interpreting Results
===================

**Key Performance Indicators**:

* **Total System Cost**: Sum of investment, operation, and shedding costs
* **Technology Mix**: Optimal capacity and operation of each technology
* **System Reliability**: Load shedding and curtailment levels
* **Storage Utilization**: Battery charge/discharge patterns
* **Network Performance**: Power flows and voltage profiles

**Economic Analysis**:

* Compare different technology combinations
* Assess cost sensitivity to key parameters
* Evaluate grid vs. off-grid scenarios
* Analyze impact of renewable penetration

**Technical Analysis**:

* System reliability assessment
* Network adequacy evaluation
* Storage utilization analysis
* Renewable energy integration

Results Analysis Example
========================

.. code-block:: python

    # Get comprehensive results
    costs = inv_sys.resCost()
    wind_results = inv_sys.resWind()
    battery_results = inv_sys.resBat()
    solar_results = inv_sys.resSolar()
    conventional_results = inv_sys.resConv()
    curtailment_results = inv_sys.resCurt()
    
    # Analyze total system cost
    total_cost = costs['total_cost'].sum()
    print(f"Total System Cost: ${total_cost:,.2f}")
    
    # Analyze technology mix
    wind_capacity = wind_results['capacity'].max()
    solar_capacity = solar_results['capacity'].max()
    battery_capacity = battery_results['capacity'].max()
    
    print(f"Optimal Capacity Mix:")
    print(f"  Wind: {wind_capacity:.2f} kW")
    print(f"  Solar: {solar_capacity:.2f} kW")
    print(f"  Battery: {battery_capacity:.2f} kWh")
    
    # Analyze system reliability
    total_shedding = curtailment_results['load_shedding'].sum()
    total_curtailment = curtailment_results['renewable_curtailment'].sum()
    
    print(f"System Reliability:")
    print(f"  Total Load Shedding: {total_shedding:.2f} kWh")
    print(f"  Total Renewable Curtailment: {total_curtailment:.2f} kWh")

Visualization and Reporting
==========================

PyEPlan results can be easily visualized using standard Python plotting libraries:

* **Time Series Plots**: Generation profiles, load patterns, storage levels
* **Bar Charts**: Cost breakdowns, capacity mix, technology comparison
* **Network Diagrams**: System topology and power flows
* **Heat Maps**: Spatial and temporal analysis of system operation

The structured DataFrame outputs enable easy integration with external analysis tools and custom visualization workflows.
