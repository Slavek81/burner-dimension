# tests/test_gui.py

"""
tests/test_gui.py

Unit tests for GUI module.
Tests GUI initialization, input validation, calculation orchestration, and file operations.
"""

import json
import os
import sys
import unittest
from unittest.mock import Mock, patch, MagicMock, mock_open

# Add src and gui directories to path for imports  # noqa: E402
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "gui"))

# Mock tkinter and calculation modules before importing GUI module
with patch.dict(
    "sys.modules",
    {
        "tkinter": MagicMock(),
        "tkinter.ttk": MagicMock(),
        "tkinter.filedialog": MagicMock(),
        "tkinter.messagebox": MagicMock(),
        "tkinter.scrolledtext": MagicMock(),
        "pandas": MagicMock(),
        "combustion": MagicMock(),
        "burner_design": MagicMock(),
        "chamber_design": MagicMock(),
        "radiation": MagicMock(),
        "pressure_losses": MagicMock(),
        "visualization": MagicMock(),
    },
):
    from gui import BurnerCalculatorGUI  # noqa: E402


class TestBurnerCalculatorGUI(unittest.TestCase):
    """Test cases for BurnerCalculatorGUI class."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock tkinter components
        self.mock_root = Mock()
        self.mock_root.title = Mock()
        self.mock_root.geometry = Mock()
        self.mock_root.minsize = Mock()
        self.mock_root.columnconfigure = Mock()
        self.mock_root.rowconfigure = Mock()

        # Mock all calculators
        self.mock_calculators = {
            "combustion": Mock(),
            "burner": Mock(),
            "chamber": Mock(),
            "radiation": Mock(),
            "pressure": Mock(),
        }

        # Mock available fuels
        self.mock_calculators["combustion"].get_available_fuels.return_value = [
            "natural_gas",
            "propane",
            "methane",
        ]

    @patch("gui.gui.CombustionCalculator")
    @patch("gui.gui.BurnerDesigner")
    @patch("gui.gui.ChamberDesigner")
    @patch("gui.gui.RadiationCalculator")
    @patch("gui.gui.PressureLossCalculator")
    def test_initialization_success(
        self, mock_pressure, mock_radiation, mock_chamber, mock_burner, mock_combustion
    ):
        """Test successful GUI initialization."""
        # Setup mocks
        mock_combustion.return_value = self.mock_calculators["combustion"]
        mock_burner.return_value = self.mock_calculators["burner"]
        mock_chamber.return_value = self.mock_calculators["chamber"]
        mock_radiation.return_value = self.mock_calculators["radiation"]
        mock_pressure.return_value = self.mock_calculators["pressure"]

        # Tkinter widgets are already mocked at module level

        # Create GUI instance
        gui = BurnerCalculatorGUI(self.mock_root)

        # Verify initialization
        self.assertEqual(gui.root, self.mock_root)
        self.assertIsInstance(gui.input_data, dict)
        self.assertIsInstance(gui.results, dict)
        self.assertIsInstance(gui.validation_errors, list)
        self.assertIsInstance(gui.calculators, dict)

        # Verify calculator initialization
        mock_combustion.assert_called_once()
        mock_burner.assert_called_once()
        mock_chamber.assert_called_once()
        mock_radiation.assert_called_once()
        mock_pressure.assert_called_once()

    @patch("gui.messagebox")
    @patch("gui.CombustionCalculator", side_effect=Exception("Calculator error"))
    @patch("gui.ttk")
    @patch("gui.tk")
    def test_initialization_calculator_error(
        self, mock_tk, mock_ttk, mock_combustion, mock_messagebox
    ):
        """Test GUI initialization with calculator error."""
        # Create GUI instance
        BurnerCalculatorGUI(self.mock_root)

        # Verify error handling
        mock_messagebox.showerror.assert_called_once()
        self.assertIn("Chyba inicializace", mock_messagebox.showerror.call_args[0][0])

    @patch("gui.ttk")
    @patch("gui.tk")
    def test_create_widgets(self, mock_tk, mock_ttk):
        """Test widget creation."""
        # Setup mocks
        mock_frame = Mock()
        mock_ttk.Frame.return_value = mock_frame
        mock_ttk.Notebook.return_value = Mock()
        mock_ttk.Label.return_value = Mock()

        with patch.object(BurnerCalculatorGUI, "__init__", lambda x, y: None):
            gui = BurnerCalculatorGUI.__new__(BurnerCalculatorGUI)
            gui.root = self.mock_root
            gui.calculators = self.mock_calculators
            gui.input_data = {}
            gui.results = {}
            gui.validation_errors = []

            # Mock required methods
            gui.create_input_tab = Mock()
            gui.create_combustion_tab = Mock()
            gui.create_burner_tab = Mock()
            gui.create_chamber_tab = Mock()
            gui.create_radiation_tab = Mock()
            gui.create_pressure_tab = Mock()
            gui.create_results_tab = Mock()
            gui.create_control_buttons = Mock()
            gui.setup_menu = Mock()
            gui.load_default_values = Mock()

            # Call method
            gui.create_widgets()

            # Verify widget creation calls
            mock_ttk.Frame.assert_called()
            gui.create_input_tab.assert_called_once()
            gui.create_combustion_tab.assert_called_once()
            gui.create_burner_tab.assert_called_once()
            gui.create_chamber_tab.assert_called_once()
            gui.create_radiation_tab.assert_called_once()
            gui.create_pressure_tab.assert_called_once()
            gui.create_results_tab.assert_called_once()
            gui.create_control_buttons.assert_called_once()

    def test_load_default_values(self):
        """Test loading of default values."""
        with patch.object(BurnerCalculatorGUI, "__init__", lambda x, y: None):
            gui = BurnerCalculatorGUI.__new__(BurnerCalculatorGUI)
            gui.input_vars = {
                "fuel_type": Mock(),
                "fuel_flow_rate": Mock(),
                "excess_air_ratio": Mock(),
                "ambient_temperature": Mock(),
                "ambient_pressure": Mock(),
                "max_gas_velocity": Mock(),
                "supply_pressure": Mock(),
                "target_residence_time": Mock(),
                "wall_insulation_thickness": Mock(),
                "target_efficiency": Mock(),
            }

            # Call method
            gui.load_default_values()

            # Verify default values are set
            gui.input_vars["fuel_type"].set.assert_called_with("natural_gas")
            gui.input_vars["fuel_flow_rate"].insert.assert_called_with(0, "0.002")
            gui.input_vars["excess_air_ratio"].insert.assert_called_with(0, "1.2")
            gui.input_vars["ambient_temperature"].insert.assert_called_with(0, "20")
            gui.input_vars["ambient_pressure"].insert.assert_called_with(0, "101325")

    def test_collect_input_data(self):
        """Test input data collection."""
        with patch.object(BurnerCalculatorGUI, "__init__", lambda x, y: None):
            gui = BurnerCalculatorGUI.__new__(BurnerCalculatorGUI)
            gui.input_vars = {
                "fuel_type": Mock(),
                "fuel_flow_rate": Mock(),
                "excess_air_ratio": Mock(),
                "ambient_temperature": Mock(),
                "ambient_pressure": Mock(),
                "max_gas_velocity": Mock(),
                "supply_pressure": Mock(),
                "target_residence_time": Mock(),
                "wall_insulation_thickness": Mock(),
                "target_efficiency": Mock(),
            }

            # Mock widget get methods
            gui.input_vars["fuel_type"].get.return_value = "natural_gas"
            gui.input_vars["fuel_flow_rate"].get.return_value = "0.002"
            gui.input_vars["excess_air_ratio"].get.return_value = "1.2"
            gui.input_vars["ambient_temperature"].get.return_value = "20"
            gui.input_vars["ambient_pressure"].get.return_value = "101325"
            gui.input_vars["max_gas_velocity"].get.return_value = "25"
            gui.input_vars["supply_pressure"].get.return_value = "3000"
            gui.input_vars["target_residence_time"].get.return_value = "0.5"
            gui.input_vars["wall_insulation_thickness"].get.return_value = "0.1"
            gui.input_vars["target_efficiency"].get.return_value = "0.85"

            # Call method
            result = gui.collect_input_data()

            # Verify collected data
            self.assertEqual(result["fuel_type"], "natural_gas")
            self.assertEqual(result["fuel_flow_rate"], 0.002)
            self.assertEqual(result["excess_air_ratio"], 1.2)
            self.assertEqual(result["ambient_temperature"], 293.15)  # Converted to K
            self.assertEqual(result["ambient_pressure"], 101325)
            self.assertEqual(result["max_gas_velocity"], 25)
            self.assertEqual(result["supply_pressure"], 3000)
            self.assertEqual(result["target_residence_time"], 0.5)
            self.assertEqual(result["wall_insulation_thickness"], 0.1)
            self.assertEqual(result["target_efficiency"], 0.85)

    def test_validate_input_valid(self):
        """Test input validation with valid data."""
        with patch.object(BurnerCalculatorGUI, "__init__", lambda x, y: None):
            gui = BurnerCalculatorGUI.__new__(BurnerCalculatorGUI)
            gui.validation_errors = []
            gui.input_data = {
                "fuel_flow_rate": 0.002,
                "excess_air_ratio": 1.2,
                "ambient_temperature": 293.15,
                "ambient_pressure": 101325,
                "max_gas_velocity": 25,
                "supply_pressure": 3000,
                "target_residence_time": 0.5,
                "wall_insulation_thickness": 0.1,
                "target_efficiency": 0.85,
            }

            # Call method
            result = gui.validate_input()

            # Should be valid
            self.assertTrue(result)
            self.assertEqual(len(gui.validation_errors), 0)

    def test_validate_input_invalid(self):
        """Test input validation with invalid data."""
        with patch.object(BurnerCalculatorGUI, "__init__", lambda x, y: None):
            gui = BurnerCalculatorGUI.__new__(BurnerCalculatorGUI)
            gui.validation_errors = []
            gui.input_data = {
                "fuel_flow_rate": -0.002,  # Invalid: negative
                "excess_air_ratio": 0.5,  # Invalid: too low
                "ambient_temperature": 200,  # Invalid: too low
                "ambient_pressure": -1000,  # Invalid: negative
                "max_gas_velocity": -10,  # Invalid: negative
                "supply_pressure": -100,  # Invalid: negative
                "target_residence_time": -0.1,  # Invalid: negative
                "wall_insulation_thickness": -0.01,  # Invalid: negative
                "target_efficiency": 1.5,  # Invalid: >1
            }

            # Call method
            result = gui.validate_input()

            # Should be invalid
            self.assertFalse(result)
            self.assertGreater(len(gui.validation_errors), 0)

    @patch("gui.threading.Thread")
    def test_run_calculations(self, mock_thread):
        """Test calculation execution."""
        with patch.object(BurnerCalculatorGUI, "__init__", lambda x, y: None):
            gui = BurnerCalculatorGUI.__new__(BurnerCalculatorGUI)
            gui.collect_input_data = Mock(return_value={"fuel_type": "natural_gas"})
            gui.validate_input = Mock(return_value=True)
            gui._update_status = Mock()

            # Mock thread
            mock_thread_instance = Mock()
            mock_thread.return_value = mock_thread_instance

            # Call method
            gui.run_calculations()

            # Verify thread creation and start
            mock_thread.assert_called_once()
            mock_thread_instance.start.assert_called_once()
            gui._update_status.assert_called_with("Probíhají výpočty...")

    @patch("gui.messagebox")
    def test_run_calculations_validation_error(self, mock_messagebox):
        """Test calculation execution with validation errors."""
        with patch.object(BurnerCalculatorGUI, "__init__", lambda x, y: None):
            gui = BurnerCalculatorGUI.__new__(BurnerCalculatorGUI)
            gui.collect_input_data = Mock(return_value={})
            gui.validate_input = Mock(return_value=False)
            gui.validation_errors = ["Error 1", "Error 2"]

            # Call method
            gui.run_calculations()

            # Verify error message
            mock_messagebox.showerror.assert_called_once()
            error_args = mock_messagebox.showerror.call_args[0]
            self.assertIn("Chybné vstupní", error_args[0])
            self.assertIn("Error 1", error_args[1])
            self.assertIn("Error 2", error_args[1])

    def test_perform_calculations_success(self):
        """Test successful calculation execution."""
        with patch.object(BurnerCalculatorGUI, "__init__", lambda x, y: None):
            gui = BurnerCalculatorGUI.__new__(BurnerCalculatorGUI)
            gui.input_data = {
                "fuel_type": "natural_gas",
                "fuel_flow_rate": 0.002,
                "excess_air_ratio": 1.2,
                "ambient_temperature": 293.15,
                "supply_pressure": 3000,
                "target_residence_time": 0.5,
                "wall_insulation_thickness": 0.1,
                "target_efficiency": 0.85,
            }
            gui.results = {}
            gui._update_status = Mock()
            gui._calculation_finished = Mock()

            # Mock calculator results
            mock_combustion_result = Mock()
            mock_combustion_result.adiabatic_flame_temperature = 2100
            mock_burner_result = Mock()
            mock_chamber_result = Mock()
            mock_radiation_result = Mock()

            gui.calculators = {
                "combustion": Mock(),
                "burner": Mock(),
                "chamber": Mock(),
                "radiation": Mock(),
                "pressure": Mock(),
            }

            gui.calculators["combustion"].calculate_combustion_products.return_value = (
                mock_combustion_result
            )
            gui.calculators["burner"].design_burner.return_value = mock_burner_result
            gui.calculators["chamber"].design_chamber.return_value = mock_chamber_result
            gui.calculators["radiation"].calculate_flame_radiation.return_value = (
                mock_radiation_result
            )

            # Call method
            gui._perform_calculations()

            # Verify calculations were called
            gui.calculators[
                "combustion"
            ].calculate_combustion_products.assert_called_once()
            gui.calculators["burner"].design_burner.assert_called_once()
            gui.calculators["chamber"].design_chamber.assert_called_once()
            gui.calculators["radiation"].calculate_flame_radiation.assert_called_once()

            # Verify results stored
            self.assertIn("combustion", gui.results)
            self.assertIn("burner", gui.results)
            self.assertIn("chamber", gui.results)
            self.assertIn("radiation", gui.results)

    def test_perform_calculations_error_handling(self):
        """Test calculation error handling."""
        with patch.object(BurnerCalculatorGUI, "__init__", lambda x, y: None):
            gui = BurnerCalculatorGUI.__new__(BurnerCalculatorGUI)
            gui.input_data = {
                "fuel_type": "natural_gas",
                "fuel_flow_rate": 0.002,
                "excess_air_ratio": 1.2,
            }
            gui.results = {}
            gui._update_status = Mock()
            gui._calculation_finished = Mock()

            # Mock calculator that raises exception
            gui.calculators = {
                "combustion": Mock(),
                "burner": Mock(),
                "chamber": Mock(),
                "radiation": Mock(),
                "pressure": Mock(),
            }

            gui.calculators["combustion"].calculate_combustion_products.side_effect = (
                Exception("Calculation error")
            )

            # Call method
            gui._perform_calculations()

            # Verify error handling
            self.assertIn("errors", gui.results)
            self.assertIn("combustion", gui.results["errors"])

    @patch("gui.filedialog")
    def test_load_input_file_success(self, mock_filedialog):
        """Test successful input file loading."""
        with patch.object(BurnerCalculatorGUI, "__init__", lambda x, y: None):
            gui = BurnerCalculatorGUI.__new__(BurnerCalculatorGUI)
            gui.input_vars = {
                "fuel_type": Mock(),
                "fuel_flow_rate": Mock(),
                "excess_air_ratio": Mock(),
            }

            # Mock file dialog
            test_file = "/test/input.json"
            mock_filedialog.askopenfilename.return_value = test_file

            # Mock file content
            test_data = {
                "fuel_type": "propane",
                "fuel_flow_rate": 0.003,
                "excess_air_ratio": 1.3,
            }

            with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
                # Call method
                gui.load_input_file()

                # Verify data loaded
                gui.input_vars["fuel_type"].set.assert_called_with("propane")
                gui.input_vars["fuel_flow_rate"].delete.assert_called()
                gui.input_vars["fuel_flow_rate"].insert.assert_called_with(0, "0.003")

    @patch("gui.filedialog")
    @patch("gui.messagebox")
    def test_load_input_file_error(self, mock_messagebox, mock_filedialog):
        """Test input file loading error handling."""
        with patch.object(BurnerCalculatorGUI, "__init__", lambda x, y: None):
            gui = BurnerCalculatorGUI.__new__(BurnerCalculatorGUI)

            # Mock file dialog
            test_file = "/test/invalid.json"
            mock_filedialog.askopenfilename.return_value = test_file

            # Mock file error
            with patch(
                "builtins.open", side_effect=FileNotFoundError("File not found")
            ):
                # Call method
                gui.load_input_file()

                # Verify error message
                mock_messagebox.showerror.assert_called_once()

    @patch("gui.filedialog")
    def test_save_input_file_success(self, mock_filedialog):
        """Test successful input file saving."""
        with patch.object(BurnerCalculatorGUI, "__init__", lambda x, y: None):
            gui = BurnerCalculatorGUI.__new__(BurnerCalculatorGUI)
            gui.collect_input_data = Mock(
                return_value={"fuel_type": "natural_gas", "fuel_flow_rate": 0.002}
            )

            # Mock file dialog
            test_file = "/test/output.json"
            mock_filedialog.asksaveasfilename.return_value = test_file

            with patch("builtins.open", mock_open()) as mock_file:
                # Call method
                gui.save_input_file()

                # Verify file written
                mock_file.assert_called_once_with(test_file, "w", encoding="utf-8")
                mock_file().write.assert_called()

    @patch("gui.filedialog")
    @patch("gui.messagebox")
    def test_save_input_file_error(self, mock_messagebox, mock_filedialog):
        """Test input file saving error handling."""
        with patch.object(BurnerCalculatorGUI, "__init__", lambda x, y: None):
            gui = BurnerCalculatorGUI.__new__(BurnerCalculatorGUI)
            gui.collect_input_data = Mock(return_value={})

            # Mock file dialog
            test_file = "/test/output.json"
            mock_filedialog.asksaveasfilename.return_value = test_file

            # Mock file error
            with patch(
                "builtins.open", side_effect=PermissionError("Permission denied")
            ):
                # Call method
                gui.save_input_file()

                # Verify error message
                mock_messagebox.showerror.assert_called_once()

    @patch("gui.filedialog")
    def test_export_results_success(self, mock_filedialog):
        """Test successful results export."""
        with patch.object(BurnerCalculatorGUI, "__init__", lambda x, y: None):
            gui = BurnerCalculatorGUI.__new__(BurnerCalculatorGUI)
            gui.results = {"combustion": Mock(), "burner": Mock(), "chamber": Mock()}

            # Mock file dialog
            test_file = "/test/results.txt"
            mock_filedialog.asksaveasfilename.return_value = test_file

            with patch("builtins.open", mock_open()) as mock_file:
                # Call method
                gui.export_results()

                # Verify file written
                mock_file.assert_called_once_with(test_file, "w", encoding="utf-8")
                mock_file().write.assert_called()

    @patch("gui.messagebox")
    def test_export_results_no_data(self, mock_messagebox):
        """Test results export with no data."""
        with patch.object(BurnerCalculatorGUI, "__init__", lambda x, y: None):
            gui = BurnerCalculatorGUI.__new__(BurnerCalculatorGUI)
            gui.results = {}

            # Call method
            gui.export_results()

            # Verify warning message
            mock_messagebox.showwarning.assert_called_once()
            warning_args = mock_messagebox.showwarning.call_args[0]
            self.assertIn("žádné výsledky", warning_args[1])

    def test_update_status(self):
        """Test status update."""
        with patch.object(BurnerCalculatorGUI, "__init__", lambda x, y: None):
            gui = BurnerCalculatorGUI.__new__(BurnerCalculatorGUI)
            gui.status_label = Mock()

            # Call method
            gui._update_status("Test message")

            # Verify status updated
            gui.status_label.config.assert_called_with(text="Test message")

    @patch("gui.messagebox")
    def test_calculation_finished_success(self, mock_messagebox):
        """Test calculation finished with success."""
        with patch.object(BurnerCalculatorGUI, "__init__", lambda x, y: None):
            gui = BurnerCalculatorGUI.__new__(BurnerCalculatorGUI)
            gui.results = {"combustion": Mock(), "burner": Mock()}
            gui._update_status = Mock()
            gui._display_all_results = Mock()

            # Call method
            gui._calculation_finished()

            # Verify success handling
            gui._update_status.assert_called_with("Výpočty dokončeny")
            gui._display_all_results.assert_called_once()
            mock_messagebox.showinfo.assert_called_once()

    @patch("gui.messagebox")
    def test_calculation_finished_with_errors(self, mock_messagebox):
        """Test calculation finished with errors."""
        with patch.object(BurnerCalculatorGUI, "__init__", lambda x, y: None):
            gui = BurnerCalculatorGUI.__new__(BurnerCalculatorGUI)
            gui.results = {"errors": {"combustion": "Error occurred"}}
            gui._update_status = Mock()
            gui._display_all_results = Mock()

            # Call method
            gui._calculation_finished()

            # Verify error handling
            gui._update_status.assert_called_with("Výpočty dokončeny s chybami")
            mock_messagebox.showwarning.assert_called_once()

    def test_display_all_results(self):
        """Test display of all results."""
        with patch.object(BurnerCalculatorGUI, "__init__", lambda x, y: None):
            gui = BurnerCalculatorGUI.__new__(BurnerCalculatorGUI)
            gui.results = {
                "combustion": Mock(),
                "burner": Mock(),
                "chamber": Mock(),
                "radiation": Mock(),
            }

            # Mock display methods
            gui._display_combustion_results = Mock()
            gui._display_burner_results = Mock()
            gui._display_chamber_results = Mock()
            gui._display_radiation_results = Mock()
            gui._display_pressure_results = Mock()

            # Call method
            gui._display_all_results()

            # Verify all display methods called
            gui._display_combustion_results.assert_called_once()
            gui._display_burner_results.assert_called_once()
            gui._display_chamber_results.assert_called_once()
            gui._display_radiation_results.assert_called_once()

    def test_clear_results(self):
        """Test clearing of results."""
        with patch.object(BurnerCalculatorGUI, "__init__", lambda x, y: None):
            gui = BurnerCalculatorGUI.__new__(BurnerCalculatorGUI)
            gui.results = {"old_data": "value"}
            gui.combustion_results_text = Mock()
            gui.burner_results_text = Mock()
            gui.chamber_results_text = Mock()
            gui.radiation_results_text = Mock()
            gui.pressure_results_text = Mock()
            gui.overall_results_text = Mock()
            gui._update_status = Mock()

            # Call method
            gui.clear_results()

            # Verify results cleared
            self.assertEqual(gui.results, {})
            gui.combustion_results_text.delete.assert_called_with("1.0", "end")
            gui.burner_results_text.delete.assert_called_with("1.0", "end")
            gui.chamber_results_text.delete.assert_called_with("1.0", "end")
            gui.radiation_results_text.delete.assert_called_with("1.0", "end")
            gui.pressure_results_text.delete.assert_called_with("1.0", "end")
            gui.overall_results_text.delete.assert_called_with("1.0", "end")

    def test_input_data_collection_type_conversion(self):
        """Test proper type conversion in input data collection."""
        with patch.object(BurnerCalculatorGUI, "__init__", lambda x, y: None):
            gui = BurnerCalculatorGUI.__new__(BurnerCalculatorGUI)
            gui.input_vars = {
                "fuel_type": Mock(),
                "fuel_flow_rate": Mock(),
                "excess_air_ratio": Mock(),
                "ambient_temperature": Mock(),
            }

            # Mock widget returns with string values
            gui.input_vars["fuel_type"].get.return_value = "natural_gas"
            gui.input_vars["fuel_flow_rate"].get.return_value = "0.002"
            gui.input_vars["excess_air_ratio"].get.return_value = "1.2"
            gui.input_vars["ambient_temperature"].get.return_value = "25.5"

            # Call method
            result = gui.collect_input_data()

            # Verify type conversions
            self.assertIsInstance(result["fuel_flow_rate"], float)
            self.assertIsInstance(result["excess_air_ratio"], float)
            self.assertIsInstance(result["ambient_temperature"], float)
            self.assertEqual(result["ambient_temperature"], 298.65)  # 25.5°C to K

    def test_validation_edge_cases(self):
        """Test validation with edge case values."""
        with patch.object(BurnerCalculatorGUI, "__init__", lambda x, y: None):
            gui = BurnerCalculatorGUI.__new__(BurnerCalculatorGUI)
            gui.validation_errors = []

            # Test with boundary values
            gui.input_data = {
                "fuel_flow_rate": 0.0001,  # Very small but positive
                "excess_air_ratio": 1.0,  # Minimum stoichiometric
                "ambient_temperature": 223.15,  # -50°C (cold but valid)
                "ambient_pressure": 50000,  # Low pressure but positive
                "max_gas_velocity": 0.1,  # Very low but positive
                "supply_pressure": 100,  # Low but positive
                "target_residence_time": 0.01,  # Very short but positive
                "wall_insulation_thickness": 0.001,  # Very thin but positive
                "target_efficiency": 0.1,  # Low but valid
            }

            # Call method
            result = gui.validate_input()

            # Should still be valid
            self.assertTrue(result)

    def test_error_accumulation_in_validation(self):
        """Test that validation accumulates all errors."""
        with patch.object(BurnerCalculatorGUI, "__init__", lambda x, y: None):
            gui = BurnerCalculatorGUI.__new__(BurnerCalculatorGUI)
            gui.validation_errors = []

            # Multiple invalid values
            gui.input_data = {
                "fuel_flow_rate": -0.002,  # Invalid
                "excess_air_ratio": 0.5,  # Invalid
                "ambient_temperature": 100,  # Invalid
                "ambient_pressure": -1000,  # Invalid
                "max_gas_velocity": -10,  # Invalid
                "supply_pressure": -100,  # Invalid
                "target_residence_time": -0.1,  # Invalid
                "wall_insulation_thickness": -0.01,  # Invalid
                "target_efficiency": 1.5,  # Invalid
            }

            # Call method
            result = gui.validate_input()

            # Should accumulate multiple errors
            self.assertFalse(result)
            self.assertGreaterEqual(len(gui.validation_errors), 8)  # At least 8 errors


if __name__ == "__main__":
    unittest.main()
