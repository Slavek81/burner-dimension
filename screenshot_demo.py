#!/usr/bin/env python3
# screenshot_demo.py

"""
screenshot_demo.py

Script to demonstrate how the GUI would look when running.
Creates a mockup description of the visual interface.
"""


def describe_gui_appearance():
    """Describe how the GUI looks and functions."""

    print("VIZUÁLNÍ POPIS GUI APLIKACE")
    print("=" * 50)
    print()

    print("📱 HLAVNÍ OKNO:")
    print("- Velikost: 1200x800 pixelů (přizpůsobitelná)")
    print("- Název: 'Návrh plynového hořáku a spalovací komory'")
    print("- Moderní vzhled s GTK/Windows nativním témem")
    print()

    print("📑 ZÁLOŽKY (Notebook widget):")
    tabs = [
        ("Vstupní parametry", "Formulář s 10 vstupními poli ve skupinách"),
        ("Výpočty spalování", "Textová oblast s výsledky spalování"),
        ("Návrh hořáku", "Výsledky dimenzování hořáku"),
        ("Návrh komory", "Parametry spalovací komory"),
        ("Radiační přenos", "Výpočty tepelného záření"),
        ("Tlakové ztráty", "Analýza tlakových ztrát systému"),
        ("Výsledky", "Souhrnný report všech výpočtů"),
    ]

    for i, (name, desc) in enumerate(tabs, 1):
        print(f"  {i}. {name:20} - {desc}")
    print()

    print("🎛️ VSTUPNÍ FORMULÁŘ:")
    print("┌─ Palivo ──────────────────────────────┐")
    print("│ Typ paliva: [Dropdown] natural_gas ▼  │")
    print("├─ Průtoky ─────────────────────────────┤")
    print("│ Hmotnostní průtok [kg/s]: [0.01     ] │")
    print("│ Koeficient přebytku [-]:  [1.2      ] │")
    print("├─ Provozní podmínky ───────────────────┤")
    print("│ Teplota okolí [°C]:       [20       ] │")
    print("│ Tlak okolí [Pa]:          [101325   ] │")
    print("├─ Parametry hořáku ────────────────────┤")
    print("│ Max. rychlost plynu [m/s]:[50       ] │")
    print("│ Tlak přívodu [Pa]:        [3000     ] │")
    print("├─ Parametry komory ────────────────────┤")
    print("│ Tepelný výkon [kW]:       [500      ] │")
    print("│ Max. teplota [°C]:        [1200     ] │")
    print("│ Hustota toku [kW/m²]:     [800      ] │")
    print("└───────────────────────────────────────┘")
    print()

    print("🔘 TLAČÍTKA (spodní panel):")
    print("┌─────────────────────────────────────────────────────────┐")
    print("│ [████████████████████] 🔄 Progress                      │")
    print("│                      [Načíst] [Uložit] [Export] [▶ Výpočet] │")
    print("└─────────────────────────────────────────────────────────┘")
    print()

    print("📊 VÝSLEDKY (ukázka záložky):")
    print("┌─ VÝSLEDKY VÝPOČTU SPALOVÁNÍ ──────────────────────────┐")
    print("│                                                        │")
    print("│ Typ paliva: natural_gas                               │")
    print("│ Hmotnostní průtok paliva: 0.010000 kg/s              │")
    print("│ Hmotnostní průtok vzduchu: 0.206400 kg/s             │")
    print("│ Hmotnostní průtok spalin: 0.216400 kg/s              │")
    print("│                                                        │")
    print("│ Koeficient přebytku vzduchu: 1.20 [-]                │")
    print("│ Adiabatická teplota plamene: 2068.3 K (1795.1 °C)   │")
    print("│ Tepelný výkon: 500.0 kW                              │")
    print("│                                                        │")
    print("│ Složení spalin:                                        │")
    print("│   CO₂: 10.00 % obj.                                   │")
    print("│   O₂: 3.50 % obj.                                     │")
    print("│                                                        │")
    print("└────────────────────────────────────────────────────────┘")
    print()

    print("⚠️ CHYBOVÉ HLÁŠKY:")
    print("┌─ Chyby ve vstupních datech ─────────────────────────┐")
    print("│                                                      │")
    print("│ Nalezeny následující chyby ve vstupních datech:     │")
    print("│                                                      │")
    print("│ • Hmotnostní průtok paliva musí být větší než nula  │")
    print("│ • Koeficient přebytku vzduchu musí být ≥ 1.0        │")
    print("│ • Tlak přívodu plynu musí být alespoň 1000 Pa       │")
    print("│                                                      │")
    print("│                                    [OK]              │")
    print("└──────────────────────────────────────────────────────┘")
    print()

    print("💾 EXPORT DIALOG:")
    print("┌─ Export výsledků ────────────────────────────────────┐")
    print("│                                                      │")
    print("│ Formát exportu:                                      │")
    print("│ ○ TXT soubor                                        │")
    print("│ ● CSV soubor                                        │")
    print("│ ○ Excel soubor                                      │")
    print("│                                                      │")
    print("│ Obsah exportu:                                       │")
    print("│ ☑ Vstupní parametry                                 │")
    print("│ ☑ Výsledky výpočtů                                  │")
    print("│ ☐ Detailní údaje                                    │")
    print("│                                                      │")
    print("│                           [Zrušit] [Exportovat]     │")
    print("└──────────────────────────────────────────────────────┘")
    print()

    print("🎨 BAREVNÉ SCHÉMA:")
    print("- Pozadí: Světle šedá/bílá (systémové)")
    print("- Tlačítka: Modré akcenty pro primární akce")
    print("- Text: Tmavě šedá/černá")
    print("- Chyby: Červený text a ikony")
    print("- Úspěch: Zelené značky")
    print("- Progress: Modrý gradient")
    print()

    print("🔧 INTERAKTIVNÍ PRVKY:")
    print("- Dropdown pro výběr paliva")
    print("- Entry fields s validací při psaní")
    print("- Tooltips s nápovědou")
    print("- Progress bar při výpočtu")
    print("- Scrollable textové oblasti pro výsledky")
    print("- Resizable okno s minimální velikostí")
    print()

    print("📱 RESPONSIVNÍ DESIGN:")
    print("- Minimální velikost: 1000x600 px")
    print("- Přizpůsobitelné panely")
    print("- Scroll v dlouhých výsledcích")
    print("- Grid layout s váhami")
    print()

    print("✨ UX FUNKCE:")
    print("- Automatické načtení výchozích hodnot")
    print("- Klávetové zkratky (Ctrl+O, Ctrl+S)")
    print("- Progress feedback při dlouhých operacích")
    print("- Informační statusbar")
    print("- Context menu (pravé tlačítko)")
    print("- Drag & drop pro JSON soubory")


if __name__ == "__main__":
    describe_gui_appearance()
