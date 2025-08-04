# API Reference

Complete API reference for the Gas Burner and Combustion Chamber Design Calculator.

## Core Modules

### combustion.py

#### CombustionCalculator

The main class for performing combustion calculations.

```python
from src.combustion import CombustionCalculator

calculator = CombustionCalculator()
```

**Methods:**

- `calculate(fuel_data, excess_air_ratio=1.2)` - Perform complete combustion analysis
- `theoretical_air_requirement(fuel_composition)` - Calculate stoichiometric air needs
- `combustion_products(fuel_data, excess_air_ratio)` - Determine combustion products
- `adiabatic_flame_temperature(fuel_data, excess_air_ratio)` - Calculate flame temperature

### burner_design.py

#### BurnerDesign

Calculations for burner dimensioning and design.

```python
from src.burner_design import BurnerDesign

burner = BurnerDesign()
```

**Methods:**

- `calculate(power, fuel_type, **kwargs)` - Main burner design calculation
- `nozzle_sizing(flow_rate, pressure_drop)` - Calculate nozzle dimensions
- `gas_velocity_calculation(flow_rate, area)` - Determine gas velocities
- `pressure_requirements(system_losses)` - Calculate required gas pressure

### chamber_design.py

#### ChamberDesign

Combustion chamber sizing and optimization.

```python
from src.chamber_design import ChamberDesign

chamber = ChamberDesign()
```

**Methods:**

- `calculate(power, fuel_data, **kwargs)` - Complete chamber design
- `volume_calculation(power, heat_loading)` - Determine required volume
- `geometry_optimization(volume, constraints)` - Optimize chamber geometry
- `residence_time_calculation(volume, flow_rate)` - Calculate gas residence time

### radiation.py

#### RadiationCalculator

Radiative heat transfer calculations.

```python
from src.radiation import RadiationCalculator

radiation = RadiationCalculator()
```

**Methods:**

- `calculate(temperature_data, geometry_data)` - Complete radiation analysis
- `gas_emissivity(composition, temperature)` - Calculate gas emissivity
- `heat_flux_calculation(temperatures, emissivities)` - Determine heat flux
- `view_factor_calculation(geometry)` - Calculate geometric view factors

### pressure_losses.py

#### PressureLossCalculator

Pressure drop calculations throughout the system.

```python
from src.pressure_losses import PressureLossCalculator

pressure = PressureLossCalculator()
```

**Methods:**

- `calculate(system_data)` - Complete pressure loss analysis
- `component_losses(component_data)` - Calculate losses by component
- `duct_losses(duct_data, flow_data)` - Determine ductwork losses
- `total_system_loss(component_losses)` - Sum total system pressure drop

### visualization.py

#### BurnerVisualization

Chart and graph generation for analysis results.

```python
from src.visualization import BurnerVisualization

viz = BurnerVisualization(output_dir="output")
```

**Methods:**

- `plot_combustion_analysis(data, save_formats)` - Generate combustion charts
- `plot_pressure_losses(data, save_formats)` - Create pressure loss diagrams
- `plot_temperature_distribution(data, save_formats)` - Temperature visualizations
- `plot_burner_geometry(data, save_formats)` - Technical drawings
- `export_all_visualizations(data, save_formats)` - Generate all charts

### report.py

#### BurnerReportGenerator

Comprehensive report generation in multiple formats.

```python
from src.report import BurnerReportGenerator

report_gen = BurnerReportGenerator(output_dir="output")
```

**Methods:**

- `generate_text_report(results, filename)` - Create detailed text report
- `generate_csv_export(results, filename)` - Export data to CSV
- `generate_excel_report(results, filename)` - Create Excel workbook
- `generate_complete_report(results, formats)` - Generate all report types

## GUI Module

### gui.py

#### BurnerCalculatorGUI

Main GUI application class using tkinter.

```python
from gui.gui import BurnerCalculatorGUI
import tkinter as tk

root = tk.Tk()
app = BurnerCalculatorGUI(root)
```

**Key Methods:**

- `setup_input_frame()` - Create input parameter interface
- `setup_results_frame()` - Create results display area
- `setup_visualization_frame()` - Create chart display area
- `perform_calculation()` - Execute calculations and update display
- `export_results()` - Export results in various formats

## Data Structures

### Fuel Data Format

