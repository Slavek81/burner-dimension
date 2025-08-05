# src/radiation.py

"""
src/radiation.py

Radiation heat transfer calculations module for gas burner design application.
Handles Stefan-Boltzmann law applications, view factors, radiation
exchange, and material emissivity.
"""

import math
import json
import os
from dataclasses import dataclass
from typing import Dict, List

try:
    from .combustion import CombustionCalculator
except ImportError:
    from combustion import CombustionCalculator


@dataclass
class RadiationResults:
    """
    Data class containing results of radiation heat transfer calculations.

    Attributes:
        total_radiation_heat_transfer (float): Total radiation heat transfer [W]
        flame_to_wall_heat_transfer (float): Flame to wall radiation [W]
        wall_to_ambient_heat_transfer (float): Wall to ambient radiation [W]
        flame_emissivity (float): Effective flame emissivity [-]
        wall_emissivity (float): Wall surface emissivity [-]
        flame_absorptivity (float): Flame absorptivity [-]
        view_factor_flame_wall (float): View factor from flame to wall [-]
        radiation_efficiency (float): Radiation heat transfer efficiency [%]
        mean_beam_length (float): Mean beam length for gas radiation [m]
    """

    total_radiation_heat_transfer: float
    flame_to_wall_heat_transfer: float
    wall_to_ambient_heat_transfer: float
    flame_emissivity: float
    wall_emissivity: float
    flame_absorptivity: float
    view_factor_flame_wall: float
    radiation_efficiency: float
    mean_beam_length: float


@dataclass
class SurfaceProperties:
    """
    Data class for surface radiation properties.

    Attributes:
        area (float): Surface area [m²]
        temperature (float): Surface temperature [K]
        emissivity (float): Surface emissivity [-]
        absorptivity (float): Surface absorptivity [-]
    """

    area: float
    temperature: float
    emissivity: float
    absorptivity: float


