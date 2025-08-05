# tests/test_burner_design.py

"""
tests/test_burner_design.py

Unit tests for burner design module.
Tests burner dimensioning, pressure calculations, and validation logic.
"""

import math
import os
import sys
import unittest
from unittest.mock import Mock, patch

# Add src directory to path for imports  # noqa: E402
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from burner_design import BurnerDesigner, BurnerDesignResults  # noqa: E402
from combustion import CombustionCalculator  # noqa: E402


class TestBurnerDesigner(unittest.TestCase):
    """Test cases for BurnerDesigner class."""

    def setUp(self):
        """Set up test fixtures."""
        self.designer = BurnerDesigner()
        self.mock_combustion = Mock(spec=CombustionCalculator)
        
        # Mock fuel properties for testing (more realistic values)
        self.mock_fuel_props = {
            "properties": {
                "lower_heating_value_mass": 50000000,  # J/kg
                "molecular_weight": 16.04,  # g/mol
                "density": 0.717  # kg/m³
            }
        }
        
        # Mock constants
        self.mock_constants = {
            "universal_gas_constant": 8.314  # J/(mol·K)
        }
        
        # Setup mock combustion calculator
        self.mock_combustion.get_fuel_properties.return_value = self.mock_fuel_props
        self.mock_combustion.constants = self.mock_constants
        
        # Mock combustion results
        mock_result = Mock()
        mock_result.fuel_flow_rate = 0.002
        mock_result.air_flow_rate = 0.034
        self.mock_combustion.calculate_combustion_products.return_value = mock_result

    def test_initialization_default(self):
        """Test default initialization."""
        designer = BurnerDesigner()
        self.assertIsInstance(designer.combustion_calc, CombustionCalculator)
        self.assertEqual(designer.safety_factor, 1.2)
        self.assertEqual(designer.MAX_GAS_VELOCITY, 100.0)
        self.assertEqual(designer.MIN_GAS_VELOCITY, 5.0)

    def test_initialization_with_parameters(self):
        """Test initialization with custom parameters."""
        mock_calc = Mock()
        designer = BurnerDesigner(combustion_calculator=mock_calc, safety_factor=1.5)
        self.assertEqual(designer.combustion_calc, mock_calc)
        self.assertEqual(designer.safety_factor, 1.5)

    def test_design_burner_basic(self):
        """Test basic burner design calculation."""
        designer = BurnerDesigner(combustion_calculator=self.mock_combustion)
        
        result = designer.design_burner(
            fuel_type="methane",
            required_power=20000,   # 20 kW to avoid heat density issues
            supply_pressure=8000,   # Higher pressure to avoid limits
            target_velocity=5.0,    # Very low velocity for larger area
            excess_air_ratio=1.2
        )
        
        # Check result type and basic properties
        self.assertIsInstance(result, BurnerDesignResults)
        self.assertGreater(result.burner_diameter, 0)
        self.assertGreater(result.burner_area, 0)
        self.assertEqual(result.gas_velocity, 5.0)
        self.assertGreater(result.burner_pressure_drop, 0)
        self.assertGreater(result.required_supply_pressure, 0)
        self.assertGreater(result.heat_release_density, 0)
        self.assertGreater(result.burner_length, 0)
        self.assertGreater(result.flame_length, 0)

    def test_design_burner_without_target_velocity(self):
        """Test burner design with automatic velocity calculation."""
        designer = BurnerDesigner(combustion_calculator=self.mock_combustion)
        
        result = designer.design_burner(
            fuel_type="methane",
            required_power=50000,
            supply_pressure=8000
        )
        
        # Velocity should be calculated automatically
        self.assertGreaterEqual(result.gas_velocity, designer.MIN_GAS_VELOCITY)
        self.assertLessEqual(result.gas_velocity, designer.MAX_GAS_VELOCITY)

    def test_design_burner_different_fuels(self):
        """Test burner design with different fuel types."""
        designer = BurnerDesigner(combustion_calculator=self.mock_combustion)
        
        fuels = ["methane", "natural_gas", "propane"]
        
        for fuel in fuels:
            with self.subTest(fuel=fuel):
                result = designer.design_burner(
                    fuel_type=fuel,
                    required_power=50000,
                    supply_pressure=8000,
                    target_velocity=8.0
                )
                self.assertIsInstance(result, BurnerDesignResults)
                self.assertGreater(result.burner_diameter, 0)

    def test_design_burner_power_scaling(self):
        """Test that burner dimensions scale properly with power."""
        designer = BurnerDesigner(combustion_calculator=self.mock_combustion)
        
        powers = [50000, 100000, 200000]  # 50, 100, 200 kW
        results = []
        
        for power in powers:
            result = designer.design_burner(
                fuel_type="methane",
                required_power=power,
                supply_pressure=10000,
                target_velocity=8.0
            )
            results.append(result)
        
        # Higher power should require larger burner area
        self.assertLess(results[0].burner_area, results[1].burner_area)
        self.assertLess(results[1].burner_area, results[2].burner_area)

    def test_invalid_power(self):
        """Test validation of invalid power values."""
        designer = BurnerDesigner(combustion_calculator=self.mock_combustion)
        
        # Zero power
        with self.assertRaises(ValueError) as context:
            designer.design_burner(
                fuel_type="methane",
                required_power=0,
                supply_pressure=8000
            )
        self.assertIn("větší než nula", str(context.exception))
        
        # Negative power
        with self.assertRaises(ValueError):
            designer.design_burner(
                fuel_type="methane",
                required_power=-1000,
                supply_pressure=8000
            )

    def test_invalid_pressure(self):
        """Test validation of invalid pressure values."""
        designer = BurnerDesigner(combustion_calculator=self.mock_combustion)
        
        # Zero pressure
        with self.assertRaises(ValueError) as context:
            designer.design_burner(
                fuel_type="methane",
                required_power=50000,
                supply_pressure=0
            )
        self.assertIn("větší než nula", str(context.exception))
        
        # Negative pressure
        with self.assertRaises(ValueError):
            designer.design_burner(
                fuel_type="methane",
                required_power=50000,
                supply_pressure=-1000
            )

    def test_insufficient_supply_pressure(self):
        """Test handling of insufficient supply pressure."""
        designer = BurnerDesigner(combustion_calculator=self.mock_combustion)
        
        with self.assertRaises(ValueError) as context:
            designer.design_burner(
                fuel_type="methane",
                required_power=50000,
                supply_pressure=100,  # Very low pressure
                target_velocity=25.0   # Moderate velocity
            )
        self.assertIn("Nedostatečný tlak", str(context.exception))

    def test_calculate_gas_density(self):
        """Test gas density calculation."""
        designer = BurnerDesigner(combustion_calculator=self.mock_combustion)
        
        density = designer._calculate_gas_density("methane", 3000, 293.15)
        
        # Check reasonable density value for methane at these conditions
        self.assertGreater(density, 0)
        self.assertLess(density, 10)  # Should be less than 10 kg/m³
        
        # Test pressure scaling
        density_high = designer._calculate_gas_density("methane", 6000, 293.15)
        self.assertGreater(density_high, density)

    def test_calculate_optimal_velocity(self):
        """Test optimal velocity calculation."""
        designer = BurnerDesigner()
        
        # Test different fuel types
        vel_methane = designer._calculate_optimal_velocity("methane", 100000)
        vel_propane = designer._calculate_optimal_velocity("propane", 100000)
        vel_natural_gas = designer._calculate_optimal_velocity("natural_gas", 100000)
        
        # All velocities should be within limits
        for vel in [vel_methane, vel_propane, vel_natural_gas]:
            self.assertGreaterEqual(vel, designer.MIN_GAS_VELOCITY)
            self.assertLessEqual(vel, designer.MAX_GAS_VELOCITY)
        
        # Test power scaling
        vel_low = designer._calculate_optimal_velocity("methane", 50000)
        vel_high = designer._calculate_optimal_velocity("methane", 200000)
        self.assertLessEqual(vel_low, vel_high)

    def test_calculate_burner_pressure_drop(self):
        """Test burner pressure drop calculation."""
        designer = BurnerDesigner()
        
        pressure_drop = designer._calculate_burner_pressure_drop(
            gas_density=1.0,
            velocity=20.0,
            diameter=0.1
        )
        
        self.assertGreater(pressure_drop, 0)
        
        # Test velocity scaling (pressure drop ~ velocity²)
        pressure_drop_high = designer._calculate_burner_pressure_drop(
            gas_density=1.0,
            velocity=40.0,
            diameter=0.1
        )
        
        # Should be approximately 4 times higher (2²)
        self.assertAlmostEqual(pressure_drop_high / pressure_drop, 4.0, places=1)

    def test_calculate_flame_length(self):
        """Test flame length calculation."""
        designer = BurnerDesigner(combustion_calculator=self.mock_combustion)
        
        flame_length = designer._calculate_flame_length(
            burner_diameter=0.1,
            gas_velocity=20.0,
            fuel_type="methane"
        )
        
        self.assertGreater(flame_length, 0)
        
        # Flame length should be reasonable relative to burner diameter
        min_expected = 0.1 * 5   # 5 * diameter
        max_expected = 0.1 * 50  # 50 * diameter
        self.assertGreaterEqual(flame_length, min_expected)
        self.assertLessEqual(flame_length, max_expected)

    def test_velocity_limits_enforcement(self):
        """Test that velocity limits are properly enforced."""
        designer = BurnerDesigner(combustion_calculator=self.mock_combustion)
        
        # Test very high target velocity gets clamped
        result_high = designer.design_burner(
            fuel_type="methane",
            required_power=50000,
            supply_pressure=10000,  # High pressure to avoid pressure limit
            target_velocity=120.0   # Above maximum
        )
        self.assertEqual(result_high.gas_velocity, designer.MAX_GAS_VELOCITY)
        
        # Test very low target velocity gets clamped
        result_low = designer.design_burner(
            fuel_type="methane",
            required_power=50000,
            supply_pressure=8000,
            target_velocity=2.0     # Below minimum
        )
        self.assertEqual(result_low.gas_velocity, designer.MIN_GAS_VELOCITY)

    def test_validate_design(self):
        """Test design validation."""
        designer = BurnerDesigner()
        
        # Create valid design results
        valid_results = BurnerDesignResults(
            burner_diameter=0.1,
            burner_area=0.008,
            gas_velocity=20.0,
            burner_pressure_drop=500,
            required_supply_pressure=600,
            heat_release_density=2e6,
            burner_length=0.3,
            flame_length=1.0
        )
        
        validation = designer.validate_design(valid_results)
        
        # Check validation structure
        self.assertIn("velocity_in_range", validation)
        self.assertIn("heat_density_acceptable", validation)
        self.assertIn("reasonable_dimensions", validation)
        self.assertIn("pressure_drop_reasonable", validation)
        
        # All should pass for valid design
        for criterion, passed in validation.items():
            self.assertTrue(passed, f"Validation failed for {criterion}")

    def test_validate_design_failures(self):
        """Test validation with invalid design parameters."""
        designer = BurnerDesigner()
        
        # Create invalid design results
        invalid_results = BurnerDesignResults(
            burner_diameter=2.0,    # Too large
            burner_area=0.008,
            gas_velocity=200.0,     # Too high
            burner_pressure_drop=2500,
            required_supply_pressure=3000,
            heat_release_density=8e6,  # Too high
            burner_length=0.3,
            flame_length=1.0
        )
        
        validation = designer.validate_design(invalid_results)
        
        # These should fail
        self.assertFalse(validation["velocity_in_range"])
        self.assertFalse(validation["heat_density_acceptable"])
        self.assertFalse(validation["reasonable_dimensions"])

    def test_get_design_recommendations(self):
        """Test design recommendations generation."""
        designer = BurnerDesigner()
        
        # Create design with issues
        problematic_results = BurnerDesignResults(
            burner_diameter=0.1,
            burner_area=0.008,
            gas_velocity=2.0,       # Too low
            burner_pressure_drop=500,
            required_supply_pressure=600,
            heat_release_density=8e6,  # Too high
            burner_length=0.3,
            flame_length=5.0        # Very long flame
        )
        
        recommendations = designer.get_design_recommendations(problematic_results)
        
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
        
        # Check that recommendations contain expected content
        rec_text = " ".join(recommendations)
        self.assertIn("rychlost", rec_text.lower())

    def test_high_heat_density_handling(self):
        """Test handling of excessive heat density."""
        # Mock very high power requirement
        mock_combustion = Mock(spec=CombustionCalculator)
        mock_fuel_props = {
            "properties": {
                "lower_heating_value_mass": 50000000,
                "molecular_weight": 16.04,
                "density": 0.717
            }
        }
        mock_combustion.get_fuel_properties.return_value = mock_fuel_props
        mock_combustion.constants = {"universal_gas_constant": 8.314}
        
        mock_result = Mock()
        mock_result.fuel_flow_rate = 0.02  # High flow rate
        mock_combustion.calculate_combustion_products.return_value = mock_result
        
        designer = BurnerDesigner(combustion_calculator=mock_combustion)
        
        with self.assertRaises(ValueError) as context:
            designer.design_burner(
                fuel_type="methane",
                required_power=10000000,  # 10 MW - very high
                supply_pressure=8000,
                target_velocity=8.0
            )
        self.assertIn("hustota tepelného toku", str(context.exception))

    def test_burner_design_results_dataclass(self):
        """Test BurnerDesignResults dataclass functionality."""
        results = BurnerDesignResults(
            burner_diameter=0.1,
            burner_area=0.008,
            gas_velocity=20.0,
            burner_pressure_drop=500,
            required_supply_pressure=600,
            heat_release_density=2e6,
            burner_length=0.3,
            flame_length=1.0
        )
        
        # Test all attributes are accessible
        self.assertEqual(results.burner_diameter, 0.1)
        self.assertEqual(results.burner_area, 0.008)
        self.assertEqual(results.gas_velocity, 20.0)
        self.assertEqual(results.burner_pressure_drop, 500)
        self.assertEqual(results.required_supply_pressure, 600)
        self.assertEqual(results.heat_release_density, 2e6)
        self.assertEqual(results.burner_length, 0.3)
        self.assertEqual(results.flame_length, 1.0)

    def test_edge_case_small_burner(self):
        """Test design of very small burner."""
        designer = BurnerDesigner(combustion_calculator=self.mock_combustion)
        
        result = designer.design_burner(
            fuel_type="methane",
            required_power=10000,    # 10 kW - small but reasonable
            supply_pressure=8000,
            target_velocity=10.0
        )
        
        # Should still produce valid results
        self.assertGreater(result.burner_diameter, 0)
        self.assertGreater(result.burner_area, 0)

    def test_edge_case_large_burner(self):
        """Test design of large burner within limits."""
        designer = BurnerDesigner(combustion_calculator=self.mock_combustion)
        
        result = designer.design_burner(
            fuel_type="methane",
            required_power=500000,  # 500 kW - large but reasonable
            supply_pressure=5000,   # Higher pressure
            target_velocity=15.0    # Lower velocity for larger area
        )
        
        # Should produce valid results
        self.assertGreater(result.burner_diameter, 0)
        self.assertLess(result.heat_release_density, designer.MAX_HEAT_DENSITY)

    def test_constants_validation(self):
        """Test that design constants are reasonable."""
        designer = BurnerDesigner()
        
        # Check design constants are reasonable
        self.assertGreater(designer.MAX_GAS_VELOCITY, designer.MIN_GAS_VELOCITY)
        self.assertGreater(designer.MAX_HEAT_DENSITY, 1e6)  # At least 1 MW/m²
        self.assertGreater(designer.BURNER_PRESSURE_DROP_COEFF, 0)
        self.assertLess(designer.BURNER_PRESSURE_DROP_COEFF, 2.0)


if __name__ == "__main__":
    unittest.main()