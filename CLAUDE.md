# Projekt: Dimenzování plynového hořáku a spalovací komory

## Kontext
Navrhnout a implementovat Python aplikaci s GUI (tkinter), která umožní technický výpočet hořáku a spalovací komory pro plynná paliva včetně:
- výpočtu spalování
- dimenzování hořáku a komory
- výpočtu radiační výměny tepla
- výpočtu tlakových ztrát
- grafických výstupů a exportu výstupního protokolu

## Goals
- GUI vytvoř pomocí knihovny tkinter
- vstupní soubory se musí načítat pomocí souborů json
- výstupy ukládat do txt, csv a excelu
- grafy ukládat do pdf, png a jpeg (mít možnost volby)
- kontrola vstupních dat - pokud je nějaká chyba ve vstupech, zobrazí se okno s vypsáním problémů
- Spustitelnost bez Claude Code

## Tasks (check-list)
- [ ] Najít na internetu potřebné informace k výpočtům - výzkum
- [ ] Vytvořit strukturu složek a souborů
- [ ] Vytvoř soukromý repozitář na mém githubu s názvem "burner-dimension"
- [ ] Tvorba hlavních souborů aplikace
- [ ] Vytvořit GUI aplikace
- [ ] Zkontrolovat, že třídy a metody obsahují docstringy a kód je řádně okomentován - vše anglicky
- [ ] Zajistit, že výstup je česky
- [ ] Vygenerovat (aktualizuj) README.md a PRD.md v angličtině
- [ ] Vygeneruj (aktualizuj pokud je potřeba) dokumentaci projektu do adresáře "docs" 
- [ ] Pushni finální verzi na github

## 🔁 Subtasky
Claude Code musí používat subtasky pro každý modul zvlášť. Každý `/run` příkaz výše odpovídá samostatnému subtasku.

## ⚙️ Vývojové kroky
1. `/run define-use-cases` – zformuluj scénáře použití
2. `/run design-code-structure` – navrhni strukturu modulu
3. `/run generate-calculation-module` – generuj spalovací výpočty
4. `/run generate-burner-dimensioning` – výpočet hořáku
5. `/run generate-chamber-dimensioning` – výpočet komory
6. `/run calculate-radiation-transfer` – výpočet radiace
7. `/run calculate-pressure-losses` – výpočet Δp
8. `/run generate-gui` – vygeneruj tkinter GUI
9. `/run generate-plots` – grafy
10. `/run export-report` – export výpočtu
11. `/run generate-docs` – dokumentace
12. `/run diagnose-ci-errors` – analýza chyb z CI
13. Případně tvorba dalších souborů

## Structure
### Předběžný návrh struktury
```
burner_calc/
├── main.py
├── src/
│   ├── combustion.py
│   ├── burner_design.py
│   ├── chamber_design.py
│   ├── radiation.py
│   ├── pressure_losses.py
│   ├── report.py
│   └── visualization.py
├── gui/
│   └── gui.py
├── data/
│   └── fuels.json
├── output/
│   └── report.txt
├── docs/
│   └── ...
├── tests/
│   └── ...
└── CLAUDE.md, PRD.md, README.md
```
### Dle potřeby strukturu uprav

## Coding Guidelines 
- Používejte type hints pro všechny parametry a návratové hodnoty
- Dodržujte PEP 8 naming conventions
- Maximální délka řádku: 88 znaků
- Používejte dataclasses pro datové struktury
- Kód v angličtině, výstupy v češtině
- Výpočetní funkce musí být odděleny od GUI, aplikace musí být spustitelná i bez GUI
- Testy, dokumentace a výpočty budou v samostatných modulech
- Všechny třídy a metody musí obsahovat docstringy a komentáře kódu v angličtině.
- Na začátku každého souboru napiš umístění, např. "#src/main.py"
- Projekt v Pythonu
- Projekt bude 100 % samostatně spustitelný
- Generguj (aktualizuj) soubor README.md a PRD.md v **angličtině**
- Generuj dokumentaci k projektu: **v angličtině**
- Pokud budeš dělat nějaké změny, tak vždy soubor README.md a PRD.md aktualizuj, stejně tak dokumentaci projektu

