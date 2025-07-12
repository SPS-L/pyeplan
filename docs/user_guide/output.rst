#######
 Output
#######

PyEPLAN generates comprehensive output files that provide detailed analysis results for investment planning, operation planning, and system performance evaluation.

Output File Structure
====================

PyEPLAN produces several types of output files:

1. **Results Summary Files**: High-level results and key performance indicators
2. **Detailed Analysis Files**: Hourly/daily operation details
3. **Visualization Files**: Plots and charts for result interpretation
4. **Financial Reports**: Cost breakdowns and economic analysis

Investment Planning Outputs
==========================

**Investment Summary** (`investment_summary.csv`)
* Optimal technology selection and sizing
* Total investment costs by technology
* Annualized costs and levelized cost of energy (LCOE)
* System reliability metrics

**Capacity Expansion Plan** (`capacity_plan.csv`)
* Year-by-year capacity additions
* Technology mix evolution
* Geographic distribution of new capacity

**Financial Analysis** (`financial_analysis.csv`)
* Net present value (NPV) calculations
* Internal rate of return (IRR)
* Payback period analysis
* Sensitivity analysis results

Operation Planning Outputs
=========================

**Hourly Dispatch** (`hourly_dispatch.csv`)
* Generator output for each hour
* Storage charge/discharge profiles
* Grid exchange power
* Reserve allocation

**System Performance** (`system_performance.csv`)
* System reliability metrics
* Loss of load probability (LOLP)
* Expected energy not served (EENS)
* Capacity factor analysis

**Cost Analysis** (`operation_costs.csv`)
* Fuel costs by generator
* Variable O&M costs
* Grid exchange costs
* Total operation costs

Network Analysis Outputs
========================

**Network Configuration** (`network_config.csv`)
* Optimal line connections
* Line capacities and flows
* Voltage profiles
* Loss analysis

**Geographic Visualization** (`network_map.html`)
* Interactive map showing network layout
* Generator and load locations
* Line connections and capacities

Output File Formats
==================

PyEPLAN generates outputs in multiple formats:

* **CSV Files**: Tabular data for further analysis
* **Excel Files**: Formatted reports with multiple sheets
* **HTML Files**: Interactive visualizations
* **PNG/PDF Files**: Static plots and charts

Example Output Structure
========================

```
results/
├── investment_summary.csv
├── capacity_plan.csv
├── financial_analysis.csv
├── hourly_dispatch.csv
├── system_performance.csv
├── operation_costs.csv
├── network_config.csv
├── plots/
│   ├── generation_profile.png
│   ├── cost_breakdown.png
│   └── network_layout.png
└── reports/
    ├── investment_report.xlsx
    └── operation_report.xlsx
```

Interpreting Results
===================

**Key Performance Indicators**:
* **LCOE**: Levelized Cost of Energy (USD/kWh)
* **NPV**: Net Present Value of investment
* **IRR**: Internal Rate of Return
* **LOLP**: Loss of Load Probability
* **Capacity Factor**: Average utilization of generators

**Economic Analysis**:
* Compare different technology combinations
* Assess sensitivity to key parameters
* Evaluate grid vs. off-grid scenarios
* Analyze impact of renewable penetration

**Technical Analysis**:
* System reliability assessment
* Network adequacy evaluation
* Storage utilization analysis
* Reserve requirement analysis

Visualization and Reporting
==========================

PyEPLAN provides comprehensive visualization capabilities:

* **Generation Profiles**: Time series plots of renewable and conventional generation
* **Load Profiles**: Daily and seasonal load patterns
* **Cost Breakdowns**: Pie charts and bar charts of cost components
* **Network Layouts**: Geographic visualization of system topology
* **Sensitivity Analysis**: Parameter impact on key metrics

The visualization tools help users understand complex optimization results and communicate findings to stakeholders effectively.
