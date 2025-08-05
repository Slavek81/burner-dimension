# src/burner_design.py

"""
src/burner_design.py

Burner design and dimensioning module for gas burner design application.
Handles burner sizing calculations, pressure requirements, and flow calculations.
"""

import math
from dataclasses import dataclass
from typing import Dict

try:
    from .combustion import CombustionCalculator
except ImportError:
    from combustion import CombustionCalculator


@dataclass
class BurnerDesignResults:
    """
    Data class containing results of burner design calculations.

    Attributes:
        burner_diameter (float): Required burner diameter [m]
        burner_area (float): Burner cross-sectional area [m²]
        gas_velocity (float): Gas velocity at burner outlet [m/s]
        burner_pressure_drop (float): Pressure drop across burner [Pa]
        required_supply_pressure (float): Required gas supply pressure [Pa]
        heat_release_density (float): Heat release per unit area [W/m²]
        burner_length (float): Required burner length [m]
        flame_length (float): Estimated flame length [m]
    """

    burner_diameter: float
    burner_area: float
    gas_velocity: float
    burner_pressure_drop: float
    required_supply_pressure: float
    heat_release_density: float
    burner_length: float
    flame_length: float


class BurnerDesigner:
    """
    Designer for gas burners with dimensional calculations.

    This class handles the sizing and design of gas burners based on
    combustion requirements, pressure constraints, and safety factors.

    Attributes:
        combustion_calc (CombustionCalculator): Combustion calculator instance
        safety_factor (float): Safety factor for design calculations
    """

    def __init__(
        self,
        combustion_calculator: CombustionCalculator = None,
        safety_factor: float = 1.2,
        fuel_data_path: str = None,
    ):
        """
        Initialize the burner designer.

        Args:
            combustion_calculator (CombustionCalculator, optional): Combustion calculator instance
            safety_factor (float): Safety factor for design calculations
            fuel_data_path (str, optional): Path to fuel data file
        """
        self.combustion_calc = combustion_calculator or CombustionCalculator(
            fuel_data_path=fuel_data_path
        )
        self.safety_factor = safety_factor

        # Design constants
        self.MAX_GAS_VELOCITY = 100.0  # m/s, maximum allowable gas velocity
        self.MIN_GAS_VELOCITY = 5.0  # m/s, minimum gas velocity for stability
        self.MAX_HEAT_DENSITY = 5e6  # W/m², maximum heat release density
        self.BURNER_PRESSURE_DROP_COEFF = 0.8  # Pressure drop coefficient

    def design_burner(
        self,
        fuel_type: str,
        required_power: float,
        supply_pressure: float,
        target_velocity: float = None,
        excess_air_ratio: float = 1.2,
    ) -> BurnerDesignResults:
        """
        Design a gas burner based on power requirements.

        Args:
            fuel_type (str): Type of fuel to be used
            required_power (float): Required thermal power [W]
            supply_pressure (float): Available gas supply pressure [Pa]
            target_velocity (float, optional): Target gas velocity [m/s]
            excess_air_ratio (float): Excess air ratio

        Returns:
            BurnerDesignResults: Complete burner design results

        Raises:
            ValueError: If design parameters are invalid or unfeasible
        """
        if required_power <= 0:
            raise ValueError("Požadovaný výkon musí být větší než nula")

        if supply_pressure <= 0:
            raise ValueError("Tlak plynu musí být větší než nula")

        # Get fuel properties
        fuel_props = self.combustion_calc.get_fuel_properties(fuel_type)["properties"]

        # Calculate required fuel flow rate
        fuel_flow_rate = required_power / fuel_props["lower_heating_value_mass"]

        # Calculate combustion properties
        # Note: combustion_results currently not used in calculations
        # but available for future enhancements
        _ = self.combustion_calc.calculate_combustion_products(
            fuel_type, fuel_flow_rate, excess_air_ratio
        )

        # Calculate gas density at operating conditions
        # Calculate gas density at 20°C
        gas_density = self._calculate_gas_density(fuel_type, supply_pressure, 293.15)

        # Calculate burner dimensions
        if target_velocity is None:
            target_velocity = self._calculate_optimal_velocity(
                fuel_type, required_power
            )

        # Validate velocity range
        if target_velocity < self.MIN_GAS_VELOCITY:
            target_velocity = self.MIN_GAS_VELOCITY
        elif target_velocity > self.MAX_GAS_VELOCITY:
            target_velocity = self.MAX_GAS_VELOCITY

        # Calculate burner area and diameter
        volume_flow_rate = fuel_flow_rate / gas_density
        burner_area = volume_flow_rate / target_velocity
        burner_diameter = math.sqrt(4 * burner_area / math.pi)

        # Calculate pressure drop across burner
        burner_pressure_drop = self._calculate_burner_pressure_drop(
            gas_density, target_velocity, burner_diameter
        )

        # Calculate required supply pressure
        required_supply_pressure = burner_pressure_drop * self.safety_factor

        if required_supply_pressure > supply_pressure:
            raise ValueError(
                f"Nedostatečný tlak plynu. "
                f"Požadováno: {required_supply_pressure:.0f} Pa, "
                f"k dispozici: {supply_pressure:.0f} Pa"
            )

        # Calculate heat release density
        heat_release_density = required_power / burner_area

        if heat_release_density > self.MAX_HEAT_DENSITY:
            raise ValueError(
                f"Příliš vysoká hustota tepelného toku: "
                f"{heat_release_density/1e6:.1f} MW/m². "
                f"Maximum: {self.MAX_HEAT_DENSITY/1e6:.1f} MW/m²"
            )

        # Calculate burner length (L/D ratio typically 2-4 for gas burners)
        burner_length = burner_diameter * 3.0

        # Estimate flame length
        flame_length = self._calculate_flame_length(
            burner_diameter, target_velocity, fuel_type
        )

        return BurnerDesignResults(
            burner_diameter=burner_diameter,
            burner_area=burner_area,
            gas_velocity=target_velocity,
            burner_pressure_drop=burner_pressure_drop,
            required_supply_pressure=required_supply_pressure,
            heat_release_density=heat_release_density,
            burner_length=burner_length,
            flame_length=flame_length,
        )

    def _calculate_gas_density(
        self, fuel_type: str, pressure: float, temperature: float
    ) -> float:
        """
        Calculate gas density at given conditions.

        Args:
            fuel_type (str): Type of fuel
            pressure (float): Gas pressure [Pa]
            temperature (float): Gas temperature [K]

        Returns:
            float: Gas density [kg/m³]
        """
        fuel_props = self.combustion_calc.get_fuel_properties(fuel_type)["properties"]
        constants = self.combustion_calc.constants

        # Using ideal gas law: ρ = (P * M) / (R * T)
        # Convert g/mol to kg/mol
        molecular_weight = fuel_props["molecular_weight"] / 1000
        gas_constant = constants["universal_gas_constant"]

        density = (pressure * molecular_weight) / (gas_constant * temperature)

        return density

    def _calculate_optimal_velocity(self, fuel_type: str, power: float) -> float:
        """
        Calculate optimal gas velocity based on fuel type and power.

        Args:
            fuel_type (str): Type of fuel
            power (float): Required power [W]

        Returns:
            float: Optimal gas velocity [m/s]
        """
        # Empirical correlation based on power and fuel type
        if fuel_type in ["natural_gas", "methane"]:
            base_velocity = 20.0  # m/s
        elif fuel_type == "propane":
            base_velocity = 15.0  # m/s
        else:
            base_velocity = 20.0  # m/s

        # Adjust velocity based on power (higher power -> higher velocity for mixing)
        power_factor = min(2.0, (power / 100000) ** 0.3)  # Scale factor for power

        optimal_velocity = base_velocity * power_factor

        # Ensure within limits
        return max(self.MIN_GAS_VELOCITY, min(self.MAX_GAS_VELOCITY, optimal_velocity))

    def _calculate_burner_pressure_drop(
        self, gas_density: float, velocity: float, diameter: float
    ) -> float:
        """
        Calculate pressure drop across the burner.

        Args:
            gas_density (float): Gas density [kg/m³]
            velocity (float): Gas velocity [m/s]
            diameter (float): Burner diameter [m]

        Returns:
            float: Pressure drop [Pa]
        """
        # Using orifice pressure drop equation: ΔP = K * ρ * V² / 2
        # K factor includes discharge coefficient and geometry effects
        k_factor = self.BURNER_PRESSURE_DROP_COEFF

        pressure_drop = k_factor * gas_density * velocity**2 / 2

        return pressure_drop

    def _calculate_flame_length(
        self, burner_diameter: float, gas_velocity: float, fuel_type: str
    ) -> float:
        """
        Estimate flame length based on burner geometry and conditions.

        Args:
            burner_diameter (float): Burner diameter [m]
            gas_velocity (float): Gas velocity [m/s]
            fuel_type (str): Type of fuel

        Returns:
            float: Estimated flame length [m]
        """
        # Empirical correlation for turbulent diffusion flames
        # L/D = C * Re^n where Re is Reynolds number

        fuel_props = self.combustion_calc.get_fuel_properties(fuel_type)["properties"]
        gas_density = fuel_props["density"]

        # Estimate viscosity (simplified)
        viscosity = 1.5e-5  # Pa·s, typical for gases at moderate temperature

        # Calculate Reynolds number
        reynolds = gas_density * gas_velocity * burner_diameter / viscosity

        # Empirical constants for flame length correlation
        if fuel_type in ["natural_gas", "methane"]:
            c_constant = 0.2
            n_exponent = 0.5
        else:
            c_constant = 0.25
            n_exponent = 0.5

        # Calculate flame length
        flame_length = c_constant * (reynolds**n_exponent) * burner_diameter

        # Apply reasonable limits
        min_length = burner_diameter * 5
        max_length = burner_diameter * 50

        return max(min_length, min(max_length, flame_length))

    def validate_design(self, design_results: BurnerDesignResults) -> Dict[str, bool]:
        """
        Validate burner design against safety and performance criteria.

        Args:
            design_results (BurnerDesignResults): Design results to validate

        Returns:
            Dict[str, bool]: Validation results for different criteria
        """
        validation = {
            "velocity_in_range": (
                self.MIN_GAS_VELOCITY
                <= design_results.gas_velocity
                <= self.MAX_GAS_VELOCITY
            ),
            "heat_density_acceptable": (
                design_results.heat_release_density <= self.MAX_HEAT_DENSITY
            ),
            "reasonable_dimensions": (
                0.001 <= design_results.burner_diameter <= 1.0
                and 0.01 <= design_results.burner_length <= 5.0
            ),
            "pressure_drop_reasonable": (
                design_results.burner_pressure_drop
                < design_results.required_supply_pressure * 0.8
            ),
        }

        return validation

    def get_design_recommendations(self, design_results: BurnerDesignResults) -> list:
        """
        Get design recommendations based on calculated results.

        Args:
            design_results (BurnerDesignResults): Design results

        Returns:
            list: List of design recommendations
        """
        recommendations = []

        validation = self.validate_design(design_results)

        if not validation["velocity_in_range"]:
            if design_results.gas_velocity < self.MIN_GAS_VELOCITY:
                recommendations.append(
                    "Rychlost plynu je příliš nízká - zvyšte tlak nebo zmenšete průměr"
                )
            else:
                recommendations.append(
                    "Rychlost plynu je příliš vysoká - snižte tlak nebo zvětšete průměr"
                )

        if not validation["heat_density_acceptable"]:
            recommendations.append(
                "Hustota tepelného toku je příliš vysoká - zvětšete plochu hořáku"
            )

        if design_results.heat_release_density > 3e6:
            recommendations.append(
                "Doporučuje se přídavné chlazení při vysoké hustotě tepelného toku"
            )

        if design_results.flame_length > design_results.burner_length * 10:
            recommendations.append(
                "Dlouhý plamen - zvažte úpravu geometrie spalovací komory"
            )

        return recommendations