## 📝 POVINNÉ PSANÍ NÁZVŮ
### Pro psaní názvů souborů, tříd, metod a proměnných vždy používej tato pravidla:
- **English only** – jasná, popisná angličtina, zkratky jen když jsou standardní (API, HTTP).
- **Soubor** → `snake_case` + přípona (`data_loader.py`).
- **Třída** → `CamelCase` (`HeatExchangerModel`, `JsonParser`).
- **Funkce / metoda** → `snake_case` s slovesem (`calculate_pressure_drop`).
- **Proměnná** → `snake_case` s podstatným jménem (`pressure_drop`); smyčkové indexy `i`,`j`,`k` jen do 3 hloubek.
- **Konstanta** (modul) → `UPPER_SNAKE_CASE` (`MAX_ITERATIONS`).
- **Privátní / asynchronní** → `_helper()`, `task_async()`.
- **Abstraktní báze & testy** → `BaseController`, soubory `test_*.py`.
- **Konzistence** – nikdy nemíchat styly; před mergem přejmenovat vše nevyhovující.
- **Kontrola** – automatické lintry (`pylint`, `flake8-naming`) + PR review tyto zásady vynucují.

## Workflow (Claude)
- Pomáhej s refaktoringem a přehledností kódu
- Dělej refaktoring
- Přemýšlej nad budoucí rozšiřitelností aplikace
- Využívej vhodné návrhové vzory
- Sleduj úkoly a automaticky je odškrtni, jakmile je hotovo
- Měj přístup ke všem souborům v projektu
- **VŽDY dodržuj workflow kontrol kvality** - viz sekce níže
- **KÓD VŽDY KONTROLUJ** - flake8 + bandit + testy
- **NIKDY necommituj kód bez kontrol** - nejdřív flake8 + testy

## 📝 POVINNÉ KOMENTOVÁNÍ KÓDU

### 🚨 CRITICAL: KAŽDÝ SOUBOR MUSÍ MÍT KOMENTÁŘE!

#### 1. FILE HEADERS (POVINNÉ):
```python
"""
src/player.py

Player management system for Demon Attack game.
Handles player movement, shooting mechanics, and collision detection.
"""
```

#### 2. CLASS DOCUMENTATION (POVINNÉ):
```python
class Player:
    """
    Represents the player's laser cannon in the game.
    
    The Player class handles horizontal movement, shooting with rate limiting,
    and collision detection. Player is restricted to bottom area of screen.
    
    Attributes:
        rect (pygame.Rect): Position and collision boundaries
        speed (int): Movement speed in pixels per frame
        fire_rate (int): Minimum milliseconds between shots
        last_shot (int): Timestamp of last shot fired
    """
```

#### 3. METHOD DOCUMENTATION (POVINNÉ):
```python
def update(self, keys_pressed):
    """
    Update player position and state based on input.
    
    Processes keyboard input for movement and applies boundary checking
    to prevent player from moving outside screen boundaries.
    
    Args:
        keys_pressed (pygame.key.ScancodeWrapper): Current keyboard state
        
    Note:
        Movement is restricted to horizontal axis only.
        Speed is constant regardless of frame rate.
    """
```

#### 4. COMPLEX LOGIC COMMENTS (POVINNÉ):
```python
# Calculate wave movement using sine function for smooth enemy motion
wave_offset = math.sin(self.wave_time * self.wave_frequency) * self.wave_amplitude

# Rate limiting: prevent bullet spam by checking time since last shot
if current_time - self.last_shot >= self.fire_rate:
    # Sufficient time has passed, allow shooting
    self.last_shot = current_time
    return True
```

