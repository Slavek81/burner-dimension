# tests/test_pressure_losses.py

"""
tests/test_pressure_losses.py

Unit tests for pressure loss calculation module.
Tests friction calculations, fitting losses, and system optimization.
"""

import math
import os
import sys
import unittest
from unittest.mock import Mock

# Add src directory to path for imports  # noqa: E402
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from pressure_losses import (  # noqa: E402
    PressureLossCalculator,
    PressureLossResults,
    PipeSegment,
    Fitting,
)
from burner_design import BurnerDesignResults  # noqa: E402
from combustion import CombustionCalculator  # noqa: E402


class TestPressureLossCalculator(unittest.TestCase):
    """Test cases for PressureLossCalculator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.calculator = PressureLossCalculator()

        # Create mock combustion calculator
        self.mock_combustion = Mock(spec=CombustionCalculator)

        # Sample pipe segments for testing
        self.sample_pipe_segments = [
            PipeSegment(
                length=10.0,
                diameter=0.05,  # 50mm
                roughness=0.000045,
                material="steel_new",
                elevation_change=2.0,
            ),
            PipeSegment(
                length=5.0,
                diameter=0.025,  # 25mm
                roughness=0.000045,
                material="steel_new",
                elevation_change=0.0,
            ),
        ]

        # Sample fittings for testing
        self.sample_fittings = [
            Fitting("elbow_90_long", 2, 0.6, 0.05),
            Fitting("gate_valve_open", 1, 0.15, 0.05),
            Fitting("tee_through", 1, 0.2, 0.05),
            Fitting("pipe_exit", 1, 1.0, 0.025),
        ]

        # Sample burner results
        self.sample_burner_results = BurnerDesignResults(
            burner_diameter=0.1,
            burner_area=0.008,
            gas_velocity=20.0,
            burner_pressure_drop=500.0,
            required_supply_pressure=600.0,
            heat_release_density=2e6,
            burner_length=0.3,
            flame_length=1.0,
        )

    def test_initialization_default(self):
        """Test default initialization."""
        calc = PressureLossCalculator()
        self.assertIsInstance(calc.combustion_calc, CombustionCalculator)
        self.assertEqual(calc.safety_factor, 1.3)
        self.assertIsInstance(calc.PIPE_ROUGHNESS, dict)
        self.assertIsInstance(calc.FITTING_COEFFICIENTS, dict)

    def test_initialization_with_parameters(self):
        """Test initialization with custom parameters."""
        calc = PressureLossCalculator(
            combustion_calculator=self.mock_combustion, safety_factor=1.5
        )
        self.assertEqual(calc.combustion_calc, self.mock_combustion)
        self.assertEqual(calc.safety_factor, 1.5)

    def test_calculate_system_pressure_losses_basic(self):
        """Test basic system pressure loss calculation."""
        result = self.calculator.calculate_system_pressure_losses(
            pipe_segments=self.sample_pipe_segments,
            fittings=self.sample_fittings,
            mass_flow_rate=0.002,  # kg/s
            gas_density=0.8,  # kg/m³
            gas_viscosity=1.5e-5,  # Pa·s
            burner_results=self.sample_burner_results,
        )

        # Check result type and basic properties
        self.assertIsInstance(result, PressureLossResults)
        self.assertGreater(result.total_pressure_loss, 0)
        self.assertGreater(result.friction_losses, 0)
        self.assertGreater(result.minor_losses, 0)
        self.assertGreater(result.elevation_losses, 0)
        self.assertEqual(result.burner_pressure_loss, 500.0)
        self.assertGreater(result.required_supply_pressure, result.total_pressure_loss)
        self.assertGreater(result.reynolds_number, 0)
        self.assertGreater(result.friction_factor, 0)
        self.assertGreater(result.velocity_pressure, 0)

    def test_calculate_system_pressure_losses_no_burner(self):
        """Test pressure loss calculation without burner results."""
        result = self.calculator.calculate_system_pressure_losses(
            pipe_segments=self.sample_pipe_segments,
            fittings=self.sample_fittings,
            mass_flow_rate=0.002,
            gas_density=0.8,
            gas_viscosity=1.5e-5,
        )

        self.assertEqual(result.burner_pressure_loss, 0.0)
        self.assertGreater(result.total_pressure_loss, 0)

    def test_calculate_system_pressure_losses_flow_rate_scaling(self):
        """Test that pressure losses scale properly with flow rate."""
        flow_rates = [0.001, 0.002, 0.004]  # kg/s
        results = []

        for flow_rate in flow_rates:
            result = self.calculator.calculate_system_pressure_losses(
                pipe_segments=self.sample_pipe_segments,
                fittings=self.sample_fittings,
                mass_flow_rate=flow_rate,
                gas_density=0.8,
                gas_viscosity=1.5e-5,
            )
            results.append(result)

        # Pressure losses should increase with flow rate (approximately as flow²)
        self.assertLess(results[0].total_pressure_loss, results[1].total_pressure_loss)
        self.assertLess(results[1].total_pressure_loss, results[2].total_pressure_loss)

    def test_invalid_mass_flow_rate(self):
        """Test validation of invalid mass flow rate."""
        # Zero flow rate
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate_system_pressure_losses(
                pipe_segments=self.sample_pipe_segments,
                fittings=self.sample_fittings,
                mass_flow_rate=0.0,
                gas_density=0.8,
            )
        self.assertIn("větší než nula", str(context.exception))

        # Negative flow rate
        with self.assertRaises(ValueError):
            self.calculator.calculate_system_pressure_losses(
                pipe_segments=self.sample_pipe_segments,
                fittings=self.sample_fittings,
                mass_flow_rate=-0.001,
                gas_density=0.8,
            )

    def test_invalid_gas_density(self):
        """Test validation of invalid gas density."""
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate_system_pressure_losses(
                pipe_segments=self.sample_pipe_segments,
                fittings=self.sample_fittings,
                mass_flow_rate=0.002,
                gas_density=0.0,
            )
        self.assertIn("větší než nula", str(context.exception))

    def test_empty_pipe_segments(self):
        """Test validation of empty pipe segments list."""
        with self.assertRaises(ValueError) as context:
            self.calculator.calculate_system_pressure_losses(
                pipe_segments=[],
                fittings=self.sample_fittings,
                mass_flow_rate=0.002,
                gas_density=0.8,
            )
        self.assertIn("alespoň jeden úsek", str(context.exception))

    def test_calculate_pipe_friction_loss(self):
        """Test pipe friction loss calculation."""
        segment = self.sample_pipe_segments[0]

        friction_loss, reynolds, friction_factor, velocity_pressure = (
            self.calculator._calculate_pipe_friction_loss(
                segment=segment,
                mass_flow_rate=0.002,
                gas_density=0.8,
                gas_viscosity=1.5e-5,
            )
        )

        # Check all returned values are positive
        self.assertGreater(friction_loss, 0)
        self.assertGreater(reynolds, 0)
        self.assertGreater(friction_factor, 0)
        self.assertGreater(velocity_pressure, 0)

        # Check Reynolds number is reasonable
        self.assertGreater(reynolds, 1000)  # Should be turbulent

        # Check friction factor is in reasonable range
        self.assertGreater(friction_factor, 0.01)
        self.assertLess(friction_factor, 0.1)

    def test_calculate_friction_factor_laminar(self):
        """Test friction factor calculation in laminar regime."""
        reynolds = 1000  # Laminar flow
        roughness = 0.000045
        diameter = 0.05

        f = self.calculator._calculate_friction_factor(reynolds, roughness, diameter)

        # For laminar flow: f = 64/Re
        expected_f = 64 / reynolds
        self.assertAlmostEqual(f, expected_f, places=4)

    def test_calculate_friction_factor_turbulent(self):
        """Test friction factor calculation in turbulent regime."""
        reynolds = 10000  # Turbulent flow
        roughness = 0.000045
        diameter = 0.05

        f = self.calculator._calculate_friction_factor(reynolds, roughness, diameter)

        # Should be in reasonable range for turbulent flow
        self.assertGreater(f, 0.01)
        self.assertLess(f, 0.1)

    def test_calculate_friction_factor_transition(self):
        """Test friction factor calculation in transition regime."""
        reynolds = 3000  # Transition regime
        roughness = 0.000045
        diameter = 0.05

        f = self.calculator._calculate_friction_factor(reynolds, roughness, diameter)

        # Should be between laminar and turbulent values
        f_laminar = 64 / 2300
        f_turbulent = self.calculator._colebrook_white(4000, roughness / diameter)

        self.assertGreater(f, min(f_laminar, f_turbulent))
        self.assertLess(f, max(f_laminar, f_turbulent))

    def test_colebrook_white(self):
        """Test Colebrook-White equation solution."""
        reynolds = 10000
        relative_roughness = 0.001

        f = self.calculator._colebrook_white(reynolds, relative_roughness)

        # Check convergence - substitute back into equation
        term1 = relative_roughness / 3.7
        term2 = 2.51 / (reynolds * math.sqrt(f))
        lhs = -2 * math.log10(term1 + term2)
        rhs = 1 / math.sqrt(f)

        self.assertAlmostEqual(lhs, rhs, places=3)

    def test_calculate_fitting_loss(self):
        """Test fitting loss calculation."""
        fitting = self.sample_fittings[0]  # elbow_90_long

        loss = self.calculator._calculate_fitting_loss(
            fitting=fitting, mass_flow_rate=0.002, gas_density=0.8
        )

        self.assertGreater(loss, 0)

        # Test quantity scaling
        fitting_double = Fitting("elbow_90_long", 4, 0.6, 0.05)
        loss_double = self.calculator._calculate_fitting_loss(
            fitting_double, 0.002, 0.8
        )

        self.assertAlmostEqual(loss_double, loss * 2, places=1)

    def test_calculate_elevation_losses(self):
        """Test elevation loss calculation."""
        # Create pipe segments with elevation changes
        segments_with_elevation = [
            PipeSegment(10.0, 0.05, 0.000045, "steel", 5.0),  # 5m rise
            PipeSegment(5.0, 0.05, 0.000045, "steel", -2.0),  # 2m drop
        ]

        elevation_loss = self.calculator._calculate_elevation_losses(
            segments_with_elevation, 0.8
        )

        # Net elevation change: 5 - 2 = 3m
        # Expected loss: ρ * g * Δh = 0.8 * 9.81 * 3
        expected_loss = 0.8 * 9.81 * 3

        self.assertAlmostEqual(elevation_loss, expected_loss, places=2)

    def test_get_pipe_roughness(self):
        """Test pipe roughness database."""
        # Test known materials
        steel_roughness = self.calculator.get_pipe_roughness("steel_new")
        self.assertEqual(steel_roughness, 0.000045)

        copper_roughness = self.calculator.get_pipe_roughness("copper")
        self.assertEqual(copper_roughness, 0.0000015)

        # Test unknown material (should return default)
        unknown_roughness = self.calculator.get_pipe_roughness("unknown_material")
        self.assertEqual(unknown_roughness, 0.00015)

    def test_get_fitting_coefficient(self):
        """Test fitting coefficient database."""
        # Test known fittings
        elbow_coeff = self.calculator.get_fitting_coefficient("elbow_90_sharp")
        self.assertEqual(elbow_coeff, 0.9)

        valve_coeff = self.calculator.get_fitting_coefficient("gate_valve_open")
        self.assertEqual(valve_coeff, 0.15)

        # Test unknown fitting (should return default)
        unknown_coeff = self.calculator.get_fitting_coefficient("unknown_fitting")
        self.assertEqual(unknown_coeff, 1.0)

    def test_calculate_equivalent_length(self):
        """Test equivalent length calculation."""
        fittings = [
            Fitting("elbow_90_sharp", 2, 0.9, 0.05),
            Fitting("gate_valve_open", 1, 0.15, 0.05),
        ]

        equivalent_length = self.calculator.calculate_equivalent_length(fittings, 0.05)

        # Expected: 2 * 30 * 0.05 + 1 * 8 * 0.05 = 3.0 + 0.4 = 3.4m
        expected_length = 2 * 30 * 0.05 + 1 * 8 * 0.05

        self.assertAlmostEqual(equivalent_length, expected_length, places=2)

    def test_optimize_pipe_diameter(self):
        """Test pipe diameter optimization."""
        optimization = self.calculator.optimize_pipe_diameter(
            length=10.0,
            mass_flow_rate=0.002,
            gas_density=0.8,
            max_pressure_loss=1000.0,
            material="steel_new",
            max_velocity=15.0,
        )

        # Check result structure
        self.assertIn("diameter", optimization)
        self.assertIn("velocity", optimization)
        self.assertIn("pressure_loss", optimization)
        self.assertIn("reynolds_number", optimization)
        self.assertIn("friction_factor", optimization)

        # Check constraints are satisfied
        self.assertLessEqual(optimization["pressure_loss"], 1000.0)
        self.assertLessEqual(optimization["velocity"], 15.0)
        self.assertGreater(optimization["diameter"], 0)

    def test_optimize_pipe_diameter_impossible_constraints(self):
        """Test pipe diameter optimization with impossible constraints."""
        optimization = self.calculator.optimize_pipe_diameter(
            length=100.0,
            mass_flow_rate=1.0,  # Much higher flow rate
            gas_density=0.8,
            max_pressure_loss=1.0,  # Even lower pressure limit
            material="steel_new",
            max_velocity=1.0,  # Even lower velocity limit
        )

        # Should return warning or find best possible solution
        if "warning" in optimization:
            self.assertEqual(optimization["pressure_loss"], float("inf"))
        else:
            # Algorithm found a solution within constraints
            self.assertLessEqual(optimization["pressure_loss"], 1.0)
            self.assertLessEqual(optimization["velocity"], 1.0)

    def test_create_standard_fittings_list(self):
        """Test creation of standard fittings list."""
        pipe_diameter = 0.05
        fittings = self.calculator.create_standard_fittings_list(pipe_diameter)

        self.assertIsInstance(fittings, list)
        self.assertGreater(len(fittings), 0)

        # Check all fittings have correct diameter
        for fitting in fittings:
            self.assertEqual(fitting.diameter, pipe_diameter)
            self.assertIsInstance(fitting.type, str)
            self.assertGreater(fitting.quantity, 0)
            self.assertGreater(fitting.loss_coefficient, 0)

    def test_pipe_segment_dataclass(self):
        """Test PipeSegment dataclass functionality."""
        segment = PipeSegment(
            length=10.0,
            diameter=0.05,
            roughness=0.000045,
            material="steel_new",
            elevation_change=2.0,
        )

        self.assertEqual(segment.length, 10.0)
        self.assertEqual(segment.diameter, 0.05)
        self.assertEqual(segment.roughness, 0.000045)
        self.assertEqual(segment.material, "steel_new")
        self.assertEqual(segment.elevation_change, 2.0)

    def test_fitting_dataclass(self):
        """Test Fitting dataclass functionality."""
        fitting = Fitting(
            type="elbow_90_long", quantity=2, loss_coefficient=0.6, diameter=0.05
        )

        self.assertEqual(fitting.type, "elbow_90_long")
        self.assertEqual(fitting.quantity, 2)
        self.assertEqual(fitting.loss_coefficient, 0.6)
        self.assertEqual(fitting.diameter, 0.05)

    def test_pressure_loss_results_dataclass(self):
        """Test PressureLossResults dataclass functionality."""
        results = PressureLossResults(
            total_pressure_loss=1000.0,
            friction_losses=600.0,
            minor_losses=200.0,
            elevation_losses=100.0,
            burner_pressure_loss=100.0,
            required_supply_pressure=1300.0,
            system_resistance_coefficient=2.5,
            reynolds_number=5000.0,
            friction_factor=0.025,
            velocity_pressure=400.0,
        )

        # Test all attributes are accessible
        self.assertEqual(results.total_pressure_loss, 1000.0)
        self.assertEqual(results.friction_losses, 600.0)
        self.assertEqual(results.minor_losses, 200.0)
        self.assertEqual(results.elevation_losses, 100.0)
        self.assertEqual(results.burner_pressure_loss, 100.0)
        self.assertEqual(results.required_supply_pressure, 1300.0)
        self.assertEqual(results.system_resistance_coefficient, 2.5)
        self.assertEqual(results.reynolds_number, 5000.0)
        self.assertEqual(results.friction_factor, 0.025)
        self.assertEqual(results.velocity_pressure, 400.0)

    def test_edge_case_very_small_pipe(self):
        """Test calculation with very small pipe diameter."""
        small_segment = PipeSegment(
            length=1.0,
            diameter=0.01,  # 10mm - small diameter
            roughness=0.000045,
            material="steel_new",
        )

        friction_loss, reynolds, friction_factor, velocity_pressure = (
            self.calculator._calculate_pipe_friction_loss(
                segment=small_segment,
                mass_flow_rate=0.0001,  # Small flow rate
                gas_density=0.8,
                gas_viscosity=1.5e-5,
            )
        )

        # Should still produce valid results
        self.assertGreater(friction_loss, 0)
        self.assertGreater(reynolds, 0)
        self.assertGreater(friction_factor, 0)

    def test_edge_case_very_large_pipe(self):
        """Test calculation with very large pipe diameter."""
        large_segment = PipeSegment(
            length=10.0,
            diameter=0.5,  # 500mm - large diameter
            roughness=0.000045,
            material="steel_new",
        )

        friction_loss, reynolds, friction_factor, velocity_pressure = (
            self.calculator._calculate_pipe_friction_loss(
                segment=large_segment,
                mass_flow_rate=0.1,  # Large flow rate
                gas_density=0.8,
                gas_viscosity=1.5e-5,
            )
        )

        # Should still produce valid results
        self.assertGreater(friction_loss, 0)
        self.assertGreater(reynolds, 0)
        self.assertGreater(friction_factor, 0)

    def test_safety_factor_application(self):
        """Test that safety factor is properly applied."""
        calc_15 = PressureLossCalculator(safety_factor=1.5)
        calc_20 = PressureLossCalculator(safety_factor=2.0)

        # Calculate same system with different safety factors
        result_15 = calc_15.calculate_system_pressure_losses(
            pipe_segments=self.sample_pipe_segments,
            fittings=self.sample_fittings,
            mass_flow_rate=0.002,
            gas_density=0.8,
        )

        result_20 = calc_20.calculate_system_pressure_losses(
            pipe_segments=self.sample_pipe_segments,
            fittings=self.sample_fittings,
            mass_flow_rate=0.002,
            gas_density=0.8,
        )

        # Total pressure loss should be the same
        self.assertAlmostEqual(
            result_15.total_pressure_loss, result_20.total_pressure_loss, places=1
        )

        # Required supply pressure should scale with safety factor
        expected_ratio = 2.0 / 1.5
        actual_ratio = (
            result_20.required_supply_pressure / result_15.required_supply_pressure
        )
        self.assertAlmostEqual(actual_ratio, expected_ratio, places=2)

    def test_different_pipe_materials(self):
        """Test calculations with different pipe materials."""
        materials = ["steel_new", "copper", "plastic", "cast_iron"]
        results = []

        for material in materials:
            segment = PipeSegment(
                length=10.0,
                diameter=0.05,
                roughness=self.calculator.get_pipe_roughness(material),
                material=material,
            )

            friction_loss, _, friction_factor, _ = (
                self.calculator._calculate_pipe_friction_loss(
                    segment, 0.002, 0.8, 1.5e-5
                )
            )

            results.append(
                {
                    "material": material,
                    "friction_loss": friction_loss,
                    "friction_factor": friction_factor,
                }
            )

        # Smoother materials should have lower friction factors and losses
        smooth_materials = ["copper", "plastic"]
        rough_materials = ["cast_iron", "steel_used"]

        for smooth in smooth_materials:
            smooth_result = next(r for r in results if r["material"] == smooth)
            for rough in rough_materials:
                if rough in [r["material"] for r in results]:
                    rough_result = next(r for r in results if r["material"] == rough)
                    self.assertLess(
                        smooth_result["friction_factor"],
                        rough_result["friction_factor"],
                    )


if __name__ == "__main__":
    unittest.main()
