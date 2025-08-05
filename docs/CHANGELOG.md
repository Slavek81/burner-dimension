# Changelog

## [1.1.0] - 2025-01-05

### Added
- **Detailed Results Display**: Structured output with comprehensive engineering parameters
- **Auto-switching Interface**: Automatically switches to Results tab after calculations complete
- **Enhanced Burner Design**: Realistic sizing with industry-standard parameters
- **Improved Output Sections**: Multi-section results display for better organization

### Changed
- **Heat Release Density Limit**: Increased from 80 MW/m² to 150 MW/m² for industrial applications
- **Default GUI Values**: Adjusted to more realistic parameters (100 kW, 0.002 kg/s fuel flow)
- **Results Structure**: Enhanced with geometry, thermal, and pressure analysis sections
- **Combustion Results**: Added mass flows in kg/h and detailed combustion ratios
- **Burner Results**: Added L/D ratios, pressure reserves, and flame parameters
- **Chamber Results**: Added volume in liters, temperature in °C, and thermal loss analysis

### Fixed
- **Unrealistic Calculations**: Corrected fundamental calculation error in gas flow computation
- **GUI Syntax Error**: Removed unmatched parenthesis causing startup failure
- **Test Suite**: Updated tests to reflect new heat density limits
- **Code Quality**: Removed whitespace issues and duplicate code sections

### Technical Improvements
- **Gas Density Calculation**: Now uses mixture density (fuel + air) instead of pure fuel density
- **Volume Flow Calculation**: Uses total gas flow (fuel + air) for accurate burner sizing
- **Input Validation**: Enhanced error checking with meaningful Czech messages
- **Design Validation**: Improved criteria for realistic burner dimensions

### Results
- **Realistic Burner Sizing**: 100 kW application now yields 49mm diameter (previously >3000mm)
- **Proper Heat Density**: 54 MW/m² for 100 kW (within industrial standards)
- **Improved User Experience**: Automatic result viewing and detailed technical information
- **Professional Output**: Industry-standard formatting with comprehensive parameters

## [1.0.0] - 2024-12-XX

### Initial Release
- Complete combustion analysis calculations
- Burner design and dimensioning
- Combustion chamber design
- Radiation heat transfer calculations
- Pressure loss analysis
- Professional GUI with Czech localization
- Multiple export formats (TXT, CSV, Excel)
- JSON configuration support
- Comprehensive test suite