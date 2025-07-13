"""
Unit tests for the dataproc module.

This module tests the data processing functionality including:
- PVGIS API integration
- Time series clustering
- Data preprocessing
- File generation
"""

import unittest
import pandas as pd
import numpy as np
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
import urllib.request

# Import the module to test
from pyeplan.dataproc import datsys


class TestDatsys(unittest.TestCase):
    """Test cases for the datsys class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        
        # Create minimal test data files
        self._create_test_data_files()
        
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def _create_test_data_files(self):
        """Create minimal test data files for testing."""
        # Create mgpc_dist.xlsx with minimal data
        load_data = pd.DataFrame({
            'Load Point': [0, 1, 2],
            'Latitude': [0.25, 0.26, 0.27],
            'Longitude': [32.40, 32.41, 32.42]
        })
        
        # Add 24 columns for hourly load data (D:AA)
        for i in range(24):
            load_data[f'Hour_{i}'] = [10 + i, 15 + i, 20 + i]
        
        load_levels = pd.DataFrame({
            'Load Level': [50, 75, 100],
            'Renewable': [25, 35, 45]  # Add a second column for prep data
        })
        
        # Create Excel file with multiple sheets
        with pd.ExcelWriter(os.path.join(self.test_dir, 'mgpc_dist.xlsx')) as writer:
            load_data.to_excel(writer, sheet_name='Load Point', index=False)
            load_levels.to_excel(writer, sheet_name='Load Level', index=False)

    @patch('urllib.request.urlopen')
    def test_init_basic_parameters(self, mock_urlopen):
        """Test datsys initialization with basic parameters."""
        # Mock PVGIS 5.3 API response
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"outputs": {"hourly": [{"time": "2020-01-01 00:00:00", "P": 0, "G(i)": 0, "H_sun": 0, "T2m": 25, "WS10m": 2, "Int": 0}]}}'
        mock_urlopen.return_value = mock_response
        
        # Test basic initialization
        data_sys = datsys(
            inp_folder=self.test_dir,
            lat=0.25,
            lon=32.40,
            year=2020,
            pvcalc=1,
            pp=50,
            sys_loss=14,
            n_clust=3,
            pf_c=0.95,
            pf_p=1.0,
            sbase=1000
        )
        
        # Check basic attributes
        self.assertEqual(data_sys.lat, 0.25)
        self.assertEqual(data_sys.lon, 32.40)
        self.assertEqual(data_sys.startyear, 2020)
        self.assertEqual(data_sys.endyear, 2020)
        self.assertEqual(data_sys.pvcalculation, 1)
        self.assertEqual(data_sys.peakpower, 50)
        self.assertEqual(data_sys.loss, 14)
        self.assertEqual(data_sys.n_clust, 3)
        self.assertEqual(data_sys.pf_c, 0.95)
        self.assertEqual(data_sys.pf_p, 1.0)
        self.assertEqual(data_sys.sbase, 1000)
        self.assertEqual(data_sys.inp_folder, self.test_dir)

    @patch('urllib.request.urlopen')
    def test_init_default_parameters(self, mock_urlopen):
        """Test datsys initialization with default parameters."""
        # Mock PVGIS 5.3 API response
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"outputs": {"hourly": [{"time": "2020-01-01 00:00:00", "P": 0, "G(i)": 0, "H_sun": 0, "T2m": 25, "WS10m": 2, "Int": 0}]}}'
        mock_urlopen.return_value = mock_response
        
        # Test with default parameters
        data_sys = datsys(inp_folder=self.test_dir)
        
        # Check default values
        self.assertEqual(data_sys.lat, 0.251148605450955)
        self.assertEqual(data_sys.lon, 32.404833929733)
        self.assertEqual(data_sys.startyear, 2016)
        self.assertEqual(data_sys.pvcalculation, 1)
        self.assertEqual(data_sys.peakpower, 50)
        self.assertEqual(data_sys.loss, 14)
        self.assertEqual(data_sys.trackingtype, 2)
        self.assertEqual(data_sys.optimalinclination, 1)
        self.assertEqual(data_sys.optimalangles, 1)
        self.assertEqual(data_sys.outputformat, 'json')  # Updated default for PVGIS 5.3
        self.assertEqual(data_sys.browser, 1)

    @patch('urllib.request.urlopen')
    def test_pvgis_api_url_construction(self, mock_urlopen):
        """Test PVGIS 5.3 API URL construction."""
        # Mock PVGIS 5.3 API response
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"outputs": {"hourly": [{"time": "2020-01-01 00:00:00", "P": 0, "G(i)": 0, "H_sun": 0, "T2m": 25, "WS10m": 2, "Int": 0}]}}'
        mock_urlopen.return_value = mock_response
        
        data_sys = datsys(
            inp_folder=self.test_dir,
            lat=0.25,
            lon=32.40,
            year=2020,
            pvcalc=1,
            pp=50,
            sys_loss=14
        )
        
        # Check that URL contains expected PVGIS 5.3 parameters
        expected_url_parts = [
            'api/v5_3/seriescalc',  # New API endpoint
            'lat=0.25',
            'lon=32.40',
            'startyear=2020',
            'endyear=2020',
            'pvcalculation=1',
            'peakpower=50',
            'loss=14',
            'trackingtype=2',
            'optimalinclination=1',
            'optimalangles=1',
            'outputformat=json',  # Default format for PVGIS 5.3
            'browser=1',
            'raddatabase=PVGIS-SARAH2',  # New parameter
            'components=1',  # New parameter
            'horirrad=1',  # New parameter
            'optrad=1',  # New parameter
            'selectrad=1',  # New parameter
            'usehorizon=1',  # New parameter
            'showtemperatures=1',  # New parameter
            'temp2m=1',  # New parameter
            'wind_speed=1',  # New parameter
            'wind_speed_height=10',  # New parameter
            'albedo=0.2',  # New parameter
            'mountingplace=free',  # New parameter
            'angle=0',  # New parameter
            'aspect=0',  # New parameter
            'technology=crystSi'  # New parameter
        ]
        
        for part in expected_url_parts:
            self.assertIn(part, data_sys.data_link)

    @patch('urllib.request.urlopen')
    def test_data_extract_pvcalc_1(self, mock_urlopen):
        """Test data extraction with pvcalc=1 (power + radiation)."""
        # Mock PVGIS 5.3 API response with power data
        json_response = {
            "outputs": {
                "hourly": [
                    {"time": "2020-01-02 00:00:00", "P": 0, "G(i)": 0, "H_sun": 0, "T2m": 25, "WS10m": 2, "Int": 0},
                    {"time": "2020-01-02 01:00:00", "P": 10, "G(i)": 100, "H_sun": 10, "T2m": 26, "WS10m": 3, "Int": 0},
                    {"time": "2020-01-02 02:00:00", "P": 20, "G(i)": 200, "H_sun": 20, "T2m": 27, "WS10m": 4, "Int": 0}
                ]
            }
        }
        import json
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(json_response).encode('utf-8')
        mock_urlopen.return_value = mock_response
        
        data_sys = datsys(
            inp_folder=self.test_dir,
            lat=0.25,
            lon=32.40,
            year=2020,
            pvcalc=1
        )
        
        # Test data extraction
        data_sys.data_extract()
        
        # Check that data was processed
        self.assertIsNotNone(data_sys.data_local_time)
        self.assertIsNotNone(data_sys.PV_power)
        self.assertIsNotNone(data_sys.sol_irrad)
        self.assertIsNotNone(data_sys.wind_speed)

    @patch('urllib.request.urlopen')
    def test_data_extract_pvcalc_0(self, mock_urlopen):
        """Test data extraction with pvcalc=0 (radiation only)."""
        # Mock PVGIS 5.3 API response with radiation data only
        json_response = {
            "outputs": {
                "hourly": [
                    {"time": "2020-01-02 00:00:00", "G(i)": 0, "H_sun": 0, "T2m": 25, "WS10m": 2, "Int": 0},
                    {"time": "2020-01-02 01:00:00", "G(i)": 100, "H_sun": 10, "T2m": 26, "WS10m": 3, "Int": 0},
                    {"time": "2020-01-02 02:00:00", "G(i)": 200, "H_sun": 20, "T2m": 27, "WS10m": 4, "Int": 0}
                ]
            }
        }
        import json
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(json_response).encode('utf-8')
        mock_urlopen.return_value = mock_response
        
        data_sys = datsys(
            inp_folder=self.test_dir,
            lat=0.25,
            lon=32.40,
            year=2020,
            pvcalc=0
        )
        
        # Test data extraction
        data_sys.data_extract()
        
        # Check that data was processed
        self.assertIsNotNone(data_sys.data_local_time)
        self.assertIsNotNone(data_sys.sol_irrad)
        self.assertIsNotNone(data_sys.wind_speed)
        # PV_power should not exist when pvcalc=0
        self.assertFalse(hasattr(data_sys, 'PV_power'))

    @patch('urllib.request.urlopen')
    def test_kmeans_clustering(self, mock_urlopen):
        """Test K-means clustering functionality."""
        # Mock PVGIS 5.3 API response
        json_response = {
            "outputs": {
                "hourly": [
                    {"time": "2020-01-02 00:00:00", "P": 0, "G(i)": 0, "H_sun": 0, "T2m": 25, "WS10m": 2, "Int": 0},
                    {"time": "2020-01-02 01:00:00", "P": 10, "G(i)": 100, "H_sun": 10, "T2m": 26, "WS10m": 3, "Int": 0},
                    {"time": "2020-01-02 02:00:00", "P": 20, "G(i)": 200, "H_sun": 20, "T2m": 27, "WS10m": 4, "Int": 0}
                ]
            }
        }
        import json
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(json_response).encode('utf-8')
        mock_urlopen.return_value = mock_response
        
        data_sys = datsys(
            inp_folder=self.test_dir,
            lat=0.25,
            lon=32.40,
            year=2020,
            pvcalc=1,
            n_clust=2
        )
        
        # Extract data first
        data_sys.data_extract()
        
        # Test clustering
        data_sys.kmeans_clust()
        
        # Check that output files were created
        expected_files = [
            'psol_dist.csv',
            'qsol_dist.csv',
            'pwin_dist.csv',
            'qwin_dist.csv',
            'dtim_dist.csv'
        ]
        
        for filename in expected_files:
            filepath = os.path.join(self.test_dir, filename)
            self.assertTrue(os.path.exists(filepath), f"File {filename} was not created")

    @patch('urllib.request.urlopen')
    def test_file_generation(self, mock_urlopen):
        """Test that all required files are generated during initialization."""
        # Mock PVGIS 5.3 API response
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"outputs": {"hourly": [{"time": "2020-01-02 00:00:00", "P": 0, "G(i)": 0, "H_sun": 0, "T2m": 25, "WS10m": 2, "Int": 0}]}}'
        mock_urlopen.return_value = mock_response
        
        data_sys = datsys(inp_folder=self.test_dir)
        
        # Check that required files were created
        expected_files = [
            'prep_dist.csv',
            'qrep_dist.csv',
            'geol_dist.csv',
            'pdem_dist.csv',
            'qdem_dist.csv'
        ]
        
        for filename in expected_files:
            filepath = os.path.join(self.test_dir, filename)
            self.assertTrue(os.path.exists(filepath), f"File {filename} was not created")

    @patch('urllib.request.urlopen')
    def test_timezone_detection(self, mock_urlopen):
        """Test timezone detection functionality."""
        # Mock PVGIS 5.3 API response
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"outputs": {"hourly": [{"time": "2020-01-02 00:00:00", "P": 0, "G(i)": 0, "H_sun": 0, "T2m": 25, "WS10m": 2, "Int": 0}]}}'
        mock_urlopen.return_value = mock_response
        
        data_sys = datsys(
            inp_folder=self.test_dir,
            lat=0.25,
            lon=32.40
        )
        
        # Check that timezone was detected
        self.assertIsNotNone(data_sys.local_time_zone)
        self.assertIsInstance(data_sys.local_time_zone, str)

    def test_invalid_input_folder(self):
        """Test handling of invalid input folder."""
        with self.assertRaises(FileNotFoundError):
            datsys(inp_folder="/nonexistent/folder")

    @patch('urllib.request.urlopen')
    def test_power_factor_calculations(self, mock_urlopen):
        """Test power factor calculations for active and reactive power."""
        # Mock PVGIS 5.3 API response
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"outputs": {"hourly": [{"time": "2020-01-02 00:00:00", "P": 0, "G(i)": 0, "H_sun": 0, "T2m": 25, "WS10m": 2, "Int": 0}]}}'
        mock_urlopen.return_value = mock_response
        
        data_sys = datsys(
            inp_folder=self.test_dir,
            pf_c=0.9,  # Power factor for consumption
            pf_p=0.95  # Power factor for production
        )
        
        # Check that reactive power was calculated
        self.assertIsNotNone(data_sys.qrep)
        self.assertIsNotNone(data_sys.qdem)
        
        # Check that dataframes have correct shapes
        self.assertEqual(data_sys.prep.shape, data_sys.qrep.shape)
        self.assertEqual(data_sys.pdem.shape, data_sys.qdem.shape)

    @patch('urllib.request.urlopen')
    def test_pvgis_53_json_response_handling(self, mock_urlopen):
        """Test handling of PVGIS 5.3 JSON response format."""
        # Mock PVGIS 5.3 JSON response
        json_response = {
            "outputs": {
                "hourly": [
                    {
                        "time": "2020-01-01 00:00:00",
                        "P": 0,
                        "G(i)": 0,
                        "H_sun": 0,
                        "T2m": 25,
                        "WS10m": 2,
                        "Int": 0
                    },
                    {
                        "time": "2020-01-01 01:00:00",
                        "P": 10,
                        "G(i)": 100,
                        "H_sun": 10,
                        "T2m": 26,
                        "WS10m": 3,
                        "Int": 0
                    }
                ]
            }
        }
        
        import json
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(json_response).encode('utf-8')
        mock_urlopen.return_value = mock_response
        
        data_sys = datsys(
            inp_folder=self.test_dir,
            lat=0.25,
            lon=32.40,
            year=2020
        )
        
        # Check that JSON data was parsed correctly
        self.assertIsNotNone(data_sys.data)
        self.assertIn('time', data_sys.data.columns)
        self.assertIn('P', data_sys.data.columns)
        self.assertIn('G(i)', data_sys.data.columns)
        self.assertIn('WS10m', data_sys.data.columns)

    @patch('urllib.request.urlopen')
    def test_automatic_database_selection(self, mock_urlopen):
        """Test automatic radiation database selection based on location."""
        # Mock PVGIS 5.3 API response
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"outputs": {"hourly": [{"time": "2020-01-01 00:00:00", "P": 0, "G(i)": 0, "H_sun": 0, "T2m": 25, "WS10m": 2, "Int": 0}]}}'
        mock_urlopen.return_value = mock_response
        
        # Test SARAH2 database selection for global coverage
        data_sys_sarah2 = datsys(
            inp_folder=self.test_dir,
            lat=0.25,  # Within SARAH2 coverage
            lon=32.40
        )
        self.assertIn('raddatabase=PVGIS-SARAH2', data_sys_sarah2.data_link)
        
        # Test ERA5 database selection for regions outside SARAH2 coverage
        data_sys_era5 = datsys(
            inp_folder=self.test_dir,
            lat=70.0,  # Outside SARAH2 coverage
            lon=32.40
        )
        self.assertIn('raddatabase=PVGIS-ERA5', data_sys_era5.data_link)

    @patch('urllib.request.urlopen')
    def test_manual_database_selection(self, mock_urlopen):
        """Test manual radiation database selection."""
        # Mock PVGIS 5.3 API response
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"outputs": {"hourly": [{"time": "2020-01-01 00:00:00", "P": 0, "G(i)": 0, "H_sun": 0, "T2m": 25, "WS10m": 2, "Int": 0}]}}'
        mock_urlopen.return_value = mock_response
        
        # Test manual database selection
        data_sys = datsys(
            inp_folder=self.test_dir,
            lat=0.25,
            lon=32.40,
            raddatabase='PVGIS-NSRDB'
        )
        self.assertIn('raddatabase=PVGIS-NSRDB', data_sys.data_link)

    @patch('urllib.request.urlopen')
    def test_column_name_normalization(self, mock_urlopen):
        """Test column name normalization for PVGIS 5.3."""
        # Mock PVGIS 5.3 JSON response with alternative column names
        json_response = {
            "outputs": {
                "hourly": [
                    {
                        "time": "2020-01-01 00:00:00",
                        "P": 0,
                        "G_i": 0,  # Alternative column name
                        "H_sun": 0,
                        "T_2m": 25,  # Alternative column name
                        "WS_10m": 2,  # Alternative column name
                        "Int": 0
                    }
                ]
            }
        }
        
        import json
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(json_response).encode('utf-8')
        mock_urlopen.return_value = mock_response
        
        data_sys = datsys(
            inp_folder=self.test_dir,
            lat=0.25,
            lon=32.40,
            year=2020
        )
        
        # Check that column names were normalized
        self.assertIn('G(i)', data_sys.data.columns)
        self.assertIn('T2m', data_sys.data.columns)
        self.assertIn('WS10m', data_sys.data.columns)

    @patch('urllib.request.urlopen')
    def test_error_handling_pvgis_53(self, mock_urlopen):
        """Test error handling for PVGIS 5.3 API errors."""
        # Mock HTTP error response
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="https://re.jrc.ec.europa.eu/api/v5_3/seriescalc",
            code=400,
            msg="Bad Request",
            hdrs={},
            fp=None
        )
        
        with self.assertRaises(urllib.error.HTTPError):
            datsys(inp_folder=self.test_dir, lat=0.25, lon=32.40)

    @patch('urllib.request.urlopen')
    def test_validation_method(self, mock_urlopen):
        """Test the _validate_output_format method."""
        # Mock PVGIS 5.3 API response
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"outputs": {"hourly": [{"time": "2020-01-01 00:00:00", "P": 0, "G(i)": 0, "H_sun": 0, "T2m": 25, "WS10m": 2, "Int": 0}]}}'
        mock_urlopen.return_value = mock_response
        
        data_sys = datsys(
            inp_folder=self.test_dir,
            lat=0.25,
            lon=32.40,
            year=2020,
            n_clust=2
        )
        
        # Extract data and perform clustering
        data_sys.data_extract()
        data_sys.kmeans_clust()
        
        # Test validation method
        data_sys._validate_output_format()
        
        # Check that validation passed (no exception raised)
        self.assertTrue(True)  # If we reach here, validation passed


class TestDatsysIntegration(unittest.TestCase):
    """Integration tests for datsys with real data files."""

    def setUp(self):
        """Set up test fixtures with real example data."""
        # Use the 5_bus example data
        self.example_dir = "examples/5_bus"
        
        # Skip tests if example data is not available
        if not os.path.exists(self.example_dir):
            self.skipTest("Example data not available")

    @patch('urllib.request.urlopen')
    def test_with_real_example_data(self, mock_urlopen):
        """Test datsys with real example data from 5_bus case."""
        # Mock PVGIS 5.3 API response
        json_response = {
            "outputs": {
                "hourly": [
                    {"time": "2020-01-02 00:00:00", "P": 0, "G(i)": 0, "H_sun": 0, "T2m": 25, "WS10m": 2, "Int": 0},
                    {"time": "2020-01-02 01:00:00", "P": 10, "G(i)": 100, "H_sun": 10, "T2m": 26, "WS10m": 3, "Int": 0},
                    {"time": "2020-01-02 02:00:00", "P": 20, "G(i)": 200, "H_sun": 20, "T2m": 27, "WS10m": 4, "Int": 0}
                ]
            }
        }
        import json
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(json_response).encode('utf-8')
        mock_urlopen.return_value = mock_response
        
        # Test with real example data
        data_sys = datsys(
            inp_folder=self.example_dir,
            lat=0.25,
            lon=32.40,
            year=2020,
            n_clust=3
        )
        
        # Test data extraction
        data_sys.data_extract()
        
        # Test clustering
        data_sys.kmeans_clust()
        
        # Verify that the system can process real data
        self.assertIsNotNone(data_sys.loc)
        self.assertIsNotNone(data_sys.pdem)
        self.assertIsNotNone(data_sys.prep)


if __name__ == '__main__':
    unittest.main() 