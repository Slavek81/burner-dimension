# src/chamber_design.py

"""
src/chamber_design.py

Combustion chamber design and dimensioning module for gas burner design application.
Handles chamber volume calculations, heat transfer, residence time, and temperature distribution.
"""

import math
from dataclasses import dataclass
from typing import Dict, Tuple

try:
    from .combustion import CombustionCalculator, CombustionResults
    from .burner_design import BurnerDesigner
except ImportError:
    from combustion import CombustionCalculator, CombustionResults
    from burner_design import BurnerDesigner


@dataclass
class ChamberDesignResults:
    """
    Data class containing results of combustion chamber design calculations.

    Attributes:
        chamber_volume (float): Required chamber volume [m³]
        chamber_diameter (float): Chamber diameter [m]
        chamber_length (float): Chamber length [m]
        chamber_area (float): Chamber cross-sectional area [m²]
        residence_time (float): Gas residence time in chamber [s]
        heat_transfer_coefficient (float): Overall heat transfer coefficient [W/m²K]
        wall_temperature (float): Average wall temperature [K]
        heat_loss_rate (float): Heat loss through chamber walls [W]
        thermal_efficiency (float): Thermal efficiency of chamber [%]
        volume_heat_release_rate (float): Volume heat release rate [W/m³]
    """

    chamber_volume: float
    chamber_diameter: float
    chamber_length: float
    chamber_area: float
    residence_time: float
    heat_transfer_coefficient: float
    wall_temperature: float
    heat_loss_rate: float
    thermal_efficiency: float
    volume_heat_release_rate: float

    @property
    def chamber_wall_temperature(self) -> float:
        """
        Alias for wall_temperature for backward compatibility.
        
        Returns:
            float: Average wall temperature [K]
        """
        return self.wall_temperature


