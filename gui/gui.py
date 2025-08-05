# gui/gui.py

"""
gui/gui.py

Comprehensive tkinter GUI application for gas burner and combustion chamber design.
Provides complete user interface with tabs for different calculation sections,
input validation, file I/O, and results export functionality.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os
import sys
import traceback
import csv
import pandas as pd
from datetime import datetime
import threading

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

try:
    from combustion import CombustionCalculator
    from burner_design import BurnerDesigner
    from chamber_design import ChamberDesigner
    from radiation import RadiationCalculator
    from pressure_losses import PressureLossCalculator
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)


class BurnerCalculatorGUI:
    """
    Main GUI application for burner calculator.

    This class provides a comprehensive tkinter-based interface for gas burner
    and combustion chamber design calculations including input validation,
    file operations, and results export functionality.

    Attributes:
        root (tk.Tk): Main window
        notebook (ttk.Notebook): Tab container
        input_data (dict): Current input parameters
        results (dict): Calculation results from all modules
        calculators (dict): Instances of calculation classes
    """

    def __init__(self, root: tk.Tk):
        """
        Initialize the GUI application.

        Args:
            root (tk.Tk): Main tkinter window
        """
        self.root = root
        self.root.title("Návrh plynového hořáku a spalovací komory")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)

        # Initialize data storage
        self.input_data = {}
        self.results = {}
        self.validation_errors = []

        # Initialize calculators
        try:
            self.calculators = {
                "combustion": CombustionCalculator(),
                "burner": BurnerDesigner(),
                "chamber": ChamberDesigner(),
                "radiation": RadiationCalculator(),
                "pressure": PressureLossCalculator(),
            }
        except Exception as e:
            messagebox.showerror(
                "Chyba inicializace", f"Chyba při načítání výpočetních modulů: {e}"
            )
            return

        # Create GUI elements
        self.create_widgets()
        self.setup_menu()
        self.load_default_values()

    def create_widgets(self):
        """Create and arrange all GUI widgets."""
        # Create main frame with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Title label
        title_label = ttk.Label(
            main_frame,
            text="Návrh plynového hořáku a spalovací komory",
            font=("Arial", 16, "bold"),
        )
        title_label.grid(row=0, column=0, pady=(0, 10))

        # Create notebook (tab container)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create tabs
        self.create_input_tab()
        self.create_combustion_tab()
        self.create_burner_tab()
        self.create_chamber_tab()
        self.create_radiation_tab()
        self.create_pressure_tab()
        self.create_results_tab()

        # Create control buttons
        self.create_control_buttons(main_frame)

    def create_input_tab(self):
        """Create input parameters tab."""
        input_frame = ttk.Frame(self.notebook)
        self.notebook.add(input_frame, text="Vstupní parametry")

        # Create scrollable frame
        canvas = tk.Canvas(input_frame)
        scrollbar = ttk.Scrollbar(input_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Input fields storage
        self.input_vars = {}

        # Fuel selection section
        fuel_frame = ttk.LabelFrame(scrollable_frame, text="Palivo", padding="10")
        fuel_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(fuel_frame, text="Typ paliva:").grid(
            row=0, column=0, sticky="w", padx=(0, 10)
        )
        self.input_vars["fuel_type"] = ttk.Combobox(
            fuel_frame,
            values=list(self.calculators["combustion"].get_available_fuels()),
            state="readonly",
        )
        self.input_vars["fuel_type"].grid(row=0, column=1, sticky="ew", padx=(0, 10))
        self.input_vars["fuel_type"].set("natural_gas")

        # Fuel flow parameters
        flow_frame = ttk.LabelFrame(scrollable_frame, text="Průtoky", padding="10")
        flow_frame.pack(fill="x", padx=5, pady=5)

        # Fuel flow rate
        ttk.Label(flow_frame, text="Hmotnostní průtok paliva [kg/s]:").grid(
            row=0, column=0, sticky="w"
        )
        self.input_vars["fuel_flow_rate"] = ttk.Entry(flow_frame)
        self.input_vars["fuel_flow_rate"].grid(
            row=0, column=1, sticky="ew", padx=(10, 0)
        )

        # Excess air ratio
        ttk.Label(flow_frame, text="Koeficient přebytku vzduchu [-]:").grid(
            row=1, column=0, sticky="w"
        )
        self.input_vars["excess_air_ratio"] = ttk.Entry(flow_frame)
        self.input_vars["excess_air_ratio"].grid(
            row=1, column=1, sticky="ew", padx=(10, 0)
        )

        # Operating conditions
        conditions_frame = ttk.LabelFrame(
            scrollable_frame, text="Provozní podmínky", padding="10"
        )
        conditions_frame.pack(fill="x", padx=5, pady=5)

        # Ambient temperature
        ttk.Label(conditions_frame, text="Teplota okolí [°C]:").grid(
            row=0, column=0, sticky="w"
        )
        self.input_vars["ambient_temperature"] = ttk.Entry(conditions_frame)
        self.input_vars["ambient_temperature"].grid(
            row=0, column=1, sticky="ew", padx=(10, 0)
        )

        # Ambient pressure
        ttk.Label(conditions_frame, text="Tlak okolí [Pa]:").grid(
            row=1, column=0, sticky="w"
        )
        self.input_vars["ambient_pressure"] = ttk.Entry(conditions_frame)
        self.input_vars["ambient_pressure"].grid(
            row=1, column=1, sticky="ew", padx=(10, 0)
        )

        # Burner design parameters
        burner_frame = ttk.LabelFrame(
            scrollable_frame, text="Parametry hořáku", padding="10"
        )
        burner_frame.pack(fill="x", padx=5, pady=5)

        # Maximum gas velocity
        ttk.Label(burner_frame, text="Maximální rychlost plynu [m/s]:").grid(
            row=0, column=0, sticky="w"
        )
        self.input_vars["max_gas_velocity"] = ttk.Entry(burner_frame)
        self.input_vars["max_gas_velocity"].grid(
            row=0, column=1, sticky="ew", padx=(10, 0)
        )

        # Supply pressure
        ttk.Label(burner_frame, text="Tlak přívodu plynu [Pa]:").grid(
            row=1, column=0, sticky="w"
        )
        self.input_vars["supply_pressure"] = ttk.Entry(burner_frame)
        self.input_vars["supply_pressure"].grid(
            row=1, column=1, sticky="ew", padx=(10, 0)
        )

        # Chamber design parameters
        chamber_frame = ttk.LabelFrame(
            scrollable_frame, text="Parametry komory", padding="10"
        )
        chamber_frame.pack(fill="x", padx=5, pady=5)

        # Required heat output
        ttk.Label(chamber_frame, text="Požadovaný tepelný výkon [kW]:").grid(
            row=0, column=0, sticky="w"
        )
        self.input_vars["heat_output"] = ttk.Entry(chamber_frame)
        self.input_vars["heat_output"].grid(row=0, column=1, sticky="ew", padx=(10, 0))

        # Maximum chamber temperature
        ttk.Label(chamber_frame, text="Maximální teplota komory [°C]:").grid(
            row=1, column=0, sticky="w"
        )
        self.input_vars["max_chamber_temp"] = ttk.Entry(chamber_frame)
        self.input_vars["max_chamber_temp"].grid(
            row=1, column=1, sticky="ew", padx=(10, 0)
        )

        # Note: Heat release density is calculated automatically in burner design

        # Configure column weights
        for frame in [
            fuel_frame,
            flow_frame,
            conditions_frame,
            burner_frame,
            chamber_frame,
        ]:
            frame.columnconfigure(1, weight=1)

    def create_combustion_tab(self):
        """Create combustion calculations results tab."""
        combustion_frame = ttk.Frame(self.notebook)
        self.notebook.add(combustion_frame, text="Výpočty spalování")

        # Results display
        self.combustion_text = scrolledtext.ScrolledText(
            combustion_frame, height=20, font=("Courier", 10)
        )
        self.combustion_text.pack(fill="both", expand=True, padx=10, pady=10)

    def create_burner_tab(self):
        """Create burner design results tab."""
        burner_frame = ttk.Frame(self.notebook)
        self.notebook.add(burner_frame, text="Návrh hořáku")

        # Results display
        self.burner_text = scrolledtext.ScrolledText(
            burner_frame, height=20, font=("Courier", 10)
        )
        self.burner_text.pack(fill="both", expand=True, padx=10, pady=10)

    def create_chamber_tab(self):
        """Create chamber design results tab."""
        chamber_frame = ttk.Frame(self.notebook)
        self.notebook.add(chamber_frame, text="Návrh komory")

        # Results display
        self.chamber_text = scrolledtext.ScrolledText(
            chamber_frame, height=20, font=("Courier", 10)
        )
        self.chamber_text.pack(fill="both", expand=True, padx=10, pady=10)

    def create_radiation_tab(self):
        """Create radiation transfer results tab."""
        radiation_frame = ttk.Frame(self.notebook)
        self.notebook.add(radiation_frame, text="Radiační přenos")

        # Results display
        self.radiation_text = scrolledtext.ScrolledText(
            radiation_frame, height=20, font=("Courier", 10)
        )
        self.radiation_text.pack(fill="both", expand=True, padx=10, pady=10)

    def create_pressure_tab(self):
        """Create pressure losses results tab."""
        pressure_frame = ttk.Frame(self.notebook)
        self.notebook.add(pressure_frame, text="Tlakové ztráty")

        # Results display
        self.pressure_text = scrolledtext.ScrolledText(
            pressure_frame, height=20, font=("Courier", 10)
        )
        self.pressure_text.pack(fill="both", expand=True, padx=10, pady=10)

    def create_results_tab(self):
        """Create summary results tab."""
        results_frame = ttk.Frame(self.notebook)
        self.notebook.add(results_frame, text="Výsledky")

        # Results display
        self.results_text = scrolledtext.ScrolledText(
            results_frame, height=20, font=("Courier", 10)
        )
        self.results_text.pack(fill="both", expand=True, padx=10, pady=10)

    def create_control_buttons(self, parent):
        """Create control buttons at the bottom of the window."""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, pady=(10, 0), sticky="ew")

        # Progress bar
        self.progress = ttk.Progressbar(button_frame, mode="indeterminate")
        self.progress.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Buttons
        ttk.Button(
            button_frame, text="Načíst vstup", command=self.load_input_file
        ).pack(side="right", padx=(0, 5))
        ttk.Button(
            button_frame, text="Uložit vstup", command=self.save_input_file
        ).pack(side="right", padx=(0, 5))
        ttk.Button(
            button_frame, text="Exportovat výsledky", command=self.export_results
        ).pack(side="right", padx=(0, 5))
        ttk.Button(
            button_frame,
            text="Spustit výpočet",
            command=self.run_calculations,
            style="Accent.TButton",
        ).pack(side="right", padx=(0, 5))

    def setup_menu(self):
        """Setup application menu."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Soubor", menu=file_menu)
        file_menu.add_command(label="Nový projekt", command=self.new_project)
        file_menu.add_command(label="Načíst vstup...", command=self.load_input_file)
        file_menu.add_command(label="Uložit vstup...", command=self.save_input_file)
        file_menu.add_separator()
        file_menu.add_command(
            label="Exportovat výsledky...", command=self.export_results
        )
        file_menu.add_separator()
        file_menu.add_command(label="Ukončit", command=self.root.quit)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Nástroje", menu=tools_menu)
        tools_menu.add_command(label="Validovat vstup", command=self.validate_input)
        tools_menu.add_command(
            label="Výchozí hodnoty", command=self.load_default_values
        )

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Nápověda", menu=help_menu)
        help_menu.add_command(label="O aplikaci", command=self.show_about)

    def load_default_values(self):
        """Load default input values."""
        defaults = {
            "fuel_type": "natural_gas",
            "fuel_flow_rate": "0.002",
            "excess_air_ratio": "1.2",
            "ambient_temperature": "20",
            "ambient_pressure": "101325",
            "max_gas_velocity": "50",
            "supply_pressure": "3000",
            "heat_output": "100",
            "max_chamber_temp": "1200",
        }

        for key, value in defaults.items():
            if key in self.input_vars:
                try:
                    # Try using set method (for Combobox)
                    self.input_vars[key].set(value)
                except AttributeError:
                    # Fall back to delete/insert (for Entry)
                    self.input_vars[key].delete(0, tk.END)
                    self.input_vars[key].insert(0, value)

    def validate_input(self) -> bool:
        """
        Validate all input parameters.

        Returns:
            bool: True if all inputs are valid, False otherwise
        """
        self.validation_errors = []

        try:
            # Get input values
            self.collect_input_data()

            # Validate fuel flow rate
            if self.input_data["fuel_flow_rate"] <= 0:
                self.validation_errors.append(
                    "Hmotnostní průtok paliva musí být větší než nula"
                )

            # Validate excess air ratio
            if self.input_data["excess_air_ratio"] < 1.0:
                self.validation_errors.append(
                    "Koeficient přebytku vzduchu musí být ≥ 1.0"
                )

            # Validate temperatures
            if (
                self.input_data["ambient_temperature"] < -50
                or self.input_data["ambient_temperature"] > 100
            ):
                self.validation_errors.append(
                    "Teplota okolí musí být mezi -50°C a 100°C"
                )

            if (
                self.input_data["max_chamber_temp"] < 500
                or self.input_data["max_chamber_temp"] > 2000
            ):
                self.validation_errors.append(
                    "Maximální teplota komory musí být mezi 500°C a 2000°C"
                )

            # Validate pressures
            if (
                self.input_data["ambient_pressure"] < 50000
                or self.input_data["ambient_pressure"] > 200000
            ):
                self.validation_errors.append(
                    "Tlak okolí musí být mezi 50 kPa a 200 kPa"
                )

            if self.input_data["supply_pressure"] < 1000:
                self.validation_errors.append(
                    "Tlak přívodu plynu musí být alespoň 1000 Pa"
                )

            # Validate gas velocity
            if (
                self.input_data["max_gas_velocity"] < 1
                or self.input_data["max_gas_velocity"] > 200
            ):
                self.validation_errors.append(
                    "Maximální rychlost plynu musí být mezi 1 a 200 m/s"
                )

            # Validate heat output
            if self.input_data["heat_output"] <= 0:
                self.validation_errors.append(
                    "Požadovaný tepelný výkon musí být větší než nula"
                )

        except ValueError as e:
            self.validation_errors.append(f"Chyba při převodu číselných hodnot: {e}")
        except Exception as e:
            self.validation_errors.append(f"Neočekávaná chyba při validaci: {e}")

        # Show validation results
        if self.validation_errors:
            error_message = "Nalezeny následující chyby ve vstupních datech:\n\n"
            error_message += "\n".join(
                [f"• {error}" for error in self.validation_errors]
            )
            messagebox.showerror("Chyby ve vstupních datech", error_message)
            return False
        else:
            return True

    def collect_input_data(self):
        """Collect all input data from GUI fields."""
        self.input_data = {}

        # Get string values
        self.input_data["fuel_type"] = self.input_vars["fuel_type"].get()

        # Get numeric values with conversion
        numeric_fields = [
            "fuel_flow_rate",
            "excess_air_ratio",
            "ambient_temperature",
            "ambient_pressure",
            "max_gas_velocity",
            "supply_pressure",
            "heat_output",
            "max_chamber_temp",
        ]

        for field in numeric_fields:
            value_str = self.input_vars[field].get().strip()
            if not value_str:
                raise ValueError(f"Pole '{field}' je prázdné")

            try:
                self.input_data[field] = float(value_str)
            except ValueError:
                raise ValueError(
                    f"Neplatná číselná hodnota v poli '{field}': {value_str}"
                )

    def run_calculations(self):
        """Run all calculations in separate thread."""
        # Validate input first
        if not self.validate_input():
            return

        # Start progress indicator
        self.progress.start()

        # Disable calculate button
        for child in self.root.winfo_children():
            if isinstance(child, ttk.Frame):
                for subchild in child.winfo_children():
                    if isinstance(subchild, ttk.Button) and "Spustit výpočet" in str(
                        subchild
                    ):
                        subchild.configure(state="disabled")

        # Run calculations in separate thread
        calc_thread = threading.Thread(target=self._perform_calculations)
        calc_thread.daemon = True
        calc_thread.start()

    def _perform_calculations(self):
        """Perform all calculations (runs in separate thread)."""
        try:
            # Clear previous results
            self.results = {}

            # Combustion calculations
            self.root.after(0, self._update_status, "Výpočet spalování...")
            combustion_calc = self.calculators["combustion"]
            combustion_results = combustion_calc.calculate_combustion_products(
                self.input_data["fuel_type"],
                self.input_data["fuel_flow_rate"],
                self.input_data["excess_air_ratio"],
            )
            self.results["combustion"] = combustion_results

            # Burner design calculations
            self.root.after(0, self._update_status, "Návrh hořáku...")
            burner_calc = self.calculators["burner"]
            burner_results = burner_calc.design_burner(
                self.input_data["fuel_type"],
                combustion_results.heat_release_rate,
                self.input_data["supply_pressure"],
                self.input_data["max_gas_velocity"],
                self.input_data["excess_air_ratio"],
            )
            self.results["burner"] = burner_results

            # Chamber design calculations
            self.root.after(0, self._update_status, "Návrh komory...")
            chamber_calc = self.calculators["chamber"]
            chamber_results = chamber_calc.design_chamber(
                fuel_type=self.input_data["fuel_type"],
                required_power=self.input_data["heat_output"] * 1000,  # Convert kW to W
                target_residence_time=0.8,  # Realistic residence time
                # Convert °C to K
                ambient_temperature=self.input_data["ambient_temperature"] + 273.15,
            )
            self.results["chamber"] = chamber_results

            # Radiation calculations
            self.root.after(0, self._update_status, "Výpočet radiace...")
            radiation_calc = self.calculators["radiation"]
            radiation_results = radiation_calc.calculate_flame_radiation(
                flame_temperature=combustion_results.adiabatic_flame_temperature,
                chamber_wall_temperature=chamber_results.chamber_wall_temperature,
                chamber_diameter=chamber_results.chamber_diameter,
                chamber_length=chamber_results.chamber_length,
                fuel_type=self.input_data["fuel_type"],
                excess_air_ratio=combustion_results.excess_air_ratio,
            )
            self.results["radiation"] = radiation_results

            # Pressure loss calculations
            self.root.after(0, self._update_status, "Výpočet tlakových ztrát...")
            pressure_calc = self.calculators["pressure"]

            # Create sample pipe segments and fittings for demonstration
            from src.pressure_losses import PipeSegment

            sample_pipe_segments = [
                PipeSegment(
                    length=chamber_results.chamber_length
                    + 2.0,  # Chamber + connection pipes
                    diameter=burner_results.burner_diameter,
                    roughness=0.000045,  # Steel pipe
                    material="steel_new",
                    elevation_change=0.5,  # Small elevation change
                )
            ]

            sample_fittings = pressure_calc.create_standard_fittings_list(
                burner_results.burner_diameter
            )

            # Calculate gas density from combustion results
            fuel_props = combustion_calc.get_fuel_properties(
                self.input_data["fuel_type"]
            )
            molecular_weight = (
                fuel_props["properties"]["molecular_weight"] / 1000
            )  # g/mol to kg/mol
            gas_constant = combustion_calc.constants["universal_gas_constant"]
            gas_density = (101325 * molecular_weight) / (
                gas_constant * 573
            )  # At ~300°C

            pressure_results = pressure_calc.calculate_system_pressure_losses(
                pipe_segments=sample_pipe_segments,
                fittings=sample_fittings,
                mass_flow_rate=combustion_results.flue_gas_flow_rate,
                gas_density=gas_density,
                burner_results=burner_results,
            )
            self.results["pressure"] = pressure_results

            # Update GUI with results
            self.root.after(0, self._display_all_results)

        except Exception as e:
            error_msg = f"Chyba při výpočtu: {str(e)}\n\n{traceback.format_exc()}"
            self.root.after(0, lambda: messagebox.showerror("Chyba výpočtu", error_msg))

        finally:
            # Stop progress and re-enable button
            self.root.after(0, self._calculation_finished)

    def _update_status(self, message: str):
        """Update status message (called from main thread)."""
        # You could add a status label here if desired
        pass

    def _calculation_finished(self):
        """Called when calculations are finished."""
        self.progress.stop()

        # Re-enable calculate button
        for child in self.root.winfo_children():
            if isinstance(child, ttk.Frame):
                for subchild in child.winfo_children():
                    if isinstance(subchild, ttk.Button) and "Spustit výpočet" in str(
                        subchild
                    ):
                        subchild.configure(state="normal")

    def _display_all_results(self):
        """Display all calculation results in respective tabs."""
        try:
            if "combustion" in self.results:
                self._display_combustion_results()

            if "burner" in self.results:
                self._display_burner_results()

            if "chamber" in self.results:
                self._display_chamber_results()

            if "radiation" in self.results:
                self._display_radiation_results()

            if "pressure" in self.results:
                self._display_pressure_results()

            self._display_summary_results()
            
            # Automatically switch to Results tab after calculation
            for i in range(self.notebook.index("end")):
                tab_text = self.notebook.tab(i, "text")
                if "Výsledky" in tab_text:
                    self.notebook.select(i)
                    break

        except Exception as e:
            messagebox.showerror(
                "Chyba zobrazení", f"Chyba při zobrazování výsledků: {e}"
            )

    def _display_combustion_results(self):
        """Display combustion calculation results."""
        results = self.results["combustion"]

        text = "VÝSLEDKY VÝPOČTU SPALOVÁNÍ\n"
        text += "=" * 50 + "\n\n"

        # Základní parametry paliva
        text += f"Typ paliva: {self.input_data['fuel_type']}\n"
        text += f"Koeficient přebytku vzduchu: {self.input_data['excess_air_ratio']} [-]\n\n"

        # Hmotnostní průtoky
        text += "HMOTNOSTNÍ PRŮTOKY:\n"
        text += "-" * 25 + "\n"
        text += f"Palivo: {results.fuel_flow_rate:.6f} kg/s ({results.fuel_flow_rate*3600:.3f} kg/h)\n"
        text += f"Vzduch: {results.air_flow_rate:.6f} kg/s ({results.air_flow_rate*3600:.3f} kg/h)\n"
        text += f"Spaliny: {results.flue_gas_flow_rate:.6f} kg/s ({results.flue_gas_flow_rate*3600:.3f} kg/h)\n"
        text += f"Celkový průtok (palivo+vzduch): {results.fuel_flow_rate + results.air_flow_rate:.6f} kg/s\n\n"

        # Poměry a stechiometrie
        text += "SPALOVACÍ POMĚRY:\n"
        text += "-" * 20 + "\n"
        text += f"Teoretická potřeba vzduchu: {results.air_flow_rate/results.fuel_flow_rate:.1f} kg vzduchu/kg paliva\n"
        text += f"Množství vzniklých spalin: {results.flue_gas_flow_rate/results.fuel_flow_rate:.1f} kg spalin/kg paliva\n\n"

        text += f"Koeficient přebytku vzduchu: {results.excess_air_ratio:.2f} [-]\n"
        text += (
            f"Adiabatická teplota plamene: {results.adiabatic_flame_temperature:.1f} K "
        )
        text += f"({results.adiabatic_flame_temperature-273.15:.1f} °C)\n"
        text += f"Tepelný výkon: {results.heat_release_rate/1000:.1f} kW\n\n"

        text += "Složení spalin:\n"
        text += f"  CO₂: {results.co2_volume_percent:.2f} % obj.\n"
        text += f"  O₂: {results.o2_volume_percent:.2f} % obj.\n"

        self.combustion_text.delete(1.0, tk.END)
        self.combustion_text.insert(1.0, text)

    def _display_burner_results(self):
        """Display burner design results."""
        results = self.results["burner"]

        text = "VÝSLEDKY NÁVRHU HOŘÁKU\n"
        text += "=" * 50 + "\n\n"

        # Geometrické rozměry
        text += "GEOMETRICKÉ ROZMĚRY:\n"
        text += "-" * 25 + "\n"
        text += f"Průměr hořáku: {results.burner_diameter*1000:.1f} mm\n"
        text += f"Plocha hořáku: {results.burner_area*1000000:.1f} mm² ({results.burner_area:.6f} m²)\n"
        text += f"Délka hořáku: {results.burner_length*1000:.0f} mm\n"
        text += f"Poměr L/D: {results.burner_length/results.burner_diameter:.1f} [-]\n\n"

        # Provozní parametry
        text += "PROVOZNÍ PARAMETRY:\n"
        text += "-" * 23 + "\n"
        text += f"Rychlost plynu: {results.gas_velocity:.1f} m/s\n"
        text += f"Hustota tepelného toku: {results.heat_release_density/1e6:.1f} MW/m²\n"
        text += f"Tepelný výkon: {self.input_data['heat_output']} kW\n"
        text += f"Specifický výkon: {float(self.input_data['heat_output'])*1000/results.burner_area:.0f} W/m²\n\n"

        # Tlakové parametry
        text += "TLAKOVÉ PARAMETRY:\n"
        text += "-" * 21 + "\n"
        text += f"Tlaková ztráta hořáku: {results.burner_pressure_drop:.0f} Pa\n"
        text += f"Požadovaný tlak plynu: {results.required_supply_pressure:.0f} Pa\n"
        text += f"Dostupný tlak plynu: {self.input_data['supply_pressure']} Pa\n"
        text += f"Rezerva tlaku: {float(self.input_data['supply_pressure']) - results.required_supply_pressure:.0f} Pa\n\n"

        # Plamene
        text += "PARAMETRY PLAMENE:\n"
        text += "-" * 20 + "\n"
        text += f"Odhadovaná délka plamene: {results.flame_length*1000:.0f} mm\n"
        text += f"Poměr plamene k hořáku: {results.flame_length/results.burner_length:.1f} [-]\n\n"
        )

        text += f"Hustota tepelného toku: {results.heat_release_density/1000:.0f} kW/m²\n"

        self.burner_text.delete(1.0, tk.END)
        self.burner_text.insert(1.0, text)

    def _display_chamber_results(self):
        """Display chamber design results."""
        results = self.results["chamber"]

        text = "VÝSLEDKY NÁVRHU SPALOVACÍ KOMORY\n"
        text += "=" * 50 + "\n\n"

        # Geometrické rozměry komory
        text += "GEOMETRICKÉ ROZMĚRY:\n"
        text += "-" * 25 + "\n"
        text += f"Objem komory: {results.chamber_volume:.3f} m³ ({results.chamber_volume*1000:.0f} litrů)\n"
        text += f"Délka komory: {results.chamber_length:.2f} m ({results.chamber_length*1000:.0f} mm)\n"
        text += f"Průměr komory: {results.chamber_diameter:.2f} m ({results.chamber_diameter*1000:.0f} mm)\n"
        text += f"Povrch komory: {results.chamber_surface_area:.2f} m²\n"
        text += f"Poměr L/D komory: {results.chamber_length/results.chamber_diameter:.1f} [-]\n\n"

        # Tepelné parametry
        text += "TEPELNÉ PARAMETRY:\n"  
        text += "-" * 21 + "\n"
        text += f"Doba zdržení spalin: {results.residence_time:.3f} s\n"
        text += f"Objemová hustota výkonu: {results.volume_heat_release_rate/1e6:.1f} MW/m³\n"
        text += f"Teplota stěny komory: {results.wall_temperature:.0f} K ({results.wall_temperature-273.15:.0f} °C)\n"
        text += f"Tepelná účinnost: {results.thermal_efficiency:.1f} %\n\n"

        # Tepelné ztráty
        text += "ANALÝZA TEPELNÝCH ZTRÁT:\n"
        text += "-" * 27 + "\n"
        text += f"Rychlost ztrát tepla: {results.heat_loss_rate/1000:.1f} kW\n"
        text += f"Součinitel přestupu tepla: {results.heat_transfer_coefficient:.1f} W/m²·K\n"
        text += f"Podíl ztrát z celkového výkonu: {results.heat_loss_rate/(float(self.input_data['heat_output'])*1000)*100:.1f} %\n\n"

        text += f"Hustota tepelného toku: {results.volume_heat_release_rate/1000:.0f} kW/m³\n"
        text += f"Součinitel přestupu tepla: {results.heat_transfer_coefficient:.1f} W/(m²·K)\n"

        self.chamber_text.delete(1.0, tk.END)
        self.chamber_text.insert(1.0, text)

    def _display_radiation_results(self):
        """Display radiation transfer results."""
        results = self.results["radiation"]

        text = "VÝSLEDKY VÝPOČTU RADIAČNÍHO PŘENOSU TEPLA\n"
        text += "=" * 50 + "\n\n"

        text += f"Radiační tepelný tok: {results.total_radiation_heat_transfer/1000:.1f} kW\n"
        text += f"Emisivita plamene: {results.flame_emissivity:.3f} [-]\n"
        text += f"Emisivita stěny: {results.wall_emissivity:.3f} [-]\n\n"

        text += f"Tepelný tok plamen → stěna: {results.flame_to_wall_heat_transfer/1000:.1f} kW\n"
        text += f"Tepelný tok stěna → okolí: {results.wall_to_ambient_heat_transfer/1000:.1f} kW\n\n"

        text += f"Střední beam length: {results.mean_beam_length:.3f} m\n"
        text += f"Účinnost radiačního přenosu: {results.radiation_efficiency:.1f} %\n"

        self.radiation_text.delete(1.0, tk.END)
        self.radiation_text.insert(1.0, text)

    def _display_pressure_results(self):
        """Display pressure loss results."""
        results = self.results["pressure"]

        text = "VÝSLEDKY VÝPOČTU TLAKOVÝCH ZTRÁT\n"
        text += "=" * 50 + "\n\n"

        text += f"Celková tlaková ztráta: {results.total_pressure_loss:.0f} Pa\n\n"

        text += "Jednotlivé tlakové ztráty:\n"
        text += f"  Hořák: {results.burner_pressure_loss:.0f} Pa\n"
        text += f"  Třecí ztráty v potrubí: {results.friction_losses:.0f} Pa\n"
        text += f"  Místní odpory: {results.minor_losses:.0f} Pa\n"
        text += f"  Výškové ztráty: {results.elevation_losses:.0f} Pa\n\n"

        text += f"Rychlostní tlak: {results.velocity_pressure:.1f} Pa\n"
        text += f"Reynoldsovo číslo: {results.reynolds_number:.0f} [-]\n"
        text += f"Součinitel tření: {results.friction_factor:.6f} [-]\n"

        self.pressure_text.delete(1.0, tk.END)
        self.pressure_text.insert(1.0, text)

    def _display_summary_results(self):
        """Display summary of all results."""
        text = "SOUHRNNÉ VÝSLEDKY NÁVRHU\n"
        text += "=" * 60 + "\n\n"

        text += f"Datum výpočtu: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n"

        # Input summary
        text += "VSTUPNÍ PARAMETRY:\n"
        text += "-" * 30 + "\n"
        text += f"Typ paliva: {self.input_data['fuel_type']}\n"
        text += f"Hmotnostní průtok paliva: {self.input_data['fuel_flow_rate']} kg/s\n"
        text += (
            f"Koeficient přebytku vzduchu: {self.input_data['excess_air_ratio']} [-]\n"
        )
        text += f"Požadovaný tepelný výkon: {self.input_data['heat_output']} kW\n\n"

        # Key results summary
        if all(
            key in self.results
            for key in ["combustion", "burner", "chamber", "radiation", "pressure"]
        ):
            text += "KLÍČOVÉ VÝSLEDKY:\n"
            text += "-" * 30 + "\n"

            # Combustion
            combustion = self.results["combustion"]
            text += (
                f"Skutečný tepelný výkon: {combustion.heat_release_rate/1000:.1f} kW\n"
            )
            text += f"Průtok vzduchu: {combustion.air_flow_rate:.6f} kg/s\n"
            text += f"Teplota plamene: {combustion.adiabatic_flame_temperature-273.15:.0f} °C\n\n"

            # Burner
            burner = self.results["burner"]
            text += f"Průměr hořáku: {burner.burner_diameter*1000:.1f} mm\n"
            text += f"Délka hořáku: {burner.burner_length*1000:.0f} mm\n"
            text += f"Rychlost plynu: {burner.gas_velocity:.1f} m/s\n\n"

            # Chamber
            chamber = self.results["chamber"]
            text += f"Objem komory: {chamber.chamber_volume:.3f} m³\n"
            text += f"Rozměry komory: ⌀{chamber.chamber_diameter*1000:.0f} × "
            text += f"{chamber.chamber_length*1000:.0f} mm\n"
            text += f"Doba zdržení: {chamber.residence_time:.3f} s\n\n"

            # Pressure
            pressure = self.results["pressure"]
            text += f"Celková tlaková ztráta: {pressure.total_pressure_loss:.0f} Pa\n"
            text += f"Požadovaný přítlak: {burner.required_supply_pressure:.0f} Pa\n\n"

            # Radiation
            radiation = self.results["radiation"]
            text += (
                f"Radiační tepelný tok: {radiation.total_radiation_heat_transfer/1000:.1f} kW\n"
            )

        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, text)

    def load_input_file(self):
        """Load input parameters from JSON file."""
        filename = filedialog.askopenfilename(
            title="Načíst vstupní parametry",
            filetypes=[("JSON soubory", "*.json"), ("Všechny soubory", "*.*")],
        )

        if filename:
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Load values into GUI fields
                for key, value in data.items():
                    if key in self.input_vars:
                        if isinstance(self.input_vars[key], ttk.Combobox):
                            self.input_vars[key].set(str(value))
                        else:
                            self.input_vars[key].delete(0, tk.END)
                            self.input_vars[key].insert(0, str(value))

                messagebox.showinfo(
                    "Úspěch", f"Vstupní parametry načteny ze souboru:\n{filename}"
                )

            except Exception as e:
                messagebox.showerror("Chyba", f"Chyba při načítání souboru:\n{e}")

    def save_input_file(self):
        """Save current input parameters to JSON file."""
        filename = filedialog.asksaveasfilename(
            title="Uložit vstupní parametry",
            defaultextension=".json",
            filetypes=[("JSON soubory", "*.json"), ("Všechny soubory", "*.*")],
        )

        if filename:
            try:
                self.collect_input_data()

                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(self.input_data, f, indent=2, ensure_ascii=False)

                messagebox.showinfo(
                    "Úspěch", f"Vstupní parametry uloženy do souboru:\n{filename}"
                )

            except Exception as e:
                messagebox.showerror("Chyba", f"Chyba při ukládání souboru:\n{e}")

    def export_results(self):
        """Export calculation results to various formats."""
        if not self.results:
            messagebox.showwarning("Varování", "Nejprve spusťte výpočet")
            return

        # Ask for export format
        ExportDialog(self.root, self.results, self.input_data)

    def new_project(self):
        """Start new project with default values."""
        result = messagebox.askyesno(
            "Nový projekt",
            "Opravdu chcete začít nový projekt?\n"
            "Všechny neusložené změny budou ztraceny.",
        )
        if result:
            self.load_default_values()
            self.results = {}

            # Clear all result displays
            for text_widget in [
                self.combustion_text,
                self.burner_text,
                self.chamber_text,
                self.radiation_text,
                self.pressure_text,
                self.results_text,
            ]:
                text_widget.delete(1.0, tk.END)

    def show_about(self):
        """Show about dialog."""
        about_text = """Návrh plynového hořáku a spalovací komory

Verze: 1.0
Autor: Aplikace pro technický výpočet

Aplikace umožňuje komplexní návrh plynového hořáku
a spalovací komory včetně výpočtu:
• Spalovacích procesů
• Dimenzování hořáku
• Návrhu spalovací komory
• Radiačního přenosu tepla
• Tlakových ztrát

Podporované formáty exportu:
• TXT, CSV, Excel
• Grafy: PDF, PNG, JPEG"""

        messagebox.showinfo("O aplikaci", about_text)


