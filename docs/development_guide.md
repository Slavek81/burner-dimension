# Development Guide

## Table of Contents
1. [Development Environment Setup](#development-environment-setup)
2. [Project Structure](#project-structure)
3. [Coding Standards](#coding-standards)
4. [Development Workflow](#development-workflow)
5. [Testing Guidelines](#testing-guidelines)
6. [Documentation Standards](#documentation-standards)
7. [Contributing Guidelines](#contributing-guidelines)
8. [Release Process](#release-process)

## Development Environment Setup

### Prerequisites

#### Required Software
- **Python 3.8+**: Primary development language
- **Git**: Version control system
- **IDE/Editor**: VS Code, PyCharm, or similar with Python support
- **pip**: Python package manager (included with Python)

#### Recommended Tools
- **conda/mamba**: Environment management
- **Docker**: Containerization (optional)
- **Make**: Build automation
- **GitHub CLI**: For repository management

### Environment Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/username/burner-dimension.git
cd burner-dimension
```

#### 2. Create Development Environment
```bash
# Using venv (built-in)
python -m venv dev_env
source dev_env/bin/activate  # Linux/macOS
# dev_env\Scripts\activate   # Windows

# Or using conda
conda create -n burner_dev python=3.9
conda activate burner_dev
```

#### 3. Install Dependencies
```bash
# Core dependencies
pip install -r requirements.txt

# Development dependencies
pip install -r requirements-dev.txt

# Or install everything at once
make install
```

#### 4. Setup Pre-commit Hooks
```bash
pre-commit install
```

#### 5. Verify Setup
```bash
# Run tests
python -m pytest tests/

# Check code quality
make lint

# Run integration test
python integration_test.py
```

### IDE Configuration

#### VS Code Settings
Create `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "./dev_env/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": ["--max-line-length=88"],
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests/"],
    "editor.formatOnSave": true,
    "editor.rulers": [88],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        ".pytest_cache": true,
        "*.egg-info": true
    }
}
```

#### PyCharm Configuration
1. Set Python interpreter to your virtual environment
2. Enable flake8 linting: Settings → Tools → External Tools
3. Configure black formatter: Settings → Tools → External Tools
4. Set up pytest: Settings → Tools → Python Integrated Tools

## Project Structure

### Directory Layout
```
burner_calc/
├── src/                    # Core calculation modules
│   ├── __init__.py
│   ├── combustion.py       # Combustion calculations
│   ├── burner_design.py    # Burner sizing
│   ├── chamber_design.py   # Chamber design
│   ├── radiation.py        # Heat transfer
│   ├── pressure_losses.py  # Pressure calculations
│   ├── visualization.py    # Charts and plots
│   └── report.py          # Report generation
├── gui/                   # User interface
│   ├── __init__.py
│   └── gui.py            # Main GUI application
├── data/                 # Configuration and data files
│   └── fuels.json       # Fuel properties database
├── tests/               # Test suite
│   ├── __init__.py
│   ├── test_combustion.py
│   ├── test_burner_design.py
│   ├── test_chamber_design.py
│   ├── test_radiation.py
│   ├── test_pressure_losses.py
│   ├── test_visualization.py
│   ├── test_report.py
│   └── test_gui.py
├── docs/                # Documentation
│   ├── README.md
│   ├── user_guide.md
│   ├── installation.md
│   ├── examples.md
│   ├── calculation_methods.md
│   ├── architecture.md
│   ├── api_reference.md
│   ├── development_guide.md
│   ├── testing.md
│   └── deployment.md
├── output/              # Generated reports and charts
├── input/               # Sample input files
├── main.py             # Main application entry point
├── launch_gui.py       # GUI launcher
├── integration_test.py # Integration testing
├── requirements.txt    # Core dependencies
├── requirements-dev.txt # Development dependencies
├── Makefile           # Build automation
├── .pre-commit-config.yaml # Pre-commit configuration
├── .gitignore         # Git ignore patterns
├── setup.py           # Package setup (if needed)
├── CLAUDE.md          # Project documentation
├── PRD.md             # Product requirements
└── README.md          # Project overview
```

### Module Responsibilities

#### Core Modules (`src/`)
- **combustion.py**: Stoichiometric calculations, flame analysis
- **burner_design.py**: Burner sizing, pressure requirements
- **chamber_design.py**: Chamber volume, heat transfer, efficiency
- **radiation.py**: Radiative heat transfer, emissivity calculations
- **pressure_losses.py**: Hydraulic calculations, system pressure analysis
- **visualization.py**: Chart generation, technical drawings
- **report.py**: Multi-format report generation

#### Support Modules
- **gui/gui.py**: User interface, event handling
- **data/**: Configuration files, fuel properties
- **tests/**: Comprehensive test suite
- **docs/**: Technical documentation

## Coding Standards

### Python Style Guide

#### PEP 8 Compliance
- **Line length**: Maximum 88 characters (Black formatter standard)
- **Indentation**: 4 spaces (no tabs)
- **Naming conventions**:
  - Variables and functions: `snake_case`
  - Classes: `CamelCase`
  - Constants: `UPPER_SNAKE_CASE`
  - Private methods/attributes: `_leading_underscore`

#### Type Hints
Use type hints for all function parameters and return values:
```python
from typing import Dict, List, Optional, Tuple

def calculate_combustion(
    fuel_type: str,
    fuel_flow: float,
    excess_air: float = 1.2
) -> CombustionResults:
    """Calculate combustion products and properties."""
    pass
```

#### Documentation Standards
Every class, method, and function must have comprehensive docstrings:

```python
class CombustionCalculator:
    """
    Calculator for combustion processes in gas burners.
    
    This class handles stoichiometric calculations, flame temperature
    calculations, and determination of combustion products composition
    for various gas fuels.
    
    Attributes:
        fuel_data (dict): Fuel properties loaded from JSON file
        constants (dict): Physical constants
        
    Example:
        >>> calc = CombustionCalculator()
        >>> result = calc.calculate_combustion_products('natural_gas', 0.01, 1.2)
        >>> print(f"Flame temp: {result.adiabatic_flame_temperature:.0f} K")
    """
    
    def calculate_combustion_products(
        self, 
        fuel_type: str, 
        fuel_flow_rate: float, 
        excess_air_ratio: float = 1.2
    ) -> CombustionResults:
        """
        Calculate complete combustion products and properties.
        
        Performs stoichiometric analysis and determines flame temperature,
        combustion products composition, and heat release rate.
        
        Args:
            fuel_type: Type of fuel ('natural_gas', 'methane', 'propane')
            fuel_flow_rate: Fuel mass flow rate [kg/s]
            excess_air_ratio: Excess air ratio (≥1.0)
            
        Returns:
            Complete combustion calculation results including:
            - Fuel, air, and flue gas flow rates
            - Adiabatic flame temperature
            - Heat release rate
            - Flue gas composition (CO2, O2 percentages)
            
        Raises:
            ValueError: If fuel_type is not supported or parameters are invalid
            
        Example:
            >>> calc = CombustionCalculator()
            >>> result = calc.calculate_combustion_products('natural_gas', 0.01, 1.2)
            >>> print(f"Heat release: {result.heat_release_rate/1000:.1f} kW")
        """
        pass
```

### Code Quality Tools

#### Automated Formatting
```bash
# Format code with Black
black src/ gui/ tests/

# Sort imports with isort
isort src/ gui/ tests/
```

#### Linting
```bash
# Check with flake8
flake8 src/ gui/ tests/ --max-line-length=88

# Security check with bandit
bandit -r src/ gui/
```

#### Type Checking
```bash
# Static type checking with mypy
mypy src/ gui/
```

### Data Classes and Structures

Use dataclasses for structured data:
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class CombustionResults:
    """Results from combustion calculations."""
    
    fuel_flow_rate: float              # [kg/s]
    air_flow_rate: float               # [kg/s]
    flue_gas_flow_rate: float          # [kg/s]
    adiabatic_flame_temperature: float # [K]
    heat_release_rate: float           # [W]
    excess_air_ratio: float            # [-]
    co2_volume_percent: float          # [%]
    o2_volume_percent: float           # [%]
    
    def __post_init__(self):
        """Validate data after initialization."""
        if self.fuel_flow_rate <= 0:
            raise ValueError("Fuel flow rate must be positive")
        if self.excess_air_ratio < 1.0:
            raise ValueError("Excess air ratio must be ≥ 1.0")
```

### Error Handling Patterns

#### Custom Exceptions
```python
class BurnerCalculationError(Exception):
    """Base exception for burner calculation errors."""
    pass

class InvalidFuelTypeError(BurnerCalculationError):
    """Raised when an unsupported fuel type is specified."""
    pass

class CalculationConvergenceError(BurnerCalculationError):
    """Raised when iterative calculations fail to converge."""
    pass
```

#### Validation Patterns
```python
def validate_inputs(self, **kwargs) -> None:
    """Validate input parameters."""
    errors = []
    
    if 'power' in kwargs and kwargs['power'] <= 0:
        errors.append("Power must be greater than zero")
    
    if 'pressure' in kwargs and kwargs['pressure'] <= 0:
        errors.append("Pressure must be greater than zero")
    
    if errors:
        raise ValueError("; ".join(errors))
```

## Development Workflow

### Git Workflow

#### Branch Strategy
- **main**: Production-ready code
- **develop**: Integration branch for features
- **feature/**: Feature development branches
- **hotfix/**: Critical bug fixes
- **release/**: Release preparation

#### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
```bash
git commit -m "feat(combustion): add biogas fuel support"
git commit -m "fix(gui): handle empty input validation"
git commit -m "docs(api): update calculation methods documentation"
```

#### Development Cycle
1. **Create feature branch**:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/new-calculation-method
   ```

2. **Develop and commit**:
   ```bash
   # Make changes
   git add .
   git commit -m "feat(calculation): implement new method"
   ```

3. **Test and validate**:
   ```bash
   make test
   make lint
   make security-check
   ```

4. **Push and create PR**:
   ```bash
   git push origin feature/new-calculation-method
   # Create pull request through GitHub
   ```

### Code Review Process

#### Review Checklist
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Type hints are present
- [ ] Error handling is appropriate
- [ ] Performance implications considered
- [ ] Security vulnerabilities checked

#### Review Guidelines
1. **Functionality**: Does the code work as intended?
2. **Design**: Is the code well-structured and maintainable?
3. **Tests**: Are there adequate tests for new functionality?
4. **Documentation**: Is the code self-documenting with good docstrings?
5. **Performance**: Are there any performance concerns?
6. **Security**: Are there potential security vulnerabilities?

### Automated Quality Checks

#### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
        language_version: python3.9

  - repo: https://github.com/pycqa/isort
    rev: 5.10.1  
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
        args: [--max-line-length=88]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.4
    hooks:
      - id: bandit
        args: ["-r", "src/", "gui/"]
```

#### CI/CD Pipeline
```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10"]
        
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
        
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
        
    - name: Lint with flake8
      run: flake8 src/ gui/ tests/
      
    - name: Security check with bandit
      run: bandit -r src/ gui/
      
    - name: Test with pytest
      run: pytest tests/ --cov=src --cov-report=xml
      
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## Testing Guidelines

### Test Organization

#### Test Structure
```
tests/
├── unit/              # Unit tests for individual modules
│   ├── test_combustion.py
│   ├── test_burner_design.py
│   └── ...
├── integration/       # Integration tests
│   ├── test_full_calculation.py
│   └── test_gui_workflow.py
├── fixtures/          # Test data and fixtures
│   ├── sample_inputs.json
│   └── expected_results.json
└── conftest.py       # Pytest configuration
```

#### Test Categories
1. **Unit Tests**: Test individual functions and methods
2. **Integration Tests**: Test module interactions
3. **System Tests**: Test complete workflows
4. **GUI Tests**: Test user interface functionality
5. **Performance Tests**: Test calculation speed and memory usage

### Writing Tests

#### Unit Test Example
```python
# tests/unit/test_combustion.py
import pytest
from src.combustion import CombustionCalculator, CombustionResults

class TestCombustionCalculator:
    """Test suite for CombustionCalculator class."""
    
    @pytest.fixture
    def calculator(self):
        """Create calculator instance for testing."""
        return CombustionCalculator()
    
    def test_calculate_stoichiometric_air_natural_gas(self, calculator):
        """Test stoichiometric air calculation for natural gas."""
        fuel_flow = 0.01  # kg/s
        air_flow = calculator.calculate_stoichiometric_air('natural_gas', fuel_flow)
        
        expected_air_flow = fuel_flow * 17.2  # Air-fuel ratio for natural gas
        assert abs(air_flow - expected_air_flow) < 1e-6
    
    def test_calculate_combustion_products_valid_inputs(self, calculator):
        """Test combustion products calculation with valid inputs."""
        result = calculator.calculate_combustion_products(
            'natural_gas', 0.01, 1.2
        )
        
        assert isinstance(result, CombustionResults)
        assert result.fuel_flow_rate == 0.01
        assert result.excess_air_ratio == 1.2
        assert result.adiabatic_flame_temperature > 1500  # Reasonable range
        assert result.heat_release_rate > 0
    
    def test_calculate_combustion_products_invalid_fuel(self, calculator):
        """Test error handling for invalid fuel type."""
        with pytest.raises(ValueError, match="Nepodporovaný typ paliva"):
            calculator.calculate_combustion_products('invalid_fuel', 0.01, 1.2)
    
    def test_calculate_combustion_products_negative_flow(self, calculator):
        """Test error handling for negative fuel flow."""
        with pytest.raises(ValueError, match="větší než nula"):
            calculator.calculate_combustion_products('natural_gas', -0.01, 1.2)
    
    @pytest.mark.parametrize("excess_air,expected_co2", [
        (1.0, 12.0),
        (1.2, 10.0),
        (1.5, 8.0),
    ])
    def test_co2_percentage_with_excess_air(self, calculator, excess_air, expected_co2):
        """Test CO2 percentage calculation with different excess air ratios."""
        result = calculator.calculate_combustion_products(
            'natural_gas', 0.01, excess_air
        )
        
        assert abs(result.co2_volume_percent - expected_co2) < 0.5
```

#### Integration Test Example
```python
# tests/integration/test_full_calculation.py
import pytest
from src.combustion import CombustionCalculator
from src.burner_design import BurnerDesigner
from src.chamber_design import ChamberDesigner

class TestFullCalculationWorkflow:
    """Test complete calculation workflow integration."""
    
    @pytest.fixture
    def calculators(self):
        """Create integrated calculator instances."""
        combustion_calc = CombustionCalculator()
        burner_designer = BurnerDesigner(combustion_calc)
        chamber_designer = ChamberDesigner(combustion_calc, burner_designer)
        
        return {
            'combustion': combustion_calc,
            'burner': burner_designer,  
            'chamber': chamber_designer
        }
    
    def test_complete_burner_design_workflow(self, calculators):
        """Test complete design workflow from inputs to results."""
        # Input parameters
        fuel_type = 'natural_gas'
        required_power = 100000  # 100 kW
        supply_pressure = 3000   # 3000 Pa
        
        # Combustion calculation
        fuel_flow = required_power / 50e6  # Approximate for natural gas
        combustion_results = calculators['combustion'].calculate_combustion_products(
            fuel_type, fuel_flow, 1.2
        )
        
        # Burner design
        burner_results = calculators['burner'].design_burner(
            fuel_type, required_power, supply_pressure
        )
        
        # Chamber design
        chamber_results = calculators['chamber'].design_chamber(
            fuel_type, required_power, 0.5
        )
        
        # Validate results consistency
        assert combustion_results.fuel_flow_rate > 0
        assert burner_results.burner_diameter > 0
        assert chamber_results.chamber_volume > 0
        
        # Check physical reasonableness
        assert 1200 < combustion_results.adiabatic_flame_temperature < 2500
        assert 0.01 < burner_results.burner_diameter < 0.5
        assert 0.1 < chamber_results.chamber_volume < 10.0
```

### Test Configuration

#### pytest Configuration
```python
# conftest.py
import pytest
import json
import os
from pathlib import Path

@pytest.fixture(scope="session")
def test_data_dir():
    """Path to test data directory."""
    return Path(__file__).parent / "fixtures"

@pytest.fixture(scope="session")
def sample_fuel_data(test_data_dir):
    """Load sample fuel data for testing."""
    with open(test_data_dir / "sample_fuels.json") as f:
        return json.load(f)

@pytest.fixture(scope="session")
def temp_output_dir(tmp_path_factory):
    """Create temporary directory for test outputs."""
    return tmp_path_factory.mktemp("test_output")

@pytest.fixture(autouse=True)
def cleanup_output_files(temp_output_dir):
    """Clean up output files after each test."""
    yield
    # Cleanup logic here
    for file in temp_output_dir.glob("*"):
        if file.is_file():
            file.unlink()
```

### Performance Testing

#### Benchmark Tests
```python
# tests/performance/test_benchmarks.py
import time
import pytest
from src.combustion import CombustionCalculator

class TestPerformanceBenchmarks:
    """Performance benchmarks for calculation modules."""
    
    def test_combustion_calculation_speed(self):
        """Benchmark combustion calculation performance."""
        calculator = CombustionCalculator()
        
        start_time = time.time()
        
        # Perform multiple calculations
        for i in range(1000):
            calculator.calculate_combustion_products('natural_gas', 0.01, 1.2)
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        # Should complete 1000 calculations in under 1 second
        assert elapsed < 1.0
        print(f"1000 calculations completed in {elapsed:.3f} seconds")
    
    @pytest.mark.slow
    def test_memory_usage(self):
        """Test memory usage during calculations."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        calculator = CombustionCalculator()
        
        # Perform calculations
        results = []
        for i in range(10000):
            result = calculator.calculate_combustion_products('natural_gas', 0.01, 1.2)
            results.append(result)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable
        assert memory_increase < 100  # Less than 100 MB increase
        print(f"Memory increase: {memory_increase:.1f} MB")
```

## Documentation Standards

### Documentation Types

#### Code Documentation
- **Docstrings**: All classes, methods, and functions
- **Type hints**: All parameters and return values
- **Comments**: Complex algorithms and business logic
- **README files**: Module-level explanations

#### User Documentation
- **User Guide**: How to use the application
- **Installation Guide**: Setup instructions
- **API Reference**: Programming interface
- **Examples**: Usage examples and tutorials

#### Developer Documentation
- **Architecture**: System design and patterns
- **Development Guide**: This document
- **Testing Guide**: Testing procedures
- **Deployment Guide**: Release and deployment

### Documentation Generation

#### Automated Documentation
```bash
# Generate API documentation with Sphinx
sphinx-apidoc -o docs/api src/
sphinx-build -b html docs/ docs/_build/html

# Generate coverage reports
pytest --cov=src --cov-report=html
```

#### Documentation Review
1. **Accuracy**: Information is correct and up-to-date
2. **Completeness**: All features and functions are documented
3. **Clarity**: Instructions are clear and easy to follow
4. **Examples**: Code examples work and are helpful
5. **Navigation**: Documents are well-organized and linked

## Contributing Guidelines

### Contribution Process

#### 1. Issue Creation
- Search existing issues first
- Use issue templates
- Provide detailed descriptions
- Add appropriate labels

#### 2. Development
- Fork the repository
- Create feature branch
- Follow coding standards
- Write tests for new features
- Update documentation

#### 3. Pull Request
- Use PR template
- Link to related issues
- Provide clear description
- Include screenshots for UI changes
- Request appropriate reviewers

### Contribution Types

#### Bug Fixes
- Include reproduction steps
- Add regression tests
- Update documentation if needed

#### New Features
- Discuss design in issues first
- Include comprehensive tests
- Update user documentation
- Add API documentation

#### Documentation
- Follow documentation standards
- Include examples where helpful
- Check for broken links
- Validate formatting

## Release Process

### Version Management

#### Semantic Versioning
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

Examples:
- `1.0.0` → `1.0.1` (bug fix)
- `1.0.1` → `1.1.0` (new feature)
- `1.1.0` → `2.0.0` (breaking change)

#### Release Branches
```bash
# Create release branch
git checkout develop
git checkout -b release/1.2.0

# Update version numbers
# Update CHANGELOG.md
# Final testing

# Merge to main
git checkout main
git merge release/1.2.0
git tag v1.2.0

# Merge back to develop
git checkout develop
git merge main
```

### Release Checklist

#### Pre-release
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated
- [ ] Version numbers are updated
- [ ] Security vulnerabilities addressed
- [ ] Performance regression tests pass

#### Release
- [ ] Create release branch
- [ ] Final testing and validation
- [ ] Create GitHub release
- [ ] Update package repositories
- [ ] Deploy to production environment
- [ ] Monitor for issues

#### Post-release
- [ ] Monitor error rates
- [ ] Update documentation site
- [ ] Announce to users
- [ ] Plan next release
- [ ] Address any critical issues

---

*This development guide provides comprehensive information for contributing to the Gas Burner Calculator project. Follow these guidelines to ensure high-quality, maintainable code.*