class ChamberDesigner:
    """
    Designer for combustion chambers with thermal calculations.

    This class handles the sizing and design of combustion chambers based on
    combustion requirements, heat transfer calculations, and residence time constraints.

    Attributes:
        combustion_calc (CombustionCalculator): Combustion calculator instance
        burner_designer (BurnerDesigner): Burner designer instance
        safety_factor (float): Safety factor for design calculations
    """

    def __init__(
        self,
        combustion_calculator: CombustionCalculator = None,
        burner_designer: BurnerDesigner = None,
        safety_factor: float = 1.5,
        fuel_data_path: str = None,
    ):
        """
        Initialize the chamber designer.

        Args:
            combustion_calculator (CombustionCalculator, optional): Combustion calculator instance
            burner_designer (BurnerDesigner, optional): Burner designer instance
            safety_factor (float): Safety factor for design calculations
            fuel_data_path (str, optional): Path to fuel data file
        """
        self.combustion_calc = combustion_calculator or CombustionCalculator(
            fuel_data_path=fuel_data_path
        )
        self.burner_designer = burner_designer or BurnerDesigner(self.combustion_calc)
        self.safety_factor = safety_factor

        # Design constants
        self.MIN_RESIDENCE_TIME = (
            0.1  # s, minimum residence time for complete combustion
        )
        self.MAX_RESIDENCE_TIME = 10.0  # s, maximum practical residence time
        self.MAX_VOLUME_HEAT_RATE = 3e6  # W/m³, maximum volume heat release rate
        self.MIN_CHAMBER_DIAMETER = 0.1  # m, minimum practical chamber diameter
        self.MAX_CHAMBER_DIAMETER = 3.0  # m, maximum practical chamber diameter
        self.TYPICAL_LD_RATIO = 3.0  # Length to diameter ratio
        self.WALL_THICKNESS = 0.05  # m, typical refractory wall thickness

    def design_chamber(
        self,
        fuel_type: str,
        required_power: float,
        target_residence_time: float = 0.5,
        wall_insulation_thickness: float = 0.1,
        ambient_temperature: float = 293.15,
        target_efficiency: float = 0.85,
    ) -> ChamberDesignResults:
        """
        Design a combustion chamber based on power and residence time requirements.

        Args:
            fuel_type (str): Type of fuel to be used
            required_power (float): Required thermal power [W]
            target_residence_time (float): Target gas residence time [s]
            wall_insulation_thickness (float): Wall insulation thickness [m]
            ambient_temperature (float): Ambient temperature [K]
            target_efficiency (float): Target thermal efficiency [-]

        Returns:
            ChamberDesignResults: Complete chamber design results

        Raises:
            ValueError: If design parameters are invalid or unfeasible
        """
        if required_power <= 0:
            raise ValueError("Požadovaný výkon musí být větší než nula")

        if target_residence_time < self.MIN_RESIDENCE_TIME:
            raise ValueError(
                f"Doba zdržení je příliš krátká. Minimum: {self.MIN_RESIDENCE_TIME} s"
            )

        if target_residence_time > self.MAX_RESIDENCE_TIME:
            raise ValueError(
                f"Doba zdržení je příliš dlouhá. Maximum: {self.MAX_RESIDENCE_TIME} s"
            )

        # Get fuel properties and calculate combustion
        fuel_props = self.combustion_calc.get_fuel_properties(fuel_type)["properties"]
        fuel_flow_rate = required_power / fuel_props["lower_heating_value_mass"]

        combustion_results = self.combustion_calc.calculate_combustion_products(
            fuel_type, fuel_flow_rate, 1.2  # 20% excess air
        )

        # Calculate required chamber volume based on residence time
        flue_gas_volume_flow = self._calculate_flue_gas_volume_flow(
            combustion_results, combustion_results.adiabatic_flame_temperature
        )

        chamber_volume = (
            flue_gas_volume_flow * target_residence_time * self.safety_factor
        )

        # Calculate chamber dimensions
        chamber_diameter, chamber_length, chamber_area = (
            self._calculate_chamber_dimensions(chamber_volume)
        )

        # Calculate volume heat release rate
        volume_heat_release_rate = required_power / chamber_volume

        if volume_heat_release_rate > self.MAX_VOLUME_HEAT_RATE:
            # Increase chamber size if heat release rate is too high
            chamber_volume = required_power / self.MAX_VOLUME_HEAT_RATE
            chamber_diameter, chamber_length, chamber_area = (
                self._calculate_chamber_dimensions(chamber_volume)
            )
            volume_heat_release_rate = required_power / chamber_volume

        # Calculate actual residence time with new dimensions
        actual_residence_time = chamber_volume / flue_gas_volume_flow

        # Calculate heat transfer and wall temperature
        heat_transfer_coefficient = self._calculate_heat_transfer_coefficient(
            combustion_results.adiabatic_flame_temperature,
            chamber_diameter,
            combustion_results.flue_gas_flow_rate,
        )

        wall_temperature = self._calculate_wall_temperature(
            combustion_results.adiabatic_flame_temperature,
            heat_transfer_coefficient,
            wall_insulation_thickness,
            ambient_temperature,
        )

        # Calculate heat losses
        chamber_surface_area = self._calculate_chamber_surface_area(
            chamber_diameter, chamber_length
        )

        heat_loss_rate = self._calculate_heat_loss(
            chamber_surface_area,
            wall_temperature,
            ambient_temperature,
            wall_insulation_thickness,
        )

        # Calculate thermal efficiency
        thermal_efficiency = (1 - heat_loss_rate / required_power) * 100

        if thermal_efficiency < target_efficiency * 100:
            # Increase insulation thickness recommendation
            pass  # This could trigger a warning or recommendation

        return ChamberDesignResults(
            chamber_volume=chamber_volume,
            chamber_diameter=chamber_diameter,
            chamber_length=chamber_length,
            chamber_area=chamber_area,
            residence_time=actual_residence_time,
            heat_transfer_coefficient=heat_transfer_coefficient,
            wall_temperature=wall_temperature,
            heat_loss_rate=heat_loss_rate,
            thermal_efficiency=thermal_efficiency,
            volume_heat_release_rate=volume_heat_release_rate,
        )

    def _calculate_flue_gas_volume_flow(
        self, combustion_results: CombustionResults, gas_temperature: float
    ) -> float:
        """
        Calculate flue gas volumetric flow rate at operating temperature.

        Args:
            combustion_results (CombustionResults): Combustion calculation results
            gas_temperature (float): Gas temperature [K]

        Returns:
            float: Volumetric flow rate [m³/s]
        """
        constants = self.combustion_calc.constants

        # Using ideal gas law to convert mass flow to volume flow
        # V̇ = (ṁ * R * T) / (P * M)
        gas_constant = constants["universal_gas_constant"]
        pressure = constants["standard_pressure"]  # Assume atmospheric pressure
        molecular_weight = constants["air_molecular_weight"] / 1000  # kg/mol

        volume_flow = (
            combustion_results.flue_gas_flow_rate * gas_constant * gas_temperature
        ) / (pressure * molecular_weight)

        return volume_flow

    def _calculate_chamber_dimensions(
        self, volume: float
    ) -> Tuple[float, float, float]:
        """
        Calculate chamber dimensions based on required volume.

        Args:
            volume (float): Required chamber volume [m³]

        Returns:
            Tuple[float, float, float]: Diameter, length, and cross-sectional area
        """
        # Calculate diameter based on cylindrical chamber with L/D ratio
        # V = π * D² * L / 4, with L = L/D * D
        diameter = (4 * volume / (math.pi * self.TYPICAL_LD_RATIO)) ** (1 / 3)

        # Apply practical limits
        diameter = max(
            self.MIN_CHAMBER_DIAMETER, min(self.MAX_CHAMBER_DIAMETER, diameter)
        )

        # Calculate length and area
        length = self.TYPICAL_LD_RATIO * diameter
        area = math.pi * diameter**2 / 4

        return diameter, length, area

    def _calculate_heat_transfer_coefficient(
        self, gas_temperature: float, chamber_diameter: float, mass_flow_rate: float
    ) -> float:
        """
        Calculate overall heat transfer coefficient from gas to chamber walls.

        Args:
            gas_temperature (float): Average gas temperature [K]
            chamber_diameter (float): Chamber diameter [m]
            mass_flow_rate (float): Gas mass flow rate [kg/s]

        Returns:
            float: Heat transfer coefficient [W/m²K]
        """
        # Simplified calculation based on empirical correlations
        # For turbulent flow in cylindrical chambers

        # Calculate Reynolds number (simplified)
        gas_velocity = mass_flow_rate / (
            1.0 * math.pi * chamber_diameter**2 / 4  # Assuming ρ ≈ 1 kg/m³ at high temp
        )

        reynolds = (
            1.0 * gas_velocity * chamber_diameter / 2e-5
        )  # ν ≈ 2e-5 m²/s for hot gases

        # Nusselt number correlation for turbulent flow
        if reynolds > 2300:
            nusselt = 0.023 * (reynolds**0.8) * (0.7**0.4)  # Pr ≈ 0.7 for gases
        else:
            nusselt = 3.66  # Laminar flow

        # Thermal conductivity of hot combustion gases
        thermal_conductivity = 0.05 + (gas_temperature - 273.15) * 5e-5  # Empirical

        # Heat transfer coefficient
        h = nusselt * thermal_conductivity / chamber_diameter

        return h

    def _calculate_wall_temperature(
        self,
        gas_temperature: float,
        heat_transfer_coefficient: float,
        insulation_thickness: float,
        ambient_temperature: float,
    ) -> float:
        """
        Calculate chamber wall temperature considering heat transfer.

        Args:
            gas_temperature (float): Gas temperature [K]
            heat_transfer_coefficient (float): Heat transfer coefficient [W/m²K]
            insulation_thickness (float): Insulation thickness [m]
            ambient_temperature (float): Ambient temperature [K]

        Returns:
            float: Wall temperature [K]
        """
        # Thermal conductivity of insulation (typical refractory material)
        insulation_conductivity = 0.2  # W/mK

        # External heat transfer coefficient (natural convection + radiation)
        h_external = 10.0  # W/m²K

        # Thermal resistances
        r_convection = 1 / heat_transfer_coefficient
        r_conduction = insulation_thickness / insulation_conductivity
        r_external = 1 / h_external

        total_resistance = r_convection + r_conduction + r_external

        # Heat flux (assuming steady state)
        heat_flux = (gas_temperature - ambient_temperature) / total_resistance

        # Wall temperature (inner surface)
        wall_temperature = gas_temperature - heat_flux * r_convection

        return wall_temperature

    def _calculate_chamber_surface_area(self, diameter: float, length: float) -> float:
        """
        Calculate total heat transfer surface area of cylindrical chamber.

        Args:
            diameter (float): Chamber diameter [m]
            length (float): Chamber length [m]

        Returns:
            float: Surface area [m²]
        """
        # Cylindrical surface area: A = π * D * L + 2 * π * D²/4 (including ends)
        cylindrical_area = math.pi * diameter * length
        end_areas = 2 * math.pi * diameter**2 / 4

        return cylindrical_area + end_areas

    def _calculate_heat_loss(
        self,
        surface_area: float,
        wall_temperature: float,
        ambient_temperature: float,
        insulation_thickness: float,
    ) -> float:
        """
        Calculate heat loss from chamber to ambient.

        Args:
            surface_area (float): Chamber surface area [m²]
            wall_temperature (float): Wall temperature [K]
            ambient_temperature (float): Ambient temperature [K]
            insulation_thickness (float): Insulation thickness [m]

        Returns:
            float: Heat loss rate [W]
        """
        # Thermal conductivity of insulation
        insulation_conductivity = 0.2  # W/mK

        # External heat transfer coefficient
        h_external = 10.0  # W/m²K

        # Overall heat transfer coefficient through insulation
        u_overall = 1 / (
            insulation_thickness / insulation_conductivity + 1 / h_external
        )

        # Heat loss calculation
        heat_loss = u_overall * surface_area * (wall_temperature - ambient_temperature)

        return heat_loss

    def calculate_temperature_distribution(
        self,
        design_results: ChamberDesignResults,
        combustion_results: CombustionResults,
        num_points: int = 10,
    ) -> Dict[str, list]:
        """
        Calculate temperature distribution along chamber length.

        Args:
            design_results (ChamberDesignResults): Chamber design results
            combustion_results (CombustionResults): Combustion results
            num_points (int): Number of calculation points along length

        Returns:
            Dict[str, list]: Dictionary with position and temperature arrays
        """
        positions = []
        temperatures = []

        inlet_temperature = combustion_results.adiabatic_flame_temperature

        for i in range(num_points + 1):
            position = i * design_results.chamber_length / num_points
            positions.append(position)

            # Exponential temperature decay along length (simplified model)
            decay_constant = 2.0 / design_results.chamber_length
            temperature = inlet_temperature * math.exp(
                -decay_constant * position
            ) + design_results.wall_temperature * (
                1 - math.exp(-decay_constant * position)
            )
            temperatures.append(temperature)

        return {"positions": positions, "temperatures": temperatures}

    def validate_design(self, design_results: ChamberDesignResults) -> Dict[str, bool]:
        """
        Validate chamber design against safety and performance criteria.

        Args:
            design_results (ChamberDesignResults): Design results to validate

        Returns:
            Dict[str, bool]: Validation results for different criteria
        """
        validation = {
            "residence_time_adequate": (
                self.MIN_RESIDENCE_TIME
                <= design_results.residence_time
                <= self.MAX_RESIDENCE_TIME
            ),
            "volume_heat_rate_acceptable": (
                design_results.volume_heat_release_rate <= self.MAX_VOLUME_HEAT_RATE
            ),
            "dimensions_reasonable": (
                self.MIN_CHAMBER_DIAMETER
                <= design_results.chamber_diameter
                <= self.MAX_CHAMBER_DIAMETER
            ),
            "efficiency_acceptable": (
                design_results.thermal_efficiency >= 70.0  # Minimum 70% efficiency
            ),
            "wall_temperature_safe": (
                design_results.wall_temperature
                <= 1800.0  # Maximum safe wall temperature
            ),
        }

        return validation

    def get_design_recommendations(self, design_results: ChamberDesignResults) -> list:
        """
        Get design recommendations based on calculated results.

        Args:
            design_results (ChamberDesignResults): Design results

        Returns:
            list: List of design recommendations
        """
        recommendations = []

        validation = self.validate_design(design_results)

        if not validation["residence_time_adequate"]:
            if design_results.residence_time < self.MIN_RESIDENCE_TIME:
                recommendations.append(
                    "Doba zdržení je příliš krátká - zvětšete objem komory"
                )
            else:
                recommendations.append(
                    "Doba zdržení je příliš dlouhá - zmenšete objem komory"
                )

        if not validation["volume_heat_rate_acceptable"]:
            recommendations.append(
                "Objemová hustota tepelného toku je příliš vysoká - zvětšete komoru"
            )

        if not validation["efficiency_acceptable"]:
            recommendations.append(
                "Nízká tepelná účinnost - zvyšte izolaci nebo optimalizujte geometrii"
            )

        if design_results.wall_temperature > 1600:
            recommendations.append(
                "Vysoká teplota stěny - zvyšte chlazení nebo izolaci"
            )

        if design_results.chamber_length / design_results.chamber_diameter > 5:
            recommendations.append("Velmi dlouhá komora - zvažte jiný poměr L/D")

        return recommendations


