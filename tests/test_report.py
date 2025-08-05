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
from report import BurnerReportGenerator, CalculationMetadata  # noqa: E402


class TestBurnerReportGenerator(unittest.TestCase):
    """Test cases for BurnerReportGenerator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.generator = BurnerReportGenerator()

        # Create sample data
        self.metadata = CalculationMetadata(
            fuel_type="methane",
            required_power=100000,  # 100 kW
            excess_air_ratio=1.1,
            supply_pressure=3000,  # Pa
            calculation_date="2024-01-15 10:30:00",
            software_version="1.0.0",
        )

        # Mock calculation results
        self.sample_results = {
            "burner_diameter": 0.050,  # m
            "burner_area": 0.00196,  # m²
            "gas_velocity": 25.0,  # m/s
            "burner_pressure_drop": 250,  # Pa
            "heat_release_density": 50e6,  # W/m²
            "chamber_volume": 0.025,  # m³
            "residence_time": 0.15,  # s
            "flame_temperature": 2100,  # K
            "thermal_efficiency": 85.0,  # %
        }

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_generate_text_report(self):
        """Test text report generation."""
        output_file = os.path.join(self.temp_dir, "test_report.txt")

        # Generate report
        self.generator.generate_text_report(
            metadata=self.metadata,
            results=self.sample_results,
            output_file=output_file,
        )

        # Check file was created
        self.assertTrue(os.path.exists(output_file))

        # Check content
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("PROTOKOL VÝPOČTU HOŘÁKU", content)
        self.assertIn("methane", content)
        self.assertIn("100.0 kW", content)
        self.assertIn("50.0 mm", content)  # diameter in mm

    def test_generate_csv_report(self):
        """Test CSV report generation."""
        output_file = os.path.join(self.temp_dir, "test_report.csv")

        # Generate report
        self.generator.generate_csv_report(
            metadata=self.metadata,
            results=self.sample_results,
            output_file=output_file,
        )

        # Check file was created
        self.assertTrue(os.path.exists(output_file))

        # Check content
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Parametr,Hodnota,Jednotka", content)
        self.assertIn("methane", content)
        self.assertIn("100.0", content)

    def test_generate_excel_report(self):
        """Test Excel report generation."""
        output_file = os.path.join(self.temp_dir, "test_report.xlsx")

        # Generate report
        self.generator.generate_excel_report(
            metadata=self.metadata,
            results=self.sample_results,
            output_file=output_file,
        )

        # Check file was created
        self.assertTrue(os.path.exists(output_file))

        # Check file size (Excel files should not be empty)
        file_size = os.path.getsize(output_file)
        self.assertGreater(file_size, 1000)  # Should be at least 1KB

    def test_format_scientific_notation(self):
        """Test scientific notation formatting."""
        # Test large numbers
        result = self.generator._format_number(5e7)
        self.assertEqual(result, "5.0×10⁷")

        # Test small numbers
        result = self.generator._format_number(1.5e-3)
        self.assertEqual(result, "1.5×10⁻³")

        # Test normal numbers
        result = self.generator._format_number(123.45)
        self.assertEqual(result, "123.4")

    def test_format_units(self):
        """Test unit formatting."""
        # Test power units
        result = self.generator._format_with_units(100000, "power")
        self.assertEqual(result, "100.0 kW")

        # Test pressure units
        result = self.generator._format_with_units(3000, "pressure")
        self.assertEqual(result, "3000 Pa")

        # Test diameter units
        result = self.generator._format_with_units(0.050, "diameter")
        self.assertEqual(result, "50.0 mm")

    def test_validate_results_structure(self):
        """Test validation of results structure."""
        # Test valid results
        is_valid = self.generator._validate_results(self.sample_results)
        self.assertTrue(is_valid)

        # Test missing required fields
        incomplete_results = {"burner_diameter": 0.050}
        is_valid = self.generator._validate_results(incomplete_results)
        self.assertFalse(is_valid)

        # Test invalid data types
        invalid_results = self.sample_results.copy()
        invalid_results["burner_diameter"] = "invalid"
        is_valid = self.generator._validate_results(invalid_results)
        self.assertFalse(is_valid)

    def test_file_path_validation(self):
        """Test file path validation."""
        # Test invalid directory
        invalid_path = "/nonexistent/directory/report.txt"
        with self.assertRaises(ValueError):
            self.generator.generate_text_report(
                metadata=self.metadata,
                results=self.sample_results,
                output_file=invalid_path,
            )

    def test_empty_results_handling(self):
        """Test handling of empty results."""
        empty_results = {}
        output_file = os.path.join(self.temp_dir, "empty_report.txt")

        with self.assertRaises(ValueError):
            self.generator.generate_text_report(
                metadata=self.metadata,
                results=empty_results,
                output_file=output_file,
            )

    def test_unicode_handling(self):
        """Test proper Unicode handling in reports."""
        # Create metadata with Czech characters
        unicode_metadata = CalculationMetadata(
            fuel_type="zemní_plyn",
            required_power=50000,
            excess_air_ratio=1.2,
            supply_pressure=2500,
            calculation_date="2024-01-15 14:30:00",
            software_version="1.0.0",
        )

        output_file = os.path.join(self.temp_dir, "unicode_report.txt")

        # Should not raise encoding errors
        self.generator.generate_text_report(
            metadata=unicode_metadata,
            results=self.sample_results,
            output_file=output_file,
        )

        # Check file was created and contains Czech characters
        self.assertTrue(os.path.exists(output_file))
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("zemní_plyn", content)


if __name__ == "__main__":
    unittest.main()
