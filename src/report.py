# src/report.py

"""
src/report.py

Comprehensive reporting module for gas burner and combustion chamber calculations.
Generates detailed reports in multiple formats (TXT, CSV, Excel) with complete
calculation results, analysis, and recommendations.
"""

import os
import csv
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
import pandas as pd
from dataclasses import dataclass, asdict


@dataclass
class CalculationMetadata:
    """
    Metadata for calculation report.

    Contains information about the calculation session including
    timestamps, software version, and user parameters.
    """

    calculation_id: str
    timestamp: str
    software_version: str
    user_name: Optional[str] = None
    project_name: Optional[str] = None
    calculation_type: str = "Gas Burner Design"


class BurnerReportGenerator:
    """
    Comprehensive report generator for burner calculations.

    This class handles the generation of detailed technical reports
    in multiple formats, including text summaries, CSV data exports,
    and Excel workbooks with multiple sheets.

    Attributes:
        output_dir (str): Directory for saving report files
        report_metadata (CalculationMetadata): Metadata for the current report
    """

    def __init__(self, output_dir: str = "output"):
        """
        Initialize report generator.

        Args:
            output_dir: Directory path for saving report files
        """
        self.output_dir = output_dir
        self.report_metadata = None

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

    def set_metadata(
        self, project_name: str = None, user_name: str = None, software_version: str = "1.0.0"
    ) -> None:
        """
        Set metadata for the current calculation report.

        Args:
            project_name: Name of the project or calculation
            user_name: Name of the user performing calculation
            software_version: Version of the calculation software
        """
        self.report_metadata = CalculationMetadata(
            calculation_id=f"CALC_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.now().isoformat(),
            software_version=software_version,
            user_name=user_name,
            project_name=project_name,
        )

    def generate_text_report(
        self, calculation_results: Dict, filename: Optional[str] = None
    ) -> str:
        """
        Generate comprehensive text report.

        Creates a detailed text report with all calculation results,
        formatted for easy reading and technical review.

        Args:
            calculation_results: Complete results from all calculation modules
            filename: Optional custom filename (auto-generated if None)

        Returns:
            Path to the generated text report file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"burner_calculation_report_{timestamp}.txt"

        filepath = os.path.join(self.output_dir, filename)

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                # Write header
                f.write("=" * 80 + "\n")
                f.write("ZPRÁVA O VÝPOČTU PLYNOVÉHO HOŘÁKU A SPALOVACÍ KOMORY\n")
                f.write("=" * 80 + "\n\n")

                # Write metadata
                if self.report_metadata:
                    f.write("METADATA VÝPOČTU\n")
                    f.write("-" * 40 + "\n")
                    f.write(f"ID výpočtu: {self.report_metadata.calculation_id}\n")
                    f.write(f"Datum a čas: {self.report_metadata.timestamp}\n")
                    f.write(f"Verze software: {self.report_metadata.software_version}\n")
                    if self.report_metadata.project_name:
                        f.write(f"Název projektu: {self.report_metadata.project_name}\n")
                    if self.report_metadata.user_name:
                        f.write(f"Uživatel: {self.report_metadata.user_name}\n")
                    f.write("\n")

                # Write input parameters
                if "inputs" in calculation_results:
                    f.write("VSTUPNÍ PARAMETRY\n")
                    f.write("-" * 40 + "\n")
                    inputs = calculation_results["inputs"]
                    for key, value in inputs.items():
                        f.write(f"{key}: {value}\n")
                    f.write("\n")

                # Write combustion analysis
                if "combustion" in calculation_results:
                    f.write("ANALÝZA SPALOVÁNÍ\n")
                    f.write("-" * 40 + "\n")
                    combustion = calculation_results["combustion"]

                    f.write(
                        f"Teoretické množství vzduchu: {combustion.get('theoretical_air', 'N/A')} m³/m³\n"
                    )
                    f.write(
                        f"Skutečné množství vzduchu: {combustion.get('actual_air', 'N/A')} m³/m³\n"
                    )
                    f.write(f"Přebytek vzduchu: {combustion.get('excess_air', 'N/A')} %\n")
                    f.write(f"Výhřevnost paliva: {combustion.get('heating_value', 'N/A')} MJ/m³\n")
                    f.write(f"Teplota spalování: {combustion.get('combustion_temp', 'N/A')} °C\n")

                    if "products" in combustion:
                        f.write("\nSložení spalin:\n")
                        for component, concentration in combustion["products"].items():
                            f.write(f"  {component}: {concentration:.2f}%\n")
                    f.write("\n")

                # Write burner design
                if "burner" in calculation_results:
                    f.write("NÁVRH HOŘÁKU\n")
                    f.write("-" * 40 + "\n")
                    burner = calculation_results["burner"]

                    f.write(f"Typ hořáku: {burner.get('type', 'N/A')}\n")
                    f.write(f"Výkon hořáku: {burner.get('power', 'N/A')} kW\n")
                    f.write(f"Průměr trysky: {burner.get('nozzle_diameter', 'N/A')} mm\n")
                    f.write(f"Rychlost plynu: {burner.get('gas_velocity', 'N/A')} m/s\n")
                    f.write(f"Tlak plynu: {burner.get('gas_pressure', 'N/A')} Pa\n")
                    f.write("\n")

                # Write chamber design
                if "chamber" in calculation_results:
                    f.write("NÁVRH SPALOVACÍ KOMORY\n")
                    f.write("-" * 40 + "\n")
                    chamber = calculation_results["chamber"]

                    f.write(f"Objem komory: {chamber.get('volume', 'N/A')} m³\n")
                    f.write(f"Délka komory: {chamber.get('length', 'N/A')} m\n")
                    f.write(f"Průměr komory: {chamber.get('diameter', 'N/A')} m\n")
                    f.write(f"Doba zdržení: {chamber.get('residence_time', 'N/A')} s\n")
                    f.write(f"Tepelné zatížení: {chamber.get('heat_loading', 'N/A')} kW/m³\n")
                    f.write("\n")

                # Write radiation analysis
                if "radiation" in calculation_results:
                    f.write("ANALÝZA RADIAČNÍHO PŘENOSU TEPLA\n")
                    f.write("-" * 40 + "\n")
                    radiation = calculation_results["radiation"]

                    f.write(f"Radiační tepelný tok: {radiation.get('heat_flux', 'N/A')} kW/m²\n")
                    f.write(f"Emisivita plynů: {radiation.get('gas_emissivity', 'N/A')}\n")
                    f.write(f"Emisivita stěn: {radiation.get('wall_emissivity', 'N/A')}\n")
                    f.write(f"Účinnost radiace: {radiation.get('radiation_efficiency', 'N/A')} %\n")
                    f.write("\n")

                # Write pressure losses
                if "pressure_losses" in calculation_results:
                    f.write("ANALÝZA TLAKOVÝCH ZTRÁT\n")
                    f.write("-" * 40 + "\n")
                    pressure = calculation_results["pressure_losses"]

                    if "components" in pressure:
                        f.write("Tlakové ztráty podle komponent:\n")
                        total_loss = 0
                        for component, loss in pressure["components"].items():
                            f.write(f"  {component}: {loss:.1f} Pa\n")
                            total_loss += loss
                        f.write(f"Celková tlaková ztráta: {total_loss:.1f} Pa\n")
                    f.write("\n")

                # Write performance summary
                f.write("SHRNUTÍ VÝKONU\n")
                f.write("-" * 40 + "\n")
                if "efficiency" in calculation_results:
                    f.write(f"Celková účinnost: {calculation_results['efficiency']:.1f} %\n")
                if "emissions" in calculation_results:
                    f.write("Emise:\n")
                    for pollutant, concentration in calculation_results["emissions"].items():
                        f.write(f"  {pollutant}: {concentration:.1f} mg/m³\n")

                # Write recommendations
                f.write("\nDOPORUČENÍ A POZNÁMKY\n")
                f.write("-" * 40 + "\n")
                if "recommendations" in calculation_results:
                    for rec in calculation_results["recommendations"]:
                        f.write(f"• {rec}\n")
                else:
                    f.write("• Ověřte výsledky výpočtu s technickou dokumentací\n")
                    f.write("• Proveďte měření emisí při uvedení do provozu\n")
                    f.write("• Pravidelně kontrolujte nastavení hořáku\n")

                f.write("\n" + "=" * 80 + "\n")
                f.write("Konec zprávy\n")
                f.write("=" * 80 + "\n")

            return filepath

        except Exception as e:
            print(f"Chyba při vytváření textové zprávy: {e}")
            return ""

    def generate_csv_export(self, calculation_results: Dict, filename: Optional[str] = None) -> str:
        """
        Generate CSV export of calculation results.

        Creates a structured CSV file with all numerical results
        suitable for further analysis or data import.

        Args:
            calculation_results: Complete calculation results
            filename: Optional custom filename

        Returns:
            Path to the generated CSV file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"burner_calculation_data_{timestamp}.csv"

        filepath = os.path.join(self.output_dir, filename)

        try:
            # Flatten calculation results for CSV export
            flattened_data = []

            def flatten_dict(d, parent_key="", sep="_"):
                """Recursively flatten nested dictionary."""
                items = []
                for k, v in d.items():
                    new_key = f"{parent_key}{sep}{k}" if parent_key else k
                    if isinstance(v, dict):
                        items.extend(flatten_dict(v, new_key, sep=sep).items())
                    elif isinstance(v, (list, tuple)):
                        for i, item in enumerate(v):
                            items.append((f"{new_key}_{i}", item))
                    else:
                        items.append((new_key, v))
                return dict(items)

            flat_results = flatten_dict(calculation_results)

            # Create CSV data
            with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)

                # Write header
                writer.writerow(["Parametr", "Hodnota", "Jednotka", "Kategorie"])

                # Write metadata
                if self.report_metadata:
                    writer.writerow(
                        ["calculation_id", self.report_metadata.calculation_id, "-", "metadata"]
                    )
                    writer.writerow(["timestamp", self.report_metadata.timestamp, "-", "metadata"])
                    writer.writerow(
                        ["software_version", self.report_metadata.software_version, "-", "metadata"]
                    )

                # Write flattened results
                for key, value in flat_results.items():
                    # Determine category from key
                    category = key.split("_")[0] if "_" in key else "general"

                    # Determine unit (simplified logic)
                    unit = self._determine_unit(key, value)

                    writer.writerow([key, value, unit, category])

            return filepath

        except Exception as e:
            print(f"Chyba při vytváření CSV exportu: {e}")
            return ""

    def generate_excel_report(
        self, calculation_results: Dict, filename: Optional[str] = None
    ) -> str:
        """
        Generate comprehensive Excel report with multiple sheets.

        Creates an Excel workbook with separate sheets for different
        aspects of the calculation (inputs, results, analysis, etc.).

        Args:
            calculation_results: Complete calculation results
            filename: Optional custom filename

        Returns:
            Path to the generated Excel file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"burner_calculation_report_{timestamp}.xlsx"

        filepath = os.path.join(self.output_dir, filename)

        try:
            with pd.ExcelWriter(filepath, engine="openpyxl") as writer:

                # Sheet 1: Summary
                summary_data = {"Parametr": [], "Hodnota": [], "Jednotka": []}

                # Add key results to summary
                if "burner" in calculation_results:
                    burner = calculation_results["burner"]
                    summary_data["Parametr"].extend(["Výkon hořáku", "Průměr trysky"])
                    summary_data["Hodnota"].extend(
                        [burner.get("power", "N/A"), burner.get("nozzle_diameter", "N/A")]
                    )
                    summary_data["Jednotka"].extend(["kW", "mm"])

                if "chamber" in calculation_results:
                    chamber = calculation_results["chamber"]
                    summary_data["Parametr"].extend(["Objem komory", "Doba zdržení"])
                    summary_data["Hodnota"].extend(
                        [chamber.get("volume", "N/A"), chamber.get("residence_time", "N/A")]
                    )
                    summary_data["Jednotka"].extend(["m³", "s"])

                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name="Shrnutí", index=False)

                # Sheet 2: Input Parameters
                if "inputs" in calculation_results:
                    inputs_data = {
                        "Parametr": list(calculation_results["inputs"].keys()),
                        "Hodnota": list(calculation_results["inputs"].values()),
                    }
                    inputs_df = pd.DataFrame(inputs_data)
                    inputs_df.to_excel(writer, sheet_name="Vstupní parametry", index=False)

                # Sheet 3: Combustion Analysis
                if "combustion" in calculation_results:
                    combustion = calculation_results["combustion"]
                    combustion_data = {"Parametr": [], "Hodnota": [], "Jednotka": []}

                    combustion_params = {
                        "theoretical_air": ("Teoretické množství vzduchu", "m³/m³"),
                        "actual_air": ("Skutečné množství vzduchu", "m³/m³"),
                        "excess_air": ("Přebytek vzduchu", "%"),
                        "heating_value": ("Výhřevnost", "MJ/m³"),
                        "combustion_temp": ("Teplota spalování", "°C"),
                    }

                    for key, (name, unit) in combustion_params.items():
                        if key in combustion:
                            combustion_data["Parametr"].append(name)
                            combustion_data["Hodnota"].append(combustion[key])
                            combustion_data["Jednotka"].append(unit)

                    combustion_df = pd.DataFrame(combustion_data)
                    combustion_df.to_excel(writer, sheet_name="Spalování", index=False)

                # Sheet 4: Burner Design
                if "burner" in calculation_results:
                    burner = calculation_results["burner"]
                    burner_data = {"Parametr": [], "Hodnota": [], "Jednotka": []}

                    burner_params = {
                        "type": ("Typ hořáku", "-"),
                        "power": ("Výkon", "kW"),
                        "nozzle_diameter": ("Průměr trysky", "mm"),
                        "gas_velocity": ("Rychlost plynu", "m/s"),
                        "gas_pressure": ("Tlak plynu", "Pa"),
                    }

                    for key, (name, unit) in burner_params.items():
                        if key in burner:
                            burner_data["Parametr"].append(name)
                            burner_data["Hodnota"].append(burner[key])
                            burner_data["Jednotka"].append(unit)

                    burner_df = pd.DataFrame(burner_data)
                    burner_df.to_excel(writer, sheet_name="Hořák", index=False)

                # Sheet 5: Pressure Losses
                if (
                    "pressure_losses" in calculation_results
                    and "components" in calculation_results["pressure_losses"]
                ):
                    pressure_data = calculation_results["pressure_losses"]["components"]
                    pressure_df = pd.DataFrame(
                        list(pressure_data.items()), columns=["Komponenta", "Tlaková ztráta [Pa]"]
                    )
                    pressure_df.to_excel(writer, sheet_name="Tlakové ztráty", index=False)

                # Sheet 6: Metadata
                if self.report_metadata:
                    metadata_data = {
                        "Atribut": [
                            "ID výpočtu",
                            "Datum a čas",
                            "Verze software",
                            "Projekt",
                            "Uživatel",
                        ],
                        "Hodnota": [
                            self.report_metadata.calculation_id,
                            self.report_metadata.timestamp,
                            self.report_metadata.software_version,
                            self.report_metadata.project_name or "N/A",
                            self.report_metadata.user_name or "N/A",
                        ],
                    }
                    metadata_df = pd.DataFrame(metadata_data)
                    metadata_df.to_excel(writer, sheet_name="Metadata", index=False)

            return filepath

        except Exception as e:
            print(f"Chyba při vytváření Excel zprávy: {e}")
            return ""

    def _determine_unit(self, parameter_name: str, value: Any) -> str:
        """
        Determine appropriate unit for a parameter based on its name.

        Args:
            parameter_name: Name of the parameter
            value: Parameter value

        Returns:
            Appropriate unit string
        """
        parameter_name = parameter_name.lower()

        # Temperature units
        if "temp" in parameter_name or "temperature" in parameter_name:
            return "°C"

        # Pressure units
        if "pressure" in parameter_name or "loss" in parameter_name:
            return "Pa"

        # Power units
        if "power" in parameter_name or "heat" in parameter_name:
            return "kW"

        # Velocity units
        if "velocity" in parameter_name or "speed" in parameter_name:
            return "m/s"

        # Volume units
        if "volume" in parameter_name:
            return "m³"

        # Time units
        if "time" in parameter_name:
            return "s"

        # Diameter/length units
        if "diameter" in parameter_name or "length" in parameter_name:
            return "m"

        # Percentage units
        if "efficiency" in parameter_name or "excess" in parameter_name:
            return "%"

        # Default
        return "-"

    def generate_complete_report(
        self,
        calculation_results: Dict,
        formats: List[str] = ["txt", "csv", "xlsx"],
        project_name: str = None,
        user_name: str = None,
    ) -> Dict[str, str]:
        """
        Generate complete report in all requested formats.

        This is the main method for generating comprehensive reports
        including all calculation results and analysis.

        Args:
            calculation_results: Complete results from all calculation modules
            formats: List of output formats ('txt', 'csv', 'xlsx')
            project_name: Name of the project
            user_name: Name of the user

        Returns:
            Dictionary with paths to generated report files
        """
        # Set metadata
        self.set_metadata(project_name=project_name, user_name=user_name)

        generated_files = {}

        try:
            # Generate text report
            if "txt" in formats:
                txt_file = self.generate_text_report(calculation_results)
                if txt_file:
                    generated_files["txt"] = txt_file

            # Generate CSV export
            if "csv" in formats:
                csv_file = self.generate_csv_export(calculation_results)
                if csv_file:
                    generated_files["csv"] = csv_file

            # Generate Excel report
            if "xlsx" in formats:
                excel_file = self.generate_excel_report(calculation_results)
                if excel_file:
                    generated_files["xlsx"] = excel_file

            print(f"Vygenerováno {len(generated_files)} zpráv v požadovaných formátech")
            return generated_files

        except Exception as e:
            print(f"Chyba při generování kompletní zprávy: {e}")
            return generated_files
