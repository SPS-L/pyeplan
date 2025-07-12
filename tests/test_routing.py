"""
Unit tests for the routing module.

This module tests the network routing functionality including:
- Minimum spanning tree algorithm
- Geographic distance calculations
- Cable parameter calculations
- Network topology generation
"""

import unittest
import pandas as pd
import numpy as np
import os
import tempfile
import shutil
import networkx as nx
from unittest.mock import patch, MagicMock

# Import the module to test
from pyeplan.routing import rousys, distance


class TestRousys(unittest.TestCase):
    """Test cases for the rousys class."""

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
        # Create geol_dist.csv with node coordinates
        geol_data = pd.DataFrame({
            'Longtitude': [32.40, 32.41, 32.42, 32.43, 32.44],
            'Latitude': [0.25, 0.26, 0.27, 0.28, 0.29]
        })
        geol_data.to_csv(os.path.join(self.test_dir, 'geol_dist.csv'), index=False)
        
        # Create cblt_dist.csv with cable parameters
        cable_data = pd.DataFrame({
            'crs': [35, 35, 35, 35, 35],
            'r7': [0.524, 0.524, 0.524, 0.524, 0.524],
            'x7': [0.084, 0.084, 0.084, 0.084, 0.084],
            'i7': [130, 130, 130, 130, 130]
        })
        cable_data.to_csv(os.path.join(self.test_dir, 'cblt_dist.csv'), index=False)

    def test_init_basic_parameters(self):
        """Test rousys initialization with basic parameters."""
        route_sys = rousys(
            inp_folder=self.test_dir,
            crs=35,
            typ=7,
            vbase=415,
            sbase=1
        )
        
        # Check basic attributes
        self.assertEqual(route_sys.crs, 35)
        self.assertEqual(route_sys.typ, 7)
        self.assertEqual(route_sys.vbase, 415)
        self.assertEqual(route_sys.sbase, 1000)  # Converted to VA
        self.assertEqual(route_sys.node, 5)  # Number of nodes from geol_dist.csv
        self.assertEqual(route_sys.inp_folder, self.test_dir)

    def test_init_default_parameters(self):
        """Test rousys initialization with default parameters."""
        route_sys = rousys(inp_folder=self.test_dir)
        
        # Check default values
        self.assertEqual(route_sys.crs, 35)
        self.assertEqual(route_sys.typ, 7)
        self.assertEqual(route_sys.vbase, 415)
        self.assertEqual(route_sys.sbase, 1000)

    def test_cable_parameter_calculations(self):
        """Test cable parameter calculations."""
        route_sys = rousys(
            inp_folder=self.test_dir,
            crs=35,
            typ=7,
            vbase=415,
            sbase=1
        )
        
        # Check that cable parameters were calculated
        self.assertIsNotNone(route_sys.r)
        self.assertIsNotNone(route_sys.x)
        self.assertIsNotNone(route_sys.i)
        self.assertIsNotNone(route_sys.p)
        self.assertIsNotNone(route_sys.q)
        
        # Check that parameters are numeric
        self.assertIsInstance(route_sys.r, (int, float))
        self.assertIsInstance(route_sys.x, (int, float))
        self.assertIsInstance(route_sys.i, (int, float))
        self.assertIsInstance(route_sys.p, (int, float))
        self.assertIsInstance(route_sys.q, (int, float))

    def test_base_calculations(self):
        """Test base value calculations."""
        route_sys = rousys(
            inp_folder=self.test_dir,
            vbase=415,
            sbase=1
        )
        
        # Check base calculations
        expected_zbase = (415**2) / 1000  # vbase^2 / sbase
        expected_ibase = 1000 / (np.sqrt(3) * 415)
        
        self.assertAlmostEqual(route_sys.zbase, expected_zbase, places=6)
        self.assertAlmostEqual(route_sys.ibase, expected_ibase, places=6)

    def test_min_spn_tre_creates_files(self):
        """Test that min_spn_tre creates required output files."""
        route_sys = rousys(inp_folder=self.test_dir)
        
        # Run minimum spanning tree algorithm
        route_sys.min_spn_tre()
        
        # Check that output files were created
        expected_files = [
            'rou_dist.csv',
            'elin_dist.csv'
        ]
        
        for filename in expected_files:
            filepath = os.path.join(self.test_dir, filename)
            self.assertTrue(os.path.exists(filepath), f"File {filename} was not created")

    def test_rou_dist_file_structure(self):
        """Test the structure of the generated rou_dist.csv file."""
        route_sys = rousys(inp_folder=self.test_dir)
        route_sys.min_spn_tre()
        
        # Read the generated file
        rou_dist = pd.read_csv(os.path.join(self.test_dir, 'rou_dist.csv'))
        
        # Check file structure
        expected_columns = ['from', 'to', 'distance']
        for col in expected_columns:
            self.assertIn(col, rou_dist.columns)
        
        # Check that distances are positive
        self.assertTrue(all(rou_dist['distance'] > 0))
        
        # Check that we have n-1 edges (minimum spanning tree)
        self.assertEqual(len(rou_dist), route_sys.node - 1)

    def test_elin_dist_file_structure(self):
        """Test the structure of the generated elin_dist.csv file."""
        route_sys = rousys(inp_folder=self.test_dir)
        route_sys.min_spn_tre()
        
        # Read the generated file
        elin_dist = pd.read_csv(os.path.join(self.test_dir, 'elin_dist.csv'))
        
        # Check file structure
        expected_columns = ['from', 'to', 'ini', 'res', 'rea', 'sus', 'pmax', 'qmax']
        for col in expected_columns:
            self.assertIn(col, elin_dist.columns)
        
        # Check that electrical parameters are calculated
        self.assertTrue(all(elin_dist['res'] > 0))  # Resistance should be positive
        self.assertTrue(all(elin_dist['pmax'] > 0))  # Power limits should be positive
        self.assertTrue(all(elin_dist['qmax'] > 0))  # Power limits should be positive

    def test_network_topology_connectivity(self):
        """Test that the generated network is connected."""
        route_sys = rousys(inp_folder=self.test_dir)
        route_sys.min_spn_tre()
        
        # Read the routing file
        rou_dist = pd.read_csv(os.path.join(self.test_dir, 'rou_dist.csv'))
        
        # Create a graph from the routing data
        G = nx.Graph()
        for _, row in rou_dist.iterrows():
            G.add_edge(row['from'], row['to'])
        
        # Check that the graph is connected
        self.assertTrue(nx.is_connected(G))
        
        # Check that it's a tree (no cycles)
        self.assertEqual(len(G.edges()), len(G.nodes()) - 1)

    def test_invalid_cable_type(self):
        """Test handling of invalid cable type."""
        # Create cable data without the required type
        cable_data = pd.DataFrame({
            'crs': [35],
            'r1': [0.524],  # Different type
            'x1': [0.084],
            'i1': [130]
        })
        cable_data.to_csv(os.path.join(self.test_dir, 'cblt_dist.csv'), index=False)
        
        # This should raise an error when trying to access r7
        with self.assertRaises((KeyError, IndexError)):
            route_sys = rousys(inp_folder=self.test_dir, typ=7)

    def test_different_cable_cross_sections(self):
        """Test different cable cross sections."""
        # Create cable data with multiple cross sections
        cable_data = pd.DataFrame({
            'crs': [25, 35, 50],
            'r7': [0.727, 0.524, 0.387],
            'x7': [0.084, 0.084, 0.084],
            'i7': [100, 130, 170]
        })
        cable_data.to_csv(os.path.join(self.test_dir, 'cblt_dist.csv'), index=False)
        
        # Test with different cross sections
        for crs in [25, 35, 50]:
            route_sys = rousys(inp_folder=self.test_dir, crs=crs, typ=7)
            self.assertEqual(route_sys.crs, crs)
            self.assertIsNotNone(route_sys.r)
            self.assertIsNotNone(route_sys.x)
            self.assertIsNotNone(route_sys.i)

    def test_geol_data_loading(self):
        """Test loading of geographical data."""
        route_sys = rousys(inp_folder=self.test_dir)
        
        # Check that geographical data was loaded
        self.assertIsInstance(route_sys.geol, pd.DataFrame)
        self.assertEqual(len(route_sys.geol), route_sys.node)
        
        # Check required columns
        required_columns = ['Longtitude', 'Latitude']
        for col in required_columns:
            self.assertIn(col, route_sys.geol.columns)

    def test_cable_data_loading(self):
        """Test loading of cable data."""
        route_sys = rousys(inp_folder=self.test_dir)
        
        # Check that cable data was loaded
        self.assertIsInstance(route_sys.cblt, pd.DataFrame)
        
        # Check required columns
        required_columns = ['crs', 'r7', 'x7', 'i7']
        for col in required_columns:
            self.assertIn(col, route_sys.cblt.columns)


