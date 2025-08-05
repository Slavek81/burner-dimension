# Gas Burner Calculator - User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [GUI Interface Overview](#gui-interface-overview)
4. [Input Parameters](#input-parameters)
5. [Calculation Results](#calculation-results)
6. [Data Import/Export](#data-importexport)
7. [Visualization Features](#visualization-features)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)

## Introduction

The Gas Burner Calculator is a comprehensive engineering tool designed for the thermal design and analysis of gas burners and combustion chambers. It provides accurate calculations for:

- Combustion stoichiometry and flame characteristics
- Burner dimensioning and pressure requirements
- Combustion chamber design and heat transfer
- Radiation heat transfer calculations
- Pressure loss analysis throughout the gas system

## Getting Started

### System Requirements
- Python 3.8 or higher
- Windows, macOS, or Linux operating system
- Minimum 4GB RAM
- Display resolution: 1024x768 or higher

### Launching the Application

1. **From Python environment:**
   ```bash
   python main.py
   ```

2. **Using the launcher script:**
   ```bash
   python launch_gui.py
   ```

3. **Direct GUI launch:**
   ```bash
   python gui/gui.py
   ```

The application will open in a new window with the main interface.

## GUI Interface Overview

### Main Window Layout

The application features a tabbed interface with the following sections:

#### 1. Input Parameters Tab
- **Fuel Selection**: Choose from available fuel types
- **Power Requirements**: Specify thermal power output
- **Operating Conditions**: Set pressure, temperature, and air ratios
- **Geometry Parameters**: Define chamber and burner dimensions

#### 2. Combustion Analysis Tab
- **Stoichiometric Calculations**: Air-fuel ratios and flow rates
- **Flame Properties**: Temperature and composition analysis
- **Combustion Products**: Flue gas analysis and emissions

#### 3. Burner Design Tab
- **Dimensional Calculations**: Diameter, length, and area sizing
- **Flow Analysis**: Velocity and pressure drop calculations
- **Design Validation**: Safety checks and recommendations

#### 4. Chamber Design Tab
- **Volume Calculations**: Based on residence time requirements
- **Heat Transfer Analysis**: Wall temperatures and efficiency
- **Thermal Performance**: Heat losses and insulation requirements

#### 5. Pressure Analysis Tab
- **System Components**: Pipe segments and fittings definition
- **Loss Calculations**: Friction, minor, and elevation losses
- **Optimization Tools**: Diameter and pressure optimization

#### 6. Results Summary Tab
- **Comprehensive Overview**: All calculation results
- **Performance Metrics**: Key design parameters
- **Validation Status**: Design compliance checks

### Control Buttons

- **Calculate**: Execute all calculations with current parameters
- **Reset**: Clear all inputs and results
- **Load**: Import calculation data from JSON file
- **Save**: Export current setup to JSON file
- **Generate Report**: Create comprehensive output reports
- **Export Charts**: Save visualization plots

## Input Parameters

### Fuel Properties
Select from predefined fuel types or customize properties:

- **Natural Gas**: Standard pipeline gas composition
- **Methane**: Pure methane properties
- **Propane**: Commercial propane characteristics

**Key Properties:**
- Lower Heating Value (LHV): Energy content per unit mass
- Molecular Weight: For density calculations
- Air-Fuel Ratio: Stoichiometric requirements

### Operating Conditions

#### Power Requirements
- **Thermal Power [kW]**: Desired heat output from burner
- **Range**: Typically 10 kW to 1000 kW for industrial applications

#### Pressure Settings
- **Supply Pressure [Pa]**: Available gas pressure at inlet
- **Operating Pressure [Pa]**: Pressure at burner inlet
- **Typical Values**: 2000-5000 Pa for low-pressure systems

#### Air Conditions
- **Excess Air Ratio**: Lambda value (typically 1.1-1.3)
- **Air Temperature [°C]**: Combustion air temperature
- **Humidity**: Air moisture content (if applicable)

### Geometry Parameters

#### Burner Configuration
- **Target Velocity [m/s]**: Gas exit velocity (10-50 m/s typical)
- **Burner Type**: Single or multiple nozzle configuration
- **Mixing Method**: Premixed or diffusion combustion

#### Chamber Dimensions
- **Residence Time [s]**: Gas retention time (0.1-2.0 s typical)
- **Length/Diameter Ratio**: Chamber geometry factor (2-5 typical)
- **Insulation Thickness [m]**: Refractory lining thickness

## Calculation Results

### Combustion Analysis Results

#### Flow Rates
- **Fuel Flow Rate [kg/s]**: Mass flow of fuel required
- **Air Flow Rate [kg/s]**: Combustion air requirement
- **Flue Gas Flow Rate [kg/s]**: Total combustion products

#### Flame Characteristics
- **Adiabatic Flame Temperature [K]**: Theoretical maximum temperature
- **Actual Flame Temperature [K]**: Considering heat losses
- **Flame Length [m]**: Estimated flame dimensions

#### Emissions Analysis
- **CO₂ Content [%]**: Carbon dioxide in flue gas
- **O₂ Content [%]**: Excess oxygen level
- **NOₓ Estimation**: Nitrogen oxide formation potential

### Burner Design Results

#### Physical Dimensions
- **Burner Diameter [mm]**: Required nozzle diameter
- **Burner Length [mm]**: Recommended burner length
- **Cross-sectional Area [mm²]**: Flow area

#### Performance Parameters
- **Gas Velocity [m/s]**: Actual exit velocity
- **Pressure Drop [Pa]**: Burner pressure loss
- **Heat Release Density [MW/m²]**: Thermal intensity

### Chamber Design Results

#### Volume and Geometry
- **Chamber Volume [m³]**: Required combustion volume
- **Chamber Diameter [m]**: Internal diameter
- **Chamber Length [m]**: Axial length

#### Thermal Performance
- **Wall Temperature [°C]**: Inner surface temperature
- **Heat Transfer Coefficient [W/m²K]**: Overall heat transfer
- **Thermal Efficiency [%]**: Energy utilization efficiency

### Pressure Loss Analysis

#### System Components
- **Friction Losses [Pa]**: Pipe wall friction
- **Minor Losses [Pa]**: Fittings and components
- **Elevation Losses [Pa]**: Hydrostatic pressure changes

#### Flow Characteristics
- **Reynolds Number**: Flow regime indicator
- **Friction Factor**: Darcy-Weisbach coefficient
- **System Resistance Coefficient**: Overall K-factor

## Data Import/Export

### Input Data Format (JSON)

The application uses JSON format for input data:

```json
{
  "fuel_type": "natural_gas",
  "required_power": 100000,
  "supply_pressure": 3000,
  "excess_air_ratio": 1.2,
  "target_residence_time": 0.5,
  "chamber_insulation_thickness": 0.1,
  "pipe_segments": [
    {
      "length": 10.0,
      "diameter": 0.05,
      "material": "steel_new",
      "elevation_change": 0.0
    }
  ],
  "fittings": [
    {
      "type": "elbow_90_long",
      "quantity": 2,
      "diameter": 0.05
    }
  ]
}
```

### Output Formats

#### Text Reports (.txt)
- Human-readable summary
- Complete calculation results
- Design recommendations
- Input parameter summary

#### CSV Data (.csv)
- Tabular data format
- Suitable for spreadsheet analysis
- Multiple data tables
- Easy data manipulation

#### Excel Workbooks (.xlsx)
- Multiple worksheets
- Formatted tables and charts
- Professional presentation
- Advanced data analysis features

### Chart Exports

Visualization charts can be exported in multiple formats:
- **PDF**: Vector format for publications
- **PNG**: High-resolution bitmap
- **JPEG**: Compressed bitmap format

## Visualization Features

### Combustion Analysis Charts

#### Flame Temperature Distribution
- Axial temperature profile
- Radial temperature gradients
- Heat release visualization

#### Gas Composition Plots
- Flue gas analysis
- Excess air optimization
- Emissions tracking

### Pressure Loss Visualization

#### System Schematic
- Pipe network diagram
- Component identification
- Flow direction indicators

#### Pressure Profile
- Pressure drop distribution
- Major loss contributors
- Optimization opportunities

### Burner Geometry Plots

#### Cross-sectional Views
- Burner configuration
- Flow patterns
- Mixing characteristics

#### 3D Visualization
- Chamber geometry
- Flame envelope
- Heat transfer surfaces

## Troubleshooting

### Common Issues

#### Calculation Errors

**Problem**: "Insufficient gas pressure" error
**Solution**: 
- Increase supply pressure
- Reduce system pressure losses
- Check pipe sizing

**Problem**: "Flame temperature too high" warning
**Solution**:
- Increase excess air ratio
- Check fuel type selection
- Verify input parameters

**Problem**: "Residence time too short" error
**Solution**:
- Increase chamber volume
- Reduce gas flow rates
- Adjust chamber geometry

#### Interface Issues

**Problem**: Charts not displaying
**Solution**:
- Check matplotlib installation
- Verify output directory permissions
- Update graphics drivers

**Problem**: Export functions failing
**Solution**:
- Check file permissions
- Verify output directory exists
- Ensure sufficient disk space

### Input Validation

The application performs extensive input validation:

#### Range Checking
- Power: 1 kW to 10 MW
- Pressure: 100 Pa to 100 kPa
- Temperature: 0°C to 2000°C
- Excess air: 1.0 to 3.0

#### Physical Constraints
- Velocity limits for safe operation
- Pressure drop within acceptable ranges
- Temperature limits for materials
- Geometric feasibility checks

### Error Messages

#### Critical Errors
- **Red indicators**: Calculation cannot proceed
- **Detailed descriptions**: Specific problem identification
- **Suggested solutions**: Recommended corrective actions

#### Warnings
- **Yellow indicators**: Calculation proceeds with caution
- **Performance alerts**: Suboptimal operating conditions
- **Design recommendations**: Suggested improvements

## Best Practices

### Input Data Guidelines

#### Fuel Selection
- Use standard fuel properties when possible
- Verify heating values with supplier data
- Consider seasonal variations in gas composition

#### Operating Conditions
- Allow 20-30% safety margin in pressure
- Consider ambient temperature variations
- Account for altitude effects on air density

#### Geometry Constraints
- Maintain practical length/diameter ratios
- Consider manufacturing limitations
- Allow for thermal expansion

### Design Optimization

#### Efficiency Maximization
- Optimize excess air ratio (typically 1.1-1.2)
- Minimize heat losses through insulation
- Balance residence time with chamber size

#### Safety Considerations
- Maintain adequate safety factors
- Consider emergency shutdown requirements
- Ensure proper ventilation
- Design for pressure relief

#### Cost Optimization
- Balance initial cost with operating efficiency
- Consider maintenance accessibility
- Evaluate lifecycle costs
- Plan for future capacity changes

### Reporting Guidelines

#### Documentation Standards
- Include all input assumptions
- Document calculation methods
- Provide design recommendations
- Include safety considerations

#### Quality Assurance
- Verify all input parameters
- Cross-check critical results
- Review design recommendations
- Validate against industry standards

---

*For additional support or questions about specific calculations, refer to the technical documentation or contact the development team.*