#!/usr/bin/env python3
# launch_gui.py

"""
launch_gui.py

Simple launcher script for the burner calculator GUI application.
This script can be used to launch the GUI with proper error handling.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

def check_dependencies():
    """Check if all required dependencies are available."""
    missing_deps = []
    
    try:
        import pandas
    except ImportError:
        missing_deps.append("pandas")
    
    try:
        import numpy
    except ImportError:
        missing_deps.append("numpy")
    
    return missing_deps

def main():
    """Launch the GUI application with dependency checking."""
    print("Spouštím GUI aplikaci pro návrh plynového hořáku...")
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"Varování: Chybí následující závislosti: {', '.join(missing)}")
        print("Některé funkce nemusí fungovat správně.")
        print("Instalujte je pomocí: pip install " + " ".join(missing))
    
    try:
        # Add src directory to path
        current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
        src_path = os.path.join(current_dir, 'src')
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        
        # Import GUI module
        from gui.gui import BurnerCalculatorGUI
        
        # Create root window
        root = tk.Tk()
        
        # Set up error handling for GUI
        def handle_error(exc_type, exc_value, exc_traceback):
            """Handle uncaught exceptions in GUI."""
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            
            error_msg = f"Neočekávaná chyba: {exc_type.__name__}: {exc_value}"
            messagebox.showerror("Chyba aplikace", error_msg)
            print(error_msg)
        
        sys.excepthook = handle_error
        
        # Initialize and run application  
        app = BurnerCalculatorGUI(root)
        
        print("GUI aplikace spuštěna úspěšně!")
        print("Pro uzavření aplikace zavřete hlavní okno.")
        
        # Start main loop
        root.mainloop()
        
    except ImportError as e:
        print(f"Chyba při importu modulů: {e}")
        print("Zkontrolujte, zda jsou všechny soubory na svém místě.")
        sys.exit(1)
        
    except Exception as e:
        print(f"Neočekávaná chyba při spuštění: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("Aplikace ukončena.")

if __name__ == "__main__":
    main()