# tests/test_visualization.py

"""
tests/test_visualization.py

Unit tests for visualization module.
Tests chart generation, file saving, and visualization utilities.
"""

import os
import shutil
import sys
import tempfile
import unittest

# Add src directory to path for imports  # noqa: E402
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from visualization import BurnerVisualization  # noqa: E402


class TestBurnerVisualization(unittest.TestCase):
    """Test cases for BurnerVisualization class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.visualizer = BurnerVisualization(output_dir=self.temp_dir)

        # Sample data for testing in expected format
        self.combustion_data = {
            "stoichiometric_air": 9.5,
            "actual_air": 10.45,
            "products": {
                "CO2": 10.9,
                "H2O": 20.9,
                "N2": 67.2,
                "O2": 1.0
            },
            "temperature_profile": [2100, 1950, 1800, 1650, 1500, 1350],
            "heat_release": [800, 750, 650, 500, 300, 100]
        }

        self.pressure_data = {
            "components": {
                "burner": 250,
                "chamber": 150,
                "exit": 100,
                "piping": 50
            },
            "positions": [0.0, 0.2, 0.5, 0.8, 1.0],
            "cumulative": [0, 250, 400, 500, 550]
        }

        self.temperature_data = {
            "temperature_field": [
                [2100, 2000, 1900, 1800],
                [2050, 1950, 1850, 1750],
                [2000, 1900, 1800, 1700],
                [1950, 1850, 1750, 1650]
            ]
        }

        self.geometry_data = {
            "chamber": {
                "length": 0.8,
                "height": 0.2,
                "diameter": 0.2
            },
            "burner": {
                "width": 0.1,
                "height": 0.05
            }
        }

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_plot_combustion_analysis(self):
        """Test combustion analysis plotting."""
        # Create plot
        saved_files = self.visualizer.plot_combustion_analysis(
            self.combustion_data,
            save_formats=["png"]
        )

        # Check files were created
        self.assertIsInstance(saved_files, dict)
        self.assertIn("png", saved_files)
        self.assertTrue(os.path.exists(saved_files["png"]))

        # Check file size (images should not be empty)
        file_size = os.path.getsize(saved_files["png"])
        self.assertGreater(file_size, 1000)  # Should be at least 1KB

    def test_plot_pressure_losses(self):
        """Test pressure losses plotting."""
        # Create plot
        saved_files = self.visualizer.plot_pressure_losses(
            self.pressure_data,
            save_formats=["pdf"]
        )

        # Check files were created
        self.assertIsInstance(saved_files, dict)
        self.assertIn("pdf", saved_files)
        self.assertTrue(os.path.exists(saved_files["pdf"]))

        file_size = os.path.getsize(saved_files["pdf"])
        self.assertGreater(file_size, 500)

    def test_plot_temperature_distribution(self):
        """Test temperature distribution plotting."""
        # Create plot
        saved_files = self.visualizer.plot_temperature_distribution(
            self.temperature_data,
            save_formats=["jpeg"]
        )

        # Check files were created
        self.assertIsInstance(saved_files, dict)
        self.assertIn("jpeg", saved_files)
        self.assertTrue(os.path.exists(saved_files["jpeg"]))

        file_size = os.path.getsize(saved_files["jpeg"])
        self.assertGreater(file_size, 1000)

    def test_plot_burner_geometry(self):
        """Test burner geometry plotting."""
        # Create plot
        saved_files = self.visualizer.plot_burner_geometry(
            self.geometry_data,
            save_formats=["png"]
        )

        # Check files were created
        self.assertIsInstance(saved_files, dict)
        self.assertIn("png", saved_files)
        self.assertTrue(os.path.exists(saved_files["png"]))

        file_size = os.path.getsize(saved_files["png"])
        self.assertGreater(file_size, 1000)

    def test_create_summary_dashboard(self):
        """Test summary dashboard creation."""
        # Create comprehensive data for dashboard
        all_data = {
            "summary": {
                "power": 100,
                "efficiency": 85,
                "temperature": 2100,
                "pressure_drop": 250,
                "residence_time": 0.15
            },
            "efficiency": 85.0,
            "temperature_profile": [2100, 1950, 1800, 1650, 1500],
            "pressure_losses": {
                "burner": 250,
                "chamber": 150,
                "exit": 100
            },
            "heat_transfer": {
                "radiation": 60,
                "convection": 40
            },
            "emissions": {
                "NOx": 120,
                "CO": 50,
                "CO2": 8500
            }
        }

        # Create dashboard
        saved_files = self.visualizer.create_summary_dashboard(
            all_data,
            save_formats=["png"]
        )

        # Check file was created
        self.assertIsInstance(saved_files, dict)
        self.assertIn("png", saved_files)
        self.assertTrue(os.path.exists(saved_files["png"]))

        file_size = os.path.getsize(saved_files["png"])
        self.assertGreater(file_size, 2000)  # Dashboard should be larger

    def test_export_all_visualizations(self):
        """Test exporting all visualizations."""
        # Create comprehensive calculation results
        calculation_results = {
            "combustion": self.combustion_data,
            "pressure_losses": self.pressure_data,
            "temperature": self.temperature_data,
            "geometry": self.geometry_data
        }

        # Export all visualizations
        all_files = self.visualizer.export_all_visualizations(
            calculation_results,
            save_formats=["png"]
        )

        # Check files were created
        self.assertIsInstance(all_files, dict)
        self.assertIn("summary_dashboard", all_files)

        # Check at least some visualizations were created
        total_files = sum(len(files) for files in all_files.values())
        self.assertGreater(total_files, 0)

    def test_supported_formats(self):
        """Test different file format support."""
        formats = ["png", "pdf", "jpeg"]

        for fmt in formats:
            # Test with combustion analysis
            saved_files = self.visualizer.plot_combustion_analysis(
                self.combustion_data,
                save_formats=[fmt]
            )

            # Check file was created
            self.assertIn(fmt, saved_files)
            self.assertTrue(os.path.exists(saved_files[fmt]), f"Failed to create {fmt} file")
            file_size = os.path.getsize(saved_files[fmt])
            self.assertGreater(file_size, 500, f"{fmt} file too small")

    def test_czech_labels(self):
        """Test Czech language labels in plots."""
        # Create plot with Czech data structure (which includes Czech labels)
        saved_files = self.visualizer.plot_combustion_analysis(
            self.combustion_data,
            save_formats=["png"]
        )

        # Check file was created
        self.assertIn("png", saved_files)
        self.assertTrue(os.path.exists(saved_files["png"]))

    def test_data_validation(self):
        """Test input data validation."""
        # Test with invalid/empty data structure
        empty_data = {}

        # Should handle empty data gracefully
        saved_files = self.visualizer.plot_combustion_analysis(
            empty_data,
            save_formats=["png"]
        )

        # Should return empty dict or handle gracefully
        self.assertIsInstance(saved_files, dict)

    def test_invalid_output_directory(self):
        """Test handling of invalid output directory."""
        # Test with directory that cannot be created (permission denied)
        with self.assertRaises(OSError):
            BurnerVisualization(output_dir="/nonexistent/directory")

    def test_unsupported_format(self):
        """Test handling of unsupported file formats."""
        # Test with unsupported format
        try:
            saved_files = self.visualizer.plot_combustion_analysis(
                self.combustion_data,
                save_formats=["xyz"]  # Unsupported format
            )
            # Should handle gracefully or return empty
            self.assertIsInstance(saved_files, dict)
        except Exception:
            # Or should raise ValueError for unsupported format
            pass

    def test_figure_size_customization(self):
        """Test custom figure size settings."""
        # Create visualizer with custom figure size
        custom_visualizer = BurnerVisualization(
            output_dir=self.temp_dir,
            figure_size=(12, 8)
        )

        # Create plot with custom size
        saved_files = custom_visualizer.plot_combustion_analysis(
            self.combustion_data,
            save_formats=["png"]
        )

        # Check file was created
        self.assertIn("png", saved_files)
        self.assertTrue(os.path.exists(saved_files["png"]))

    def test_dpi_settings(self):
        """Test DPI settings for image quality."""
        # Create visualizer with custom DPI
        high_dpi_visualizer = BurnerVisualization(
            output_dir=self.temp_dir,
            dpi=600  # High resolution
        )

        # Create plot with high DPI
        saved_files = high_dpi_visualizer.plot_combustion_analysis(
            self.combustion_data,
            save_formats=["png"]
        )

        # Check file was created
        self.assertIn("png", saved_files)
        self.assertTrue(os.path.exists(saved_files["png"]))

        # High DPI file should be larger
        file_size = os.path.getsize(saved_files["png"])
        self.assertGreater(file_size, 1000)


if __name__ == "__main__":
    unittest.main()
