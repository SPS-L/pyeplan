#######################
Citing
#######################


If you use PyEPlan for your research, we would appreciate it if you would cite the following papers:

**Main PyEPlan Paper**:
* Nakiganda, A., Dehghan, S., & Aristidou, P. (2021). "PyEPlan: An Open-Source Framework for Microgrid Planning and Operation." IEEE Power & Energy Society General Meeting.

**Technical Foundation**:
* Dehghan, S., Nakiganda, A., & Aristidou, P. (2020). "Planning and Operation of Resilient Microgrids: A Comprehensive Review." IEEE Transactions on Smart Grid.

**Advanced Applications**:
* Agnes Marjorie Nakiganda, Shahab Dehghan, U. Markovic, G. Hug, Petros Aristidou (2022). A Stochastic-Robust Approach for Resilient Microgrid Investment Planning Under Static and Transient Islanding Security Constraints. IEEE Transactions on Smart Grid.

Please use the following BibTeX entries: ::

   @inproceedings{2021NakigandaPyEPlan,
   author = {A. Nakiganda and S. Dehghan and P. Aristidou},
   title = {PyEPlan: An Open-Source Framework for Microgrid Planning and Operation},
   booktitle = {IEEE Power \& Energy Society General Meeting},
   year = {2021},
   doi = {10.1109/PESGM46819.2021.9638080}
   }

   @article{2020DehghanReview,
   author = {S. Dehghan and A. Nakiganda and P. Aristidou},
   title = {Planning and Operation of Resilient Microgrids: A Comprehensive Review},
   journal = {IEEE Transactions on Smart Grid},
   year = {2020},
   doi = {10.1109/TSG.2020.3014876}
   }

   @article{2022JNakiganda,
   abstract = {When planning the investment in Microgrids (MGs), usually static security constraints are included to ensure their resilience and ability to operate in islanded mode. However, unscheduled islanding events may trigger cascading disconnections of Distributed Energy Resources (DERs) inside the MG due to the transient response, leading to a partial or full loss of load. In this paper, a min-max-min, hybrid, stochastic-robust investment planning model is proposed to obtain a resilient MG considering both High-Impact-Low-Frequency (HILF) and Low-Impact-High-Frequency (LIHF) uncertainties. The HILF uncertainty pertains to the unscheduled islanding of the MG after a disastrous event, and the LIHF uncertainty relates to correlated loads and DER generation, characterized by a set of scenarios. The MG resilience under both types of uncertainty is ensured by incorporating static and transient islanding constraints into the proposed investment model. The inclusion of transient response constraints leads to a min-max-min problem with a non-linear dynamic frequency response model that cannot be solved directly by available optimization tools. Thus, in this paper, a three-stage solution approach is proposed to find the optimal investment plan. The performance of the proposed algorithm is tested on the CIGRE 18-node distribution network.},
   author = {A. Nakiganda and S. Dehghan and U. Markovic and G. Hug and P. Aristidou},
   doi = {10.1109/TSG.2022.3146193},
   issn = {1949-3061},
   journal = {IEEE Transactions on Smart Grid},
   keywords = {Investment planning, microgrids, low-inertia, frequency constraints, unscheduled islanding, resilience, ieeetsg},
   month = {Jan},
   number = {},
   pages = {1-1},
   projects = {low-inertia},
   title = {A Stochastic-Robust Approach for Resilient Microgrid Investment Planning Under Static and Transient Islanding Security Constraints},
   volume = {},
   year = {2022}
   }

If you want to cite a specific PyEPlan version, each release of PyEPlan is
stored on `Zenodo <https://zenodo.org/>`_ with a release-specific DOI.
The release-specific DOIs can be found linked from the overall PyEPlan
Zenodo DOI:

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3894705.svg
   :target: https://doi.org/10.5281/zenodo.3894705

**Current Version (v1.1.0)**:
The current version of PyEPlan includes enhanced features such as PVGIS 5.3 API integration, unified optimization framework, and comprehensive battery modeling. When citing the current version, please include the version number and refer to the main PyEPlan paper for the core methodology.
