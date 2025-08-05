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
        self.visualizer = BurnerVisualization()

        # Sample data for testing
        self.sample_data = {
            "positions": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
            "temperatures": [2100, 1950, 1800, 1650, 1500, 1350],
            "pressures": [101325, 101200, 101100, 101000, 100950, 100900],
            "velocities": [25.0, 22.5, 20.0, 17.5, 15.0, 12.5],
        }

        self.burner_results = {
            "burner_diameter": 0.050,  # m
            "gas_velocity": 25.0,  # m/s
            "heat_release_density": 50e6,  # W/m²
            "burner_pressure_drop": 250,  # Pa
        }

        self.chamber_results = {
            "chamber_volume": 0.025,  # m³
            "chamber_diameter": 0.200,  # m
            "chamber_length": 0.800,  # m
            "residence_time": 0.15,  # s
            "thermal_efficiency": 85.0,  # %
        }

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_plot_temperature_profile(self):
        """Test temperature profile plotting."""
        output_file = os.path.join(self.temp_dir, "temperature_profile.png")

        # Create plot
        self.visualizer.plot_temperature_profile(
            positions=self.sample_data["positions"],
            temperatures=self.sample_data["temperatures"],
            title="Test Temperature Profile",
            output_file=output_file,
        )

        # Check file was created
        self.assertTrue(os.path.exists(output_file))

        # Check file size (images should not be empty)
        file_size = os.path.getsize(output_file)
        self.assertGreater(file_size, 1000)  # Should be at least 1KB

    def test_plot_pressure_profile(self):
        """Test pressure profile plotting."""
        output_file = os.path.join(self.temp_dir, "pressure_profile.pdf")

        # Create plot
        self.visualizer.plot_pressure_profile(
            positions=self.sample_data["positions"],
            pressures=self.sample_data["pressures"],
            title="Test Pressure Profile",
            output_file=output_file,
        )

        # Check file was created
        self.assertTrue(os.path.exists(output_file))
        file_size = os.path.getsize(output_file)
        self.assertGreater(file_size, 500)

    def test_plot_velocity_profile(self):
        """Test velocity profile plotting."""
        output_file = os.path.join(self.temp_dir, "velocity_profile.jpg")

        # Create plot
        self.visualizer.plot_velocity_profile(
            positions=self.sample_data["positions"],
            velocities=self.sample_data["velocities"],
            title="Test Velocity Profile",
            output_file=output_file,
        )

        # Check file was created
        self.assertTrue(os.path.exists(output_file))
        file_size = os.path.getsize(output_file)
        self.assertGreater(file_size, 1000)

    def test_plot_burner_characteristics(self):
        """Test burner characteristics plotting."""
        output_file = os.path.join(self.temp_dir, "burner_chars.png")

        # Create multi-parameter data
        diameters = [0.025, 0.030, 0.035, 0.040, 0.045, 0.050]
        velocities = [45.0, 31.2, 23.0, 17.7, 14.1, 11.3]
        pressure_drops = [800, 470, 280, 190, 130, 95]

        # Create plot
        self.visualizer.plot_burner_characteristics(
            diameters=diameters,
            velocities=velocities,
            pressure_drops=pressure_drops,
            title="Burner Design Characteristics",
            output_file=output_file,
        )

        # Check file was created
        self.assertTrue(os.path.exists(output_file))
        file_size = os.path.getsize(output_file)
        self.assertGreater(file_size, 1000)

    def test_create_burner_diagram(self):
        """Test burner schematic diagram creation."""
        output_file = os.path.join(self.temp_dir, "burner_diagram.png")

        # Create diagram
        self.visualizer.create_burner_diagram(
            burner_diameter=self.burner_results["burner_diameter"],
            chamber_diameter=self.chamber_results["chamber_diameter"],
            chamber_length=self.chamber_results["chamber_length"],
            output_file=output_file,
        )

        # Check file was created
        self.assertTrue(os.path.exists(output_file))
        file_size = os.path.getsize(output_file)
        self.assertGreater(file_size, 1000)

    def test_create_summary_dashboard(self):
        """Test summary dashboard creation."""
        output_file = os.path.join(self.temp_dir, "dashboard.png")

        # Create dashboard
        self.visualizer.create_summary_dashboard(
            burner_results=self.burner_results,
            chamber_results=self.chamber_results,
            temperature_data=self.sample_data,
            output_file=output_file,
        )

        # Check file was created
        self.assertTrue(os.path.exists(output_file))
        file_size = os.path.getsize(output_file)
        self.assertGreater(file_size, 2000)  # Dashboard should be larger

    def test_supported_formats(self):
        """Test different file format support."""
        formats = ["png", "pdf", "jpg", "jpeg"]

        for fmt in formats:
            output_file = os.path.join(self.temp_dir, f"test_plot.{fmt}")

            # Test with temperature profile
            self.visualizer.plot_temperature_profile(
                positions=self.sample_data["positions"],
                temperatures=self.sample_data["temperatures"],
                title=f"Test Plot - {fmt.upper()}",
                output_file=output_file,
            )

            # Check file was created
            self.assertTrue(os.path.exists(output_file), f"Failed to create {fmt} file")
            file_size = os.path.getsize(output_file)
            self.assertGreater(file_size, 500, f"{fmt} file too small")

    def test_czech_labels(self):
        """Test Czech language labels in plots."""
        output_file = os.path.join(self.temp_dir, "czech_labels.png")

        # Create plot with Czech labels
        self.visualizer.plot_temperature_profile(
            positions=self.sample_data["positions"],
            temperatures=self.sample_data["temperatures"],
            title="Teplotní profil spalovací komory",
            xlabel="Pozice [m]",
            ylabel="Teplota [°C]",
            output_file=output_file,
        )

        # Check file was created
        self.assertTrue(os.path.exists(output_file))

    def test_data_validation(self):
        """Test input data validation."""
        # Test mismatched array lengths
        with self.assertRaises(ValueError):
            self.visualizer.plot_temperature_profile(
                positions=[0.0, 0.1, 0.2],  # 3 elements
                temperatures=[2100, 1950],  # 2 elements
                title="Invalid Data",
                output_file=os.path.join(self.temp_dir, "invalid.png"),
            )

        # Test empty data
        with self.assertRaises(ValueError):
            self.visualizer.plot_temperature_profile(
                positions=[],
                temperatures=[],
                title="Empty Data",
                output_file=os.path.join(self.temp_dir, "empty.png"),
            )

    def test_invalid_output_directory(self):
        """Test handling of invalid output directory."""
        invalid_path = "/nonexistent/directory/plot.png"

        with self.assertRaises(ValueError):
            self.visualizer.plot_temperature_profile(
                positions=self.sample_data["positions"],
                temperatures=self.sample_data["temperatures"],
                title="Invalid Path Test",
                output_file=invalid_path,
            )

    def test_unsupported_format(self):
        """Test handling of unsupported file formats."""
        unsupported_file = os.path.join(self.temp_dir, "test.xyz")

        with self.assertRaises(ValueError):
            self.visualizer.plot_temperature_profile(
                positions=self.sample_data["positions"],
                temperatures=self.sample_data["temperatures"],
                title="Unsupported Format",
                output_file=unsupported_file,
            )

    def test_figure_size_customization(self):
        """Test custom figure size settings."""
        output_file = os.path.join(self.temp_dir, "custom_size.png")

        # Create plot with custom size
        self.visualizer.plot_temperature_profile(
            positions=self.sample_data["positions"],
            temperatures=self.sample_data["temperatures"],
            title="Custom Size Test",
            output_file=output_file,
            figure_size=(12, 8),  # Custom width x height
        )

        # Check file was created
        self.assertTrue(os.path.exists(output_file))

    def test_color_scheme_options(self):
        """Test different color scheme options."""
        output_file = os.path.join(self.temp_dir, "color_scheme.png")

        # Test with specific color scheme
        self.visualizer.plot_temperature_profile(
            positions=self.sample_data["positions"],
            temperatures=self.sample_data["temperatures"],
            title="Color Scheme Test",
            output_file=output_file,
            color_scheme="scientific",  # professional color scheme
        )

        # Check file was created
        self.assertTrue(os.path.exists(output_file))


if __name__ == "__main__":
    unittest.main()
