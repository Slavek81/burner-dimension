# integration_test.py

"""
Integration test for all burner calculation modules.

This script demonstrates how all calculation modules work together
to provide a complete burner design solution.
"""

import sys

sys.path.append("src")

from src import (
    CombustionCalculator,
    BurnerDesigner,
    ChamberDesigner,
    RadiationCalculator,
    PressureLossCalculator,
    PipeSegment,
    Fitting,
)


def main():
    """
    Complete integration test of all calculation modules.
    """
    print("=" * 60)
    print("KOMPLETNÍ VÝPOČET PLYNOVÉHO HOŘÁKU")
    print("=" * 60)

    # Input parameters
    fuel_type = "natural_gas"
    required_power = 100000  # W (100 kW)
    supply_pressure = 3000  # Pa (30 mbar)
    excess_air_ratio = 1.2

    print(f"Vstupní parametry:")
    print(f"Typ paliva: {fuel_type}")
    print(f"Požadovaný výkon: {required_power/1000:.1f} kW")
    print(f"Tlak plynu: {supply_pressure:.0f} Pa")
    print(f"Koeficient přebytku vzduchu: {excess_air_ratio}")
    print()

    try:
        # 1. Combustion calculations
        print("1. SPALOVACÍ VÝPOČTY")
        print("-" * 30)

        combustion_calc = CombustionCalculator()
        fuel_flow_rate = (
            required_power
            / combustion_calc.get_fuel_properties(fuel_type)["properties"][
                "lower_heating_value_mass"
            ]
        )

        combustion_results = combustion_calc.calculate_combustion_products(
            fuel_type, fuel_flow_rate, excess_air_ratio
        )

        print(f"Průtok paliva: {combustion_results.fuel_flow_rate:.6f} kg/s")
        print(f"Průtok vzduchu: {combustion_results.air_flow_rate:.4f} kg/s")
        print(f"Průtok spalin: {combustion_results.flue_gas_flow_rate:.4f} kg/s")
        print(
            f"Adiabatická teplota plamene: {combustion_results.adiabatic_flame_temperature:.0f} K ({combustion_results.adiabatic_flame_temperature-273.15:.0f} °C)"
        )
        print(f"CO₂ ve spalinách: {combustion_results.co2_volume_percent:.1f} %")
        print(f"O₂ ve spalinách: {combustion_results.o2_volume_percent:.1f} %")
        print()

        # 2. Burner design
        print("2. NÁVRH HOŘÁKU")
        print("-" * 30)

        burner_designer = BurnerDesigner(combustion_calc)
        burner_results = burner_designer.design_burner(
            fuel_type=fuel_type,
            required_power=required_power,
            supply_pressure=supply_pressure,
            excess_air_ratio=excess_air_ratio,
        )

        print(f"Průměr hořáku: {burner_results.burner_diameter*1000:.1f} mm")
        print(f"Plocha hořáku: {burner_results.burner_area*1000*1000:.1f} mm²")
        print(f"Rychlost plynu: {burner_results.gas_velocity:.1f} m/s")
        print(f"Tlaková ztráta hořáku: {burner_results.burner_pressure_drop:.0f} Pa")
        print(
            f"Hustota tepelného toku: {burner_results.heat_release_density/1e6:.2f} MW/m²"
        )
        print(f"Délka hořáku: {burner_results.burner_length*1000:.0f} mm")
        print(f"Délka plamene: {burner_results.flame_length*1000:.0f} mm")
        print()

        # 3. Chamber design
        print("3. NÁVRH SPALOVACÍ KOMORY")
        print("-" * 30)

        chamber_designer = ChamberDesigner(combustion_calc, burner_designer)
        chamber_results = chamber_designer.design_chamber(
            fuel_type=fuel_type,
            required_power=required_power,
            target_residence_time=0.5,
        )

        print(f"Objem komory: {chamber_results.chamber_volume:.3f} m³")
        print(f"Průměr komory: {chamber_results.chamber_diameter*1000:.0f} mm")
        print(f"Délka komory: {chamber_results.chamber_length*1000:.0f} mm")
        print(f"Doba zdržení: {chamber_results.residence_time:.2f} s")
        print(f"Teplota stěny: {chamber_results.wall_temperature-273.15:.0f} °C")
        print(f"Tepelná účinnost: {chamber_results.thermal_efficiency:.1f} %")
        print(f"Tepelné ztráty: {chamber_results.heat_loss_rate/1000:.1f} kW")
        print()

        # 4. Radiation calculations
        print("4. RADIAČNÍ PŘENOS TEPLA")
        print("-" * 30)

        radiation_calc = RadiationCalculator(combustion_calc)
        radiation_results = radiation_calc.calculate_flame_radiation(
            flame_temperature=combustion_results.adiabatic_flame_temperature,
            chamber_wall_temperature=chamber_results.wall_temperature,
            chamber_diameter=chamber_results.chamber_diameter,
            chamber_length=chamber_results.chamber_length,
            fuel_type=fuel_type,
            excess_air_ratio=excess_air_ratio,
            soot_concentration=0.001,
        )

        print(
            f"Celkový radiační přenos: {radiation_results.total_radiation_heat_transfer/1000:.1f} kW"
        )
        print(
            f"Přenos plamen → stěna: {radiation_results.flame_to_wall_heat_transfer/1000:.1f} kW"
        )
        print(
            f"Přenos stěna → okolí: {radiation_results.wall_to_ambient_heat_transfer/1000:.1f} kW"
        )
        print(f"Emisivita plamene: {radiation_results.flame_emissivity:.3f}")
        print(f"Emisivita stěny: {radiation_results.wall_emissivity:.3f}")
        print(f"View faktor: {radiation_results.view_factor_flame_wall:.3f}")
        print(f"Účinnost radiace: {radiation_results.radiation_efficiency:.1f} %")
        print()

        # 5. Pressure loss calculations
        print("5. TLAKOVÉ ZTRÁTY V SYSTÉMU")
        print("-" * 30)

        pressure_calc = PressureLossCalculator(combustion_calc)

        # Define typical gas piping system
        pipe_segments = [
            PipeSegment(
                length=10.0,
                diameter=0.05,  # 50mm
                roughness=pressure_calc.get_pipe_roughness("steel_new"),
                material="steel_new",
                elevation_change=2.0,
            ),
            PipeSegment(
                length=5.0,
                diameter=0.025,  # 25mm
                roughness=pressure_calc.get_pipe_roughness("steel_new"),
                material="steel_new",
                elevation_change=0.0,
            ),
        ]

        fittings = [
            Fitting(
                "pipe_entrance_rounded",
                1,
                pressure_calc.get_fitting_coefficient("pipe_entrance_rounded"),
                0.05,
            ),
            Fitting(
                "elbow_90_long",
                3,
                pressure_calc.get_fitting_coefficient("elbow_90_long"),
                0.05,
            ),
            Fitting(
                "gate_valve_open",
                1,
                pressure_calc.get_fitting_coefficient("gate_valve_open"),
                0.05,
            ),
            Fitting(
                "reducer_gradual",
                1,
                pressure_calc.get_fitting_coefficient("reducer_gradual"),
                0.025,
            ),
        ]

        gas_density = 0.8  # kg/m³ at operating conditions
        pressure_results = pressure_calc.calculate_system_pressure_losses(
            pipe_segments=pipe_segments,
            fittings=fittings,
            mass_flow_rate=combustion_results.fuel_flow_rate,
            gas_density=gas_density,
            burner_results=burner_results,
        )

        print(f"Třecí ztráty: {pressure_results.friction_losses:.0f} Pa")
        print(f"Místní ztráty: {pressure_results.minor_losses:.0f} Pa")
        print(f"Výškové ztráty: {pressure_results.elevation_losses:.0f} Pa")
        print(f"Ztráty hořáku: {pressure_results.burner_pressure_loss:.0f} Pa")
        print(f"Celkové ztráty: {pressure_results.total_pressure_loss:.0f} Pa")
        print(f"Požadovaný přítlak: {pressure_results.required_supply_pressure:.0f} Pa")
        print(f"Reynoldsovo číslo: {pressure_results.reynolds_number:.0f}")
        print()

        # 6. Summary and validation
        print("6. SHRNUTÍ A VALIDACE")
        print("-" * 30)

        # Validate burner design
        burner_validation = burner_designer.validate_design(burner_results)
        chamber_validation = chamber_designer.validate_design(chamber_results)

        print("Validace hořáku:")
        for criterion, passed in burner_validation.items():
            status = "✓" if passed else "✗"
            print(f"  {status} {criterion}")

        print("Validace komory:")
        for criterion, passed in chamber_validation.items():
            status = "✓" if passed else "✗"
            print(f"  {status} {criterion}")

        # Check pressure compatibility
        pressure_ok = pressure_results.required_supply_pressure <= supply_pressure
        print(
            f"Tlakový požadavek: {'✓' if pressure_ok else '✗'} {pressure_results.required_supply_pressure:.0f} Pa ≤ {supply_pressure:.0f} Pa"
        )

        print()
        print("=" * 60)
        print("VÝPOČET DOKONČEN ÚSPĚŠNĚ")
        print("=" * 60)

        # Get recommendations
        burner_recommendations = burner_designer.get_design_recommendations(
            burner_results
        )
        chamber_recommendations = chamber_designer.get_design_recommendations(
            chamber_results
        )

        if burner_recommendations or chamber_recommendations:
            print("\nDOPOREČENÍ:")
            for i, rec in enumerate(
                burner_recommendations + chamber_recommendations, 1
            ):
                print(f"{i}. {rec}")

    except Exception as e:
        print(f"CHYBA PŘI VÝPOČTU: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
