# PyEPlan: A Python-based Energy Planning tool

[![PyPI version](https://img.shields.io/pypi/v/pyeplan.svg)](https://pypi.python.org/pypi/pyeplan) [![image](https://img.shields.io/github/license/SPS-L/pyeplan)](LICENSE.txt) [![image](https://zenodo.org/badge/DOI/10.5281/zenodo.3894705.svg)](https://doi.org/10.5281/zenodo.3894705)

PyEPlan is a [free software](http://www.gnu.org/philosophy/free-sw.en.html) toolbox for designing resilient mini-grids in developing countries. The initial development was funded under the UKRI GCRF project [CRESUM-HYRES](https://cera.leeds.ac.uk/cresum-hyres/) at the [University of Leeds](https://leeds.ac.uk/), but is now supported and co-developed by people in different universities (such as [CUT](https://sps.cut.ac.cy), [ICL](https://www.imperial.ac.uk/)).

## Overview

PyEPlan is a comprehensive Python library designed for the planning and operation of resilient microgrids. It provides tools for data processing, network routing, and investment/operation optimization of microgrid systems, with particular focus on applications in developing countries and rural electrification projects.

## Key Features

- **Data Processing & Resource Assessment**: Integration with PVGIS API for solar irradiance and wind speed data
- **Network Topology Optimization**: Minimum spanning tree algorithms for optimal network design
- **Investment & Operation Optimization**: Mixed-integer linear programming for microgrid planning
- **Multi-Objective Optimization**: Cost, reliability, and sustainability optimization
- **Geographic Information System**: GIS capabilities for location-based planning
- **Battery Energy Storage**: Comprehensive modeling of energy storage systems
- **Renewable Energy Integration**: Support for solar PV, wind turbines, and hybrid systems
- **Multiple Solver Support**: GLPK, CBC, IPOPT, Gurobi optimization solvers

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Create Virtual Environment (Recommended)

#### Using venv (Python's built-in virtual environment)

```bash
# Create virtual environment
python -m venv pyeplan_env

# Activate virtual environment
# On Windows:
pyeplan_env\Scripts\activate
# On macOS/Linux:
source pyeplan_env/bin/activate
```

#### Using conda (Alternative)

```bash
# Create conda environment
conda create -n pyeplan_env python=3.9

# Activate conda environment
conda activate pyeplan_env
```

### From PyPI (Recommended)

```bash
pip install pyeplan
```

### From Source

```bash
git clone https://github.com/SPS-L/pyeplan.git
cd pyeplan
pip install -e .
```

### Dependencies

PyEPlan requires the following Python packages:
- pandas
- numpy
- networkx
- matplotlib
- pyomo
- timezonefinder
- scikit-learn
- mplleaflet

These will be automatically installed when installing PyEPlan.

### Optimization Solvers

PyEPlan supports multiple optimization solvers. For basic usage, GLPK (GNU Linear Programming Kit) is recommended:

#### Installing GLPK

**Windows:**
```bash
# Using conda (recommended)
conda install -c defaults -c conda-forge glpk

# Using winget
winget install GnuWin32.GLPK

# Manual installation
# Download from https://www.gnu.org/software/glpk/
```

**macOS:**
```bash
# Using Homebrew
brew install glpk

# Using conda
conda install -c defaults -c conda-forge glpk
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install glpk-utils libglpk-dev
```

**Linux (CentOS/RHEL/Fedora):**
```bash
# CentOS/RHEL
sudo yum install glpk glpk-devel

# Fedora
sudo dnf install glpk glpk-devel
```

#### Alternative Solvers

PyEPlan also supports:

**CBC (COIN-OR Branch and Cut):**
```bash
# Using conda (recommended)
conda install -c defaults -c conda-forge coin-or-cbc

# Using pip
pip install cylp

# Manual installation
# Download from https://github.com/coin-or/Cbc/releases
```

**IPOPT (Interior Point Optimizer):**
```bash
# Using conda
conda install -c defaults -c conda-forge ipopt

# Using pip
pip install ipopt
```

**Gurobi:**
Commercial solver, requires license. Download from [Gurobi website](https://www.gurobi.com/downloads/).

For solver-specific installation instructions, see the [Pyomo documentation](https://pyomo.readthedocs.io/en/stable/installation.html).

## Quick Start

### Basic Usage

```python
import pyeplan

# 1. Data Processing
data_sys = pyeplan.datsys("input_folder", lat=0.25, lon=32.40, year=2016)
data_sys.data_extract()
data_sys.kmeans_clust()

# 2. Network Routing
route_sys = pyeplan.rousys("input_folder", crs=35, typ=7, vbase=415)
route_sys.min_spn_tre()

# 3. Investment and Operation Optimization
inv_sys = pyeplan.inosys("input_folder", ref_bus=0)
inv_sys.solve(solver='glpk', invest=True, onlyopr=False)

# 4. View Results
inv_sys.resCost()
inv_sys.resSolar()
inv_sys.resWind()
inv_sys.resBat()
```

### Input Data Structure

PyEPlan requires specific CSV files in your input folder:

**Required Files:**
- `mgpc_dist.xlsx`: Load point and load level data
- `cgen_dist.csv`: Conventional generator candidate data
- `egen_dist.csv`: Existing conventional generator data
- `csol_dist.csv`: Solar PV candidate data
- `esol_dist.csv`: Existing solar PV data
- `cwin_dist.csv`: Wind turbine candidate data
- `ewin_dist.csv`: Existing wind turbine data
- `cbat_dist.csv`: Battery storage candidate data
- `elin_dist.csv`: Electrical line data
- `pdem_dist.csv`: Active power demand profiles
- `qdem_dist.csv`: Reactive power demand profiles
- `psol_dist.csv`: Solar power scenarios
- `pwin_dist.csv`: Wind power scenarios
- `dtim_dist.csv`: Time duration for each scenario

## Core Modules

### 1. Data Processing (`datsys`)

Handles renewable energy resource assessment and data preprocessing:

```python
from pyeplan.dataproc import datsys

# Initialize data processing system
data_sys = datsys(
    inp_folder="input_folder",
    lat=0.25,           # Latitude in decimal degrees
    lon=32.40,          # Longitude in decimal degrees
    year=2016,          # Year for data collection
    pvcalc=1,           # PV calculation method (0=radiation, 1=power+radiation)
    pp=50,              # Nominal power of PV system in kW
    n_clust=5,          # Number of clusters for time series
    sbase=1000          # Base apparent power in kW
)

# Extract and process time series data
data_sys.data_extract()

# Perform K-means clustering for scenario reduction
data_sys.kmeans_clust()
```

### 2. Network Routing (`rousys`)

Implements network topology optimization using minimum spanning tree algorithms:

```python
from pyeplan.routing import rousys

# Initialize routing system
route_sys = rousys(
    inp_folder="input_folder",
    crs=35,             # Cross section of cables in mm²
    typ=7,              # Type of cables
    vbase=415,          # Line-to-line voltage in V
    sbase=1             # Base apparent power in kW
)

# Generate minimum spanning tree network topology
route_sys.min_spn_tre()
```

### 3. Investment & Operation Optimization (`inosys`)

Formulates and solves mixed-integer linear programming problems:

```python
from pyeplan.investoper import inosys

# Initialize optimization system
inv_sys = inosys(
    inp_folder="input_folder",
    ref_bus=0,          # Reference bus number
    dshed_cost=1000000, # Demand shedding cost
    rshed_cost=500,     # Renewable shedding cost
    vmin=0.85,          # Minimum voltage limit
    vmax=1.15,          # Maximum voltage limit
    sbase=1             # Base apparent power in kW
)

# Solve optimization problem
inv_sys.solve(
    solver='glpk',      # Optimization solver
    invest=True,        # Include investment decisions
    onlyopr=False       # Solve both investment and operation
)

# View results
inv_sys.resCost()       # Total costs
inv_sys.resSolar()      # Solar investment results
inv_sys.resWind()       # Wind investment results
inv_sys.resBat()        # Battery investment results
inv_sys.resConv()       # Conventional generator results
inv_sys.resCurt()       # Curtailment results
```

## Mathematical Formulation

The optimization problem minimizes total system cost:

```
min Z = C_inv + C_opr + C_shed
```

Subject to constraints:
- Power balance constraints (active and reactive)
- Generator capacity limits
- Battery storage constraints
- Network flow constraints
- Voltage limits
- Investment constraints

Where:
- `C_inv`: Investment costs (generators, storage, renewables)
- `C_opr`: Operational costs (fuel, maintenance, etc.)
- `C_shed`: Penalty costs for demand shedding and curtailment

## Examples

### Example 1: 5-Bus Microgrid Planning

```python
import pyeplan

# Complete microgrid planning workflow
data_sys = pyeplan.datsys("examples/5_bus/", lat=0.25, lon=32.40, year=2016)
data_sys.data_extract()
data_sys.kmeans_clust()

route_sys = pyeplan.rousys("examples/5_bus/", crs=35, typ=7, vbase=415)
route_sys.min_spn_tre()

inv_sys = pyeplan.inosys("examples/5_bus/", ref_bus=0)
inv_sys.solve(solver='glpk', invest=True, onlyopr=False)
inv_sys.resCost()
```

### Example 2: Standalone Hybrid System

```python
import pyeplan

# SHS (Standalone Hybrid System) planning
data_sys = pyeplan.datsys("examples/wat_inv/", lat=0.25, lon=32.40, year=2016)
data_sys.data_extract()
data_sys.kmeans_clust()

inv_sys = pyeplan.inosys("examples/wat_inv/", ref_bus=0)
inv_sys.solve(solver='glpk', invest=True, onlyopr=False)
inv_sys.resSolar()
inv_sys.resBat()
```

## Output Files

PyEPlan generates comprehensive output files in the `results/` directory:

**Investment Results:**
- `xg.csv`: Conventional generator investments
- `xs.csv`: Solar PV investments
- `xw.csv`: Wind turbine investments
- `xb.csv`: Battery storage investments

**Operational Results:**
- `pcg.csv`, `qcg.csv`: Conventional generator operation
- `pcs.csv`, `qcs.csv`: Solar PV operation
- `pcw.csv`, `qcw.csv`: Wind turbine operation
- `pbc.csv`, `pbd.csv`: Battery charging/discharging
- `vol.csv`: Bus voltages
- `pel.csv`, `qel.csv`: Line flows

**Cost Results:**
- `obj.csv`: Total cost breakdown

## Documentation

- **API Reference**: [https://pyeplan.sps-lab.org/](https://pyeplan.sps-lab.org/)
- **User Guide**: Available in the `docs/` directory
- **Examples**: Jupyter notebooks in the `examples/` directory

## Testing

PyEPlan includes comprehensive unit tests covering all major functionality. The test suite ensures code quality and reliability.

### Test Structure

The tests are organized in the `tests/` directory:

- **`test_dataproc.py`**: Data processing module tests (353 lines)
  - PVGIS API integration
  - Time series clustering
  - Data preprocessing and file generation
  - Power factor calculations
  - Timezone handling

- **`test_routing.py`**: Network routing module tests (385 lines)
  - Minimum spanning tree algorithm
  - Geographic distance calculations
  - Cable parameter calculations
  - Network topology generation

- **`test_investoper.py`**: Investment/operation optimization tests (626 lines)
  - Model initialization and data loading
  - Optimization problem formulation
  - Solver integration
  - Result processing and output generation

- **`test_pyeplan_integration.py`**: Integration tests (539 lines)
  - End-to-end workflows
  - Module interactions
  - Real-world example scenarios
  - Error handling and edge cases

### Running Tests

#### Prerequisites

```bash
# Install test dependencies
pip install -r requirements.txt
```

#### Quick Test Run

```bash
# Run all tests
python tests/run_tests.py

# Run with verbose output
python tests/run_tests.py --verbose

# Run specific test module
python tests/run_tests.py --module test_dataproc

# List available test modules
python tests/run_tests.py --list
```

#### Using unittest directly

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_dataproc

# Run specific test class
python -m unittest tests.test_dataproc.TestDatsys

# Run specific test method
python -m unittest tests.test_dataproc.TestDatsys.test_init_basic_parameters
```

#### Using pytest (recommended)

```bash
# Install pytest
pip install pytest

# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_dataproc.py

# Run tests matching pattern
pytest tests/ -k "test_init"
```

### Test Coverage

The test suite covers:

✅ **Data Processing Module**
- Initialization with various parameters
- PVGIS API integration (mocked)
- Time series data extraction and clustering
- File generation and output validation
- Error handling for invalid inputs

✅ **Network Routing Module**
- Cable parameter calculations
- Minimum spanning tree generation
- Geographic distance calculations
- Network topology validation

✅ **Investment/Operation Module**
- Model initialization and data loading
- Optimization problem formulation (mocked)
- Result processing and output generation
- Utility functions

✅ **Integration Tests**
- Complete workflow testing
- Module interaction testing
- Real example data processing
- Error handling and edge cases

### Mocking Strategy

Tests use mocking to ensure reliability:
- **PVGIS API**: Mocked to avoid network calls
- **Optimization Solvers**: Mocked to avoid solver dependencies
- **File System**: Uses temporary directories
- **Network Operations**: Mocked where appropriate

### Continuous Integration

Tests are designed for CI/CD environments:
- No external network dependencies
- No external solver dependencies
- Fast execution with minimal data processing
- Clear pass/fail criteria

For detailed testing information, see [tests/README.md](tests/README.md).

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## Citation

If you use PyEPlan in your research, please cite:

```bibtex
@software{pyeplan2020,
  title={PyEPlan: A Python-based Energy Planning tool},
  author={Dehghan, Shahab and Nakiganda, Agnes and Aristidou, Petros},
  year={2020},
  url={https://github.com/SPS-L/pyeplan},
  doi={10.5281/zenodo.3894705}
}
```

## References

- Dehghan, S., Nakiganda, A., & Aristidou, P. (2020). "Planning and Operation of Resilient Microgrids: A Comprehensive Review." IEEE Transactions on Smart Grid.
- Nakiganda, A., Dehghan, S., & Aristidou, P. (2021). "PyEPlan: An Open-Source Framework for Microgrid Planning and Operation." IEEE Power & Energy Society General Meeting.

## License

This project is licensed under the Apache Software License - see the [LICENSE.txt](LICENSE.txt) file for details.

## Support

- **Email**: s.dehghan@ieee.org
- **Website**: [https://pyeplan.sps-lab.org/](https://pyeplan.sps-lab.org/)
- **GitHub Issues**: [https://github.com/SPS-L/pyeplan/issues](https://github.com/SPS-L/pyeplan/issues)

## Acknowledgments

- UKRI GCRF project [CRESUM-HYRES](https://cera.leeds.ac.uk/cresum-hyres/)
- [University of Leeds](https://leeds.ac.uk/)
- [Cyprus University of Technology](https://sps.cut.ac.cy)
