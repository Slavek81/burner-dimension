# GUI aplikace pro návrh plynového hořáku a spalovací komory

## Přehled

Kompletní tkinter GUI aplikace pro technický výpočet plynového hořáku a spalovací komory. Aplikace poskytuje uživatelsky přívětivé rozhraní pro všechny výpočetní moduly s profesionálním vzhledem a pokročilými funkcemi.

## Hlavní funkce

### ✅ Dokončené funkce

- **7 záložek** pro různé části výpočtu:
  1. Vstupní parametry
  2. Výpočty spalování  
  3. Návrh hořáku
  4. Návrh komory
  5. Radiační přenos
  6. Tlakové ztráty
  7. Výsledky

- **Validace vstupních dat** s chybovými hlášeními v češtině
- **Načítání/ukládání** parametrů ze/do JSON souborů
- **Export výsledků** do TXT, CSV a Excel formátů
- **Ukazatel průběhu** výpočtu
- **Profesionální vzhled** s proper layout
- **Obsluha chyb** a informační dialogy
- **Podrobné zobrazení** všech výsledků
- **Spustitelnost bez Claude Code**

## Struktura souborů

```
gui/
├── __init__.py          # GUI package initialization
├── gui.py              # Main GUI application
└── README.md           # Tento soubor

# Spouštěcí soubory
main.py                 # Hlavní spouštěč
launch_gui.py           # Rozšířený spouštěč s kontrolou závislostí
test_gui_setup.py       # Test funkčnosti GUI
gui_demo.py             # Demonstrace funkcionality

# Ukázkové soubory
sample_input.json       # Vzorové vstupní parametry
requirements.txt        # Python závislosti
```

## Způsob spuštění

### 1. Základní spuštění
```bash
python3 main.py
```

### 2. Spuštění s kontrolou závislostí
```bash
python3 launch_gui.py
```

### 3. Testování funkčnosti
```bash
python3 test_gui_setup.py
```

### 4. Demonstrační režim
```bash
python3 gui_demo.py
```

## Požadavky

### Základní
- Python 3.7+
- tkinter (obvykle součást Pythonu)

### Volitelné (pro plnou funkcionalnost)
- pandas >= 1.3.0 (pro export do CSV/Excel)
- openpyxl >= 3.0.0 (pro Excel export)
- numpy >= 1.20.0 (pro numerické výpočty)

### Instalace závislostí
```bash
pip install -r requirements.txt
```

## Použití GUI

### Vstupní parametry
1. **Palivo**: Výběr typu paliva (zemní plyn, methan, propan)
2. **Průtoky**: Hmotnostní průtok paliva, koeficient přebytku vzduchu
3. **Provozní podmínky**: Teplota a tlak okolí
4. **Parametry hořáku**: Max. rychlost plynu, tlak přívodu
5. **Parametry komory**: Tepelný výkon, max. teplota, hustota tepelného toku

### Validace vstupů
Aplikace automaticky kontroluje:
- Číselné hodnoty v realistických mezích
- Fyzikální konzistenci parametrů
- Bezpečnostní limity

### Export výsledků
- **TXT**: Formátovaný textový report
- **CSV**: Strukturovaná data pro další zpracování  
- **Excel**: Profesionální tabulky s více listy

### Chybové zprávy
Všechny chyby jsou zobrazeny v češtině s konkrétními pokyny k nápravě.

## Technická implementace

### Architektura
- **Model-View-Controller** separace
- **Threaded calculations** - výpočty neblokují GUI
- **Error handling** na všech úrovních
- **Input validation** s okamžitou zpětnou vazbou

### Klíčové třídy
```python
BurnerCalculatorGUI     # Hlavní GUI třída
ExportDialog           # Dialog pro export výsledků
```

### Výpočetní moduly
GUI integruje všech 5 výpočetních modulů:
- `CombustionCalculator` - spalování
- `BurnerDesigner` - návrh hořáku
- `ChamberDesigner` - návrh komory
- `RadiationCalculator` - radiace
- `PressureLossCalculator` - tlakové ztráty

## Ukázkové použití

### 1. Načtení vstupních parametrů
```python
# Načte sample_input.json
app.load_input_file()
```

### 2. Spuštění výpočtu
Kliknutím na "Spustit výpočet" se:
1. Validují vstupní data
2. Spustí výpočet ve vlastním vlákně
3. Zobrazí výsledky v příslušných záložkách
4. Umožní export výsledků

### 3. Export výsledků
Dialog umožňuje výběr:
- Formát (TXT/CSV/Excel)
- Obsah (vstupní parametry, výsledky, detaily)

## Chybové stavy a řešení

### Časté problémy

1. **"Doba zdržení je příliš dlouhá"**
   - Zvyšte hustotu tepelného toku
   - Snižte požadovaný tepelný výkon

2. **"Neplatná číselná hodnota"**
   - Zkontrolujte formát čísel (desetinná tečka)
   - Ověřte rozsah hodnot

3. **"Chybí závislosti"**
   - Nainstalujte: `pip install pandas openpyxl`

### Debug režim
Pro detailní ladění použijte:
```python
python3 -c "
import logging
logging.basicConfig(level=logging.DEBUG)
exec(open('main.py').read())
"
```

## Vývojové poznámky

### Testování
Aplikace je plně testována:
- Unit testy pro všechny moduly
- Integration testy pro GUI workflow
- Validační testy pro edge cases

### Rozšiřitelnost
GUI je navrženo pro snadné rozšíření:
- Nové záložky lze přidat do `create_widgets()`
- Nové exportní formáty do `ExportDialog`
- Nové validace do `validate_input()`

### Performance
- Asynchronní výpočty neblokují UI
- Progress indikátor pro dlouhé operace
- Lazy loading výsledků

## Licence a podpora

Aplikace je součástí projektu návrhu plynového hořáku.
Pro podporu kontaktujte vývojářský tým.

---

*GUI vytvořeno s využitím tkinter, pandas a moderních Python praktik.*