### 📋 KOMENTOVÁNÍ CHECKLIST:

**File Level:**
- [ ] File header s umístěním (např. "src/player.py")
- [ ] Module purpose description
- [ ] Author/date info pokud relevantní

**Class Level:**
- [ ] Class purpose a responsibility
- [ ] Key attributes documented
- [ ] Usage examples pokud complex

**Method Level:**
- [ ] Method purpose a behavior
- [ ] Parameters s types a descriptions
- [ ] Return values documented
- [ ] Side effects noted

**Code Level:**
- [ ] Complex algorithms explained
- [ ] Magic numbers s význam
- [ ] Non-obvious logic clarified
- [ ] Performance considerations noted


## 🧪 POVINNÉ KONTROLY KVALITY KÓDU - ZERO FAILURES POLICY
**⚠️ KRITICKÉ: KAŽDÝ COMMIT MUSÍ PROJÍT IDENTICKÝMI KONTROLAMI JAKO GITHUB CI!**

### 🚨 POVINNÉ KROKY PŘED KAŽDÝM COMMITEM:

#### 1. INSTALACE PRE-COMMIT HOOKS (jednorázově):
```bash
make install
# Nebo manuálně:
pip install pre-commit pytest-cov flake8 bandit black
pre-commit install
```

#### 2. LOKÁLNÍ CI SIMULACE (POVINNÉ PŘED KAŽDÝM PUSHEM):
```bash
# Spustí IDENTICKÉ kontroly jako GitHub Actions CI
make ci-local
```

**Tento příkaz spustí v tomto pořadí:**
1. `flake8 src/ tests/ --max-line-length=100 --exclude=__pycache__`
2. `bandit -r src/ --severity-level medium`  
3. `python -m pytest tests/ -v --tb=short`
4. `python -m pytest tests/ --cov=src --cov-report=term-missing`

#### 3. PRE-COMMIT HOOKS AUTOMATICKY KONTROLUJÍ:
- **Flake8** - kódový styl (identický s CI)
- **Bandit** - bezpečnostní kontrola (identický s CI)  
- **Pytest** - všechny testy (identický s CI)
- **Coverage** - pokrytí kódu (identický s CI)

#### 4. Kontrola komentářů a docstringů
- **kontroluj** úplnost a kvalitu docstringů a komentářů
- **doplň** komentáře a docstringy pokud chybí

### 🔄 WORKFLOW - ZERO CI FAILURES:

```bash
# 1. Proveď změny v kódu
# 2. POVINNĚ spusť lokální CI simulaci  
make ci-local

# 3. Pokud vše prošlo ✅, teprve pak:
git add .
git commit -m "commit message"  # Pre-commit hooks se spustí automaticky
git push origin main

# 4. Pokud něco selhalo ❌:
# - OPRAV všechny chyby  
# - Znovu spusť make ci-local
# - Teprve pak commituj
```

### ⚡ RYCHLÉ PŘÍKAZY:

```bash
make quality-check  # Jen flake8 + bandit (rychlé)
make test-all      # Jen testy + coverage (rychlé)  
make lint          # Jen flake8
make security-check # Jen bandit
make clean         # Vyčistí dočasné soubory
```

### 🎯 PRAVIDLA ZERO FAILURES:

1. **❌ NIKDY nepushuj** bez `make ci-local`
2. **❌ NIKDY neignoruj** pre-commit hook failures  
3. **❌ NIKDY necommituj** pokud lokální CI selhalo
4. **✅ VŽDY oprav** všechny chyby lokálně před pushem
5. **✅ VŽDY používaj** identické příkazy jako CI

### 🔧 TROUBLESHOOTING:

**Pre-commit hook selhal?**
```bash
# Zkontroluj co selhalo
pre-commit run --all-files

# Oprav chyby a zkus znovu
git add .
git commit -m "message"
```

