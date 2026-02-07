# Fingerprint Rainbow Optimizer

A Python GUI application to optimize and visualize the distribution of 100 fingerprints across a 7-band rainbow (red, orange, yellow, green, blue, indigo, violet).

## Features

- **Fingerprint Dimension Input**: Configure fingerprint width and height with presets for child and adult fingerprints
- **Automatic Fingerprint Allocation**: Intelligently distributes 100 fingerprints across rainbow bands based on arc length
- **Paper Size Selection**: Choose from standard US and A-series paper sizes, or specify custom dimensions
- **Auto Paper Size**: Automatically selects the smallest paper size that fits the rainbow with specified margins
- **Configurable Margins**: Set minimum margin requirements for printing
- **Real-time Visualization**: See the rainbow layout with fingerprint ellipses positioned on each colored band
- **Detailed Information**: View allocation statistics and dimensions

## Installation

### Ubuntu System Setup

1. **Update system packages**:
```bash
sudo apt update
sudo apt upgrade -y
```

2. **Install Python 3 and required system packages**:
```bash
sudo apt install python3 python3-tk python3-matplotlib python3-numpy -y
```

## Usage

### Running the Application

```bash
python3 fingerprint_rainbow.py
```

Or make it executable:
```bash
chmod +x fingerprint_rainbow.py
./fingerprint_rainbow.py
```

### Using the GUI

1. **Set Fingerprint Dimensions**:
   - Enter width (short axis) and height (long axis) in inches
   - Use preset buttons for child (0.4" × 0.6") or adult (0.5" × 0.8") defaults

2. **Configure Paper Size**:
   - Choose from dropdown: Letter, Legal, Tabloid, A4, A3, A2, A1, or Custom
   - For custom sizes, select "Custom" and enter dimensions manually
   - Enable "Auto-select paper size" to automatically choose the smallest suitable paper

3. **Set Margins**:
   - Enter desired margin size in inches (default: 1.5")

4. **Generate Rainbow**:
   - Click "Generate Rainbow" to create and visualize the layout
   - View allocation details in the info panel
   - The visualization shows colored bands with fingerprint ellipses positioned correctly

## How It Works

### Fingerprint Allocation Algorithm

The application uses a proportional allocation algorithm:
1. Calculates the arc length of each rainbow band (half-circle)
2. Determines how many fingerprints can fit along each arc based on fingerprint height
3. Distributes 100 fingerprints proportionally based on each band's capacity
4. Larger outer bands receive more fingerprints than smaller inner bands

### Visualization

- Each band is drawn as a semi-circular wedge with appropriate color
- Fingerprints are represented as ellipses positioned along the band's arc
- Ellipses are oriented radially (long axis aligned with radius)
- Short axis is tangent to the band's center line

### Paper Size Selection

When auto-select is enabled:
- Calculates required paper dimensions (rainbow + 2 × margin)
- Searches through standard paper sizes
- Selects the smallest paper that accommodates the rainbow
- If no standard size fits, suggests custom dimensions

## Paper Sizes Included

### US Standard Sizes
- Letter: 8.5" × 11"
- Legal: 8.5" × 14"
- Tabloid: 11" × 17"

### A-Series Sizes
- A4: 8.27" × 11.69"
- A3: 11.69" × 16.54"
- A2: 16.54" × 23.39"
- A1: 23.39" × 33.11"

## Example Use Cases

1. **School Art Project**: Use child fingerprint defaults with Letter paper and 1" margins
2. **Community Mural**: Use adult fingerprints with A2 or larger paper
3. **Custom Installation**: Adjust fingerprint sizes and use auto-paper selection for optimal sizing

## Tips

- For best results, measure actual fingerprints and use those dimensions
- Use auto-paper size to avoid trial and error with paper selection
- Larger margins provide more room for mounting or framing
- The outer violet band will have the most fingerprints, inner red band the fewest

## Troubleshooting

**Error: "tkinter module not found"**
```bash
sudo apt install python3-tk
```

**Error: "matplotlib module not found"**
```bash
pip3 install matplotlib
```

**Warning: Rainbow exceeds paper size**
- Enable auto-paper size selection
- Or manually select a larger paper size
- Or reduce margin size
- Or use smaller fingerprint dimensions

## Technical Details

- Built with: Python 3, tkinter, matplotlib, numpy
- GUI Framework: tkinter (Python's standard GUI library)
- Visualization: matplotlib with embedded canvas
- Geometry: Uses ellipse patches and wedge patches for accurate representation

## License

Free to use for educational and personal projects.
