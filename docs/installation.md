# Installation Guide

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Methods](#installation-methods)
3. [Dependencies](#dependencies)
4. [Setup Instructions](#setup-instructions)
5. [Configuration](#configuration)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Installation](#advanced-installation)

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10, macOS 10.14, or Linux (Ubuntu 18.04+)
- **Python Version**: Python 3.8 or higher
- **RAM**: 4 GB minimum, 8 GB recommended
- **Storage**: 500 MB free disk space
- **Display**: 1024x768 resolution minimum

### Recommended Requirements
- **Operating System**: Latest stable versions
- **Python Version**: Python 3.9 or 3.10
- **RAM**: 8 GB or more
- **Storage**: 1 GB free disk space
- **Display**: 1920x1080 or higher resolution
- **Graphics**: Dedicated graphics card for better visualization performance

### Software Dependencies
- Python 3.8+
- pip (Python package installer)
- Git (for development installation)

## Installation Methods

### Method 1: Direct Download (Recommended for Users)

1. **Download the Application**
   ```bash
   git clone https://github.com/username/burner-dimension.git
   cd burner-dimension
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python main.py
   ```

### Method 2: Virtual Environment Installation (Recommended for Development)

1. **Create Virtual Environment**
   ```bash
   python -m venv burner_env
   ```

2. **Activate Virtual Environment**
   
   **Windows:**
   ```bash
   burner_env\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source burner_env/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Application**
   ```bash
   python main.py
   ```

### Method 3: Docker Installation (Advanced Users)

1. **Build Docker Image**
   ```bash
   docker build -t burner-calculator .
   ```

2. **Run Container**
   ```bash
   docker run -p 8080:8080 burner-calculator
   ```

## Dependencies

### Core Dependencies

#### Python Packages
```
numpy>=1.21.0
pandas>=1.3.0
matplotlib>=3.4.0
tkinter (included with Python)
json (standard library)
dataclasses (standard library)
typing (standard library)
```

#### Development Dependencies
```
pytest>=6.0.0
pytest-cov>=2.12.0
flake8>=3.9.0
black>=21.0.0
pre-commit>=2.15.0
bandit>=1.7.0
```

### Optional Dependencies

#### Enhanced Visualization
```
plotly>=5.0.0          # Interactive plots
seaborn>=0.11.0        # Statistical visualizations
```

#### Advanced Data Handling
```
openpyxl>=3.0.0        # Excel file support
xlsxwriter>=3.0.0      # Excel writing capabilities
```

#### Scientific Computing
```
scipy>=1.7.0           # Advanced mathematical functions
sympy>=1.8.0           # Symbolic mathematics
```

## Setup Instructions

### Step 1: Python Installation

#### Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer with "Add Python to PATH" checked
3. Verify installation: `python --version`

#### macOS
1. **Using Homebrew (Recommended):**
   ```bash
   brew install python@3.9
   ```

2. **Using Official Installer:**
   - Download from [python.org](https://www.python.org/downloads/)
   - Run the installer package

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

#### Linux (CentOS/RHEL)
```bash
sudo yum install python3 python3-pip
```

### Step 2: Get the Application

#### Option A: Download ZIP
1. Go to the GitHub repository
2. Click "Code" → "Download ZIP"
3. Extract to desired location

#### Option B: Git Clone
```bash
git clone https://github.com/username/burner-dimension.git
cd burner-dimension
```

### Step 3: Install Dependencies

#### Basic Installation
```bash
pip install -r requirements.txt
```

#### Development Installation
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### Full Installation (All Features)
```bash
pip install -r requirements.txt
pip install plotly seaborn scipy sympy openpyxl xlsxwriter
```

### Step 4: Initial Setup

1. **Create Output Directory**
   ```bash
   mkdir -p output
   mkdir -p input
   ```

2. **Verify Data Files**
   ```bash
   ls data/fuels.json
   ```

3. **Test Installation**
   ```bash
   python -c "import src.combustion; print('Installation successful')"
   ```

## Configuration

### Application Configuration

#### Default Configuration
The application uses default settings that work for most installations. No additional configuration is required for basic usage.

#### Custom Configuration
Create a `config.json` file in the root directory:

```json
{
  "output_directory": "output",
  "input_directory": "input",
  "default_fuel": "natural_gas",
  "gui_theme": "default",
  "plot_style": "seaborn",
  "auto_save": true,
  "backup_count": 3,
  "log_level": "INFO"
}
```

### Environment Variables

#### Optional Environment Variables
```bash
export BURNER_CALC_OUTPUT_DIR="/path/to/output"
export BURNER_CALC_LOG_LEVEL="DEBUG"
export BURNER_CALC_THEME="dark"
```

#### Setting Environment Variables

**Windows:**
```cmd
set BURNER_CALC_OUTPUT_DIR=C:\path\to\output
```

**macOS/Linux:**
```bash
export BURNER_CALC_OUTPUT_DIR="/path/to/output"
```

### GUI Configuration

#### Display Settings
- The application automatically detects screen resolution
- Scaling is handled automatically
- For high-DPI displays, ensure system scaling is configured properly

#### Theme Customization
- Default theme works on all systems
- Dark theme available for supported systems
- Custom themes can be configured in `config.json`

## Verification

### Basic Verification Tests

#### 1. Import Test
```bash
python -c "
import src.combustion
import src.burner_design
import src.chamber_design
import src.radiation
import src.pressure_losses
import src.visualization
import src.report
print('All modules imported successfully')
"
```

#### 2. GUI Test
```bash
python gui/gui.py
```
- Verify the main window opens
- Check all tabs are accessible
- Confirm input fields are responsive

#### 3. Calculation Test
```bash
python -c "
from src.combustion import CombustionCalculator
calc = CombustionCalculator()
result = calc.calculate_combustion_products('natural_gas', 0.01, 1.2)
print(f'Calculation test passed: {result.heat_release_rate:.0f} W')
"
```

### Advanced Verification

#### Run Test Suite
```bash
python -m pytest tests/ -v
```

#### Run Integration Test
```bash
python integration_test.py
```

#### Check Code Quality
```bash
flake8 src/ gui/ --max-line-length=88
```

### Performance Verification

#### Memory Usage Test
```bash
python -c "
import psutil, os
from src.combustion import CombustionCalculator

process = psutil.Process(os.getpid())
initial_memory = process.memory_info().rss / 1024 / 1024

calc = CombustionCalculator()
for i in range(100):
    calc.calculate_combustion_products('natural_gas', 0.01, 1.2)

final_memory = process.memory_info().rss / 1024 / 1024
print(f'Memory usage: {initial_memory:.1f} MB -> {final_memory:.1f} MB')
"
```

## Troubleshooting

### Common Issues

#### Issue 1: Python Not Found
**Error**: `'python' is not recognized as an internal or external command`

**Solutions**:
1. **Windows**: Add Python to PATH during installation
2. **Try alternative**: Use `python3` instead of `python`
3. **Reinstall Python** with PATH option enabled

#### Issue 2: Permission Denied
**Error**: `Permission denied` when installing packages

**Solutions**:
1. **Use virtual environment** (recommended)
2. **Install with user flag**: `pip install --user -r requirements.txt`
3. **Run as administrator** (Windows) or use `sudo` (Linux/macOS)

#### Issue 3: tkinter Not Available
**Error**: `ModuleNotFoundError: No module named 'tkinter'`

**Solutions**:
1. **Linux**: `sudo apt install python3-tk`
2. **macOS**: Reinstall Python with tkinter support
3. **Windows**: Reinstall Python with "tcl/tk and IDLE" option

#### Issue 4: Module Import Errors
**Error**: `ModuleNotFoundError: No module named 'src'`

**Solutions**:
1. **Run from correct directory**: Ensure you're in the project root
2. **Check PYTHONPATH**: Add project directory to Python path
3. **Use absolute imports**: Modify import statements if necessary

#### Issue 5: matplotlib Display Issues
**Error**: Charts not displaying or GUI freezing

**Solutions**:
1. **Linux**: Install GUI backend: `sudo apt install python3-tk`
2. **macOS**: Update to latest matplotlib version
3. **Set backend explicitly**: Add `matplotlib.use('TkAgg')` before imports

### Advanced Troubleshooting

#### Debug Mode
Enable debug logging:
```bash
python main.py --debug
```

#### Verbose Output
Run with verbose output:
```bash
python main.py --verbose
```

#### Clean Installation
If issues persist:
1. Remove virtual environment
2. Clear pip cache: `pip cache purge`
3. Reinstall from scratch

#### Check System Compatibility
```bash
python -c "
import sys, platform
print(f'Python: {sys.version}')
print(f'Platform: {platform.platform()}')
print(f'Architecture: {platform.architecture()}')
"
```

### Getting Help

#### Documentation
- Check the [User Guide](user_guide.md)
- Review [API Reference](api_reference.md)
- See [Examples](examples.md)

#### Community Support
- GitHub Issues: Report bugs and request features
- Discussions: Ask questions and share experiences

#### Professional Support
For professional installations or custom modifications, contact the development team.

## Advanced Installation

### Development Environment Setup

#### 1. Clone with Development Tools
```bash
git clone https://github.com/username/burner-dimension.git
cd burner-dimension
git checkout develop
```

#### 2. Install Pre-commit Hooks
```bash
pip install pre-commit
pre-commit install
```

#### 3. Setup IDE Integration
Configure your IDE for:
- Python path recognition
- Linting with flake8
- Code formatting with black
- Type checking with mypy

### Production Deployment

#### Web Server Deployment
```bash
# Install additional dependencies
pip install gunicorn flask

# Run web interface
gunicorn --bind 0.0.0.0:8000 web_app:app
```

#### Containerized Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8080

CMD ["python", "main.py", "--web"]
```

### Custom Installation

#### Minimal Installation
For computational core only:
```bash
pip install numpy pandas
# Copy only src/ directory
python -c "from src.combustion import CombustionCalculator"
```

#### Scientific Installation
For research and development:
```bash
pip install numpy pandas matplotlib scipy sympy jupyter
# Full scientific stack
```

---

*For installation issues not covered in this guide, please check the troubleshooting section or contact support.*