################
 Installation
################


Getting Python
==============

If it's your first time with Python, we recommend `Anaconda <https://www.continuum.io/downloads>`_ as an easy-to-use environment that includes many basic packages. Anaconda is available
for Windows, Mac OS X and GNU/Linux.

PyEPlan requires Python 3.8 or higher.

Getting a solver for linear optimisation
========================================

PyEPlan works with the free software:

- `Cbc <https://projects.coin-or.org/Cbc#DownloadandInstall>`_
- `GLPK <https://www.gnu.org/software/glpk/>`_ (`WinGLKP <http://winglpk.sourceforge.net/>`_)
- `IPOPT <https://coin-or.github.io/Ipopt/>`_

and the commercial software:

- `Gurobi <https://www.gurobi.com/documentation/quickstart.html>`_
- `CPLEX <https://www.ibm.com/products/ilog-cplex-optimization-studio>`_
- `MOSEK <https://www.mosek.com/>`_

For installation instructions of these solvers for your operating system, follow the links above.

Depending on your operating system, you can also install some of the open-source solvers in a ``conda`` environment.

For GLPK on all operating systems::

    conda install -c conda-forge glpk

For CBC on all operating systems except for Windows::

    conda install -c conda-forge coincbc

For IPOPT on all operating systems::

    conda install -c conda-forge ipopt

.. note::
    Commercial solvers such as Gurobi, CPLEX, and MOSEK currently significantly outperform open-source solvers for large-scale problems.
    It might be the case that you can only retrieve solutions by using a commercial solver.


Installing PyEPlan
==================

If you have the Python package installer ``pip`` then just run::

    pip install pyeplan

If you're feeling adventurous, you can also install the latest master branch from github with::

    pip install git+https://github.com/SPS-L/pyeplan.git

For development installation::

    git clone https://github.com/SPS-L/pyeplan.git
    cd pyeplan
    pip install -e .

Dependencies
============

PyEPlan has the following key dependencies:

**Core Dependencies**:
- `pandas <http://pandas.pydata.org/>`_ - Data manipulation and analysis
- `numpy <http://www.numpy.org/>`_ - Numerical computations
- `pyomo <http://www.pyomo.org/>`_ - Mathematical optimization modeling
- `scikit-learn <https://scikit-learn.org/>`_ - Machine learning and clustering
- `networkx <https://networkx.github.io/>`_ - Graph algorithms and network analysis
- `matplotlib <https://matplotlib.org/>`_ - Data visualization
- `openpyxl <https://openpyxl.readthedocs.io/>`_ - Excel file handling
- `timezonefinder <https://github.com/MrMinimal64/timezonefinder>`_ - Geographic timezone calculations

**Optional Dependencies**:
- `folium <https://python-visualization.github.io/folium/>`_ - Interactive map visualization
- `scipy <http://scipy.org/>`_ - Scientific computing (for advanced features)

All dependencies are automatically installed when using pip.


.. _upgrading-pyeplan:

Upgrading PyEPlan
=================

To upgrade pyeplan with pip, do at the command line::

    pip install -U pyeplan

Don't forget to read the :doc:`../help_ref/release_notes` regarding API changes
that might require you to update your code.

Verifying Installation
======================

To verify that PyEPlan is installed correctly, run the following in Python::

    import pyeplan
    print(pyeplan.__version__)
    
    # Test basic functionality
    from pyeplan import datsys, rousys, inosys
    print("PyEPlan modules imported successfully!")

If you encounter any issues, please check the troubleshooting section or report the problem on the GitHub repository.
