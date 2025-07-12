.. pyeplan documentation master file

PyEPLAN: A Python-based Energy Planning tool
============================================

.. image:: https://img.shields.io/pypi/v/pyeplan.svg
    :target: https://pypi.python.org/pypi/pyeplan
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/l/pyeplan.svg
    :target: License

.. image:: https://img.shields.io/github/stars/SPS-L/pyeplan.svg
    :target: https://github.com/SPS-L/pyeplan
    :alt: GitHub stars

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3894705.svg
   :target: https://doi.org/10.5281/zenodo.3894705


PyEPLAN stands for "Python-based Energy Planning tool". It is a `free software <http://www.gnu.org/philosophy/free-sw.en.html>`_ toolbox for Planning and Operation of Sustainable Micro-grids.

PyEPLAN provides a comprehensive framework for microgrid planning and operation optimization, featuring:

* **Data Processing**: Historical weather data extraction and representative day clustering
* **Network Routing**: Optimal feeder routing using minimum spanning tree algorithms  
* **Investment Planning**: Long-term capacity expansion and technology selection
* **Operation Planning**: Short-term dispatch optimization and cost analysis

The tool supports both on-grid and off-grid microgrid configurations, handles uncertainty through scenario-based optimization, and integrates renewable energy sources with conventional generation and energy storage systems. 

Documentation
=============

**Getting Started**

* :doc:`get_started/introduction`
* :doc:`get_started/installation`
* :doc:`get_started/examples`

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Getting Started

   get_started/introduction
   get_started/installation
   get_started/examples

**User Guide**

* :doc:`user_guide/input`
* :doc:`user_guide/planning`
* :doc:`user_guide/output`

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: User Guide

   user_guide/input
   user_guide/planning
   user_guide/output


**Help & References**

* :doc:`help_ref/release_notes`
* :doc:`help_ref/api_reference`
* :doc:`help_ref/citing`
* :doc:`help_ref/users`
* :doc:`LICENSE`

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: Help & References

   help_ref/release_notes
   help_ref/api_reference
   help_ref/citing
   help_ref/users
   LICENSE.rst
   
.. image:: img/gcrf.jpg
    :width: 200px
    :align: center
    :alt: alternate text
