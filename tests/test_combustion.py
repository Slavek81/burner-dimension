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
        self.calculator = CombustionCalculator()

    def test_methane_stoichiometry(self):
        """Test stoichiometric calculations for methane."""
        result = self.calculator.calculate_stoichiometry("methane")

        # Check basic properties
        self.assertIsInstance(result, dict)
        self.assertIn("air_fuel_ratio_mass", result)
        self.assertIn("products_per_fuel_mass", result)

        # Verify methane stoichiometry: CH4 + 2O2 -> CO2 + 2H2O
        # Theoretical air/fuel ratio for methane ≈ 17.2 kg air/kg fuel
        self.assertAlmostEqual(result["air_fuel_ratio_mass"], 17.23, places=1)

    def test_propane_stoichiometry(self):
        """Test stoichiometric calculations for propane."""
        result = self.calculator.calculate_stoichiometry("propane")

        # Check basic properties
        self.assertIsInstance(result, dict)
        self.assertIn("air_fuel_ratio_mass", result)

        # Theoretical air/fuel ratio for propane ≈ 15.6 kg air/kg fuel
        self.assertAlmostEqual(result["air_fuel_ratio_mass"], 15.64, places=1)

    def test_natural_gas_stoichiometry(self):
        """Test stoichiometric calculations for natural gas."""
        result = self.calculator.calculate_stoichiometry("natural_gas")

        # Check basic properties
        self.assertIsInstance(result, dict)
        self.assertIn("air_fuel_ratio_mass", result)

        # Natural gas is mostly methane, so similar ratio
        self.assertAlmostEqual(result["air_fuel_ratio_mass"], 16.5, delta=1.0)

    def test_combustion_products(self):
        """Test combustion products calculation."""
        result = self.calculator.calculate_combustion_products(
            fuel_type="methane", fuel_flow_rate=0.1, excess_air_ratio=1.1
        )

        # Check result structure
        self.assertIsInstance(result, object)
        self.assertTrue(hasattr(result, "fuel_flow_rate"))
        self.assertTrue(hasattr(result, "air_flow_rate"))
        self.assertTrue(hasattr(result, "products_flow_rate"))

        # Check values
        self.assertEqual(result.fuel_flow_rate, 0.1)
        self.assertGreater(result.air_flow_rate, 0)
        self.assertGreater(result.products_flow_rate, 0)

    def test_temperature_calculation(self):
        """Test adiabatic flame temperature calculation."""
        temperature = self.calculator.calculate_adiabatic_temperature(
            "methane", excess_air_ratio=1.0
        )

        # Methane adiabatic flame temperature should be ~2220K (1950°C)
        self.assertGreater(temperature, 2000)  # K
        self.assertLess(temperature, 2500)  # K

    def test_invalid_fuel_type(self):
        """Test handling of invalid fuel type."""
        with self.assertRaises(ValueError):
            self.calculator.calculate_stoichiometry("invalid_fuel")

    def test_excess_air_validation(self):
        """Test validation of excess air ratio."""
        # Test minimum excess air ratio
        with self.assertRaises(ValueError):
            self.calculator.calculate_combustion_products(
                "methane", 0.1, excess_air_ratio=0.8
            )

        # Test maximum excess air ratio
        with self.assertRaises(ValueError):
            self.calculator.calculate_combustion_products(
                "methane", 0.1, excess_air_ratio=5.0
            )

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


if __name__ == "__main__":
    unittest.main()