```python
fuel_data = {
    "name": "Natural Gas",
    "heating_value": 35.8,  # MJ/m³
    "density": 0.717,       # kg/m³
    "composition": {
        "CH4": 95.0,        # %
        "C2H6": 3.0,        # %
        "C3H8": 1.0,        # %
        "N2": 1.0           # %
    }
}
```

### Calculation Results Format

```python
results = {
    "inputs": {
        "fuel_type": "Natural Gas",
        "power": 100,  # kW
        "excess_air_ratio": 1.2
    },
    "combustion": {
        "theoretical_air": 9.52,    # m³/m³
        "actual_air": 11.42,        # m³/m³
        "excess_air": 20.0,         # %
        "combustion_temp": 1850,    # °C
        "products": {
            "CO2": 8.5,   # %
            "H2O": 16.8,  # %
            "N2": 71.2,   # %
            "O2": 3.5     # %
        }
    },
    "burner": {
        "power": 100,              # kW
        "nozzle_diameter": 8.5,    # mm
        "gas_velocity": 25.0,      # m/s
        "gas_pressure": 2500       # Pa
    },
    "chamber": {
        "volume": 2.5,            # m³
        "length": 2.0,            # m
        "diameter": 1.2,          # m
        "residence_time": 0.85,   # s
        "heat_loading": 40        # kW/m³
    },
    "radiation": {
        "heat_flux": 85.5,           # kW/m²
        "gas_emissivity": 0.25,      # -
        "wall_emissivity": 0.85,     # -
        "radiation_efficiency": 78.5 # %
    },
    "pressure_losses": {
        "components": {
            "Burner": 50.0,    # Pa
            "Chamber": 30.0,   # Pa
            "Ducting": 20.0,   # Pa
            "Stack": 15.0      # Pa
        },
        "total": 115.0         # Pa
    }
}
```

## Error Handling

All modules implement comprehensive error handling:

- **Input Validation**: All parameters validated before calculation
- **Calculation Errors**: Mathematical errors caught and reported
- **File Operations**: File I/O errors handled gracefully
- **GUI Errors**: Interface errors displayed to user

### Common Exceptions

- `ValueError` - Invalid input parameters
- `KeyError` - Missing required data fields
- `FileNotFoundError` - Missing configuration files
- `CalculationError` - Custom exception for calculation failures

## Usage Examples

### Basic Calculation Workflow

```python
from src.combustion import CombustionCalculator
from src.burner_design import BurnerDesign
from src.chamber_design import ChamberDesign

# Load fuel data
with open('data/fuels.json', 'r') as f:
    fuels = json.load(f)

natural_gas = fuels['natural_gas']

# Perform calculations
combustion = CombustionCalculator()
combustion_results = combustion.calculate(natural_gas, excess_air_ratio=1.2)

burner = BurnerDesign()
burner_results = burner.calculate(power=100, fuel_data=natural_gas)

chamber = ChamberDesign()
chamber_results = chamber.calculate(power=100, fuel_data=natural_gas)

# Generate reports
from src.report import BurnerReportGenerator
report_gen = BurnerReportGenerator()

all_results = {
    'inputs': {'power': 100, 'fuel_type': 'Natural Gas'},
    'combustion': combustion_results,
    'burner': burner_results,
    'chamber': chamber_results
}

report_files = report_gen.generate_complete_report(
    all_results, 
    formats=['txt', 'csv', 'xlsx']
)
```

### Visualization Example

```python
from src.visualization import BurnerVisualization

viz = BurnerVisualization(output_dir="charts")

# Generate individual charts
combustion_charts = viz.plot_combustion_analysis(
    combustion_results, 
    save_formats=['png', 'pdf']
)

# Generate comprehensive dashboard
dashboard = viz.create_summary_dashboard(
    all_results,
    save_formats=['png', 'pdf']
)
```

## Configuration

### Fuel Database Configuration

The fuel database (`data/fuels.json`) can be extended with custom fuels:

```json
{
  "custom_fuel": {
    "name": "Custom Biogas",
    "heating_value": 22.5,
    "density": 1.15,
    "composition": {
      "CH4": 60.0,
      "CO2": 38.0,
      "H2S": 1.5,
      "N2": 0.5
    }
  }
}
```

### GUI Configuration

GUI settings can be customized through initialization parameters:

```python
app = BurnerCalculatorGUI(
    root,
    default_output_dir="custom_output",
    enable_advanced_features=True,
    language="czech"
)
```

---

*This API reference covers all public methods and interfaces. For implementation details, refer to the source code and inline documentation.*