# Example usage and testing functions
def main():
    """
    Example usage of the ChamberDesigner class.
    """
    try:
        designer = ChamberDesigner()

        # Example design calculation
        fuel_type = "natural_gas"
        required_power = 100000  # W (100 kW)
        target_residence_time = 0.5  # s

        results = designer.design_chamber(
            fuel_type=fuel_type,
            required_power=required_power,
            target_residence_time=target_residence_time,
        )

        print(f"Návrh spalovací komory pro {fuel_type}:")
        print(f"Požadovaný výkon: {required_power/1000:.1f} kW")
        print(f"Objem komory: {results.chamber_volume:.3f} m³")
        print(f"Průměr komory: {results.chamber_diameter*1000:.0f} mm")
        print(f"Délka komory: {results.chamber_length*1000:.0f} mm")
        print(f"Doba zdržení: {results.residence_time:.2f} s")
        print(
            f"Objemová hustota tepelného toku: {results.volume_heat_release_rate/1e6:.2f} MW/m³"
        )
        print(f"Teplota stěny: {results.wall_temperature-273.15:.0f} °C")
        print(f"Tepelná účinnost: {results.thermal_efficiency:.1f} %")
        print(f"Tepelné ztráty: {results.heat_loss_rate/1000:.1f} kW")

        # Temperature distribution
        temp_dist = designer.calculate_temperature_distribution(
            results,
            designer.combustion_calc.calculate_combustion_products(
                fuel_type, 0.002, 1.2
            ),
        )

        print("\nTeplotní profil:")
        for i, (pos, temp) in enumerate(
            zip(temp_dist["positions"], temp_dist["temperatures"])
        ):
            if i % 3 == 0:  # Print every 3rd point
                print(f"Pozice {pos*1000:.0f} mm: {temp-273.15:.0f} °C")

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
