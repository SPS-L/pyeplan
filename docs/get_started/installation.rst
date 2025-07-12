################
 Installation
################


Getting Python
==============

If it's your first time with Python, we recommend `Anaconda <https://www.continuum.io/downloads>`_ as an easy-to-use environment that includes many basic packages. Anaconda is available
for Windows, Mac OS X and GNU/Linux.


Getting a solver for linear optimisation
========================================

PyEPLAN works with the free software:

- `Cbc <https://projects.coin-or.org/Cbc#DownloadandInstall>`_
- `GLPK <https://www.gnu.org/software/glpk/>`_ (`WinGLKP <http://winglpk.sourceforge.net/>`_)

and the commercial software:

- `Gurobi <https://www.gurobi.com/documentation/quickstart.html>`_
- `CPLEX <https://www.ibm.com/products/ilog-cplex-optimization-studio>`_
- `FICO Xpress <https://www.fico.com/en/products/fico-xpress-optimization>`_

For installation instructions of these solvers for your operating system, follow the links above.

Depending on your operating system, you can also install some of the open-source solvers in a ``conda`` environment.

For GLPK on all operating systems::

    conda install -c conda-forge glpk

For CBC on all operating systems except for Windows::

    conda install -c conda-forge coincbc

.. note::
    Commercial solvers such as Gurobi, CPLEX, and Xpress currently significantly outperform open-source solvers for large-scale problems.
    It might be the case that you can only retrieve solutions by using a commercial solver.


Installing PyEPLAN
==================

If you have the Python package installer ``pip`` then just run::

    pip install pyeplan

If you're feeling adventurous, you can also install the latest master branch from github with::

    pip install git+https://github.com/SPS-L/pyeplan.git


.. _upgrading-pyeplan:

Upgrading PyEPLAN
=================

To upgrade pyeplan with pip, do at the command line::

    pip install -U pyeplan

Don't forget to read the :doc:`../help_ref/release_notes` regarding API changes
that might require you to update your code.
