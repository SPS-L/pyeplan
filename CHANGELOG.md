# Changelog

All notable changes to PyEPlan will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Version management automation with bump2version
- Custom version bumping script
- Comprehensive contributing guidelines
- Automated git tagging and release process

### Changed
- Updated contributing documentation with version management guidelines
- Enhanced development workflow documentation

## [1.1.1] - 2025-01-XX

### Added
- Initial release of PyEPlan package
- Data processing module (datsys) for renewable energy resource assessment
- Network routing module (rousys) for topology optimization
- Investment and operation optimization module (inosys)
- PVGIS API integration for solar and wind data
- K-means clustering for time series analysis
- Minimum spanning tree algorithm for network design
- Mixed-integer linear programming optimization
- Support for multiple solvers (GLPK, CBC, IPOPT, Gurobi)
- Geographic information system (GIS) capabilities
- Battery energy storage system modeling
- Multi-objective optimization (cost, reliability, sustainability)

### Features
- Solar irradiance and wind speed data fetching from PVGIS API
- Time series clustering using K-means algorithm
- Load profile and renewable generation data processing
- Timezone conversion and data preprocessing
- Network topology and cable specifications generation
- Routing and electrical line distribution file creation
- Microgrid investment decision optimization
- Operational constraints handling (power balance, voltage limits)
- Support for various renewable energy technologies

### Documentation
- Comprehensive API documentation
- User guide with examples
- Installation and setup instructions
- Jupyter notebook examples
- Case studies and tutorials

### Examples
- 1-bus microgrid planning example
- 5-bus microgrid planning example
- Solar home system (SHS) planning example
- Watoto Village case study

## [1.0.0] - 2024-XX-XX

### Added
- Initial development version
- Core functionality implementation
- Basic documentation structure

---

## Version History

- **1.1.1**: First stable release with full functionality
- **1.0.0**: Initial development version

## Release Types

- **MAJOR**: Breaking changes, incompatible API changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

## Contributing

When adding entries to this changelog, please follow these guidelines:

1. **Added**: New features
2. **Changed**: Changes in existing functionality
3. **Deprecated**: Soon-to-be removed features
4. **Removed**: Removed features
5. **Fixed**: Bug fixes
6. **Security**: Vulnerability fixes

Each change should be concise and descriptive. 