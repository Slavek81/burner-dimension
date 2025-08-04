# src/__init__.py

"""
Burner calculation modules package.

This package contains all calculation modules for gas burner design:
- combustion: Combustion calculations and stoichiometry
- burner_design: Burner dimensioning and design  
- chamber_design: Combustion chamber design and heat transfer
- radiation: Radiation heat transfer calculations
- pressure_losses: Pressure loss calculations for piping systems
"""

# Version info
__version__ = "1.0.0"
__author__ = "Burner Design Application"

# Import main classes for easy access
from .combustion import CombustionCalculator, CombustionResults
from .burner_design import BurnerDesigner, BurnerDesignResults
from .chamber_design import ChamberDesigner, ChamberDesignResults
from .radiation import RadiationCalculator, RadiationResults
from .pressure_losses import PressureLossCalculator, PressureLossResults, PipeSegment, Fitting

__all__ = [
    'CombustionCalculator',
    'CombustionResults', 
    'BurnerDesigner',
    'BurnerDesignResults',
    'ChamberDesigner', 
    'ChamberDesignResults',
    'RadiationCalculator',
    'RadiationResults',
    'PressureLossCalculator',
    'PressureLossResults',
    'PipeSegment',
    'Fitting'
]