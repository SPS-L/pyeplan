import pandas as pd
import pyomo.environ as pe
import os
import shutil 

class invsys:

    def __init__(self,inp_folder='',dshed_cost=1000000,rshed_cost=500,vmin=0.8,vmax=1.2,sbase=100,ref_bus=0):
        """Initialise the investment problem.

        :param str inp_folder: The input directory for the data. It expects to find several CSV files detailing the system input data (Default current folder)
        :param float dshed_cost: Demand Shedding Price (Default 1000000)
        :param float rshed_cost: Renewable Shedding Price (Default 500)
        :param float vmin: Minimum node voltage (Default 0.8)
        :param float vmax: Maximum node voltage (Default 1.2)
        :param float sbase: Base Apparent Power (default 100 MVA)
        :param int ref_bus: Reference node (Default 0)

        :Example:

        >>> import pyeplan
        >>> sys_inv = pyeplan.invsys("3bus_inv")

        """

        self.cgen = pd.read_csv(inp_folder+os.sep+'cgen_dist.csv')
        self.egen = pd.read_csv(inp_folder+os.sep+'egen_dist.csv')
        
        self.cren = pd.read_csv(inp_folder+os.sep+'cren_dist.csv')
        self.eren = pd.read_csv(inp_folder+os.sep+'eren_dist.csv')
        
        self.clin = pd.read_csv(inp_folder+os.sep+'elin_dist.csv')
        self.elin = pd.read_csv(inp_folder+os.sep+'elin_dist.csv')
        
        self.pdem = pd.read_csv(inp_folder+os.sep+'pdem_dist.csv')
        self.qdem = pd.read_csv(inp_folder+os.sep+'qdem_dist.csv')
        
        self.pren = pd.read_csv(inp_folder+os.sep+'pren_dist.csv')
        self.qren = pd.read_csv(inp_folder+os.sep+'qren_dist.csv')
        
        
        self.ncg = len(self.cgen)
        self.neg = len(self.egen)
        
        self.ncr = len(self.cren)
        self.ner = len(self.eren)
        
        self.ncl = len(self.clin)
        self.nel = len(self.elin)
        
        self.nbb = self.pdem.shape[1]
        self.ntt = self.pdem.shape[0]
        
        self.cds = dshed_cost    
        self.crs = rshed_cost    
        self.sb = sbase          
        self.vmin = vmin   
        self.vmax = vmax
        self.inp_folder = inp_folder
       

    def solve(self,solver='cbc',network=True,commit=True):
        """Solve the investment problem.

        :param str solver: the solver to be used (Default is 'cbc')
        :param bool network: Include the network constraints
        :param bool commit: ???

        :returns: ???
        :rtype: int

        :Example:

        >>> import pyeplan
        >>> sys_inv = pyeplan.invsys("3bus_inv")
        >>> sys_inv.solve(outdir='res_inv')

        """
              
        #Define the Model
        m = pe.ConcreteModel()
        
        #Define the Sets
        m.cg = pe.Set(initialize=list(range(self.ncg)),ordered=True)
        m.eg = pe.Set(initialize=list(range(self.neg)),ordered=True)
        
        m.cr = pe.Set(initialize=list(range(self.ncr)),ordered=True)
        m.er = pe.Set(initialize=list(range(self.ner)),ordered=True)
        
        m.cl = pe.Set(initialize=list(range(self.ncl)),ordered=True)
        m.el = pe.Set(initialize=list(range(self.nel)),ordered=True)
        
        m.bb = pe.Set(initialize=list(range(self.nbb)),ordered=True)
        m.tt = pe.Set(initialize=list(range(self.ntt)),ordered=True)

        #Define Variables
        
        #Objective Function
        m.z = pe.Var() 
        
        #Active and Reactive Power Generations (Conventional)
        m.pcg = pe.Var(m.cg,m.tt,within=pe.NonNegativeReals)
        m.peg = pe.Var(m.eg,m.tt,within=pe.NonNegativeReals)
        
        m.qcg = pe.Var(m.cg,m.tt,within=pe.NonNegativeReals)
        m.qeg = pe.Var(m.eg,m.tt,within=pe.NonNegativeReals)
        
        #Active and Reactive Power Generations (Renewable)
        m.pcr = pe.Var(m.cr,m.tt,within=pe.NonNegativeReals)
        m.per = pe.Var(m.er,m.tt,within=pe.NonNegativeReals)
        
        m.qcr = pe.Var(m.cr,m.tt,within=pe.Reals)
        m.qer = pe.Var(m.er,m.tt,within=pe.Reals)
        
        #Demand and Renewable Shedding
        m.pds = pe.Var(m.bb,m.tt,within=pe.Binary)
        m.prs = pe.Var(m.bb,m.tt,within=pe.NonNegativeReals)
        
        #Voltage Magnitude  
        m.vol = pe.Var(m.bb,m.tt,within=pe.Reals,bounds=(self.vmin,self.vmax))
        
        #Active and Reactive Line Flows
        m.pcl = pe.Var(m.cl,m.tt,within=pe.Reals)    #Active Power
        m.pel = pe.Var(m.el,m.tt,within=pe.Reals)    #Active Power
        
        m.qcl = pe.Var(m.cl,m.tt,within=pe.Reals)    #Reactive Power
        m.qel = pe.Var(m.el,m.tt,within=pe.Reals)    #Reactive Power
        
        #Commitment Status
        if commit:
          m.cu = pe.Var(m.cg,m.tt,within=pe.Binary)
          m.eu = pe.Var(m.eg,m.tt,within=pe.Binary)
        else:
          m.cu = pe.Var(m.cg,m.tt,within=pe.NonNegativeReals,bounds=(0,1))
          m.eu = pe.Var(m.eg,m.tt,within=pe.NonNegativeReals,bounds=(0,1))
        
        #Investment Status (Conventional) 
        m.xg = pe.Var(m.cg,within=pe.Binary)
        
        #Investment Status (Renewable) 
        m.xr = pe.Var(m.cr,within=pe.Binary)
        
        #Investment Status (Line) 
        m.xl = pe.Var(m.cr,within=pe.Binary)
        
        #Objective Function
        def obj_rule(m):
            return m.z
        m.obj = pe.Objective(rule=obj_rule)

        #Definition Cost
        def cost_def_rule(m):
            if commit:
                return m.z == sum(self.cgen['icost'][cg]*m.xg[cg] for cg in m.cg) + \
                              sum(self.cren['icost'][cr]*m.xr[cr] for cr in m.cr) + \
                              sum(self.clin['icost'][cl]*m.xl[cl] for cl in m.cl) + \
                              sum(self.cgen['scost'][cg]*m.cu[cg,tt] for cg in m.cg for tt in m.tt) + \
                              sum(self.egen['scost'][eg]*m.cu[eg,tt] for eg in m.eg for tt in m.tt) - \
                              sum(self.cgen['scost'][cg]*m.cu[cg,tt-1] for cg in m.cg for tt in m.tt if tt>1) - \
                              sum(self.egen['scost'][eg]*m.eu[eg,tt-1] for eg in m.eg for tt in m.tt if tt>1) + \
                              self.sb*(sum(self.cgen['ocost'][cg]*m.pcg[cg,tt] for cg in m.cg for tt in m.tt) + \
                                       sum(self.egen['ocost'][eg]*m.peg[eg,tt] for eg in m.eg for tt in m.tt) + \
                                       sum(self.cren['ocost'][cr]*m.pcr[cr,tt] for cr in m.cr for tt in m.tt) + \
                                       sum(self.eren['ocost'][er]*m.per[er,tt] for er in m.er for tt in m.tt) + \
                                       sum(self.cds*self.pdem.iloc[tt,bb]*m.pds[bb,tt] for bb in m.bb for tt in m.tt) + \
                                       sum(self.crs*m.prs[bb,tt] for bb in m.bb for tt in m.tt))
            else:
                return m.z == sum(self.cgen['icost'][cg]*m.xg[cg] for cg in m.cg) + \
                              sum(self.cren['icost'][cr]*m.xr[cr] for cr in m.cr) + \
                              sum(self.clin['icost'][cl]*m.xl[cl] for cl in m.cl) + \
                              self.sb*(sum(self.cgen['ocost'][cg]*m.pcg[cg,tt] for cg in m.cg for tt in m.tt) + \
                                       sum(self.egen['ocost'][eg]*m.peg[eg,tt] for eg in m.eg for tt in m.tt) + \
                                       sum(self.cren['ocost'][cr]*m.pcr[cr,tt] for cr in m.cr for tt in m.tt) + \
                                       sum(self.eren['ocost'][er]*m.per[er,tt] for er in m.er for tt in m.tt) + \
                                       sum(self.cds*self.pdem.iloc[tt,bb]*m.pds[bb,tt] for bb in m.bb for tt in m.tt) + \
                                       sum(self.crs*m.prs[bb,tt] for bb in m.bb for tt in m.tt))
        m.cost_def = pe.Constraint(rule=cost_def_rule)

        #Active Energy Balance
        def act_bal_rule(m,bb,tt):
            return sum(m.pcg[cg,tt] for cg in m.cg if self.cgen['bus'][cg] == bb) + \
                   sum(m.peg[eg,tt] for eg in m.eg if self.egen['bus'][eg] == bb) + \
                   sum(m.pcr[cr,tt] for cr in m.cr if self.cren['bus'][cr] == bb) + \
                   sum(m.per[er,tt] for er in m.er if self.eren['bus'][er] == bb) + \
                   sum(m.pcl[cl,tt] for cl in m.cl if self.clin['to'][cl] == bb) + \
                   sum(m.pel[el,tt] for el in m.el if self.elin['to'][el] == bb) == \
                   sum(m.pcl[cl,tt] for cl in m.cl if self.clin['from'][cl] == bb) + \
                   sum(m.pel[el,tt] for el in m.el if self.elin['from'][el] == bb) + \
                   self.pdem.iloc[tt,bb]*(1 - m.pds[bb,tt])
        m.act_bal = pe.Constraint(m.bb, m.tt, rule=act_bal_rule)
        
        #Reactive Energy Balance
        def rea_bal_rule(m,bb,tt):
            return sum(m.qcg[cg,tt] for cg in m.cg if self.cgen['bus'][cg] == bb) + \
                   sum(m.qeg[eg,tt] for eg in m.eg if self.egen['bus'][eg] == bb) + \
                   sum(m.qcr[cr,tt] for cr in m.cr if self.cren['bus'][cr] == bb) + \
                   sum(m.qer[er,tt] for er in m.er if self.eren['bus'][er] == bb) + \
                   sum(m.qcl[cl,tt] for cl in m.cl if self.clin['to'][cl] == bb) + \
                   sum(m.qel[el,tt] for el in m.el if self.elin['to'][el] == bb) == \
                   sum(m.qcl[cl,tt] for cl in m.cl if self.clin['from'][cl] == bb) + \
                   sum(m.qel[el,tt] for el in m.el if self.elin['from'][el] == bb) + \
                   self.qdem.iloc[tt,bb]*(1 - m.pds[bb,tt])
        m.rea_bal = pe.Constraint(m.bb, m.tt, rule=rea_bal_rule)

        #Minimum Active Generation (Conventional)
        def min_act_cgen_rule(m,cg,tt):
            return m.pcg[cg,tt] >= m.cu[cg,tt]*self.cgen['pmin'][cg]
        m.min_act_cgen = pe.Constraint(m.cg, m.tt, rule=min_act_cgen_rule)
        
        def min_act_egen_rule(m,eg,tt):
            return m.peg[eg,tt] >= m.eu[eg,tt]*self.egen['pmin'][eg]
        m.min_act_egen = pe.Constraint(m.eg, m.tt, rule=min_act_egen_rule)
        
        #Minimum Active Generation (Renewable)
        def min_act_cren_rule(m,cr,tt):
            return m.pcr[cr,tt] >= self.cren['pmin'][cr]
        m.min_act_cren = pe.Constraint(m.cg, m.tt, rule=min_act_cren_rule)
        
        def min_act_eren_rule(m,er,tt):
            return m.per[er,tt] >= self.eren['pmin'][er]
        m.min_act_eren = pe.Constraint(m.eg, m.tt, rule=min_act_eren_rule)

        #Maximum Active Generation (Conventional)
        def max_act_cgen_rule(m,cg,tt):
            return m.pcg[cg,tt] <= m.cu[cg,tt]*self.cgen['pmax'][cg]
        m.max_act_cgen = pe.Constraint(m.cg, m.tt, rule=max_act_cgen_rule)
        
        def max_act_egen_rule(m,eg,tt):
            return m.peg[eg,tt] <= m.eu[eg,tt]*self.egen['pmax'][eg]
        m.max_act_egen = pe.Constraint(m.eg, m.tt, rule=max_act_egen_rule)
        
        #Maximum Active Generation (Renewable)
        def max_act_cren_rule(m,cr,tt):
            return m.pcr[cr,tt] <= m.xr[cr]*self.cren['pmax'][cr]*sum(self.pren.iloc[tt,bb] for bb in m.bb if self.cren['bus'][cr] == bb)
        m.max_act_cren = pe.Constraint(m.cr, m.tt, rule=max_act_cren_rule)
        
        def max_act_eren_rule(m,er,tt):
            return m.per[er,tt] <= self.eren['pmax'][er]*sum(self.pren.iloc[tt,bb] for bb in m.bb if self.eren['bus'][er] == bb)
        m.max_act_eren = pe.Constraint(m.er, m.tt, rule=max_act_eren_rule)
        
        #Minimum Reactive Generation (Conventional)
        def min_rea_cgen_rule(m,cg,tt):
            return m.qcg[cg,tt] >= m.cu[cg,tt]*self.cgen['qmin'][cg]
        m.min_rea_cgen = pe.Constraint(m.cg, m.tt, rule=min_rea_cgen_rule)
        
        def min_rea_egen_rule(m,eg,tt):
            return m.qeg[eg,tt] >= m.eu[eg,tt]*self.egen['qmin'][eg]
        m.min_rea_egen = pe.Constraint(m.eg, m.tt, rule=min_rea_egen_rule)
        
        #Minimum Reactive Generation (Renewable)
        def min_rea_cren_rule(m,cr,tt):
            return m.qcr[cr,tt] >= m.xr[cr]*self.cren['qmin'][cr]
        m.min_rea_cren = pe.Constraint(m.cr, m.tt, rule=min_rea_cren_rule)
        
        def min_rea_eren_rule(m,er,tt):
            return m.qer[er,tt] >= self.eren['qmin'][er]
        m.min_rea_eren = pe.Constraint(m.er, m.tt, rule=min_rea_eren_rule)

        #Maximum Reactive Generation (Conventional)
        def max_rea_cgen_rule(m,cg,tt):
            return m.qcg[cg,tt] <= m.cu[cg,tt]*self.cgen['qmax'][cg]
        m.max_rea_cgen = pe.Constraint(m.cg, m.tt, rule=max_rea_cgen_rule)
        
        def max_rea_egen_rule(m,eg,tt):
            return m.qeg[eg,tt] <= m.eu[eg,tt]*self.egen['qmax'][eg]
        m.max_rea_egen = pe.Constraint(m.eg, m.tt, rule=max_rea_egen_rule)

        #Maximum Reactive Generation (Renewable)
        def max_rea_cren_rule(m,cr,tt):
            return m.qcr[cr,tt] <= m.xr[cr]*self.cren['qmax'][cr]
        m.max_rea_cren = pe.Constraint(m.cr, m.tt, rule=max_rea_cren_rule)
        
        def max_rea_eren_rule(m,er,tt):
            return m.qer[er,tt] <= self.eren['qmax'][er]
        m.max_rea_eren = pe.Constraint(m.er, m.tt, rule=max_rea_eren_rule)
        
        #Maximum Renewable Shedding
        def max_shed_rule(m,bb,tt):
            return m.prs[bb,tt] <= (sum(m.xr[cr]*self.cren['pmax'][cr]*sum(self.pren.iloc[tt,bb] for bb in m.bb if self.cren['bus'][cr] == bb) for cr in m.cr) + \
                                    sum(self.eren['pmax'][er]*sum(self.pren.iloc[tt,bb] for bb in m.bb if self.eren['bus'][er] == bb) for er in m.er)) - \
                                   (sum(m.pcr[cr,tt] for cr in m.cr if self.cren['bus'][cr] == bb) + \
                                    sum(m.per[er,tt] for er in m.er if self.eren['bus'][er] == bb)) 
        m.max_shed = pe.Constraint(m.bb, m.tt, rule=max_shed_rule)

        #Line flow Definition
        def flow_rule(m,cl,el,tt):
            if network:
                if el == cl: 
                    return (m.vol[self.clin['from'][cl],tt] - m.vol[self.clin['to'][cl],tt]) == \
                                  self.clin['res'][cl]*(m.pcl[cl,tt]+m.pel[el,tt]) + \
                                  self.clin['rea'][cl]*(m.qcl[cl,tt]+m.qel[el,tt])
                else: return pe.Constraint.Skip
            else:
                return pe.Constraint.Skip
        m.flow = pe.Constraint(m.cl, m.el, m.tt, rule=flow_rule)
        
        #Max Active Line Flow
        def max_act_cflow_rule(m,cl,tt):
            if network:
              return m.pcl[cl,tt] <= self.clin['pmax'][cl]*m.xl[cl]
            else:
              return pe.Constraint.Skip
        m.max_act_cflow = pe.Constraint(m.cl, m.tt, rule=max_act_cflow_rule)
        
        def max_act_eflow_rule(m,el,tt):
            if network:
              return m.pel[el,tt] <= self.elin['pmax'][el]*self.elin['ini'][el]
            else:
              return pe.Constraint.Skip
        m.max_act_eflow = pe.Constraint(m.el, m.tt, rule=max_act_eflow_rule)

        #Min Active Line Flow
        def min_act_cflow_rule(m,cl,tt):
            if network:
              return m.pcl[cl,tt] >= -self.clin['pmax'][cl]*m.xl[cl]
            else:
              return pe.Constraint.Skip
        m.min_act_cflow = pe.Constraint(m.cl, m.tt, rule=min_act_cflow_rule)
        
        def min_act_eflow_rule(m,el,tt):
            if network:
              return m.pel[el,tt] >= -self.elin['pmax'][el]*self.elin['ini'][el]
            else:
              return pe.Constraint.Skip
        m.min_act_eflow = pe.Constraint(m.el, m.tt, rule=min_act_eflow_rule)

        #Max Reactive Line Flow
        def max_rea_cflow_rule(m,cl,tt):
            if network:
              return m.qcl[cl,tt] <= self.clin['qmax'][cl]*m.xl[cl]
            else:
              return pe.Constraint.Skip
        m.max_rea_cflow = pe.Constraint(m.cl, m.tt, rule=max_rea_cflow_rule)
        
        def max_rea_eflow_rule(m,el,tt):
            if network:
              return m.qel[el,tt] <= self.elin['qmax'][el]*self.elin['ini'][el]
            else:
              return pe.Constraint.Skip
        m.max_rea_eflow = pe.Constraint(m.el, m.tt, rule=max_rea_eflow_rule)

        #Min Reactive Line Flow
        def min_rea_cflow_rule(m,cl,tt):
            if network:
              return m.qcl[cl,tt] >= -self.clin['qmax'][cl]*m.xl[cl]
            else:
              return pe.Constraint.Skip
        m.min_rea_cflow = pe.Constraint(m.cl, m.tt, rule=min_rea_cflow_rule)
        
        def min_rea_eflow_rule(m,el,tt):
            if network:
              return m.qel[el,tt] >= -self.elin['qmax'][el]*self.elin['ini'][el]
            else:
              return pe.Constraint.Skip
        m.min_rea_eflow = pe.Constraint(m.el, m.tt, rule=min_rea_eflow_rule)
        
        #Voltage Magnitude at Reference Bus
        def vol_ref_rule(m,tt):
            if network:
                return sum(m.vol[bb,tt] for bb in m.bb if bb==0) == 1
            else:
                return pe.Constraint.Skip
        m.vol_ref = pe.Constraint(m.tt, rule=vol_ref_rule)
        
        #Investment Status 
        def inv_stat_rule(m,cg,tt):
            return m.cu[cg,tt] <= m.xg[cg] 
        m.inv_stat = pe.Constraint(m.cg, m.tt, rule=inv_stat_rule)
        
        #Solve the optimization problem
        solver_manager = pe.SolverManagerFactory('neos')
        opt = pe.SolverFactory(solver)
        opt.options['threads'] = 1
        opt.options['mipgap'] = 1e-9
        result = solver_manager.solve(m,opt=opt,symbolic_solver_labels=True,tee=True)
        print(result['Solver'][0])
        print(m.display())

        #Save the results
        self.output = m
        
        self.xg_output = pyomo2dfinv(m.xg,m.cg).T
        self.xr_output = pyomo2dfinv(m.xr,m.cr).T
        self.xl_output = pyomo2dfinv(m.xl,m.cl).T
        
        self.cu_output = pyomo2dfopr(m.cu,m.cg,m.tt).T
        self.eu_output = pyomo2dfopr(m.eu,m.eg,m.tt).T
        
        self.pcg_output = pyomo2dfopr(m.pcg,m.cg,m.tt).T
        self.qcg_output = pyomo2dfopr(m.qcg,m.cg,m.tt).T
        
        self.peg_output = pyomo2dfopr(m.peg,m.eg,m.tt).T
        self.qeg_output = pyomo2dfopr(m.qeg,m.eg,m.tt).T
        
        self.pcr_output = pyomo2dfopr(m.pcr,m.cr,m.tt).T
        self.qcr_output = pyomo2dfopr(m.qcr,m.cr,m.tt).T
        
        self.per_output = pyomo2dfopr(m.per,m.er,m.tt).T
        self.qer_output = pyomo2dfopr(m.qer,m.er,m.tt).T
        
        self.pds_output = pyomo2dfopr(m.pds,m.bb,m.tt).T
        self.prs_output = pyomo2dfopr(m.prs,m.bb,m.tt).T
        
        self.vol_output = pyomo2dfopr(m.vol,m.bb,m.tt).T
        
        self.pcl_output = pyomo2dfopr(m.pcl,m.cl,m.tt).T
        self.qcl_output = pyomo2dfopr(m.qcl,m.cl,m.tt).T
        
        self.pel_output = pyomo2dfopr(m.pel,m.cl,m.tt).T
        self.qel_output = pyomo2dfopr(m.qel,m.cl,m.tt).T

        # Setup the results folder
        outdir = self.inp_folder + os.sep + 'results'
        if os.path.exists(outdir):
            shutil.rmtree(outdir) 
        os.makedirs(outdir)
        
        self.xg_output.to_csv(outdir+os.sep+'investment_conventional.csv',index=False)
        self.xr_output.to_csv(outdir+os.sep+'investment_renewable.csv',index=False)
        self.xr_output.to_csv(outdir+os.sep+'investment_line.csv',index=False)
        
        self.cu_output.to_csv(outdir+os.sep+'cu.csv',index=False)
        self.eu_output.to_csv(outdir+os.sep+'eu.csv',index=False)
        
        self.pcg_output.to_csv(outdir+os.sep+'pcg.csv',index=False)
        self.qcg_output.to_csv(outdir+os.sep+'qcg.csv',index=False)
        
        self.peg_output.to_csv(outdir+os.sep+'peg.csv',index=False)
        self.qeg_output.to_csv(outdir+os.sep+'qeg.csv',index=False)
        
        self.pcr_output.to_csv(outdir+os.sep+'pcr.csv',index=False)
        self.qcr_output.to_csv(outdir+os.sep+'qcr.csv',index=False)
        
        self.per_output.to_csv(outdir+os.sep+'per.csv',index=False)
        self.qer_output.to_csv(outdir+os.sep+'qer.csv',index=False)
        
        self.pds_output.to_csv(outdir+os.sep+'pds.csv',index=False)
        self.prs_output.to_csv(outdir+os.sep+'prs.csv',index=False)
        
        self.vol_output.to_csv(outdir+os.sep+'vol.csv',index=False)
       
        self.pcl_output.to_csv(outdir+os.sep+'pcl.csv',index=False)
        self.qcl_output.to_csv(outdir+os.sep+'qcl.csv',index=False)
        
        self.pel_output.to_csv(outdir+os.sep+'pel.csv',index=False)
        self.qel_output.to_csv(outdir+os.sep+'qel.csv',index=False)

def pyomo2dfinv(pyomo_var,index1):
    mat = []
    for i in index1:
        row = []
        row.append(pyomo_var[i].value)
        mat.append(row)
    return pd.DataFrame(mat)

def pyomo2dfopr(pyomo_var,index1,index2,dec=6):
    mat = []
    for i in index1:
        row = []
        for j in index2:
            row.append(round(pyomo_var[i,j].value,dec))
        mat.append(row)
    return pd.DataFrame(mat)
