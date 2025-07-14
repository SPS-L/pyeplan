#######################
Release Notes
#######################

This section documents the version history and changes in PyEPlan releases.

PyEPlan 1.1.0 (Current Version)
===============================

**Production Release - Enhanced Features**

New Features:

* **PVGIS 5.3 API Integration**: Updated to latest PVGIS API with support for multiple radiation databases (SARAH2, ERA5, NSRDB)
* **Enhanced Data Processing**: Improved time series clustering with K-means algorithm and better data validation
* **Unified Optimization Framework**: Combined investment and operation planning in single MILP formulation
* **Comprehensive Battery Modeling**: Advanced battery energy storage system (BESS) modeling with state of charge tracking
* **Network Topology Optimization**: Minimum spanning tree algorithm for optimal feeder routing
* **Multiple Solver Support**: Enhanced support for GLPK, CBC, IPOPT, Gurobi, and other Pyomo-compatible solvers

Enhancements:

* **Improved API Structure**: Clean module organization with datsys, rousys, and inosys classes
* **Better Error Handling**: Comprehensive validation for input data and API communication
* **Enhanced Documentation**: Complete API reference and usage examples
* **Geographic Data Processing**: Haversine distance calculations and timezone detection
* **Flexible Optimization Modes**: Investment-only, operation-only, and combined modes
* **Structured Results**: Pandas DataFrame outputs for easy analysis and visualization

Technical Improvements:

* **Memory Optimization**: Efficient data structures and sparse matrix handling
* **Numerical Stability**: Improved convergence for large-scale optimization problems
* **Code Quality**: Enhanced code documentation and type hints
* **Modular Design**: Clean separation of concerns between data processing, routing, and optimization

PyEPlan 1.0.0 (12 Jul 2024)
============================

**Major Release - Production Ready**

New Features:

* Complete rewrite of core optimization engine for improved performance
* Enhanced data processing with support for multiple weather data sources
* Advanced clustering algorithms for representative day selection
* Comprehensive API documentation and examples
* Improved error handling and validation
* Support for both on-grid and off-grid microgrid configurations
* Integration with multiple optimization solvers (Gurobi, CPLEX, GLPK, CBC)

Enhancements:

* Better memory management for large-scale problems
* Enhanced visualization capabilities with interactive plots
* Improved network routing algorithms
* More accurate financial modeling and cost analysis
* Better handling of renewable energy uncertainty
* Enhanced user interface and documentation

Bug Fixes:

* Fixed convergence issues in large optimization problems
* Corrected timezone handling in weather data extraction
* Improved numerical stability in clustering algorithms
* Fixed memory leaks in long-running simulations

Breaking Changes:

* Updated API for better consistency and usability
* Changed default solver parameters for improved performance
* Modified input file formats for better standardization

PyEPlan 0.5 (18 Oct 2023)
==========================

**Minor Release**

Bug Fixes:

* Fixed various issues and made it compatible with Python >v3.11
* Improved package compatibility and installation
* Enhanced error handling for newer Python versions

PyEPlan 0.4 (14 Nov 2022)
==========================

**Minor Release**

Features:

* Enhanced data processing capabilities
* Improved optimization algorithms
* Better documentation and examples
* Enhanced error handling and validation

PyEPlan 0.3 (14 Feb 2022)
==========================

**Patch Release**

Bug Fixes:

* Updated __init__.py for better package structure
* Fixed import issues and module organization
* Improved package distribution

PyEPlan 0.1 (15 Jun 2020)
==========================

**First Beta Release (Pre-release)**

Features:

* Initial implementation of core modules
* Basic data processing capabilities
* Simple routing algorithms
* Investment and operation planning optimization
* Support for basic renewable energy sources

Known Issues:

* Limited solver support
* Basic error handling
* Minimal documentation
* Performance issues with large problems

Development Roadmap
==================

**Upcoming Features (v1.2.0)**:

* Real-time optimization capabilities
* Advanced uncertainty modeling with Monte Carlo simulation
* Integration with additional renewable energy data sources
* Enhanced visualization and reporting tools
* Support for multi-objective optimization
* Advanced machine learning integration for load forecasting

**Future Plans (v2.0.0)**:

* Cloud-based deployment options
* Real-time monitoring and control integration
* Integration with SCADA systems
* Advanced grid services modeling
* Support for electric vehicle charging infrastructure
* Multi-energy system optimization (heat, electricity, hydrogen)

Migration Guide
==============

**From v1.0.0 to v1.1.0**:

* Updated PVGIS API integration - new radiation database options
* Enhanced battery modeling with improved state of charge tracking
* Unified optimization framework - combined investment and operation planning
* Improved result methods with structured DataFrame outputs
* Enhanced error handling and validation

**From v0.5 to v1.0.0**:

* Update import statements to use new module structure
* Modify input file formats to match new standards
* Update solver configuration parameters
* Review and update custom scripts for API changes

**From v0.4 to v0.5**:

* No breaking changes - compatibility improvements only
* Enhanced Python 3.11+ support

**From v0.3 to v0.4**:

* Enhanced functionality with improved algorithms
* Better documentation and error handling

**From v0.1 to v0.3**:

* Updated package structure and imports
* Improved module organization
* Enhanced error handling