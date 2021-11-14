import pandas as pd
import numpy as np
import urllib.request
import urllib.parse
import matplotlib.pyplot as plt
import math 
import os
import shutil 
from timezonefinder import TimezoneFinder
from sklearn.cluster import KMeans


class datsys:
    def __init__(self, inp_folder = '', lat = 0.251148605450955, lon = 32.404833929733,year = 2016, pvcalc = 1, pp = 50, sys_loss = 14, n_clust = 1, pf_c = 1, pf_p = 1, sbase = 1000):
        
        
        '''
        Initialise the Data Processing module. The PVGIS tool (https://ec.europa.eu/jrc/en/pvgis) has been  
        to collect renewable production data sets at different locations across the world.  
        '''
        self.loc = pd.read_excel(inp_folder + os.sep + 'mgpc_dist.xlsx', sheet_name = 'Load Point', skiprows= 0, usecols = 'A,B')
        
        self.pdem = pd.read_excel(inp_folder + os.sep + 'mgpc_dist.xlsx', sheet_name = 'Load Point', skiprows= 0, usecols = 'D:AA')
        
        self.prep = pd.read_excel(inp_folder + os.sep + 'mgpc_dist.xlsx', sheet_name = 'Load Level', skiprows= 0, skipfooter=0, usecols = 'B')
        
        #Latitude (in decimal degrees, south is negative)
        self.lat = lat 
        
        #Longitude (in decimal degrees, west is negative)
        self.lon = lon 
        
        #Raddatabase = 'PVGIS-SARAH' #Name of the radiation database (DB): "PVGIS-SARAH" for Europe, Africa and Asia  are PVGIS-SARAH, PVGIS-NSRDB and PVGIS-ERA5 based on the chosen location.
        
        #Start year of data collection 
        self.startyear = year
        
        #End year of data collection 
        self.endyear = year
        
        #Calculation method of PV output parameters: pvcalc = 0 -> solar radiation calculations, pvcalc = 1 -> solar radiation and power production calculations        
        self.pvcalculation = pvcalc 
        
        #Nominal power of the PV system [kW]
        self.peakpower = pp 
        
        #Sum of system losses [%]
        self.loss = sys_loss 
        
        #Type of sun tracking
        self.trackingtype = 2 
        '''
        0 = fixed 
        1 = single horizontal axis aligned north-south, 
        2 = two-axis tracking,
        3 = vertical axis tracking, 
        4 = single horizontal axis aligned east-west, 
        5 = single inclined axis aligned north-south
        '''
        
        #Calculate the optimum inclination angle
        self.optimalinclination =  1 
        '''
        Value of 1 for "yes". All other values (or no value) mean "no". Not relevant for 2-axis tracking.
        '''
        
        #Calculate the optimum inclination AND orientation angles#
        self.optimalangles =  1 
        '''
        Value of 1 for "yes". All other values (or no value) mean "no". Not relevant for tracking planes.
        '''
        
        #Type of output.
        self.outputformat = 'basic' 
        ''' 
        Choices: 
        "csv"  
        "basic"  
        "json" 
        '''
        
        #Format of outpout
        '''
        0 = output as stream 
        1 = output as file 
        '''
        self.browser = 1
        
        #Number of clusters 
        self.n_clust = n_clust
        
        #Power Factor at each consumption point 
        self.pf_c = pf_c
        
        #Power factor at each production point (renewable)
        self.pf_p = pf_p
        
        #Base apparent power 
        self.sbase = sbase
        
        #Data extraction from PVGIS
        self.data_link = 'https://re.jrc.ec.europa.eu/api/seriescalc'
        self.data_link = self.data_link + '?lat=' + str(self.lat) + '&lon=' + str(self.lon) 
        self.data_link = self.data_link + '&startyear=' + str(self.startyear) + '&endyear=' + str(self.endyear) 
        self.data_link = self.data_link + '&pvcalculation=' + str(self.pvcalculation) + '&peakpower=' + str(self.peakpower) 
        self.data_link = self.data_link + '&loss=' + str(self.loss) + '&trackingtype=' + str(self.trackingtype)
        self.data_link = self.data_link + '&optimalinclination=' + str(self.optimalinclination) + '&optimalangles=' + str(self.optimalangles)
        self.data_link = self.data_link + '&outputformat=' + self.outputformat + '&browser=' + str(self.browser)
        self.data = pd.read_csv(urllib.request.urlopen(self.data_link), skiprows=2, header=None) 
    
        '''
        Data columns description as described by PVGIS:
            
        Time = Date and hour
        P = PV system power (W) ** Column not included if pvcalc = 0
        G(i) = Global irradiance on the inclined plane (plane of the array) (W/m2)
        H_sun = Sun height (degree)
        T2m = 2-m air temperature (degree Celsius)
        WS10m = 10-m total wind speed (m/s)
        Int = 1 means solar radiation values are reconstructed
        
        '''
        
        #Finding timezone based on latitude and longitude 
        tf = TimezoneFinder()
        self.local_time_zone = tf.timezone_at(lng=self.lon, lat=self.lat)
    
        #Calculating active and reactive power at each load point   
        self.prep = self.prep[np.repeat(self.prep.columns.values,self.n_clust)]
        self.qrep = math.tan(math.acos(self.pf_c))*self.prep  

        self.prep.columns = list(range(self.n_clust))
        self.qrep.columns = list(range(self.n_clust))
        
        self.prep.to_csv(inp_folder + os.sep + 'prep_dist.csv', index = False)
        self.qrep.to_csv(inp_folder + os.sep + 'qrep_dist.csv', index = False)
 
        self.loc.to_csv(inp_folder + os.sep + 'geol_dist.csv')
       
        self.pdem.columns = list(range(24))
        self.qdem = self.pdem 
       
        self.pdem.T.to_csv(inp_folder + os.sep + 'pdem_dist.csv', index = False)
        self.qdem.T.to_csv(inp_folder + os.sep + 'qdem_dist.csv', index = False)
        
        self.inp_folder = inp_folder
  
    #Data pre-processing    
    def data_extract(self):
        #Convert to local time zone
        
        #Create yearly UTC timestamps using pandas
        UTC_time = pd.date_range(str(self.startyear) +'-01-01', str(self.endyear+1) +'-01-01', freq='1H', closed='left', tz='UTC')
        
        #Convert UTC to local time
        local_time = UTC_time.tz_convert(self.local_time_zone)
        
        #Convert back to naive timestamps, but in local time zone
        local_time_naive = local_time.tz_localize(None)
    
        date_local = pd.DataFrame(local_time_naive)
        date_local[1] = pd.to_datetime(date_local[0], format='%Y:%M:%D').dt.date
        date_local[2] = pd.to_datetime(date_local[0], format='%Y:%M:%D').dt.time
        
        if self.pvcalculation == 1:
            #Add to data 
            self.data[7] = date_local[0]
            self.data[8] = date_local[1]
            self.data[9] = date_local[2]
    
            #Extract 
            ext = (self.data[7] >= str(self.startyear) + '-1-2 00:00:00') & (self.data[7] <= str(self.endyear) + '-12-30 23:00:00')
            self.data_local_time = self.data.loc[ext]
            
            #Extracting PV power
            self.PV_power = pd.pivot(self.data_local_time, index=8, columns=9, values=1) 
            
            #Extracting solar irradiance data
            self.sol_irrad = pd.pivot(self.data_local_time, index=8, columns=9, values=2) 
            
            #Extracting wind speed data
            self.wind_speed = pd.pivot(self.data_local_time, index=8, columns=9, values=5) 
        
            power_chrono = pd.DataFrame(self.PV_power/self.sbase)
            power_chrono.to_csv(self.inp_folder + os.sep + 'power_chrono.csv',index = False)
            
        if self.pvcalculation == 0:
            #Add to data 
            self.data[6] = date_local[0]
            self.data[7] = date_local[1]
            self.data[8] = date_local[2]
    
            #Extract 
            ext = (self.data[6] >= str(self.startyear) + '-1-2 00:00:00') & (self.data[6] <= str(self.endyear) + '-12-30 23:00:00')
            self.data_local_time = self.data.loc[ext]
            
            #Extracting solar irradiance data 
            self.sol_irrad = pd.pivot(self.data_local_time, index=7, columns=8, values=1) 
            
            #Extracting wind speed data
            self.wind_speed = pd.pivot(self.data_local_time, index=7, columns=8, values=4) 
    
    def kmeans_clust(self):
        #Defining the kmeans function with initialization as k-means++
        kmeans = KMeans(n_clusters=self.n_clust, init='k-means++')
    
        #Fitting the k-means algorithm on data
        model_PV_power = kmeans.fit(self.PV_power)
        PV_centers = model_PV_power.cluster_centers_
        
        PV_labels = model_PV_power.labels_
        model_sol_irrad = kmeans.fit(self.sol_irrad)
        
        irrad_centers = model_sol_irrad.cluster_centers_
        model_wind_speed = kmeans.fit(self.wind_speed)
    
        wind_centers = model_wind_speed.cluster_centers_
        
        ini_dtim = [sum(PV_labels == n) for n in range(self.n_clust)]

        dtim_tot = sum(ini_dtim)

        for n in range(self.n_clust):
            ini_dtim[n] += (365 - dtim_tot)/self.n_clust
        
        dtim = pd.DataFrame(ini_dtim)
        dtim.columns = ['dt']
        
        psol = pd.DataFrame(PV_centers/self.sbase)
        psol = psol.T
        qsol = math.tan(math.acos(self.pf_p))*psol
        #Saving clustered data
        psol.to_csv(self.inp_folder + os.sep + 'psol_dist.csv', index = False) 
        qsol.to_csv(self.inp_folder + os.sep + 'qsol_dist.csv', index = False)
        
        pwin = pd.DataFrame(0*wind_centers/self.sbase)
        pwin = pwin.T
        qwin = math.tan(math.acos(self.pf_p))*pwin
        
        #Saving clustered data
        pwin.to_csv(self.inp_folder + os.sep + 'pwin_dist.csv', index = False) 
        qwin.to_csv(self.inp_folder + os.sep + 'qwin_dist.csv', index = False)
        
        dtim.to_csv(self.inp_folder + os.sep + 'dtim_dist.csv', index = False)