# Example usage and testing functions
def main():
    """
    Example usage of the BurnerDesigner class.
    """
    try:
        designer = BurnerDesigner()

        # Example design calculation
        fuel_type = "natural_gas"
        required_power = 100000  # W (100 kW)
        supply_pressure = 3000  # Pa (30 mbar)

        results = designer.design_burner(
            fuel_type=fuel_type,
            required_power=required_power,
            supply_pressure=supply_pressure,
        )

        print(f"Návrh hořáku pro {fuel_type}:")
        print(f"Požadovaný výkon: {required_power/1000:.1f} kW")
        print(f"Průměr hořáku: {results.burner_diameter*1000:.1f} mm")
        print(f"Plocha hořáku: {results.burner_area*1000*1000:.1f} mm²")
        print(f"Rychlost plynu: {results.gas_velocity:.1f} m/s")
        print(f"Tlaková ztráta: {results.burner_pressure_drop:.0f} Pa")
        print(f"Hustota tepelného toku: {results.heat_release_density/1e6:.2f} MW/m²")
        print(f"Délka hořáku: {results.burner_length*1000:.0f} mm")
        print(f"Odhadovaná délka plamene: {results.flame_length*1000:.0f} mm")

        # Validation
        validation = designer.validate_design(results)
        print("\nValidace návrhu:")
        for criterion, passed in validation.items():
            status = "✓" if passed else "✗"
            print(f"{status} {criterion}: {'Prošlo' if passed else 'Neprošlo'}")

        # Recommendations
        recommendations = designer.get_design_recommendations(results)
        if recommendations:
            print("\nDoporučení:")
            for i, rec in enumerate(recommendations, 1):
                print(f"{i}. {rec}")

    except Exception as e:
        print(f"Chyba: {e}")


if __name__ == "__main__":
    main()
