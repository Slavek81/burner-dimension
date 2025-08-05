# tests/test_chamber_design.py

"""
tests/test_chamber_design.py

Unit tests for chamber design module.
Tests chamber dimensioning, heat transfer calculations, and validation logic.
"""

import math
import os
import sys
import unittest
from unittest.mock import Mock

# Add src directory to path for imports  # noqa: E402
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from chamber_design import ChamberDesigner, ChamberDesignResults  # noqa: E402
from combustion import CombustionCalculator, CombustionResults  # noqa: E402
from burner_design import BurnerDesigner  # noqa: E402


class TestChamberDesigner(unittest.TestCase):
    """Test cases for ChamberDesigner class."""

    def setUp(self):
        """Set up test fixtures."""
        # Use correct path to data directory
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "fuels.json")
        self.designer = ChamberDesigner(fuel_data_path=data_path)

        # Create mock objects
        self.mock_combustion = Mock(spec=CombustionCalculator)
        self.mock_burner = Mock(spec=BurnerDesigner)

        # Mock fuel properties
        self.mock_fuel_props = {
            "properties": {
                "lower_heating_value_mass": 50000000,  # J/kg
                "molecular_weight": 16.04,  # g/mol
                "density": 0.717  # kg/m³
            }
        }

        # Mock constants
        self.mock_constants = {
            "universal_gas_constant": 8.314,  # J/(mol·K)
            "standard_pressure": 101325,      # Pa
            "air_molecular_weight": 28.97     # g/mol
        }

        # Mock combustion results
        self.mock_combustion_result = CombustionResults(
            fuel_flow_rate=0.002,
            air_flow_rate=0.034,
            flue_gas_flow_rate=0.036,
            excess_air_ratio=1.2,
            adiabatic_flame_temperature=2100.0,
            heat_release_rate=100000,
            co2_volume_percent=10.0,
            o2_volume_percent=2.0
        )

        # Setup mock returns
        self.mock_combustion.get_fuel_properties.return_value = self.mock_fuel_props
        self.mock_combustion.constants = self.mock_constants
        self.mock_combustion.calculate_combustion_products.return_value = (
            self.mock_combustion_result
        )

    def test_initialization_default(self):
        """Test default initialization."""
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "fuels.json")
        designer = ChamberDesigner(fuel_data_path=data_path)
        self.assertIsInstance(designer.combustion_calc, CombustionCalculator)
        self.assertIsInstance(designer.burner_designer, BurnerDesigner)
        self.assertEqual(designer.safety_factor, 1.5)

    def test_initialization_with_parameters(self):
        """Test initialization with custom parameters."""
        designer = ChamberDesigner(
            combustion_calculator=self.mock_combustion,
            burner_designer=self.mock_burner,
            safety_factor=2.0
        )
        self.assertEqual(designer.combustion_calc, self.mock_combustion)
        self.assertEqual(designer.burner_designer, self.mock_burner)
        self.assertEqual(designer.safety_factor, 2.0)

    def test_design_chamber_basic(self):
        """Test basic chamber design calculation."""
        designer = ChamberDesigner(combustion_calculator=self.mock_combustion)

        result = designer.design_chamber(
            fuel_type="methane",
            required_power=100000,  # 100 kW
            target_residence_time=0.5,
            wall_insulation_thickness=0.1,
            ambient_temperature=293.15,
            target_efficiency=0.85
        )

        # Check result type and basic properties
        self.assertIsInstance(result, ChamberDesignResults)
        self.assertGreater(result.chamber_volume, 0)
        self.assertGreater(result.chamber_diameter, 0)
        self.assertGreater(result.chamber_length, 0)
        self.assertGreater(result.chamber_area, 0)
        self.assertGreater(result.residence_time, 0)
        self.assertGreater(result.heat_transfer_coefficient, 0)
        self.assertGreater(result.wall_temperature, 293.15)  # Should be above ambient
        self.assertGreater(result.heat_loss_rate, 0)
        self.assertGreater(result.thermal_efficiency, 0)
        self.assertGreater(result.volume_heat_release_rate, 0)

    def test_design_chamber_different_parameters(self):
        """Test chamber design with different parameter values."""
        designer = ChamberDesigner(combustion_calculator=self.mock_combustion)

        # Test different residence times
        residence_times = [0.2, 0.5, 1.0]
        results = []

        for rt in residence_times:
            result = designer.design_chamber(
                fuel_type="methane",
                required_power=100000,
                target_residence_time=rt
            )
            results.append(result)

        # Longer residence time should require larger chamber
        self.assertLess(results[0].chamber_volume, results[1].chamber_volume)
        self.assertLess(results[1].chamber_volume, results[2].chamber_volume)

    def test_design_chamber_power_scaling(self):
        """Test that chamber dimensions scale properly with power."""
        designer = ChamberDesigner(combustion_calculator=self.mock_combustion)

        powers = [50000, 100000, 200000]  # 50, 100, 200 kW
        results = []

        for power in powers:
            # Adjust fuel flow rate in mock for different powers
            fuel_flow = power / 50000000  # Consistent with mock heating value
            self.mock_combustion_result.fuel_flow_rate = fuel_flow
            self.mock_combustion_result.flue_gas_flow_rate = fuel_flow * 18  # Approximate

            result = designer.design_chamber(
                fuel_type="methane",
                required_power=power,
                target_residence_time=0.5
            )
            results.append(result)

        # Higher power should require larger chamber volume
        self.assertLess(results[0].chamber_volume, results[1].chamber_volume)
        self.assertLess(results[1].chamber_volume, results[2].chamber_volume)

    def test_invalid_power(self):
        """Test validation of invalid power values."""
        designer = ChamberDesigner(combustion_calculator=self.mock_combustion)

        # Zero power
        with self.assertRaises(ValueError) as context:
            designer.design_chamber(
                fuel_type="methane",
                required_power=0,
                target_residence_time=0.5
            )
        self.assertIn("větší než nula", str(context.exception))

        # Negative power
        with self.assertRaises(ValueError):
            designer.design_chamber(
                fuel_type="methane",
                required_power=-1000,
                target_residence_time=0.5
            )

    def test_invalid_residence_time(self):
        """Test validation of invalid residence time values."""
        designer = ChamberDesigner(combustion_calculator=self.mock_combustion)

        # Too short residence time
        with self.assertRaises(ValueError) as context:
            designer.design_chamber(
                fuel_type="methane",
                required_power=100000,
                target_residence_time=0.05  # Below minimum
            )
        self.assertIn("příliš krátká", str(context.exception))

        # Too long residence time
        with self.assertRaises(ValueError) as context:
            designer.design_chamber(
                fuel_type="methane",
                required_power=100000,
                target_residence_time=15.0  # Above maximum
            )
        self.assertIn("příliš dlouhá", str(context.exception))

    def test_calculate_flue_gas_volume_flow(self):
        """Test flue gas volume flow calculation."""
        designer = ChamberDesigner(combustion_calculator=self.mock_combustion)

        volume_flow = designer._calculate_flue_gas_volume_flow(
            self.mock_combustion_result,
            2100.0  # Temperature in K
        )

        self.assertGreater(volume_flow, 0)

        # Test temperature scaling (higher temperature -> higher volume flow)
        volume_flow_high = designer._calculate_flue_gas_volume_flow(
            self.mock_combustion_result,
            2500.0  # Higher temperature
        )

        self.assertGreater(volume_flow_high, volume_flow)

    def test_calculate_chamber_dimensions(self):
        """Test chamber dimension calculations."""
        designer = ChamberDesigner()

        volume = 1.0  # m³
        diameter, length, area = designer._calculate_chamber_dimensions(volume)

        # Check basic properties
        self.assertGreater(diameter, 0)
        self.assertGreater(length, 0)
        self.assertGreater(area, 0)

        # Check dimensional relationships
        self.assertAlmostEqual(area, math.pi * diameter**2 / 4, places=6)
        self.assertAlmostEqual(length, diameter * designer.TYPICAL_LD_RATIO, places=6)

        # Check volume consistency
        calculated_volume = area * length
        self.assertAlmostEqual(calculated_volume, volume, places=6)

    def test_calculate_chamber_dimensions_limits(self):
        """Test chamber dimension limits."""
        designer = ChamberDesigner()

        # Very small volume
        diameter_small, _, _ = designer._calculate_chamber_dimensions(0.001)
        self.assertGreaterEqual(diameter_small, designer.MIN_CHAMBER_DIAMETER)

        # Very large volume
        diameter_large, _, _ = designer._calculate_chamber_dimensions(100.0)
        self.assertLessEqual(diameter_large, designer.MAX_CHAMBER_DIAMETER)

    def test_calculate_heat_transfer_coefficient(self):
        """Test heat transfer coefficient calculation."""
        designer = ChamberDesigner()

        h = designer._calculate_heat_transfer_coefficient(
            gas_temperature=2100.0,
            chamber_diameter=0.5,
            mass_flow_rate=0.05
        )

        self.assertGreater(h, 0)
        self.assertLess(h, 1000)  # Reasonable range for gas-to-wall heat transfer

        # Test parameter dependencies
        h_high_temp = designer._calculate_heat_transfer_coefficient(2500.0, 0.5, 0.05)
        self.assertGreater(h_high_temp, h)  # Higher temperature -> higher h

        h_high_flow = designer._calculate_heat_transfer_coefficient(2100.0, 0.5, 0.1)
        self.assertGreater(h_high_flow, h)  # Higher flow -> higher h

    def test_calculate_wall_temperature(self):
        """Test wall temperature calculation."""
        designer = ChamberDesigner()

        wall_temp = designer._calculate_wall_temperature(
            gas_temperature=2100.0,
            heat_transfer_coefficient=50.0,
            insulation_thickness=0.1,
            ambient_temperature=293.15
        )

        # Wall temperature should be between gas and ambient
        self.assertGreater(wall_temp, 293.15)
        self.assertLess(wall_temp, 2100.0)

        # Test insulation effect
        wall_temp_thick = designer._calculate_wall_temperature(
            2100.0, 50.0, 0.2, 293.15  # Thicker insulation
        )
        self.assertGreater(wall_temp_thick, wall_temp)  # Better insulation -> higher inner wall temp

    def test_calculate_chamber_surface_area(self):
        """Test chamber surface area calculation."""
        designer = ChamberDesigner()

        diameter = 1.0  # m
        length = 3.0   # m

        surface_area = designer._calculate_chamber_surface_area(diameter, length)

        # Expected area: πDL + 2π(D²/4)
        expected_cylindrical = math.pi * diameter * length
        expected_ends = 2 * math.pi * diameter**2 / 4
        expected_total = expected_cylindrical + expected_ends

        self.assertAlmostEqual(surface_area, expected_total, places=6)

    def test_calculate_heat_loss(self):
        """Test heat loss calculation."""
        designer = ChamberDesigner()

        heat_loss = designer._calculate_heat_loss(
            surface_area=10.0,
            wall_temperature=800.0,  # K
            ambient_temperature=293.15,
            insulation_thickness=0.1
        )

        self.assertGreater(heat_loss, 0)

        # Test temperature difference scaling
        heat_loss_high = designer._calculate_heat_loss(
            10.0, 1000.0, 293.15, 0.1  # Higher wall temperature
        )
        self.assertGreater(heat_loss_high, heat_loss)

    def test_calculate_temperature_distribution(self):
        """Test temperature distribution calculation."""
        designer = ChamberDesigner(combustion_calculator=self.mock_combustion)

        # Create sample design results
        design_results = ChamberDesignResults(
            chamber_volume=1.0,
            chamber_diameter=1.0,
            chamber_length=3.0,
            chamber_area=0.785,
            residence_time=0.5,
            heat_transfer_coefficient=50.0,
            wall_temperature=800.0,
            heat_loss_rate=5000.0,
            thermal_efficiency=80.0,
            volume_heat_release_rate=1e6
        )

        temp_dist = designer.calculate_temperature_distribution(
            design_results,
            self.mock_combustion_result,
            num_points=5
        )

        # Check structure
        self.assertIn("positions", temp_dist)
        self.assertIn("temperatures", temp_dist)
        self.assertEqual(len(temp_dist["positions"]), 6)  # num_points + 1
        self.assertEqual(len(temp_dist["temperatures"]), 6)

        # Check temperature decay
        temperatures = temp_dist["temperatures"]
        self.assertGreater(temperatures[0], temperatures[-1])  # Should decrease along length

        # Check position range
        positions = temp_dist["positions"]
        self.assertEqual(positions[0], 0.0)
        self.assertEqual(positions[-1], design_results.chamber_length)

    def test_validate_design(self):
        """Test design validation."""
        designer = ChamberDesigner()

        # Create valid design results
        valid_results = ChamberDesignResults(
            chamber_volume=1.0,
            chamber_diameter=1.0,
            chamber_length=3.0,
            chamber_area=0.785,
            residence_time=0.5,
            heat_transfer_coefficient=50.0,
            wall_temperature=1200.0,  # K
            heat_loss_rate=5000.0,
            thermal_efficiency=80.0,
            volume_heat_release_rate=1e6
        )

        validation = designer.validate_design(valid_results)

        # Check validation structure
        expected_keys = [
            "residence_time_adequate",
            "volume_heat_rate_acceptable",
            "dimensions_reasonable",
            "efficiency_acceptable",
            "wall_temperature_safe"
        ]

        for key in expected_keys:
            self.assertIn(key, validation)

        # All should pass for valid design
        for criterion, passed in validation.items():
            with self.subTest(criterion=criterion):
                self.assertTrue(passed, f"Validation failed for {criterion}")

    def test_validate_design_failures(self):
        """Test validation with invalid design parameters."""
        designer = ChamberDesigner()

        # Create invalid design results
        invalid_results = ChamberDesignResults(
            chamber_volume=1.0,
            chamber_diameter=5.0,     # Too large
            chamber_length=3.0,
            chamber_area=0.785,
            residence_time=0.05,     # Too short
            heat_transfer_coefficient=50.0,
            wall_temperature=2000.0,  # Too high
            heat_loss_rate=50000.0,   # High losses
            thermal_efficiency=50.0,  # Low efficiency
            volume_heat_release_rate=5e6  # Too high
        )

        validation = designer.validate_design(invalid_results)

        # These should fail
        self.assertFalse(validation["residence_time_adequate"])
        self.assertFalse(validation["volume_heat_rate_acceptable"])
        self.assertFalse(validation["dimensions_reasonable"])
        self.assertFalse(validation["efficiency_acceptable"])
        self.assertFalse(validation["wall_temperature_safe"])

    def test_get_design_recommendations(self):
        """Test design recommendations generation."""
        designer = ChamberDesigner()

        # Create design with various issues
        problematic_results = ChamberDesignResults(
            chamber_volume=1.0,
            chamber_diameter=1.0,
            chamber_length=8.0,      # Very long (L/D > 5)
            chamber_area=0.785,
            residence_time=0.05,     # Too short
            heat_transfer_coefficient=50.0,
            wall_temperature=1700.0,  # High temperature
            heat_loss_rate=50000.0,
            thermal_efficiency=60.0,  # Low efficiency
            volume_heat_release_rate=5e6  # Too high
        )

        recommendations = designer.get_design_recommendations(problematic_results)

        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)

        # Check that recommendations contain expected content
        rec_text = " ".join(recommendations).lower()
        self.assertTrue(any(word in rec_text for word in ["komor", "izolac", "objem"]))

    def test_high_volume_heat_rate_correction(self):
        """Test automatic correction of high volume heat release rate."""
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
        mock_combustion.constants = self.mock_constants

        # High flow rate combustion result
        high_power_result = CombustionResults(
            fuel_flow_rate=0.02,  # High flow rate
            air_flow_rate=0.34,
            flue_gas_flow_rate=0.36,
            excess_air_ratio=1.2,
            adiabatic_flame_temperature=2100.0,
            heat_release_rate=1000000,  # High heat release
            co2_volume_percent=10.0,
            o2_volume_percent=2.0
        )
        mock_combustion.calculate_combustion_products.return_value = high_power_result

        designer = ChamberDesigner(combustion_calculator=mock_combustion)

        # Should automatically increase chamber size to reduce volume heat rate
        result = designer.design_chamber(
            fuel_type="methane",
            required_power=1000000,  # 1 MW
            target_residence_time=0.5
        )

        # Volume heat rate should be within limits
        self.assertLessEqual(result.volume_heat_release_rate, designer.MAX_VOLUME_HEAT_RATE)

    def test_chamber_design_results_dataclass(self):
        """Test ChamberDesignResults dataclass functionality."""
        results = ChamberDesignResults(
            chamber_volume=1.0,
            chamber_diameter=1.0,
            chamber_length=3.0,
            chamber_area=0.785,
            residence_time=0.5,
            heat_transfer_coefficient=50.0,
            wall_temperature=800.0,
            heat_loss_rate=5000.0,
            thermal_efficiency=80.0,
            volume_heat_release_rate=1e6
        )

        # Test all attributes are accessible
        self.assertEqual(results.chamber_volume, 1.0)
        self.assertEqual(results.chamber_diameter, 1.0)
        self.assertEqual(results.chamber_length, 3.0)
        self.assertEqual(results.chamber_area, 0.785)
        self.assertEqual(results.residence_time, 0.5)
        self.assertEqual(results.heat_transfer_coefficient, 50.0)
        self.assertEqual(results.wall_temperature, 800.0)
        self.assertEqual(results.heat_loss_rate, 5000.0)
        self.assertEqual(results.thermal_efficiency, 80.0)
        self.assertEqual(results.volume_heat_release_rate, 1e6)
        
        # Test backward compatibility property
        self.assertEqual(results.chamber_wall_temperature, 800.0)
        self.assertEqual(results.wall_temperature, results.chamber_wall_temperature)

    def test_edge_case_minimal_chamber(self):
        """Test design of minimal chamber."""
        designer = ChamberDesigner(combustion_calculator=self.mock_combustion)

        # Very low flow rate for small chamber
        small_result = CombustionResults(
            fuel_flow_rate=0.0002,
            air_flow_rate=0.0034,
            flue_gas_flow_rate=0.0036,
            excess_air_ratio=1.2,
            adiabatic_flame_temperature=2100.0,
            heat_release_rate=10000,
            co2_volume_percent=10.0,
            o2_volume_percent=2.0
        )
        self.mock_combustion.calculate_combustion_products.return_value = small_result

        result = designer.design_chamber(
            fuel_type="methane",
            required_power=10000,   # 10 kW - small
            target_residence_time=0.5
        )

        # Should still produce valid results within limits
        self.assertGreaterEqual(result.chamber_diameter, designer.MIN_CHAMBER_DIAMETER)
        self.assertGreater(result.chamber_volume, 0)

    def test_different_insulation_thicknesses(self):
        """Test chamber design with different insulation thicknesses."""
        designer = ChamberDesigner(combustion_calculator=self.mock_combustion)

        thicknesses = [0.05, 0.1, 0.2]  # Different insulation thicknesses
        results = []

        for thickness in thicknesses:
            result = designer.design_chamber(
                fuel_type="methane",
                required_power=100000,
                target_residence_time=0.5,
                wall_insulation_thickness=thickness
            )
            results.append(result)

        # Better insulation should result in higher inner wall temperature, lower heat losses, higher efficiency
        self.assertLess(results[0].wall_temperature, results[2].wall_temperature)  # Thicker insulation -> higher inner wall temp
        self.assertGreater(results[0].heat_loss_rate, results[2].heat_loss_rate)   # Thinner insulation -> higher heat losses
        self.assertLess(results[0].thermal_efficiency, results[2].thermal_efficiency)  # Thinner insulation -> lower efficiency

    def test_constants_validation(self):
        """Test that design constants are reasonable."""
        designer = ChamberDesigner()

        # Check design constants are reasonable
        self.assertGreater(designer.MIN_RESIDENCE_TIME, 0)
        self.assertGreater(designer.MAX_RESIDENCE_TIME, designer.MIN_RESIDENCE_TIME)
        self.assertGreater(designer.MAX_VOLUME_HEAT_RATE, 1e6)  # At least 1 MW/m³
        self.assertGreater(designer.MIN_CHAMBER_DIAMETER, 0)
        self.assertGreater(designer.MAX_CHAMBER_DIAMETER, designer.MIN_CHAMBER_DIAMETER)
        self.assertGreater(designer.TYPICAL_LD_RATIO, 1.0)
        self.assertGreater(designer.WALL_THICKNESS, 0)


if __name__ == "__main__":
    unittest.main()