class ExportDialog:
    """Dialog for exporting results in various formats."""

    def __init__(self, parent, results: dict, input_data: dict):
        """
        Initialize export dialog.

        Args:
            parent: Parent window
            results (dict): Calculation results
            input_data (dict): Input parameters
        """
        self.results = results
        self.input_data = input_data

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Export výsledků")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.create_export_widgets()

    def create_export_widgets(self):
        """Create export dialog widgets."""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Format selection
        format_frame = ttk.LabelFrame(main_frame, text="Formát exportu", padding="10")
        format_frame.pack(fill="x", pady=(0, 10))

        self.format_var = tk.StringVar(value="txt")
        ttk.Radiobutton(
            format_frame, text="TXT soubor", variable=self.format_var, value="txt"
        ).pack(anchor="w")
        ttk.Radiobutton(
            format_frame, text="CSV soubor", variable=self.format_var, value="csv"
        ).pack(anchor="w")
        ttk.Radiobutton(
            format_frame, text="Excel soubor", variable=self.format_var, value="excel"
        ).pack(anchor="w")

        # Content selection
        content_frame = ttk.LabelFrame(main_frame, text="Obsah exportu", padding="10")
        content_frame.pack(fill="x", pady=(0, 10))

        self.include_input = tk.BooleanVar(value=True)
        self.include_results = tk.BooleanVar(value=True)
        self.include_detailed = tk.BooleanVar(value=False)

        ttk.Checkbutton(
            content_frame, text="Vstupní parametry", variable=self.include_input
        ).pack(anchor="w")
        ttk.Checkbutton(
            content_frame, text="Výsledky výpočtů", variable=self.include_results
        ).pack(anchor="w")
        ttk.Checkbutton(
            content_frame, text="Detailní údaje", variable=self.include_detailed
        ).pack(anchor="w")

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(10, 0))

        ttk.Button(button_frame, text="Zrušit", command=self.dialog.destroy).pack(
            side="right", padx=(5, 0)
        )
        ttk.Button(button_frame, text="Exportovat", command=self.export_data).pack(
            side="right"
        )

    def export_data(self):
        """Export data in selected format."""
        format_type = self.format_var.get()

        # Get filename
        if format_type == "txt":
            filename = filedialog.asksaveasfilename(
                title="Export do TXT",
                defaultextension=".txt",
                filetypes=[("Text soubory", "*.txt")],
            )
        elif format_type == "csv":
            filename = filedialog.asksaveasfilename(
                title="Export do CSV",
                defaultextension=".csv",
                filetypes=[("CSV soubory", "*.csv")],
            )
        elif format_type == "excel":
            filename = filedialog.asksaveasfilename(
                title="Export do Excel",
                defaultextension=".xlsx",
                filetypes=[("Excel soubory", "*.xlsx")],
            )

        if not filename:
            return

        try:
            if format_type == "txt":
                self._export_txt(filename)
            elif format_type == "csv":
                self._export_csv(filename)
            elif format_type == "excel":
                self._export_excel(filename)

            messagebox.showinfo("Úspěch", f"Výsledky exportovány do:\n{filename}")
            self.dialog.destroy()

        except Exception as e:
            messagebox.showerror("Chyba", f"Chyba při exportu:\n{e}")

    def _export_txt(self, filename: str):
        """Export results to TXT file."""
        with open(filename, "w", encoding="utf-8") as f:
            f.write("VÝSLEDKY VÝPOČTU PLYNOVÉHO HOŘÁKU A SPALOVACÍ KOMORY\n")
            f.write("=" * 60 + "\n\n")
            f.write(
                f"Datum exportu: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n"
            )

            if self.include_input.get():
                f.write("VSTUPNÍ PARAMETRY:\n")
                f.write("-" * 30 + "\n")
                for key, value in self.input_data.items():
                    f.write(f"{key}: {value}\n")
                f.write("\n")

            if self.include_results.get():
                f.write("VÝSLEDKY VÝPOČTŮ:\n")
                f.write("-" * 30 + "\n")

                for module_name, results in self.results.items():
                    f.write(f"\n{module_name.upper()}:\n")
                    if hasattr(results, "__dict__"):
                        for attr, value in results.__dict__.items():
                            f.write(f"  {attr}: {value}\n")
                    f.write("\n")

    def _export_csv(self, filename: str):
        """Export results to CSV file."""
        data = []

        if self.include_input.get():
            for key, value in self.input_data.items():
                data.append(["Vstup", key, value, ""])

        if self.include_results.get():
            for module_name, results in self.results.items():
                if hasattr(results, "__dict__"):
                    for attr, value in results.__dict__.items():
                        data.append(["Výsledek", module_name, attr, value])

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Typ", "Modul/Kategorie", "Parametr", "Hodnota"])
            writer.writerows(data)

    def _export_excel(self, filename: str):
        """Export results to Excel file."""
        try:
            with pd.ExcelWriter(filename, engine="openpyxl") as writer:

                if self.include_input.get():
                    input_df = pd.DataFrame(
                        list(self.input_data.items()), columns=["Parametr", "Hodnota"]
                    )
                    input_df.to_excel(
                        writer, sheet_name="Vstupní parametry", index=False
                    )

                if self.include_results.get():
                    for module_name, results in self.results.items():
                        if hasattr(results, "__dict__"):
                            result_df = pd.DataFrame(
                                list(results.__dict__.items()),
                                columns=["Parametr", "Hodnota"],
                            )
                            result_df.to_excel(
                                writer, sheet_name=module_name.capitalize(), index=False
                            )

        except ImportError:
            # Fallback if pandas/openpyxl not available
            messagebox.showerror(
                "Chyba", "Pro export do Excel je potřeba nainstalovat pandas a openpyxl"
            )


def main():
    """Main function to run the GUI application."""
    root = tk.Tk()

    # Set up styling
    style = ttk.Style()
    style.theme_use("clam")

    # Create and run application
    BurnerCalculatorGUI(root)

    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")

    root.mainloop()


if __name__ == "__main__":
    main()
