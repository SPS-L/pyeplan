#######################
Release Notes
#######################

This section documents the version history and changes in PyEPLAN releases.

PyEPLAN 1.0.0 (12 Jul 2024)
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

PyEPLAN 0.5 (18 Oct 2023)
==========================

**Minor Release**

Bug Fixes:

* Fixed various issues and made it compatible with Python >v3.11
* Improved package compatibility and installation
* Enhanced error handling for newer Python versions

PyEPLAN 0.4 (14 Nov 2022)
==========================

**Minor Release**

Features:

* Enhanced data processing capabilities
* Improved optimization algorithms
* Better documentation and examples
* Enhanced error handling and validation

PyEPLAN 0.3 (14 Feb 2022)
==========================

**Patch Release**

Bug Fixes:

* Updated __init__.py for better package structure
* Fixed import issues and module organization
* Improved package distribution

PyEPLAN 0.1 (15 Jun 2020)
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

**Upcoming Features (v1.1.0)**:

* Real-time optimization capabilities
* Advanced uncertainty modeling
* Integration with external data sources
* Enhanced visualization and reporting
* Support for energy storage optimization

**Future Plans (v2.0.0)**:

* Multi-objective optimization
* Advanced machine learning integration
* Cloud-based deployment options
* Real-time monitoring and control
* Integration with SCADA systems

Migration Guide
==============

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