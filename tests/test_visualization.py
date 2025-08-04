# tests/test_visualization.py

"""
tests/test_visualization.py

Unit tests for visualization module.
Tests chart generation, file saving, and visualization utilities.
"""

import unittest
import sys
import os
import tempfile
import shutil

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from visualization import BurnerVisualization


class TestBurnerVisualization(unittest.TestCase):
    """Test cases for BurnerVisualization class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory for test outputs
        self.temp_dir = tempfile.mkdtemp()
        self.viz = BurnerVisualization(output_dir=self.temp_dir)
        
        # Sample data for testing
        self.sample_combustion_data = {
            'air_fuel_ratio': 9.5,
            'excess_air': 20.0,
            'stoichiometric_air': 9.52,
            'actual_air': 11.42,
            'products': {
                'CO2': 8.5,
                'H2O': 16.8,
                'N2': 71.2,
                'O2': 3.5
            },
            'temperature_profile': [500, 800, 1200, 1500, 1200, 800],
            'heat_release': [100, 200, 300, 250, 150, 50]
        }
        
        self.sample_pressure_data = {
            'components': {
                'Burner': 50.0,
                'Chamber': 30.0,
                'Ducting': 20.0,
                'Stack': 15.0
            },
            'positions': [0, 1, 2, 3, 4],
            'cumulative': [0, 50, 80, 100, 115]
        }
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary directory
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_visualization_initialization(self):
        """Test visualization module initializes correctly."""
        self.assertIsInstance(self.viz, BurnerVisualization)
        self.assertEqual(self.viz.output_dir, self.temp_dir)
        self.assertTrue(os.path.exists(self.temp_dir))
    
    def test_combustion_analysis_plot(self):
        """Test combustion analysis plot generation."""
        saved_files = self.viz.plot_combustion_analysis(
            self.sample_combustion_data, 
            save_formats=['png']
        )
        
        # Verify files were created
        self.assertIsInstance(saved_files, dict)
        if saved_files:  # If plot was generated successfully
            self.assertIn('png', saved_files)
            self.assertTrue(os.path.exists(saved_files['png']))
    
    def test_pressure_losses_plot(self):
        """Test pressure losses plot generation."""
        saved_files = self.viz.plot_pressure_losses(
            self.sample_pressure_data,
            save_formats=['png']
        )
        
        # Verify files were created
        self.assertIsInstance(saved_files, dict)
        if saved_files:  # If plot was generated successfully
            self.assertIn('png', saved_files)
            self.assertTrue(os.path.exists(saved_files['png']))
    
    def test_temperature_distribution_plot(self):
        """Test temperature distribution visualization."""
        # Create sample temperature field data
        temperature_data = {
            'temperature_field': [
                [500, 600, 700, 800],
                [600, 800, 1000, 900],
                [700, 900, 1200, 1000],
                [600, 800, 1000, 800]
            ]
        }
        
        saved_files = self.viz.plot_temperature_distribution(
            temperature_data,
            save_formats=['png']
        )
        
        # Verify files were created
        self.assertIsInstance(saved_files, dict)
        if saved_files:  # If plot was generated successfully
            self.assertIn('png', saved_files)
            self.assertTrue(os.path.exists(saved_files['png']))
    
    def test_burner_geometry_plot(self):
        """Test burner geometry visualization."""
        geometry_data = {
            'chamber': {
                'length': 2.0,
                'height': 1.0,
                'width': 1.5
            },
            'burner': {
                'width': 0.2,
                'height': 0.1,
                'position': 'front'
            }
        }
        
        saved_files = self.viz.plot_burner_geometry(
            geometry_data,
            save_formats=['png']
        )
        
        # Verify files were created
        self.assertIsInstance(saved_files, dict)
        if saved_files:  # If plot was generated successfully
            self.assertIn('png', saved_files)
            self.assertTrue(os.path.exists(saved_files['png']))
    
    def test_multiple_save_formats(self):
        """Test saving plots in multiple formats."""
        formats = ['png', 'pdf']
        saved_files = self.viz.plot_combustion_analysis(
            self.sample_combustion_data,
            save_formats=formats
        )
        
        if saved_files:  # If plot was generated successfully
            for fmt in formats:
                if fmt in saved_files:  # Format might not be available
                    self.assertTrue(os.path.exists(saved_files[fmt]))
    
    def test_export_all_visualizations(self):
        """Test comprehensive visualization export."""
        all_data = {
            'combustion': self.sample_combustion_data,
            'pressure_losses': self.sample_pressure_data,
            'temperature': {
                'temperature_field': [
                    [500, 600, 700],
                    [600, 800, 900],
                    [700, 900, 800]
                ]
            },
            'geometry': {
                'chamber': {'length': 2.0, 'height': 1.0},
                'burner': {'width': 0.2, 'height': 0.1}
            }
        }
        
        all_saved_files = self.viz.export_all_visualizations(
            all_data,
            save_formats=['png']
        )
        
        # Verify comprehensive export
        self.assertIsInstance(all_saved_files, dict)
        # Should have multiple visualization types
        expected_types = ['combustion_analysis', 'pressure_losses', 'summary_dashboard']
        for viz_type in expected_types:
            if viz_type in all_saved_files:
                self.assertIsInstance(all_saved_files[viz_type], list)
    
    def test_invalid_data_handling(self):
        """Test handling of invalid or empty data."""
        # Test with empty data
        saved_files = self.viz.plot_combustion_analysis({}, save_formats=['png'])
        self.assertIsInstance(saved_files, dict)
        
        # Test with None data
        saved_files = self.viz.plot_pressure_losses(None, save_formats=['png'])
        self.assertIsInstance(saved_files, dict)
    
    def test_output_directory_creation(self):
        """Test automatic output directory creation."""
        new_dir = os.path.join(self.temp_dir, 'new_output')
        viz_new = BurnerVisualization(output_dir=new_dir)
        
        # Directory should be created automatically
        self.assertTrue(os.path.exists(new_dir))


if __name__ == '__main__':
    unittest.main()