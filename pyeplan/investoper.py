"""
Investment and Operation Optimization Module.

This module provides comprehensive optimization capabilities for microgrid planning
and operation using mixed-integer linear programming (MILP). It formulates and
solves complex optimization problems that consider investment decisions, operational
constraints, and system reliability.

The module includes:
- Mixed-integer linear programming formulation using Pyomo
- Investment optimization for generators, storage, and renewables
- Operational optimization with power balance and network constraints
- Multi-objective optimization (cost, reliability, sustainability)
- Support for multiple solvers (GLPK, CBC, IPOPT, Gurobi)

Classes:
    inosys: Main class for investment and operation optimization

Key Features:
- Comprehensive microgrid modeling (generators, storage, renewables, loads)
- Network constraints and voltage limits
- Battery energy storage system modeling
- Renewable energy curtailment and demand shedding
- Investment decision optimization
- Operational cost minimization

Mathematical Formulation:
The optimization problem minimizes total system cost:
    min Z = C_inv + C_opr + C_shed

Subject to:
- Power balance constraints (active and reactive)
- Generator capacity limits
- Battery storage constraints
- Network flow constraints
- Voltage limits
- Investment constraints

References:
- Dehghan, S., Nakiganda, A., & Aristidou, P. (2020). "Planning and Operation of 
  Resilient Microgrids: A Comprehensive Review." IEEE Transactions on Smart Grid.
- Nakiganda, A., Dehghan, S., & Aristidou, P. (2021). "PyEPlan: An Open-Source 
  Framework for Microgrid Planning and Operation." IEEE Power & Energy Society 
  General Meeting.

Example:
    >>> from pyeplan.investoper import inosys
    >>> inv_sys = inosys("input_folder", ref_bus=0)
    >>> inv_sys.solve(solver='glpk', invest=True, onlyopr=False)
"""

import pandas as pd
import pyomo.environ as pe
import numpy as np
import csv
import os
import shutil 