**CI na GitHubu stále selhává?**
```bash
# Stáhni nejnovější změny a znovu testuj
git pull origin main
make ci-local

# Pokud lokálně projde, ale CI selhává → kontaktuj support
```

### 📋 CHECKLIST PŘED KAŽDÝM PUSHEM:

- [ ] `make ci-local` prošlo bez chyb ✅
- [ ] Pre-commit hooks jsou nainstalované ✅  
- [ ] Všechny testy procházejí ✅
- [ ] Flake8 nehlásí chyby ✅
- [ ] Bandit nehlásí medium/high problémy ✅
- [ ] Coverage je adekvátní ✅

**Pouze pokud je vše ✅, push na GitHub!**


## 📝 Dokumentace projektu

### 🔧 Struktura
Claude by měl vytvářet a aktualizovat následující dokumenty:

| Soubor | Účel | Jazyk |
|--------|------|--------|
| `README.md` | Úvodní popis projektu, návod ke spuštění, příklady použití | 🇬🇧 anglicky |
| `PRD.md` | Specifikace produktu – co má aplikace umět, pro koho a proč | 🇬🇧 anglicky |
| `docs/` nebo `docs.md` | Technická dokumentace – jak projekt funguje uvnitř | 🇬🇧 anglicky |
| Komentáře v kódu | Popis tříd, funkcí, algoritmů | 💬 anglicky |
| Výstupy v terminálu nebo GUI | Zprávy pro uživatele | 🇨🇿 česky |

### 📋 Pokyny pro Claude Code

- Dokumentaci generuj průběžně během vývoje - anglicky
- Pokud upravíš kód, aktualizuj dokumentaci
- Dokumentuj každou třídu, funkci a modul (`docstring` + komentáře)
- Generuj vývojovou dokumentaci do `docs/` nebo `docs.md`
- Odkazuj v `README.md` na další dokumentaci

### 🧪 Kvalita dokumentace

Claude by měl:
- Vysvětlit architekturu (např. vrstvy, moduly, závislosti)
- Přidat příklady použití funkcí (ideálně testovatelné)
- Uvést názvy autorů, datum a historii verzí (volitelně)

### ✅ Automatizované požadavky

1. Po každé změně v kódu zkontroluj a aktualizuj komentáře.
2. Po dokončení modulu spusť příkaz:
   ```
   /run generate-docs-for src/
   ```
3. Před commitem proveď:
   - kontrolu syntaxe dokumentace (`markdownlint`, `docformatter`)
   - kontrolu, zda nejsou `TODO` nebo prázdné sekce


## 🔄 Git Workflow - DŮLEŽITÉ!
- **AUTOMATICKY commituj** po každé významné změně (nový soubor, oprava, feature)
- **VŽDY pushuj na GitHub** po commitu - POVINNÉ!
- **COMMIT MESSAGE formát**: "feat/fix/docs: popis změny"
- **PUSH IHNED** po dokončení úkolu nebo na konci práce
- **Commit často** - i malé změny, lepší než ztratit práci

## Git příkazy které MUSÍŠ používat:
```bash
git add .
git commit -m "feat: popis změny"  
git push origin main
```
**DŮLEŽITÉ**: Po KAŽDÉM commitu MUSÍŠ pushovat na GitHub!

## WORKFLOW testing - DŮLEŽITÉ
- pro všechny důležité metody a funkce a celou aplikaci vytvářej vhodné testy
 - **AUTOMATICKY spouštěj** tohoto agent @tester při větších změnách v kódu. Testovací soubory vytvářej v adresáři @tests

## 🤖 MCP servery

Při vývoji se povoluje využití MCP serverů definovaných v `.claude.json` pro:
- extrakci dat z datasheetů
- ověřování fyzikálních konstant
- doplňkový výpočet pomocí externího agenta

## Vývojové proměnné
- `language`: Python 3.10
- `framework`: pytest

## Spuštění
```bash
python main.py
```








