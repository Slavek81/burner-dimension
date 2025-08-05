# tests/test_radiation.py

"""
tests/test_radiation.py

Unit tests for radiation heat transfer module.
Tests Stefan-Boltzmann law applications, view factors, and material properties.
"""

import math
import os
import sys
import unittest
from unittest.mock import Mock, patch

# Add src directory to path for imports  # noqa: E402
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from radiation import (  # noqa: E402
    RadiationCalculator,
    RadiationResults,
    SurfaceProperties
)
from combustion import CombustionCalculator  # noqa: E402


class TestRadiationCalculator(unittest.TestCase):
    """Test cases for RadiationCalculator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.calculator = RadiationCalculator()
        
        # Create mock combustion calculator
        self.mock_combustion = Mock(spec=CombustionCalculator)
        
        # Mock constants
        self.mock_constants = {
            "stefan_boltzmann_constant": 5.67e-8  # W/(m²·K⁴)
        }
        self.mock_combustion.constants = self.mock_constants
        
        # Sample parameters for testing
        self.flame_temperature = 2100.0  # K
        self.wall_temperature = 1200.0   # K  
        self.chamber_diameter = 0.5      # m
        self.chamber_length = 1.5        # m
        self.fuel_type = "natural_gas"

    def test_initialization_default(self):
        """Test default initialization."""
        calc = RadiationCalculator()
        self.assertIsInstance(calc.combustion_calc, CombustionCalculator)
        self.assertIsInstance(calc.material_data, dict)
        self.assertEqual(calc.stefan_boltzmann, 5.67e-8)

    def test_initialization_with_combustion_calculator(self):
        """Test initialization with custom combustion calculator."""
        calc = RadiationCalculator(combustion_calculator=self.mock_combustion)
        self.assertEqual(calc.combustion_calc, self.mock_combustion)

    def test_load_material_data_default(self):
        """Test loading of default material data when file is not available."""
        with patch('builtins.open', side_effect=FileNotFoundError):
            calc = RadiationCalculator()
            
            # Should have default material data
            self.assertIn("steel_oxidized", calc.material_data)
            self.assertIn("refractory_brick", calc.material_data)
            self.assertIn("flame_gases", calc.material_data)
            self.assertIn("soot_particles", calc.material_data)
            
            # Check default values
            self.assertEqual(calc.material_data["steel_oxidized"]["emissivity"], 0.79)
            self.assertEqual(calc.material_data["refractory_brick"]["emissivity"], 0.75)

    def test_calculate_flame_radiation_basic(self):
        """Test basic flame radiation calculation."""
        result = self.calculator.calculate_flame_radiation(
            flame_temperature=self.flame_temperature,
            chamber_wall_temperature=self.wall_temperature,
            chamber_diameter=self.chamber_diameter,
            chamber_length=self.chamber_length,
            fuel_type=self.fuel_type,
            excess_air_ratio=1.2,
            soot_concentration=0.0
        )
        
        # Check result type and basic properties
        self.assertIsInstance(result, RadiationResults)
        self.assertGreater(result.total_radiation_heat_transfer, 0)
        self.assertGreater(result.flame_to_wall_heat_transfer, 0)
        self.assertGreater(result.wall_to_ambient_heat_transfer, 0)
        self.assertGreater(result.flame_emissivity, 0)
        self.assertLess(result.flame_emissivity, 1.0)
        self.assertGreater(result.wall_emissivity, 0)
        self.assertLess(result.wall_emissivity, 1.0)
        self.assertEqual(result.flame_absorptivity, result.flame_emissivity)  # Gray body assumption
        self.assertGreater(result.view_factor_flame_wall, 0)
        self.assertLess(result.view_factor_flame_wall, 1.0)
        self.assertGreater(result.radiation_efficiency, 0)
        self.assertGreater(result.mean_beam_length, 0)

    def test_calculate_flame_radiation_with_soot(self):
        """Test flame radiation calculation with soot particles."""
        result_no_soot = self.calculator.calculate_flame_radiation(
            flame_temperature=self.flame_temperature,
            chamber_wall_temperature=self.wall_temperature,
            chamber_diameter=self.chamber_diameter,
            chamber_length=self.chamber_length,
            fuel_type=self.fuel_type,
            soot_concentration=0.0
        )
        
        result_with_soot = self.calculator.calculate_flame_radiation(
            flame_temperature=self.flame_temperature,
            chamber_wall_temperature=self.wall_temperature,
            chamber_diameter=self.chamber_diameter,
            chamber_length=self.chamber_length,
            fuel_type=self.fuel_type,
            soot_concentration=0.001  # kg/m³
        )
        
        # Soot should increase flame emissivity and heat transfer
        self.assertGreater(result_with_soot.flame_emissivity, result_no_soot.flame_emissivity)
        self.assertGreater(
            result_with_soot.flame_to_wall_heat_transfer, 
            result_no_soot.flame_to_wall_heat_transfer
        )

    def test_calculate_flame_radiation_different_fuels(self):
        """Test flame radiation with different fuel types."""
        fuels = ["natural_gas", "propane", "methane"]
        results = []
        
        for fuel in fuels:
            result = self.calculator.calculate_flame_radiation(
                flame_temperature=self.flame_temperature,
                chamber_wall_temperature=self.wall_temperature,
                chamber_diameter=self.chamber_diameter,
                chamber_length=self.chamber_length,
                fuel_type=fuel,
                excess_air_ratio=1.2,
                soot_concentration=0.0
            )
            results.append(result)
        
        # All should produce valid results
        for result in results:
            self.assertGreater(result.total_radiation_heat_transfer, 0)
            self.assertGreater(result.flame_emissivity, 0)

    def test_invalid_temperature_relationship(self):
        """Test validation of temperature relationship."""
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate_flame_radiation(
                flame_temperature=1000.0,  # Lower than wall temperature
                chamber_wall_temperature=1200.0,
                chamber_diameter=self.chamber_diameter,
                chamber_length=self.chamber_length,
                fuel_type=self.fuel_type
            )
        self.assertIn("vyšší než teplota stěny", str(context.exception))

    def test_invalid_chamber_dimensions(self):
        """Test validation of chamber dimensions."""
        # Zero diameter
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate_flame_radiation(
                flame_temperature=self.flame_temperature,
                chamber_wall_temperature=self.wall_temperature,
                chamber_diameter=0.0,
                chamber_length=self.chamber_length,
                fuel_type=self.fuel_type
            )
        self.assertIn("kladné", str(context.exception))
        
        # Negative length
        with self.assertRaises(ValueError):
            self.calculator.calculate_flame_radiation(
                flame_temperature=self.flame_temperature,
                chamber_wall_temperature=self.wall_temperature,
                chamber_diameter=self.chamber_diameter,
                chamber_length=-1.0,
                fuel_type=self.fuel_type
            )

    def test_calculate_mean_beam_length(self):
        """Test mean beam length calculation."""
        beam_length = self.calculator._calculate_mean_beam_length(
            diameter=self.chamber_diameter,
            length=self.chamber_length
        )
        
        self.assertGreater(beam_length, 0)
        
        # Should be reasonable relative to chamber dimensions
        self.assertLess(beam_length, max(self.chamber_diameter, self.chamber_length))
        
        # Test scaling with dimensions
        beam_length_large = self.calculator._calculate_mean_beam_length(
            diameter=self.chamber_diameter * 2,
            length=self.chamber_length * 2
        )
        self.assertGreater(beam_length_large, beam_length)

    def test_calculate_flame_emissivity(self):
        """Test flame emissivity calculation."""
        beam_length = 0.5  # m
        
        emissivity = self.calculator._calculate_flame_emissivity(
            temperature=self.flame_temperature,
            beam_length=beam_length,
            fuel_type="natural_gas",
            excess_air_ratio=1.2,
            soot_concentration=0.0
        )
        
        # Should be between 0 and 1
        self.assertGreater(emissivity, 0)
        self.assertLess(emissivity, 1.0)
        
        # Test different excess air ratios
        emissivity_lean = self.calculator._calculate_flame_emissivity(
            self.flame_temperature, beam_length, "natural_gas", 2.0, 0.0
        )
        
        # Leaner mixture should have lower emissivity
        self.assertLess(emissivity_lean, emissivity)

    def test_get_wall_emissivity(self):
        """Test wall emissivity retrieval."""
        # Test known material
        steel_emissivity = self.calculator._get_wall_emissivity("steel_oxidized")
        self.assertEqual(steel_emissivity, 0.79)
        
        # Test unknown material (should return default)
        unknown_emissivity = self.calculator._get_wall_emissivity("unknown_material")
        self.assertEqual(unknown_emissivity, 0.8)

    def test_calculate_view_factor_cylinder(self):
        """Test view factor calculation for cylindrical chamber."""
        # Test different aspect ratios
        view_factor_short = self.calculator._calculate_view_factor_cylinder(1.0, 0.3)  # L/D = 0.3
        view_factor_medium = self.calculator._calculate_view_factor_cylinder(1.0, 2.0)  # L/D = 2.0
        view_factor_long = self.calculator._calculate_view_factor_cylinder(1.0, 8.0)   # L/D = 8.0
        
        # All should be between 0 and 1
        for vf in [view_factor_short, view_factor_medium, view_factor_long]:
            self.assertGreater(vf, 0)
            self.assertLess(vf, 1.0)
        
        # Long cylinders should have higher view factors
        self.assertLess(view_factor_short, view_factor_medium)
        self.assertLess(view_factor_medium, view_factor_long)

    def test_calculate_flame_to_wall_radiation(self):
        """Test flame to wall radiation calculation."""
        flame_volume = math.pi * (self.chamber_diameter / 2) ** 2 * self.chamber_length
        wall_area = math.pi * self.chamber_diameter * self.chamber_length
        
        heat_transfer = self.calculator._calculate_flame_to_wall_radiation(
            flame_volume=flame_volume,
            wall_area=wall_area,
            flame_temperature=self.flame_temperature,
            wall_temperature=self.wall_temperature,
            flame_emissivity=0.3,
            wall_emissivity=0.8,
            view_factor=0.8
        )
        
        self.assertGreater(heat_transfer, 0)
        
        # Test temperature scaling (should scale with T⁴ difference)
        heat_transfer_high_temp = self.calculator._calculate_flame_to_wall_radiation(
            flame_volume, wall_area, self.flame_temperature + 200, self.wall_temperature,
            0.3, 0.8, 0.8
        )
        
        self.assertGreater(heat_transfer_high_temp, heat_transfer)

    def test_calculate_surface_radiation(self):
        """Test surface radiation calculation."""
        area = 1.0  # m²
        surface_temp = 1200.0  # K
        ambient_temp = 293.15  # K
        
        heat_transfer = self.calculator._calculate_surface_radiation(
            area=area,
            surface_temperature=surface_temp,
            ambient_temperature=ambient_temp,
            surface_emissivity=0.8,
            ambient_absorptivity=0.9
        )
        
        self.assertGreater(heat_transfer, 0)
        
        # Test temperature scaling
        heat_transfer_high = self.calculator._calculate_surface_radiation(
            area, surface_temp + 200, ambient_temp, 0.8, 0.9
        )
        
        self.assertGreater(heat_transfer_high, heat_transfer)
        
        # Test area scaling
        heat_transfer_double_area = self.calculator._calculate_surface_radiation(
            area * 2, surface_temp, ambient_temp, 0.8, 0.9
        )
        
        self.assertAlmostEqual(heat_transfer_double_area, heat_transfer * 2, places=1)

    def test_calculate_outer_surface_area(self):
        """Test outer surface area calculation."""
        inner_diameter = 0.5  # m
        length = 1.5         # m
        wall_thickness = 0.1 # m
        
        outer_area = self.calculator._calculate_outer_surface_area(
            inner_diameter, length, wall_thickness
        )
        
        self.assertGreater(outer_area, 0)
        
        # Should be larger than inner surface area
        inner_area = math.pi * inner_diameter * length + 2 * math.pi * (inner_diameter / 2) ** 2
        self.assertGreater(outer_area, inner_area)
        
        # Test thickness scaling
        outer_area_thick = self.calculator._calculate_outer_surface_area(
            inner_diameter, length, wall_thickness * 2
        )
        
        self.assertGreater(outer_area_thick, outer_area)

    def test_calculate_radiation_exchange_network(self):
        """Test radiation exchange network calculation."""
        # Create test surfaces
        surfaces = [
            SurfaceProperties(area=1.0, temperature=1500.0, emissivity=0.8, absorptivity=0.8),
            SurfaceProperties(area=2.0, temperature=1200.0, emissivity=0.7, absorptivity=0.7),
            SurfaceProperties(area=1.5, temperature=800.0, emissivity=0.9, absorptivity=0.9)
        ]
        
        # Create view factor matrix
        view_factors = [
            [0.0, 0.3, 0.2],
            [0.15, 0.0, 0.4],
            [0.1, 0.5, 0.0]
        ]
        
        heat_transfers = self.calculator.calculate_radiation_exchange_network(
            surfaces, view_factors
        )
        
        # Check that results are generated
        self.assertIsInstance(heat_transfers, dict)
        self.assertGreater(len(heat_transfers), 0)
        
        # Check specific heat transfer keys
        self.assertIn("surface_0_to_surface_1", heat_transfers)
        self.assertIn("surface_0_to_surface_2", heat_transfers)
        self.assertIn("surface_1_to_surface_2", heat_transfers)
        
        # All heat transfers should be finite numbers
        for key, value in heat_transfers.items():
            self.assertIsInstance(value, (int, float))
            self.assertFalse(math.isnan(value))
            self.assertFalse(math.isinf(value))

    def test_radiation_exchange_network_invalid_matrix(self):
        """Test radiation exchange network with invalid view factor matrix."""
        surfaces = [
            SurfaceProperties(area=1.0, temperature=1500.0, emissivity=0.8, absorptivity=0.8),
            SurfaceProperties(area=2.0, temperature=1200.0, emissivity=0.7, absorptivity=0.7)
        ]
        
        # Wrong size matrix
        view_factors = [
            [0.0, 0.3, 0.2],  # 3 elements instead of 2
            [0.15, 0.0]       # 2 elements
        ]
        
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate_radiation_exchange_network(surfaces, view_factors)
        self.assertIn("čtvercová", str(context.exception))

    def test_get_material_emissivity(self):
        """Test material emissivity retrieval."""
        # Test known material
        steel_emissivity = self.calculator.get_material_emissivity("steel_oxidized")
        self.assertEqual(steel_emissivity, 0.79)
        
        # Test with temperature
        steel_emissivity_temp = self.calculator.get_material_emissivity("steel_oxidized", 1200.0)
        self.assertEqual(steel_emissivity_temp, 0.79)
        
        # Test unknown material
        unknown_emissivity = self.calculator.get_material_emissivity("unknown_material")
        self.assertEqual(unknown_emissivity, 0.8)

    def test_surface_properties_dataclass(self):
        """Test SurfaceProperties dataclass functionality."""
        surface = SurfaceProperties(
            area=1.5,
            temperature=1200.0,
            emissivity=0.8,
            absorptivity=0.75
        )
        
        self.assertEqual(surface.area, 1.5)
        self.assertEqual(surface.temperature, 1200.0)
        self.assertEqual(surface.emissivity, 0.8)
        self.assertEqual(surface.absorptivity, 0.75)

    def test_radiation_results_dataclass(self):
        """Test RadiationResults dataclass functionality."""
        results = RadiationResults(
            total_radiation_heat_transfer=50000.0,
            flame_to_wall_heat_transfer=45000.0,
            wall_to_ambient_heat_transfer=5000.0,
            flame_emissivity=0.3,
            wall_emissivity=0.8,
            flame_absorptivity=0.3,
            view_factor_flame_wall=0.85,
            radiation_efficiency=75.0,
            mean_beam_length=0.6
        )
        
        # Test all attributes are accessible
        self.assertEqual(results.total_radiation_heat_transfer, 50000.0)
        self.assertEqual(results.flame_to_wall_heat_transfer, 45000.0)
        self.assertEqual(results.wall_to_ambient_heat_transfer, 5000.0)
        self.assertEqual(results.flame_emissivity, 0.3)
        self.assertEqual(results.wall_emissivity, 0.8)
        self.assertEqual(results.flame_absorptivity, 0.3)
        self.assertEqual(results.view_factor_flame_wall, 0.85)
        self.assertEqual(results.radiation_efficiency, 75.0)
        self.assertEqual(results.mean_beam_length, 0.6)

    def test_temperature_effects_on_radiation(self):
        """Test effects of temperature on radiation calculations."""
        base_result = self.calculator.calculate_flame_radiation(
            flame_temperature=2000.0,
            chamber_wall_temperature=1200.0,
            chamber_diameter=self.chamber_diameter,
            chamber_length=self.chamber_length,
            fuel_type=self.fuel_type
        )
        
        high_temp_result = self.calculator.calculate_flame_radiation(
            flame_temperature=2400.0,  # Higher flame temperature
            chamber_wall_temperature=1200.0,
            chamber_diameter=self.chamber_diameter,
            chamber_length=self.chamber_length,
            fuel_type=self.fuel_type
        )
        
        # Higher temperature should increase heat transfer
        self.assertGreater(
            high_temp_result.flame_to_wall_heat_transfer,
            base_result.flame_to_wall_heat_transfer
        )

    def test_chamber_size_effects_on_radiation(self):
        """Test effects of chamber size on radiation calculations."""
        small_result = self.calculator.calculate_flame_radiation(
            flame_temperature=self.flame_temperature,
            chamber_wall_temperature=self.wall_temperature,
            chamber_diameter=0.3,
            chamber_length=0.9,
            fuel_type=self.fuel_type
        )
        
        large_result = self.calculator.calculate_flame_radiation(
            flame_temperature=self.flame_temperature,
            chamber_wall_temperature=self.wall_temperature,
            chamber_diameter=0.8,
            chamber_length=2.4,
            fuel_type=self.fuel_type
        )
        
        # Larger chamber should generally have higher total heat transfer
        self.assertGreater(
            large_result.flame_to_wall_heat_transfer,
            small_result.flame_to_wall_heat_transfer
        )

    def test_excess_air_ratio_effects(self):
        """Test effects of excess air ratio on flame emissivity."""
        lean_result = self.calculator.calculate_flame_radiation(
            flame_temperature=self.flame_temperature,
            chamber_wall_temperature=self.wall_temperature,
            chamber_diameter=self.chamber_diameter,
            chamber_length=self.chamber_length,
            fuel_type=self.fuel_type,
            excess_air_ratio=2.0  # Very lean
        )
        
        rich_result = self.calculator.calculate_flame_radiation(
            flame_temperature=self.flame_temperature,
            chamber_wall_temperature=self.wall_temperature,
            chamber_diameter=self.chamber_diameter,
            chamber_length=self.chamber_length,
            fuel_type=self.fuel_type,
            excess_air_ratio=1.1  # Slightly lean
        )
        
        # Rich mixture should have higher emissivity due to higher product concentrations
        self.assertGreater(rich_result.flame_emissivity, lean_result.flame_emissivity)

    def test_constants_validation(self):
        """Test that physical constants are reasonable."""
        # Stefan-Boltzmann constant should be approximately 5.67e-8
        self.assertAlmostEqual(self.calculator.stefan_boltzmann, 5.67e-8, places=10)
        
        # Absorption coefficients should be positive
        self.assertGreater(self.calculator.CO2_ABSORPTION_COEFF, 0)
        self.assertGreater(self.calculator.H2O_ABSORPTION_COEFF, 0)
        self.assertGreater(self.calculator.SOOT_ABSORPTION_COEFF, 0)

    def test_edge_case_minimal_temperature_difference(self):
        """Test radiation calculation with minimal temperature difference."""
        result = self.calculator.calculate_flame_radiation(
            flame_temperature=1201.0,  # Just 1K above wall temperature
            chamber_wall_temperature=1200.0,
            chamber_diameter=self.chamber_diameter,
            chamber_length=self.chamber_length,
            fuel_type=self.fuel_type
        )
        
        # Should still produce valid results, but very low heat transfer
        self.assertGreater(result.flame_to_wall_heat_transfer, 0)
        self.assertLess(result.flame_to_wall_heat_transfer, 1000)  # Should be small

    def test_edge_case_very_high_temperatures(self):
        """Test radiation calculation with very high temperatures."""
        result = self.calculator.calculate_flame_radiation(
            flame_temperature=3000.0,  # Very high temperature
            chamber_wall_temperature=1800.0,
            chamber_diameter=self.chamber_diameter,
            chamber_length=self.chamber_length,
            fuel_type=self.fuel_type
        )
        
        # Should still produce valid results
        self.assertGreater(result.flame_to_wall_heat_transfer, 0)
        self.assertLess(result.flame_emissivity, 1.0)  # Should not exceed 1


if __name__ == "__main__":
    unittest.main()