##########################################
 Introduction
##########################################

**PyEPLAN** is an open-source **Py**-thon-based **E**-nergy **Plan**-ning tool for design and operation of optimized microgrid networks. It supports functions ranging from renewable generation profile creation, network layout design to optimization of design and operation costs for microgrids packaged in four modules. Used independently and/or jointly, the different packages provide the user with detailed analysis of short and long-term costs and benefits of different generation resources and impacts of their characteristics on system operation. The tool is customizable allowing users to neglect or input desired network characteristics, choose from a pool of generation sources both renewable and non-renewable, etc.

PyEPLAN addresses the growing need for sustainable energy solutions in developing regions and remote communities by providing a comprehensive framework for microgrid planning and operation. The tool incorporates advanced optimization techniques and machine learning algorithms to handle the inherent uncertainty in renewable energy generation and load demand patterns.

The initial development of the tool was funded under the UKRI GCRF project `CRESUM-HYRES <https://cera.leeds.ac.uk/cresum-hyres/>`_ at the `University of Leeds <https://leeds.ac.uk/>`_, but is now supported and co-developed by people in different universities (such as `CUT <https://sps.cut.ac.cy>`_, `ICL <https://www.imperial.ac.uk/>`_).

In the next sections detailed information on fuctionality of each supported module, installation and usage is provided.


     

Functionality
=============

The functions available in PyEPLAN are packaged into four key modules that can be utilized independently or simultaneously:

.. image:: PyEPLAN_architecture.png

**Data Processor**

The Data Processor module supports two main functionalities:

* **Historical Data Extraction**: It extracts historical data on wind speed and solar radiation based on user-provided coordinates of the generation source location from openly available satellite information and creates 24-hour daily profiles for the given period of time. This data is sourced from NASA's POWER project and other meteorological databases.

* **Representative Day Clustering**: It finds representative days based on daily profiles of load demands and power generations of renewable energy sources by applying machine learning algorithms such as K-means and Hierarchical clustering. The representative days are used as operation scenarios providing the input data needed for the investment/operation planning modules, significantly reducing computational complexity while maintaining solution accuracy.

**Feeder Routing**

The Feeder Routing module finds the least cost network design given the geographical distances between nodes, technical line parameters and cost of the different line types. It takes user map coordinates of the node or load point locations and provides an optimal system layout using the minimum spanning tree algorithm. The module considers:

* **Geographic Constraints**: Real-world terrain and accessibility factors
* **Technical Parameters**: Line resistance, reactance, and current carrying capacity
* **Economic Factors**: Capital costs for different cable types and installation
* **Network Topology**: Radial or meshed network configurations

**Investment Planning**

This module aims to minimize both investment costs during a long-term planning horizon (i.e., from one year to several years) under both investment and operation related techno-economic constraints. Capabilities include:

* **Optimal Technology Sizing**: Determination of optimal capacity for renewable generators, energy storage, and conventional units
* **Optimal Siting**: Geographic placement of generation and storage facilities
* **Cost Analysis**: Capital and operation costs predictions with detailed financial modeling
* **Grid Integration**: On-grid and off-grid modeling capabilities
* **Uncertainty Handling**: Scenario-based optimization considering weather variability and load uncertainty

The investment planning module requires network characteristics (i.e., candidate/existing lines) as well as long-term/short-term estimated/forecasted load demands and power generations of RESs to obtain the optimal solution. The former can be user defined or obtained from the Feeder Routing module, and the latter can be user defined or obtained from the Data Processor module.

**Operation Planning**

This module aims to minimize operation costs during a short-term planning horizon (i.e., one day, hourly) under operation related techno-economic constraints. This module can be used independently or synchronously with the investment planning module. Capabilities include:

* **Adequacy Analysis**: Assessment of system reliability and capacity adequacy for both on-grid and off-grid configurations
* **Security Analysis**: Evaluation of system security under various operating conditions and contingencies
* **Operation Costs Analysis**: Detailed breakdown of operational expenses including fuel costs, maintenance, and grid exchange costs
* **Real-time Dispatch**: Optimal unit commitment and economic dispatch considering technical constraints
* **Reserve Management**: Spinning and non-spinning reserve allocation for system reliability

Since both investment and operation planning modules include various optimisation problems, the open-source, Python-based, optimisation modelling module `Pyomo <http://www.pyomo.org/>`_ is used with diverse abilities in formulating, solving, and analysing optimisation problems. Additionally, PyEPLAN can utilise a broad range of solvers both open-source and commercial as supported by Pyomo, to obtain the optimal solution in both investment and operation planning modules.

What PyEPLAN uses under the hood
================================

PyEPLAN is built on a robust foundation of scientific Python packages:

* `pandas <http://pandas.pydata.org/>`_ for data manipulation and time series analysis
* `numpy <http://www.numpy.org/>`_ and `scipy <http://scipy.org/>`_ for numerical computations and optimization algorithms
* `pyomo <http://www.pyomo.org/>`_ for mathematical optimization modeling and problem formulation
* `matplotlib <https://matplotlib.org/>`_ for data visualization and plotting
* `networkx <https://networkx.github.io/>`_ for graph algorithms and network analysis
* `scikit-learn <https://scikit-learn.org/>`_ for machine learning and clustering algorithms
* `openpyxl <https://openpyxl.readthedocs.io/>`_ for Excel file handling
* `timezonefinder <https://github.com/MrMinimal64/timezonefinder>`_ for geographic timezone calculations 


Other comparable software
=========================

* HOMER Energy
* RETScreen



Target user group
=================

PyEPLAN is a tool intended for researchers, planners and students aiming at the creation and operation of cost-optimised resilient and sustainable microgrid networks.



Licence
=======

PyEPLAN is released under the `Apache License 2.0 <https://www.apache.org/licenses/LICENSE-2.0>`_.
