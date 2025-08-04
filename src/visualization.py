# src/visualization.py

"""
src/visualization.py

Visualization module for gas burner and combustion chamber calculations.
Generates charts and graphs for combustion analysis, pressure loss visualization,
and temperature distribution plots.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from typing import Dict, List, Optional, Tuple
import os
from datetime import datetime


class BurnerVisualization:
    """
    Handles all visualization tasks for burner calculations.
    
    This class provides methods to generate various charts and diagrams
    including combustion analysis plots, pressure loss graphs, temperature
    distributions, and burner geometry visualizations.
    
    Attributes:
        figure_size (tuple): Default figure size for plots
        dpi (int): Resolution for saved figures
        output_dir (str): Directory for saving visualizations
    """
    
    def __init__(self, output_dir: str = "output", figure_size: Tuple[int, int] = (10, 8), dpi: int = 300):
        """
        Initialize visualization manager.
        
        Args:
            output_dir: Directory path for saving visualization files
            figure_size: Default size for matplotlib figures (width, height)
            dpi: Resolution for saved images
        """
        self.output_dir = output_dir
        self.figure_size = figure_size
        self.dpi = dpi
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Set matplotlib style
        plt.style.use('default')
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.alpha'] = 0.3

    def plot_combustion_analysis(self, 
                                combustion_data: Dict,
                                save_formats: List[str] = ['png']) -> Dict[str, str]:
        """
        Create combustion analysis visualization.
        
        Generates a comprehensive plot showing air-fuel ratio, combustion products,
        and temperature distribution.
        
        Args:
            combustion_data: Dictionary containing combustion calculation results
            save_formats: List of formats to save ('png', 'pdf', 'jpeg')
            
        Returns:
            Dictionary with paths to saved files for each format
        """
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=self.figure_size)
            fig.suptitle('Analýza spalování', fontsize=16, fontweight='bold')
            
            # Plot 1: Air-fuel ratio
            if 'air_fuel_ratio' in combustion_data and 'excess_air' in combustion_data:
                ax1.bar(['Teoretický', 'Skutečný'], 
                       [combustion_data.get('stoichiometric_air', 0),
                        combustion_data.get('actual_air', 0)],
                       color=['lightblue', 'darkblue'])
                ax1.set_title('Poměr vzduch-palivo')
                ax1.set_ylabel('m³/m³')
                ax1.grid(True, alpha=0.3)
            
            # Plot 2: Combustion products composition
            if 'products' in combustion_data:
                products = combustion_data['products']
                components = list(products.keys())
                values = list(products.values())
                
                ax2.pie(values, labels=components, autopct='%1.1f%%', startangle=90)
                ax2.set_title('Složení spalin')
            
            # Plot 3: Temperature profile
            if 'temperature_profile' in combustion_data:
                temps = combustion_data['temperature_profile']
                positions = np.linspace(0, 100, len(temps))
                ax3.plot(positions, temps, 'r-', linewidth=2, marker='o')
                ax3.set_title('Teplotní profil')
                ax3.set_xlabel('Pozice [%]')
                ax3.set_ylabel('Teplota [°C]')
                ax3.grid(True, alpha=0.3)
            
            # Plot 4: Heat release rate
            if 'heat_release' in combustion_data:
                heat_data = combustion_data['heat_release']
                ax4.bar(range(len(heat_data)), heat_data, color='orange')
                ax4.set_title('Rychlost uvolňování tepla')
                ax4.set_xlabel('Zóna')
                ax4.set_ylabel('kW/m³')
                ax4.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Save in requested formats
            saved_files = {}
            base_filename = f"combustion_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            for fmt in save_formats:
                filename = f"{base_filename}.{fmt}"
                filepath = os.path.join(self.output_dir, filename)
                plt.savefig(filepath, format=fmt, dpi=self.dpi, bbox_inches='tight')
                saved_files[fmt] = filepath
            
            plt.close()
            return saved_files
            
        except Exception as e:
            print(f"Chyba při vytváření grafu spalování: {e}")
            return {}

    def plot_pressure_losses(self, 
                           pressure_data: Dict,
                           save_formats: List[str] = ['png']) -> Dict[str, str]:
        """
        Visualize pressure losses throughout the burner system.
        
        Creates a detailed plot showing pressure drops across different
        components of the burner and combustion chamber.
        
        Args:
            pressure_data: Dictionary containing pressure loss calculations
            save_formats: List of formats to save the plot
            
        Returns:
            Dictionary with paths to saved files
        """
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.figure_size)
            fig.suptitle('Analýza tlakových ztrát', fontsize=16, fontweight='bold')
            
            # Plot 1: Pressure losses by component
            if 'components' in pressure_data:
                components = list(pressure_data['components'].keys())
                losses = list(pressure_data['components'].values())
                
                bars = ax1.bar(components, losses, color=['red', 'orange', 'yellow', 'green'])
                ax1.set_title('Tlakové ztráty podle komponent')
                ax1.set_ylabel('Tlak [Pa]')
                ax1.tick_params(axis='x', rotation=45)
                
                # Add value labels on bars
                for bar, loss in zip(bars, losses):
                    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01*max(losses),
                            f'{loss:.1f}', ha='center', va='bottom')
            
            # Plot 2: Cumulative pressure drop
            if 'cumulative' in pressure_data:
                positions = pressure_data['positions']
                cumulative = pressure_data['cumulative']
                
                ax2.plot(positions, cumulative, 'b-', linewidth=2, marker='s')
                ax2.fill_between(positions, cumulative, alpha=0.3)
                ax2.set_title('Kumulativní tlaková ztráta')
                ax2.set_xlabel('Pozice v systému')
                ax2.set_ylabel('Kumulativní ztráta [Pa]')
                ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Save files
            saved_files = {}
            base_filename = f"pressure_losses_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            for fmt in save_formats:
                filename = f"{base_filename}.{fmt}"
                filepath = os.path.join(self.output_dir, filename)
                plt.savefig(filepath, format=fmt, dpi=self.dpi, bbox_inches='tight')
                saved_files[fmt] = filepath
            
            plt.close()
            return saved_files
            
        except Exception as e:
            print(f"Chyba při vytváření grafu tlakových ztrát: {e}")
            return {}

    def plot_temperature_distribution(self, 
                                    temperature_data: Dict,
                                    save_formats: List[str] = ['png']) -> Dict[str, str]:
        """
        Create temperature distribution visualization.
        
        Generates 2D heat map and temperature contours for the combustion chamber.
        
        Args:
            temperature_data: Dictionary containing temperature field data
            save_formats: List of output formats
            
        Returns:
            Dictionary with saved file paths
        """
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
            fig.suptitle('Rozložení teploty ve spalovací komoře', fontsize=16, fontweight='bold')
            
            if 'temperature_field' in temperature_data:
                temp_field = np.array(temperature_data['temperature_field'])
                
                # Plot 1: Heat map
                im1 = ax1.imshow(temp_field, cmap='hot', interpolation='bilinear')
                ax1.set_title('Teplotní mapa')
                ax1.set_xlabel('Šířka komory')
                ax1.set_ylabel('Výška komory')
                cbar1 = plt.colorbar(im1, ax=ax1)
                cbar1.set_label('Teplota [°C]')
                
                # Plot 2: Contour lines
                x = np.linspace(0, temp_field.shape[1], temp_field.shape[1])
                y = np.linspace(0, temp_field.shape[0], temp_field.shape[0])
                X, Y = np.meshgrid(x, y)
                
                contours = ax2.contour(X, Y, temp_field, levels=10, colors='black', alpha=0.6)
                ax2.clabel(contours, inline=True, fontsize=8)
                im2 = ax2.contourf(X, Y, temp_field, levels=20, cmap='hot', alpha=0.8)
                ax2.set_title('Izotermy')
                ax2.set_xlabel('Šířka komory')
                ax2.set_ylabel('Výška komory')
                cbar2 = plt.colorbar(im2, ax=ax2)
                cbar2.set_label('Teplota [°C]')
            
            plt.tight_layout()
            
            # Save files
            saved_files = {}
            base_filename = f"temperature_distribution_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            for fmt in save_formats:
                filename = f"{base_filename}.{fmt}"
                filepath = os.path.join(self.output_dir, filename)
                plt.savefig(filepath, format=fmt, dpi=self.dpi, bbox_inches='tight')
                saved_files[fmt] = filepath
            
            plt.close()
            return saved_files
            
        except Exception as e:
            print(f"Chyba při vytváření grafu rozložení teploty: {e}")
            return {}

    def plot_burner_geometry(self, 
                           geometry_data: Dict,
                           save_formats: List[str] = ['png']) -> Dict[str, str]:
        """
        Visualize burner and chamber geometry.
        
        Creates technical drawing showing burner dimensions, chamber layout,
        and key geometric parameters.
        
        Args:
            geometry_data: Dictionary containing geometric parameters
            save_formats: List of output formats
            
        Returns:
            Dictionary with saved file paths
        """
        try:
            fig, ax = plt.subplots(1, 1, figsize=self.figure_size)
            ax.set_aspect('equal')
            ax.set_title('Geometrie hořáku a spalovací komory', fontsize=16, fontweight='bold')
            
            # Draw combustion chamber
            if 'chamber' in geometry_data:
                chamber = geometry_data['chamber']
                chamber_rect = patches.Rectangle(
                    (0, 0), chamber.get('length', 1), chamber.get('height', 1),
                    linewidth=2, edgecolor='black', facecolor='lightgray', alpha=0.3
                )
                ax.add_patch(chamber_rect)
                
                # Add chamber dimensions
                ax.text(chamber.get('length', 1)/2, -0.1, 
                       f"Délka: {chamber.get('length', 0):.2f} m", 
                       ha='center', va='top')
                ax.text(-0.1, chamber.get('height', 1)/2, 
                       f"Výška: {chamber.get('height', 0):.2f} m", 
                       ha='right', va='center', rotation=90)
            
            # Draw burner
            if 'burner' in geometry_data:
                burner = geometry_data['burner']
                burner_width = burner.get('width', 0.1)
                burner_height = burner.get('height', 0.05)
                
                burner_rect = patches.Rectangle(
                    (-burner_width, chamber.get('height', 1)/2 - burner_height/2),
                    burner_width, burner_height,
                    linewidth=2, edgecolor='red', facecolor='orange'
                )
                ax.add_patch(burner_rect)
                
                # Add burner label
                ax.text(-burner_width/2, chamber.get('height', 1)/2,
                       'HOŘÁK', ha='center', va='center', fontweight='bold')
            
            # Add flow direction arrows
            arrow_props = dict(arrowstyle='->', lw=2, color='blue')
            ax.annotate('', xy=(0.3, chamber.get('height', 1)/2), 
                       xytext=(0, chamber.get('height', 1)/2), arrowprops=arrow_props)
            ax.text(0.15, chamber.get('height', 1)/2 + 0.05, 'Směr toku', 
                   ha='center', color='blue', fontweight='bold')
            
            # Set axis limits and labels
            ax.set_xlim(-0.3, chamber.get('length', 1) + 0.1)
            ax.set_ylim(-0.2, chamber.get('height', 1) + 0.1)
            ax.set_xlabel('Délka [m]')
            ax.set_ylabel('Výška [m]')
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Save files
            saved_files = {}
            base_filename = f"burner_geometry_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            for fmt in save_formats:
                filename = f"{base_filename}.{fmt}"
                filepath = os.path.join(self.output_dir, filename)
                plt.savefig(filepath, format=fmt, dpi=self.dpi, bbox_inches='tight')
                saved_files[fmt] = filepath
            
            plt.close()
            return saved_files
            
        except Exception as e:
            print(f"Chyba při vytváření geometrického nákresu: {e}")
            return {}

    def create_summary_dashboard(self, 
                               all_data: Dict,
                               save_formats: List[str] = ['png']) -> Dict[str, str]:
        """
        Create comprehensive dashboard with all key visualizations.
        
        Combines multiple charts into a single summary dashboard showing
        all important aspects of the burner calculation.
        
        Args:
            all_data: Dictionary containing all calculation results
            save_formats: List of output formats
            
        Returns:
            Dictionary with saved file paths
        """
        try:
            fig = plt.figure(figsize=(16, 12))
            fig.suptitle('Přehled výpočtu hořáku a spalovací komory', 
                        fontsize=20, fontweight='bold')
            
            # Create subplot grid
            gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
            
            # Plot 1: Key parameters summary (top left)
            ax1 = fig.add_subplot(gs[0, 0])
            if 'summary' in all_data:
                params = list(all_data['summary'].keys())[:5]  # Top 5 parameters
                values = [all_data['summary'][p] for p in params]
                ax1.barh(params, values, color='skyblue')
                ax1.set_title('Klíčové parametry')
            
            # Plot 2: Combustion efficiency (top middle)
            ax2 = fig.add_subplot(gs[0, 1])
            if 'efficiency' in all_data:
                efficiency = all_data['efficiency']
                wedges, texts, autotexts = ax2.pie(
                    [efficiency, 100-efficiency], 
                    labels=['Využité', 'Ztráty'],
                    autopct='%1.1f%%',
                    colors=['green', 'red']
                )
                ax2.set_title('Účinnost spalování')
            
            # Plot 3: Temperature profile (top right)
            ax3 = fig.add_subplot(gs[0, 2])
            if 'temperature_profile' in all_data:
                temps = all_data['temperature_profile']
                positions = np.linspace(0, 100, len(temps))
                ax3.plot(positions, temps, 'r-', linewidth=2)
                ax3.set_title('Teplotní profil')
                ax3.set_xlabel('Pozice [%]')
                ax3.set_ylabel('T [°C]')
            
            # Plot 4: Pressure losses (middle left)
            ax4 = fig.add_subplot(gs[1, 0])
            if 'pressure_losses' in all_data:
                components = list(all_data['pressure_losses'].keys())
                losses = list(all_data['pressure_losses'].values())
                ax4.bar(components, losses, color='orange')
                ax4.set_title('Tlakové ztráty')
                ax4.tick_params(axis='x', rotation=45)
            
            # Plot 5: Heat transfer (middle center)
            ax5 = fig.add_subplot(gs[1, 1])
            if 'heat_transfer' in all_data:
                ht_data = all_data['heat_transfer']
                mechanisms = list(ht_data.keys())
                values = list(ht_data.values())
                ax5.pie(values, labels=mechanisms, autopct='%1.1f%%')
                ax5.set_title('Přenos tepla')
            
            # Plot 6: Flow pattern (middle right)
            ax6 = fig.add_subplot(gs[1, 2])
            if 'flow_pattern' in all_data:
                # Simple flow visualization
                x = np.linspace(0, 10, 20)
                y = np.linspace(0, 5, 10)
                X, Y = np.meshgrid(x, y)
                U = np.ones_like(X)
                V = 0.1 * np.sin(X)
                ax6.quiver(X, Y, U, V, alpha=0.7)
                ax6.set_title('Proudění')
                ax6.set_aspect('equal')
            
            # Plot 7: Emissions (bottom span)
            ax7 = fig.add_subplot(gs[2, :])
            if 'emissions' in all_data:
                emissions = all_data['emissions']
                pollutants = list(emissions.keys())
                concentrations = list(emissions.values())
                bars = ax7.bar(pollutants, concentrations, 
                              color=['brown', 'gray', 'purple', 'orange'])
                ax7.set_title('Emise')
                ax7.set_ylabel('Koncentrace [mg/m³]')
                
                # Add limit lines if available
                if 'emission_limits' in all_data:
                    limits = all_data['emission_limits']
                    for i, (pollutant, limit) in enumerate(limits.items()):
                        if pollutant in pollutants:
                            ax7.axhline(y=limit, color='red', linestyle='--', alpha=0.7)
            
            plt.tight_layout()
            
            # Save files
            saved_files = {}
            base_filename = f"dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            for fmt in save_formats:
                filename = f"{base_filename}.{fmt}"
                filepath = os.path.join(self.output_dir, filename)
                plt.savefig(filepath, format=fmt, dpi=self.dpi, bbox_inches='tight')
                saved_files[fmt] = filepath
            
            plt.close()
            return saved_files
            
        except Exception as e:
            print(f"Chyba při vytváření dashboard: {e}")
            return {}

    def export_all_visualizations(self, 
                                calculation_results: Dict,
                                save_formats: List[str] = ['png', 'pdf']) -> Dict[str, List[str]]:
        """
        Generate all available visualizations for complete calculation results.
        
        This is the main method that creates all relevant charts and diagrams
        for a complete burner calculation analysis.
        
        Args:
            calculation_results: Complete results from all calculation modules
            save_formats: List of formats to save all visualizations
            
        Returns:
            Dictionary with lists of file paths for each visualization type
        """
        all_saved_files = {}
        
        try:
            # Generate combustion analysis plots
            if 'combustion' in calculation_results:
                files = self.plot_combustion_analysis(
                    calculation_results['combustion'], save_formats
                )
                all_saved_files['combustion_analysis'] = list(files.values())
            
            # Generate pressure loss plots
            if 'pressure_losses' in calculation_results:
                files = self.plot_pressure_losses(
                    calculation_results['pressure_losses'], save_formats
                )
                all_saved_files['pressure_losses'] = list(files.values())
            
            # Generate temperature distribution plots
            if 'temperature' in calculation_results:
                files = self.plot_temperature_distribution(
                    calculation_results['temperature'], save_formats
                )
                all_saved_files['temperature_distribution'] = list(files.values())
            
            # Generate geometry visualization
            if 'geometry' in calculation_results:
                files = self.plot_burner_geometry(
                    calculation_results['geometry'], save_formats
                )
                all_saved_files['burner_geometry'] = list(files.values())
            
            # Generate summary dashboard
            files = self.create_summary_dashboard(calculation_results, save_formats)
            all_saved_files['summary_dashboard'] = list(files.values())
            
            print(f"Vytvořeno {len(all_saved_files)} typů vizualizací")
            return all_saved_files
            
        except Exception as e:
            print(f"Chyba při vytváření vizualizací: {e}")
            return all_saved_files