class TestDistanceFunction(unittest.TestCase):
    """Test cases for the distance function."""

    def test_distance_basic_calculation(self):
        """Test basic distance calculation."""
        # Test distance between two points
        point1 = (0.25, 32.40)  # (lat, lon)
        point2 = (0.26, 32.41)  # (lat, lon)
        
        dist = distance(point1, point2)
        
        # Check that distance is positive
        self.assertGreater(dist, 0)
        
        # Check that distance is reasonable (should be ~1-2 km for these coordinates)
        self.assertLess(dist, 5000)  # Less than 5 km

    def test_distance_same_point(self):
        """Test distance calculation for the same point."""
        point = (0.25, 32.40)
        dist = distance(point, point)
        
        # Distance should be very close to zero
        self.assertAlmostEqual(dist, 0, places=2)

    def test_distance_opposite_hemispheres(self):
        """Test distance calculation across hemispheres."""
        # Northern hemisphere
        point1 = (45.0, -75.0)  # New York area
        # Southern hemisphere
        point2 = (-33.9, 151.2)  # Sydney area
        
        dist = distance(point1, point2)
        
        # Distance should be very large (around 15,000 km)
        self.assertGreater(dist, 10000000)  # More than 10,000 km

    def test_distance_polar_regions(self):
        """Test distance calculation in polar regions."""
        # North Pole area
        point1 = (80.0, 0.0)
        # South Pole area
        point2 = (-80.0, 0.0)
        
        dist = distance(point1, point2)
        
        # Distance should be very large
        self.assertGreater(dist, 15000000)  # More than 15,000 km

    def test_distance_equator(self):
        """Test distance calculation along the equator."""
        point1 = (0.0, 0.0)  # Prime meridian, equator
        point2 = (0.0, 1.0)  # 1 degree east, equator
        
        dist = distance(point1, point2)
        
        # Distance should be approximately 111 km (1 degree at equator)
        self.assertAlmostEqual(dist, 111000, delta=1000)  # Within 1 km

    def test_distance_meridian(self):
        """Test distance calculation along a meridian."""
        point1 = (0.0, 0.0)  # Prime meridian, equator
        point2 = (1.0, 0.0)  # Prime meridian, 1 degree north
        
        dist = distance(point1, point2)
        
        # Distance should be approximately 111 km (1 degree of latitude)
        self.assertAlmostEqual(dist, 111000, delta=1000)  # Within 1 km

    def test_distance_negative_coordinates(self):
        """Test distance calculation with negative coordinates."""
        point1 = (-0.25, -32.40)  # Negative lat and lon
        point2 = (0.25, 32.40)    # Positive lat and lon
        
        dist = distance(point1, point2)
        
        # Distance should be positive
        self.assertGreater(dist, 0)

    def test_distance_large_values(self):
        """Test distance calculation with large coordinate values."""
        point1 = (90.0, 180.0)   # Maximum lat and lon
        point2 = (-90.0, -180.0) # Minimum lat and lon
        
        dist = distance(point1, point2)
        
        # Distance should be very large (around 20,000 km)
        self.assertGreater(dist, 18000000)  # More than 18,000 km


class TestRousysIntegration(unittest.TestCase):
    """Integration tests for rousys with real data files."""

    def setUp(self):
        """Set up test fixtures with real example data."""
        # Use the 5_bus example data
        self.example_dir = "examples/5_bus"
        
        # Skip tests if example data is not available
        if not os.path.exists(self.example_dir):
            self.skipTest("Example data not available")

    def test_with_real_example_data(self):
        """Test rousys with real example data from 5_bus case."""
        route_sys = rousys(
            inp_folder=self.example_dir,
            crs=35,
            typ=7,
            vbase=415,
            sbase=1
        )
        
        # Test minimum spanning tree generation
        route_sys.min_spn_tre()
        
        # Verify that the system can process real data
        self.assertIsNotNone(route_sys.geol)
        self.assertIsNotNone(route_sys.cblt)
        self.assertGreater(route_sys.node, 0)
        
        # Check that output files were created
        expected_files = ['rou_dist.csv', 'elin_dist.csv']
        for filename in expected_files:
            filepath = os.path.join(self.example_dir, filename)
            self.assertTrue(os.path.exists(filepath), f"File {filename} was not created")


if __name__ == '__main__':
    unittest.main() 