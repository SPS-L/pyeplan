import pandas as pd
import pyomo.environ as pe
import csv
import os
import shutil 

class inosys:

    def __init__(self, inp_folder, ref_bus, dshed_cost = 1000000, rshed_cost = 500, phase = 3, vmin=0.85, vmax=1.15, sbase = 1, sc_fa = 1):
        
        '''
        Initialise the investment and operation problem.
        :param str inp_folder: The input directory for the data. It expects to find several CSV files detailing the system input data (Default current folder)
        :param float dshed_cost: Demand Shedding Price (Default 1000000)
        :param float rshed_cost: Renewable Shedding Price (Default 500)
        :param int phase: Number of Phases (Default 3)
        :param float vmin: Minimum node voltage (Default 0.85)
        :param float vmax: Maximum node voltage (Default 1.15)
        :param float sbase: Base Apparent Power (Default 1 kW)
        :param int ref_bus: Reference node
        :param float sc_fa: Scaling Factor (Default 1)
        :Example:
        >>> import pyeplan
        >>> sys_inv = pyeplan.inosys("wat_inv", ref_bus = 260)
        '''
        
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


    def solve(self, solver = 'glpk', neos = False, invest = False, onlyopr = True, commit = False, solemail = ''):
        '''
        Solve the investment and operation problem.
        :param str solver: Solver to be used. Available: glpk, cbc, ipopt, gurobi
        :param bool network: True/False indicates including/excluding network-related constraints 
        :param bool invest: True/False indicates binary/continuous nature of investement-related decision variables 
        :param bool onlyopr: True/False indicates if the problem will only solve the operation or both investment and operation
        :param bool commit: True/False indicates if ???
        :param bool neos: True/False indicates if ???
        :Example:
        >>> import pyeplan
        >>> sys_inv = pyeplan.inosys("wat_inv", ref_bus = 260)
        >>> sys_inv.solve()
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
        opt = pe.SolverFactory(solver)
        if solver == 'gurobi':
            opt.options['threads'] = 0
            opt.options['mipgap'] = 0
        if neos:
            os.environ['NEOS_EMAIL'] = solemail
            solver_manager = pe.SolverManagerFactory('neos')
            result = solver_manager.solve(m,opt=opt,symbolic_solver_labels=True,tee=True)
        else:
            result = opt.solve(m,symbolic_solver_labels=True,tee=True)
        
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
        outdir = self.inp_folder + os.sep + 'results'
        if os.path.exists(outdir):
            shutil.rmtree(outdir) 
        os.makedirs(outdir)
        
        with open(outdir + os.sep + 'obj.csv', 'w', newline='') as csvfile:
            thewriter = csv.writer(csvfile)   
            thewriter.writerow(['total costs', self.total])
            thewriter.writerow(['total investment costs', self.total_inv])
            thewriter.writerow(['total operation costs', self.total_opr])
        
        self.xg_output.to_csv(outdir + os.sep + 'xg.csv', index=False)
        self.xs_output.to_csv(outdir + os.sep + 'xs.csv', index=False)
        self.xw_output.to_csv(outdir + os.sep + 'xw.csv', index=False)
        self.xb_output.to_csv(outdir + os.sep + 'xb.csv', index=False)
        
        self.cu_output.to_csv(outdir + os.sep + 'cu.csv', index=False)
        self.eu_output.to_csv(outdir + os.sep + 'eu.csv', index=False)
        
        self.pcg_output.to_csv(outdir + os.sep + 'pcg.csv', index=False)
        self.qcg_output.to_csv(outdir + os.sep + 'qcg.csv', index=False)
        
        self.peg_output.to_csv(outdir + os.sep + 'peg.csv', index=False)
        self.qeg_output.to_csv(outdir + os.sep + 'qeg.csv', index=False)
        
        self.pcs_output.to_csv(outdir + os.sep + 'pcs.csv',index=False)
        self.qcs_output.to_csv(outdir + os.sep + 'qcs.csv',index=False)
        
        self.pes_output.to_csv(outdir + os.sep + 'pes.csv',index=False)
        self.qes_output.to_csv(outdir + os.sep + 'qes.csv',index=False)
        
        self.pcw_output.to_csv(outdir + os.sep + 'pcw.csv',index=False)
        self.qcw_output.to_csv(outdir + os.sep + 'qcw.csv',index=False)
        
        self.pew_output.to_csv(outdir + os.sep + 'pew.csv',index=False)
        self.qew_output.to_csv(outdir + os.sep + 'qew.csv',index=False)
        
        self.pbc_output.to_csv(outdir + os.sep + 'pbc.csv',index=False)
        self.pbd_output.to_csv(outdir + os.sep + 'pbd.csv',index=False)
        self.qcd_output.to_csv(outdir + os.sep + 'qcd.csv',index=False)
        
        self.pds_output.to_csv(outdir + os.sep + 'pds.csv',index=False)
        self.pss_output.to_csv(outdir + os.sep + 'pss.csv',index=False)
        self.pws_output.to_csv(outdir + os.sep + 'pws.csv',index=False)
        
        self.vol_output.to_csv(outdir + os.sep + 'vol.csv',index=False)
        
        self.pel_output.to_csv(outdir + os.sep + 'pel.csv',index=False)
        self.qel_output.to_csv(outdir + os.sep + 'qel.csv',index=False)

def pyomo2dfinv(pyomo_var,index1):
    mat = []
    for i in index1:
        row = []
        row.append(pyomo_var[i].value)
        mat.append(row)
    return pd.DataFrame(mat)


def pyomo2dfopr(pyomo_var,index1,index2,index3,dec=6):
    mat = []
    for i in index1:
        row = []
        for k in index3:
            for j in index2:
                row.append(round(pyomo_var[i,j,k].value,dec))
        mat.append(row)
    return pd.DataFrame(mat)

def pyomo2dfoprm(pyomo_var,index1,index2,index3):
    mat = []
    for i in index1:
        row = []
        for k in index3:
            for j in index2: 
                row.append(pyomo_var[i,j,k].value)
        mat.append(row)
    return pd.DataFrame(mat)