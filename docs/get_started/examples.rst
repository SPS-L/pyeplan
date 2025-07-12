################
 Examples
################

PyEPLAN provides comprehensive examples demonstrating various use cases and applications. These examples are available in the `PyEPLAN github repository <https://github.com/SPS-L/PyEPLAN>`_.

Available Examples
==================

**1. Single Bus Microgrid Planning**
   - Location: `examples/1_bus/`
   - Description: Basic microgrid planning for a single bus system
   - Demonstrates: Data processing, investment planning, and operation optimization

**2. Five Bus Microgrid System**
   - Location: `examples/5_bus/`
   - Description: Multi-bus microgrid planning with network considerations
   - Demonstrates: Network routing, multi-bus optimization, and system integration

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

1. **Clone the repository**:

    git clone https://github.com/SPS-L/pyeplan.git
    cd pyeplan


2. **Install PyEPLAN**:

    pip install -e .


3. **Run Jupyter notebooks**:

    jupyter notebook examples/


4. **Explore the data files** in each example directory to understand the input format and requirements.

Example Workflow
===============

A typical PyEPLAN workflow involves:

1. **Data Preparation**: Use the Data Processor to extract weather data and create representative days
2. **Network Design**: Use the Routing module to design optimal feeder connections
3. **Investment Planning**: Optimize technology selection and sizing for long-term planning
4. **Operation Analysis**: Analyze short-term operation costs and system performance

Each example demonstrates different aspects of this workflow, from simple single-bus systems to complex multi-bus networks with real-world constraints.

