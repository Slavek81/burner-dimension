# Calculation Methods and Mathematical Formulas

## Table of Contents
1. [Overview](#overview)
2. [Combustion Calculations](#combustion-calculations)
3. [Burner Design Calculations](#burner-design-calculations)
4. [Chamber Design Calculations](#chamber-design-calculations)
5. [Radiation Heat Transfer](#radiation-heat-transfer)
6. [Pressure Loss Calculations](#pressure-loss-calculations)
7. [Physical Constants and Properties](#physical-constants-and-properties)
8. [Validation Methods](#validation-methods)

## Overview

This document provides a comprehensive description of all mathematical methods and formulas used in the Gas Burner Calculator. Each calculation is based on established engineering principles and industry-standard methods.

### Notation and Units

#### Symbols Used
- **ṁ** = mass flow rate [kg/s]
- **V̇** = volumetric flow rate [m³/s]
- **Q** = heat transfer rate [W]
- **T** = temperature [K]
- **P** = pressure [Pa]
- **ρ** = density [kg/m³]
- **μ** = dynamic viscosity [Pa·s]
- **λ** = excess air ratio [-]
- **ε** = emissivity [-]
- **σ** = Stefan-Boltzmann constant [W/m²K⁴]

#### Unit System
All calculations use SI base units unless otherwise specified.

## Combustion Calculations

### Stoichiometric Air Requirement

The theoretical air requirement for complete combustion is calculated based on fuel composition:

#### For Hydrocarbon Fuels (CₓHᵧ)
```
Stoichiometric air requirement:
A₀ = (x + y/4) × 4.76 × 22.4/12.01 × ρ_air/ρ_fuel

Where:
- x = number of carbon atoms
- y = number of hydrogen atoms  
- 4.76 = accounting for nitrogen in air (1/0.21)
- 22.4 = molar volume at STP [L/mol]
- 12.01 = carbon atomic weight [g/mol]
```

#### Mass-based Air-Fuel Ratio
```
AFR_mass = ṁ_air / ṁ_fuel

For natural gas (CH₄):
AFR_mass ≈ 17.2
```

### Actual Air Flow Calculation

```
ṁ_air,actual = λ × ṁ_air,stoichiometric

Where:
λ = excess air ratio (typically 1.1 - 1.3)
```

### Combustion Products Flow Rate

```
ṁ_flue_gas = ṁ_fuel + ṁ_air,actual
```

### Adiabatic Flame Temperature

The adiabatic flame temperature is calculated using energy balance:

```
T_ad = T_reactants + (LHV × ṁ_fuel) / (Σ(ṁᵢ × cp,ᵢ)_products)

Where:
- LHV = Lower Heating Value [J/kg]
- cp,i = specific heat of product i [J/kg·K]
```

#### Simplified Correlation (Used in Code)
```
T_ad = T_base × (1 - (λ - 1) × 0.3) + T_ambient

Where:
- T_base = 2200 K for natural gas
- Correction factor accounts for excess air cooling effect
```

### Flue Gas Composition

#### CO₂ Volume Percentage
```
CO₂_vol% = CO₂_stoichiometric / λ

For natural gas: CO₂_stoichiometric ≈ 12%
```

#### O₂ Volume Percentage  
```
O₂_vol% = (λ - 1) × 21 / λ

This represents excess oxygen from excess air
```

## Burner Design Calculations

### Required Fuel Flow Rate

```
ṁ_fuel = Q_required / LHV

Where:
- Q_required = thermal power requirement [W]
- LHV = lower heating value [J/kg]
```

### Gas Density at Operating Conditions

Using ideal gas law:
```
ρ_gas = (P × M) / (R × T)

Where:
- P = gas pressure [Pa]
- M = molecular weight [kg/mol]
- R = universal gas constant [J/mol·K]
- T = gas temperature [K]
```

### Burner Sizing

#### Cross-sectional Area
```
A_burner = V̇_total / v_target

Where:
- V̇_total = total volumetric flow rate [m³/s]
- v_target = target gas velocity [m/s]
```

#### Burner Diameter
```
D_burner = √(4 × A_burner / π)
```

#### Volume Flow Rate
```
V̇_total = (ṁ_fuel + ṁ_air) / ρ_mixture
```

### Optimal Gas Velocity

Empirical correlation based on fuel type and power:
```
v_optimal = v_base × (P_thermal / 100000)^0.3

Where:
- v_base = base velocity for fuel type [m/s]
- P_thermal = thermal power [W]
- Exponent 0.3 accounts for mixing requirements
```

### Pressure Drop Across Burner

Using orifice flow equation:
```
ΔP_burner = K × ρ_gas × v² / 2

Where:
- K = pressure drop coefficient (≈ 0.8)
- v = gas velocity [m/s]
```

### Flame Length Estimation

Empirical correlation for turbulent diffusion flames:
```
L_flame / D_burner = C × Re^n

Where:
- C = empirical constant (0.2-0.25)
- n = exponent (≈ 0.5)
- Re = Reynolds number
```

#### Reynolds Number
```
Re = ρ × v × D / μ

Where:
- μ = dynamic viscosity [Pa·s]
```

## Chamber Design Calculations

### Required Chamber Volume

Based on residence time requirements:
```
V_chamber = V̇_flue_gas × τ × SF

Where:
- τ = target residence time [s]
- SF = safety factor (typically 1.5)
```

### Flue Gas Volume Flow Rate

At operating temperature:
```
V̇_flue_gas = (ṁ_flue_gas × R_specific × T_gas) / P_operating

Where:
- R_specific = specific gas constant [J/kg·K]
- T_gas = average gas temperature [K]
```

### Chamber Dimensions

Assuming cylindrical geometry with L/D ratio:
```
V_chamber = π × D² × L / 4 = π × D² × (L/D × D) / 4

Solving for diameter:
D_chamber = (4 × V_chamber / (π × L/D_ratio))^(1/3)

Length:
L_chamber = L/D_ratio × D_chamber
```

### Volume Heat Release Rate

```
q_vol = Q_thermal / V_chamber [W/m³]

Typical maximum: 3 × 10⁶ W/m³
```

### Heat Transfer Coefficient

For turbulent flow in cylindrical chambers:
```
Nu = 0.023 × Re^0.8 × Pr^0.4  (Dittus-Boelter correlation)

h = Nu × k_gas / D_chamber

Where:
- Nu = Nusselt number
- Pr = Prandtl number (≈ 0.7 for gases)
- k_gas = thermal conductivity [W/m·K]
```

### Wall Temperature Calculation

Using thermal resistance network:
```
T_wall = T_gas - q_flux × R_convection

Where:
R_convection = 1 / h_convection

Heat flux:
q_flux = (T_gas - T_ambient) / R_total

Total thermal resistance:
R_total = 1/h + δ_insulation/k_insulation + 1/h_external
```

### Chamber Surface Area

For cylindrical chamber:
```
A_surface = π × D × L + 2 × π × D²/4

Where:
- First term = cylindrical surface
- Second term = end surfaces
```

### Thermal Efficiency

```
η_thermal = (Q_useful / Q_input) × 100%

η_thermal = (1 - Q_losses / Q_input) × 100%

Where:
Q_losses = heat loss through chamber walls
```

## Radiation Heat Transfer

### Stefan-Boltzmann Law

For radiation between two surfaces:
```
Q_radiation = σ × A × F × ε_effective × (T₁⁴ - T₂⁴)

Where:
- σ = 5.67 × 10⁻⁸ W/m²K⁴ (Stefan-Boltzmann constant)
- A = surface area [m²]
- F = view factor [-]
- ε_effective = effective emissivity [-]
```

### Mean Beam Length

For cylindrical geometry:
```
L_mean = 3.6 × V_chamber / A_surface

This is used for gas radiation calculations
```

### Flame Emissivity

#### Gas Radiation (CO₂ and H₂O)
```
ε_CO₂ = 1 - exp(-k_CO₂ × P_CO₂ × L_mean)
ε_H₂O = 1 - exp(-k_H₂O × P_H₂O × L_mean)

Combined gas emissivity:
ε_gas = ε_CO₂ + ε_H₂O - 0.15 × ε_CO₂ × ε_H₂O

Where:
- k_CO₂, k_H₂O = absorption coefficients [m⁻¹atm⁻¹]
- P_CO₂, P_H₂O = partial pressures [atm]
```

#### Soot Contribution
```
ε_soot = 1 - exp(-k_soot × C_soot × L_mean)

Total flame emissivity:
ε_flame = 1 - (1 - ε_gas) × (1 - ε_soot)

Where:
- k_soot = soot absorption coefficient [m⁻¹]
- C_soot = soot concentration [kg/m³]
```

### View Factors

#### Cylindrical Chamber (Volume to Surface)
```
For L/D < 0.5:  F = 0.7
For L/D > 5.0:  F = 0.9
For 0.5 ≤ L/D ≤ 5.0:  F = 0.7 + 0.2 × (L/D - 0.5) / 4.5
```

### Effective Emissivity

For two-surface radiation exchange:
```
1/ε_effective = 1/ε₁ + (A₁/A₂) × (1/ε₂ - 1)

Where:
- ε₁, ε₂ = emissivities of surfaces 1 and 2
- A₁, A₂ = areas of surfaces 1 and 2
```

### Radiation Exchange Between Multiple Surfaces

Using radiosity method:
```
Jᵢ = εᵢ × σ × Tᵢ⁴ + ρᵢ × Σ(Fᵢⱼ × Jⱼ)

Where:
- Jᵢ = radiosity of surface i [W/m²]
- ρᵢ = reflectivity = 1 - εᵢ
- Fᵢⱼ = view factor from surface i to j
```

## Pressure Loss Calculations

### Darcy-Weisbach Equation

For friction losses in pipes:
```
ΔP_friction = f × (L/D) × (ρ × v²/2)

Where:
- f = Darcy friction factor [-]
- L = pipe length [m]
- D = pipe diameter [m]
- v = fluid velocity [m/s]
```

### Friction Factor Calculation

#### Laminar Flow (Re < 2300)
```
f = 64 / Re
```

#### Turbulent Flow (Re > 4000)
Colebrook-White equation:
```
1/√f = -2 × log₁₀(ε/(3.7×D) + 2.51/(Re×√f))

Where:
- ε = pipe roughness [m]
- Solved iteratively
```

#### Transition Region (2300 ≤ Re ≤ 4000)
Linear interpolation between laminar and turbulent values.

### Reynolds Number
```
Re = ρ × v × D / μ

Where:
- μ = dynamic viscosity [Pa·s]
```

### Minor Losses

For fittings and components:
```
ΔP_minor = K × (ρ × v²/2)

Where:
- K = loss coefficient (depends on fitting type)
```

### Elevation Losses

Hydrostatic pressure change:
```
ΔP_elevation = ρ × g × Δh

Where:
- g = gravitational acceleration = 9.81 m/s²
- Δh = elevation change [m]
```

### Total System Pressure Loss

```
ΔP_total = ΔP_friction + ΔP_minor + ΔP_elevation + ΔP_burner
```

### Equivalent Length Method

Converting minor losses to equivalent pipe length:
```
L_equivalent = K × D / f

Total equivalent length:
L_total = L_actual + Σ(L_equivalent,i)
```

## Physical Constants and Properties

### Universal Constants

| Constant | Symbol | Value | Units |
|----------|--------|-------|-------|
| Universal Gas Constant | R | 8314.46 | J/kmol·K |
| Stefan-Boltzmann Constant | σ | 5.67×10⁻⁸ | W/m²K⁴ |
| Gravitational Acceleration | g | 9.81 | m/s² |
| Standard Pressure | P₀ | 101325 | Pa |
| Standard Temperature | T₀ | 273.15 | K |

### Fuel Properties

#### Natural Gas (Typical)
| Property | Value | Units |
|----------|-------|-------|
| Lower Heating Value | 50,000 | kJ/kg |
| Molecular Weight | 16.04 | kg/kmol |
| Density (STP) | 0.717 | kg/m³ |
| Air-Fuel Ratio (mass) | 17.2 | - |

#### Methane (CH₄)
| Property | Value | Units |
|----------|-------|-------|
| Lower Heating Value | 50,013 | kJ/kg |
| Molecular Weight | 16.04 | kg/kmol |
| Density (STP) | 0.717 | kg/m³ |
| Air-Fuel Ratio (mass) | 17.2 | - |

#### Propane (C₃H₈)
| Property | Value | Units |
|----------|-------|-------|
| Lower Heating Value | 46,000 | kJ/kg |
| Molecular Weight | 44.10 | kg/kmol |
| Density (STP) | 1.967 | kg/m³ |
| Air-Fuel Ratio (mass) | 15.7 | - |

### Material Properties

#### Emissivity Values
| Material | Emissivity | Temperature Range |
|----------|------------|-------------------|
| Steel (oxidized) | 0.79 | 500-1000°C |
| Refractory Brick | 0.75 | 800-1200°C |
| Flame Gases | 0.2-0.8 | Variable |
| Soot Particles | 0.85 | 800-2000°C |

#### Pipe Roughness Values
| Material | Roughness (mm) |
|----------|----------------|
| Steel (new) | 0.045 |
| Steel (used) | 0.15 |
| Galvanized | 0.15 |
| Cast Iron | 0.26 |
| Copper | 0.0015 |
| Plastic | 0.0015 |

### Gas Properties

#### Air Properties (at 20°C, 1 atm)
| Property | Value | Units |
|----------|-------|-------|
| Density | 1.225 | kg/m³ |
| Dynamic Viscosity | 1.81×10⁻⁵ | Pa·s |
| Thermal Conductivity | 0.0257 | W/m·K |
| Specific Heat | 1005 | J/kg·K |
| Prandtl Number | 0.707 | - |

#### Combustion Products (typical)
| Property | Value | Units |
|----------|-------|-------|
| Molecular Weight | 28.8 | kg/kmol |
| Specific Heat | 1100 | J/kg·K |
| Thermal Conductivity | 0.05-0.08 | W/m·K |

## Validation Methods

### Mass Balance Validation

```
Σ(ṁ_in) = Σ(ṁ_out)

Input: ṁ_fuel + ṁ_air
Output: ṁ_flue_gas

Verification: |ṁ_in - ṁ_out| / ṁ_in < 0.001
```

### Energy Balance Validation

```
Q_input = Q_output + Q_losses

Q_input = ṁ_fuel × LHV
Q_output = ṁ_flue_gas × cp × (T_out - T_ref)
Q_losses = heat losses through walls

Verification: |Q_in - Q_out - Q_losses| / Q_in < 0.05
```

### Dimensional Analysis

All equations are checked for dimensional consistency:
- Force balance: [M L T⁻²]
- Energy balance: [M L² T⁻²]
- Heat transfer: [M T⁻³]

### Physical Reasonableness Checks

#### Temperature Limits
- Flame temperature: 1200K < T < 2500K
- Wall temperature: 300K < T < 1800K
- Gas temperature: T_ambient < T < T_flame

#### Pressure Limits
- System pressure: 100 Pa < P < 100 kPa
- Pressure drops: ΔP < 0.5 × P_supply
- Velocity pressure: 1 Pa < P_velocity < 1000 Pa

#### Flow Limits
- Gas velocity: 1 m/s < v < 100 m/s
- Reynolds number: 1000 < Re < 10⁶
- Mass flow rate: ṁ > 0

### Convergence Criteria

For iterative calculations:
```
|x_n+1 - x_n| / x_n < tolerance

Where:
- tolerance = 1×10⁻⁶ for temperatures
- tolerance = 1×10⁻⁸ for pressures
- tolerance = 1×10⁻⁶ for friction factors
```

### Error Propagation

Uncertainty analysis using partial derivatives:
```
δf = √(Σ((∂f/∂xᵢ) × δxᵢ)²)

Where:
- δf = uncertainty in calculated result
- δxᵢ = uncertainty in input parameter i
```

---

*All calculation methods are based on established engineering principles and have been validated against industry standards and experimental data.*