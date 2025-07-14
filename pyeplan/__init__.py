#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PyEPlan: Python library for planning and operation of resilient microgrids.

PyEPlan is a comprehensive Python library designed for the planning and operation
of resilient microgrids. It provides tools for data processing, network routing,
and investment/operation optimization of microgrid systems.

The library consists of three main modules:

1. **datsys** (dataproc.py): Data processing and renewable energy resource assessment
   - Fetches solar irradiance and wind speed data from PVGIS API
   - Performs time series clustering using K-means algorithm
   - Processes load profiles and renewable generation data
   - Handles timezone conversion and data preprocessing

2. **rousys** (routing.py): Network routing and topology optimization
   - Implements minimum spanning tree algorithm for network design
   - Calculates geographical distances between nodes
   - Generates network topology and cable specifications
   - Creates routing and electrical line distribution files

3. **inosys** (investoper.py): Investment and operation optimization
   - Formulates and solves mixed-integer linear programming problems
   - Optimizes microgrid investment decisions (generators, storage, renewables)
   - Handles operational constraints (power balance, voltage limits, etc.)
   - Supports multiple solvers (GLPK, CBC, IPOPT, Gurobi)

Key Features:
- Integration with PVGIS for renewable energy data
- Geographic information system (GIS) capabilities
- Multi-objective optimization (cost, reliability, sustainability)
- Support for various renewable energy technologies
- Battery energy storage system modeling
- Network topology optimization

References:
- Dehghan, S., Nakiganda, A., & Aristidou, P. (2020). "Planning and Operation of 
  Resilient Microgrids: A Comprehensive Review." IEEE Transactions on Smart Grid.
- Nakiganda, A., Dehghan, S., & Aristidou, P. (2021). "PyEPlan: An Open-Source 
  Framework for Microgrid Planning and Operation." IEEE Power & Energy Society 
  General Meeting.

Example Usage:
    >>> import pyeplan
    >>> 
    >>> # Data processing
    >>> data_sys = pyeplan.datsys("input_folder", lat=0.25, lon=32.40, year=2016)
    >>> data_sys.data_extract()
    >>> data_sys.kmeans_clust()
    >>> 
    >>> # Network routing
    >>> route_sys = pyeplan.rousys("input_folder", crs=35, typ=7, vbase=415)
    >>> route_sys.min_spn_tre()
    >>> 
    >>> # Investment and operation optimization
    >>> inv_sys = pyeplan.inosys("input_folder", ref_bus=0)
    >>> inv_sys.solve(solver='glpk', invest=True, onlyopr=False)
"""

__name__ = "pyeplan"
__version__ = '1.1.1'
__author__ = u'2025 Shahab Dehghan, Agnes Nakiganda, Petros Aristidou'
__copyright__ = u'2025 Shahab Dehghan, Agnes Nakiganda, Petros Aristidou'
__license__ ='Apache Software License',
__maintainer__ = "s.dehghan@ieee.org"
__email__ = "s.dehghan@ieee.org"
__url__ = "https://pyeplan.sps-lab.org/"
__status__ = "5 - Production/Stable"


from .investoper import inosys
from .routing import rousys
from .dataproc import datsys

__all__ = ['inosys', 'rousys', 'datsys']
