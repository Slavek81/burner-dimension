# Mathematical Formulas and Equations

## Table of Contents
1. [Notation and Unit System](#notation-and-unit-system)
2. [Fundamental Constants](#fundamental-constants)
3. [Combustion Chemistry](#combustion-chemistry)
4. [Thermodynamics](#thermodynamics)
5. [Fluid Mechanics](#fluid-mechanics)
6. [Heat Transfer](#heat-transfer)
7. [Radiation Heat Transfer](#radiation-heat-transfer)
8. [Pressure Loss Calculations](#pressure-loss-calculations)
9. [Burner Design Equations](#burner-design-equations)
10. [Chamber Design Equations](#chamber-design-equations)
11. [Validation and Error Analysis](#validation-and-error-analysis)

## Notation and Unit System

### Primary Symbols

| Symbol | Description | SI Unit |
|--------|-------------|---------|
| **ṁ** | Mass flow rate | kg/s |
| **V̇** | Volumetric flow rate | m³/s |
| **Q̇** | Heat transfer rate | W |
| **T** | Temperature | K |
| **P** | Pressure | Pa |
| **ρ** | Density | kg/m³ |
| **μ** | Dynamic viscosity | Pa·s |
| **ν** | Kinematic viscosity | m²/s |
| **λ** | Excess air ratio | - |
| **ε** | Emissivity | - |
| **α** | Absorptivity | - |
| **σ** | Stefan-Boltzmann constant | W/m²K⁴ |
| **h** | Heat transfer coefficient | W/m²K |
| **k** | Thermal conductivity | W/mK |
| **cp** | Specific heat at constant pressure | J/kgK |
| **cv** | Specific heat at constant volume | J/kgK |
| **R** | Gas constant | J/kgK |
| **γ** | Specific heat ratio | - |

### Subscripts and Superscripts

| Notation | Meaning |
|----------|---------|
| **f** | Fuel |
| **a** | Air |
| **fg** | Flue gas |
| **w** | Wall |
| **amb** | Ambient |
| **ad** | Adiabatic |
| **s** | Stoichiometric |
| **0** | Reference state |
| **in** | Inlet |
| **out** | Outlet |
| **∞** | Infinity or bulk conditions |

## Fundamental Constants

### Universal Constants

```
Universal gas constant:     R = 8314.46 J/kmol·K
Stefan-Boltzmann constant:  σ = 5.670374419 × 10⁻⁸ W/m²K⁴
Gravitational acceleration: g = 9.80665 m/s²
Standard pressure:          P₀ = 101325 Pa
Standard temperature:       T₀ = 273.15 K
```

### Air Properties (at 15°C, 1 atm)

```
Density:                    ρₐᵢᵣ = 1.225 kg/m³
Dynamic viscosity:          μₐᵢᵣ = 1.81 × 10⁻⁵ Pa·s
Thermal conductivity:       kₐᵢᵣ = 0.0257 W/mK
Specific heat:              cp,air = 1005 J/kgK
Prandtl number:            Prₐᵢᵣ = 0.707
Molecular weight:           Mₐᵢᵣ = 28.97 kg/kmol
```

## Combustion Chemistry

### Stoichiometric Combustion

#### General Hydrocarbon Combustion
For a hydrocarbon fuel CₓHᵧ:

```
CₓHᵧ + (x + y/4)(O₂ + 3.76N₂) → xCO₂ + (y/2)H₂O + 3.76(x + y/4)N₂
```

#### Stoichiometric Air-Fuel Ratio (Mass Basis)
```
AFRₛ = ṁₐᵢᵣ,ₛ / ṁfuel = (x + y/4) × 4.76 × Mₐᵢᵣ / Mfuel

Where:
- x = number of carbon atoms
- y = number of hydrogen atoms
- Mₐᵢᵣ = 28.97 kg/kmol (molecular weight of air)
- Mfuel = molecular weight of fuel [kg/kmol]
```

#### Specific Cases

**Methane (CH₄):**
```
CH₄ + 2(O₂ + 3.76N₂) → CO₂ + 2H₂O + 7.52N₂
AFRₛ = 2 × 4.76 × 28.97 / 16.04 = 17.19
```

**Propane (C₃H₈):**
```
C₃H₈ + 5(O₂ + 3.76N₂) → 3CO₂ + 4H₂O + 18.8N₂
AFRₛ = 5 × 4.76 × 28.97 / 44.10 = 15.67
```

### Actual Combustion with Excess Air

#### Excess Air Factor
```
λ = ṁₐᵢᵣ,actual / ṁₐᵢᵣ,stoichiometric

Typical values: 1.05 ≤ λ ≤ 1.30
```

#### Actual Air Flow Rate
```
ṁₐᵢᵣ,actual = λ × AFRₛ × ṁfuel
```

#### Total Mass Flow Rate
```
ṁfg = ṁfuel + ṁₐᵢᵣ,actual = ṁfuel(1 + λ × AFRₛ)
```

### Combustion Products Composition

#### CO₂ Volume Percentage
```
CO₂% = (xCO₂,stoich / λ) × 100%

For methane: CO₂% = (12 / λ)%
For propane: CO₂% = (13.8 / λ)%
```

#### O₂ Volume Percentage
```
O₂% = ((λ - 1) × 21 / λ) × 100%

This represents excess oxygen in flue gas
```

#### H₂O Volume Percentage
```
H₂O% = (yH₂O,stoich / λ) × 100%

For methane: H₂O% = (24 / λ)%
For propane: H₂O% = (18.4 / λ)%
```

## Thermodynamics

### Ideal Gas Law
```
PV = nRT    (molar form)
PV = mRₛT   (mass form)

Where:
- Rₛ = R/M = specific gas constant [J/kgK]
- M = molecular weight [kg/kmol]
```

### Gas Density at Operating Conditions
```
ρ = PM / (RT) = P / (RₛT)

For fuel-air mixtures:
ρmix = Pmix / (Rmix × Tmix)

Where:
Rmix = Σ(xᵢ × Rᵢ)  (mass-weighted average)
```

### Adiabatic Flame Temperature

#### Energy Balance Method
```
Hreactants + Qcombustion = Hproducts

ṁfuel × LHV + Σ(ṁᵢ × hᵢ)reactants = Σ(ṁⱼ × hⱼ)products

Where:
- LHV = Lower heating value [J/kg]
- hᵢ = specific enthalpy [J/kg]
```

#### Simplified Correlation (Used in Code)
```
Tad = Tbase × F(λ) + Tambient

Where:
F(λ) = 1 - α(λ - 1)    (excess air cooling factor)

For natural gas:
- Tbase = 2200 K
- α = 0.3 (cooling coefficient)
```

#### Temperature-Dependent Specific Heat
```
cp(T) = a₀ + a₁T + a₂T² + a₃T³

For combustion products (typical):
cp,fg ≈ 1000 + 0.2T + 10⁻⁵T²  [J/kgK]
```

### Heat Release Rate
```
Q̇thermal = ṁfuel × LHV × ηcombustion

Where:
- ηcombustion ≈ 0.99 (combustion efficiency)
- For complete combustion: ηcombustion = 1.0
```

## Fluid Mechanics

### Reynolds Number
```
Re = ρvD/μ = vD/ν

Where:
- v = fluid velocity [m/s]
- D = characteristic length (diameter) [m]
- ν = kinematic viscosity [m²/s]
```

### Flow Regimes
```
Laminar:     Re < 2300
Transition:  2300 ≤ Re ≤ 4000
Turbulent:   Re > 4000
```

### Velocity Calculation
```
v = V̇/A = ṁ/(ρA)

Where:
- A = cross-sectional area [m²]
- For circular pipes: A = πD²/4
```

### Dynamic Pressure
```
Pdynamic = ρv²/2

This represents kinetic energy per unit volume
```

### Continuity Equation
```
ṁ = ρ₁A₁v₁ = ρ₂A₂v₂ = constant

For incompressible flow: A₁v₁ = A₂v₂
```

## Heat Transfer

### Convective Heat Transfer

#### Newton's Law of Cooling
```
Q̇conv = hA(Twall - Tfluid)

Where:
- h = convective heat transfer coefficient [W/m²K]
- A = heat transfer area [m²]
```

#### Nusselt Number Correlations

**For Internal Flow in Pipes (Dittus-Boelter):**
```
Nu = 0.023 × Re⁰·⁸ × Pr^n

Where:
- n = 0.4 for heating (Twall > Tfluid)
- n = 0.3 for cooling (Twall < Tfluid)
- Valid for: Re > 10⁴, 0.7 < Pr < 160
```

**For External Flow over Cylinders:**
```
Nu = C × Re^m × Pr^(1/3)

Where C and m depend on Re range
```

#### Heat Transfer Coefficient
```
h = Nu × kfluid / D

Where:
- kfluid = thermal conductivity of fluid [W/mK]
```

### Conductive Heat Transfer

#### Fourier's Law
```
Q̇cond = -kA(dT/dx)

For steady-state through a wall:
Q̇cond = kA(T₁ - T₂)/δ

Where:
- δ = wall thickness [m]
```

#### Thermal Resistance
```
Rth = δ/(kA)    (conduction)
Rth = 1/(hA)    (convection)

For series resistances:
Rtotal = R₁ + R₂ + R₃ + ...
```

### Overall Heat Transfer

#### Overall Heat Transfer Coefficient
```
1/UA = 1/(h₁A₁) + δwall/(kwall×Awall) + 1/(h₂A₂)

For thin walls: A₁ ≈ A₂ ≈ Awall
1/U = 1/h₁ + δwall/kwall + 1/h₂
```

## Radiation Heat Transfer

### Stefan-Boltzmann Law

#### Basic Form
```
Q̇rad = εσAT⁴

Where:
- ε = emissivity (0 ≤ ε ≤ 1)
- σ = 5.670374419 × 10⁻⁸ W/m²K⁴
```

#### Net Radiation Between Two Surfaces
```
Q̇net = σA₁F₁₂εeff(T₁⁴ - T₂⁴)

Where:
- F₁₂ = view factor from surface 1 to 2
- εeff = effective emissivity
```

### Effective Emissivity

#### For Two Large Parallel Plates
```
1/εeff = 1/ε₁ + 1/ε₂ - 1
```

#### For Surface 1 Inside Surface 2 (A₁ << A₂)
```
1/εeff = 1/ε₁ + (A₁/A₂)(1/ε₂ - 1)

If A₁ << A₂: εeff ≈ ε₁
```

### View Factors

#### Geometric Relations
```
Reciprocity: A₁F₁₂ = A₂F₂₁
Summation: Σⱼ F₁ⱼ = 1 (for enclosure)
```

#### Specific Geometries

**Concentric Cylinders:**
```
F₁₂ = 1 (inner to outer)
F₂₁ = A₁/A₂ = D₁/D₂ (outer to inner)
```

**Volume to Enclosing Surface:**
```
For L/D < 0.5:  F = 0.65
For L/D > 5.0:  F = 0.95
For 0.5 ≤ L/D ≤ 5.0:  F = 0.65 + 0.3(L/D - 0.5)/4.5
```

### Gas Radiation

#### Mean Beam Length
```
Lm = 3.6 × V/A

Where:
- V = gas volume [m³]
- A = enclosing surface area [m²]
```

#### Gas Emissivity (Simplified)
```
εCO₂ = C₁ × (PCO₂ × Lm)^n₁
εH₂O = C₂ × (PH₂O × Lm)^n₂

Combined gas emissivity:
εgas = εCO₂ + εH₂O - Δε

Where:
- Δε ≈ 0.15 × εCO₂ × εH₂O (overlap correction)
```

#### Flame Emissivity with Soot
```
εflame = 1 - (1 - εgas)(1 - εsoot)

Where:
εsoot = 1 - exp(-KsootCsootLm)

Typical values:
- Ksoot = 3-10 m⁻¹/(kg/m³) (soot extinction coefficient)
- Csoot = 0.01-0.1 kg/m³ (soot concentration)
```

## Pressure Loss Calculations

### Darcy-Weisbach Equation

#### Friction Losses in Pipes
```
ΔPfriction = f × (L/D) × (ρv²/2)

Where:
- f = Darcy friction factor
- L = pipe length [m]
- D = pipe diameter [m]
```

### Friction Factor Correlations

#### Laminar Flow (Re < 2300)
```
f = 64/Re
```

#### Turbulent Flow - Smooth Pipes
```
1/√f = -2 log₁₀(2.51/(Re√f))    (Prandtl equation)

Simplified (Blasius, Re < 10⁵):
f = 0.316/Re^0.25
```

#### Turbulent Flow - Rough Pipes
```
1/√f = -2 log₁₀(ε/D/3.7 + 2.51/(Re√f))    (Colebrook-White)

Where:
- ε = absolute roughness [m]
- ε/D = relative roughness
```

#### Approximation for Rough Pipes (Haaland)
```
1/√f = -1.8 log₁₀[(ε/D/3.7)^1.11 + 6.9/Re]
```

### Minor Losses

#### General Form
```
ΔPminor = K × (ρv²/2)

Where K = loss coefficient (dimensionless)
```

#### Common Fitting Coefficients
```
Elbow 90° (long radius):    K = 0.3-0.5
Elbow 90° (short radius):   K = 0.7-0.9
Tee (through):              K = 0.1-0.2
Tee (branch):               K = 1.5-2.0
Gate valve (open):          K = 0.1-0.2
Globe valve (open):         K = 6-10
Entry (sharp):              K = 0.5
Entry (well-rounded):       K = 0.04
Exit:                       K = 1.0
```

### Elevation Losses
```
ΔPelevation = ρg(z₂ - z₁)

Where:
- g = 9.81 m/s²
- (z₂ - z₁) = elevation change [m] (positive = upward)
```

### Total System Pressure Loss
```
ΔPtotal = ΔPfriction + ΔPminor + ΔPelevation

Or using equivalent length method:
ΔPtotal = f × (Ltotal/D) × (ρv²/2)

Where:
Ltotal = Lactual + Σ(Leq,i)
Leq = K × D/f    (equivalent length of fitting)
```

## Burner Design Equations

### Fuel Flow Rate Calculation
```
ṁfuel = Q̇required / (LHV × ηcombustion)

Where:
- Q̇required = thermal power requirement [W]
- LHV = lower heating value [J/kg]
- ηcombustion ≈ 0.99 (combustion efficiency)
```

### Gas Velocity and Burner Sizing

#### Target Velocity Selection
```
vtarget = vbase × (Q̇thermal/Q̇ref)^α

Where:
- vbase = base velocity for fuel type [m/s]
- Q̇ref = reference power (typically 100 kW)
- α ≈ 0.2-0.3 (scaling exponent)

Typical ranges:
- Natural gas: 15-40 m/s
- Propane: 10-30 m/s
```

#### Cross-Sectional Area
```
Aburner = V̇total / vtarget

Where:
V̇total = (ṁfuel + ṁair) / ρmix
```

#### Burner Diameter
```
Dburner = √(4Aburner/π)

For multiple nozzles:
Dsingle = √(4Aburner/(π × Nnozzles))
```

### Pressure Drop Across Burner

#### Orifice Flow Model
```
ΔPburner = Cd × (ρmixv²/2)

Where:
- Cd ≈ 0.6-0.8 (discharge coefficient)
- Typical values: Cd = 0.75 for well-designed burners
```

#### Required Supply Pressure
```
Psupply = Poperating + ΔPsystem + ΔPburner + Psafety

Where:
- ΔPsystem = total system pressure losses
- Psafety = safety margin (typically 20-30% of total)
```

### Flame Length Estimation

#### Empirical Correlation for Turbulent Jets
```
Lflame/Dburner = C × Re^n

Where:
- C = 0.2-0.25 (empirical constant)
- n ≈ 0.5 (Reynolds number exponent)
- Re = ρvD/μ (based on burner exit conditions)
```

#### Alternative Correlation (Hawthorne et al.)
```
Lflame/Dburner = k × (ṁfuel/ṁair,stoich)

Where:
- k ≈ 5.3 for turbulent diffusion flames
```

### Heat Release Density
```
qv = Q̇thermal / Vflame    [W/m³]

Typical design limits:
- qv < 3 × 10⁶ W/m³ (to avoid flame quenching)
- qv > 1 × 10⁵ W/m³ (for stable combustion)
```

## Chamber Design Equations

### Volume Requirements

#### Residence Time Method
```
Vchamber = V̇fg × τresidence × SFvolume

Where:
- V̇fg = volumetric flow rate of flue gas at operating temperature [m³/s]
- τresidence = target residence time [s]
- SFvolume = volume safety factor (typically 1.3-1.8)
```

#### Flue Gas Volume Flow Rate
```
V̇fg = ṁfg × Rspecific × Tavg / Pavg

Where:
- Rspecific = specific gas constant for flue gas [J/kgK]
- Tavg = average gas temperature in chamber [K]
- Pavg = average pressure in chamber [Pa]
```

### Chamber Geometry

#### Cylindrical Chamber Dimensions
```
Vchamber = (π/4) × D² × L

With aspect ratio constraint:
AR = L/D (typically 2-5)

Solving simultaneously:
D = (4Vchamber/(π × AR))^(1/3)
L = AR × D
```

#### Surface Area Calculation
```
Asurface = πDL + 2 × (π/4)D²    (cylinder + end caps)
Asurface = πD(L + D/2)          (simplified)
```

### Heat Transfer Analysis

#### Volume Heat Release Rate
```
qvolume = Q̇thermal / Vchamber    [W/m³]

Design limits:
- Industrial burners: qvolume < 3 × 10⁶ W/m³
- Residential burners: qvolume < 1 × 10⁶ W/m³
```

#### Wall Heat Flux
```
q"wall = Q̇loss / Asurface    [W/m²]

Where:
Q̇loss = heat loss through chamber walls
```

### Thermal Analysis

#### Energy Balance
```
Q̇in = Q̇useful + Q̇loss

Where:
- Q̇in = ṁfuel × LHV (heat input)
- Q̇useful = useful heat output
- Q̇loss = heat loss through walls
```

#### Thermal Efficiency
```
ηthermal = Q̇useful / Q̇in = (Q̇in - Q̇loss) / Q̇in

Target efficiency: ηthermal > 85%
```

#### Wall Temperature Calculation
```
Twall = Tgas - q"wall/hconv

Where:
hconv = convective heat transfer coefficient inside chamber
```

#### Heat Loss Through Insulated Wall
```
Q̇loss = UA(Twall,inner - Tambient)

Where:
1/U = 1/hinner + δinsulation/kinsulation + 1/houter

For thick insulation: U ≈ kinsulation/δinsulation
```

## Validation and Error Analysis

### Mass Balance Validation
```
Σṁin = Σṁout

Input streams: ṁfuel + ṁair
Output streams: ṁfg

Tolerance: |ṁin - ṁout|/ṁin < 0.001 (0.1%)
```

### Energy Balance Validation
```
Σ(ṁh)in + Q̇in = Σ(ṁh)out + Q̇out + Q̇loss

Simplified:
Q̇fuel = Q̇sensible + Q̇latent + Q̇loss

Tolerance: |Ein - Eout|/Ein < 0.05 (5%)
```

### Dimensional Analysis

#### Force Balance [MLT⁻²]
```
Pressure forces: P × A ~ [ML⁻¹T⁻²][L²] = [MLT⁻²]
Momentum forces: ρv²A ~ [ML⁻³][L²T⁻²][L²] = [MLT⁻²]
```

#### Energy Balance [ML²T⁻²]
```
Heat input: ṁ × LHV ~ [MT⁻¹][L²T⁻²] = [ML²T⁻²]
Enthalpy flow: ṁ × h ~ [MT⁻¹][L²T⁻²] = [ML²T⁻²]
```

#### Heat Transfer [MT⁻³]
```
Convection: hA(ΔT) ~ [MT⁻³K⁻¹][L²][K] = [MT⁻³]
Radiation: σAT⁴ ~ [ML²T⁻³K⁻⁴][L²][K⁴] = [MT⁻³]
```

### Physical Reasonableness Checks

#### Temperature Limits
```
Ambient: 273K < Tambient < 323K
Flame: 1200K < Tflame < 2500K
Wall: Tambient < Twall < 0.8 × Tflame
```

#### Pressure Limits
```
Supply pressure: 1000 Pa < Psupply < 100,000 Pa
Pressure drops: ΔP < 0.5 × Psupply
Velocity pressure: 1 Pa < ρv²/2 < 1000 Pa
```

#### Velocity Limits
```
Gas velocities: 5 m/s < v < 100 m/s
Reynolds number: 1000 < Re < 10⁶
Mach number: Ma < 0.3 (incompressible assumption)
```

### Error Propagation Analysis

#### General Formula
```
δf = √(Σ(∂f/∂xi × δxi)²)

Where:
- δf = uncertainty in calculated result
- ∂f/∂xi = partial derivative with respect to variable xi
- δxi = uncertainty in input variable xi
```

#### Example: Burner Diameter Error
```
D = √(4ṁ/(πρv))

∂D/∂ṁ = 1/(2√(πρvṁ))
∂D/∂ρ = -√(ṁ)/(2√(πρ³v))
∂D/∂v = -√(ṁ)/(2√(πρv³))

δD = √((∂D/∂ṁ × δṁ)² + (∂D/∂ρ × δρ)² + (∂D/∂v × δv)²)
```

### Convergence Criteria

#### Iterative Solutions
```
|xn+1 - xn|/xn < tolerance

Recommended tolerances:
- Temperature: 1×10⁻⁶ (0.0001%)
- Pressure: 1×10⁻⁸ (1×10⁻⁶%)
- Friction factor: 1×10⁻⁶
- Heat transfer coefficient: 1×10⁻⁵
```

#### Maximum Iterations
```
Typical limits:
- Friction factor (Colebrook): 100 iterations
- Temperature iteration: 50 iterations
- Pressure iteration: 30 iterations
```

---

*All mathematical formulations are based on established engineering principles, validated correlations, and international standards. The equations presented here form the computational foundation of the Gas Burner Calculator application.*