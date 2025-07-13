"""
Network Routing and Topology Optimization Module.

This module provides functionality for network routing and topology optimization
of microgrid systems. It implements minimum spanning tree algorithms for optimal
network design and calculates electrical parameters for distribution networks.

The module includes:
- Geographic distance calculations using Haversine formula
- Minimum spanning tree algorithm for network topology optimization
- Cable parameter calculations and electrical line specifications
- Network visualization capabilities with matplotlib and mplleaflet

Classes:
    rousys: Main class for routing system operations

Functions:
    distance: Calculate geographical distance between two points

References:
- Dehghan, S., Nakiganda, A., & Aristidou, P. (2020). "Planning and Operation of 
  Resilient Microgrids: A Comprehensive Review." IEEE Transactions on Smart Grid.
- Nakiganda, A., Dehghan, S., & Aristidou, P. (2021). "PyEPlan: An Open-Source 
  Framework for Microgrid Planning and Operation." IEEE Power & Energy Society 
  General Meeting.

Example:
    >>> from pyeplan.routing import rousys
    >>> route_sys = rousys("input_folder", crs=35, typ=7, vbase=415)
    >>> route_sys.min_spn_tre()
"""

import numpy as np 
import pandas as pd 
import networkx as nx
import matplotlib.pyplot as plt
import math
import os
import shutil
import mplleaflet



class rousys:
    """
    Routing system class for microgrid network topology optimization.
    
    This class implements minimum spanning tree algorithms and electrical parameter
    calculations for microgrid network design. It processes geographical data,
    calculates optimal network topologies, and generates electrical line specifications.
    
    Attributes:
        geol (pd.DataFrame): Geographical locations of all nodes (latitude/longitude)
        node (int): Number of nodes in the network
        cblt (pd.DataFrame): Cable parameters and specifications
        crs (int): Cross section of cables in mm²
        typ (int): Type of cables
        vbase (float): Line-to-line voltage in V
        sbase (float): Base three-phase apparent power in VA
        zbase (float): Base impedance in Ω
        ibase (float): Base current in A
        r (float): Per-unit resistance of selected cable
        x (float): Per-unit reactance of selected cable
        i (float): Per-unit current rating of selected cable
        p (float): Per-unit active power limit
        q (float): Per-unit reactive power limit
        inp_folder (str): Input folder path for data files
    
    Methods:
        min_spn_tre(): Generate minimum spanning tree network topology
    """
    
    def __init__(self, inp_folder = '', crs = 35, typ = 7, vbase = 415, sbase = 1):
        """
        Initialize the routing system.
        
        Parameters:
            inp_folder (str): Input folder path containing data files (default: '')
            crs (int): Cross section of cables in mm² (default: 35)
            typ (int): Type of cables (default: 7)
            vbase (float): Line-to-line voltage in V (default: 415)
            sbase (float): Base apparent power in kW (default: 1)
        
        Required input files:
            - geol_dist.csv: Geographical coordinates of nodes
            - cblt_dist.csv: Cable parameters and specifications
        
        Example:
            >>> route_sys = rousys("input_folder", crs=35, typ=7, vbase=415, sbase=1)
        """
        
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
        self.zbase = (self.vbase**2)/self.sbase
        
        #Base curent
        self.ibase = self.sbase/(math.sqrt(3)*self.vbase)
        
        #Calculations of line/cable parameters 
        self.r = self.cblt.loc[self.cblt['crs'] == crs,'r'+str(typ)].values[0]*1e-3/self.zbase
        self.x = self.cblt.loc[self.cblt['crs'] == crs,'x'+str(typ)].values[0]*1e-3/self.zbase
        self.i = self.cblt.loc[self.cblt['crs'] == crs,'i'+str(typ)].values[0]/self.ibase
        self.p = (math.sqrt(2)/2)*self.i
        self.q = (math.sqrt(2)/2)*self.i
        self.inp_folder = inp_folder

    
    def min_spn_tre(self):
        """
        Generate minimum spanning tree network topology.
        
        This method implements Kruskal's minimum spanning tree algorithm to find
        the optimal network topology that connects all nodes with minimum total
        cable length. It creates network visualizations and generates output files
        for routing and electrical line specifications.
        
        Output files generated:
            - path.png: Network topology visualization
            - rou_dist.csv: Routing distances between connected nodes
            - elin_dist.csv: Electrical line parameters and specifications
        
        The method performs the following steps:
        1. Creates a complete graph with all nodes
        2. Calculates distances between all node pairs
        3. Applies minimum spanning tree algorithm
        4. Generates network visualizations
        5. Creates routing and electrical parameter files
        
        Example:
            >>> route_sys = rousys("input_folder")
            >>> route_sys.min_spn_tre()
        """
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
        # mplleaflet.show(fig=ax.figure)  # Commented out due to matplotlib compatibility issues 
        

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

def distance(origin, destination):
    """
    Calculate geographical distance between two points using Haversine formula.
    
    This function computes the great-circle distance between two points on Earth's
    surface given their latitude and longitude coordinates. It uses the Haversine
    formula which accounts for the spherical shape of the Earth.
    
    Parameters:
        origin (tuple): (latitude, longitude) of the origin point in decimal degrees
        destination (tuple): (latitude, longitude) of the destination point in decimal degrees
    
    Returns:
        float: Distance between the two points in meters
    
    Notes:
        - Latitude: positive for North, negative for South
        - Longitude: positive for East, negative for West
        - Uses Earth's radius of 6,371,000 meters
        - Returns distance in meters
    
    Example:
        >>> dist = distance((0.25, 32.40), (0.26, 32.41))
        >>> print(f"Distance: {dist:.2f} meters")
    """
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
