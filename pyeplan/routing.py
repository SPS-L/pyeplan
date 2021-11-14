import numpy as np 
import pandas as pd 
import networkx as nx
import matplotlib.pyplot as plt
import math
import os
import shutil
import mplleaflet



class rousys:
    def __init__(self, inp_folder = '', crs = 35, typ = 7, vbase = 415, sbase = 1):
        
        #Geogaphical locations of all nodes
        self.geol = pd.read_csv(inp_folder + os.sep + 'geol_dist.csv')     
        
        #Number of all nodes 
        self.node = len(self.geol)     

        #Parameters of cables                        
        self.cblt = pd.read_csv(inp_folder + os.sep + 'cblt_dist.csv')
        
        #Cross section of cables [mm]
        self.crs = crs     

         #Type of cables                                 
        self.typ = typ   

        #Line-to-Line voltage [V]                                  
        self.vbase = vbase                                  
        
        #Base three-phase apparnet power [VA] 
        self.sbase = 1000*sbase         

        #Base impedance                          
        self.zbase = (vbase**2)/sbase
        
        #Base curent
        self.ibase = sbase/(math.sqrt(3)*vbase)
        
        #Calculations of line/cable parameters 
        self.r = self.cblt.loc[self.cblt['crs'] == crs,'r'+str(typ)].values[0]*1e-3/self.zbase
        self.x = self.cblt.loc[self.cblt['crs'] == crs,'x'+str(typ)].values[0]*1e-3/self.zbase
        self.i = self.cblt.loc[self.cblt['crs'] == crs,'i'+str(typ)].values[0]/self.ibase
        self.p = (math.sqrt(2)/2)*self.i
        self.q = (math.sqrt(2)/2)*self.i
        self.inp_folder = inp_folder

    
    #Minimum spanning tree algorithm  
    def min_spn_tre(self):
        G = nx.Graph()
        
        for n in range(self.node):
            G.add_node(n,pos =(self.geol['Longtitude'][n], self.geol['Latitude'][n]))
            
        for n in range(self.node):
            for m in range(self.node):
                if n != m:
                    G.add_edge(n,m,weight=distance((self.geol['Longtitude'][n], self.geol['Latitude'][n]), (self.geol['Longtitude'][m], self.geol['Latitude'][m])))
        T = nx.minimum_spanning_tree(G)
        nx.draw(T, nx.get_node_attributes(T,'pos'),node_size=5, width = 2, node_color = 'red', edge_color='blue')
        plt.savefig("path.png")
        
        fig, ax = plt.subplots()
        pos = nx.get_node_attributes(T,'pos')
        nx.draw_networkx_nodes(T,pos=pos,node_size=10,node_color='red')
        nx.draw_networkx_edges(T,pos=pos,edge_color='blue')
        mplleaflet.show(fig=ax.figure) 
        

        rou_dist = pd.DataFrame(sorted(T.edges(data=True)))
        rou_dist = rou_dist.rename({0: 'from', 1: 'to', 2: 'distance'}, axis=1) 
        dist = rou_dist.loc[:, 'distance']
        rou_dist['distance'] = [d.get('weight') for d in dist] 
        rou_dist.to_csv(self.inp_folder + os.sep + 'rou_dist.csv', index=False)
        
        elin_dist = rou_dist.loc[:,'from':'to']
        elin_dist['ini'] = 1  
        elin_dist['res'] = [self.r*d.get('weight') for d in dist]
        elin_dist['rea'] = [self.x*d.get('weight') for d in dist]
        elin_dist['sus'] = [0 for d in dist]
        elin_dist['pmax'] = self.p
        elin_dist['qmax'] = self.q
        elin_dist.to_csv(self.inp_folder + os.sep + 'elin_dist.csv', index=False)

#Convert latitude and longtitude to XY coordinates 
def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    # Radius in meter
    radius = 6371000  

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
    * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d
