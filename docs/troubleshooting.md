# Troubleshooting Guide

## Table of Contents
1. [Installation Issues](#installation-issues)
2. [GUI Problems](#gui-problems)
3. [Calculation Errors](#calculation-errors)
4. [Input/Output Issues](#inputoutput-issues)
5. [Performance Problems](#performance-problems)
6. [Common Error Messages](#common-error-messages)
7. [Data File Issues](#data-file-issues)
8. [Platform-Specific Issues](#platform-specific-issues)
9. [Advanced Debugging](#advanced-debugging)
10. [Getting Support](#getting-support)

## Installation Issues

### Python Environment Problems

#### Issue: Python version compatibility
**Symptoms:**
- `SyntaxError` during import
- Module compatibility warnings
- Type hint errors

**Solutions:**
1. **Check Python version:**
   ```bash
   python --version
   # Should be 3.8 or higher
   ```

2. **Upgrade Python if necessary:**
   ```bash
   # Using conda
   conda install python=3.9
   
   # Using pyenv
   pyenv install 3.9.0
   pyenv global 3.9.0
   ```

3. **Use virtual environment:**
   ```bash
   python -m venv burner_env
   source burner_env/bin/activate  # Linux/macOS
   burner_env\Scripts\activate     # Windows
   ```

#### Issue: Missing dependencies
**Symptoms:**
- `ModuleNotFoundError` when importing packages
- Import errors for scientific packages

**Solutions:**
1. **Install all dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install scientific packages separately:**
   ```bash
   pip install numpy pandas matplotlib scipy
   ```

3. **For conda environments:**
   ```bash
   conda install numpy pandas matplotlib scipy
   ```

4. **Check for conflicting packages:**
   ```bash
   pip check
   ```

#### Issue: tkinter not available
**Symptoms:**
- `ModuleNotFoundError: No module named 'tkinter'`
- GUI fails to start

**Solutions:**
1. **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt-get install python3-tk
   ```

2. **Linux (CentOS/RHEL):**
   ```bash
   sudo yum install tkinter
   # or
   sudo dnf install python3-tkinter
   ```

3. **macOS:**
   ```bash
   # If using Homebrew Python
   brew install python-tk
   
   # If using system Python, reinstall with tkinter
   brew reinstall python@3.9
   ```

4. **Windows:**
   - Reinstall Python with "tcl/tk and IDLE" option checked
   - Or install from Microsoft Store

### Package Installation Issues

#### Issue: Compilation errors during pip install
**Symptoms:**
- C compiler errors
- Failed building wheel for packages
- Microsoft Visual C++ errors (Windows)

**Solutions:**
1. **Windows - Install Visual Studio Build Tools:**
   - Download and install Microsoft C++ Build Tools
   - Or install Visual Studio Community

2. **Use pre-compiled wheels:**
   ```bash
   pip install --only-binary=all numpy pandas matplotlib
   ```

3. **Use conda instead of pip:**
   ```bash
   conda install numpy pandas matplotlib scipy
   ```

4. **Clear pip cache:**
   ```bash
   pip cache purge
   pip install --no-cache-dir -r requirements.txt
   ```

## GUI Problems

### Window Display Issues

#### Issue: GUI window doesn't appear
**Symptoms:**
- Python script runs but no window shows
- Process runs in background

**Solutions:**
1. **Check display environment (Linux):**
   ```bash
   echo $DISPLAY
   # Should show something like :0 or :1
   ```

2. **For SSH connections, enable X11 forwarding:**
   ```bash
   ssh -X username@hostname
   ```

3. **Try different GUI backend:**
   ```python
   import matplotlib
   matplotlib.use('TkAgg')  # Force TkAgg backend
   ```

4. **Run with explicit display:**
   ```bash
   DISPLAY=:0 python main.py
   ```

#### Issue: GUI appears but is unresponsive
**Symptoms:**
- Window opens but buttons don't work
- Interface freezes during calculations

**Solutions:**
1. **Check for blocking operations:**
   - Long calculations block GUI thread
   - Add progress indicators or threading

2. **Increase system resources:**
   ```bash
   # Check available memory
   free -h  # Linux
   
   # Check CPU usage
   top      # Linux/macOS
   ```

3. **Update tkinter:**
   ```bash
   # Reinstall Python with latest tkinter
   brew reinstall python@3.9  # macOS
   ```

### Layout and Rendering Issues

#### Issue: GUI elements are misaligned or cut off
**Symptoms:**
- Buttons or text fields not visible
- Scrollbars not working
- Text truncated

**Solutions:**
1. **Check screen resolution and scaling:**
   ```python
   import tkinter as tk
   root = tk.Tk()
   print(f"Screen: {root.winfo_screenwidth()}x{root.winfo_screenheight()}")
   print(f"DPI: {root.winfo_fpixels('1i')}")
   ```

2. **Adjust GUI scaling:**
   ```python
   # In GUI initialization
   root.tk.call('tk', 'scaling', 2.0)  # Double scaling
   ```

3. **Set minimum window size:**
   ```python
   root.minsize(800, 600)
   ```

4. **For high-DPI displays:**
   ```python
   import tkinter as tk
   try:
       from tkinter import ttk
       # Enable DPI awareness on Windows
       import ctypes
       ctypes.windll.shcore.SetProcessDpiAwareness(1)
   except:
       pass
   ```

## Calculation Errors

### Input Validation Errors

#### Issue: Invalid fuel type error
**Symptoms:**
- `ValueError: Unsupported fuel type`
- Available fuels not recognized

**Solutions:**
1. **Check available fuel types:**
   ```python
   from src.combustion import CombustionCalculator
   calc = CombustionCalculator()
   print(calc.get_available_fuels())
   ```

2. **Verify fuel data file:**
   ```bash
   cat data/fuels.json | head -20
   ```

3. **Use exact fuel type names:**
   ```python
   # Correct
   fuel_type = "natural_gas"
   
   # Incorrect
   fuel_type = "Natural Gas"  # Case sensitive
   ```

#### Issue: Pressure calculation fails
**Symptoms:**
- `CalculationError: Insufficient supply pressure`
- Negative pressure values

**Solutions:**
1. **Check input ranges:**
   ```python
   # Valid pressure ranges
   supply_pressure = 2000  # Pa (minimum ~1000 Pa)
   operating_pressure = 1500  # Pa
   ```

2. **Increase supply pressure:**
   ```python
   # If pressure drop is too high
   supply_pressure *= 1.5  # Increase by 50%
   ```

3. **Reduce system losses:**
   - Use larger pipe diameters
   - Minimize fittings and bends
   - Choose smoother pipe materials

### Physical Constraint Violations

#### Issue: Flame temperature too high/low
**Symptoms:**
- Temperature outside realistic range
- Warning messages about temperature limits

**Solutions:**
1. **Adjust excess air ratio:**
   ```python
   # Higher lambda reduces temperature
   excess_air_ratio = 1.3  # Instead of 1.1
   ```

2. **Check fuel properties:**
   ```python
   props = calc.get_fuel_properties(fuel_type)
   print(f"LHV: {props['properties']['lower_heating_value_mass']}")
   ```

3. **Verify calculation method:**
   - Check if using appropriate correlations
   - Consider heat losses in real systems

#### Issue: Impossible burner dimensions
**Symptoms:**
- Extremely small or large burner diameters
- Unrealistic velocities

**Solutions:**
1. **Check power-to-size ratio:**
   ```python
   # Typical range: 1-5 MW/m² for burner area
   power_density = required_power / burner_area
   ```

2. **Adjust target velocity:**
   ```python
   # Typical gas velocities: 10-50 m/s
   target_velocity = 25.0  # m/s
   ```

3. **Review fuel flow calculations:**
   ```python
   fuel_flow = required_power / heating_value
   # Check if fuel_flow is reasonable
   ```

## Input/Output Issues

### File Access Problems

#### Issue: Cannot load fuel data
**Symptoms:**
- `FileNotFoundError: data/fuels.json`
- JSON parsing errors

**Solutions:**
1. **Check file existence:**
   ```bash
   ls -la data/fuels.json
   ```

2. **Create missing directory:**
   ```bash
   mkdir -p data
   ```

3. **Validate JSON format:**
   ```bash
   python -m json.tool data/fuels.json
   ```

4. **Fix JSON syntax errors:**
   ```json
   {
     "fuels": {
       "natural_gas": {
         "name": "Natural Gas",
         "properties": {
           "lower_heating_value_mass": 50000000
         }
       }
     }
   }
   ```

#### Issue: Cannot save output files
**Symptoms:**
- Permission denied errors
- Output directory not found

**Solutions:**
1. **Create output directory:**
   ```bash
   mkdir -p output
   chmod 755 output
   ```

2. **Check disk space:**
   ```bash
   df -h  # Check available space
   ```

3. **Fix permissions:**
   ```bash
   chmod 644 output/*.txt
   chmod 755 output/
   ```

4. **Use absolute paths:**
   ```python
   import os
   output_dir = os.path.abspath("output")
   ```

### Data Export Issues

#### Issue: Charts not saving
**Symptoms:**
- Empty PDF/PNG files
- Matplotlib errors

**Solutions:**
1. **Check matplotlib backend:**
   ```python
   import matplotlib
   print(matplotlib.get_backend())
   matplotlib.use('Agg')  # For headless systems
   ```

2. **Install additional dependencies:**
   ```bash
   pip install pillow  # For image formats
   ```

3. **Set proper DPI:**
   ```python
   plt.savefig('chart.png', dpi=300, bbox_inches='tight')
   ```

4. **Handle memory issues:**
   ```python
   plt.close('all')  # Close figures after saving
   ```

#### Issue: Excel export fails
**Symptoms:**
- `ModuleNotFoundError: openpyxl`
- Corrupted Excel files

**Solutions:**
1. **Install Excel dependencies:**
   ```bash
   pip install openpyxl xlsxwriter
   ```

2. **Use alternative format:**
   ```python
   # If Excel fails, use CSV
   df.to_csv('output.csv', index=False)
   ```

3. **Check data types:**
   ```python
   # Ensure numeric data is proper type
   df = df.astype({'column': 'float64'})
   ```

## Performance Problems

### Slow Calculations

#### Issue: Long calculation times
**Symptoms:**
- GUI freezes during calculations
- Timeouts or user impatience

**Solutions:**
1. **Profile code performance:**
   ```python
   import time
   start_time = time.time()
   result = expensive_calculation()
   print(f"Calculation took: {time.time() - start_time:.2f}s")
   ```

2. **Optimize iterative calculations:**
   ```python
   # Use better initial guesses
   # Reduce convergence tolerance if appropriate
   tolerance = 1e-6  # Instead of 1e-8
   ```

3. **Use vectorized operations:**
   ```python
   import numpy as np
   # Instead of loops, use numpy arrays
   results = np.array([calc(x) for x in values])
   ```

4. **Add progress indicators:**
   ```python
   from tqdm import tqdm
   for i in tqdm(range(iterations)):
       # calculations
   ```

### Memory Issues

#### Issue: Out of memory errors
**Symptoms:**
- `MemoryError` exceptions
- System becomes unresponsive

**Solutions:**
1. **Monitor memory usage:**
   ```python
   import psutil
   import os
   process = psutil.Process(os.getpid())
   print(f"Memory: {process.memory_info().rss / 1024 / 1024:.1f} MB")
   ```

2. **Process data in chunks:**
   ```python
   # Instead of loading all data at once
   for chunk in pd.read_csv('large_file.csv', chunksize=1000):
       process(chunk)
   ```

3. **Clear variables:**
   ```python
   del large_variable
   import gc
   gc.collect()
   ```

## Common Error Messages

### "Module not found" Errors

**Error:** `ModuleNotFoundError: No module named 'src'`

**Cause:** Python path issues or running from wrong directory

**Solutions:**
1. **Run from project root:**
   ```bash
   cd /path/to/burner-dimension
   python main.py
   ```

2. **Add to Python path:**
   ```python
   import sys
   sys.path.append('/path/to/project')
   ```

3. **Use relative imports correctly:**
   ```python
   from .combustion import CombustionCalculator  # Relative
   from src.combustion import CombustionCalculator  # Absolute
   ```

### Calculation Validation Errors

**Error:** `ValueError: Excess air ratio must be >= 1.0`

**Cause:** Invalid input parameter

**Solution:**
```python
excess_air_ratio = max(1.0, user_input)  # Ensure minimum value
```

**Error:** `CalculationError: Convergence failed after maximum iterations`

**Cause:** Iterative calculation didn't converge

**Solutions:**
1. **Improve initial guess:**
   ```python
   initial_guess = better_estimate()
   ```

2. **Increase iteration limit:**
   ```python
   max_iterations = 1000  # Instead of 100
   ```

3. **Check input validity:**
   ```python
   if not is_physically_reasonable(inputs):
       raise ValueError("Inputs outside valid range")
   ```

## Data File Issues

### Corrupted Fuel Database

#### Issue: JSON parsing errors in fuel data
**Symptoms:**
- `json.JSONDecodeError`
- Missing fuel properties

**Solutions:**
1. **Validate JSON syntax:**
   ```bash
   python -c "import json; json.load(open('data/fuels.json'))"
   ```

2. **Restore from backup:**
   ```bash
   cp data/fuels.json.bak data/fuels.json
   ```

3. **Recreate fuel database:**
   ```json
   {
     "constants": {
       "universal_gas_constant": 8314.46,
       "stefan_boltzmann_constant": 5.67e-8
     },
     "fuels": {
       "natural_gas": {
         "name": "Natural Gas",
         "properties": {
           "lower_heating_value_mass": 50000000,
           "molecular_weight": 16.04,
           "density": 0.717,
           "air_fuel_ratio_mass": 17.2
         }
       }
     }
   }
   ```

### Missing Configuration Files

#### Issue: Default settings not loading
**Symptoms:**
- Using hardcoded defaults
- Configuration changes not persisting

**Solutions:**
1. **Create default config:**
   ```json
   {
     "output_directory": "output",
     "default_fuel": "natural_gas",
     "gui_theme": "default",
     "auto_save": true,
     "log_level": "INFO"
   }
   ```

2. **Handle missing config gracefully:**
   ```python
   try:
       with open('config.json', 'r') as f:
           config = json.load(f)
   except FileNotFoundError:
       config = get_default_config()
   ```

## Platform-Specific Issues

### Windows-Specific Problems

#### Issue: Path separator problems
**Symptoms:**
- File not found errors
- Invalid path errors

**Solutions:**
1. **Use os.path.join:**
   ```python
   import os
   path = os.path.join('data', 'fuels.json')
   ```

2. **Use pathlib (Python 3.4+):**
   ```python
   from pathlib import Path
   path = Path('data') / 'fuels.json'
   ```

#### Issue: Long path names
**Symptoms:**
- File operations fail on deep directory structures

**Solutions:**
1. **Enable long path support:**
   - Windows 10: Enable via Group Policy or Registry
   - Use UNC paths: `\\?\C:\very\long\path`

2. **Use shorter paths:**
   ```python
   # Move project to shorter path
   # C:\burner\ instead of C:\very\long\path\to\project\
   ```

### Linux-Specific Problems

#### Issue: Display issues in SSH
**Symptoms:**
- GUI won't start over SSH
- X11 errors

**Solutions:**
1. **Enable X11 forwarding:**
   ```bash
   ssh -X username@hostname
   # or
   ssh -Y username@hostname  # Trusted X11 forwarding
   ```

2. **Install X11 libraries:**
   ```bash
   sudo apt-get install xauth x11-apps
   ```

3. **Use VNC or remote desktop instead:**
   ```bash
   # Install VNC server
   sudo apt-get install tightvncserver
   ```

#### Issue: Permission denied
**Symptoms:**
- Cannot write to directories
- Cannot execute scripts

**Solutions:**
1. **Check file permissions:**
   ```bash
   ls -la main.py
   chmod +x main.py
   ```

2. **Check directory permissions:**
   ```bash
   chmod 755 output/
   chmod 644 output/*.txt
   ```

### macOS-Specific Problems

#### Issue: Security restrictions
**Symptoms:**
- "App cannot be opened" errors
- Quarantine warnings

**Solutions:**
1. **Remove quarantine:**
   ```bash
   xattr -r -d com.apple.quarantine /path/to/app
   ```

2. **Allow in Security & Privacy:**
   - System Preferences → Security & Privacy
   - Allow app to run

#### Issue: Python version conflicts
**Symptoms:**
- Multiple Python versions
- Wrong version being used

**Solutions:**
1. **Use specific Python version:**
   ```bash
   python3.9 main.py
   ```

2. **Create alias:**
   ```bash
   alias python=/usr/local/bin/python3.9
   ```

3. **Use pyenv:**
   ```bash
   pyenv local 3.9.0
   ```

## Advanced Debugging

### Enabling Debug Mode

#### Comprehensive Logging
1. **Enable debug logging:**
   ```python
   import logging
   logging.basicConfig(
       level=logging.DEBUG,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
       handlers=[
           logging.FileHandler('debug.log'),
           logging.StreamHandler()
       ]
   )
   ```

2. **Add debug prints to calculations:**
   ```python
   def calculate_something(inputs):
       print(f"DEBUG: Inputs = {inputs}")
       result = complex_calculation(inputs)
       print(f"DEBUG: Result = {result}")
       return result
   ```

### Performance Profiling

#### Using cProfile
```python
import cProfile
import pstats

def profile_calculation():
    cProfile.run('main_calculation()', 'profile_stats')
    stats = pstats.Stats('profile_stats')
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # Top 10 functions
```

#### Memory Profiling
```python
from memory_profiler import profile

@profile
def memory_intensive_function():
    # Your function here
    pass
```

### Interactive Debugging

#### Using pdb
```python
import pdb

def problematic_function():
    pdb.set_trace()  # Debugger will stop here
    # Your code here
```

#### Using ipdb (enhanced debugger)
```bash
pip install ipdb
```

```python
import ipdb
ipdb.set_trace()
```

## Getting Support

### Information to Collect

Before seeking support, collect the following information:

1. **System Information:**
   ```bash
   python --version
   pip list | grep -E "(numpy|pandas|matplotlib|tkinter)"
   uname -a  # Linux/macOS
   systeminfo  # Windows
   ```

2. **Error Information:**
   ```python
   import traceback
   try:
       problematic_code()
   except Exception as e:
       print(f"Error: {e}")
       traceback.print_exc()
   ```

3. **Configuration Details:**
   - Input parameters used
   - Configuration files content
   - Environment variables

### Creating Minimal Reproducible Example

```python
# Minimal example that reproduces the issue
from src.combustion import CombustionCalculator

try:
    calc = CombustionCalculator()
    result = calc.calculate_combustion_products(
        fuel_type="natural_gas",
        fuel_flow_rate=0.01,
        excess_air_ratio=1.2
    )
    print("Success:", result.adiabatic_flame_temperature)
except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()
```

### Support Channels

1. **GitHub Issues:**
   - Create detailed bug reports
   - Include system information and error logs
   - Provide minimal reproducible examples

2. **Documentation:**
   - Check API Reference for correct usage
   - Review User Guide for best practices
   - Consult Installation Guide for setup issues

3. **Community:**
   - Stack Overflow with relevant tags
   - Scientific computing forums
   - Engineering calculation communities

### Self-Diagnosis Checklist

Before seeking support, verify:

- [ ] Python version is 3.8 or higher
- [ ] All dependencies are installed correctly
- [ ] Running from correct directory
- [ ] Input files exist and are valid
- [ ] Sufficient disk space and memory
- [ ] Firewall/antivirus not blocking
- [ ] Latest version of the application
- [ ] Tried suggested solutions from this guide

---

*This troubleshooting guide covers the most common issues encountered when using the Gas Burner Calculator. For issues not covered here, please create a GitHub issue with detailed information about your problem.*