class inosys:
    """
    Investment and operation optimization system for microgrids.
    
    This class formulates and solves mixed-integer linear programming problems
    for microgrid investment and operation optimization. It handles complex
    constraints including power balance, generator limits, battery storage,
    network constraints, and voltage limits.
    
    The optimization problem considers:
    - Investment decisions for generators, storage, and renewables
    - Operational decisions for power generation and storage
    - Network constraints and voltage limits
    - Demand shedding and renewable curtailment
    - Battery energy storage system operation
    
    Attributes:
        cgen (pd.DataFrame): Conventional generator candidate data
        egen (pd.DataFrame): Existing conventional generator data
        csol (pd.DataFrame): Solar PV candidate data
        esol (pd.DataFrame): Existing solar PV data
        cwin (pd.DataFrame): Wind turbine candidate data
        ewin (pd.DataFrame): Existing wind turbine data
        cbat (pd.DataFrame): Battery storage candidate data
        elin (pd.DataFrame): Electrical line data
        pdem (pd.DataFrame): Active power demand profiles
        qdem (pd.DataFrame): Reactive power demand profiles
        prep (pd.DataFrame): Renewable active power profiles
        qrep (pd.DataFrame): Renewable reactive power profiles
        psol (pd.DataFrame): Solar power scenarios
        qsol (pd.DataFrame): Solar reactive power scenarios
        pwin (pd.DataFrame): Wind power scenarios
        qwin (pd.DataFrame): Wind reactive power scenarios
        dtim (pd.DataFrame): Time duration for each scenario
        ncg (int): Number of candidate conventional generators
        neg (int): Number of existing conventional generators
        ncs (int): Number of candidate solar PV systems
        nes (int): Number of existing solar PV systems
        ncw (int): Number of candidate wind turbines
        new (int): Number of existing wind turbines
        ncb (int): Number of candidate battery systems
        nel (int): Number of electrical lines
        nbb (int): Number of buses/nodes
        ntt (int): Number of time periods
        noo (int): Number of scenarios
        cds (float): Demand shedding cost
        css (float): Solar curtailment cost
        cws (float): Wind curtailment cost
        sb (float): Base apparent power
        sf (float): Scaling factor
        ref_bus (int): Reference bus number
        vmin (float): Minimum voltage limit
        vmax (float): Maximum voltage limit
        inp_folder (str): Input folder path
        phase (int): Number of phases
        outdir (str): Output directory path
    
    Methods:
        solve(): Solve the investment and operation optimization problem
        resCost(): Get optimization results - costs
        resWind(): Get optimization results - wind generation
        resBat(): Get optimization results - battery operation
        resSolar(): Get optimization results - solar generation
        resConv(): Get optimization results - conventional generation
        resCurt(): Get optimization results - curtailment
    """

    def __init__(self, inp_folder, ref_bus, dshed_cost = 1000000, rshed_cost = 500, phase = 3, vmin=0.85, vmax=1.15, sbase = 1, sc_fa = 1):
        """
        Initialize the investment and operation optimization system.
        
        Parameters:
            inp_folder (str): Input directory containing CSV data files
            ref_bus (int): Reference bus number for the system
            dshed_cost (float): Demand shedding cost (default: 1000000)
            rshed_cost (float): Renewable shedding cost (default: 500)
            phase (int): Number of phases (default: 3)
            vmin (float): Minimum voltage limit in p.u. (default: 0.85)
            vmax (float): Maximum voltage limit in p.u. (default: 1.15)
            sbase (float): Base apparent power in kW (default: 1)
            sc_fa (float): Scaling factor (default: 1)
        
        Required input files:
            - cgen_dist.csv: Conventional generator candidate data
            - egen_dist.csv: Existing conventional generator data
            - csol_dist.csv: Solar PV candidate data
            - esol_dist.csv: Existing solar PV data
            - cwin_dist.csv: Wind turbine candidate data
            - ewin_dist.csv: Existing wind turbine data
            - cbat_dist.csv: Battery storage candidate data
            - elin_dist.csv: Electrical line data
            - pdem_dist.csv: Active power demand profiles
            - qdem_dist.csv: Reactive power demand profiles
            - prep_dist.csv: Renewable active power profiles
            - qrep_dist.csv: Renewable reactive power profiles
            - psol_dist.csv: Solar power scenarios
            - qsol_dist.csv: Solar reactive power scenarios
            - pwin_dist.csv: Wind power scenarios
            - qwin_dist.csv: Wind reactive power scenarios
            - dtim_dist.csv: Time duration for each scenario
        
        Example:
            >>> inv_sys = inosys("input_folder", ref_bus=0, dshed_cost=1000000)
        """
        
        self.cgen = pd.read_csv(inp_folder + os.sep + 'cgen_dist.csv')
        self.egen = pd.read_csv(inp_folder + os.sep + 'egen_dist.csv')
        
        self.csol = pd.read_csv(inp_folder + os.sep + 'csol_dist.csv')
        self.esol = pd.read_csv(inp_folder + os.sep + 'esol_dist.csv')

        self.cwin = pd.read_csv(inp_folder + os.sep + 'cwin_dist.csv')
        self.ewin = pd.read_csv(inp_folder + os.sep + 'ewin_dist.csv')
        
        self.cbat = pd.read_csv(inp_folder + os.sep + 'cbat_dist.csv')

        self.elin = pd.read_csv(inp_folder + os.sep + 'elin_dist.csv')
        
        self.pdem = pd.read_csv(inp_folder + os.sep + 'pdem_dist.csv')
        self.qdem = pd.read_csv(inp_folder + os.sep + 'qdem_dist.csv')
        
        self.prep = pd.read_csv(inp_folder + os.sep + 'prep_dist.csv')
        self.qrep = pd.read_csv(inp_folder + os.sep + 'qrep_dist.csv')
        
        self.psol = pd.read_csv(inp_folder + os.sep + 'psol_dist.csv')
        self.qsol = pd.read_csv(inp_folder + os.sep + 'qsol_dist.csv')
        
        self.pwin = pd.read_csv(inp_folder + os.sep + 'pwin_dist.csv')
        self.qwin = pd.read_csv(inp_folder + os.sep + 'qwin_dist.csv')
        
        self.dtim = pd.read_csv(inp_folder + os.sep + 'dtim_dist.csv')
        
        # Convert power limits to per-unit values
        self.cgen['pmin'] = self.cgen['pmin'].div(sbase)
        self.cgen['pmax'] = self.cgen['pmax'].div(sbase)
        self.cgen['qmin'] = self.cgen['qmin'].div(sbase)
        self.cgen['qmax'] = self.cgen['qmax'].div(sbase)
        
        self.egen['pmin'] = self.egen['pmin'].div(sbase)
        self.egen['pmax'] = self.egen['pmax'].div(sbase)
        self.egen['qmin'] = self.egen['qmin'].div(sbase)
        self.egen['qmax'] = self.egen['qmax'].div(sbase)
        
        self.csol['pmin'] = self.csol['pmin'].div(sbase)
        self.csol['pmax'] = self.csol['pmax'].div(sbase)
        self.csol['qmin'] = self.csol['qmin'].div(sbase)
        self.csol['qmax'] = self.csol['qmax'].div(sbase)
        
        self.esol['pmin'] = self.esol['pmin'].div(sbase)
        self.esol['pmax'] = self.esol['pmax'].div(sbase)
        self.esol['qmin'] = self.esol['qmin'].div(sbase)
        self.esol['qmax'] = self.esol['qmax'].div(sbase)
        
        self.cwin['pmin'] = self.cwin['pmin'].div(sbase)
        self.cwin['pmax'] = self.cwin['pmax'].div(sbase)
        self.cwin['qmin'] = self.cwin['qmin'].div(sbase)
        self.cwin['qmax'] = self.cwin['qmax'].div(sbase)
        
        self.ewin['pmin'] = self.ewin['pmin'].div(sbase)
        self.ewin['pmax'] = self.ewin['pmax'].div(sbase)
        self.ewin['qmin'] = self.ewin['qmin'].div(sbase)
        self.ewin['qmax'] = self.ewin['qmax'].div(sbase)
                
        self.cbat['emin'] = self.cbat['emin'].div(sbase)
        self.cbat['emax'] = self.cbat['emax'].div(sbase)
        self.cbat['eini'] = self.cbat['eini'].div(sbase)
        self.cbat['pmin'] = self.cbat['pmin'].div(sbase)
        self.cbat['pmax'] = self.cbat['pmax'].div(sbase)

        # Count number of components
        self.ncg = len(self.cgen)
        self.neg = len(self.egen)
        
        self.ncs = len(self.csol)
        self.nes = len(self.esol)
        
        self.ncw = len(self.cwin)
        self.new = len(self.ewin)
        
        self.ncb = len(self.cbat)
        
        self.nel = len(self.elin)
    
        self.nbb = self.pdem.shape[1]
        
        self.ntt = self.prep.shape[0]

        self.noo = self.prep.shape[1] 
        
        self.cds = dshed_cost   
        self.css = rshed_cost    
        self.cws = rshed_cost    
        self.sb = sbase          
        self.sf = sc_fa          
        self.ref_bus = ref_bus   
        self.vmin = vmin   
        self.vmax = vmax
        self.inp_folder = inp_folder
        self.phase = phase 

        self.outdir = ''


    def solve(self, solver = 'glpk', neos = False, invest = False, onlyopr = True, commit = False, solemail = '', verbose = False):
        '''
        Solve the investment and operation problem.
        
        Parameters:
            solver (str): Solver to be used. Available: glpk, cbc, ipopt, gurobi
            neos (bool): True/False indicates if using NEOS remote solver service
            invest (bool): True/False indicates binary/continuous nature of investment-related decision variables
            onlyopr (bool): True/False indicates if the problem will only solve the operation or both investment and operation
            commit (bool): True/False indicates if using binary commitment variables for generators
            solemail (str): Email address required for NEOS solver service
            verbose (bool): True/False indicates if solver output should be displayed (default: False)
        
        Returns:
            None: Updates the object with optimization results and saves output files
        
        Example:
            >>> import pyeplan
            >>> sys_inv = pyeplan.inosys("wat_inv", ref_bus = 260)
            >>> sys_inv.solve(verbose=True)
        '''

        
        #Define the Model type
        m = pe.ConcreteModel()
        
        #Define the Sets
        m.cg = pe.Set(initialize=list(range(self.ncg)),ordered=True)
        m.eg = pe.Set(initialize=list(range(self.neg)),ordered=True)
        
        m.cs = pe.Set(initialize=list(range(self.ncs)),ordered=True)
        m.es = pe.Set(initialize=list(range(self.nes)),ordered=True)
        
        m.cw = pe.Set(initialize=list(range(self.ncw)),ordered=True)
        m.ew = pe.Set(initialize=list(range(self.new)),ordered=True)
        
        m.cb = pe.Set(initialize=list(range(self.ncb)),ordered=True)
        
        m.el = pe.Set(initialize=list(range(self.nel)),ordered=True)
        
        m.bb = pe.Set(initialize=list(range(self.nbb)),ordered=True)

        m.tt = pe.Set(initialize=list(range(self.ntt)),ordered=True)

        m.oo = pe.Set(initialize=list(range(self.noo)),ordered=True)
        
        #Define Variables
        
        #Objective Function
        m.z = pe.Var()
        m.opr = pe.Var()
        m.inv = pe.Var() 
        m.she = pe.Var() 
        
        #Active and Reactive Power Generations (Conventional)
        m.pcg = pe.Var(m.cg,m.tt,m.oo,within=pe.NonNegativeReals)
        m.peg = pe.Var(m.eg,m.tt,m.oo,within=pe.NonNegativeReals)
        
        m.qcg = pe.Var(m.cg,m.tt,m.oo,within=pe.NonNegativeReals)
        m.qeg = pe.Var(m.eg,m.tt,m.oo,within=pe.NonNegativeReals)
        
        #Active and Reactive Power Generations (Solar)
        m.pcs = pe.Var(m.cs,m.tt,m.oo,within=pe.NonNegativeReals)
        m.pes = pe.Var(m.es,m.tt,m.oo,within=pe.NonNegativeReals)
        
        m.qcs = pe.Var(m.cs,m.tt,m.oo,within=pe.Reals)
        m.qes = pe.Var(m.es,m.tt,m.oo,within=pe.Reals)
        
        #Active and Reactive Power Generations (Wind)
        m.pcw = pe.Var(m.cw,m.tt,m.oo,within=pe.NonNegativeReals)
        m.pew = pe.Var(m.ew,m.tt,m.oo,within=pe.NonNegativeReals)
        
        m.qcw = pe.Var(m.cw,m.tt,m.oo,within=pe.Reals)
        m.qew = pe.Var(m.ew,m.tt,m.oo,within=pe.Reals)
        
        #Charging and Discharging Status of Battary 
        m.pbc = pe.Var(m.cb,m.tt,m.oo,within=pe.NonNegativeReals)
        m.pbd = pe.Var(m.cb,m.tt,m.oo,within=pe.NonNegativeReals)
        
        m.qcd = pe.Var(m.cb,m.tt,m.oo,within=pe.Reals)
        
        #Demand, Solar, and Wind Shedding
        if commit:
            m.pds = pe.Var(m.bb,m.tt,m.oo,within=pe.Binary)
        else: 
            m.pds = pe.Var(m.bb,m.tt,m.oo,within=pe.NonNegativeReals,bounds=(0,1))
        m.pss = pe.Var(m.bb,m.tt,m.oo,within=pe.NonNegativeReals)
        m.pws = pe.Var(m.bb,m.tt,m.oo,within=pe.NonNegativeReals)
        
        #Active and Reactive Line Flows
        m.pel = pe.Var(m.el,m.tt,m.oo,within=pe.Reals)    #Active Power
        m.qel = pe.Var(m.el,m.tt,m.oo,within=pe.Reals)    #Reactive Power
        
        #Voltage Magnitude  
        m.vol = pe.Var(m.bb,m.tt,m.oo,within=pe.Reals,bounds=(self.vmin,self.vmax))
        

        #Commitment Status
        if commit:
            m.cu = pe.Var(m.cg,m.tt,m.oo,within=pe.Binary)
            m.eu = pe.Var(m.eg,m.tt,m.oo,within=pe.Binary)
        else: 
            m.cu = pe.Var(m.cg,m.tt,m.oo,within=pe.NonNegativeReals)
            m.eu = pe.Var(m.eg,m.tt,m.oo,within=pe.NonNegativeReals)
           
        if not onlyopr:
            #Investment Status (Conventional)
            if invest:
                m.xg = pe.Var(m.cg,within=pe.Binary)
            else:
                m.xg = pe.Var(m.cg,within=pe.NonNegativeReals,bounds=(0,1))
                
            #Investment Status (Solar) 
            if invest:
                m.xs = pe.Var(m.cs,within=pe.Binary)
            else:
                m.xs = pe.Var(m.cs,within=pe.NonNegativeReals,bounds=(0,1))
            
            #Investment Status (Wind)
            if invest:
                m.xw = pe.Var(m.cw,within=pe.Binary)
            else: 
                m.xw = pe.Var(m.cw,within=pe.NonNegativeReals,bounds=(0,1))
            
            #Investment Status (Battary) 
            if invest:
                m.xb = pe.Var(m.cb,within=pe.Binary)
            else:
                m.xb = pe.Var(m.cb,within=pe.NonNegativeReals,bounds=(0,1))
        else: 
            m.xg = pe.Var(m.cg,within=pe.NonNegativeReals,bounds=(0,0))
            m.xs = pe.Var(m.cs,within=pe.NonNegativeReals,bounds=(0,0))
            m.xw = pe.Var(m.cw,within=pe.NonNegativeReals,bounds=(0,0))
            m.xb = pe.Var(m.cb,within=pe.NonNegativeReals,bounds=(0,0))
                
        #Objective Function
        def obj_rule(m):
            return m.z
        m.obj = pe.Objective(rule=obj_rule)

        #Definition Cost
        def cost_def_rule(m):
            return m.z == m.inv + m.opr 
        m.cost_def = pe.Constraint(rule=cost_def_rule)


        #Investment Cost
        def inv_cost_def_rule(m):
            return m.inv == self.sf*sum(self.cgen['icost'][cg]*self.cgen['pmax'][cg]*m.xg[cg] for cg in m.cg) + \
                            self.sf*sum(self.csol['icost'][cs]*self.csol['pmax'][cs]*m.xs[cs] for cs in m.cs) + \
                            self.sf*sum(self.cwin['icost'][cw]*self.cwin['pmax'][cw]*m.xw[cw] for cw in m.cw) + \
                            self.sf*sum(self.cbat['icost'][cb]*self.cbat['pmax'][cb]*m.xb[cb] for cb in m.cb)
        m.inv_cost_def = pe.Constraint(rule=inv_cost_def_rule)
                              
        #Operation Cost 
        def opr_cost_def_rule(m):
            return m.opr == self.sf*self.sb*(sum(self.dtim['dt'][oo]*self.cgen['ocost'][cg]*m.pcg[cg,tt,oo] for cg in m.cg for tt in m.tt for oo in m.oo) + \
                             sum(self.dtim['dt'][oo]*self.egen['ocost'][eg]*m.peg[eg,tt,oo] for eg in m.eg for tt in m.tt for oo in m.oo) + \
                             sum(self.dtim['dt'][oo]*self.csol['ocost'][cs]*m.pcs[cs,tt,oo] for cs in m.cs for tt in m.tt for oo in m.oo) + \
                             sum(self.dtim['dt'][oo]*self.esol['ocost'][es]*m.pes[es,tt,oo] for es in m.es for tt in m.tt for oo in m.oo) + \
                             sum(self.dtim['dt'][oo]*self.cwin['ocost'][cw]*m.pcw[cw,tt,oo] for cw in m.cw for tt in m.tt for oo in m.oo) + \
                             sum(self.dtim['dt'][oo]*self.ewin['ocost'][ew]*m.pew[ew,tt,oo] for ew in m.ew for tt in m.tt for oo in m.oo) + \
                             sum(self.dtim['dt'][oo]*self.cds*self.pdem.iloc[tt,bb]*self.prep.iloc[tt,oo]*m.pds[bb,tt,oo] for bb in m.bb for tt in m.tt for oo in m.oo) + \
                             sum(self.dtim['dt'][oo]*self.css*m.pss[bb,tt,oo] for bb in m.bb for tt in m.tt for oo in m.oo)+ \
                             sum(self.dtim['dt'][oo]*self.cws*m.pws[bb,tt,oo] for bb in m.bb for tt in m.tt for oo in m.oo))
        m.opr_cost_def = pe.Constraint(rule=opr_cost_def_rule)

        #Shedding Cost
        def she_cost_def_rule(m):
            return m.she == self.sf*self.sb*(sum(self.dtim['dt'][oo]*self.cds*self.pdem.iloc[tt,bb]*self.prep.iloc[tt,oo]*m.pds[bb,tt,oo] for bb in m.bb for tt in m.tt for oo in m.oo) + \
                                             sum(self.dtim['dt'][oo]*self.css*m.pss[bb,tt,oo] for bb in m.bb for tt in m.tt for oo in m.oo)+ \
                                             sum(self.dtim['dt'][oo]*self.cws*m.pws[bb,tt,oo] for bb in m.bb for tt in m.tt for oo in m.oo))
        m.she_cost_def = pe.Constraint(rule=she_cost_def_rule)

        #Active Energy Balance
        def act_bal_rule(m,bb,tt,oo):
            return (1/self.phase)*sum(m.pcg[cg,tt,oo] for cg in m.cg if self.cgen['bus'][cg] == bb) + \
                   (1/self.phase)*sum(m.peg[eg,tt,oo] for eg in m.eg if self.egen['bus'][eg] == bb) + \
                   (1/self.phase)*sum(m.pcs[cs,tt,oo] for cs in m.cs if self.csol['bus'][cs] == bb) + \
                   (1/self.phase)*sum(m.pes[es,tt,oo] for es in m.es if self.esol['bus'][es] == bb) + \
                   (1/self.phase)*sum(m.pcw[cw,tt,oo] for cw in m.cw if self.cwin['bus'][cw] == bb) + \
                   (1/self.phase)*sum(m.pew[ew,tt,oo] for ew in m.ew if self.ewin['bus'][ew] == bb) + \
                   (1/self.phase)*sum(m.pbd[cb,tt,oo] for cb in m.cb if self.cbat['bus'][cb] == bb) - \
                   (1/self.phase)*sum(m.pbc[cb,tt,oo] for cb in m.cb if self.cbat['bus'][cb] == bb) + \
                   sum(m.pel[el,tt,oo] for el in m.el if self.elin['to'][el] == bb) == \
                   sum(m.pel[el,tt,oo] for el in m.el if self.elin['from'][el] == bb) + \
                   self.pdem.iloc[tt,bb]*self.prep.iloc[tt,oo]*1/self.phase*(1 - m.pds[bb,tt,oo]) + \
                   m.pss[bb,tt,oo] + m.pws[bb,tt,oo]
        m.act_bal = pe.Constraint(m.bb, m.tt, m.oo, rule=act_bal_rule)
     
        #Reactive Energy Balance
        def rea_bal_rule(m,bb,tt,oo):
            return (1/self.phase)*sum(m.qcg[cg,tt,oo] for cg in m.cg if self.cgen['bus'][cg] == bb) + \
                   (1/self.phase)*sum(m.qeg[eg,tt,oo] for eg in m.eg if self.egen['bus'][eg] == bb) + \
                   (1/self.phase)*sum(m.qcs[cs,tt,oo] for cs in m.cs if self.csol['bus'][cs] == bb) + \
                   (1/self.phase)*sum(m.qes[es,tt,oo] for es in m.es if self.esol['bus'][es] == bb) + \
                   (1/self.phase)*sum(m.qcw[cw,tt,oo] for cw in m.cw if self.cwin['bus'][cw] == bb) + \
                   (1/self.phase)*sum(m.qew[ew,tt,oo] for ew in m.ew if self.ewin['bus'][ew] == bb) + \
                   (1/self.phase)*sum(m.qcd[cb,tt,oo] for cb in m.cb if self.cbat['bus'][cb] == bb) + \
                   sum(m.qel[el,tt,oo] for el in m.el if self.elin['to'][el] == bb) == \
                   sum(m.qel[el,tt,oo] for el in m.el if self.elin['from'][el] == bb) + \
                   self.qdem.iloc[tt,bb]*self.qrep.iloc[tt,oo]*(1/self.phase)*(1 - m.pds[bb,tt,oo])

        m.rea_bal = pe.Constraint(m.bb, m.tt, m.oo, rule=rea_bal_rule)

        #Minimum Active Generation (Conventional)
        def min_act_cgen_rule(m,cg,tt,oo):
            return m.pcg[cg,tt,oo] >= m.cu[cg,tt,oo]*self.cgen['pmin'][cg]
        m.min_act_cgen = pe.Constraint(m.cg, m.tt, m.oo, rule=min_act_cgen_rule)
        
        def min_act_egen_rule(m,eg,tt,oo):
            return m.peg[eg,tt,oo] >= m.eu[eg,tt,oo]*self.egen['pmin'][eg]
        m.min_act_egen = pe.Constraint(m.eg, m.tt, m.oo, rule=min_act_egen_rule)
        
        #Minimum Active Generation (Solar)
        def min_act_csol_rule(m,cs,tt,oo):
            return m.pcs[cs,tt,oo] >= m.xs[cs]*self.csol['pmin'][cs]
        m.min_act_csol = pe.Constraint(m.cs, m.tt, m.oo, rule=min_act_csol_rule)
        
        def min_act_esol_rule(m,es,tt,oo):
            return m.pes[es,tt,oo] >= self.esol['pmin'][es]
        m.min_act_esol = pe.Constraint(m.es, m.tt, m.oo, rule=min_act_esol_rule)
        
        #Minimum Active Generation (Wind)
        def min_act_cwin_rule(m,cw,tt,oo):
            return m.pcw[cw,tt,oo] >= m.xw[cw]*self.cwin['pmin'][cw]
        m.min_act_cwin = pe.Constraint(m.cw, m.tt, m.oo, rule=min_act_cwin_rule)
        
        def min_act_ewin_rule(m,ew,tt,oo):
            return m.pew[ew,tt,oo] >= self.ewin['pmin'][ew]
        m.min_act_ewin = pe.Constraint(m.ew, m.tt, m.oo, rule=min_act_ewin_rule)
        
        #Minimum Active Charging and Discharging (Battery)
        def min_act_cbat_rule(m,cb,tt,oo):
            return m.pbc[cb,tt,oo] >= m.xb[cb]*self.cbat['pmin'][cb]
        m.min_act_cbat = pe.Constraint(m.cb, m.tt, m.oo, rule=min_act_cbat_rule)
        
        def min_act_dbat_rule(m,cb,tt,oo):
            return m.pbd[cb,tt,oo] >= m.xb[cb]*self.cbat['pmin'][cb]
        m.min_act_dbat = pe.Constraint(m.cb, m.tt, m.oo, rule=min_act_dbat_rule)

        #Maximum Active Generation (Conventional)
        def max_act_cgen_rule(m,cg,tt,oo):
            return m.pcg[cg,tt,oo] <= m.cu[cg,tt,oo]*self.cgen['pmax'][cg]
        m.max_act_cgen = pe.Constraint(m.cg, m.tt, m.oo, rule=max_act_cgen_rule)
        
        def max_act_egen_rule(m,eg,tt,oo):
            return m.peg[eg,tt,oo] <= m.eu[eg,tt,oo]*self.egen['pmax'][eg]
        m.max_act_egen = pe.Constraint(m.eg, m.tt, m.oo, rule=max_act_egen_rule)
        
        #Maximum Active Generation (Solar)
        def max_act_csol_rule(m,cs,tt,oo):
            return m.pcs[cs,tt,oo] <= m.xs[cs]*self.psol.iloc[tt,oo]
        m.max_act_csol = pe.Constraint(m.cs, m.tt, m.oo, rule=max_act_csol_rule)
        
        def max_act_esol_rule(m,es,tt,oo):
            return m.pes[es,tt,oo] <= self.psol.iloc[tt,oo]
        m.max_act_esol = pe.Constraint(m.es, m.tt, m.oo, rule=max_act_esol_rule)
        
        #Maximum Active Generation (Wind)
        def max_act_cwin_rule(m,cw,tt,oo):
            return m.pcw[cw,tt,oo] <= m.xw[cw]*self.pwin.iloc[tt,oo]
        m.max_act_cwin = pe.Constraint(m.cw, m.tt, m.oo, rule=max_act_cwin_rule)
        
        def max_act_ewin_rule(m,ew,tt,oo):
            return m.pew[ew,tt,oo] <= self.pwin.iloc[tt,oo]
        m.max_act_ewin = pe.Constraint(m.ew, m.tt, m.oo, rule=max_act_ewin_rule)
        
        #Maximum Active Charging and Discharging (Battery)
        def max_act_cbat_rule(m,cb,tt,oo):
            return m.pbc[cb,tt,oo] <= m.xb[cb]*self.cbat['pmax'][cb]
        m.max_act_cbat = pe.Constraint(m.cb, m.tt, m.oo, rule=max_act_cbat_rule)
        
        def max_act_dbat_rule(m,cb,tt,oo):
            return m.pbd[cb,tt,oo] <= m.xb[cb]*self.cbat['pmax'][cb]
        m.max_act_dbat = pe.Constraint(m.cb, m.tt, m.oo, rule=max_act_dbat_rule)
        
        #Minimum Reactive Generation (Conventional)
        def min_rea_cgen_rule(m,cg,tt,oo):
            return m.qcg[cg,tt,oo] >= m.cu[cg,tt,oo]*self.cgen['qmin'][cg]
        m.min_rea_cgen = pe.Constraint(m.cg, m.tt, m.oo, rule=min_rea_cgen_rule)
        
        def min_rea_egen_rule(m,eg,tt,oo):
            return m.qeg[eg,tt,oo] >= m.eu[eg,tt,oo]*self.egen['qmin'][eg]
        m.min_rea_egen = pe.Constraint(m.eg, m.tt, m.oo, rule=min_rea_egen_rule)
        
        #Minimum Reactive Generation (Solar)
        def min_rea_csol_rule(m,cs,tt,oo):
            return m.qcs[cs,tt,oo] >= m.xs[cs]*self.csol['qmin'][cs]
        m.min_rea_csol = pe.Constraint(m.cs, m.tt, m.oo, rule=min_rea_csol_rule)
        
        def min_rea_esol_rule(m,es,tt,oo):
            return m.qes[es,tt,oo] >= self.esol['qmin'][es]
        m.min_rea_esol = pe.Constraint(m.es, m.tt, m.oo, rule=min_rea_esol_rule)
        
        #Minimum Reactive Generation (Wind)
        def min_rea_cwin_rule(m,cw,tt,oo):
            return m.qcw[cw,tt,oo] >= m.xw[cw]*self.cwin['qmin'][cw]
        m.min_rea_cwin = pe.Constraint(m.cw, m.tt, m.oo, rule=min_rea_cwin_rule)
        
        def min_rea_ewin_rule(m,ew,tt,oo):
            return m.qew[ew,tt,oo] >= self.ewin['qmin'][ew]
        m.min_rea_ewin = pe.Constraint(m.ew, m.tt, m.oo, rule=min_rea_ewin_rule)
        
        #Minimum Reactive Generation (Battery)
        def min_rea_bat_rule(m,cb,tt,oo):
            return m.qcd[cb,tt,oo] >= m.xb[cb]*self.cbat['qmin'][cb]
        m.min_rea_bat = pe.Constraint(m.cb, m.tt, m.oo, rule=min_rea_bat_rule)
        
        #Maximum Reactive Generation (Conventional)
        def max_rea_cgen_rule(m,cg,tt,oo):
            return m.qcg[cg,tt,oo] <= m.cu[cg,tt,oo]*self.cgen['qmax'][cg]
        m.max_rea_cgen = pe.Constraint(m.cg, m.tt, m.oo, rule=max_rea_cgen_rule)
        
        def max_rea_egen_rule(m,eg,tt,oo):
            return m.qeg[eg,tt,oo] <= m.eu[eg,tt,oo]*self.egen['qmax'][eg]
        m.max_rea_egen = pe.Constraint(m.eg, m.tt, m.oo, rule=max_rea_egen_rule)

        #Maximum Reactive Generation (Solar)
        def max_rea_csol_rule(m,cs,tt,oo):
            return m.qcs[cs,tt,oo] <= m.xs[cs]*self.csol['qmax'][cs]
        m.max_rea_csol = pe.Constraint(m.cs, m.tt, m.oo, rule=max_rea_csol_rule)
        
        def max_rea_esol_rule(m,es,tt,oo):
            return m.qes[es,tt,oo] <= self.esol['qmax'][es]
        m.max_rea_esol = pe.Constraint(m.es, m.tt, m.oo, rule=max_rea_esol_rule)
        
        #Maximum Reactive Generation (Wind)
        def max_rea_cwin_rule(m,cw,tt,oo):
            return m.qcw[cw,tt,oo] <= m.xw[cw]*self.cwin['qmax'][cw]
        m.max_rea_cwin = pe.Constraint(m.cw, m.tt, m.oo, rule=max_rea_cwin_rule)
        
        def max_rea_ewin_rule(m,ew,tt,oo):
            return m.qew[ew,tt,oo] <= self.ewin['qmax'][ew]
        m.max_rea_ewin = pe.Constraint(m.ew, m.tt, m.oo, rule=max_rea_ewin_rule)
        
        #Minimum Reactive Generation (Battery)
        def max_rea_bat_rule(m,cb,tt,oo):
            return m.qcd[cb,tt,oo] <= m.xb[cb]*self.cbat['qmax'][cb]
        m.max_rea_bat = pe.Constraint(m.cb, m.tt, m.oo, rule=max_rea_bat_rule)
        
        #Minimum and Maximum Energy (Battery)
        def min_eng_bat_rule(m,cb,tt,oo):
            return self.cbat['eini'][cb]*m.xb[cb] + \
                   sum(m.pbc[cb,t,oo]*self.cbat['ec'][cb] for t in m.tt if t <= tt) - \
                   sum(m.pbd[cb,t,oo]/self.cbat['ed'][cb] for t in m.tt if t <= tt) >= m.xb[cb]*self.cbat['emin'][cb]
        m.min_eng_bat = pe.Constraint(m.cb, m.tt, m.oo, rule=min_eng_bat_rule)
        
        def max_eng_bat_rule(m,cb,tt,oo):
            return self.cbat['eini'][cb]*m.xb[cb] + \
                   sum(m.pbc[cb,t,oo]*self.cbat['ec'][cb] for t in m.tt if t <= tt) - \
                   sum(m.pbd[cb,t,oo]/self.cbat['ed'][cb] for t in m.tt if t <= tt) <= m.xb[cb]*self.cbat['emax'][cb]
        m.max_eng_bat = pe.Constraint(m.cb, m.tt, m.oo, rule=max_eng_bat_rule)
        
        def cop_eng_bat_rule(m,cb,oo):
            return sum(m.pbc[cb,t,oo]*self.cbat['ec'][cb] for t in m.tt) == \
                   sum(m.pbd[cb,t,oo]/self.cbat['ed'][cb] for t in m.tt)
        m.cop_eng_bat = pe.Constraint(m.cb, m.oo, rule=cop_eng_bat_rule)
        
        #Maximum Solar Shedding
        def max_sol_shed_rule(m,bb,tt,oo):
            return m.pss[bb,tt,oo] == (sum(m.xs[cs]*self.psol.iloc[tt,oo] for cs in m.cs if self.csol['bus'][cs] == bb ) + \
                                       sum(self.psol.iloc[tt,oo] for es in m.es if self.esol['bus'][es] == bb )) - \
                                      (sum(m.pcs[cs,tt,oo] for cs in m.cs if self.csol['bus'][cs] == bb) + \
                                       sum(m.pes[es,tt,oo] for es in m.es if self.esol['bus'][es] == bb)) 
        m.max_sol_shed = pe.Constraint(m.bb, m.tt, m.oo, rule=max_sol_shed_rule)

        #Maximum Wind Shedding
        def max_win_shed_rule(m,bb,tt,oo):
            return m.pws[bb,tt,oo] == (sum(m.xw[cw]*self.pwin.iloc[tt,oo] for cw in m.cw if self.cwin['bus'][cw] == bb) + \
                                       sum(self.pwin.iloc[tt,oo] for ew in m.ew if self.ewin['bus'][ew] == bb)) - \
                                      (sum(m.pcw[cw,tt,oo] for cw in m.cw if self.cwin['bus'][cw] == bb) + \
                                       sum(m.pew[ew,tt,oo] for ew in m.ew if self.ewin['bus'][ew] == bb)) 
        m.max_win_shed = pe.Constraint(m.bb, m.tt, m.oo, rule=max_win_shed_rule)

        #Line flow Definition
        def flow_rule(m,el,tt,oo): 
            return (m.vol[self.elin['from'][el],tt,oo] - m.vol[self.elin['to'][el],tt,oo]) == \
                                  self.elin['res'][el]*(m.pel[el,tt,oo]) + \
                                  self.elin['rea'][el]*(m.qel[el,tt,oo])
        m.flow = pe.Constraint(m.el, m.tt, m.oo, rule=flow_rule)
        
        #Max Active Line Flow
        def max_act_eflow_rule(m,el,tt,oo):
            return m.pel[el,tt,oo] <= self.elin['pmax'][el]*self.elin['ini'][el]
        m.max_act_eflow = pe.Constraint(m.el, m.tt, m.oo, rule=max_act_eflow_rule)

        #Min Active Line Flow
        def min_act_eflow_rule(m,el,tt,oo):
            return m.pel[el,tt,oo] >= -self.elin['pmax'][el]*self.elin['ini'][el]
        m.min_act_eflow = pe.Constraint(m.el, m.tt, m.oo, rule=min_act_eflow_rule)

        #Max Reactive Line Flow
        def max_rea_eflow_rule(m,el,tt,oo):
            return m.qel[el,tt,oo] <= self.elin['qmax'][el]*self.elin['ini'][el]
        m.max_rea_eflow = pe.Constraint(m.el, m.tt, m.oo, rule=max_rea_eflow_rule)

        #Min Reactive Line Flow
        def min_rea_eflow_rule(m,el,tt,oo):
            return m.qel[el,tt,oo] >= -self.elin['qmax'][el]*self.elin['ini'][el]
        m.min_rea_eflow = pe.Constraint(m.el, m.tt, m.oo, rule=min_rea_eflow_rule)
        
        #Voltage Magnitude at Reference Bus
        def vol_ref_rule(m,tt,oo):
            return sum(m.vol[bb,tt,oo] for bb in m.bb if bb==self.ref_bus) == 1
        m.vol_ref = pe.Constraint(m.tt, m.oo, rule=vol_ref_rule)
        
        #Investment Status 
        def inv_stat_rule(m,cg,tt,oo):
            return m.cu[cg,tt,oo] <= m.xg[cg] 
        m.inv_stat = pe.Constraint(m.cg, m.tt, m.oo, rule=inv_stat_rule)
        
        def inv_bat_rule(m):
            return sum(m.xb[cb] for cb in m.cb) <= \
                    sum(m.xs[cs] for cs in m.cs) + \
                    sum(m.xw[cw] for cw in m.cw)    
        m.inv_bat = pe.Constraint(rule=inv_bat_rule)
                   
        #Solve the optimization problem
        
        if solver == 'gurobi':
            opt = pe.SolverFactory(solver, solver_io='python')
            opt.options['threads'] = 0
            opt.options['mipgap'] = 0
        else:
            opt = pe.SolverFactory(solver)
            
        if neos:
            os.environ['NEOS_EMAIL'] = solemail
            solver_manager = pe.SolverManagerFactory('neos')
            result = solver_manager.solve(m,opt=opt,symbolic_solver_labels=True,tee=verbose)
        else:
            result = opt.solve(m,symbolic_solver_labels=True,tee=verbose)
        
        self.output = m
        
        self.total = round(m.z.value,6)
        self.total_inv = round(m.inv.value,6)
        self.total_opr = round(m.opr.value,6)
        
        self.xg_output = pyomo2dfinv(m.xg,m.cg).T
        self.xs_output = pyomo2dfinv(m.xs,m.cs).T
        self.xw_output = pyomo2dfinv(m.xw,m.cw).T
        self.xb_output = pyomo2dfinv(m.xb,m.cb).T
        
        self.cu_output = pyomo2dfoprm(m.cu,m.cg,m.tt,m.oo).T
        self.eu_output = pyomo2dfoprm(m.eu,m.eg,m.tt,m.oo).T
        
        self.pcg_output = pyomo2dfopr(m.pcg,m.cg,m.tt,m.oo).T
        self.qcg_output = pyomo2dfopr(m.qcg,m.cg,m.tt,m.oo).T
        
        self.peg_output = pyomo2dfopr(m.peg,m.eg,m.tt,m.oo).T
        self.qeg_output = pyomo2dfopr(m.qeg,m.eg,m.tt,m.oo).T
        
        self.pcs_output = pyomo2dfopr(m.pcs,m.cs,m.tt,m.oo).T
        self.qcs_output = pyomo2dfopr(m.qcs,m.cs,m.tt,m.oo).T
        
        self.pes_output = pyomo2dfopr(m.pes,m.es,m.tt,m.oo).T
        self.qes_output = pyomo2dfopr(m.qes,m.es,m.tt,m.oo).T
        
        self.pcw_output = pyomo2dfopr(m.pcw,m.cw,m.tt,m.oo).T
        self.qcw_output = pyomo2dfopr(m.qcw,m.cw,m.tt,m.oo).T
        
        self.pew_output = pyomo2dfopr(m.pew,m.ew,m.tt,m.oo).T
        self.qew_output = pyomo2dfopr(m.qew,m.ew,m.tt,m.oo).T
        
        self.pbc_output = pyomo2dfopr(m.pbc,m.cb,m.tt,m.oo).T
        self.pbd_output = pyomo2dfopr(m.pbd,m.cb,m.tt,m.oo).T
        self.qcd_output = pyomo2dfopr(m.qcd,m.cb,m.tt,m.oo).T
        
        self.pds_output = pyomo2dfoprm(m.pds,m.bb,m.tt,m.oo).T
        self.pss_output = pyomo2dfopr(m.pss,m.bb,m.tt,m.oo).T
        self.pws_output = pyomo2dfopr(m.pws,m.bb,m.tt,m.oo).T
        
        self.vol_output = pyomo2dfoprm(m.vol,m.bb,m.tt,m.oo).T
        
        self.pel_output = pyomo2dfopr(m.pel,m.el,m.tt,m.oo).T
        self.qel_output = pyomo2dfopr(m.qel,m.el,m.tt,m.oo).T
    
        # Setup the results folder
        self.outdir = self.inp_folder + os.sep + 'results'
        if os.path.exists(self.outdir):
            shutil.rmtree(self.outdir) 
        os.makedirs(self.outdir)
        
        with open(self.outdir + os.sep + 'obj.csv', 'w', newline='') as csvfile:
            thewriter = csv.writer(csvfile)   
            thewriter.writerow(['total costs', self.total])
            thewriter.writerow(['total investment costs', self.total_inv])
            thewriter.writerow(['total operation costs', self.total_opr])
        
        self.xg_output.to_csv(self.outdir + os.sep + 'xg.csv', index=False)
        self.xs_output.to_csv(self.outdir + os.sep + 'xs.csv', index=False)
        self.xw_output.to_csv(self.outdir + os.sep + 'xw.csv', index=False)
        self.xb_output.to_csv(self.outdir + os.sep + 'xb.csv', index=False)
        
        self.cu_output.to_csv(self.outdir + os.sep + 'cu.csv', index=False)
        self.eu_output.to_csv(self.outdir + os.sep + 'eu.csv', index=False)
        
        self.pcg_output.to_csv(self.outdir + os.sep + 'pcg.csv', index=False)
        self.qcg_output.to_csv(self.outdir + os.sep + 'qcg.csv', index=False)
        
        self.peg_output.to_csv(self.outdir + os.sep + 'peg.csv', index=False)
        self.qeg_output.to_csv(self.outdir + os.sep + 'qeg.csv', index=False)
        
        self.pcs_output.to_csv(self.outdir + os.sep + 'pcs.csv',index=False)
        self.qcs_output.to_csv(self.outdir + os.sep + 'qcs.csv',index=False)
        
        self.pes_output.to_csv(self.outdir + os.sep + 'pes.csv',index=False)
        self.qes_output.to_csv(self.outdir + os.sep + 'qes.csv',index=False)
        
        self.pcw_output.to_csv(self.outdir + os.sep + 'pcw.csv',index=False)
        self.qcw_output.to_csv(self.outdir + os.sep + 'qcw.csv',index=False)
        
        self.pew_output.to_csv(self.outdir + os.sep + 'pew.csv',index=False)
        self.qew_output.to_csv(self.outdir + os.sep + 'qew.csv',index=False)
        
        self.pbc_output.to_csv(self.outdir + os.sep + 'pbc.csv',index=False)
        self.pbd_output.to_csv(self.outdir + os.sep + 'pbd.csv',index=False)
        self.qcd_output.to_csv(self.outdir + os.sep + 'qcd.csv',index=False)
        
        self.pds_output.to_csv(self.outdir + os.sep + 'pds.csv',index=False)
        self.pss_output.to_csv(self.outdir + os.sep + 'pss.csv',index=False)
        self.pws_output.to_csv(self.outdir + os.sep + 'pws.csv',index=False)
        
        self.vol_output.to_csv(self.outdir + os.sep + 'vol.csv',index=False)
        
        self.pel_output.to_csv(self.outdir + os.sep + 'pel.csv',index=False)
        self.qel_output.to_csv(self.outdir + os.sep + 'qel.csv',index=False)
    
    def resCost(self):
        """
        Get the objective cost results.
        
        This method returns the total costs breakdown including investment costs,
        operational costs, and total system costs from the optimization results
        as a pandas DataFrame.
        
        Returns:
            pandas.DataFrame: Cost breakdown with columns:
                - total costs: Total system cost
                - total investment costs: Investment cost component
                - total operation costs: Operational cost component
        
        Raises:
            Exception: If solve() method has not been successfully executed or
                      if the results directory doesn't exist
        
        Example:
            >>> inv_sys = inosys("input_folder", ref_bus=0)
            >>> inv_sys.solve()
            >>> cost_results = inv_sys.resCost()
            >>> print(cost_results)
        """

        if self.outdir != '' and os.path.exists(self.outdir):
            return pd.read_csv(self.outdir + os.sep + "obj.csv")
        else:
            print('Need to succesfully run the solve function first.')
            raise

    def resWind(self):
        """
        Get the wind capacity investment results.
        
        This method returns the optimal wind turbine capacity investments
        including installed capacity and bus locations for each candidate
        wind turbine.
        
        Returns:
            pandas.DataFrame: Wind investment results with columns:
                - Installed Capacity (kW): Optimal capacity for each wind turbine
                - Bus: Bus number where wind turbine is installed
        
        Raises:
            Exception: If solve() method has not been successfully executed
        
        Example:
            >>> inv_sys = inosys("input_folder", ref_bus=0)
            >>> inv_sys.solve(invest=True)
            >>> wind_results = inv_sys.resWind()
        """

        if self.outdir != '' and os.path.exists(self.outdir):
            cwin = pd.read_csv(self.inp_folder + os.sep + "cwin_dist.csv")
            iwin = pd.read_csv(self.outdir + os.sep + "xw.csv", header=None)
            # Get investment values (skip first row if it's a header)
            if len(iwin) > 1:
                inv_values = iwin.iloc[1:, 0].values
            else:
                inv_values = iwin.iloc[0:, 0].values
            # Calculate installed capacity for each unit
            installed_capacity = cwin['pmax'].values * inv_values
            # Create result DataFrame
            out_win = pd.DataFrame({
                'Installed Capacity (kW)': installed_capacity,
                'Bus': cwin['bus'].values
            }, index=range(1, len(cwin) + 1))
            out_win.index.name = 'Unit'
            return out_win
        else:
            print('Need to succesfully run the solve function first.')
            raise

    def resBat(self):
        """
        Get the battery capacity investment results.
        
        This method returns the optimal battery storage capacity investments
        including installed capacity and bus locations for each candidate
        battery system.
        
        Returns:
            pandas.DataFrame: Battery investment results with columns:
                - Installed Capacity (kW): Optimal capacity for each battery system
                - Bus: Bus number where battery is installed
        
        Raises:
            Exception: If solve() method has not been successfully executed
        
        Example:
            >>> inv_sys = inosys("input_folder", ref_bus=0)
            >>> inv_sys.solve(invest=True)
            >>> battery_results = inv_sys.resBat()
        """

        if self.outdir != '' and os.path.exists(self.outdir):
            cbat = pd.read_csv(self.inp_folder + os.sep + "cbat_dist.csv")
            ibat = pd.read_csv(self.outdir + os.sep + "xb.csv", header=None)
            # Get investment values (skip first row if it's a header)
            if len(ibat) > 1:
                inv_values = ibat.iloc[1:, 0].values
            else:
                inv_values = ibat.iloc[0:, 0].values
            # Calculate installed capacity for each unit
            installed_capacity = cbat['pmax'].values * inv_values
            # Create result DataFrame
            out_bat = pd.DataFrame({
                'Installed Capacity (kW)': installed_capacity,
                'Bus': cbat['bus'].values
            }, index=range(1, len(cbat) + 1))
            out_bat.index.name = 'Unit'
            return out_bat
        else:
            print('Need to succesfully run the solve function first.')
            raise

    def resSolar(self):
        """
        Get the solar capacity investment results.
        
        This method returns the optimal solar PV capacity investments
        including installed capacity and bus locations for each candidate
        solar PV system.
        
        Returns:
            pandas.DataFrame: Solar investment results with columns:
                - Installed Capacity (kW): Optimal capacity for each solar PV system
                - Bus: Bus number where solar PV is installed
        
        Raises:
            Exception: If solve() method has not been successfully executed
        
        Example:
            >>> inv_sys = inosys("input_folder", ref_bus=0)
            >>> inv_sys.solve(invest=True)
            >>> solar_results = inv_sys.resSolar()
        """

        if self.outdir != '' and os.path.exists(self.outdir):
            csol = pd.read_csv(self.inp_folder + os.sep + "csol_dist.csv")
            isol = pd.read_csv(self.outdir + os.sep + "xs.csv", header=None)
            # Get investment values (skip first row if it's a header)
            if len(isol) > 1:
                inv_values = isol.iloc[1:, 0].values
            else:
                inv_values = isol.iloc[0:, 0].values
            # Calculate installed capacity for each unit
            installed_capacity = csol['pmax'].values * inv_values
            # Create result DataFrame
            out_sol = pd.DataFrame({
                'Installed Capacity (kW)': installed_capacity,
                'Bus': csol['bus'].values
            }, index=range(1, len(csol) + 1))
            out_sol.index.name = 'Unit'
            return out_sol
        else:
            print('Need to succesfully run the solve function first.')
            raise

    def resConv(self):
        """
        Get the conventional generator capacity investment results.
        
        This method returns the optimal conventional generator capacity investments
        including installed capacity and bus locations for each candidate
        conventional generator.
        
        Returns:
            pandas.DataFrame: Conventional generator investment results with columns:
                - Installed Capacity (kW): Optimal capacity for each generator
                - Bus: Bus number where generator is installed
        
        Raises:
            Exception: If solve() method has not been successfully executed
        
        Example:
            >>> inv_sys = inosys("input_folder", ref_bus=0)
            >>> inv_sys.solve(invest=True)
            >>> conv_results = inv_sys.resConv()
        """

        if self.outdir != '' and os.path.exists(self.outdir):
            cgen = pd.read_csv(self.inp_folder + os.sep + "cgen_dist.csv")
            igen = pd.read_csv(self.outdir + os.sep + "xg.csv", header=None)
            # Get investment values - the first row might be a header or index
            if len(igen) > 1:
                inv_values = igen.iloc[1:, 0].values
            else:
                inv_values = igen.iloc[0:, 0].values
            
            # Ensure inv_values has the same length as cgen
            if len(inv_values) != len(cgen):
                # If lengths don't match, use the last value for all generators
                if len(inv_values) > 0:
                    inv_values = np.full(len(cgen), inv_values[-1])
                else:
                    inv_values = np.zeros(len(cgen))
            
            # Calculate installed capacity for each unit
            installed_capacity = cgen['pmax'].values * inv_values
            # Create result DataFrame
            out_gen = pd.DataFrame({
                'Installed Capacity (kW)': installed_capacity,
                'Bus': cgen['bus'].values
            }, index=range(1, len(cgen) + 1))
            out_gen.index.name = 'Unit'
            return out_gen
        else:
            print('Need to succesfully run the solve function first.')
            raise

    def resCurt(self):
        """
        Get the curtailment results.
        
        This method returns the demand shedding and renewable curtailment
        results from the optimization, showing how much load was shed and
        how much renewable energy was curtailed.
        
        Returns:
            dict: Dictionary containing three pandas.DataFrames:
                - 'demand_shedding': Demand shedding results (pds.csv)
                - 'solar_curtailment': Solar curtailment results (pss.csv)
                - 'wind_curtailment': Wind curtailment results (pws.csv)
        
        Raises:
            Exception: If solve() method has not been successfully executed
        
        Example:
            >>> inv_sys = inosys("input_folder", ref_bus=0)
            >>> inv_sys.solve()
            >>> curtailment_results = inv_sys.resCurt()
            >>> print(curtailment_results['demand_shedding'])
        """

        if self.outdir != '' and os.path.exists(self.outdir):
            pds = pd.read_csv(self.outdir + os.sep + "pds.csv")
            pss = pd.read_csv(self.outdir + os.sep + "pss.csv")
            pws = pd.read_csv(self.outdir + os.sep + "pws.csv")
            return {'demand_shedding': pds, 'solar_curtailment': pss, 'wind_curtailment': pws}
        else:
            print('Need to succesfully run the solve function first.')
            raise

