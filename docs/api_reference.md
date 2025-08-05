# API Reference

Complete API reference for the Gas Burner and Combustion Chamber Design Calculator.

## Table of Contents
1. [Core Calculation Modules](#core-calculation-modules)
2. [Data Classes](#data-classes)
3. [Supporting Modules](#supporting-modules)
4. [GUI Module](#gui-module)
5. [Usage Examples](#usage-examples)
6. [Configuration](#configuration)
7. [Error Handling](#error-handling)

## Core Calculation Modules

### combustion.py

#### CombustionCalculator

The main class for performing combustion calculations including stoichiometric analysis, flame temperature calculations, and combustion product composition.

```python
from src.combustion import CombustionCalculator

calculator = CombustionCalculator(fuel_data_path="data/fuels.json")
```

##### Constructor Parameters
- `fuel_data_path` (str, optional): Path to fuel properties JSON file. Defaults to "data/fuels.json"

##### Methods

**`calculate_stoichiometric_air(fuel_type: str, fuel_flow_rate: float) -> float`**

Calculate theoretical air requirement for complete combustion.

*Parameters:*
- `fuel_type` (str): Type of fuel ('natural_gas', 'methane', 'propane')
- `fuel_flow_rate` (float): Fuel mass flow rate [kg/s]

*Returns:*
- `float`: Required air mass flow rate [kg/s]

*Raises:*
- `ValueError`: If fuel type is not supported

```python
air_flow = calculator.calculate_stoichiometric_air('natural_gas', 0.01)
```

**`calculate_combustion_products(fuel_type: str, fuel_flow_rate: float, excess_air_ratio: float = 1.2) -> CombustionResults`**

Perform complete combustion analysis including products composition and flame temperature.

*Parameters:*
- `fuel_type` (str): Type of fuel
- `fuel_flow_rate` (float): Fuel mass flow rate [kg/s]
- `excess_air_ratio` (float): Excess air ratio (≥1.0)

*Returns:*
- `CombustionResults`: Complete combustion calculation results

*Raises:*
- `ValueError`: If parameters are invalid

```python
results = calculator.calculate_combustion_products('natural_gas', 0.01, 1.2)
print(f"Flame temperature: {results.adiabatic_flame_temperature:.0f} K")
```

**`get_fuel_properties(fuel_type: str) -> dict`**

Get properties of specified fuel type.

*Parameters:*
- `fuel_type` (str): Type of fuel

*Returns:*
- `dict`: Fuel properties including heating values, molecular weight, etc.

**`get_available_fuels() -> list`**

Get list of available fuel types.

*Returns:*
- `list`: List of fuel type identifiers

### burner_design.py

#### BurnerDesigner

Class for burner sizing calculations, pressure requirements, and flow analysis.

```python
from src.burner_design import BurnerDesigner

designer = BurnerDesigner(safety_factor=1.2)
```

##### Constructor Parameters
- `combustion_calculator` (CombustionCalculator, optional): Combustion calculator instance
- `safety_factor` (float): Safety factor for design calculations (default: 1.2)
- `fuel_data_path` (str, optional): Path to fuel data file

##### Methods

**`design_burner(fuel_type: str, required_power: float, supply_pressure: float, target_velocity: float = None, excess_air_ratio: float = 1.2) -> BurnerDesignResults`**

Design a gas burner based on power requirements and constraints.

*Parameters:*
- `fuel_type` (str): Type of fuel to be used
- `required_power` (float): Required thermal power [W]
- `supply_pressure` (float): Available gas supply pressure [Pa]
- `target_velocity` (float, optional): Target gas velocity [m/s]
- `excess_air_ratio` (float): Excess air ratio

*Returns:*
- `BurnerDesignResults`: Complete burner design results

*Raises:*
- `ValueError`: If design parameters are invalid or unfeasible

```python
burner_results = designer.design_burner(
    fuel_type="natural_gas",
    required_power=100000,  # 100 kW
    supply_pressure=3000,   # 3000 Pa
    target_velocity=25.0    # 25 m/s
)
```

**`validate_design(design_results: BurnerDesignResults) -> dict`**

Validate burner design against safety and performance criteria.

*Parameters:*
- `design_results` (BurnerDesignResults): Design results to validate

*Returns:*
- `dict`: Validation results for different criteria

**`get_design_recommendations(design_results: BurnerDesignResults) -> list`**

Get design recommendations based on calculated results.

*Parameters:*
- `design_results` (BurnerDesignResults): Design results

*Returns:*
- `list`: List of design recommendations

### chamber_design.py

#### ChamberDesigner

Class for combustion chamber sizing, heat transfer calculations, and thermal performance analysis.

```python
from src.chamber_design import ChamberDesigner

chamber_designer = ChamberDesigner(safety_factor=1.5)
```

##### Constructor Parameters
- `combustion_calculator` (CombustionCalculator, optional): Combustion calculator instance
- `burner_designer` (BurnerDesigner, optional): Burner designer instance
- `safety_factor` (float): Safety factor for design calculations (default: 1.5)
- `fuel_data_path` (str, optional): Path to fuel data file

##### Methods

**`design_chamber(fuel_type: str, required_power: float, target_residence_time: float = 0.5, wall_insulation_thickness: float = 0.1, ambient_temperature: float = 293.15, target_efficiency: float = 0.85) -> ChamberDesignResults`**

Design a combustion chamber based on power and residence time requirements.

*Parameters:*
- `fuel_type` (str): Type of fuel to be used
- `required_power` (float): Required thermal power [W]
- `target_residence_time` (float): Target gas residence time [s]
- `wall_insulation_thickness` (float): Wall insulation thickness [m]
- `ambient_temperature` (float): Ambient temperature [K]
- `target_efficiency` (float): Target thermal efficiency [-]

*Returns:*
- `ChamberDesignResults`: Complete chamber design results

```python
chamber_results = chamber_designer.design_chamber(
    fuel_type="natural_gas",
    required_power=100000,
    target_residence_time=0.5,
    wall_insulation_thickness=0.1
)
```

**`calculate_temperature_distribution(design_results: ChamberDesignResults, combustion_results: CombustionResults, num_points: int = 10) -> dict`**

Calculate temperature distribution along chamber length.

*Parameters:*
- `design_results` (ChamberDesignResults): Chamber design results
- `combustion_results` (CombustionResults): Combustion results
- `num_points` (int): Number of calculation points along length

*Returns:*
- `dict`: Dictionary with 'positions' and 'temperatures' arrays

### radiation.py

#### RadiationCalculator

Class for radiation heat transfer calculations including Stefan-Boltzmann law applications, view factors, and material emissivity.

```python
from src.radiation import RadiationCalculator

radiation_calc = RadiationCalculator()
```

##### Constructor Parameters
- `combustion_calculator` (CombustionCalculator, optional): Combustion calculator instance

##### Methods

**`calculate_flame_radiation(flame_temperature: float, chamber_wall_temperature: float, chamber_diameter: float, chamber_length: float, fuel_type: str, excess_air_ratio: float = 1.2, soot_concentration: float = 0.0) -> RadiationResults`**

Calculate radiation heat transfer from flame to chamber walls.

*Parameters:*
- `flame_temperature` (float): Average flame temperature [K]
- `chamber_wall_temperature` (float): Chamber wall temperature [K]
- `chamber_diameter` (float): Chamber internal diameter [m]
- `chamber_length` (float): Chamber length [m]
- `fuel_type` (str): Type of fuel
- `excess_air_ratio` (float): Excess air ratio
- `soot_concentration` (float): Soot concentration [kg/m³]

*Returns:*
- `RadiationResults`: Complete radiation calculation results

```python
radiation_results = radiation_calc.calculate_flame_radiation(
    flame_temperature=1800,  # K
    chamber_wall_temperature=1200,  # K
    chamber_diameter=0.5,  # m
    chamber_length=1.5,  # m
    fuel_type="natural_gas"
)
```

**`calculate_radiation_exchange_network(surfaces: List[SurfaceProperties], view_factors_matrix: List[List[float]]) -> dict`**

Calculate radiation exchange between multiple surfaces using network method.

*Parameters:*
- `surfaces` (List[SurfaceProperties]): List of surface properties
- `view_factors_matrix` (List[List[float]]): Matrix of view factors

*Returns:*
- `dict`: Heat transfer rates between surfaces

**`get_material_emissivity(material_name: str, temperature: float = None) -> float`**

Get material emissivity, potentially temperature-dependent.

*Parameters:*
- `material_name` (str): Material identifier
- `temperature` (float, optional): Temperature [K]

*Returns:*
- `float`: Material emissivity [-]

### pressure_losses.py

#### PressureLossCalculator

Class for pressure loss calculations in gas piping systems including friction losses, minor losses, and elevation effects.

```python
from src.pressure_losses import PressureLossCalculator

pressure_calc = PressureLossCalculator(safety_factor=1.3)
```

##### Constructor Parameters
- `combustion_calculator` (CombustionCalculator, optional): Combustion calculator instance
- `safety_factor` (float): Safety factor for pressure calculations (default: 1.3)

##### Methods

**`calculate_system_pressure_losses(pipe_segments: List[PipeSegment], fittings: List[Fitting], mass_flow_rate: float, gas_density: float, gas_viscosity: float = 1.5e-5, burner_results: BurnerDesignResults = None) -> PressureLossResults`**

Calculate total pressure losses in gas piping system.

*Parameters:*
- `pipe_segments` (List[PipeSegment]): List of pipe segments
- `fittings` (List[Fitting]): List of fittings and components
- `mass_flow_rate` (float): Gas mass flow rate [kg/s]
- `gas_density` (float): Gas density [kg/m³]
- `gas_viscosity` (float): Dynamic viscosity [Pa·s]
- `burner_results` (BurnerDesignResults, optional): Burner design results

*Returns:*
- `PressureLossResults`: Complete pressure loss calculation results

```python
pipe_segments = [
    PipeSegment(length=10.0, diameter=0.05, roughness=0.000045, material="steel_new")
]
fittings = [
    Fitting("elbow_90_long", 2, 0.6, 0.05)
]

pressure_results = pressure_calc.calculate_system_pressure_losses(
    pipe_segments=pipe_segments,
    fittings=fittings,
    mass_flow_rate=0.002,
    gas_density=0.8
)
```

**`optimize_pipe_diameter(length: float, mass_flow_rate: float, gas_density: float, max_pressure_loss: float, material: str = "steel_new", max_velocity: float = 20.0) -> dict`**

Optimize pipe diameter based on pressure drop and velocity constraints.

*Parameters:*
- `length` (float): Pipe length [m]
- `mass_flow_rate` (float): Mass flow rate [kg/s]
- `gas_density` (float): Gas density [kg/m³]
- `max_pressure_loss` (float): Maximum allowable pressure loss [Pa]
- `material` (str): Pipe material
- `max_velocity` (float): Maximum gas velocity [m/s]

*Returns:*
- `dict`: Optimized diameter and related parameters

**`get_pipe_roughness(material: str) -> float`**

Get pipe roughness value for specified material.

**`get_fitting_coefficient(fitting_type: str) -> float`**

Get loss coefficient for specified fitting type.

## Data Classes

### CombustionResults

```python
@dataclass
class CombustionResults:
    fuel_flow_rate: float              # [kg/s]
    air_flow_rate: float               # [kg/s]  
    flue_gas_flow_rate: float          # [kg/s]
    adiabatic_flame_temperature: float # [K]
    heat_release_rate: float           # [W]
    excess_air_ratio: float            # [-]
    co2_volume_percent: float          # [%]
    o2_volume_percent: float           # [%]
```

### BurnerDesignResults

```python
@dataclass
class BurnerDesignResults:
    burner_diameter: float             # [m]
    burner_area: float                 # [m²]
    gas_velocity: float                # [m/s]
    burner_pressure_drop: float        # [Pa]
    required_supply_pressure: float    # [Pa]
    heat_release_density: float        # [W/m²]
    burner_length: float               # [m]
    flame_length: float                # [m]
```

### ChamberDesignResults

```python
@dataclass
class ChamberDesignResults:
    chamber_volume: float              # [m³]
    chamber_diameter: float            # [m]
    chamber_length: float              # [m]
    chamber_area: float                # [m²]
    chamber_surface_area: float        # [m²]
    residence_time: float              # [s]
    heat_transfer_coefficient: float   # [W/m²K]
    wall_temperature: float            # [K]
    heat_loss_rate: float              # [W]
    thermal_efficiency: float          # [%]
    volume_heat_release_rate: float    # [W/m³]
```

### RadiationResults

```python
@dataclass
class RadiationResults:
    total_radiation_heat_transfer: float    # [W]
    flame_to_wall_heat_transfer: float      # [W]
    wall_to_ambient_heat_transfer: float    # [W]
    flame_emissivity: float                 # [-]
    wall_emissivity: float                  # [-]
    flame_absorptivity: float               # [-]
    view_factor_flame_wall: float           # [-]
    radiation_efficiency: float             # [%]
    mean_beam_length: float                 # [m]
```

### PressureLossResults

```python
@dataclass
class PressureLossResults:
    total_pressure_loss: float         # [Pa]
    friction_losses: float             # [Pa]
    minor_losses: float                # [Pa]
    elevation_losses: float            # [Pa]
    burner_pressure_loss: float        # [Pa]
    required_supply_pressure: float    # [Pa]
    system_resistance_coefficient: float # [-]
    reynolds_number: float             # [-]
    friction_factor: float             # [-]
    velocity_pressure: float           # [Pa]
```

### PipeSegment

```python
@dataclass
class PipeSegment:
    length: float                      # [m]
    diameter: float                    # [m]
    roughness: float                   # [m]
    material: str                      # Material type
    elevation_change: float = 0.0      # [m] (positive = upward)
```

### Fitting

```python
@dataclass
class Fitting:
    type: str                          # Fitting type
    quantity: int                      # Number of fittings
    loss_coefficient: float            # Loss coefficient K [-]
    diameter: float                    # [m]
```

### SurfaceProperties

```python
@dataclass
class SurfaceProperties:
    area: float                        # [m²]
    temperature: float                 # [K]
    emissivity: float                  # [-]
    absorptivity: float                # [-]
```

## Supporting Modules

### visualization.py

#### BurnerVisualization

Class for generating charts and visualizations of calculation results.

```python
from src.visualization import BurnerVisualization

viz = BurnerVisualization(
    output_dir="output",
    figure_size=(10, 8),
    dpi=300
)
```

##### Constructor Parameters
- `output_dir` (str): Directory for saving visualization files (default: "output")
- `figure_size` (tuple): Default figure size (width, height) (default: (10, 8))
- `dpi` (int): Resolution for saved images (default: 300)

##### Methods

**`plot_combustion_analysis(combustion_results: CombustionResults, save_formats: List[str] = ['png']) -> List[str]`**

Generate combustion analysis charts including flame temperature, gas composition, and flow rates.

*Parameters:*
- `combustion_results` (CombustionResults): Combustion calculation results
- `save_formats` (List[str]): Output formats ['png', 'pdf', 'jpeg']

*Returns:*
- `List[str]`: List of generated file paths

**`plot_pressure_losses(pressure_results: PressureLossResults, system_components: dict, save_formats: List[str] = ['png']) -> List[str]`**

Generate pressure loss distribution charts.

**`plot_temperature_distribution(chamber_results: ChamberDesignResults, temperature_data: dict, save_formats: List[str] = ['png']) -> List[str]`**

Generate temperature distribution plots along chamber length.

**`plot_burner_geometry(burner_results: BurnerDesignResults, chamber_results: ChamberDesignResults, save_formats: List[str] = ['png']) -> List[str]`**

Generate technical drawings of burner and chamber geometry.

**`create_summary_dashboard(all_results: dict, save_formats: List[str] = ['png']) -> List[str]`**

Create comprehensive dashboard with all key results.

### report.py

#### BurnerReportGenerator

Class for generating comprehensive reports in multiple formats.

```python
from src.report import BurnerReportGenerator

report_gen = BurnerReportGenerator(output_dir="output")
```

##### Constructor Parameters
- `output_dir` (str): Directory for saving report files (default: "output")

##### Methods

**`generate_text_report(results: dict, project_name: str = "Burner_Calculation") -> str`**

Generate comprehensive text report with all calculations and recommendations.

*Parameters:*
- `results` (dict): All calculation results
- `project_name` (str): Project identifier for the report

*Returns:*
- `str`: Path to generated text file

**`generate_csv_export(results: dict, project_name: str = "Burner_Calculation") -> str`**

Export calculation data to CSV format for spreadsheet analysis.

**`generate_excel_report(results: dict, project_name: str = "Burner_Calculation") -> str`**

Create Excel workbook with multiple worksheets for different calculation aspects.

**`generate_comprehensive_report(results: dict, project_name: str = "Burner_Calculation") -> dict`**

Generate all report formats and return file paths.

*Returns:*
- `dict`: Dictionary with format names as keys and file paths as values

## GUI Module

### gui.py

#### BurnerCalculatorGUI

Main GUI application class using tkinter for user interface.

```python
from gui.gui import BurnerCalculatorGUI
import tkinter as tk

root = tk.Tk()
app = BurnerCalculatorGUI(root)
root.mainloop()
```

##### Constructor Parameters
- `master` (tk.Tk): Root tkinter window
- `output_dir` (str): Default output directory (default: "output")
- `fuel_data_path` (str): Path to fuel data file

##### Key Methods

**`setup_notebook()`**

Create tabbed interface with all calculation sections.

**`setup_input_tab()`**

Create input parameter interface with fuel selection, power settings, and operating conditions.

**`setup_results_tabs()`**

Create results display tabs for different calculation modules.

**`perform_calculations()`**

Execute all calculations based on current input parameters and update displays.

**`load_input_file()`**

Load calculation parameters from JSON file.

**`save_input_file()`**

Save current input parameters to JSON file.

**`export_results()`**

Export calculation results in selected formats.

**`show_error_dialog(message: str)`**

Display error message to user.

**`show_validation_warnings(warnings: List[str])`**

Display validation warnings and recommendations.

## Usage Examples

### Complete Calculation Workflow

```python
from src.combustion import CombustionCalculator
from src.burner_design import BurnerDesigner
from src.chamber_design import ChamberDesigner
from src.radiation import RadiationCalculator
from src.pressure_losses import PressureLossCalculator
from src.visualization import BurnerVisualization
from src.report import BurnerReportGenerator

# Initialize calculators
combustion_calc = CombustionCalculator()
burner_designer = BurnerDesigner(combustion_calc)
chamber_designer = ChamberDesigner(combustion_calc, burner_designer)
radiation_calc = RadiationCalculator(combustion_calc)
pressure_calc = PressureLossCalculator(combustion_calc)

# Design parameters
fuel_type = "natural_gas"
required_power = 150000  # 150 kW
supply_pressure = 4000   # 4000 Pa
excess_air_ratio = 1.15
residence_time = 0.6     # 0.6 seconds

# Perform calculations
fuel_flow = required_power / combustion_calc.get_fuel_properties(fuel_type)['properties']['lower_heating_value_mass']

combustion_results = combustion_calc.calculate_combustion_products(
    fuel_type, fuel_flow, excess_air_ratio
)

burner_results = burner_designer.design_burner(
    fuel_type=fuel_type,
    required_power=required_power,
    supply_pressure=supply_pressure,
    excess_air_ratio=excess_air_ratio
)

chamber_results = chamber_designer.design_chamber(
    fuel_type=fuel_type,
    required_power=required_power,
    target_residence_time=residence_time
)

radiation_results = radiation_calc.calculate_flame_radiation(
    flame_temperature=combustion_results.adiabatic_flame_temperature,
    chamber_wall_temperature=chamber_results.wall_temperature,
    chamber_diameter=chamber_results.chamber_diameter,
    chamber_length=chamber_results.chamber_length,
    fuel_type=fuel_type,
    excess_air_ratio=excess_air_ratio
)

# Define piping system
pipe_segments = [
    PipeSegment(10.0, 0.05, pressure_calc.get_pipe_roughness("steel_new"), "steel_new", 0.0)
]
fittings = [
    Fitting("elbow_90_long", 3, pressure_calc.get_fitting_coefficient("elbow_90_long"), 0.05),
    Fitting("gate_valve_open", 1, pressure_calc.get_fitting_coefficient("gate_valve_open"), 0.05)
]

pressure_results = pressure_calc.calculate_system_pressure_losses(
    pipe_segments=pipe_segments,
    fittings=fittings,
    mass_flow_rate=combustion_results.fuel_flow_rate + combustion_results.air_flow_rate,
    gas_density=0.8,  # Typical gas density
    burner_results=burner_results
)

# Compile all results
all_results = {
    'inputs': {
        'fuel_type': fuel_type,
        'required_power': required_power,
        'supply_pressure': supply_pressure,
        'excess_air_ratio': excess_air_ratio,
        'residence_time': residence_time
    },
    'combustion': combustion_results,
    'burner': burner_results,
    'chamber': chamber_results,
    'radiation': radiation_results,
    'pressure_losses': pressure_results
}

# Generate visualizations
viz = BurnerVisualization()
viz.plot_combustion_analysis(combustion_results, ['png', 'pdf'])
viz.plot_burner_geometry(burner_results, chamber_results, ['png', 'pdf'])
viz.plot_pressure_losses(pressure_results, {'pipes': pipe_segments, 'fittings': fittings}, ['png'])

# Generate reports
report_gen = BurnerReportGenerator()
report_files = report_gen.generate_comprehensive_report(all_results, "Industrial_Burner_150kW")

print("Calculation completed successfully!")
print(f"Report files: {report_files}")
```

### Parametric Study Example

```python
import numpy as np
from src.combustion import CombustionCalculator

def excess_air_study():
    """Study the effect of excess air ratio on performance"""
    
    calc = CombustionCalculator()
    fuel_type = 'natural_gas'
    power = 100000  # 100 kW
    
    # Parameter ranges
    excess_air_ratios = np.linspace(1.05, 1.5, 20)
    
    results = []
    for lambda_val in excess_air_ratios:
        fuel_flow = power / calc.get_fuel_properties(fuel_type)['properties']['lower_heating_value_mass']
        combustion_result = calc.calculate_combustion_products(fuel_type, fuel_flow, lambda_val)
        
        results.append({
            'excess_air_ratio': lambda_val,
            'flame_temperature': combustion_result.adiabatic_flame_temperature,
            'co2_percent': combustion_result.co2_volume_percent,
            'o2_percent': combustion_result.o2_volume_percent
        })
    
    return results

# Run study
study_results = excess_air_study()
optimal_lambda = min(study_results, key=lambda x: abs(x['o2_percent'] - 3.0))['excess_air_ratio']
print(f"Optimal excess air ratio for 3% O2: {optimal_lambda:.2f}")
```

## Configuration

### Fuel Database Format

The fuel database (`data/fuels.json`) defines available fuel types and their properties:

```json
{
  "constants": {
    "universal_gas_constant": 8314.46,
    "stefan_boltzmann_constant": 5.67e-8,
    "standard_pressure": 101325,
    "standard_temperature": 273.15,
    "air_molecular_weight": 28.97
  },
  "fuels": {
    "natural_gas": {
      "name": "Natural Gas",
      "properties": {
        "lower_heating_value_mass": 50000000,
        "molecular_weight": 16.04,
        "density": 0.717,
        "air_fuel_ratio_mass": 17.2
      }
    },
    "propane": {
      "name": "Propane",
      "properties": {
        "lower_heating_value_mass": 46000000,
        "molecular_weight": 44.10,
        "density": 1.967,
        "air_fuel_ratio_mass": 15.7
      }
    }
  },
  "material_properties": {
    "steel_oxidized": {
      "emissivity": 0.79,
      "temperature_range": [500, 1000]
    },
    "refractory_brick": {
      "emissivity": 0.75,
      "temperature_range": [800, 1200]
    }
  }
}
```

### Adding Custom Fuels

```python
# Example: Adding biogas as a custom fuel
custom_fuel_data = {
    "biogas": {
        "name": "Biogas",
        "properties": {
            "lower_heating_value_mass": 22000000,  # J/kg
            "molecular_weight": 24.5,  # kg/kmol
            "density": 1.1,  # kg/m³ at STP
            "air_fuel_ratio_mass": 9.5
        }
    }
}

# This would be added to the fuels.json file
```

### GUI Configuration Options

```python
# Example GUI initialization with custom settings
app = BurnerCalculatorGUI(
    master=root,
    output_dir="custom_output",
    fuel_data_path="custom_fuels.json",
    default_power=150000,  # Default power in W
    default_fuel="propane",
    enable_advanced_features=True,
    theme="dark",
    language="english"
)
```

## Error Handling

### Exception Types

All modules implement comprehensive error handling with specific exception types:

#### ValueError
Raised for invalid input parameters:
```python
try:
    result = calculator.calculate_combustion_products('invalid_fuel', 0.01, 1.2)
except ValueError as e:
    print(f"Invalid parameter: {e}")
```

#### FileNotFoundError
Raised when required data files are missing:
```python
try:
    calc = CombustionCalculator(fuel_data_path="missing_file.json")
except FileNotFoundError as e:
    print(f"Data file not found: {e}")
```

#### CalculationError (Custom)
Raised for calculation-specific errors:
```python
from src.exceptions import CalculationError

try:
    results = designer.design_burner(fuel_type="natural_gas", required_power=-1000)
except CalculationError as e:
    print(f"Calculation failed: {e}")
```

### Input Validation

All calculation methods perform comprehensive input validation:

```python
def validate_inputs(self, fuel_type: str, power: float, pressure: float):
    """Example validation method"""
    
    errors = []
    
    if fuel_type not in self.get_available_fuels():
        errors.append(f"Unsupported fuel type: {fuel_type}")
    
    if power <= 0:
        errors.append("Power must be greater than zero")
    
    if pressure <= 0:
        errors.append("Pressure must be greater than zero")
    
    if errors:
        raise ValueError("; ".join(errors))
```

### Error Recovery

The GUI implements error recovery mechanisms:

```python
def safe_calculation(self):
    """Example error recovery in GUI"""
    
    try:
        self.perform_calculations()
    except ValueError as e:
        self.show_error_dialog(f"Input Error: {e}")
        self.highlight_invalid_inputs()
    except CalculationError as e:
        self.show_error_dialog(f"Calculation Error: {e}")
        self.suggest_parameter_adjustments()
    except Exception as e:
        self.show_error_dialog(f"Unexpected Error: {e}")
        self.reset_to_default_values()
```

---

*This comprehensive API reference covers all public interfaces and methods. For additional implementation details, refer to the source code and inline documentation.*