# src/combustion.py

"""
src/combustion.py

Combustion calculations module for gas burner design application.
Handles stoichiometric calculations, flame temperature, and combustion products.
"""

import json
import os
from dataclasses import dataclass
from typing import Tuple


@dataclass
class CombustionResults:
    """
    Data class containing results of combustion calculations.

    Attributes:
        fuel_flow_rate (float): Fuel mass flow rate [kg/s]
        air_flow_rate (float): Air mass flow rate [kg/s]
        flue_gas_flow_rate (float): Flue gas mass flow rate [kg/s]
        adiabatic_flame_temperature (float): Theoretical flame temperature [K]
        heat_release_rate (float): Heat release rate [W]
        excess_air_ratio (float): Excess air ratio [-]
        co2_volume_percent (float): CO2 volume percentage in flue gas [%]
        o2_volume_percent (float): O2 volume percentage in flue gas [%]
    """

    fuel_flow_rate: float
    air_flow_rate: float
    flue_gas_flow_rate: float
    adiabatic_flame_temperature: float
    heat_release_rate: float
    excess_air_ratio: float
    co2_volume_percent: float
    o2_volume_percent: float


class CombustionCalculator:
    """
    Calculator for combustion processes in gas burners.

    This class handles stoichiometric calculations, flame temperature calculations,
    and determination of combustion products composition for various gas fuels.

    Attributes:
        fuel_data (dict): Fuel properties loaded from JSON file
        constants (dict): Physical constants
    """

    def __init__(self, fuel_data_path: str = None):
        """
        Initialize the combustion calculator.

        Args:
            fuel_data_path (str, optional): Path to fuel data JSON file.
                                          If None, uses default path.
        """
        if fuel_data_path is None:
            fuel_data_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "data", "fuels.json"
            )

        self.fuel_data = self._load_fuel_data(fuel_data_path)
        self.constants = self.fuel_data.get("constants", {})

    def _load_fuel_data(self, file_path: str) -> dict:
        """
        Load fuel data from JSON file.

        Args:
            file_path (str): Path to the JSON file

        Returns:
            dict: Loaded fuel data

        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Soubor s daty paliv nebyl nalezen: {file_path}")
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f"Neplatný JSON formát v souboru: {file_path}")

    def calculate_stoichiometric_air(self, fuel_type: str, fuel_flow_rate: float) -> float:
        """
        Calculate stoichiometric air requirement for complete combustion.

        Args:
            fuel_type (str): Type of fuel ('natural_gas', 'methane', 'propane')
            fuel_flow_rate (float): Fuel mass flow rate [kg/s]

        Returns:
            float: Required air mass flow rate [kg/s]

        Raises:
            ValueError: If fuel type is not supported
        """
        if fuel_type not in self.fuel_data["fuels"]:
            raise ValueError(f"Nepodporovaný typ paliva: {fuel_type}")

        fuel_props = self.fuel_data["fuels"][fuel_type]["properties"]
        air_fuel_ratio = fuel_props["air_fuel_ratio_mass"]

        return fuel_flow_rate * air_fuel_ratio

    def calculate_combustion_products(
        self, fuel_type: str, fuel_flow_rate: float, excess_air_ratio: float = 1.2
    ) -> CombustionResults:
        """
        Calculate complete combustion products and properties.

        Args:
            fuel_type (str): Type of fuel
            fuel_flow_rate (float): Fuel mass flow rate [kg/s]
            excess_air_ratio (float): Excess air ratio (1.0 = stoichiometric)

        Returns:
            CombustionResults: Complete combustion calculation results

        Raises:
            ValueError: If fuel type is not supported or inputs are invalid
        """
        if fuel_type not in self.fuel_data["fuels"]:
            raise ValueError(f"Nepodporovaný typ paliva: {fuel_type}")

        if fuel_flow_rate <= 0:
            raise ValueError("Průtok paliva musí být větší než nula")

        if excess_air_ratio < 1.0:
            raise ValueError("Koeficient přebytku vzduchu musí být ≥ 1.0")

        fuel_props = self.fuel_data["fuels"][fuel_type]["properties"]

        # Calculate air flow rates
        stoichiometric_air = self.calculate_stoichiometric_air(fuel_type, fuel_flow_rate)
        actual_air_flow = stoichiometric_air * excess_air_ratio

        # Calculate flue gas flow rate
        flue_gas_flow = fuel_flow_rate + actual_air_flow

        # Calculate heat release rate
        heat_release_rate = fuel_flow_rate * fuel_props["lower_heating_value_mass"]

        # Calculate adiabatic flame temperature (simplified calculation)
        adiabatic_temp = self._calculate_adiabatic_temperature(fuel_type, excess_air_ratio)

        # Calculate flue gas composition
        co2_percent, o2_percent = self._calculate_flue_gas_composition(fuel_type, excess_air_ratio)

        return CombustionResults(
            fuel_flow_rate=fuel_flow_rate,
            air_flow_rate=actual_air_flow,
            flue_gas_flow_rate=flue_gas_flow,
            adiabatic_flame_temperature=adiabatic_temp,
            heat_release_rate=heat_release_rate,
            excess_air_ratio=excess_air_ratio,
            co2_volume_percent=co2_percent,
            o2_volume_percent=o2_percent,
        )

    def _calculate_adiabatic_temperature(self, fuel_type: str, excess_air_ratio: float) -> float:
        """
        Calculate adiabatic flame temperature.

        Args:
            fuel_type (str): Type of fuel
            excess_air_ratio (float): Excess air ratio

        Returns:
            float: Adiabatic flame temperature [K]
        """
        # Simplified calculation based on heating value and heat capacity
        # More accurate calculation would require detailed thermodynamic properties
        base_temperature = 2200  # K, typical for natural gas

        # Adjust for excess air (cooling effect)
        excess_air_correction = 1.0 - (excess_air_ratio - 1.0) * 0.3

        return base_temperature * excess_air_correction + self.constants["standard_temperature"]

    def _calculate_flue_gas_composition(
        self, fuel_type: str, excess_air_ratio: float
    ) -> Tuple[float, float]:
        """
        Calculate CO2 and O2 volume percentages in flue gas.

        Args:
            fuel_type (str): Type of fuel
            excess_air_ratio (float): Excess air ratio

        Returns:
            Tuple[float, float]: CO2 and O2 volume percentages
        """
        # Simplified calculation based on empirical data
        # More accurate calculation would require detailed stoichiometric analysis

        if fuel_type == "natural_gas":
            co2_stoich = 12.0  # % volume at stoichiometric conditions
        elif fuel_type == "methane":
            co2_stoich = 12.0
        elif fuel_type == "propane":
            co2_stoich = 14.0
        else:
            co2_stoich = 12.0

        # Adjust CO2 for excess air dilution
        co2_percent = co2_stoich / excess_air_ratio

        # Calculate O2 percentage (from excess air)
        excess_air_percent = (excess_air_ratio - 1.0) * 100
        o2_percent = excess_air_percent * 0.21 / excess_air_ratio

        return co2_percent, o2_percent

    def get_fuel_properties(self, fuel_type: str) -> dict:
        """
        Get properties of specified fuel type.

        Args:
            fuel_type (str): Type of fuel

        Returns:
            dict: Fuel properties

        Raises:
            ValueError: If fuel type is not supported
        """
        if fuel_type not in self.fuel_data["fuels"]:
            raise ValueError(f"Nepodporovaný typ paliva: {fuel_type}")

        return self.fuel_data["fuels"][fuel_type]

    def get_available_fuels(self) -> list:
        """
        Get list of available fuel types.

        Returns:
            list: List of available fuel type keys
        """
        return list(self.fuel_data["fuels"].keys())


# Example usage and testing functions
def main():
    """
    Example usage of the CombustionCalculator class.
    """
    try:
        calc = CombustionCalculator()

        # Example calculation for natural gas
        fuel_type = "natural_gas"
        fuel_flow = 0.01  # kg/s
        excess_air = 1.2  # 20% excess air

        results = calc.calculate_combustion_products(fuel_type, fuel_flow, excess_air)

        print(f"Výsledky spalování pro {fuel_type}:")
        print(f"Průtok paliva: {results.fuel_flow_rate:.4f} kg/s")
        print(f"Průtok vzduchu: {results.air_flow_rate:.4f} kg/s")
        print(f"Průtok spalin: {results.flue_gas_flow_rate:.4f} kg/s")
        print(f"Adiabatická teplota plamene: {results.adiabatic_flame_temperature:.1f} K")
        print(f"Tepelný výkon: {results.heat_release_rate/1000:.1f} kW")
        print(f"CO2 ve spalinách: {results.co2_volume_percent:.1f} %")
        print(f"O2 ve spalinách: {results.o2_volume_percent:.1f} %")

    except Exception as e:
        print(f"Chyba: {e}")


if __name__ == "__main__":
    main()
