# src/pressure_losses.py

"""
src/pressure_losses.py

Pressure loss calculations module for gas burner design application.
Handles friction losses in pipes, minor losses from fittings, and system pressure requirements.
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple

try:
    from .combustion import CombustionCalculator
    from .burner_design import BurnerDesignResults
except ImportError:
    from combustion import CombustionCalculator
    from burner_design import BurnerDesignResults


@dataclass
class PipeSegment:
    """
    Data class representing a pipe segment with its properties.

    Attributes:
        length (float): Pipe length [m]
        diameter (float): Internal diameter [m]
        roughness (float): Surface roughness [m]
        material (str): Pipe material type
        elevation_change (float): Elevation change [m] (positive = upward)
    """

    length: float
    diameter: float
    roughness: float
    material: str
    elevation_change: float = 0.0


@dataclass
class Fitting:
    """
    Data class representing a pipe fitting.

    Attributes:
        type (str): Fitting type (elbow, valve, tee, etc.)
        quantity (int): Number of fittings
        loss_coefficient (float): Loss coefficient K [-]
        diameter (float): Fitting diameter [m]
    """

    type: str
    quantity: int
    loss_coefficient: float
    diameter: float


@dataclass
class PressureLossResults:
    """
    Data class containing results of pressure loss calculations.

    Attributes:
        total_pressure_loss (float): Total system pressure loss [Pa]
        friction_losses (float): Total friction losses in pipes [Pa]
        minor_losses (float): Total minor losses from fittings [Pa]
        elevation_losses (float): Pressure losses due to elevation changes [Pa]
        burner_pressure_loss (float): Pressure loss across burner [Pa]
        required_supply_pressure (float): Required supply pressure [Pa]
        system_resistance_coefficient (float): Overall system K-factor [-]
        reynolds_number (float): Reynolds number in main pipe [-]
        friction_factor (float): Darcy friction factor [-]
        velocity_pressure (float): Velocity pressure in main pipe [Pa]
    """

    total_pressure_loss: float
    friction_losses: float
    minor_losses: float
    elevation_losses: float
    burner_pressure_loss: float
    required_supply_pressure: float
    system_resistance_coefficient: float
    reynolds_number: float
    friction_factor: float
    velocity_pressure: float


class PressureLossCalculator:
    """
    Calculator for pressure losses in gas piping systems.

    This class handles calculation of friction losses, minor losses from fittings,
    elevation effects, and total system pressure requirements for gas burner systems.

    Attributes:
        combustion_calc (CombustionCalculator): Combustion calculator instance
        safety_factor (float): Safety factor for pressure calculations
        fitting_coefficients (dict): Database of fitting loss coefficients
    """

    def __init__(
        self,
        combustion_calculator: CombustionCalculator = None,
        safety_factor: float = 1.3,
    ):
        """
        Initialize the pressure loss calculator.

        Args:
            combustion_calculator (CombustionCalculator, optional): Combustion calculator instance
            safety_factor (float): Safety factor for pressure calculations
        """
        self.combustion_calc = combustion_calculator or CombustionCalculator()
        self.safety_factor = safety_factor

        # Pipe roughness values [m]
        self.PIPE_ROUGHNESS = {
            "steel_new": 0.000045,
            "steel_used": 0.00015,
            "galvanized": 0.00015,
            "cast_iron": 0.00026,
            "copper": 0.0000015,
            "plastic": 0.0000015,
            "stainless_steel": 0.000045,
        }

        # Fitting loss coefficients
        self.FITTING_COEFFICIENTS = {
            "elbow_90_sharp": 0.9,
            "elbow_90_long": 0.6,
            "elbow_45": 0.4,
            "tee_through": 0.2,
            "tee_branch": 1.0,
            "gate_valve_open": 0.15,
            "gate_valve_half": 2.1,
            "ball_valve_open": 0.05,
            "globe_valve_open": 6.0,
            "check_valve": 2.0,
            "pipe_entrance_sharp": 0.5,
            "pipe_entrance_rounded": 0.05,
            "pipe_exit": 1.0,
            "reducer_gradual": 0.2,
            "reducer_sudden": 0.5,
            "expansion_gradual": 0.3,
            "expansion_sudden": 1.0,
        }

    def calculate_system_pressure_losses(
        self,
        pipe_segments: List[PipeSegment],
        fittings: List[Fitting],
        mass_flow_rate: float,
        gas_density: float,
        gas_viscosity: float = 1.5e-5,
        burner_results: BurnerDesignResults = None,
    ) -> PressureLossResults:
        """
        Calculate total pressure losses in gas piping system.

        Args:
            pipe_segments (List[PipeSegment]): List of pipe segments
            fittings (List[Fitting]): List of fittings and components
            mass_flow_rate (float): Gas mass flow rate [kg/s]
            gas_density (float): Gas density [kg/m³]
            gas_viscosity (float): Dynamic viscosity [Pa·s]
            burner_results (BurnerDesignResults, optional): Burner design results

        Returns:
            PressureLossResults: Complete pressure loss calculation results

        Raises:
            ValueError: If input parameters are invalid
        """
        if mass_flow_rate <= 0:
            raise ValueError("Hmotnostní průtok musí být větší než nula")

        if gas_density <= 0:
            raise ValueError("Hustota plynu musí být větší než nula")

        if not pipe_segments:
            raise ValueError("Musí být zadán alespoň jeden úsek potrubí")

        # Calculate friction losses in pipe segments
        total_friction_loss = 0.0
        main_reynolds = 0.0
        main_friction_factor = 0.0
        main_velocity_pressure = 0.0

        for segment in pipe_segments:
            friction_loss, reynolds, friction_factor, velocity_pressure = (
                self._calculate_pipe_friction_loss(
                    segment, mass_flow_rate, gas_density, gas_viscosity
                )
            )
            total_friction_loss += friction_loss

            # Store values from the largest diameter pipe (assumed to be main pipe)
            if segment.diameter >= max(s.diameter for s in pipe_segments):
                main_reynolds = reynolds
                main_friction_factor = friction_factor
                main_velocity_pressure = velocity_pressure

        # Calculate minor losses from fittings
        total_minor_loss = 0.0
        for fitting in fittings:
            minor_loss = self._calculate_fitting_loss(
                fitting, mass_flow_rate, gas_density
            )
            total_minor_loss += minor_loss

        # Calculate elevation losses
        total_elevation_loss = self._calculate_elevation_losses(
            pipe_segments, gas_density
        )

        # Include burner pressure loss if provided
        burner_pressure_loss = 0.0
        if burner_results:
            burner_pressure_loss = burner_results.burner_pressure_drop

        # Calculate total system pressure loss
        total_pressure_loss = (
            total_friction_loss
            + total_minor_loss
            + total_elevation_loss
            + burner_pressure_loss
        )

        # Calculate required supply pressure with safety factor
        required_supply_pressure = total_pressure_loss * self.safety_factor

        # Calculate system resistance coefficient
        if main_velocity_pressure > 0:
            system_k_factor = total_pressure_loss / main_velocity_pressure
        else:
            system_k_factor = 0.0

        return PressureLossResults(
            total_pressure_loss=total_pressure_loss,
            friction_losses=total_friction_loss,
            minor_losses=total_minor_loss,
            elevation_losses=total_elevation_loss,
            burner_pressure_loss=burner_pressure_loss,
            required_supply_pressure=required_supply_pressure,
            system_resistance_coefficient=system_k_factor,
            reynolds_number=main_reynolds,
            friction_factor=main_friction_factor,
            velocity_pressure=main_velocity_pressure,
        )

    def _calculate_pipe_friction_loss(
        self,
        segment: PipeSegment,
        mass_flow_rate: float,
        gas_density: float,
        gas_viscosity: float,
    ) -> Tuple[float, float, float, float]:
        """
        Calculate friction loss in a single pipe segment.

        Args:
            segment (PipeSegment): Pipe segment properties
            mass_flow_rate (float): Mass flow rate [kg/s]
            gas_density (float): Gas density [kg/m³]
            gas_viscosity (float): Dynamic viscosity [Pa·s]

        Returns:
            Tuple[float, float, float, float]: Friction loss [Pa], Reynolds number,
                                               friction factor, velocity pressure [Pa]
        """
        # Calculate flow velocity
        area = math.pi * segment.diameter**2 / 4
        velocity = mass_flow_rate / (gas_density * area)

        # Calculate Reynolds number
        reynolds = gas_density * velocity * segment.diameter / gas_viscosity

        # Calculate friction factor using Colebrook-White equation
        friction_factor = self._calculate_friction_factor(
            reynolds, segment.roughness, segment.diameter
        )

        # Calculate velocity pressure
        velocity_pressure = 0.5 * gas_density * velocity**2

        # Calculate friction loss using Darcy-Weisbach equation
        friction_loss = (
            friction_factor * (segment.length / segment.diameter) * velocity_pressure
        )

        return friction_loss, reynolds, friction_factor, velocity_pressure

    def _calculate_friction_factor(
        self, reynolds: float, roughness: float, diameter: float
    ) -> float:
        """
        Calculate Darcy friction factor using Colebrook-White equation.

        Args:
            reynolds (float): Reynolds number [-]
            roughness (float): Surface roughness [m]
            diameter (float): Pipe diameter [m]

        Returns:
            float: Darcy friction factor [-]
        """
        relative_roughness = roughness / diameter

        if reynolds < 2300:
            # Laminar flow
            return 64 / reynolds
        elif reynolds < 4000:
            # Transition region - linear interpolation
            f_laminar = 64 / 2300
            f_turbulent = self._colebrook_white(4000, relative_roughness)
            return f_laminar + (f_turbulent - f_laminar) * (reynolds - 2300) / (
                4000 - 2300
            )
        else:
            # Turbulent flow - Colebrook-White equation
            return self._colebrook_white(reynolds, relative_roughness)

    def _colebrook_white(self, reynolds: float, relative_roughness: float) -> float:
        """
        Solve Colebrook-White equation iteratively for friction factor.

        Args:
            reynolds (float): Reynolds number [-]
            relative_roughness (float): Relative roughness (ε/D) [-]

        Returns:
            float: Friction factor [-]
        """
        # Initial guess using Blasius equation
        f = 0.316 * reynolds ** (-0.25)

        # Iterative solution
        for _ in range(10):  # Maximum 10 iterations
            f_new = (
                -2
                * math.log10(
                    relative_roughness / 3.7 + 2.51 / (reynolds * math.sqrt(f))
                )
            ) ** (-2)

            if abs(f_new - f) < 1e-6:
                break
            f = f_new

        return f

    def _calculate_fitting_loss(
        self, fitting: Fitting, mass_flow_rate: float, gas_density: float
    ) -> float:
        """
        Calculate pressure loss through a fitting.

        Args:
            fitting (Fitting): Fitting properties
            mass_flow_rate (float): Mass flow rate [kg/s]
            gas_density (float): Gas density [kg/m³]

        Returns:
            float: Pressure loss [Pa]
        """
        # Calculate velocity in fitting
        area = math.pi * fitting.diameter**2 / 4
        velocity = mass_flow_rate / (gas_density * area)

        # Calculate velocity pressure
        velocity_pressure = 0.5 * gas_density * velocity**2

        # Calculate loss using K-factor method
        loss = fitting.loss_coefficient * velocity_pressure * fitting.quantity

        return loss

    def _calculate_elevation_losses(
        self, pipe_segments: List[PipeSegment], gas_density: float
    ) -> float:
        """
        Calculate pressure losses due to elevation changes.

        Args:
            pipe_segments (List[PipeSegment]): List of pipe segments
            gas_density (float): Gas density [kg/m³]

        Returns:
            float: Elevation pressure loss [Pa]
        """
        total_elevation_change = sum(
            segment.elevation_change for segment in pipe_segments
        )

        # Hydrostatic pressure change: ΔP = ρ * g * Δh
        gravitational_acceleration = 9.81  # m/s²
        elevation_loss = (
            gas_density * gravitational_acceleration * total_elevation_change
        )

        return elevation_loss

    def get_pipe_roughness(self, material: str) -> float:
        """
        Get pipe roughness value for specified material.

        Args:
            material (str): Pipe material type

        Returns:
            float: Surface roughness [m]
        """
        return self.PIPE_ROUGHNESS.get(material, 0.00015)  # Default to used steel

    def get_fitting_coefficient(self, fitting_type: str) -> float:
        """
        Get loss coefficient for specified fitting type.

        Args:
            fitting_type (str): Fitting type identifier

        Returns:
            float: Loss coefficient K [-]
        """
        return self.FITTING_COEFFICIENTS.get(
            fitting_type, 1.0
        )  # Default conservative value

    def calculate_equivalent_length(
        self, fittings: List[Fitting], pipe_diameter: float
    ) -> float:
        """
        Calculate equivalent length of fittings for simplified calculations.

        Args:
            fittings (List[Fitting]): List of fittings
            pipe_diameter (float): Main pipe diameter [m]

        Returns:
            float: Total equivalent length [m]
        """
        total_equivalent_length = 0.0

        # Equivalent length factors (L/D ratios) for common fittings
        equivalent_length_factors = {
            "elbow_90_sharp": 30,
            "elbow_90_long": 20,
            "elbow_45": 16,
            "tee_through": 20,
            "tee_branch": 60,
            "gate_valve_open": 8,
            "ball_valve_open": 3,
            "globe_valve_open": 340,
            "check_valve": 135,
        }

        for fitting in fittings:
            ld_ratio = equivalent_length_factors.get(fitting.type, 30)  # Default value
            equivalent_length = ld_ratio * pipe_diameter * fitting.quantity
            total_equivalent_length += equivalent_length

        return total_equivalent_length

    def optimize_pipe_diameter(
        self,
        length: float,
        mass_flow_rate: float,
        gas_density: float,
        max_pressure_loss: float,
        material: str = "steel_new",
        max_velocity: float = 20.0,
    ) -> Dict[str, float]:
        """
        Optimize pipe diameter based on pressure drop and velocity constraints.

        Args:
            length (float): Pipe length [m]
            mass_flow_rate (float): Mass flow rate [kg/s]
            gas_density (float): Gas density [kg/m³]
            max_pressure_loss (float): Maximum allowable pressure loss [Pa]
            material (str): Pipe material
            max_velocity (float): Maximum gas velocity [m/s]

        Returns:
            Dict[str, float]: Optimized diameter and related parameters
        """
        roughness = self.get_pipe_roughness(material)

        # Iterate through diameters to find optimal size
        diameters = [d / 1000 for d in range(25, 500, 5)]  # 25mm to 500mm in 5mm steps

        best_diameter = None
        best_results = None

        for diameter in diameters:
            area = math.pi * diameter**2 / 4
            velocity = mass_flow_rate / (gas_density * area)

            # Skip if velocity exceeds limit
            if velocity > max_velocity:
                continue

            # Create temporary pipe segment
            segment = PipeSegment(
                length=length, diameter=diameter, roughness=roughness, material=material
            )

            # Calculate pressure loss
            pressure_loss, reynolds, friction_factor, velocity_pressure = (
                self._calculate_pipe_friction_loss(
                    segment, mass_flow_rate, gas_density, 1.5e-5
                )
            )

            # Check if pressure loss is acceptable
            if pressure_loss <= max_pressure_loss:
                if best_diameter is None or diameter < best_diameter:
                    best_diameter = diameter
                    best_results = {
                        "diameter": diameter,
                        "velocity": velocity,
                        "pressure_loss": pressure_loss,
                        "reynolds_number": reynolds,
                        "friction_factor": friction_factor,
                    }

        if best_results is None:
            # No suitable diameter found
            return {
                "diameter": max(diameters),
                "velocity": mass_flow_rate
                / (gas_density * math.pi * max(diameters) ** 2 / 4),
                "pressure_loss": float("inf"),
                "reynolds_number": 0,
                "friction_factor": 0,
                "warning": "Nelze dosáhnout požadované tlakové ztráty",
            }

        return best_results

    def create_standard_fittings_list(self, pipe_diameter: float) -> List[Fitting]:
        """
        Create a list of standard fittings for typical gas installation.

        Args:
            pipe_diameter (float): Main pipe diameter [m]

        Returns:
            List[Fitting]: List of standard fittings
        """
        standard_fittings = [
            Fitting("pipe_entrance_rounded", 1, 0.05, pipe_diameter),
            Fitting("elbow_90_long", 2, 0.6, pipe_diameter),
            Fitting("tee_through", 1, 0.2, pipe_diameter),
            Fitting("gate_valve_open", 1, 0.15, pipe_diameter),
            Fitting("pipe_exit", 1, 1.0, pipe_diameter),
        ]

        return standard_fittings


# Example usage and testing functions
def main():
    """
    Example usage of the PressureLossCalculator class.
    """
    try:
        calc = PressureLossCalculator()

        # Example system definition
        # Main gas supply line
        pipe_segments = [
            PipeSegment(
                length=10.0,  # 10m long
                diameter=0.05,  # 50mm diameter
                roughness=calc.get_pipe_roughness("steel_new"),
                material="steel_new",
                elevation_change=2.0,  # 2m elevation rise
            ),
            PipeSegment(
                length=5.0,  # 5m long
                diameter=0.025,  # 25mm diameter
                roughness=calc.get_pipe_roughness("steel_new"),
                material="steel_new",
                elevation_change=0.0,
            ),
        ]

        # System fittings
        fittings = [
            Fitting(
                "pipe_entrance_rounded",
                1,
                calc.get_fitting_coefficient("pipe_entrance_rounded"),
                0.05,
            ),
            Fitting(
                "elbow_90_long", 3, calc.get_fitting_coefficient("elbow_90_long"), 0.05
            ),
            Fitting(
                "tee_through", 1, calc.get_fitting_coefficient("tee_through"), 0.05
            ),
            Fitting(
                "gate_valve_open",
                1,
                calc.get_fitting_coefficient("gate_valve_open"),
                0.05,
            ),
            Fitting(
                "reducer_gradual",
                1,
                calc.get_fitting_coefficient("reducer_gradual"),
                0.025,
            ),
            Fitting("pipe_exit", 1, calc.get_fitting_coefficient("pipe_exit"), 0.025),
        ]

        # Gas properties
        mass_flow_rate = 0.002  # kg/s
        gas_density = 0.8  # kg/m³
        gas_viscosity = 1.5e-5  # Pa·s

        # Calculate pressure losses
        results = calc.calculate_system_pressure_losses(
            pipe_segments=pipe_segments,
            fittings=fittings,
            mass_flow_rate=mass_flow_rate,
            gas_density=gas_density,
            gas_viscosity=gas_viscosity,
        )

        print("Výpočet tlakových ztrát plynového systému:")
        print(f"Hmotnostní průtok: {mass_flow_rate:.4f} kg/s")
        print(f"Hustota plynu: {gas_density:.2f} kg/m³")
        print("\nTlakové ztráty:")
        print(f"Třecí ztráty v potrubí: {results.friction_losses:.0f} Pa")
        print(f"Místní ztráty armatury: {results.minor_losses:.0f} Pa")
        print(f"Výškové ztráty: {results.elevation_losses:.0f} Pa")
        print(f"Ztráty v hořáku: {results.burner_pressure_loss:.0f} Pa")
        print(f"Celkové ztráty: {results.total_pressure_loss:.0f} Pa")
        print(f"Požadovaný přítlak: {results.required_supply_pressure:.0f} Pa")
        print("\nParametry proudění:")
        print(f"Reynoldsovo číslo: {results.reynolds_number:.0f}")
        print(f"Součinitel tření: {results.friction_factor:.4f}")
        print(f"Rychlostní tlak: {results.velocity_pressure:.1f} Pa")
        print(f"Součinitel odporu systému: {results.system_resistance_coefficient:.2f}")

        # Test pipe diameter optimization
        print("\nOptimalizace průměru potrubí:")
        optimization = calc.optimize_pipe_diameter(
            length=15.0,
            mass_flow_rate=mass_flow_rate,
            gas_density=gas_density,
            max_pressure_loss=500,  # Pa
            material="steel_new",
        )

        if "warning" not in optimization:
            print(f"Optimální průměr: {optimization['diameter']*1000:.0f} mm")
            print(f"Rychlost plynu: {optimization['velocity']:.1f} m/s")
            print(f"Tlaková ztráta: {optimization['pressure_loss']:.0f} Pa")
        else:
            print(f"Upozornění: {optimization['warning']}")

        # Test equivalent length calculation
        equivalent_length = calc.calculate_equivalent_length(fittings, 0.05)
        print(f"\nEkvivalentní délka armatur: {equivalent_length:.1f} m")

    except Exception as e:
        print(f"Chyba: {e}")


if __name__ == "__main__":
    main()
