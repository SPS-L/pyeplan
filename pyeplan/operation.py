import pandas as pd
import pyomo.environ as pe
import os

class opersys:

    def __init__(self,folder,dshed_cost=1000,rshed_cost=500,vmin=0.8,vmax=1.2,sbase=100,ref_bus=0):

        self.gen = pd.read_csv(folder+os.sep+'gen_dist.csv')
        self.lin = pd.read_csv(folder+os.sep+'lin_dist.csv')
        self.pde = pd.read_csv(folder+os.sep+'pde_dist.csv')
        self.qde = pd.read_csv(folder+os.sep+'qde_dist.csv')
        self.pre = pd.read_csv(folder+os.sep+'pre_dist.csv')
        self.ng = len(self.gen)
        self.nl = len(self.lin)
        self.nb = self.pde.shape[1]
        self.nt = self.pde.shape[0]
        self.cds = dshed_cost    #Demand Shedding Price
        self.crs = rshed_cost    #Renewable Shedding Price
        self.sb = sbase          #Base Apparent Power 
        self.vmin = vmin   
        self.vmax = vmax
       

    def solve(self,solver='cbc',network=True,commit=True,outdir='results'):
        
        #Define the Model
        m = pe.ConcreteModel()
        
        #Define the Sets
        m.g = pe.Set(initialize=list(range(self.ng)),ordered=True)
        m.l = pe.Set(initialize=list(range(self.nl)),ordered=True)
        m.b = pe.Set(initialize=list(range(self.nb)),ordered=True)
        m.t = pe.Set(initialize=list(range(self.nt)),ordered=True)

        #Define Variables
        
        #Objective Function
        m.z = pe.Var() 
        
        #Active and Reactive Power Generations
        m.pgg = pe.Var(m.g,m.t,within=pe.NonNegativeReals)
        m.qgg = pe.Var(m.g,m.t,within=pe.Reals)
        
        #Demand and Renewable Shedding
        m.pds = pe.Var(m.b,m.t,within=pe.Binary)
        m.prs = pe.Var(m.b,m.t,within=pe.NonNegativeReals)
        
        #Voltage Magnitude  
        m.vol = pe.Var(m.b,m.t,within=pe.Reals,bounds=(self.vmin,self.vmax))
        
        #Active and Reactive Line Flows
        m.pll = pe.Var(m.l,m.t,within=pe.Reals)    #Active Power
        m.qll = pe.Var(m.l,m.t,within=pe.Reals)    #Reactive Power
        
        if commit:
          m.u = pe.Var(m.g,m.t,within=pe.Binary)
        else:
          m.u = pe.Var(m.g,m.t,within=pe.NonNegativeReals,bounds=(0,1))
        

        #Objective Function
        def obj_rule(m):
            return m.z
        m.obj = pe.Objective(rule=obj_rule)

        #Definition Cost
        def cost_def_rule(m):
            if commit:
                return m.z == sum(self.gen['start'][g]*m.u[g,t] for g in m.g for t in m.t) - sum(self.gen['start'][g]*m.u[g,t-1] for g in m.g for t in m.t if t>1) + self.sb*(sum(self.gen['cost'][g]*m.pgg[g,t] for g in m.g for t in m.t) + sum(self.cds*self.pde.iloc[t,b]*m.pds[b,t] for b in m.b for t in m.t) + sum(self.crs*m.prs[b,t] for b in m.b for t in m.t))
            else:
                return m.z == self.sb*(sum(self.gen['cost'][g]*m.pgg[g,t] for g in m.g for t in m.t) + sum(self.cds*self.pde.iloc[t,b]*m.pds[b,t] for b in m.b for t in m.t) + sum(self.crs*m.prs[b,t] for b in m.b for t in m.t))
        m.cost_def = pe.Constraint(rule=cost_def_rule)

        #Active Energy Balance
        def act_bal_rule(m,b,t):
            return sum(m.pgg[g,t] for g in m.g if self.gen['bus'][g] == b) + self.pre.iloc[t,b] + sum(m.pll[l,t] for l in m.l if self.lin['to'][l] == b) == self.pde.iloc[t,b]*(1 - m.pds[b,t]) + m.prs[b,t] + sum(m.pll[l,t] for l in m.l if self.lin['from'][l] == b)
        m.act_bal = pe.Constraint(m.b, m.t, rule=act_bal_rule)
        
        #Reactive Energy Balance
        def rea_bal_rule(m,b,t):
            return sum(m.qgg[g,t] for g in m.g if self.gen['bus'][g] == b) + sum(m.qll[l,t] for l in m.l if self.lin['to'][l] == b) == self.qde.iloc[t,b]*(1 - m.pds[b,t]) + sum(m.qll[l,t] for l in m.l if self.lin['from'][l] == b)
        m.rea_bal = pe.Constraint(m.b, m.t, rule=rea_bal_rule)

        #Minimum Active Generation
        def min_act_gen_rule(m,g,t):
            return m.pgg[g,t] >= m.u[g,t]*self.gen['pmin'][g]
        m.min_act_gen = pe.Constraint(m.g, m.t, rule=min_act_gen_rule)

        #Maximum Active Generation
        def max_act_gen_rule(m,g,t):
            return m.pgg[g,t] <= m.u[g,t]*self.gen['pmax'][g]
        m.max_act_gen = pe.Constraint(m.g, m.t, rule=max_act_gen_rule)
        
        #Minimum Reactive Generation
        def min_rea_gen_rule(m,g,t):
            return m.qgg[g,t] >= m.u[g,t]*self.gen['qmin'][g]
        m.min_rea_gen = pe.Constraint(m.g, m.t, rule=min_rea_gen_rule)

        #Maximum Reactive Generation
        def max_rea_gen_rule(m,g,t):
            return m.qgg[g,t] <= m.u[g,t]*self.gen['qmax'][g]
        m.max_rea_gen = pe.Constraint(m.g, m.t, rule=max_rea_gen_rule)

        #Maximum Renewable Shedding
        def max_shed_rule(m,b,t):
            return m.prs[b,t] <= self.pre.iloc[t,b]
        m.max_shed = pe.Constraint(m.b, m.t, rule=max_shed_rule)

        #Line flow Definition
        def flow_rule(m,l,t):
            if network:
                return (m.vol[self.lin['from'][l],t] - m.vol[self.lin['to'][l],t]) == self.lin['res'][l]*m.pll[l,t] + self.lin['rea'][l]*m.qll[l,t]
            else:
                return pe.Constraint.Skip
        m.flow = pe.Constraint(m.l, m.t, rule=flow_rule)

        #Max Active Line Flow
        def max_act_flow_rule(m,l,t):
            if network:
              return m.pll[l,t] <= self.lin['pmax'][l]
            else:
              return pe.Constraint.Skip
        m.max_act_flow = pe.Constraint(m.l, m.t, rule=max_act_flow_rule)

        #Min Active Line Flow
        def min_act_flow_rule(m,l,t):
            if network:
              return m.pll[l,t] >= -self.lin['pmax'][l]
            else:
              return pe.Constraint.Skip
        m.min_act_flow = pe.Constraint(m.l, m.t, rule=min_act_flow_rule)

        #Max Reactive Line Flow
        def max_rea_flow_rule(m,l,t):
            if network:
              return m.qll[l,t] <= self.lin['qmax'][l]
            else:
              return pe.Constraint.Skip
        m.max_rea_flow = pe.Constraint(m.l, m.t, rule=max_rea_flow_rule)

        #Min Reactive Line Flow
        def min_rea_flow_rule(m,l,t):
            if network:
              return m.qll[l,t] >= -self.lin['qmax'][l]
            else:
              return pe.Constraint.Skip
        m.min_rea_flow = pe.Constraint(m.l, m.t, rule=min_rea_flow_rule)
        
        #Voltage Magnitude at Reference Bus
        def vol_ref_rule(m,t):
            if network:
                return sum(m.vol[b,t] for b in m.b if b==0) == 1
            else:
                return pe.Constraint.Skip
        m.vol_ref = pe.Constraint(m.t, rule=vol_ref_rule)
        
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
        
        self.u_output = pyomo2df(m.u,m.g,m.t).T
        
        self.pgg_output = pyomo2df(m.pgg,m.g,m.t).T
        self.qgg_output = pyomo2df(m.qgg,m.g,m.t).T
        
        self.pds_output = pyomo2df(m.pds,m.b,m.t).T
        self.prs_output = pyomo2df(m.prs,m.b,m.t).T
        
        self.vol_output = pyomo2df(m.vol,m.b,m.t).T
        
        self.pll_output = pyomo2df(m.pll,m.l,m.t).T
        self.qll_output = pyomo2df(m.qll,m.l,m.t).T

        # Check if output folder exists
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        
        self.u_output.to_csv(outdir+os.sep+'u.csv',index=False)
        
        self.pgg_output.to_csv(outdir+os.sep+'pg.csv',index=False)
        self.qgg_output.to_csv(outdir+os.sep+'qg.csv',index=False)
        
        self.pds_output.to_csv(outdir+os.sep+'pds.csv',index=False)
        self.prs_output.to_csv(outdir+os.sep+'prs.csv',index=False)
        
        self.vol_output.to_csv(outdir+os.sep+'vol.csv',index=False)
       
        self.pll_output.to_csv(outdir+os.sep+'pl.csv',index=False)
        self.qll_output.to_csv(outdir+os.sep+'ql.csv',index=False)

def pyomo2df(pyomo_var,index1,index2,dec=6):
    mat = []
    for i in index1:
        row = []
        for j in index2:
            row.append(round(pyomo_var[i,j].value,dec))
        mat.append(row)
    return pd.DataFrame(mat)
