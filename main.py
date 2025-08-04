# main.py

"""
main.py

Main entry point for the Gas Burner and Combustion Chamber Design Application.
This application provides GUI-based calculations for gas burner dimensioning,
combustion chamber design, radiation heat transfer, and pressure loss calculations.
"""

import sys
import os
import tkinter as tk

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gui.gui import BurnerCalculatorGUI


def main():
    """
    Main entry point for the application.
    
    Initializes and runs the GUI application for burner calculations.
    """
    try:
        # Create root window
        root = tk.Tk()
        
        # Initialize application
        app = BurnerCalculatorGUI(root)
        
        # Start main loop
        root.mainloop()
        
    except Exception as e:
        print(f"Chyba při spuštění aplikace: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()