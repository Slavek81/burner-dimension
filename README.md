# Gas Burner and Combustion Chamber Design Calculator

A comprehensive Python application with GUI for calculating and designing gas burners and combustion chambers. This professional engineering tool provides accurate calculations for combustion analysis, burner dimensioning, chamber design, radiation heat transfer, and pressure loss analysis.

## 🚀 Features

- **Complete Combustion Analysis** - Stoichiometric calculations, flame temperature, flue gas composition
- **Burner Design & Dimensioning** - Automated sizing based on power requirements and constraints  
- **Combustion Chamber Design** - Volume calculations, heat transfer, residence time optimization
- **Radiation Heat Transfer** - Stefan-Boltzmann law, view factors, multi-surface exchange
- **Pressure Loss Analysis** - Friction losses, minor losses, system pressure requirements
- **Professional GUI** - User-friendly tkinter interface with Czech localization
- **Detailed Results Display** - Structured output with comprehensive engineering parameters
- **Auto-switching Interface** - Automatically switches to Results tab after calculations
- **Multiple Export Formats** - TXT, CSV, Excel reports with detailed calculations
- **Input Validation** - Comprehensive error checking with meaningful messages
- **JSON Configuration** - Save/load calculation parameters
- **Realistic Design Parameters** - Industry-standard limits and safety factors

## 📋 Requirements

- Python 3.7+
- tkinter (usually included with Python)
- pandas
- openpyxl (for Excel export)
- matplotlib (for charts)
- numpy

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/burner-dimension.git
cd burner-dimension
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## 💻 Usage

### GUI Application

Launch the main GUI application:
```bash
python main.py
```

The application provides 7 tabs for different calculation aspects:
1. **Vstupní parametry** (Input Parameters) - Define fuel type, flow rates, operating conditions
2. **Výpočty spalování** (Combustion Calculations) - View combustion analysis results
3. **Návrh hořáku** (Burner Design) - Burner sizing and design parameters
4. **Návrh komory** (Chamber Design) - Combustion chamber calculations
5. **Radiační přenos** (Radiation Transfer) - Heat transfer analysis
6. **Tlakové ztráty** (Pressure Losses) - System pressure analysis
7. **Výsledky** (Results) - Summary report with all calculations

### Command Line Usage

For automated calculations or integration with other tools:

```python
from src import CombustionCalculator, BurnerDesigner, ChamberDesigner

# Initialize calculators
combustion = CombustionCalculator()
burner = BurnerDesigner(combustion)
chamber = ChamberDesigner(combustion, burner)

# Perform calculations
fuel_type = "natural_gas"
fuel_flow = 0.01  # kg/s
results = combustion.calculate_combustion_products(fuel_type, fuel_flow)
```

## 📊 Supported Fuels

- **Natural Gas** - Standard composition with methane, ethane, propane
- **Pure Methane** - CH₄ with complete property database
- **Propane** - C₃H₈ for LPG applications

Each fuel includes comprehensive property data:
- Lower heating values (mass and volume basis)  
- Stoichiometric air requirements
- Density and molecular weight
- Air-fuel ratios

## 🔧 Calculation Modules

### Combustion Analysis (`src/combustion.py`)
- Stoichiometric air calculations
- Adiabatic flame temperature
- Flue gas composition (CO₂, O₂, H₂O, N₂)
- Excess air ratio effects

### Burner Design (`src/burner_design.py`)
- Burner diameter and area calculation
- Gas velocity optimization (5-100 m/s range)
- Pressure drop across burner
- Heat release density validation (up to 150 MW/m²)
- Flame length estimation
- Realistic sizing for 100 kW applications (≈49mm diameter)

### Chamber Design (`src/chamber_design.py`)
- Chamber volume based on residence time
- Heat transfer coefficients
- Wall temperature calculations
- Thermal efficiency analysis

### Radiation Heat Transfer (`src/radiation.py`)
- Stefan-Boltzmann law applications
- View factor calculations for cylindrical geometries
- Flame emissivity (CO₂, H₂O, soot particles)
- Multi-surface radiation exchange

### Pressure Loss Analysis (`src/pressure_losses.py`)
- Darcy-Weisbach friction factor calculations
- Minor losses from fittings and components
- Reynolds number and flow regime determination
- System pressure requirements

## 📁 File Structure

```
burner-calc/
├── main.py                 # Main application entry point
├── launch_gui.py           # Enhanced launcher with checks
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── PRD.md                # Product requirements document
├── CLAUDE.md             # Development instructions
├── src/                  # Core calculation modules
│   ├── __init__.py
│   ├── combustion.py     # Combustion calculations
│   ├── burner_design.py  # Burner dimensioning
│   ├── chamber_design.py # Chamber design
│   ├── radiation.py      # Radiation heat transfer
│   ├── pressure_losses.py # Pressure loss analysis
│   ├── visualization.py  # Charts and graphs
│   └── report.py         # Report generation
├── gui/                  # GUI application
│   └── gui.py           # Main GUI interface
├── data/                 # Configuration and data files
│   ├── fuels.json       # Fuel properties database
│   └── sample_input.json # Sample input parameters
├── output/              # Export directory for results
├── docs/                # Additional documentation
├── tests/               # Unit tests and validation
└── screenshots/         # GUI screenshots and demos
```

## 🧪 Testing

Run the test suite to verify installation:
```bash
python test_gui_setup.py
```

Demo calculation workflow:
```bash
python gui_demo.py
```

## 📤 Export Formats

### TXT Reports
Formatted text reports with all calculation results, suitable for documentation and archival.

### CSV Data
Structured data export for further analysis in spreadsheet applications or data processing tools.

### Excel Reports
Professional multi-sheet Excel workbooks with:
- Input parameters summary
- Detailed calculation results
- Charts and visualizations
- Design recommendations

## 🎯 Typical Applications

- **Industrial Furnace Design** - Sizing burners for heating applications
- **Process Heater Calculations** - Chemical and petrochemical industry
- **Boiler Burner Design** - Steam generation systems
- **Research & Development** - Combustion system optimization
- **Engineering Education** - Teaching combustion and heat transfer principles

## 🔒 Safety Features

- **Input Validation** - Comprehensive range checking and unit validation
- **Design Limits** - Built-in safety factors and operational limits
- **Warning Messages** - Alerts for potentially unsafe operating conditions
- **Recommendations** - Design guidance based on industry best practices

## 🌍 Localization

- **User Interface**: Czech language for ease of use
- **Technical Documentation**: English for international compatibility
- **Error Messages**: Czech with clear, actionable guidance
- **Export Reports**: Bilingual options available

## 📖 Documentation

- **README.md** - Project overview and usage guide
- **PRD.md** - Detailed product requirements and specifications
- **CLAUDE.md** - Development guidelines and coding standards
- **docs/** - Additional technical documentation and examples

## 🤝 Contributing

This project follows strict coding standards:
- Type hints for all functions and methods
- Comprehensive docstrings in English
- PEP 8 compliance with 88-character line limit
- Error handling with Czech user messages
- Unit tests for all calculation modules

## 📄 License

This project is developed for educational and professional engineering use. Please refer to the license terms for usage restrictions and permissions.

## 🔗 Related Projects

- Industrial combustion system design tools
- Heat transfer calculation software
- Pressure drop analysis utilities
- Thermal system optimization tools

## 📞 Support

For technical support, bug reports, or feature requests, please use the GitHub issue tracker or contact the development team.

---

**Professional Engineering Software for Gas Burner Design**  
*Accurate • Reliable • User-Friendly*