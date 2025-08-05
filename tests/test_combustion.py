# tests/test_combustion.py

"""
tests/test_combustion.py

Unit tests for combustion calculation module.
Tests stoichiometric calculations, air requirements, and combustion products.
"""

import os
import sys
import unittest

# Add src directory to path for imports  # noqa: E402
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from combustion import CombustionCalculator  # noqa: E402


class TestCombustionCalculator(unittest.TestCase):
    """Test cases for CombustionCalculator class."""

    def setUp(self):
        """Set up test fixtures."""
        # Use correct path to data directory
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "fuels.json")
        self.calculator = CombustionCalculator(fuel_data_path=data_path)

    def test_methane_stoichiometric_air(self):
        """Test stoichiometric air calculation for methane."""
        fuel_flow_rate = 0.01  # kg/s
        air_required = self.calculator.calculate_stoichiometric_air(
            "methane", fuel_flow_rate
        )

        # Check basic properties
        self.assertIsInstance(air_required, float)
        self.assertGreater(air_required, 0)

        # Verify methane stoichiometry: CH4 + 2O2 -> CO2 + 2H2O
        # Theoretical air/fuel ratio for methane ≈ 17.2 kg air/kg fuel
        expected_air = fuel_flow_rate * 17.23
        self.assertAlmostEqual(air_required, expected_air, places=3)

    def test_propane_stoichiometric_air(self):
        """Test stoichiometric air calculation for propane."""
        fuel_flow_rate = 0.01  # kg/s
        air_required = self.calculator.calculate_stoichiometric_air(
            "propane", fuel_flow_rate
        )

        # Check basic properties
        self.assertIsInstance(air_required, float)
        self.assertGreater(air_required, 0)

        # Theoretical air/fuel ratio for propane ≈ 15.6 kg air/kg fuel
        expected_air = fuel_flow_rate * 15.5  # Use actual value from fuel data
        self.assertAlmostEqual(air_required, expected_air, places=2)

    def test_natural_gas_stoichiometric_air(self):
        """Test stoichiometric air calculation for natural gas."""
        fuel_flow_rate = 0.01  # kg/s
        air_required = self.calculator.calculate_stoichiometric_air(
            "natural_gas", fuel_flow_rate
        )

        # Check basic properties
        self.assertIsInstance(air_required, float)
        self.assertGreater(air_required, 0)

        # Natural gas is mostly methane, so similar ratio
        # Expected air/fuel ratio around 16.5
        expected_air = fuel_flow_rate * 16.5
        self.assertAlmostEqual(air_required, expected_air, delta=fuel_flow_rate)

    def test_combustion_products(self):
        """Test combustion products calculation."""
        result = self.calculator.calculate_combustion_products(
            fuel_type="methane", fuel_flow_rate=0.1, excess_air_ratio=1.1
        )

        # Check result structure
        self.assertIsInstance(result, object)
        self.assertTrue(hasattr(result, "fuel_flow_rate"))
        self.assertTrue(hasattr(result, "air_flow_rate"))
        self.assertTrue(hasattr(result, "flue_gas_flow_rate"))  # Correct attribute name
        self.assertTrue(hasattr(result, "adiabatic_flame_temperature"))
        self.assertTrue(hasattr(result, "heat_release_rate"))
        self.assertTrue(hasattr(result, "co2_volume_percent"))
        self.assertTrue(hasattr(result, "o2_volume_percent"))

        # Check values
        self.assertEqual(result.fuel_flow_rate, 0.1)
        self.assertGreater(result.air_flow_rate, 0)
        self.assertGreater(result.flue_gas_flow_rate, 0)  # Correct attribute name
        self.assertGreater(result.adiabatic_flame_temperature, 2000)
        self.assertGreater(result.heat_release_rate, 0)
        self.assertGreater(result.co2_volume_percent, 0)
        self.assertGreater(result.o2_volume_percent, 0)

    def test_temperature_calculation(self):
        """Test adiabatic flame temperature calculation."""
        temperature = self.calculator._calculate_adiabatic_temperature(
            "methane", excess_air_ratio=1.0
        )

        # Methane adiabatic flame temperature should be ~2220K (1950°C)
        self.assertGreater(temperature, 2000)  # K
        self.assertLess(temperature, 2500)  # K

    def test_invalid_fuel_type(self):
        """Test handling of invalid fuel type."""
        with self.assertRaises(ValueError):
            self.calculator.calculate_stoichiometric_air("invalid_fuel", 0.01)

    def test_excess_air_validation(self):
        """Test validation of excess air ratio."""
        # Test minimum excess air ratio
        with self.assertRaises(ValueError):
            self.calculator.calculate_combustion_products(
                "methane", 0.1, excess_air_ratio=0.8
            )

        # Test valid excess air ratio should work
        result = self.calculator.calculate_combustion_products(
            "methane", 0.1, excess_air_ratio=2.0
        )
        self.assertIsNotNone(result)
        self.assertEqual(result.excess_air_ratio, 2.0)

    def test_fuel_flow_rate_validation(self):
        """Test validation of fuel flow rate."""
        # Test negative flow rate
        with self.assertRaises(ValueError):
            self.calculator.calculate_combustion_products(
                "methane", -0.1, excess_air_ratio=1.1
            )

        # Test zero flow rate
        with self.assertRaises(ValueError):
            self.calculator.calculate_combustion_products(
                "methane", 0.0, excess_air_ratio=1.1
            )

    def test_get_fuel_properties(self):
        """Test getting fuel properties."""
        props = self.calculator.get_fuel_properties("methane")
        self.assertIsInstance(props, dict)
        self.assertIn("name", props)
        self.assertIn("properties", props)

    def test_get_available_fuels(self):
        """Test getting available fuel types."""
        fuels = self.calculator.get_available_fuels()
        self.assertIsInstance(fuels, list)
        self.assertIn("methane", fuels)
        self.assertIn("natural_gas", fuels)
        self.assertIn("propane", fuels)

    def test_flue_gas_composition(self):
        """Test flue gas composition calculation."""
        result = self.calculator.calculate_combustion_products(
            fuel_type="natural_gas", fuel_flow_rate=0.01, excess_air_ratio=1.2
        )

        # CO2 should be reasonable percentage
        self.assertGreater(result.co2_volume_percent, 8)
        self.assertLess(result.co2_volume_percent, 15)

        # O2 should be present due to excess air
        self.assertGreater(result.o2_volume_percent, 0)
        self.assertLess(result.o2_volume_percent, 5)


if __name__ == "__main__":
    unittest.main()
