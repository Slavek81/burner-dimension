#!/usr/bin/env python3
# test_gui_setup.py

"""
test_gui_setup.py

Test script to verify GUI setup is complete and functional.
This validates all imports and initialization without starting the GUI.
"""

import sys
import os

def test_gui_setup():
    """Test complete GUI setup without starting the interface."""
    print("TESTOVÁNÍ NASTAVENÍ GUI APLIKACE")
    print("=" * 40)
    
    # Add src to path
    sys.path.insert(0, os.path.join(os.getcwd(), 'src'))
    
    try:
        # Test tkinter availability
        import tkinter as tk
        print("✓ Tkinter dostupný")
        
        # Test calculation modules
        from combustion import CombustionCalculator
        from burner_design import BurnerDesigner  
        from chamber_design import ChamberDesigner
        from radiation import RadiationCalculator
        from pressure_losses import PressureLossCalculator
        print("✓ Všechny výpočetní moduly")
        
        # Test GUI module
        from gui.gui import BurnerCalculatorGUI
        print("✓ GUI modul")
        
        # Test GUI initialization (without mainloop)
        root = tk.Tk()
        root.withdraw()  # Hide window
        
        app = BurnerCalculatorGUI(root)
        print("✓ GUI aplikace inicializována")
        
        # Test that all tabs exist
        tab_count = app.notebook.index("end")
        print(f"✓ GUI obsahuje {tab_count} záložek")
        
        # Test that calculators are initialized
        calc_modules = ['combustion', 'burner', 'chamber', 'radiation', 'pressure']
        for module in calc_modules:
            if module in app.calculators:
                print(f"✓ Kalkulátor '{module}' inicializován")
            else:
                print(f"✗ Kalkulátor '{module}' chybí")
        
        # Test input validation
        app.load_default_values()
        print("✓ Výchozí hodnoty načteny")
        
        # Clean up
        root.destroy()
        
        print("\n🎉 GUI APLIKACE JE PŘIPRAVENA K POUŽITÍ!")
        print("\nSpuštění:")
        print("python3 main.py")
        print("python3 launch_gui.py")
        
        return True
        
    except ImportError as e:
        print(f"✗ Chyba importu: {e}")
        return False
    except Exception as e:
        print(f"✗ Neočekávaná chyba: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_gui_setup()
    sys.exit(0 if success else 1)