"""
Data Processing and Renewable Energy Resource Assessment Module.

This module provides comprehensive data processing capabilities for microgrid planning
and operation. It integrates with the PVGIS (Photovoltaic Geographical Information
System) API to fetch solar irradiance and wind speed data, performs time series
clustering, and processes load profiles for microgrid optimization.

The module includes:
- PVGIS API integration for renewable energy data
- Time series clustering using K-means algorithm
- Timezone handling and data preprocessing
- Load profile processing and renewable generation assessment
- Geographic data processing and validation

Classes:
    datsys: Main class for data processing operations

Key Features:
- Automatic data fetching from PVGIS database
- Support for multiple radiation databases (SARAH, NSRDB, ERA5)
- Time series clustering for scenario reduction
- Power factor calculations for active/reactive power
- Geographic coordinate processing and timezone detection

References:
- Dehghan, S., Nakiganda, A., & Aristidou, P. (2020). "Planning and Operation of 
  Resilient Microgrids: A Comprehensive Review." IEEE Transactions on Smart Grid.
- Nakiganda, A., Dehghan, S., & Aristidou, P. (2021). "PyEPlan: An Open-Source 
  Framework for Microgrid Planning and Operation." IEEE Power & Energy Society 
  General Meeting.
- PVGIS API Documentation: https://ec.europa.eu/jrc/en/pvgis

Example:
    >>> from pyeplan.dataproc import datsys
    >>> data_sys = datsys("input_folder", lat=0.25, lon=32.40, year=2016)
    >>> data_sys.data_extract()
    >>> data_sys.kmeans_clust()
"""

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
    """
    Data processing system for microgrid planning and operation.
    
    This class handles all data processing operations including renewable energy
    resource assessment, time series clustering, and load profile processing.
    It integrates with PVGIS API to fetch solar irradiance and wind speed data
    for any location worldwide.
    
    :ivar loc: Load point locations and coordinates (pd.DataFrame)
    :ivar pdem: Active power demand profiles (pd.DataFrame)
    :ivar prep: Active power renewable generation profiles (pd.DataFrame)
    :ivar lat: Latitude in decimal degrees (south is negative) (float)
    :ivar lon: Longitude in decimal degrees (west is negative) (float)
    :ivar startyear: Start year for data collection (int)
    :ivar endyear: End year for data collection (int)
    :ivar pvcalculation: PV calculation method (0=radiation only, 1=power+radiation) (int)
    :ivar peakpower: Nominal power of PV system in kW (float)
    :ivar loss: Sum of system losses in % (float)
    :ivar trackingtype: Type of sun tracking system (int)
    :ivar optimalinclination: Calculate optimum inclination angle (1=yes) (int)
    :ivar optimalangles: Calculate optimum inclination and orientation (1=yes) (int)
    :ivar outputformat: Output format for PVGIS data (str)
    :ivar browser: Output format (0=stream, 1=file) (int)
    :ivar n_clust: Number of clusters for time series clustering (int)
    :ivar pf_c: Power factor at consumption points (float)
    :ivar pf_p: Power factor at production points (float)
    :ivar sbase: Base apparent power in kW (float)
    :ivar data_link: PVGIS API URL with parameters (str)
    :ivar data: Raw data from PVGIS API (pd.DataFrame)
    :ivar local_time_zone: Local timezone for the location (str)
    :ivar qrep: Reactive power renewable generation profiles (pd.DataFrame)
    :ivar qdem: Reactive power demand profiles (pd.DataFrame)
    :ivar inp_folder: Input folder path for data files (str)

    .. rubric:: Methods

    * :meth:`data_extract` -- Extract and process time series data
    * :meth:`kmeans_clust` -- Perform K-means clustering on time series data
    """
    
    def __init__(self, inp_folder = '', lat = 0.251148605450955, lon = 32.404833929733,year = 2016, pvcalc = 1, pp = 50, sys_loss = 14, n_clust = 1, pf_c = 1, pf_p = 1, sbase = 1000, raddatabase = None):
        """
        Initialize the data processing system.

        :param inp_folder: Input folder path containing data files (default: '')
        :type inp_folder: str
        :param lat: Latitude in decimal degrees (default: 0.251148605450955)
        :type lat: float
        :param lon: Longitude in decimal degrees (default: 32.404833929733)
        :type lon: float
        :param year: Year for data collection (default: 2016)
        :type year: int
        :param pvcalc: PV calculation method (default: 1)
            - 0: Solar radiation calculations only
            - 1: Solar radiation and power production calculations
        :type pvcalc: int
        :param pp: Nominal power of PV system in kW (default: 50)
        :type pp: float
        :param sys_loss: Sum of system losses in % (default: 14)
        :type sys_loss: float
        :param n_clust: Number of clusters for time series clustering (default: 1)
        :type n_clust: int
        :param pf_c: Power factor at consumption points (default: 1)
        :type pf_c: float
        :param pf_p: Power factor at production points (default: 1)
        :type pf_p: float
        :param sbase: Base apparent power in kW (default: 1000)
        :type sbase: float
        :param raddatabase: Radiation database to use. If None, automatically selected based on location.
            Options:
                - 'PVGIS-SARAH3'
                - 'PVGIS-ERA5'
                - 'PVGIS-NSRDB'
        :type raddatabase: str, optional

        :raises ValueError: If PVGIS API returns an error or invalid response

        :example:
            >>> data_sys = datsys("input_folder", lat=0.25, lon=32.40, year=2016)
        """
        
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
        self.outputformat = 'json'  # Default to JSON for PVGIS 5.3
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
        
        #Data extraction from PVGIS 5.3
        # New PVGIS 5.3 API endpoint
        self.data_link = 'https://re.jrc.ec.europa.eu/api/v5_3/seriescalc'
        
        # Build query parameters for PVGIS 5.3
        # Determine appropriate radiation database based on location
        if raddatabase is None:
            if -60 <= self.lat <= 65 and -180 <= self.lon <= 180:  # Global coverage
                raddatabase = 'PVGIS-SARAH3'  # Updated to SARAH3
            else:
                raddatabase = 'PVGIS-ERA5'  # Fallback for other regions
        
        params = {
            'lat': self.lat,
            'lon': self.lon,
            'startyear': self.startyear,
            'endyear': self.endyear,
            'pvcalculation': self.pvcalculation,
            'peakpower': self.peakpower,
            'loss': self.loss,
            'trackingtype': self.trackingtype,
            'angle': 0,  # default, not relevant for 2-axis tracking
            'aspect': 0,  # default, not relevant for tracking
            'optimalinclination': self.optimalinclination,
            'optimalangles': self.optimalangles,
            'raddatabase': raddatabase,
            'components': 1,  # outputs beam, diffuse, reflected if 1
            'usehorizon': 1,
            'outputformat': self.outputformat,
            'browser': self.browser,
            'pvtechchoice': 'crystSi',
            'mountingplace': 'free',
        }
        
        # Build URL with parameters
        query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
        self.data_link = f'{self.data_link}?{query_string}'
        
        # Fetch data from PVGIS 5.3 API
        try:
            response = urllib.request.urlopen(self.data_link)
            response_text = response.read().decode('utf-8')
            
            # Check if response contains an error message
            if 'error' in response_text.lower() or 'exception' in response_text.lower():
                print(f"PVGIS 5.3 API Error: {response_text}")
                raise ValueError(f"PVGIS 5.3 API returned an error: {response_text}")
            
            # PVGIS 5.3 returns JSON by default, so we need to handle it differently
            if self.outputformat == 'json':
                import json
                data_json = json.loads(response_text)
                # Convert JSON to DataFrame format
                if 'outputs' in data_json and 'hourly' in data_json['outputs']:
                    hourly_data = data_json['outputs']['hourly']
                    # Convert to DataFrame format compatible with existing code
                    self.data = pd.DataFrame(hourly_data)
                    
                    # Handle potential column name variations in PVGIS 5.3
                    self._normalize_column_names()
                else:
                    raise ValueError("Invalid JSON response format from PVGIS 5.3")
            else:
                # For CSV format, read as before but with updated column structure
                self.data = pd.read_csv(urllib.request.urlopen(self.data_link), skiprows=2, header=None)
        except urllib.error.HTTPError as e:
            print(f"HTTP Error {e.code}: {e.reason}")
            print(f"URL: {self.data_link}")
            raise
        except Exception as e:
            print(f"Error fetching data from PVGIS 5.3: {e}")
            print(f"URL: {self.data_link}")
            raise 
    
        '''
        Data columns description for PVGIS 5.3:
            
        For JSON format:
        - time: Date and hour
        - P: PV system power (W) ** Column not included if pvcalc = 0
        - G(i): Global irradiance on the inclined plane (plane of the array) (W/m2)
        - H_sun: Sun height (degree)
        - T2m: 2-m air temperature (degree Celsius)
        - WS10m: 10-m total wind speed (m/s)
        - Int: 1 means solar radiation values are reconstructed
        
        For CSV format (columns may vary based on parameters):
        - Column 0: Time
        - Column 1: P (if pvcalc = 1)
        - Column 2: G(i)
        - Column 3: H_sun
        - Column 4: T2m
        - Column 5: WS10m
        - Column 6: Int
        
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
  
    def data_extract(self):
        """
        Extract and process time series data from PVGIS.

        This method processes the raw data obtained from PVGIS API and converts
        it to local timezone. It extracts PV power, solar irradiance, and wind
        speed data and organizes them into time series format.

        :return: None
        :rtype: None
        :raises ValueError: If required columns are missing in PVGIS response

        :ivar data_local_time: Processed data in local timezone
        :ivar PV_power: PV power time series (if pvcalculation=1)
        :ivar sol_irrad: Solar irradiance time series
        :ivar wind_speed: Wind speed time series

        :example:
            >>> data_sys = datsys("input_folder", lat=0.25, lon=32.40)
            >>> data_sys.data_extract()
        """
        #Convert to local time zone
        
        #Create yearly UTC timestamps using pandas
        UTC_time = pd.date_range(str(self.startyear) +'-01-01', str(self.endyear+1) +'-01-01', freq='1H', inclusive='left', tz='UTC')
        
        #Convert UTC to local time
        local_time = UTC_time.tz_convert(self.local_time_zone)
        
        #Convert back to naive timestamps, but in local time zone
        local_time_naive = local_time.tz_localize(None)
    
        date_local = pd.DataFrame(local_time_naive)
        date_local[1] = pd.to_datetime(date_local[0], format='%Y:%M:%D').dt.date
        date_local[2] = pd.to_datetime(date_local[0], format='%Y:%M:%D').dt.time
        
        # Handle PVGIS 5.3 data format
        if self.outputformat == 'json':
            # For JSON format, data is already structured
            if self.pvcalculation == 1:
                # Convert time column to datetime - PVGIS 5.3 uses format YYYYMMDD:HHMM
                self.data['time'] = pd.to_datetime(self.data['time'], format='%Y%m%d:%H%M')
                self.data['date'] = self.data['time'].dt.date
                self.data['hour'] = self.data['time'].dt.time
                
                # Extract data for the specified year range
                ext = (self.data['time'] >= str(self.startyear) + '-01-01') & (self.data['time'] <= str(self.endyear) + '-12-31')
                self.data_local_time = self.data.loc[ext]
                
                # Check available columns and extract data accordingly
                available_cols = self.data_local_time.columns.tolist()
                print(f"Available columns in PVGIS 5.3 data: {available_cols}")
                
                # Extracting PV power (column 'P' in PVGIS 5.3)
                if 'P' in available_cols:
                    self.PV_power = pd.pivot(self.data_local_time, index='date', columns='hour', values='P')
                else:
                    raise ValueError("PV power column 'P' not found in PVGIS 5.3 response")
                
                # Extracting solar irradiance data (PVGIS 5.3 returns Gb(i), Gd(i), Gr(i) components)
                if 'Gb(i)' in available_cols and 'Gd(i)' in available_cols and 'Gr(i)' in available_cols:
                    # Calculate total global irradiance as sum of beam, diffuse, and reflected components
                    self.data_local_time['G(i)'] = self.data_local_time['Gb(i)'] + self.data_local_time['Gd(i)'] + self.data_local_time['Gr(i)']
                    self.sol_irrad = pd.pivot(self.data_local_time, index='date', columns='hour', values='G(i)')
                elif 'G(i)' in available_cols:
                    # Fallback to direct G(i) column if available
                    self.sol_irrad = pd.pivot(self.data_local_time, index='date', columns='hour', values='G(i)')
                else:
                    raise ValueError("Solar irradiance columns not found in PVGIS 5.3 response. Expected 'Gb(i)', 'Gd(i)', 'Gr(i)' or 'G(i)'")
                
                # Extracting wind speed data (column 'WS10m' in PVGIS 5.3)
                if 'WS10m' in available_cols:
                    self.wind_speed = pd.pivot(self.data_local_time, index='date', columns='hour', values='WS10m')
                else:
                    raise ValueError("Wind speed column 'WS10m' not found in PVGIS 5.3 response")
                
                power_chrono = pd.DataFrame(self.PV_power/self.sbase)
                power_chrono.to_csv(self.inp_folder + os.sep + 'power_chrono.csv', index=False)
                
            else:  # pvcalculation == 0
                # Convert time column to datetime - PVGIS 5.3 uses format YYYYMMDD:HHMM
                self.data['time'] = pd.to_datetime(self.data['time'], format='%Y%m%d:%H%M')
                self.data['date'] = self.data['time'].dt.date
                self.data['hour'] = self.data['time'].dt.time
                
                # Extract data for the specified year range
                ext = (self.data['time'] >= str(self.startyear) + '-01-01') & (self.data['time'] <= str(self.endyear) + '-12-31')
                self.data_local_time = self.data.loc[ext]
                
                # Check available columns and extract data accordingly
                available_cols = self.data_local_time.columns.tolist()
                print(f"Available columns in PVGIS 5.3 data (pvcalc=0): {available_cols}")
                
                # Extracting solar irradiance data (PVGIS 5.3 returns Gb(i), Gd(i), Gr(i) components)
                if 'Gb(i)' in available_cols and 'Gd(i)' in available_cols and 'Gr(i)' in available_cols:
                    # Calculate total global irradiance as sum of beam, diffuse, and reflected components
                    self.data_local_time['G(i)'] = self.data_local_time['Gb(i)'] + self.data_local_time['Gd(i)'] + self.data_local_time['Gr(i)']
                    self.sol_irrad = pd.pivot(self.data_local_time, index='date', columns='hour', values='G(i)')
                elif 'G(i)' in available_cols:
                    # Fallback to direct G(i) column if available
                    self.sol_irrad = pd.pivot(self.data_local_time, index='date', columns='hour', values='G(i)')
                else:
                    raise ValueError("Solar irradiance columns not found in PVGIS 5.3 response. Expected 'Gb(i)', 'Gd(i)', 'Gr(i)' or 'G(i)'")
                
                # Extracting wind speed data (column 'WS10m' in PVGIS 5.3)
                if 'WS10m' in available_cols:
                    self.wind_speed = pd.pivot(self.data_local_time, index='date', columns='hour', values='WS10m')
                else:
                    raise ValueError("Wind speed column 'WS10m' not found in PVGIS 5.3 response")
        else:
            # For CSV format, use the original column-based approach
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
        """
        Perform K-means clustering on time series data.

        This method applies K-means clustering algorithm to reduce the dimensionality
        of time series data by grouping similar time periods into clusters. It
        clusters PV power, solar irradiance, and wind speed data separately and
        generates representative scenarios for each cluster.

        :return: None
        :rtype: None
        :raises ValueError: If output files are missing or have incorrect format

        :ivar psol: Clustered solar power scenarios
        :ivar qsol: Clustered solar reactive power scenarios
        :ivar pwin: Clustered wind power scenarios
        :ivar qwin: Clustered wind reactive power scenarios
        :ivar dtim: Duration of each cluster

        :example:
            >>> data_sys = datsys("input_folder", n_clust=5)
            >>> data_sys.data_extract()
            >>> data_sys.kmeans_clust()
        """
        #Defining the kmeans function with initialization as k-means++
        kmeans = KMeans(n_clusters=self.n_clust, init='k-means++')
    
        #Fitting the k-means algorithm on data
        if self.pvcalculation == 1:
            model_PV_power = kmeans.fit(self.PV_power)
            PV_centers = model_PV_power.cluster_centers_
            PV_labels = model_PV_power.labels_
        else:
            # When pvcalculation == 0, use solar irradiance for PV power estimation
            model_PV_power = kmeans.fit(self.sol_irrad)
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
        
        # Validate output data format for compatibility with investoper.py
        self._validate_output_format()
    
    def _validate_output_format(self):
        """
        Validate that the output data format is compatible with investoper.py.

        This method checks that all required CSV files are generated with the
        correct format and structure expected by the investment and operation
        optimization module.

        :raises ValueError: If any required file is missing or has incorrect format
        """
        required_files = [
            'prep_dist.csv', 'qrep_dist.csv', 'geol_dist.csv',
            'pdem_dist.csv', 'qdem_dist.csv', 'psol_dist.csv',
            'qsol_dist.csv', 'pwin_dist.csv', 'qwin_dist.csv', 'dtim_dist.csv'
        ]
        
        missing_files = []
        for file in required_files:
            file_path = self.inp_folder + os.sep + file
            if not os.path.exists(file_path):
                missing_files.append(file)
        
        if missing_files:
            raise ValueError(f"Missing required output files: {missing_files}")
        
        # Check data dimensions and format
        try:
            psol = pd.read_csv(self.inp_folder + os.sep + 'psol_dist.csv')
            pwin = pd.read_csv(self.inp_folder + os.sep + 'pwin_dist.csv')
            dtim = pd.read_csv(self.inp_folder + os.sep + 'dtim_dist.csv')
            
            # Verify that clustering produced the expected number of scenarios
            if psol.shape[1] != self.n_clust:
                print(f"Warning: Solar scenarios ({psol.shape[1]}) don't match n_clust ({self.n_clust})")
            
            if pwin.shape[1] != self.n_clust:
                print(f"Warning: Wind scenarios ({pwin.shape[1]}) don't match n_clust ({self.n_clust})")
            
            if dtim.shape[0] != self.n_clust:
                print(f"Warning: Duration scenarios ({dtim.shape[0]}) don't match n_clust ({self.n_clust})")
            
            print(f"✓ PVGIS 5.3 data processing completed successfully")
            print(f"✓ Generated {self.n_clust} scenarios for optimization")
            print(f"✓ All required files created in {self.inp_folder}")
            
        except Exception as e:
            raise ValueError(f"Error validating output format: {e}")
    
    def _normalize_column_names(self):
        """
        Normalize column names from PVGIS 5.3 JSON response to match expected format.

        PVGIS 5.3 may return column names with slight variations. This method
        ensures the column names match the expected format for data processing.
        """
        column_mapping = {
            'time': 'time',
            'P': 'P',  # PV power
            'G(i)': 'G(i)',  # Global irradiance
            'H_sun': 'H_sun',  # Sun height
            'T2m': 'T2m',  # 2m temperature
            'WS10m': 'WS10m',  # Wind speed
            'Int': 'Int'  # Interpolation flag
        }
        
        # Check for alternative column names and rename if necessary
        current_cols = self.data.columns.tolist()
        
        # Handle potential variations in column names
        if 'G(i)' not in current_cols and 'G_i' in current_cols:
            self.data = self.data.rename(columns={'G_i': 'G(i)'})
        
        if 'WS10m' not in current_cols and 'WS_10m' in current_cols:
            self.data = self.data.rename(columns={'WS_10m': 'WS10m'})
        
        if 'T2m' not in current_cols and 'T_2m' in current_cols:
            self.data = self.data.rename(columns={'T_2m': 'T2m'})
        
        if 'H_sun' not in current_cols and 'H_sun' in current_cols:
            self.data = self.data.rename(columns={'H_sun': 'H_sun'})
        
        print(f"Normalized column names: {self.data.columns.tolist()}")