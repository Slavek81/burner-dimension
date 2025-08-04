# tests/test_report.py

"""
tests/test_report.py

Unit tests for report generation module.
Tests text, CSV, and Excel report generation functionality.
"""

import unittest
import sys
import os
import tempfile
import shutil

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from report import BurnerReportGenerator, CalculationMetadata


class TestBurnerReportGenerator(unittest.TestCase):
    """Test cases for BurnerReportGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory for test outputs
        self.temp_dir = tempfile.mkdtemp()
        self.report_gen = BurnerReportGenerator(output_dir=self.temp_dir)
        
        # Sample calculation results for testing
        self.sample_results = {
            'inputs': {
                'fuel_type': 'Natural Gas',
                'power': 100,  # kW
                'excess_air_ratio': 1.2,
                'operating_temp': 850  # °C
            },
            'combustion': {
                'theoretical_air': 9.52,
                'actual_air': 11.42,
                'excess_air': 20.0,
                'heating_value': 35.8,
                'combustion_temp': 1850,
                'products': {
                    'CO2': 8.5,
                    'H2O': 16.8,
                    'N2': 71.2,
                    'O2': 3.5
                }
            },
            'burner': {
                'type': 'Low NOx',
                'power': 100,
                'nozzle_diameter': 8.5,
                'gas_velocity': 25.0,
                'gas_pressure': 2500
            },
            'chamber': {
                'volume': 2.5,
                'length': 2.0,
                'diameter': 1.2,
                'residence_time': 0.85,
                'heat_loading': 40
            },
            'radiation': {
                'heat_flux': 85.5,
                'gas_emissivity': 0.25,
                'wall_emissivity': 0.85,
                'radiation_efficiency': 78.5
            },
            'pressure_losses': {
                'components': {
                    'Burner': 50.0,
                    'Chamber': 30.0,
                    'Ducting': 20.0,
                    'Stack': 15.0
                }
            },
            'efficiency': 82.5,
            'emissions': {
                'NOx': 45.2,
                'CO': 12.5,
                'CO2': 195.8
            }
        }
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary directory
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_report_generator_initialization(self):
        """Test report generator initializes correctly."""
        self.assertIsInstance(self.report_gen, BurnerReportGenerator)
        self.assertEqual(self.report_gen.output_dir, self.temp_dir)
        self.assertTrue(os.path.exists(self.temp_dir))
    
    def test_metadata_setting(self):
        """Test setting calculation metadata."""
        self.report_gen.set_metadata(
            project_name="Test Project",
            user_name="Test User",
            software_version="1.0.0"
        )
        
        metadata = self.report_gen.report_metadata
        self.assertIsInstance(metadata, CalculationMetadata)
        self.assertEqual(metadata.project_name, "Test Project")
        self.assertEqual(metadata.user_name, "Test User")
        self.assertEqual(metadata.software_version, "1.0.0")
        self.assertIsNotNone(metadata.calculation_id)
        self.assertIsNotNone(metadata.timestamp)
    
    def test_text_report_generation(self):
        """Test text report generation."""
        self.report_gen.set_metadata(project_name="Test Project")
        
        report_path = self.report_gen.generate_text_report(self.sample_results)
        
        # Verify file was created
        self.assertTrue(os.path.exists(report_path))
        
        # Verify file content
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for key sections
        self.assertIn('ZPRÁVA O VÝPOČTU', content)
        self.assertIn('VSTUPNÍ PARAMETRY', content)
        self.assertIn('ANALÝZA SPALOVÁNÍ', content)
        self.assertIn('NÁVRH HOŘÁKU', content)
        self.assertIn('Test Project', content)
    
    def test_csv_export_generation(self):
        """Test CSV export generation."""
        csv_path = self.report_gen.generate_csv_export(self.sample_results)
        
        # Verify file was created
        self.assertTrue(os.path.exists(csv_path))
        
        # Verify file content structure
        with open(csv_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Should have header and data rows
        self.assertGreater(len(lines), 1)
        
        # Check header format
        header = lines[0].strip()
        expected_columns = ['Parametr', 'Hodnota', 'Jednotka', 'Kategorie']
        for col in expected_columns:
            self.assertIn(col, header)
    
    def test_excel_report_generation(self):
        """Test Excel report generation."""
        try:
            import pandas as pd
            
            excel_path = self.report_gen.generate_excel_report(self.sample_results)
            
            # Verify file was created
            self.assertTrue(os.path.exists(excel_path))
            
            # Verify file can be read
            excel_file = pd.ExcelFile(excel_path)
            sheet_names = excel_file.sheet_names
            
            # Should have multiple sheets
            expected_sheets = ['Shrnutí', 'Vstupní parametry']
            for sheet in expected_sheets:
                if sheet in sheet_names:  # Some sheets might be conditional
                    df = pd.read_excel(excel_path, sheet_name=sheet)
                    self.assertFalse(df.empty)
                    
        except ImportError:
            self.skipTest("pandas or openpyxl not available for Excel testing")
    
    def test_complete_report_generation(self):
        """Test complete report generation in all formats."""
        generated_files = self.report_gen.generate_complete_report(
            self.sample_results,
            formats=['txt', 'csv'],  # Skip xlsx if pandas not available
            project_name="Complete Test Project",
            user_name="Test User"
        )
        
        # Verify files were generated
        self.assertIsInstance(generated_files, dict)
        
        # Check each requested format
        for fmt, filepath in generated_files.items():
            self.assertTrue(os.path.exists(filepath))
            # Verify file is not empty
            self.assertGreater(os.path.getsize(filepath), 0)
    
    def test_unit_determination(self):
        """Test unit determination for parameters."""
        # Test various parameter types
        test_cases = [
            ('temperature', 'value', '°C'),
            ('pressure_loss', 'value', 'Pa'),
            ('power_rating', 'value', 'kW'),
            ('gas_velocity', 'value', 'm/s'),
            ('chamber_volume', 'value', 'm³'),
            ('residence_time', 'value', 's'),
            ('burner_diameter', 'value', 'm'),
            ('combustion_efficiency', 'value', '%'),
            ('unknown_param', 'value', '-')
        ]
        
        for param_name, value, expected_unit in test_cases:
            with self.subTest(parameter=param_name):
                unit = self.report_gen._determine_unit(param_name, value)
                self.assertEqual(unit, expected_unit)
    
    def test_empty_results_handling(self):
        """Test handling of empty or minimal results."""
        empty_results = {}
        
        # Should not crash with empty results
        report_path = self.report_gen.generate_text_report(empty_results)
        self.assertTrue(os.path.exists(report_path))
        
        csv_path = self.report_gen.generate_csv_export(empty_results)
        self.assertTrue(os.path.exists(csv_path))
    
    def test_custom_filename(self):
        """Test custom filename specification."""
        custom_name = "custom_report.txt"
        report_path = self.report_gen.generate_text_report(
            self.sample_results, 
            filename=custom_name
        )
        
        expected_path = os.path.join(self.temp_dir, custom_name)
        self.assertEqual(report_path, expected_path)
        self.assertTrue(os.path.exists(expected_path))
    
    def test_output_directory_creation(self):
        """Test automatic output directory creation."""
        new_dir = os.path.join(self.temp_dir, 'new_reports')
        new_report_gen = BurnerReportGenerator(output_dir=new_dir)
        
        # Directory should be created automatically
        self.assertTrue(os.path.exists(new_dir))


if __name__ == '__main__':
    unittest.main()