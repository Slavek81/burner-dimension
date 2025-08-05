# Testing Procedures and Guidelines

## Table of Contents
1. [Testing Philosophy](#testing-philosophy)
2. [Test Architecture](#test-architecture)
3. [Unit Testing](#unit-testing)
4. [Integration Testing](#integration-testing)
5. [GUI Testing](#gui-testing)
6. [Performance Testing](#performance-testing)
7. [Test Data Management](#test-data-management)
8. [Continuous Testing](#continuous-testing)

## Testing Philosophy

### Testing Principles

#### 1. Comprehensive Coverage
- **Calculation Accuracy**: Verify mathematical correctness
- **Input Validation**: Test boundary conditions and error cases
- **Integration**: Ensure modules work together correctly
- **User Interface**: Validate GUI functionality and usability
- **Performance**: Monitor speed and memory usage

#### 2. Test-Driven Development (TDD)
```python
# Example TDD cycle for new feature
def test_new_fuel_type_calculation():
    """Test calculation with biogas fuel type."""
    calculator = CombustionCalculator()
    
    # This test should fail initially (Red)
    result = calculator.calculate_combustion_products('biogas', 0.01, 1.2)
    
    # Expected behavior
    assert result.fuel_flow_rate == 0.01
    assert result.excess_air_ratio == 1.2
    assert 1200 < result.adiabatic_flame_temperature < 2000

# Now implement the feature to make test pass (Green)
# Then refactor the implementation (Refactor)
```

#### 3. Quality Gates
- **Minimum Coverage**: 85% code coverage required
- **Zero Failures**: All tests must pass before merge
- **Performance Regression**: No significant performance degradation
- **Documentation**: Tests must be documented and maintainable

## Test Architecture

### Test Directory Structure
```
tests/
├── unit/                  # Unit tests for individual modules
│   ├── test_combustion.py
│   ├── test_burner_design.py
│   ├── test_chamber_design.py
│   ├── test_radiation.py
│   ├── test_pressure_losses.py
│   ├── test_visualization.py
│   └── test_report.py
├── integration/           # Integration tests
│   ├── test_calculation_workflow.py
│   ├── test_data_flow.py
│   └── test_error_handling.py
├── gui/                   # GUI-specific tests
│   ├── test_main_window.py
│   ├── test_input_validation.py
│   └── test_export_functions.py
├── performance/           # Performance and benchmark tests
│   ├── test_calculation_speed.py
│   ├── test_memory_usage.py
│   └── test_scalability.py
├── fixtures/              # Test data and fixtures
│   ├── sample_inputs.json
│   ├── expected_results.json
│   ├── test_fuels.json
│   └── benchmark_data.json
├── conftest.py           # Pytest configuration and fixtures
├── test_config.py        # Test configuration
└── utils.py              # Test utilities and helpers
```

### Test Categories

#### 1. Unit Tests (Fast, Isolated)
- Test individual functions and methods
- Mock external dependencies
- Focus on edge cases and error conditions
- Run quickly (< 1 second per test)

#### 2. Integration Tests (Medium Speed)
- Test module interactions
- Use real data and configurations
- Verify data flow between components
- Acceptable runtime (< 10 seconds per test)

#### 3. System Tests (Slower, Comprehensive)
- End-to-end workflow testing
- Full application integration
- Real-world scenarios
- Longer runtime acceptable (< 60 seconds per test)

## Unit Testing

### Testing Individual Modules

#### Combustion Module Tests
```python
# tests/unit/test_combustion.py
import pytest
import json
from unittest.mock import patch, mock_open
from src.combustion import CombustionCalculator, CombustionResults

class TestCombustionCalculator:
    """Comprehensive test suite for CombustionCalculator."""
    
    @pytest.fixture
    def calculator(self):
        """Create calculator with mocked fuel data."""
        mock_fuel_data = {
            "constants": {
                "universal_gas_constant": 8314.46,
                "standard_temperature": 273.15,
                "standard_pressure": 101325
            },
            "fuels": {
                "natural_gas": {
                    "properties": {
                        "lower_heating_value_mass": 50000000,
                        "molecular_weight": 16.04,
                        "density": 0.717,
                        "air_fuel_ratio_mass": 17.2
                    }
                }
            }
        }
        
        with patch('builtins.open', mock_open(read_data=json.dumps(mock_fuel_data))):
            return CombustionCalculator()
    
    def test_constructor_default_path(self):
        """Test constructor with default fuel data path."""
        with patch('builtins.open', mock_open(read_data='{"fuels": {}}')):
            calc = CombustionCalculator()
            assert calc.fuel_data is not None
    
    def test_constructor_custom_path(self):
        """Test constructor with custom fuel data path."""
        with patch('builtins.open', mock_open(read_data='{"fuels": {}}')):
            calc = CombustionCalculator("custom_path.json")
            assert calc.fuel_data is not None
    
    def test_constructor_missing_file(self):
        """Test constructor with missing fuel data file."""
        with patch('builtins.open', side_effect=FileNotFoundError):
            with pytest.raises(FileNotFoundError, match="Soubor s daty paliv nebyl nalezen"):
                CombustionCalculator("missing_file.json")
    
    def test_stoichiometric_air_natural_gas(self, calculator):
        """Test stoichiometric air calculation for natural gas."""
        fuel_flow = 0.01  # kg/s
        air_flow = calculator.calculate_stoichiometric_air('natural_gas', fuel_flow)
        
        expected = fuel_flow * 17.2  # Air-fuel ratio
        assert abs(air_flow - expected) < 1e-10
    
    def test_stoichiometric_air_invalid_fuel(self, calculator):
        """Test error handling for invalid fuel type."""
        with pytest.raises(ValueError, match="Nepodporovaný typ paliva"):
            calculator.calculate_stoichiometric_air('invalid_fuel', 0.01)
    
    @pytest.mark.parametrize("fuel_flow,expected", [
        (0.001, 0.0172),
        (0.01, 0.172),
        (0.1, 1.72),
    ])
    def test_stoichiometric_air_various_flows(self, calculator, fuel_flow, expected):
        """Test stoichiometric air calculation with various flow rates."""
        air_flow = calculator.calculate_stoichiometric_air('natural_gas', fuel_flow)
        assert abs(air_flow - expected) < 1e-10
    
    def test_combustion_products_valid_inputs(self, calculator):
        """Test combustion products calculation with valid inputs."""
        result = calculator.calculate_combustion_products('natural_gas', 0.01, 1.2)
        
        # Verify result type and basic properties
        assert isinstance(result, CombustionResults)
        assert result.fuel_flow_rate == 0.01
        assert result.excess_air_ratio == 1.2
        assert result.air_flow_rate > result.fuel_flow_rate
        assert result.flue_gas_flow_rate > result.air_flow_rate
        assert result.heat_release_rate > 0
        assert result.adiabatic_flame_temperature > 1000
    
    def test_combustion_products_stoichiometric(self, calculator):
        """Test combustion products with stoichiometric air (λ=1.0)."""
        result = calculator.calculate_combustion_products('natural_gas', 0.01, 1.0)
        
        assert result.excess_air_ratio == 1.0
        assert result.o2_volume_percent < 0.1  # Minimal oxygen in products
    
    def test_combustion_products_excess_air(self, calculator):
        """Test combustion products with excess air."""
        result = calculator.calculate_combustion_products('natural_gas', 0.01, 1.5)
        
        assert result.excess_air_ratio == 1.5
        assert result.o2_volume_percent > 5.0  # Significant oxygen in products
        assert result.co2_volume_percent < 10.0  # Diluted CO2
    
    def test_combustion_products_invalid_inputs(self, calculator):
        """Test error handling for invalid inputs."""
        # Invalid fuel type
        with pytest.raises(ValueError, match="Nepodporovaný typ paliva"):
            calculator.calculate_combustion_products('invalid', 0.01, 1.2)
        
        # Negative fuel flow
        with pytest.raises(ValueError, match="větší než nula"):
            calculator.calculate_combustion_products('natural_gas', -0.01, 1.2)
        
        # Invalid excess air ratio
        with pytest.raises(ValueError, match="≥ 1.0"):
            calculator.calculate_combustion_products('natural_gas', 0.01, 0.8)
    
    def test_adiabatic_temperature_calculation(self, calculator):
        """Test adiabatic flame temperature calculation."""
        # Test internal method through public interface
        result = calculator.calculate_combustion_products('natural_gas', 0.01, 1.2)
        
        # Temperature should be in reasonable range
        assert 1500 < result.adiabatic_flame_temperature < 2500
        
        # Higher excess air should give lower temperature
        result_high_air = calculator.calculate_combustion_products('natural_gas', 0.01, 1.8)
        assert result_high_air.adiabatic_flame_temperature < result.adiabatic_flame_temperature
    
    def test_flue_gas_composition(self, calculator):
        """Test flue gas composition calculation."""
        result = calculator.calculate_combustion_products('natural_gas', 0.01, 1.2)
        
        # CO2 and O2 percentages should be reasonable
        assert 8 < result.co2_volume_percent < 15
        assert 2 < result.o2_volume_percent < 6
        
        # Total percentage should be reasonable (not accounting for N2 and H2O)
        assert result.co2_volume_percent + result.o2_volume_percent < 20
    
    def test_get_fuel_properties(self, calculator):
        """Test fuel properties retrieval."""
        props = calculator.get_fuel_properties('natural_gas')
        
        assert 'properties' in props
        assert 'lower_heating_value_mass' in props['properties']
        assert props['properties']['lower_heating_value_mass'] == 50000000
    
    def test_get_available_fuels(self, calculator):
        """Test available fuels list."""
        fuels = calculator.get_available_fuels()
        
        assert isinstance(fuels, list)
        assert 'natural_gas' in fuels
```

#### Burner Design Module Tests
```python
# tests/unit/test_burner_design.py
import pytest
from unittest.mock import Mock, patch
from src.burner_design import BurnerDesigner, BurnerDesignResults
from src.combustion import CombustionCalculator, CombustionResults

class TestBurnerDesigner:
    """Test suite for BurnerDesigner class."""
    
    @pytest.fixture
    def mock_combustion_calc(self):
        """Create mock combustion calculator."""
        mock_calc = Mock(spec=CombustionCalculator)
        mock_calc.get_fuel_properties.return_value = {
            'properties': {
                'lower_heating_value_mass': 50000000,
                'molecular_weight': 16.04,
                'density': 0.717
            }
        }
        mock_calc.calculate_combustion_products.return_value = CombustionResults(
            fuel_flow_rate=0.002,
            air_flow_rate=0.0344,
            flue_gas_flow_rate=0.0364,
            adiabatic_flame_temperature=1900,
            heat_release_rate=100000,
            excess_air_ratio=1.2,
            co2_volume_percent=10.0,
            o2_volume_percent=3.5
        )
        mock_calc.constants = {
            'universal_gas_constant': 8314.46,
            'standard_pressure': 101325
        }
        return mock_calc
    
    @pytest.fixture
    def designer(self, mock_combustion_calc):
        """Create burner designer with mocked dependencies."""
        return BurnerDesigner(mock_combustion_calc, safety_factor=1.2)
    
    def test_constructor_default(self):
        """Test constructor with default parameters."""
        with patch('src.burner_design.CombustionCalculator'):
            designer = BurnerDesigner()
            assert designer.safety_factor == 1.2
            assert designer.MAX_GAS_VELOCITY == 100.0
            assert designer.MIN_GAS_VELOCITY == 5.0
    
    def test_constructor_custom_safety_factor(self, mock_combustion_calc):
        """Test constructor with custom safety factor."""
        designer = BurnerDesigner(mock_combustion_calc, safety_factor=1.5)
        assert designer.safety_factor == 1.5
    
    def test_design_burner_valid_inputs(self, designer):
        """Test burner design with valid inputs."""
        result = designer.design_burner(
            fuel_type='natural_gas',
            required_power=100000,
            supply_pressure=3000,
            target_velocity=25.0,
            excess_air_ratio=1.2
        )
        
        assert isinstance(result, BurnerDesignResults)
        assert result.burner_diameter > 0
        assert result.burner_area > 0
        assert result.gas_velocity == 25.0
        assert result.burner_pressure_drop > 0
        assert result.heat_release_density > 0
    
    def test_design_burner_invalid_power(self, designer):
        """Test error handling for invalid power."""
        with pytest.raises(ValueError, match="větší než nula"):
            designer.design_burner('natural_gas', -1000, 3000)
    
    def test_design_burner_invalid_pressure(self, designer):
        """Test error handling for invalid pressure."""
        with pytest.raises(ValueError, match="tlak plynu"):
            designer.design_burner('natural_gas', 100000, -100)
    
    def test_design_burner_insufficient_pressure(self, designer):
        """Test error handling for insufficient supply pressure."""
        with pytest.raises(ValueError, match="Nedostatečný tlak"):
            designer.design_burner('natural_gas', 1000000, 100)  # Very high power, low pressure
    
    def test_gas_density_calculation(self, designer):
        """Test gas density calculation."""
        density = designer._calculate_gas_density('natural_gas', 3000, 293.15)
        
        assert density > 0
        assert 0.5 < density < 2.0  # Reasonable range for gas density
    
    def test_optimal_velocity_calculation(self, designer):
        """Test optimal velocity calculation."""
        velocity = designer._calculate_optimal_velocity('natural_gas', 100000)
        
        assert designer.MIN_GAS_VELOCITY <= velocity <= designer.MAX_GAS_VELOCITY
    
    def test_burner_pressure_drop_calculation(self, designer):
        """Test burner pressure drop calculation."""
        pressure_drop = designer._calculate_burner_pressure_drop(0.8, 25.0, 0.05)
        
        assert pressure_drop > 0
        assert pressure_drop < 10000  # Reasonable upper limit
    
    def test_flame_length_calculation(self, designer):
        """Test flame length estimation."""
        flame_length = designer._calculate_flame_length(0.05, 25.0, 'natural_gas')
        
        assert flame_length > 0
        assert 0.1 < flame_length < 5.0  # Reasonable range
    
    def test_validate_design(self, designer):
        """Test design validation."""
        result = BurnerDesignResults(
            burner_diameter=0.05,
            burner_area=0.002,
            gas_velocity=25.0,
            burner_pressure_drop=500,
            required_supply_pressure=600,
            heat_release_density=50e6,
            burner_length=0.15,
            flame_length=0.8
        )
        
        validation = designer.validate_design(result)
        
        assert isinstance(validation, dict)
        assert 'velocity_in_range' in validation
        assert 'heat_density_acceptable' in validation
        assert 'reasonable_dimensions' in validation
        assert validation['velocity_in_range'] is True
    
    def test_get_design_recommendations(self, designer):
        """Test design recommendations generation."""
        # Create design with some issues
        result = BurnerDesignResults(
            burner_diameter=0.05,
            burner_area=0.002,
            gas_velocity=2.0,  # Too low
            burner_pressure_drop=500,
            required_supply_pressure=600,
            heat_release_density=200e6,  # Too high
            burner_length=0.15,
            flame_length=2.0  # Very long
        )
        
        recommendations = designer.get_design_recommendations(result)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        # Should contain recommendations about low velocity and high heat density
```

### Testing Best Practices

#### 1. Test Naming Conventions
```python
def test_[method_name]_[scenario]_[expected_result]():
    """
    Test naming pattern:
    - test_: pytest requirement
    - method_name: what is being tested
    - scenario: test conditions
    - expected_result: what should happen
    """
    pass

# Examples:
def test_calculate_stoichiometric_air_natural_gas_returns_correct_ratio():
def test_design_burner_invalid_pressure_raises_value_error():
def test_validate_design_high_velocity_returns_false():
```

#### 2. Fixture Usage
```python
@pytest.fixture(scope="session")
def fuel_database():
    """Session-scoped fixture for fuel data."""
    return load_test_fuel_data()

@pytest.fixture(scope="class")
def calculation_setup():
    """Class-scoped fixture for test setup."""
    return create_test_calculators()

@pytest.fixture
def sample_input():
    """Function-scoped fixture (default)."""
    return {"fuel_type": "natural_gas", "power": 100000}
```

#### 3. Parametrized Tests
```python
@pytest.mark.parametrize("fuel_type,expected_ratio", [
    ("natural_gas", 17.2),
    ("propane", 15.7),
    ("methane", 17.2),
])
def test_air_fuel_ratios(fuel_type, expected_ratio):
    """Test air-fuel ratios for different fuel types."""
    calculator = CombustionCalculator()
    ratio = calculator.get_air_fuel_ratio(fuel_type)
    assert abs(ratio - expected_ratio) < 0.1
```

## Integration Testing

### Module Integration Tests

#### Calculation Workflow Integration
```python
# tests/integration/test_calculation_workflow.py
import pytest
from src.combustion import CombustionCalculator
from src.burner_design import BurnerDesigner
from src.chamber_design import ChamberDesigner
from src.radiation import RadiationCalculator
from src.pressure_losses import PressureLossCalculator

class TestCalculationWorkflow:
    """Test integration between calculation modules."""
    
    @pytest.fixture(scope="class")
    def integrated_calculators(self):
        """Create integrated calculator system."""
        combustion_calc = CombustionCalculator()
        burner_designer = BurnerDesigner(combustion_calc)
        chamber_designer = ChamberDesigner(combustion_calc, burner_designer)
        radiation_calc = RadiationCalculator(combustion_calc)
        pressure_calc = PressureLossCalculator(combustion_calc)
        
        return {
            'combustion': combustion_calc,
            'burner': burner_designer,
            'chamber': chamber_designer,
            'radiation': radiation_calc,
            'pressure': pressure_calc
        }
    
    def test_complete_calculation_workflow(self, integrated_calculators):
        """Test complete burner design workflow."""
        calcs = integrated_calculators
        
        # Input parameters
        fuel_type = 'natural_gas'
        required_power = 150000  # 150 kW
        supply_pressure = 4000   # 4000 Pa
        excess_air_ratio = 1.15
        residence_time = 0.6
        
        # Step 1: Combustion calculation
        fuel_flow = required_power / 50e6  # Approximate
        combustion_results = calcs['combustion'].calculate_combustion_products(
            fuel_type, fuel_flow, excess_air_ratio
        )
        
        # Step 2: Burner design
        burner_results = calcs['burner'].design_burner(
            fuel_type=fuel_type,
            required_power=required_power,
            supply_pressure=supply_pressure,
            excess_air_ratio=excess_air_ratio
        )
        
        # Step 3: Chamber design
        chamber_results = calcs['chamber'].design_chamber(
            fuel_type=fuel_type,
            required_power=required_power,
            target_residence_time=residence_time
        )
        
        # Step 4: Radiation calculation
        radiation_results = calcs['radiation'].calculate_flame_radiation(
            flame_temperature=combustion_results.adiabatic_flame_temperature,
            chamber_wall_temperature=chamber_results.wall_temperature,
            chamber_diameter=chamber_results.chamber_diameter,
            chamber_length=chamber_results.chamber_length,
            fuel_type=fuel_type,
            excess_air_ratio=excess_air_ratio
        )
        
        # Verify integration consistency
        assert combustion_results.fuel_flow_rate > 0
        assert burner_results.burner_diameter > 0
        assert chamber_results.chamber_volume > 0
        assert radiation_results.total_radiation_heat_transfer > 0
        
        # Verify physical relationships
        assert combustion_results.heat_release_rate == required_power
        assert chamber_results.residence_time >= residence_time * 0.9  # Within 10%
        assert radiation_results.flame_emissivity < 1.0
    
    def test_parameter_consistency(self, integrated_calculators):
        """Test parameter consistency across modules."""
        calcs = integrated_calculators
        
        fuel_type = 'natural_gas'
        fuel_flow = 0.003  # kg/s
        excess_air = 1.2
        
        # Get combustion results
        combustion = calcs['combustion'].calculate_combustion_products(
            fuel_type, fuel_flow, excess_air
        )
        
        # Design burner based on combustion heat release
        burner = calcs['burner'].design_burner(
            fuel_type=fuel_type,
            required_power=combustion.heat_release_rate,
            supply_pressure=3000
        )
        
        # Verify mass flow consistency
        total_mass_flow = combustion.fuel_flow_rate + combustion.air_flow_rate
        burner_volume_flow = total_mass_flow / 0.8  # Approximate density
        calculated_velocity = burner_volume_flow / burner.burner_area
        
        # Velocity should be close to designed velocity
        assert abs(calculated_velocity - burner.gas_velocity) / burner.gas_velocity < 0.1
    
    def test_error_propagation(self, integrated_calculators):
        """Test error handling across module boundaries."""
        calcs = integrated_calculators
        
        # Test that invalid inputs propagate correctly
        with pytest.raises(ValueError):
            # Invalid fuel should fail in combustion
            combustion = calcs['combustion'].calculate_combustion_products(
                'invalid_fuel', 0.01, 1.2
            )
            
            # This should not be reached, but if it is, burner design should also fail
            calcs['burner'].design_burner(
                fuel_type='invalid_fuel',
                required_power=100000,
                supply_pressure=3000
            )
```

### Data Flow Testing

#### Data Validation Integration
```python
# tests/integration/test_data_flow.py
import pytest
import json
from src.combustion import CombustionCalculator
from src.report import BurnerReportGenerator
from src.visualization import BurnerVisualization

class TestDataFlow:
    """Test data flow through the complete system."""
    
    def test_json_input_to_calculation(self, tmp_path):
        """Test loading JSON input and performing calculations."""
        # Create test input file
        input_data = {
            "fuel_type": "natural_gas",
            "required_power": 100000,
            "supply_pressure": 3000,
            "excess_air_ratio": 1.2,
            "target_residence_time": 0.5
        }
        
        input_file = tmp_path / "test_input.json"
        with open(input_file, 'w') as f:
            json.dump(input_data, f)
        
        # Load and process
        with open(input_file, 'r') as f:
            loaded_data = json.load(f)
        
        calculator = CombustionCalculator()
        
        # Verify data integrity
        assert loaded_data["fuel_type"] == input_data["fuel_type"]
        assert loaded_data["required_power"] == input_data["required_power"]
        
        # Perform calculation
        fuel_flow = loaded_data["required_power"] / 50e6
        results = calculator.calculate_combustion_products(
            loaded_data["fuel_type"],
            fuel_flow,
            loaded_data["excess_air_ratio"]
        )
        
        assert results.excess_air_ratio == loaded_data["excess_air_ratio"]
    
    def test_calculation_to_report_generation(self, tmp_path):
        """Test generating reports from calculation results."""
        # Perform calculations
        calculator = CombustionCalculator()
        combustion_results = calculator.calculate_combustion_products(
            'natural_gas', 0.002, 1.2
        )
        
        # Prepare results for reporting
        all_results = {
            'inputs': {
                'fuel_type': 'natural_gas',
                'power': 100000,
                'excess_air_ratio': 1.2
            },
            'combustion': combustion_results
        }
        
        # Generate report
        report_gen = BurnerReportGenerator(str(tmp_path))
        report_file = report_gen.generate_text_report(all_results, "test_project")
        
        # Verify report was created
        assert tmp_path.joinpath(report_file.split('/')[-1]).exists()
        
        # Verify report contains expected data
        with open(report_file, 'r') as f:
            report_content = f.read()
        
        assert 'natural_gas' in report_content
        assert '100000' in report_content or '100.0' in report_content  # Power in kW
        assert str(combustion_results.adiabatic_flame_temperature) in report_content
```

## GUI Testing

### User Interface Testing

#### GUI Component Tests
```python
# tests/gui/test_main_window.py
import pytest
import tkinter as tk
from unittest.mock import Mock, patch
from gui.gui import BurnerCalculatorGUI

class TestBurnerCalculatorGUI:
    """Test suite for GUI functionality."""
    
    @pytest.fixture
    def root_window(self):
        """Create root window for GUI testing."""
        root = tk.Tk()
        root.withdraw()  # Hide window during testing
        yield root
        root.destroy()
    
    @pytest.fixture
    def gui_app(self, root_window, tmp_path):
        """Create GUI application for testing."""
        return BurnerCalculatorGUI(root_window, output_dir=str(tmp_path))
    
    def test_gui_initialization(self, gui_app):
        """Test GUI initialization."""
        assert gui_app.master is not None
        assert gui_app.output_dir is not None
        assert hasattr(gui_app, 'notebook')
    
    def test_input_validation_positive_power(self, gui_app):
        """Test input validation for positive power values."""
        # Set invalid power value
        gui_app.power_var.set("-1000")
        
        # Trigger validation
        errors = gui_app.validate_inputs()
        
        assert len(errors) > 0
        assert any("power" in error.lower() for error in errors)
    
    def test_input_validation_fuel_type(self, gui_app):
        """Test input validation for fuel type selection."""
        # Set invalid fuel type
        gui_app.fuel_type_var.set("invalid_fuel")
        
        errors = gui_app.validate_inputs()
        
        assert len(errors) > 0
        assert any("fuel" in error.lower() for error in errors)
    
    @patch('gui.gui.CombustionCalculator')
    @patch('gui.gui.BurnerDesigner')
    def test_perform_calculations_success(self, mock_burner, mock_combustion, gui_app):
        """Test successful calculation execution."""
        # Setup mocks
        mock_combustion_calc = Mock()
        mock_combustion.return_value = mock_combustion_calc
        
        mock_burner_designer = Mock()
        mock_burner.return_value = mock_burner_designer
        
        # Set valid inputs
        gui_app.fuel_type_var.set("natural_gas")
        gui_app.power_var.set("100000")
        gui_app.pressure_var.set("3000")
        gui_app.excess_air_var.set("1.2")
        
        # Perform calculations
        gui_app.perform_calculations()
        
        # Verify calculators were called
        mock_combustion.assert_called_once()
        mock_burner.assert_called_once()
    
    def test_export_functionality(self, gui_app, tmp_path):
        """Test export functionality."""
        # Setup some dummy results
        gui_app.results = {
            'inputs': {'fuel_type': 'natural_gas', 'power': 100000},
            'combustion': Mock()
        }
        
        # Test export
        with patch('gui.gui.BurnerReportGenerator') as mock_report_gen:
            mock_generator = Mock()
            mock_report_gen.return_value = mock_generator
            mock_generator.generate_text_report.return_value = str(tmp_path / "test_report.txt")
            
            gui_app.export_results()
            
            mock_generator.generate_text_report.assert_called_once()
    
    def test_error_handling_display(self, gui_app):
        """Test error message display."""
        error_message = "Test error message"
        
        # This should not raise an exception
        gui_app.show_error_dialog(error_message)
        
        # In a real test, you might check if error dialog was shown
        # This is challenging with tkinter, so we just ensure no exceptions
    
    def test_load_save_input_file(self, gui_app, tmp_path):
        """Test loading and saving input files."""
        # Create test input file
        test_data = {
            "fuel_type": "natural_gas",
            "required_power": 150000,
            "supply_pressure": 4000
        }
        
        input_file = tmp_path / "test_input.json"
        with open(input_file, 'w') as f:
            json.dump(test_data, f)
        
        # Test loading
        with patch('tkinter.filedialog.askopenfilename', return_value=str(input_file)):
            gui_app.load_input_file()
        
        # Verify values were loaded
        assert gui_app.fuel_type_var.get() == "natural_gas"
        assert float(gui_app.power_var.get()) == 150000
        assert float(gui_app.pressure_var.get()) == 4000
```

### GUI Integration Tests

#### End-to-End GUI Workflows
```python
# tests/gui/test_gui_workflows.py
import pytest
import tkinter as tk
import json
from unittest.mock import patch, Mock
from gui.gui import BurnerCalculatorGUI

class TestGUIWorkflows:
    """Test complete GUI workflows."""
    
    @pytest.fixture
    def gui_setup(self, tmp_path):
        """Setup GUI for workflow testing."""
        root = tk.Tk()
        root.withdraw()
        gui = BurnerCalculatorGUI(root, output_dir=str(tmp_path))
        yield gui, tmp_path
        root.destroy()
    
    def test_complete_calculation_workflow(self, gui_setup):
        """Test complete calculation workflow through GUI."""
        gui, tmp_path = gui_setup
        
        # Setup valid inputs
        gui.fuel_type_var.set("natural_gas")
        gui.power_var.set("100000")
        gui.pressure_var.set("3000")
        gui.excess_air_var.set("1.2")
        gui.residence_time_var.set("0.5")
        
        # Mock the calculation classes
        with patch('gui.gui.CombustionCalculator') as mock_combustion, \
             patch('gui.gui.BurnerDesigner') as mock_burner, \
             patch('gui.gui.ChamberDesigner') as mock_chamber:
            
            # Setup return values
            mock_combustion_instance = Mock()
            mock_combustion.return_value = mock_combustion_instance
            
            mock_burner_instance = Mock()
            mock_burner.return_value = mock_burner_instance
            
            mock_chamber_instance = Mock()
            mock_chamber.return_value = mock_chamber_instance
            
            # Perform calculation
            gui.perform_calculations()
            
            # Verify all calculators were instantiated
            mock_combustion.assert_called_once()
            mock_burner.assert_called_once()
            mock_chamber.assert_called_once()
            
            # Verify results were stored
            assert gui.results is not None
    
    def test_input_validation_workflow(self, gui_setup):
        """Test input validation workflow."""
        gui, tmp_path = gui_setup
        
        # Set invalid inputs
        gui.fuel_type_var.set("")  # Empty fuel type
        gui.power_var.set("-1000")  # Negative power
        gui.pressure_var.set("0")  # Zero pressure
        
        # Trigger validation through calculation attempt
        with patch('gui.gui.messagebox.showerror') as mock_error:
            gui.perform_calculations()
            
            # Verify error message was shown
            mock_error.assert_called_once()
    
    def test_export_workflow(self, gui_setup):
        """Test complete export workflow."""
        gui, tmp_path = gui_setup
        
        # Setup results
        gui.results = {
            'inputs': {
                'fuel_type': 'natural_gas',
                'power': 100000
            },
            'combustion': Mock(),
            'burner': Mock(),
            'chamber': Mock()
        }
        
        # Test export workflow
        with patch('gui.gui.BurnerReportGenerator') as mock_report_gen, \
             patch('gui.gui.BurnerVisualization') as mock_viz, \
             patch('gui.gui.messagebox.showinfo') as mock_info:
            
            # Setup mocks
            mock_generator = Mock()
            mock_report_gen.return_value = mock_generator
            mock_generator.generate_comprehensive_report.return_value = {
                'txt': str(tmp_path / 'report.txt'),
                'csv': str(tmp_path / 'report.csv'),
                'xlsx': str(tmp_path / 'report.xlsx')
            }
            
            mock_visualization = Mock()
            mock_viz.return_value = mock_visualization
            
            # Perform export
            gui.export_results()
            
            # Verify export was performed
            mock_generator.generate_comprehensive_report.assert_called_once()
            mock_info.assert_called_once()  # Success message shown
```

## Performance Testing

### Calculation Performance Tests

#### Speed Benchmarks
```python
# tests/performance/test_calculation_speed.py
import pytest
import time
import statistics
from src.combustion import CombustionCalculator
from src.burner_design import BurnerDesigner
from src.chamber_design import ChamberDesigner

class TestCalculationPerformance:
    """Performance benchmarks for calculation modules."""
    
    @pytest.fixture(scope="class")
    def calculators(self):
        """Setup calculators for performance testing."""
        combustion_calc = CombustionCalculator()
        burner_designer = BurnerDesigner(combustion_calc)
        chamber_designer = ChamberDesigner(combustion_calc)
        
        return {
            'combustion': combustion_calc,
            'burner': burner_designer,
            'chamber': chamber_designer
        }
    
    def test_combustion_calculation_speed(self, calculators):
        """Benchmark combustion calculation speed."""
        calc = calculators['combustion']
        
        # Warm up
        for _ in range(10):
            calc.calculate_combustion_products('natural_gas', 0.01, 1.2)
        
        # Benchmark
        times = []
        for _ in range(100):
            start_time = time.perf_counter()
            calc.calculate_combustion_products('natural_gas', 0.01, 1.2)
            end_time = time.perf_counter()
            times.append(end_time - start_time)
        
        # Analyze results
        mean_time = statistics.mean(times)
        std_dev = statistics.stdev(times)
        
        print(f"Combustion calculation - Mean: {mean_time*1000:.2f}ms, StdDev: {std_dev*1000:.2f}ms")
        
        # Performance requirement: < 10ms per calculation
        assert mean_time < 0.01, f"Combustion calculation too slow: {mean_time*1000:.2f}ms"
    
    def test_burner_design_speed(self, calculators):
        """Benchmark burner design calculation speed."""
        designer = calculators['burner']
        
        # Warm up
        for _ in range(5):
            designer.design_burner('natural_gas', 100000, 3000)
        
        # Benchmark
        times = []
        for _ in range(50):
            start_time = time.perf_counter()
            designer.design_burner('natural_gas', 100000, 3000)
            end_time = time.perf_counter()
            times.append(end_time - start_time)
        
        mean_time = statistics.mean(times)
        
        print(f"Burner design - Mean: {mean_time*1000:.2f}ms")
        
        # Performance requirement: < 50ms per calculation
        assert mean_time < 0.05, f"Burner design too slow: {mean_time*1000:.2f}ms"
    
    def test_chamber_design_speed(self, calculators):
        """Benchmark chamber design calculation speed."""
        designer = calculators['chamber']
        
        # Warm up
        for _ in range(5):
            designer.design_chamber('natural_gas', 100000, 0.5)
        
        # Benchmark
        times = []
        for _ in range(50):
            start_time = time.perf_counter()
            designer.design_chamber('natural_gas', 100000, 0.5)
            end_time = time.perf_counter()
            times.append(end_time - start_time)
        
        mean_time = statistics.mean(times)
        
        print(f"Chamber design - Mean: {mean_time*1000:.2f}ms")
        
        # Performance requirement: < 50ms per calculation
        assert mean_time < 0.05, f"Chamber design too slow: {mean_time*1000:.2f}ms"
    
    @pytest.mark.slow
    def test_batch_calculation_performance(self, calculators):
        """Test performance with batch calculations."""
        calc = calculators['combustion']
        
        # Test parameters
        batch_size = 1000
        power_range = [50000, 100000, 150000, 200000, 250000]
        
        start_time = time.perf_counter()
        
        results = []
        for power in power_range:
            fuel_flow = power / 50e6
            for _ in range(batch_size // len(power_range)):
                result = calc.calculate_combustion_products('natural_gas', fuel_flow, 1.2)
                results.append(result)
        
        end_time = time.perf_counter()
        total_time = end_time - start_time
        
        calculations_per_second = batch_size / total_time
        
        print(f"Batch performance: {calculations_per_second:.0f} calculations/second")
        
        # Performance requirement: > 1000 calculations/second
        assert calculations_per_second > 1000, f"Batch performance too slow: {calculations_per_second:.0f} calc/s"
```

#### Memory Usage Tests
```python
# tests/performance/test_memory_usage.py
import pytest
import psutil
import os
from src.combustion import CombustionCalculator
from src.burner_design import BurnerDesigner

class TestMemoryUsage:
    """Test memory usage patterns."""
    
    def get_memory_usage(self):
        """Get current memory usage in MB."""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024
    
    def test_combustion_calculator_memory_usage(self):
        """Test memory usage of combustion calculator."""
        initial_memory = self.get_memory_usage()
        
        # Create multiple calculator instances
        calculators = []
        for i in range(100):
            calc = CombustionCalculator()
            calculators.append(calc)
        
        after_creation_memory = self.get_memory_usage()
        
        # Perform calculations
        for calc in calculators:
            for j in range(10):
                result = calc.calculate_combustion_products('natural_gas', 0.01, 1.2)
        
        after_calculations_memory = self.get_memory_usage()
        
        # Clean up
        del calculators
        
        final_memory = self.get_memory_usage()
        
        creation_memory_increase = after_creation_memory - initial_memory
        calculation_memory_increase = after_calculations_memory - after_creation_memory
        
        print(f"Memory usage - Initial: {initial_memory:.1f}MB")
        print(f"After creation: {after_creation_memory:.1f}MB (+{creation_memory_increase:.1f}MB)")
        print(f"After calculations: {after_calculations_memory:.1f}MB (+{calculation_memory_increase:.1f}MB)")
        print(f"Final: {final_memory:.1f}MB")
        
        # Memory requirements
        assert creation_memory_increase < 50, f"Too much memory for creation: {creation_memory_increase:.1f}MB"
        assert calculation_memory_increase < 20, f"Too much memory during calculations: {calculation_memory_increase:.1f}MB"
    
    @pytest.mark.slow
    def test_memory_leak_detection(self):
        """Test for memory leaks during repeated calculations."""
        calc = CombustionCalculator()
        
        # Baseline memory usage
        baseline_memory = self.get_memory_usage()
        
        # Perform many calculations
        for cycle in range(10):
            for i in range(1000):
                result = calc.calculate_combustion_products('natural_gas', 0.01, 1.2)
            
            current_memory = self.get_memory_usage()
            memory_increase = current_memory - baseline_memory
            
            print(f"Cycle {cycle + 1}: {current_memory:.1f}MB (+{memory_increase:.1f}MB)")
            
            # Memory should not continuously increase
            if cycle > 5:  # Allow for initial stabilization
                assert memory_increase < 10, f"Potential memory leak detected: {memory_increase:.1f}MB increase"
```

## Test Data Management

### Test Fixtures and Data

#### Shared Test Data
```python
# tests/fixtures/test_data.py
import json
import pytest
from pathlib import Path

# Test data directory
TEST_DATA_DIR = Path(__file__).parent

def load_test_fuel_data():
    """Load test fuel data."""
    with open(TEST_DATA_DIR / "test_fuels.json") as f:
        return json.load(f)

def load_sample_inputs():
    """Load sample input configurations."""
    with open(TEST_DATA_DIR / "sample_inputs.json") as f:
        return json.load(f)

def load_expected_results():
    """Load expected calculation results for validation."""
    with open(TEST_DATA_DIR / "expected_results.json") as f:
        return json.load(f)

# Test data constants
STANDARD_TEST_CONDITIONS = {
    "fuel_type": "natural_gas",
    "required_power": 100000,
    "supply_pressure": 3000,
    "excess_air_ratio": 1.2,
    "target_residence_time": 0.5,
    "ambient_temperature": 293.15
}

PERFORMANCE_TEST_PARAMETERS = [
    {"power": 50000, "fuel": "natural_gas"},
    {"power": 100000, "fuel": "natural_gas"},
    {"power": 200000, "fuel": "natural_gas"},
    {"power": 100000, "fuel": "propane"},
    {"power": 150000, "fuel": "methane"},
]

BOUNDARY_TEST_CONDITIONS = [
    {"power": 1000, "description": "minimum power"},
    {"power": 1000000, "description": "maximum power"},
    {"excess_air": 1.0, "description": "stoichiometric"},
    {"excess_air": 3.0, "description": "high excess air"},
    {"pressure": 100, "description": "low pressure"},
    {"pressure": 10000, "description": "high pressure"},
]
```

#### Test Configuration
```python
# tests/test_config.py
import os
from pathlib import Path

# Test configuration
TEST_CONFIG = {
    "test_data_dir": Path(__file__).parent / "fixtures",
    "temp_output_dir": "/tmp/burner_calc_tests",
    "performance_test_iterations": 100,
    "memory_test_threshold_mb": 50,
    "calculation_speed_threshold_ms": 10,
    "batch_performance_threshold_cps": 1000,  # calculations per second
}

# Test environment setup
def setup_test_environment():
    """Setup test environment."""
    os.makedirs(TEST_CONFIG["temp_output_dir"], exist_ok=True)

def cleanup_test_environment():
    """Cleanup test environment."""
    import shutil
    if os.path.exists(TEST_CONFIG["temp_output_dir"]):
        shutil.rmtree(TEST_CONFIG["temp_output_dir"])

# Test markers
SLOW_TESTS_MARKER = "slow"
INTEGRATION_TESTS_MARKER = "integration"
PERFORMANCE_TESTS_MARKER = "performance"
GUI_TESTS_MARKER = "gui"
```

## Continuous Testing

### Automated Test Execution

#### Test Commands
```bash
# Run all tests
make test

# Run specific test categories
pytest -m "not slow"                    # Exclude slow tests
pytest -m "integration"                 # Integration tests only
pytest -m "performance"                 # Performance tests only
pytest tests/unit/                      # Unit tests only

# Run with coverage
pytest --cov=src --cov-report=html

# Run with detailed output
pytest -v --tb=short

# Run specific test file
pytest tests/unit/test_combustion.py -v
```

#### CI/CD Integration
```yaml
# .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10"]
        
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
        
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
        
    - name: Run unit tests
      run: pytest tests/unit/ -v
      
    - name: Run integration tests
      run: pytest tests/integration/ -v
      
    - name: Run performance tests
      run: pytest tests/performance/ -m "not slow" -v
      
    - name: Check coverage
      run: pytest --cov=src --cov-report=xml --cov-fail-under=85
      
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
```

### Test Reporting

#### Coverage Reports
```bash
# Generate HTML coverage report
pytest --cov=src --cov-report=html
open htmlcov/index.html

# Generate XML coverage report
pytest --cov=src --cov-report=xml

# Show missing lines
pytest --cov=src --cov-report=term-missing
```

#### Performance Monitoring
```python
# tests/conftest.py
import pytest
import time
import json
from pathlib import Path

@pytest.fixture(autouse=True)
def performance_monitor(request):
    """Monitor test performance."""
    start_time = time.perf_counter()
    yield
    end_time = time.perf_counter()
    
    duration = end_time - start_time
    
    # Log slow tests
    if duration > 1.0:  # 1 second threshold
        test_name = request.node.name
        print(f"SLOW TEST: {test_name} took {duration:.2f} seconds")
        
        # Log to file
        log_file = Path("test_performance.log")
        with open(log_file, "a") as f:
            f.write(f"{test_name},{duration:.3f}\n")
```

---

*This comprehensive testing guide ensures high-quality, reliable software through systematic testing practices. All tests should be maintained and updated as the codebase evolves.*