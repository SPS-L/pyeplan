################
 Examples
################

PyEPlan provides comprehensive examples demonstrating various use cases and applications. These examples are available in the `PyEPlan github repository <https://github.com/SPS-L/PyEPlan>`_.

Available Examples
==================

**1. Single Bus Microgrid Planning**
   - Location: `examples/1_bus/`
   - Description: Basic microgrid planning for a single bus system
   - Demonstrates: Data processing (datsys), investment planning, and operation optimization (inosys)

**2. Five Bus Microgrid System**
   - Location: `examples/5_bus/`
   - Description: Multi-bus microgrid planning with network considerations
   - Demonstrates: Network routing (rousys), multi-bus optimization, and system integration

**3. Watoto Village Case Study**
   - Location: `examples/wat_inv/`
   - Description: Real-world case study of rural electrification
   - Demonstrates: Practical application in developing regions

**4. Jupyter Notebook Examples**
   - `5_bus_MG_Planning_Example.ipynb`: Interactive tutorial for 5-bus system
   - `SHS_Planning_Example.ipynb`: Solar Home System planning example
   - `Watoto_Village_Case_Study.ipynb`: Detailed case study analysis

Getting Started with Examples
============================

1. **Clone the repository**::

    git clone https://github.com/SPS-L/pyeplan.git
    cd pyeplan


2. **Install PyEPlan**::

    pip install -e .


3. **Run Jupyter notebooks**::

    jupyter notebook examples/


4. **Explore the data files** in each example directory to understand the input format and requirements.

Example Workflow
===============

A typical PyEPlan workflow involves:

1. **Data Preparation**: Use the Data Processing module (datsys) to extract weather data from PVGIS API and create representative days using K-means clustering
2. **Network Design**: Use the Routing module (rousys) to design optimal feeder connections using minimum spanning tree algorithm
3. **Investment & Operation Optimization**: Use the Investment & Operation module (inosys) to optimize technology selection, sizing, and dispatch using mixed-integer linear programming

Each example demonstrates different aspects of this workflow, from simple single-bus systems to complex multi-bus networks with real-world constraints.

Basic Usage Example
==================

Here's a simple example showing the basic workflow:

.. code-block:: python

    import pyeplan
    
    # 1. Data Processing
    data_sys = pyeplan.datsys(
        inp_folder="examples/1_bus/",
        lat=0.25,
        lon=32.40,
        year=2016,
        n_clust=5
    )
    data_sys.data_extract()  # Extract data from PVGIS
    data_sys.kmeans_clust()  # Create representative days
    
    # 2. Network Routing (for multi-bus systems)
    route_sys = pyeplan.rousys(
        inp_folder="examples/5_bus/",
        crs=35,
        typ=7,
        vbase=415
    )
    route_sys.min_spn_tre()  # Generate optimal network topology
    
    # 3. Investment and Operation Optimization
    inv_sys = pyeplan.inosys(
        inp_folder="examples/1_bus/",
        ref_bus=0,
        dshed_cost=1000000,
        rshed_cost=500
    )
    inv_sys.solve(solver='glpk', invest=True, onlyopr=False)
    
    # 4. Get Results
    costs = inv_sys.resCost()
    wind_results = inv_sys.resWind()
    battery_results = inv_sys.resBat()

