# Gas Burner and Combustion Chamber Design Calculator

A comprehensive Python application for calculating and designing gas burners and combustion chambers. This tool provides detailed technical calculations for combustion analysis, burner dimensioning, chamber design, radiation heat transfer, and pressure loss analysis.

## Features

### Core Calculations
- **Combustion Analysis**: Complete stoichiometric calculations for various gaseous fuels
- **Burner Design**: Dimensional calculations for gas burners including nozzle sizing
- **Chamber Design**: Combustion chamber volume and geometry optimization
- **Radiation Heat Transfer**: Detailed radiative heat exchange calculations
- **Pressure Loss Analysis**: Comprehensive pressure drop calculations throughout the system

### User Interface
- **GUI Application**: User-friendly tkinter-based graphical interface
- **Input Validation**: Comprehensive error checking and user feedback
- **JSON Configuration**: Flexible fuel property configuration system
- **Multi-language Support**: Czech language output with English technical documentation

### Output Capabilities
- **Multiple Report Formats**: TXT, CSV, and Excel exports
- **Advanced Visualizations**: Charts and graphs in PNG, PDF, and JPEG formats
- **Technical Drawings**: Burner and chamber geometry visualizations
- **Dashboard Views**: Comprehensive summary dashboards

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start
1. Clone the repository:
```bash
git clone https://github.com/yourusername/burner-dimension.git
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

### Dependencies
- `numpy>=1.20.0` - Numerical computations
- `pandas>=1.3.0` - Data manipulation and analysis
- `matplotlib>=3.5.0` - Plotting and visualization
- `openpyxl>=3.0.0` - Excel file support
- `scipy>=1.7.0` - Advanced numerical methods

## Usage

### GUI Mode (Recommended)
Launch the graphical interface:
```bash
python main.py
```

The GUI provides:
- Input parameter forms
- Real-time calculation validation
- Interactive result visualization
- Export options for reports and charts

### Programmatic Usage
```python
from src.combustion import CombustionCalculator
from src.burner_design import BurnerDesign
from src.chamber_design import ChamberDesign
from src.radiation import RadiationCalculator
from src.pressure_losses import PressureLossCalculator

# Initialize calculators
combustion_calc = CombustionCalculator()
burner_calc = BurnerDesign()
chamber_calc = ChamberDesign()
radiation_calc = RadiationCalculator()
pressure_calc = PressureLossCalculator()

# Perform calculations
combustion_result = combustion_calc.calculate(fuel_data, excess_air=1.2)
burner_result = burner_calc.calculate(power=100, fuel_type="natural_gas")
# ... additional calculations
```

## Project Structure

```
burner-dimension/
├── main.py                    # Main application entry point
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore configuration
├── README.md                 # This file
├── PRD.md                    # Product Requirements Document
├── src/                      # Core calculation modules
│   ├── __init__.py
│   ├── combustion.py         # Combustion calculations
│   ├── burner_design.py      # Burner design calculations
│   ├── chamber_design.py     # Chamber design calculations
│   ├── radiation.py          # Radiation heat transfer
│   ├── pressure_losses.py    # Pressure loss calculations
│   ├── visualization.py      # Chart and graph generation
│   └── report.py            # Report generation
├── gui/                      # User interface
│   ├── __init__.py
│   └── gui.py               # Main GUI application
├── data/                     # Configuration and data files
│   └── fuels.json           # Fuel properties database
├── output/                   # Generated reports and charts
├── tests/                    # Unit tests
├── docs/                     # Documentation
└── .github/                  # GitHub workflows and configurations
```

## Configuration

### Fuel Properties
The application uses a JSON configuration file (`data/fuels.json`) to define fuel properties:

```json
{
  "natural_gas": {
    "name": "Zemní plyn",
    "heating_value": 35.8,
    "density": 0.717,
    "composition": {
      "CH4": 95.0,
      "C2H6": 3.0,
      "C3H8": 1.0,
      "N2": 1.0
    }
  }
}
```

### Input Parameters
Key input parameters include:
- Fuel type and properties
- Burner power rating (kW)
- Excess air ratio
- Operating temperature and pressure
- Chamber geometry constraints
- Heat transfer requirements

## Output Examples

### Text Report
```
ZPRÁVA O VÝPOČTU PLYNOVÉHO HOŘÁKU A SPALOVACÍ KOMORY
================================================================================

VSTUPNÍ PARAMETRY
----------------------------------------
Typ paliva: Zemní plyn
Výkon hořáku: 100 kW
Přebytek vzduchu: 20 %
...

ANALÝZA SPALOVÁNÍ
----------------------------------------
Teoretické množství vzduchu: 9.52 m³/m³
Skutečné množství vzduchu: 11.42 m³/m³
Teplota spalování: 1850 °C
...
```

### Visualization Examples
- Combustion analysis charts showing air-fuel ratios and product composition
- Temperature distribution heat maps
- Pressure loss diagrams
- Burner geometry technical drawings
- Comprehensive dashboard summaries

## Testing

Run the test suite:
```bash
python -m pytest tests/ -v
```

For coverage analysis:
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

## Development

### Code Quality
The project maintains high code quality standards:
- PEP 8 compliance checked with `flake8`
- Security analysis with `bandit`
- Type hints throughout the codebase
- Comprehensive docstrings and comments

### Pre-commit Hooks
Install development tools:
```bash
pip install pre-commit pytest-cov flake8 bandit black
pre-commit install
```

### Adding New Features
1. Create feature branch
2. Implement changes with tests
3. Run quality checks: `make ci-local`
4. Submit pull request

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes with appropriate tests
4. Ensure all quality checks pass
5. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Use type hints for all functions
- Write comprehensive docstrings
- Add unit tests for new functionality

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation in the `docs/` directory
- Review the Product Requirements Document (PRD.md)

## Changelog

### Version 1.0.0
- Initial release
- Complete combustion calculations
- GUI application with tkinter
- Multiple export formats
- Comprehensive visualization suite
- Full documentation and testing

## Acknowledgments

- Developed using modern Python scientific computing stack
- GUI framework: tkinter
- Visualization: matplotlib
- Data processing: pandas and numpy
- Documentation: Sphinx-compatible docstrings

---

*This application provides professional-grade calculations for gas burner and combustion chamber design. Always validate results with appropriate engineering standards and safety requirements.*