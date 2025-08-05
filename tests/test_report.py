# tests/test_report.py

"""
tests/test_report.py

Unit tests for report generation module.
Tests text, CSV, and Excel report generation functionality.
"""

import os
import shutil
import sys
import tempfile
import unittest

# Add src directory to path for imports  # noqa: E402
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from report import BurnerReportGenerator  # noqa: E402


class TestBurnerReportGenerator(unittest.TestCase):
    """Test cases for BurnerReportGenerator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.generator = BurnerReportGenerator(output_dir=self.temp_dir)

        # Mock calculation results in expected format
        self.sample_results = {
            "inputs": {
                "fuel_type": "methane",
                "fuel_flow_rate": 0.01,
                "excess_air_ratio": 1.1,
                "required_power": 100.0  # kW
            },
            "combustion": {
                "theoretical_air": 9.5,
                "actual_air": 10.45,
                "excess_air": 10.0,
                "heating_value": 50.0,
                "combustion_temp": 2100,
                "products": {
                    "CO2": 10.9,
                    "H2O": 20.9,
                    "N2": 67.2,
                    "O2": 1.0
                }
            },
            "burner": {
                "type": "Atmospheric",
                "power": 100.0,
                "nozzle_diameter": 50.0,
                "gas_velocity": 25.0,
                "gas_pressure": 3000
            },
            "chamber": {
                "volume": 0.025,
                "length": 0.8,
                "diameter": 0.2,
                "residence_time": 0.15,
                "heat_loading": 4000
            },
            "radiation": {
                "heat_flux": 50.0,
                "gas_emissivity": 0.3,
                "wall_emissivity": 0.8,
                "radiation_efficiency": 75.0
            },
            "pressure_losses": {
                "components": {
                    "burner": 250,
                    "chamber": 150,
                    "exit": 100
                }
            },
            "efficiency": 85.0,
            "emissions": {
                "NOx": 120,
                "CO": 50
            }
        }

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_generate_text_report(self):
        """Test text report generation."""
        # Set metadata first
        self.generator.set_metadata(
            project_name="Test Project",
            user_name="Test User",
            software_version="1.0.0"
        )

        # Generate report
        output_file = self.generator.generate_text_report(self.sample_results)

        # Check file was created
        self.assertTrue(os.path.exists(output_file))

        # Check content
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("ZPRÁVA O VÝPOČTU PLYNOVÉHO HOŘÁKU", content)
        self.assertIn("methane", content)
        self.assertIn("100.0", content)

    def test_generate_csv_export(self):
        """Test CSV export generation."""
        # Set metadata first
        self.generator.set_metadata(
            project_name="Test Project",
            user_name="Test User"
        )

        # Generate CSV export
        output_file = self.generator.generate_csv_export(self.sample_results)

        # Check file was created
        self.assertTrue(os.path.exists(output_file))

        # Check content
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Parametr,Hodnota,Jednotka,Kategorie", content)
        self.assertIn("methane", content)
        self.assertIn("100.0", content)

    def test_generate_excel_report(self):
        """Test Excel report generation."""
        # Set metadata first
        self.generator.set_metadata(
            project_name="Test Project",
            user_name="Test User"
        )

        # Generate Excel report
        output_file = self.generator.generate_excel_report(self.sample_results)

        # Check file was created
        self.assertTrue(os.path.exists(output_file))

        # Check file size (Excel files should not be empty)
        file_size = os.path.getsize(output_file)
        self.assertGreater(file_size, 1000)  # Should be at least 1KB

    def test_determine_unit(self):
        """Test unit determination."""
        # Test temperature units
        result = self.generator._determine_unit("temperature", 2100)
        self.assertEqual(result, "°C")

        # Test pressure units
        result = self.generator._determine_unit("pressure", 3000)
        self.assertEqual(result, "Pa")

        # Test power units
        result = self.generator._determine_unit("power", 100)
        self.assertEqual(result, "kW")

        # Test velocity units
        result = self.generator._determine_unit("velocity", 25)
        self.assertEqual(result, "m/s")

        # Test default units
        result = self.generator._determine_unit("unknown", 123)
        self.assertEqual(result, "-")

    def test_complete_report_generation(self):
        """Test complete report generation."""
        # Generate complete report with all formats
        files = self.generator.generate_complete_report(
            self.sample_results,
            formats=["txt", "csv", "xlsx"],
            project_name="Test Project",
            user_name="Test User"
        )

        # Check all files were created
        self.assertIn("txt", files)
        self.assertIn("csv", files)
        self.assertIn("xlsx", files)

        # Check files exist
        for format_type, filepath in files.items():
            self.assertTrue(os.path.exists(filepath))
            file_size = os.path.getsize(filepath)
            self.assertGreater(file_size, 100)  # Should not be empty

    def test_metadata_setting(self):
        """Test metadata setting."""
        self.generator.set_metadata(
            project_name="Test Project",
            user_name="Test User",
            software_version="2.0.0"
        )

        # Check metadata was set
        self.assertIsNotNone(self.generator.report_metadata)
        self.assertEqual(self.generator.report_metadata.project_name, "Test Project")
        self.assertEqual(self.generator.report_metadata.user_name, "Test User")
        self.assertEqual(self.generator.report_metadata.software_version, "2.0.0")

    def test_empty_results_handling(self):
        """Test handling of empty results."""
        empty_results = {}

        # Should still generate report, just with minimal content
        output_file = self.generator.generate_text_report(empty_results)
        self.assertTrue(os.path.exists(output_file))

        # Check file has basic structure
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("ZPRÁVA O VÝPOČTU", content)

    def test_unicode_handling(self):
        """Test proper Unicode handling in reports."""
        # Create results with Czech characters
        unicode_results = self.sample_results.copy()
        unicode_results["inputs"]["fuel_type"] = "zemní_plyn"

        # Set metadata with Czech project name
        self.generator.set_metadata(
            project_name="Testovací projekt",
            user_name="Test User"
        )

        # Should not raise encoding errors
        output_file = self.generator.generate_text_report(unicode_results)

        # Check file was created and contains Czech characters
        self.assertTrue(os.path.exists(output_file))
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("zemní_plyn", content)
            self.assertIn("Testovací projekt", content)


if __name__ == "__main__":
    unittest.main()
