##########################################
 Introduction
##########################################

**PyEPLAN** is an open-source **Py**-thon-based **E**-nergy **Plan**-ning tool for design and operation of optimised microgrid networks.

Functionality
=============


**PyEPLAN has four main modules:**

* Data Processor
The data processor in PyEPLAN is customised to find representative days, characterising daily profiles of load demands and power generations of renewable energy sources by applying machine learning algorithms such as K-means and Hierachical clustering. The representative days are used as operation scenarios providing the input data needed for the investment/operation planning modules.

* Feeder Routing
This module finds the least cost network design given the geographical distances between nodes, technical line parameters and cost of the different line types.

* Investment Planning
This module aims to minimise both investment costs during a long-term planning horizon (i.e., from one year to several years) under both investment and operation related techno-economic constraints

* Operation Planning
This module aims to minimise operation costs during a short-term planning horizon (i.e., one day, hourly) under operation related techno-economic constraints. 

What PyEPLAN uses under the hood
================================

It depends heavily on the following Python packages:

* `pandas <http://pandas.pydata.org/>`_ for storing data about components and time series
* `numpy <http://www.numpy.org/>`_ and `scipy <http://scipy.org/>`_ for 
* `pyomo <http://www.pyomo.org/>`_ for preparing optimisation problems
* `matplotlib <https://matplotlib.org/>`_ for 
* `networkx <https://networkx.github.io/>`_ 


Other comparable software
=========================

* ...
* ...



Target user group
=================

PyEPLAN is intended for researchers, planners ...



Licence
=======

PyEPLAN is released under the `Apache License 2.0 <https://www.apache.org/licenses/LICENSE-2.0>`_.
