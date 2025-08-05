# Usage Examples and Tutorials

## Table of Contents
1. [Basic Usage Examples](#basic-usage-examples)
2. [GUI Tutorials](#gui-tutorials)
3. [Programming Examples](#programming-examples)
4. [Real-World Applications](#real-world-applications)
5. [Advanced Use Cases](#advanced-use-cases)
6. [Troubleshooting Examples](#troubleshooting-examples)

## Basic Usage Examples

### Example 1: Simple Natural Gas Burner Design

This example demonstrates designing a basic natural gas burner for a 100 kW application.

#### Input Parameters
```json
{
  "fuel_type": "natural_gas",
  "required_power": 100000,
  "supply_pressure": 3000,
  "excess_air_ratio": 1.2,
  "target_velocity": 25.0
}
```

#### GUI Steps
1. Open the application: `python main.py`
2. Navigate to **Input Parameters** tab
3. Set the following values:
   - Fuel Type: Natural Gas
   - Required Power: 100 kW
   - Supply Pressure: 3000 Pa
   - Excess Air Ratio: 1.2
4. Click **Calculate** button
5. Review results in **Results Summary** tab

#### Expected Results
- Burner diameter: ~75 mm
- Gas velocity: ~25 m/s
- Pressure drop: ~400 Pa
- Flame temperature: ~1900 K

### Example 2: Combustion Chamber Sizing

Designing a combustion chamber for the burner from Example 1.

#### Input Parameters
```json
{
  "required_power": 100000,
  "target_residence_time": 0.5,
  "wall_insulation_thickness": 0.1,
  "ambient_temperature": 293.15,
  "target_efficiency": 0.85
}
```

#### Expected Results
- Chamber volume: ~0.15 m³
- Chamber diameter: ~400 mm
- Chamber length: ~1200 mm
- Wall temperature: ~1200°C
- Thermal efficiency: ~87%

### Example 3: Pressure System Analysis

Analyzing pressure losses in a gas delivery system.

#### System Configuration
```json
{
  "pipe_segments": [
    {
      "length": 10.0,
      "diameter": 0.05,
      "material": "steel_new",
      "elevation_change": 2.0
    }
  ],
  "fittings": [
    {
      "type": "elbow_90_long",
      "quantity": 3,
      "diameter": 0.05
    },
    {
      "type": "gate_valve_open",
      "quantity": 1,
      "diameter": 0.05
    }
  ]
}
```

#### Expected Results
- Friction losses: ~150 Pa
- Minor losses: ~200 Pa
- Elevation losses: ~16 Pa
- Total pressure loss: ~366 Pa

## GUI Tutorials

### Tutorial 1: Complete Burner Design Process

#### Step 1: Project Setup
1. Launch the application
2. Go to **File** → **New Project**
3. Enter project name: "Industrial Burner Design"
4. Save project location

#### Step 2: Define Requirements
1. Open **Input Parameters** tab
2. Set design requirements:
   - Application: Industrial heating
   - Required power: 250 kW
   - Fuel: Natural gas
   - Operating pressure: 4000 Pa

#### Step 3: Combustion Analysis
1. Navigate to **Combustion Analysis** tab
2. Set excess air ratio: 1.15
3. Click **Calculate Combustion**
4. Review flame temperature and emissions

#### Step 4: Burner Dimensioning
1. Go to **Burner Design** tab
2. Set target velocity: 30 m/s
3. Click **Calculate Burner**
4. Check design validation results

#### Step 5: Chamber Design
1. Open **Chamber Design** tab
2. Set residence time: 0.6 seconds
3. Set insulation thickness: 120 mm
4. Click **Calculate Chamber**

#### Step 6: Pressure Analysis
1. Navigate to **Pressure Analysis** tab
2. Define pipe system layout
3. Add standard fittings
4. Calculate total pressure losses

#### Step 7: Results Review
1. Go to **Results Summary** tab
2. Review all calculations
3. Check validation warnings
4. Note design recommendations

#### Step 8: Report Generation
1. Click **Generate Report** button
2. Select output formats:
   - PDF report
   - Excel workbook
   - CSV data
3. Export visualization charts
4. Save project file

### Tutorial 2: Optimization Workflow

#### Objective
Optimize burner design for maximum efficiency while meeting pressure constraints.

#### Step 1: Baseline Design
1. Create initial design with standard parameters
2. Record baseline performance metrics
3. Identify optimization targets

#### Step 2: Parameter Sensitivity Analysis
1. Vary excess air ratio: 1.1, 1.15, 1.2, 1.25, 1.3
2. For each value, record:
   - Thermal efficiency
   - NOx formation potential
   - Pressure requirements
3. Plot results to identify trends

#### Step 3: Geometric Optimization
1. Test different L/D ratios: 2, 3, 4, 5
2. Vary chamber insulation: 80, 100, 120, 150 mm
3. Optimize residence time: 0.3, 0.5, 0.7, 1.0 s

#### Step 4: Multi-Objective Analysis
1. Create performance matrix:
   - Efficiency vs. Cost
   - Emissions vs. Pressure drop
   - Size vs. Performance
2. Identify Pareto optimal solutions

#### Step 5: Final Design Selection
1. Apply engineering judgment
2. Consider manufacturing constraints
3. Select optimal design point
4. Document design rationale

### Tutorial 3: Troubleshooting Design Issues

#### Common Issue 1: Excessive Pressure Drop
**Problem**: Total pressure drop exceeds available supply pressure

**Solution Steps**:
1. Analyze pressure distribution:
   - Check pipe sizing
   - Review fitting selections
   - Evaluate elevation changes
2. Optimization actions:
   - Increase pipe diameter
   - Reduce number of fittings
   - Select low-loss components
3. Verification:
   - Recalculate system
   - Check safety margins
   - Validate flow rates

#### Common Issue 2: Poor Combustion Efficiency
**Problem**: Thermal efficiency below target value

**Diagnostic Steps**:
1. Check heat losses:
   - Review insulation thickness
   - Verify material properties
   - Calculate wall temperatures
2. Optimize combustion:
   - Adjust excess air ratio
   - Verify residence time
   - Check mixing quality
3. Improve design:
   - Increase insulation
   - Optimize chamber geometry
   - Consider heat recovery

## Programming Examples

### Example 1: Automated Calculation Script

```python
#!/usr/bin/env python3
"""
Automated burner calculation script
Demonstrates programmatic use of calculation modules
"""

from src.combustion import CombustionCalculator
from src.burner_design import BurnerDesigner
from src.chamber_design import ChamberDesigner
from src.report import BurnerReportGenerator

def calculate_burner_system(config):
    """
    Complete burner system calculation
    
    Args:
        config (dict): Calculation parameters
        
    Returns:
        dict: Complete calculation results
    """
    
    # Initialize calculators
    combustion_calc = CombustionCalculator()
    burner_designer = BurnerDesigner(combustion_calc)
    chamber_designer = ChamberDesigner(combustion_calc)
    
    # Extract parameters
    fuel_type = config['fuel_type']
    power = config['required_power']
    pressure = config['supply_pressure']
    excess_air = config.get('excess_air_ratio', 1.2)
    residence_time = config.get('residence_time', 0.5)
    
    # Combustion calculations
    fuel_flow = power / combustion_calc.get_fuel_properties(fuel_type)['properties']['lower_heating_value_mass']
    combustion_results = combustion_calc.calculate_combustion_products(
        fuel_type, fuel_flow, excess_air
    )
    
    # Burner design
    burner_results = burner_designer.design_burner(
        fuel_type=fuel_type,
        required_power=power,
        supply_pressure=pressure,
        excess_air_ratio=excess_air
    )
    
    # Chamber design
    chamber_results = chamber_designer.design_chamber(
        fuel_type=fuel_type,
        required_power=power,
        target_residence_time=residence_time
    )
    
    # Compile results
    results = {
        'combustion': combustion_results,
        'burner': burner_results,
        'chamber': chamber_results,
        'validation': {
            'burner_valid': burner_designer.validate_design(burner_results),
            'chamber_valid': chamber_designer.validate_design(chamber_results)
        }
    }
    
    return results

# Example usage
if __name__ == "__main__":
    # Configuration
    config = {
        'fuel_type': 'natural_gas',
        'required_power': 150000,  # 150 kW
        'supply_pressure': 4000,   # 4000 Pa
        'excess_air_ratio': 1.15,
        'residence_time': 0.6
    }
    
    # Calculate
    results = calculate_burner_system(config)
    
    # Display key results
    print(f"Burner diameter: {results['burner'].burner_diameter*1000:.1f} mm")
    print(f"Chamber volume: {results['chamber'].chamber_volume:.3f} m³")
    print(f"Thermal efficiency: {results['chamber'].thermal_efficiency:.1f}%")
    print(f"Flame temperature: {results['combustion'].adiabatic_flame_temperature:.0f} K")
```

### Example 2: Parametric Study Script

```python
#!/usr/bin/env python3
"""
Parametric study of excess air ratio effects
"""

import numpy as np
import matplotlib.pyplot as plt
from src.combustion import CombustionCalculator
from src.chamber_design import ChamberDesigner

def excess_air_study():
    """Study effect of excess air ratio on performance"""
    
    # Initialize
    combustion_calc = CombustionCalculator()
    chamber_designer = ChamberDesigner(combustion_calc)
    
    # Parameters
    fuel_type = 'natural_gas'
    power = 100000  # 100 kW
    excess_air_ratios = np.linspace(1.05, 1.5, 20)
    
    # Storage arrays
    flame_temps = []
    efficiencies = []
    co2_levels = []
    o2_levels = []
    
    # Calculate for each excess air ratio
    for lambda_ratio in excess_air_ratios:
        # Combustion calculation
        fuel_flow = power / combustion_calc.get_fuel_properties(fuel_type)['properties']['lower_heating_value_mass']
        combustion_result = combustion_calc.calculate_combustion_products(
            fuel_type, fuel_flow, lambda_ratio
        )
        
        # Chamber calculation
        chamber_result = chamber_designer.design_chamber(
            fuel_type=fuel_type,
            required_power=power,
            target_residence_time=0.5
        )
        
        # Store results
        flame_temps.append(combustion_result.adiabatic_flame_temperature)
        efficiencies.append(chamber_result.thermal_efficiency)
        co2_levels.append(combustion_result.co2_volume_percent)
        o2_levels.append(combustion_result.o2_volume_percent)
    
    # Create plots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    # Flame temperature
    ax1.plot(excess_air_ratios, flame_temps, 'b-', linewidth=2)
    ax1.set_xlabel('Excess Air Ratio')
    ax1.set_ylabel('Flame Temperature [K]')
    ax1.set_title('Flame Temperature vs Excess Air')
    ax1.grid(True)
    
    # Thermal efficiency
    ax2.plot(excess_air_ratios, efficiencies, 'r-', linewidth=2)
    ax2.set_xlabel('Excess Air Ratio')
    ax2.set_ylabel('Thermal Efficiency [%]')
    ax2.set_title('Efficiency vs Excess Air')
    ax2.grid(True)
    
    # CO2 levels
    ax3.plot(excess_air_ratios, co2_levels, 'g-', linewidth=2)
    ax3.set_xlabel('Excess Air Ratio')
    ax3.set_ylabel('CO₂ Content [%]')
    ax3.set_title('CO₂ vs Excess Air')
    ax3.grid(True)
    
    # O2 levels
    ax4.plot(excess_air_ratios, o2_levels, 'm-', linewidth=2)
    ax4.set_xlabel('Excess Air Ratio')
    ax4.set_ylabel('O₂ Content [%]')
    ax4.set_title('O₂ vs Excess Air')
    ax4.grid(True)
    
    plt.tight_layout()
    plt.savefig('excess_air_study.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Find optimal point
    optimal_idx = np.argmax(efficiencies)
    optimal_lambda = excess_air_ratios[optimal_idx]
    optimal_efficiency = efficiencies[optimal_idx]
    
    print(f"Optimal excess air ratio: {optimal_lambda:.2f}")
    print(f"Maximum efficiency: {optimal_efficiency:.1f}%")

if __name__ == "__main__":
    excess_air_study()
```

### Example 3: Batch Processing Script

```python
#!/usr/bin/env python3
"""
Batch processing of multiple burner designs
"""

import json
import os
from datetime import datetime
from src.combustion import CombustionCalculator
from src.burner_design import BurnerDesigner
from src.report import BurnerReportGenerator

def batch_process_designs(input_directory, output_directory):
    """
    Process multiple design files in batch
    
    Args:
        input_directory (str): Directory containing input JSON files
        output_directory (str): Directory for output reports
    """
    
    # Initialize calculators
    combustion_calc = CombustionCalculator()
    burner_designer = BurnerDesigner(combustion_calc)
    report_generator = BurnerReportGenerator(output_directory)
    
    # Process each JSON file
    for filename in os.listdir(input_directory):
        if not filename.endswith('.json'):
            continue
            
        print(f"Processing: {filename}")
        
        try:
            # Load configuration
            with open(os.path.join(input_directory, filename), 'r') as f:
                config = json.load(f)
            
            # Perform calculations
            results = calculate_design(config, combustion_calc, burner_designer)
            
            # Generate report
            report_name = f"report_{filename.replace('.json', '')}"
            report_generator.generate_comprehensive_report(
                results, report_name
            )
            
            print(f"✓ Completed: {filename}")
            
        except Exception as e:
            print(f"✗ Error processing {filename}: {e}")
            continue

def calculate_design(config, combustion_calc, burner_designer):
    """Calculate design from configuration"""
    
    # Extract parameters
    fuel_type = config['fuel_type']
    power = config['required_power']
    pressure = config['supply_pressure']
    
    # Perform calculations
    fuel_flow = power / combustion_calc.get_fuel_properties(fuel_type)['properties']['lower_heating_value_mass']
    
    combustion_results = combustion_calc.calculate_combustion_products(
        fuel_type, fuel_flow, config.get('excess_air_ratio', 1.2)
    )
    
    burner_results = burner_designer.design_burner(
        fuel_type=fuel_type,
        required_power=power,
        supply_pressure=pressure
    )
    
    return {
        'config': config,
        'combustion': combustion_results,
        'burner': burner_results,
        'timestamp': datetime.now().isoformat()
    }

# Example usage
if __name__ == "__main__":
    batch_process_designs("input_designs", "batch_output")
```

## Real-World Applications

### Application 1: Industrial Furnace Burner

#### Background
Design a burner system for a steel reheat furnace requiring 2 MW thermal input.

#### Requirements
- Fuel: Natural gas
- Power: 2,000 kW
- Operating temperature: 1200°C
- Emissions: Low NOx
- Pressure: Limited to 5 kPa supply

#### Solution Approach
1. **High-power considerations**:
   - Multiple burner configuration
   - Enhanced mixing requirements
   - Thermal stress management

2. **Design parameters**:
   ```json
   {
     "fuel_type": "natural_gas",
     "required_power": 2000000,
     "supply_pressure": 5000,
     "excess_air_ratio": 1.05,
     "target_velocity": 40,
     "burner_count": 4
   }
   ```

3. **Special considerations**:
   - Reduced excess air for NOx control
   - Higher velocity for better mixing
   - Multiple smaller burners vs. single large burner

#### Results Analysis
- Individual burner power: 500 kW each
- Burner diameter: ~120 mm each
- Total gas flow: ~0.04 kg/s
- System pressure drop: ~3.2 kPa

### Application 2: Process Heater Design

#### Background
Thermal oil heater for chemical processing, requiring precise temperature control.

#### Requirements
- Fuel: Natural gas or propane flexibility
- Power: 500 kW
- Temperature precision: ±5°C
- High efficiency: >90%
- Compact design

#### Design Strategy
1. **Fuel flexibility**:
   - Dual-fuel capability
   - Automatic fuel switching
   - Optimized combustion for each fuel

2. **Control system**:
   - Modulating burner design
   - Turndown ratio: 4:1
   - Electronic flame control

3. **Efficiency optimization**:
   - Minimal excess air
   - Heat recovery integration
   - Advanced insulation

### Application 3: Boiler Retrofit

#### Background
Upgrade existing coal boiler to natural gas operation.

#### Constraints
- Existing combustion chamber dimensions
- Limited structural modifications
- Maintain original capacity: 10 MW
- Improve emissions performance

#### Retrofit Approach
1. **Adaptation calculations**:
   - Existing chamber: 3m diameter × 8m length
   - Required modifications for gas firing
   - Burner placement optimization

2. **Performance comparison**:
   - Original coal system efficiency
   - Projected gas system efficiency
   - Emissions reduction potential

3. **Implementation plan**:
   - Phased installation approach
   - Commissioning procedure
   - Performance verification

## Advanced Use Cases

### Use Case 1: Oxy-Fuel Combustion

#### Concept
Replace air with oxygen-enriched oxidizer for enhanced performance.

#### Modifications Required
1. **Combustion calculations**:
   - Modified stoichiometric ratios
   - Higher flame temperatures
   - Different product compositions

2. **Safety considerations**:
   - Oxygen handling requirements
   - Material compatibility
   - Explosion risk mitigation

3. **Performance benefits**:
   - Reduced flue gas volumes
   - Higher thermal efficiency
   - Easier CO₂ capture

### Use Case 2: Hydrogen-Natural Gas Blends

#### Background
Evaluate performance with hydrogen blending for carbon reduction.

#### Analysis Parameters
- Hydrogen content: 0-30% by volume
- Combustion characteristics changes
- Burner design modifications needed
- Safety implications

#### Calculation Modifications
```python
def blend_properties(h2_fraction, ng_fraction=None):
    """Calculate properties of H2-NG blend"""
    if ng_fraction is None:
        ng_fraction = 1.0 - h2_fraction
    
    # Weighted properties
    lhv_blend = h2_fraction * LHV_H2 + ng_fraction * LHV_NG
    density_blend = h2_fraction * rho_H2 + ng_fraction * rho_NG
    
    return lhv_blend, density_blend
```

### Use Case 3: High-Altitude Operation

#### Challenges
- Reduced air density
- Changed combustion characteristics
- Modified heat transfer rates

#### Calculation Adjustments
```python
def altitude_correction(altitude_m):
    """Apply altitude corrections to combustion calculations"""
    # Atmospheric pressure correction
    p_ratio = (1 - 0.0065 * altitude_m / 288.15) ** 5.255
    
    # Air density correction
    rho_correction = p_ratio
    
    # Combustion adjustments
    air_flow_correction = 1 / rho_correction
    
    return p_ratio, rho_correction, air_flow_correction
```

## Troubleshooting Examples

### Problem 1: Calculation Convergence Issues

#### Symptoms
- Iterative calculations not converging
- Results oscillating between values
- Excessive computation time

#### Diagnosis Steps
```python
def diagnose_convergence(iterations, values, criteria):
    """Diagnose convergence problems"""
    
    # Check iteration history
    if len(values) > 10:
        recent_change = abs(values[-1] - values[-2]) / values[-1]
        if recent_change > criteria:
            print(f"Poor convergence: change = {recent_change:.2e}")
    
    # Check for oscillation
    if len(values) > 4:
        if (values[-1] - values[-3]) * (values[-2] - values[-4]) < 0:
            print("Oscillation detected")
    
    return recent_change < criteria
```

#### Solutions
1. Adjust convergence criteria
2. Implement relaxation factors
3. Use better initial guesses
4. Check input parameter validity

### Problem 2: Unrealistic Results

#### Symptoms
- Extremely high temperatures
- Negative pressures
- Invalid material properties

#### Validation Checks
```python
def validate_results(results):
    """Comprehensive result validation"""
    
    warnings = []
    errors = []
    
    # Temperature checks
    if results.flame_temperature > 2500:
        warnings.append("Flame temperature unusually high")
    
    if results.wall_temperature > 1800:
        errors.append("Wall temperature exceeds material limits")
    
    # Pressure checks
    if results.pressure_drop < 0:
        errors.append("Negative pressure drop - check calculation")
    
    # Physical reasonableness
    if results.efficiency > 100:
        errors.append("Efficiency > 100% - energy balance error")
    
    return warnings, errors
```

### Problem 3: GUI Performance Issues

#### Symptoms
- Slow response to user input
- Freezing during calculations
- Memory consumption growth

#### Performance Optimization
```python
import threading
from concurrent.futures import ThreadPoolExecutor

def async_calculation(calculation_func, *args, **kwargs):
    """Run calculations in separate thread"""
    
    def worker():
        try:
            result = calculation_func(*args, **kwargs)
            return {'success': True, 'result': result}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # Use thread pool for calculation
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(worker)
        return future
```

---

*These examples provide practical guidance for using the Gas Burner Calculator in various scenarios. For additional examples or specific use cases, consult the API reference or contact the development team.*