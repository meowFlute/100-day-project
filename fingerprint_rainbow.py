#!/usr/bin/env python3
"""
Fingerprint Rainbow Optimizer and Visualizer
A GUI application to optimize and visualize fingerprint placement on rainbow bands
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Ellipse, Wedge
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional
import math


@dataclass
class PaperSize:
    """Represents a paper size with name and dimensions in inches"""
    name: str
    width: float  # inches
    height: float  # inches


# Standard paper sizes
PAPER_SIZES = {
    "Letter (US)": PaperSize("Letter (US)", 8.5, 11),
    "Legal (US)": PaperSize("Legal (US)", 8.5, 14),
    "Tabloid (US)": PaperSize("Tabloid (US)", 11, 17),
    "A4": PaperSize("A4", 8.27, 11.69),
    "A3": PaperSize("A3", 11.69, 16.54),
    "A2": PaperSize("A2", 16.54, 23.39),
    "A1": PaperSize("A1", 23.39, 33.11),
    "Custom": PaperSize("Custom", 8.5, 11)
}


class FingerprintRainbow:
    """Core logic for fingerprint rainbow calculation and rendering"""
    
    # Colors from outermost (largest) to innermost (smallest)
    COLORS = ['red', 'orange', 'gold', 'green', 'blue', 'indigo', 'violet']
    TOTAL_FINGERPRINTS = 100
    
    def __init__(self, fingerprint_width: float, fingerprint_height: float, 
                 band_spacing_percent: float = 100.0, min_inner_prints: int = 5):
        """
        Initialize with fingerprint dimensions
        
        Args:
            fingerprint_width: Width of fingerprint in inches (short axis)
            fingerprint_height: Height of fingerprint in inches (long axis)
            band_spacing_percent: Percentage of fingerprint height for band spacing (default 100%)
            min_inner_prints: Minimum number of fingerprints for innermost band (default 5)
        """
        self.fp_width = fingerprint_width
        self.fp_height = fingerprint_height
        self.band_spacing_percent = band_spacing_percent
        self.band_spacing = (band_spacing_percent / 100.0) * fingerprint_height
        self.min_inner_prints = min_inner_prints
        self.allocations = self._optimize_allocation()
        
    def _optimize_allocation(self) -> List[int]:
        """
        Optimize fingerprint allocation across bands.
        Each band is a half-circle, so larger radius = more fingerprints can fit.
        Red (outermost) should have the most, violet (innermost) should have the least.
        Fingerprints are placed tangent to their neighbors.
        Respects minimum fingerprint count for innermost band.
        """
        # Calculate how many fingerprints fit in each band based on arc length
        # Band 0 (red) is outermost with largest radius
        # Band 6 (violet) is innermost with smallest radius
        band_capacities = []
        
        # Start with the innermost band (violet) and work outward
        # Each band is separated by band_spacing
        for i in range(7):
            # Band index from innermost: violet=0, indigo=1, ..., red=6
            # But we need to iterate in the order we store (red=0, violet=6)
            # So band_idx in storage is (6-i)
            
            # Calculate radius for this band (measured to center of band)
            # Innermost band (violet, storage idx 6) starts at band_spacing/2
            # Each successive band is separated by band_spacing
            band_from_center = 6 - i  # violet=0, indigo=1, ..., red=6
            mid_radius = self.band_spacing / 2 + band_from_center * self.band_spacing
            
            # Arc length at this radius
            arc_length = math.pi * mid_radius
            
            # Number of fingerprints that fit tangent to each other
            # Each fingerprint takes up fp_height of arc length
            num_fits = arc_length / self.fp_height
            
            band_capacities.append(num_fits)
        
        # Normalize to 100 total fingerprints
        total_capacity = sum(band_capacities)
        allocations = [round(w / total_capacity * self.TOTAL_FINGERPRINTS) for w in band_capacities]
        
        # Ensure innermost band (violet, index 6) meets minimum requirement
        if allocations[6] < self.min_inner_prints:
            # Need to add fingerprints to innermost band
            deficit = self.min_inner_prints - allocations[6]
            allocations[6] = self.min_inner_prints
            
            # Remove from other bands proportionally (prioritize outer bands)
            remaining_total = self.TOTAL_FINGERPRINTS - self.min_inner_prints
            remaining_capacity = sum(band_capacities[:6])
            
            for i in range(6):
                if remaining_capacity > 0:
                    proportion = band_capacities[i] / remaining_capacity
                    allocations[i] = round(proportion * remaining_total)
        
        # Final adjustment to ensure exactly 100
        diff = self.TOTAL_FINGERPRINTS - sum(allocations)
        if diff != 0:
            # Add/subtract from the band with most capacity (but not innermost if we just set it)
            candidates = list(range(6)) if allocations[6] == self.min_inner_prints else list(range(7))
            if candidates:
                max_idx = max(candidates, key=lambda i: allocations[i])
                allocations[max_idx] += diff
        
        return allocations
    
    def calculate_dimensions(self) -> Tuple[float, float]:
        """
        Calculate the total width and height of the rainbow
        
        Returns:
            (width, height) in inches
        """
        # Total radius includes all 7 bands plus the outer half of the outermost band
        # Each band is centered at: band_spacing/2 + band_num * band_spacing
        # Outermost band (red, band 6 from center) is at: band_spacing/2 + 6 * band_spacing
        # Plus we need to add fp_width/2 for the outer edge
        outermost_center = self.band_spacing / 2 + 6 * self.band_spacing
        total_radius = outermost_center + self.fp_width / 2
        width = 2 * total_radius
        height = total_radius  # Half circle
        return width, height
    
    def render(self, ax: plt.Axes, paper_width: float, paper_height: float, 
               margin: float, orientation: str = "portrait"):
        """
        Render the rainbow visualization on a matplotlib axes
        
        Args:
            ax: Matplotlib axes to render on
            paper_width: Paper width in inches
            paper_height: Paper height in inches
            margin: Margin size in inches
            orientation: "portrait" or "landscape"
        """
        ax.clear()
        ax.set_aspect('equal')
        
        # Swap dimensions if landscape
        if orientation == "landscape":
            paper_width, paper_height = paper_height, paper_width
        
        # Set up the plot with margins
        ax.set_xlim(0, paper_width)
        ax.set_ylim(0, paper_height)
        
        # Draw margin lines (light gray)
        margin_rect = plt.Rectangle((margin, margin), 
                                    paper_width - 2*margin, 
                                    paper_height - 2*margin,
                                    fill=False, edgecolor='lightgray', 
                                    linestyle='--', linewidth=1)
        ax.add_patch(margin_rect)
        
        # Calculate rainbow dimensions
        rainbow_width, rainbow_height = self.calculate_dimensions()
        
        # Center the rainbow on the paper (horizontally) and position from bottom margin
        center_x = paper_width / 2
        center_y = margin
        
        # Draw each band - band 0 (red) is outermost, band 6 (violet) is innermost
        for band_idx, (color, num_prints) in enumerate(zip(self.COLORS, self.allocations)):
            # Calculate band position from center
            # band_idx: 0=red (outermost), 6=violet (innermost)
            # band_from_center: 6=red, 0=violet
            band_from_center = 6 - band_idx
            
            # Mid radius for this band
            mid_radius = self.band_spacing / 2 + band_from_center * self.band_spacing
            
            # Inner and outer radius for the band wedge
            inner_radius = mid_radius - self.fp_width / 2
            outer_radius = mid_radius + self.fp_width / 2
            
            # Draw the band as a wedge (semi-circle)
            wedge = Wedge((center_x, center_y), outer_radius, 0, 180,
                         width=self.fp_width, facecolor=color, alpha=0.3,
                         edgecolor='black', linewidth=0.5)
            ax.add_patch(wedge)
            
            # Place fingerprints on this band, tangent to each other
            if num_prints > 0:
                for i in range(num_prints):
                    # Calculate angle for this fingerprint
                    # Fingerprints are evenly distributed and tangent to neighbors
                    # Each fingerprint occupies fp_height of arc length
                    arc_per_print = math.pi * mid_radius / num_prints
                    
                    # Center angle of this fingerprint
                    angle = (i + 0.5) * arc_per_print / mid_radius
                    
                    # Position on the arc (center of ellipse on mid_radius)
                    x = center_x + mid_radius * math.cos(angle)
                    y = center_y + mid_radius * math.sin(angle)
                    
                    # The major axis (fp_height) should be aligned with the radius
                    # The minor axis (fp_width) should be tangent to the circle (perpendicular to radius)
                    # Angle points from center outward, so major axis should be at that angle
                    # In matplotlib Ellipse, angle is in degrees, measured counter-clockwise from horizontal
                    # The angle of the radius at this position is 'angle' (in radians)
                    rotation_deg = math.degrees(angle)
                    
                    # Draw fingerprint as ellipse
                    # width = major axis (along radius) = fp_height
                    # height = minor axis (tangent to circle) = fp_width
                    ellipse = Ellipse((x, y), self.fp_height, self.fp_width,
                                    angle=rotation_deg, 
                                    facecolor='none', edgecolor='black',
                                    linewidth=0.5, alpha=0.7)
                    ax.add_patch(ellipse)
        
        # Add title with allocation info
        allocation_str = " | ".join([f"{c[:3]}: {n}" for c, n in zip(self.COLORS, self.allocations)])
        ax.set_title(f"Fingerprint Rainbow (Band Spacing: {self.band_spacing_percent:.0f}%, Min Inner: {self.min_inner_prints}) - {allocation_str}", 
                    fontsize=9, pad=10)
        
        # Remove axes
        orientation_label = orientation.capitalize()
        ax.set_xlabel(f"Paper: {paper_width:.2f}\" × {paper_height:.2f}\" ({orientation_label}) | Margins: {margin:.2f}\"")
        ax.set_xticks([])
        ax.set_yticks([])


class FingerprintRainbowGUI:
    """Main GUI application"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Fingerprint Rainbow Optimizer")
        self.root.geometry("1200x800")
        
        # Default fingerprint dimensions (inches) - child's fingerprint
        self.fp_width_var = tk.StringVar(value="0.4")  # Short axis
        self.fp_height_var = tk.StringVar(value="0.6")  # Long axis
        
        # Band spacing percentage (percentage of fingerprint height)
        self.band_spacing_var = tk.DoubleVar(value=100.0)
        
        # Minimum fingerprints for innermost circle
        self.min_inner_var = tk.StringVar(value="5")
        
        # Paper orientation
        self.orientation_var = tk.StringVar(value="portrait")
        
        # Paper size variables
        self.paper_size_var = tk.StringVar(value="Letter (US)")
        self.paper_width_var = tk.StringVar(value="8.5")
        self.paper_height_var = tk.StringVar(value="11")
        self.margin_var = tk.StringVar(value="1.5")
        self.auto_paper_size = tk.BooleanVar(value=False)
        
        # Rainbow object
        self.rainbow: Optional[FingerprintRainbow] = None
        
        # Build GUI
        self._build_gui()
        
    def _build_gui(self):
        """Construct the GUI layout"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Set up proper window close handling
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Left panel - Controls
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.N, tk.S, tk.W), padx=(0, 10))
        
        self._build_controls(control_frame)
        
        # Right panel - Visualization
        viz_frame = ttk.LabelFrame(main_frame, text="Visualization", padding="10")
        viz_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        viz_frame.columnconfigure(0, weight=1)
        viz_frame.rowconfigure(0, weight=1)
        
        # Matplotlib figure with non-interactive backend
        plt.ioff()  # Turn off interactive mode
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        # Initial message
        self.ax.text(0.5, 0.5, 'Click "Generate Rainbow" to start', 
                    ha='center', va='center', fontsize=14, color='gray')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()
    
    def _on_closing(self):
        """Handle window close event properly"""
        try:
            # Close matplotlib figure
            plt.close(self.fig)
        except:
            pass
        finally:
            # Destroy the tkinter window
            self.root.quit()
            self.root.destroy()
        
    def _build_controls(self, parent: ttk.Frame):
        """Build the control panel"""
        row = 0
        
        # Fingerprint dimensions section
        ttk.Label(parent, text="Fingerprint Dimensions (inches)", 
                 font=('TkDefaultFont', 10, 'bold')).grid(row=row, column=0, columnspan=2, 
                                                          sticky=tk.W, pady=(0, 5))
        row += 1
        
        ttk.Label(parent, text="Width (short axis):").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Entry(parent, textvariable=self.fp_width_var, width=10).grid(row=row, column=1, 
                                                                         sticky=tk.W, pady=2)
        row += 1
        
        ttk.Label(parent, text="Height (long axis):").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Entry(parent, textvariable=self.fp_height_var, width=10).grid(row=row, column=1, 
                                                                          sticky=tk.W, pady=2)
        row += 1
        
        ttk.Button(parent, text="Use Child Default (0.4\" × 0.6\")", 
                  command=self._set_child_default).grid(row=row, column=0, columnspan=2, 
                                                        pady=5, sticky=tk.W+tk.E)
        row += 1
        
        ttk.Button(parent, text="Use Adult Default (0.5\" × 0.8\")", 
                  command=self._set_adult_default).grid(row=row, column=0, columnspan=2, 
                                                        pady=5, sticky=tk.W+tk.E)
        row += 1
        
        ttk.Separator(parent, orient='horizontal').grid(row=row, column=0, columnspan=2, 
                                                        sticky=tk.W+tk.E, pady=10)
        row += 1
        
        # Band spacing section
        ttk.Label(parent, text="Band Spacing", 
                 font=('TkDefaultFont', 10, 'bold')).grid(row=row, column=0, columnspan=2, 
                                                          sticky=tk.W, pady=(0, 5))
        row += 1
        
        ttk.Label(parent, text="Spacing (% of height):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.spacing_label = ttk.Label(parent, text=f"{self.band_spacing_var.get():.0f}%")
        self.spacing_label.grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        
        self.spacing_slider = ttk.Scale(parent, from_=50, to=150, 
                                       variable=self.band_spacing_var,
                                       orient='horizontal',
                                       command=self._on_spacing_changed)
        self.spacing_slider.grid(row=row, column=0, columnspan=2, sticky=tk.W+tk.E, pady=5)
        row += 1
        
        ttk.Label(parent, text="(100% = fingerprints just touching)", 
                 font=('TkDefaultFont', 8)).grid(row=row, column=0, columnspan=2, 
                                                 sticky=tk.W, pady=(0, 5))
        row += 1
        
        ttk.Separator(parent, orient='horizontal').grid(row=row, column=0, columnspan=2, 
                                                        sticky=tk.W+tk.E, pady=10)
        row += 1
        
        # Minimum inner circle section
        ttk.Label(parent, text="Inner Circle", 
                 font=('TkDefaultFont', 10, 'bold')).grid(row=row, column=0, columnspan=2, 
                                                          sticky=tk.W, pady=(0, 5))
        row += 1
        
        ttk.Label(parent, text="Min fingerprints:").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Entry(parent, textvariable=self.min_inner_var, width=10).grid(row=row, column=1, 
                                                                          sticky=tk.W, pady=2)
        row += 1
        
        ttk.Label(parent, text="(for innermost violet band)", 
                 font=('TkDefaultFont', 8)).grid(row=row, column=0, columnspan=2, 
                                                 sticky=tk.W, pady=(0, 5))
        row += 1
        
        ttk.Separator(parent, orient='horizontal').grid(row=row, column=0, columnspan=2, 
                                                        sticky=tk.W+tk.E, pady=10)
        row += 1
        
        # Paper size section
        ttk.Label(parent, text="Paper Size", 
                 font=('TkDefaultFont', 10, 'bold')).grid(row=row, column=0, columnspan=2, 
                                                          sticky=tk.W, pady=(0, 5))
        row += 1
        
        ttk.Checkbutton(parent, text="Auto-select paper size", 
                       variable=self.auto_paper_size,
                       command=self._toggle_auto_paper).grid(row=row, column=0, columnspan=2, 
                                                             sticky=tk.W, pady=2)
        row += 1
        
        ttk.Label(parent, text="Orientation:").grid(row=row, column=0, sticky=tk.W, pady=2)
        orientation_frame = ttk.Frame(parent)
        orientation_frame.grid(row=row, column=1, sticky=tk.W, pady=2)
        ttk.Radiobutton(orientation_frame, text="Portrait", variable=self.orientation_var, 
                       value="portrait").pack(side=tk.LEFT)
        ttk.Radiobutton(orientation_frame, text="Landscape", variable=self.orientation_var, 
                       value="landscape").pack(side=tk.LEFT, padx=(5, 0))
        row += 1
        
        ttk.Label(parent, text="Preset:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.paper_combo = ttk.Combobox(parent, textvariable=self.paper_size_var, 
                                        values=list(PAPER_SIZES.keys()), 
                                        state='readonly', width=15)
        self.paper_combo.grid(row=row, column=1, sticky=tk.W, pady=2)
        self.paper_combo.bind('<<ComboboxSelected>>', self._on_paper_size_selected)
        row += 1
        
        ttk.Label(parent, text="Width (inches):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.paper_width_entry = ttk.Entry(parent, textvariable=self.paper_width_var, width=10)
        self.paper_width_entry.grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        
        ttk.Label(parent, text="Height (inches):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.paper_height_entry = ttk.Entry(parent, textvariable=self.paper_height_var, width=10)
        self.paper_height_entry.grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        
        ttk.Separator(parent, orient='horizontal').grid(row=row, column=0, columnspan=2, 
                                                        sticky=tk.W+tk.E, pady=10)
        row += 1
        
        # Margin section
        ttk.Label(parent, text="Margins", 
                 font=('TkDefaultFont', 10, 'bold')).grid(row=row, column=0, columnspan=2, 
                                                          sticky=tk.W, pady=(0, 5))
        row += 1
        
        ttk.Label(parent, text="Margin (inches):").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Entry(parent, textvariable=self.margin_var, width=10).grid(row=row, column=1, 
                                                                       sticky=tk.W, pady=2)
        row += 1
        
        ttk.Separator(parent, orient='horizontal').grid(row=row, column=0, columnspan=2, 
                                                        sticky=tk.W+tk.E, pady=10)
        row += 1
        
        # Action buttons
        ttk.Button(parent, text="Generate Rainbow", 
                  command=self._generate_rainbow,
                  style='Accent.TButton').grid(row=row, column=0, columnspan=2, 
                                               pady=10, sticky=tk.W+tk.E)
        row += 1
        
        # Info display
        self.info_frame = ttk.LabelFrame(parent, text="Rainbow Info", padding="5")
        self.info_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W+tk.E, pady=10)
        
        self.info_label = ttk.Label(self.info_frame, text="No rainbow generated yet", 
                                    justify=tk.LEFT, wraplength=250)
        self.info_label.pack()
        
    def _set_child_default(self):
        """Set child fingerprint defaults"""
        self.fp_width_var.set("0.4")
        self.fp_height_var.set("0.6")
        
    def _set_adult_default(self):
        """Set adult fingerprint defaults"""
        self.fp_width_var.set("0.5")
        self.fp_height_var.set("0.8")
    
    def _on_spacing_changed(self, value):
        """Update spacing label when slider changes"""
        self.spacing_label.config(text=f"{self.band_spacing_var.get():.0f}%")
        
    def _toggle_auto_paper(self):
        """Toggle automatic paper size selection"""
        if self.auto_paper_size.get():
            # Disable manual paper size inputs
            self.paper_combo.configure(state='disabled')
            self.paper_width_entry.configure(state='disabled')
            self.paper_height_entry.configure(state='disabled')
        else:
            # Enable manual paper size inputs
            self.paper_combo.configure(state='readonly')
            if self.paper_size_var.get() == "Custom":
                self.paper_width_entry.configure(state='normal')
                self.paper_height_entry.configure(state='normal')
            else:
                self.paper_width_entry.configure(state='disabled')
                self.paper_height_entry.configure(state='disabled')
    
    def _on_paper_size_selected(self, event=None):
        """Handle paper size selection"""
        size_name = self.paper_size_var.get()
        paper_size = PAPER_SIZES[size_name]
        
        if size_name == "Custom":
            self.paper_width_entry.configure(state='normal')
            self.paper_height_entry.configure(state='normal')
        else:
            self.paper_width_var.set(str(paper_size.width))
            self.paper_height_var.set(str(paper_size.height))
            self.paper_width_entry.configure(state='disabled')
            self.paper_height_entry.configure(state='disabled')
    
    def _find_optimal_paper_size(self, rainbow_width: float, rainbow_height: float, 
                                margin: float, orientation: str) -> Tuple[str, float, float]:
        """
        Find the smallest paper size that fits the rainbow with margins
        
        Args:
            rainbow_width: Width of rainbow in inches
            rainbow_height: Height of rainbow in inches
            margin: Required margin in inches
            orientation: "portrait" or "landscape"
            
        Returns:
            (paper_name, paper_width, paper_height)
        """
        required_width = rainbow_width + 2 * margin
        required_height = rainbow_height + 2 * margin
        
        # Sort paper sizes by area
        suitable_sizes = []
        for name, paper in PAPER_SIZES.items():
            if name == "Custom":
                continue
            
            # Check if paper fits in the requested orientation
            if orientation == "portrait":
                fits = paper.width >= required_width and paper.height >= required_height
                actual_width, actual_height = paper.width, paper.height
            else:  # landscape
                fits = paper.height >= required_width and paper.width >= required_height
                actual_width, actual_height = paper.height, paper.width
            
            if fits:
                area = paper.width * paper.height
                suitable_sizes.append((area, name, actual_width, actual_height))
        
        if suitable_sizes:
            suitable_sizes.sort()  # Sort by area
            return suitable_sizes[0][1], suitable_sizes[0][2], suitable_sizes[0][3]
        else:
            # No standard size fits, return custom size
            return "Custom", required_width, required_height
    
    def _generate_rainbow(self):
        """Generate and visualize the rainbow"""
        try:
            # Parse inputs
            fp_width = float(self.fp_width_var.get())
            fp_height = float(self.fp_height_var.get())
            margin = float(self.margin_var.get())
            band_spacing_percent = float(self.band_spacing_var.get())
            min_inner = int(self.min_inner_var.get())
            orientation = self.orientation_var.get()
            
            if fp_width <= 0 or fp_height <= 0 or margin < 0:
                raise ValueError("Dimensions must be positive")
            
            if band_spacing_percent <= 0:
                raise ValueError("Band spacing must be positive")
            
            if min_inner < 1 or min_inner > 50:
                raise ValueError("Minimum inner fingerprints must be between 1 and 50")
            
            # Create rainbow
            self.rainbow = FingerprintRainbow(fp_width, fp_height, band_spacing_percent, min_inner)
            rainbow_width, rainbow_height = self.rainbow.calculate_dimensions()
            
            # Determine paper size
            if self.auto_paper_size.get():
                paper_name, paper_width, paper_height = self._find_optimal_paper_size(
                    rainbow_width, rainbow_height, margin, orientation
                )
                self.paper_size_var.set(paper_name)
                self.paper_width_var.set(f"{paper_width:.2f}")
                self.paper_height_var.set(f"{paper_height:.2f}")
            else:
                paper_width = float(self.paper_width_var.get())
                paper_height = float(self.paper_height_var.get())
                paper_name = self.paper_size_var.get()
            
            # Check if rainbow fits (considering orientation)
            actual_width = paper_width if orientation == "portrait" else paper_height
            actual_height = paper_height if orientation == "portrait" else paper_width
            
            if rainbow_width + 2*margin > actual_width or rainbow_height + 2*margin > actual_height:
                messagebox.showwarning("Warning", 
                    f"Rainbow dimensions ({rainbow_width:.2f}\" × {rainbow_height:.2f}\") "
                    f"plus margins ({margin:.2f}\") exceed paper size "
                    f"({actual_width:.2f}\" × {actual_height:.2f}\" in {orientation}).\n\n"
                    f"Consider enabling auto-paper size or using larger paper.")
            
            # Render
            self.rainbow.render(self.ax, paper_width, paper_height, margin, orientation)
            self.canvas.draw()
            
            # Update info
            info_text = (
                f"Rainbow Dimensions:\n"
                f"  {rainbow_width:.2f}\" × {rainbow_height:.2f}\"\n\n"
                f"Paper Size: {paper_name}\n"
                f"  {paper_width:.2f}\" × {paper_height:.2f}\"\n"
                f"  Orientation: {orientation.capitalize()}\n\n"
                f"Band Spacing: {band_spacing_percent:.0f}%\n"
                f"Min Inner: {min_inner}\n\n"
                f"Fingerprint Allocation:\n"
            )
            for color, count in zip(FingerprintRainbow.COLORS, self.rainbow.allocations):
                info_text += f"  {color.capitalize()}: {count}\n"
            
            self.info_label.config(text=info_text)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = FingerprintRainbowGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
