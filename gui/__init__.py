# gui/__init__.py

"""
gui package

GUI module for the burner calculator application.
Contains tkinter-based user interface components.
"""

import tkinter as tk
from tkinter import messagebox

from .gui import BurnerCalculatorGUI

__all__ = ["BurnerCalculatorGUI", "tk", "messagebox"]