class RadiationCalculator:
    """
    Calculator for radiation heat transfer in combustion systems.

    This class handles radiation calculations between flames, chamber walls,
    and external surfaces using Stefan-Boltzmann law and view factor methods.

    Attributes:
        combustion_calc (CombustionCalculator): Combustion calculator instance
        material_data (dict): Material properties loaded from JSON
        stefan_boltzmann (float): Stefan-Boltzmann constant
    """

    def __init__(self, combustion_calculator: CombustionCalculator = None):
        """
        Initialize the radiation calculator.

        Args:
            combustion_calculator (CombustionCalculator, optional): Combustion calculator instance
        """
        self.combustion_calc = combustion_calculator or CombustionCalculator()
        self.material_data = self._load_material_data()

        # Physical constants
        self.stefan_boltzmann = self.combustion_calc.constants["stefan_boltzmann_constant"]

        # Default gas radiation properties
        self.CO2_ABSORPTION_COEFF = 0.2  # m⁻¹·atm⁻¹ at typical conditions
        self.H2O_ABSORPTION_COEFF = 0.1  # m⁻¹·atm⁻¹ at typical conditions
        self.SOOT_ABSORPTION_COEFF = 1200  # m⁻¹ for luminous flames

    def _load_material_data(self) -> dict:
        """
        Load material properties from the fuel data JSON file.

        Returns:
            dict: Material properties data
        """
        try:
            fuel_data_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "data", "fuels.json"
            )
            with open(fuel_data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("material_properties", {})
        except Exception:
            # Return default values if file loading fails
            return {
                "steel_oxidized": {"emissivity": 0.79},
                "refractory_brick": {"emissivity": 0.75},
                "flame_gases": {"emissivity": 0.2},
                "soot_particles": {"emissivity": 0.85},
            }

    def calculate_flame_radiation(
        self,
        flame_temperature: float,
        chamber_wall_temperature: float,
        chamber_diameter: float,
        chamber_length: float,
        fuel_type: str,
        excess_air_ratio: float = 1.2,
        soot_concentration: float = 0.0,
    ) -> RadiationResults:
        """
        Calculate radiation heat transfer from flame to chamber walls.

        Args:
            flame_temperature (float): Average flame temperature [K]
            chamber_wall_temperature (float): Chamber wall temperature [K]
            chamber_diameter (float): Chamber internal diameter [m]
            chamber_length (float): Chamber length [m]
            fuel_type (str): Type of fuel
            excess_air_ratio (float): Excess air ratio
            soot_concentration (float): Soot concentration [kg/m³]

        Returns:
            RadiationResults: Complete radiation calculation results
        """
        if flame_temperature <= chamber_wall_temperature:
            raise ValueError("Teplota plamene musí být vyšší než teplota stěny")

        if chamber_diameter <= 0 or chamber_length <= 0:
            raise ValueError("Rozměry komory musí být kladné")

        # Calculate mean beam length for cylindrical chamber
        mean_beam_length = self._calculate_mean_beam_length(chamber_diameter, chamber_length)

        # Calculate flame emissivity
        flame_emissivity = self._calculate_flame_emissivity(
            flame_temperature, mean_beam_length, fuel_type, excess_air_ratio, soot_concentration
        )

        # Calculate flame absorptivity (Kirchhoff's law approximation)
        flame_absorptivity = flame_emissivity  # Assumption for gray body

        # Get wall emissivity
        wall_emissivity = self._get_wall_emissivity("refractory_brick")

        # Calculate view factor from flame to walls
        view_factor_flame_wall = self._calculate_view_factor_cylinder(
            chamber_diameter, chamber_length
        )

        # Calculate flame volume and wall area
        flame_volume = math.pi * (chamber_diameter / 2) ** 2 * chamber_length
        wall_area = math.pi * chamber_diameter * chamber_length

        # Calculate radiation heat transfer using zone method
        flame_to_wall_heat_transfer = self._calculate_flame_to_wall_radiation(
            flame_volume,
            wall_area,
            flame_temperature,
            chamber_wall_temperature,
            flame_emissivity,
            wall_emissivity,
            view_factor_flame_wall,
        )

        # Calculate wall to ambient radiation
        chamber_outer_surface_area = self._calculate_outer_surface_area(
            chamber_diameter, chamber_length, wall_thickness=0.1
        )

        wall_to_ambient_heat_transfer = self._calculate_surface_radiation(
            chamber_outer_surface_area,
            chamber_wall_temperature,
            293.15,  # Ambient temperature
            wall_emissivity,
            0.9,  # Ambient absorptivity
        )

        # Calculate total radiation heat transfer
        total_radiation = flame_to_wall_heat_transfer

        # Calculate radiation efficiency
        # This represents how effectively thermal energy is transferred by radiation
        max_theoretical_radiation = (
            self.stefan_boltzmann * wall_area * (flame_temperature**4 - chamber_wall_temperature**4)
        )

        radiation_efficiency = (
            (total_radiation / max_theoretical_radiation) * 100
            if max_theoretical_radiation > 0
            else 0
        )

        return RadiationResults(
            total_radiation_heat_transfer=total_radiation,
            flame_to_wall_heat_transfer=flame_to_wall_heat_transfer,
            wall_to_ambient_heat_transfer=wall_to_ambient_heat_transfer,
            flame_emissivity=flame_emissivity,
            wall_emissivity=wall_emissivity,
            flame_absorptivity=flame_absorptivity,
            view_factor_flame_wall=view_factor_flame_wall,
            radiation_efficiency=radiation_efficiency,
            mean_beam_length=mean_beam_length,
        )

    def _calculate_mean_beam_length(self, diameter: float, length: float) -> float:
        """
        Calculate mean beam length for radiation in cylindrical chamber.

        Args:
            diameter (float): Chamber diameter [m]
            length (float): Chamber length [m]

        Returns:
            float: Mean beam length [m]
        """
        # For cylindrical geometry: L_m = 3.6 * V / A
        volume = math.pi * (diameter / 2) ** 2 * length
        surface_area = math.pi * diameter * length + 2 * math.pi * (diameter / 2) ** 2

        mean_beam_length = 3.6 * volume / surface_area

        return mean_beam_length

    def _calculate_flame_emissivity(
        self,
        temperature: float,
        beam_length: float,
        fuel_type: str,
        excess_air_ratio: float,
        soot_concentration: float,
    ) -> float:
        """
        Calculate effective flame emissivity considering gas radiation and soot.

        Args:
            temperature (float): Flame temperature [K]
            beam_length (float): Mean beam length [m]
            fuel_type (str): Type of fuel
            excess_air_ratio (float): Excess air ratio
            soot_concentration (float): Soot concentration [kg/m³]

        Returns:
            float: Effective flame emissivity [-]
        """
        # Get combustion product concentrations
        if fuel_type == "natural_gas":
            co2_fraction = 0.12 / excess_air_ratio  # Volume fraction
            h2o_fraction = 0.18 / excess_air_ratio  # Volume fraction
        elif fuel_type == "propane":
            co2_fraction = 0.14 / excess_air_ratio
            h2o_fraction = 0.16 / excess_air_ratio
        else:
            co2_fraction = 0.12 / excess_air_ratio
            h2o_fraction = 0.18 / excess_air_ratio

        # Calculate partial pressures (assuming atmospheric pressure)
        pressure = 101325  # Pa
        p_co2 = co2_fraction * pressure / 101325  # atm
        p_h2o = h2o_fraction * pressure / 101325  # atm

        # Calculate gas emissivity using exponential approximation
        # ε_gas = 1 - exp(-k * p * L)
        emissivity_co2 = 1 - math.exp(-self.CO2_ABSORPTION_COEFF * p_co2 * beam_length)
        emissivity_h2o = 1 - math.exp(-self.H2O_ABSORPTION_COEFF * p_h2o * beam_length)

        # Combine CO2 and H2O emissivities (with interaction correction)
        gas_emissivity = emissivity_co2 + emissivity_h2o - 0.15 * emissivity_co2 * emissivity_h2o

        # Add soot contribution if present
        if soot_concentration > 0:
            soot_emissivity = 1 - math.exp(
                -self.SOOT_ABSORPTION_COEFF * soot_concentration * beam_length
            )
            # Combine gas and soot emissivities
            total_emissivity = 1 - (1 - gas_emissivity) * (1 - soot_emissivity)
        else:
            total_emissivity = gas_emissivity

        # Apply temperature correction factor
        temp_correction = (temperature / 1000) ** 0.2  # Empirical correction

        return min(0.95, total_emissivity * temp_correction)  # Cap at 0.95

    def _get_wall_emissivity(self, material_type: str) -> float:
        """
        Get wall emissivity from material properties.

        Args:
            material_type (str): Material type identifier

        Returns:
            float: Material emissivity [-]
        """
        return self.material_data.get(material_type, {}).get("emissivity", 0.8)

    def _calculate_view_factor_cylinder(self, diameter: float, length: float) -> float:
        """
        Calculate view factor from flame volume to cylindrical wall.

        Args:
            diameter (float): Cylinder diameter [m]
            length (float): Cylinder length [m]

        Returns:
            float: View factor [-]
        """
        # For volume to surface in cylindrical geometry
        # Simplified calculation assuming uniform flame distribution
        aspect_ratio = length / diameter

        if aspect_ratio < 0.5:
            # Short cylinder
            view_factor = 0.7
        elif aspect_ratio > 5.0:
            # Long cylinder
            view_factor = 0.9
        else:
            # Intermediate cylinder - linear interpolation
            view_factor = 0.7 + 0.2 * (aspect_ratio - 0.5) / 4.5

        return view_factor

    def _calculate_flame_to_wall_radiation(
        self,
        flame_volume: float,
        wall_area: float,
        flame_temperature: float,
        wall_temperature: float,
        flame_emissivity: float,
        wall_emissivity: float,
        view_factor: float,
    ) -> float:
        """
        Calculate radiation heat transfer from flame volume to wall surface.

        Args:
            flame_volume (float): Flame volume [m³]
            wall_area (float): Wall surface area [m²]
            flame_temperature (float): Flame temperature [K]
            wall_temperature (float): Wall temperature [K]
            flame_emissivity (float): Flame emissivity [-]
            wall_emissivity (float): Wall emissivity [-]
            view_factor (float): View factor from flame to wall [-]

        Returns:
            float: Heat transfer rate [W]
        """
        # Using zone method for volume-to-surface radiation
        # Q = σ * A_flame * F_flame_wall * ε_effective * (T_flame⁴ - T_wall⁴)

        # Effective area (flame volume converted to equivalent area)
        effective_flame_area = flame_volume ** (2 / 3)  # Approximation for volume to area

        # Effective emissivity considering both surfaces
        emissivity_effective = 1 / (
            1 / flame_emissivity + wall_area / (effective_flame_area * wall_emissivity) - 1
        )

        # Heat transfer calculation
        heat_transfer = (
            self.stefan_boltzmann
            * effective_flame_area
            * view_factor
            * emissivity_effective
            * (flame_temperature**4 - wall_temperature**4)
        )

        return max(0, heat_transfer)

    def _calculate_surface_radiation(
        self,
        area: float,
        surface_temperature: float,
        ambient_temperature: float,
        surface_emissivity: float,
        ambient_absorptivity: float,
    ) -> float:
        """
        Calculate radiation heat transfer from surface to ambient.

        Args:
            area (float): Surface area [m²]
            surface_temperature (float): Surface temperature [K]
            ambient_temperature (float): Ambient temperature [K]
            surface_emissivity (float): Surface emissivity [-]
            ambient_absorptivity (float): Ambient absorptivity [-]

        Returns:
            float: Heat transfer rate [W]
        """
        # Simple surface to ambient radiation
        heat_transfer = (
            self.stefan_boltzmann
            * area
            * surface_emissivity
            * (surface_temperature**4 - ambient_temperature**4)
        )

        return max(0, heat_transfer)

    def _calculate_outer_surface_area(
        self, inner_diameter: float, length: float, wall_thickness: float
    ) -> float:
        """
        Calculate outer surface area of cylindrical chamber.

        Args:
            inner_diameter (float): Inner diameter [m]
            length (float): Chamber length [m]
            wall_thickness (float): Wall thickness [m]

        Returns:
            float: Outer surface area [m²]
        """
        outer_diameter = inner_diameter + 2 * wall_thickness
        outer_area = math.pi * outer_diameter * length + 2 * math.pi * (outer_diameter / 2) ** 2

        return outer_area

    def calculate_radiation_exchange_network(
        self, surfaces: List[SurfaceProperties], view_factors_matrix: List[List[float]]
    ) -> Dict[str, float]:
        """
        Calculate radiation exchange between multiple surfaces using network method.

        Args:
            surfaces (List[SurfaceProperties]): List of surface properties
            view_factors_matrix (List[List[float]]): Matrix of view factors

        Returns:
            Dict[str, float]: Heat transfer rates between surfaces
        """
        n = len(surfaces)

        if len(view_factors_matrix) != n or any(len(row) != n for row in view_factors_matrix):
            raise ValueError("Matice view faktorů musí být čtvercová a odpovídat počtu povrchů")

        # Calculate radiation heat transfer between each pair
        heat_transfers = {}

        for i in range(n):
            for j in range(i + 1, n):
                # Calculate heat transfer from surface i to surface j
                area_i = surfaces[i].area
                temp_i = surfaces[i].temperature
                temp_j = surfaces[j].temperature
                emiss_i = surfaces[i].emissivity
                emiss_j = surfaces[j].emissivity
                view_factor_ij = view_factors_matrix[i][j]

                # Effective emissivity for two-surface enclosure
                if view_factor_ij > 0:
                    effective_emissivity = 1 / (
                        1 / emiss_i + (area_i / surfaces[j].area) * (1 / emiss_j - 1)
                    )

                    heat_transfer_ij = (
                        self.stefan_boltzmann
                        * area_i
                        * view_factor_ij
                        * effective_emissivity
                        * (temp_i**4 - temp_j**4)
                    )

                    heat_transfers[f"surface_{i}_to_surface_{j}"] = heat_transfer_ij

        return heat_transfers

    def get_material_emissivity(self, material_name: str, temperature: float = None) -> float:
        """
        Get material emissivity, potentially temperature-dependent.

        Args:
            material_name (str): Material identifier
            temperature (float, optional): Temperature [K] for temperature-dependent properties

        Returns:
            float: Material emissivity [-]
        """
        if material_name not in self.material_data:
            return 0.8  # Default value

        material_props = self.material_data[material_name]

        # Check if temperature is within valid range
        if temperature and "temperature_range" in material_props:
            temp_range = material_props["temperature_range"]
            temp_celsius = temperature - 273.15

            if temp_celsius < temp_range[0] or temp_celsius > temp_range[1]:
                # Temperature outside valid range - use with caution
                pass

        return material_props.get("emissivity", 0.8)


# Example usage and testing functions
def main():
    """
    Example usage of the RadiationCalculator class.
    """
    try:
        calc = RadiationCalculator()

        # Example radiation calculation
        flame_temperature = 1800  # K
        wall_temperature = 1200  # K
        chamber_diameter = 0.5  # m
        chamber_length = 1.5  # m
        fuel_type = "natural_gas"

        results = calc.calculate_flame_radiation(
            flame_temperature=flame_temperature,
            chamber_wall_temperature=wall_temperature,
            chamber_diameter=chamber_diameter,
            chamber_length=chamber_length,
            fuel_type=fuel_type,
            excess_air_ratio=1.2,
            soot_concentration=0.001,  # kg/m³
        )

        print("Výpočet radiace pro spalovací komoru:")
        print(f"Teplota plamene: {flame_temperature-273.15:.0f} °C")
        print(f"Teplota stěny: {wall_temperature-273.15:.0f} °C")
        print(f"Rozměry komory: ⌀{chamber_diameter*1000:.0f} × {chamber_length*1000:.0f} mm")
        print("\nVýsledky radiace:")
        print(f"Celkový radiační přenos tepla: {results.total_radiation_heat_transfer/1000:.1f} kW")
        print(f"Přenos z plamene na stěnu: {results.flame_to_wall_heat_transfer/1000:.1f} kW")
        print(f"Přenos ze stěny do okolí: {results.wall_to_ambient_heat_transfer/1000:.1f} kW")
        print(f"Emisivita plamene: {results.flame_emissivity:.3f}")
        print(f"Emisivita stěny: {results.wall_emissivity:.3f}")
        print(f"View faktor plamen-stěna: {results.view_factor_flame_wall:.3f}")
        print(f"Účinnost radiace: {results.radiation_efficiency:.1f} %")
        print(f"Střední délka paprsku: {results.mean_beam_length:.3f} m")

        # Test material emissivity lookup
        print("\nEmisivity materiálů:")
        materials = ["steel_oxidized", "refractory_brick", "flame_gases", "soot_particles"]
        for material in materials:
            emissivity = calc.get_material_emissivity(material, temperature=1200)
            print(f"{material}: {emissivity:.3f}")

    except Exception as e:
        print(f"Chyba: {e}")


if __name__ == "__main__":
    main()