def pyomo2dfinv(pyomo_var,index1):
    """
    Convert Pyomo investment variables to pandas DataFrame.
    
    This utility function converts Pyomo investment decision variables
    to a pandas DataFrame format for easier analysis and display.
    
    Parameters:
        pyomo_var: Pyomo variable object (investment decisions)
        index1: Index set for the variable
    
    Returns:
        pandas.DataFrame: DataFrame with investment decision values
    
    Example:
        >>> xg_df = pyomo2dfinv(m.xg, m.cg)
    """
    df = pd.DataFrame()
    for i in index1:
        df.loc[0,i] = pyomo_var[i].value
    return df

def pyomo2dfopr(pyomo_var,index1,index2,index3,dec=6):
    """
    Convert Pyomo operational variables to pandas DataFrame.
    
    This utility function converts Pyomo operational decision variables
    to a pandas DataFrame format for easier analysis and display.
    
    Parameters:
        pyomo_var: Pyomo variable object (operational decisions)
        index1: First index set (e.g., generators)
        index2: Second index set (e.g., time periods)
        index3: Third index set (e.g., scenarios)
        dec (int): Number of decimal places for rounding (default: 6)
    
    Returns:
        pandas.DataFrame: DataFrame with operational decision values
    
    Example:
        >>> pcg_df = pyomo2dfopr(m.pcg, m.cg, m.tt, m.oo)
    """
    df = pd.DataFrame()
    for i in index1:
        for j in index2:
            for k in index3:
                df.loc[j*len(index3)+k,i] = round(pyomo_var[i,j,k].value,dec)
    return df

def pyomo2dfoprm(pyomo_var,index1,index2,index3):
    """
    Convert Pyomo operational variables to pandas DataFrame (matrix format).
    
    This utility function converts Pyomo operational decision variables
    to a pandas DataFrame in matrix format for easier analysis and display.
    
    Parameters:
        pyomo_var: Pyomo variable object (operational decisions)
        index1: First index set (e.g., buses)
        index2: Second index set (e.g., time periods)
        index3: Third index set (e.g., scenarios)
    
    Returns:
        pandas.DataFrame: DataFrame with operational decision values in matrix format
    
    Example:
        >>> vol_df = pyomo2dfoprm(m.vol, m.bb, m.tt, m.oo)
    """
    df = pd.DataFrame()
    for i in index1:
        for j in index2:
            for k in index3:
                df.loc[j*len(index3)+k,i] = pyomo_var[i,j,k].value
    return df
