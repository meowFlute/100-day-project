#!/usr/bin/env python3
"""
Test script for Fingerprint Rainbow - demonstrates core functionality
"""

from fingerprint_rainbow import FingerprintRainbow, PAPER_SIZES
import matplotlib.pyplot as plt

def test_allocation():
    """Test the fingerprint allocation algorithm"""
    print("=" * 50)
    print("Testing Fingerprint Allocation")
    print("=" * 50)
    
    # Child fingerprint dimensions with 100% spacing
    rainbow = FingerprintRainbow(fingerprint_width=0.4, fingerprint_height=0.6, 
                                 band_spacing_percent=100.0, min_inner_prints=5)
    
    print("\nChild Fingerprint (0.4\" × 0.6\") - 100% Band Spacing, Min Inner: 5:")
    print(f"Rainbow Dimensions: {rainbow.calculate_dimensions()[0]:.2f}\" × {rainbow.calculate_dimensions()[1]:.2f}\"")
    print("\nFingerprint Allocation:")
    
    total = 0
    for color, count in zip(FingerprintRainbow.COLORS, rainbow.allocations):
        print(f"  {color.capitalize():8s}: {count:2d} fingerprints")
        total += count
    
    print(f"  {'Total':8s}: {total:2d} fingerprints")
    print()
    
    # Adult fingerprint dimensions with 120% spacing and higher minimum
    rainbow_adult = FingerprintRainbow(fingerprint_width=0.5, fingerprint_height=0.8,
                                       band_spacing_percent=120.0, min_inner_prints=10)
    
    print("\nAdult Fingerprint (0.5\" × 0.8\") - 120% Band Spacing, Min Inner: 10:")
    print(f"Rainbow Dimensions: {rainbow_adult.calculate_dimensions()[0]:.2f}\" × {rainbow_adult.calculate_dimensions()[1]:.2f}\"")
    print("\nFingerprint Allocation:")
    
    total = 0
    for color, count in zip(FingerprintRainbow.COLORS, rainbow_adult.allocations):
        print(f"  {color.capitalize():8s}: {count:2d} fingerprints")
        total += count
    
    print(f"  {'Total':8s}: {total:2d} fingerprints")

def test_paper_sizes():
    """Test paper size fitting"""
    print("\n" + "=" * 50)
    print("Testing Paper Size Recommendations")
    print("=" * 50)
    
    rainbow = FingerprintRainbow(fingerprint_width=0.4, fingerprint_height=0.6,
                                 band_spacing_percent=100.0, min_inner_prints=5)
    rainbow_width, rainbow_height = rainbow.calculate_dimensions()
    margin = 1.5
    
    required_width = rainbow_width + 2 * margin
    required_height = rainbow_height + 2 * margin
    
    print(f"\nRainbow dimensions: {rainbow_width:.2f}\" × {rainbow_height:.2f}\"")
    print(f"Required space with {margin}\" margins: {required_width:.2f}\" × {required_height:.2f}\"")
    
    print("\nPaper sizes that fit (Portrait):")
    for name, paper in PAPER_SIZES.items():
        if name == "Custom":
            continue
        fits = paper.width >= required_width and paper.height >= required_height
        status = "✓ Fits" if fits else "✗ Too small"
        print(f"  {name:15s} ({paper.width:5.2f}\" × {paper.height:5.2f}\"): {status}")
    
    print("\nPaper sizes that fit (Landscape):")
    for name, paper in PAPER_SIZES.items():
        if name == "Custom":
            continue
        fits = paper.height >= required_width and paper.width >= required_height
        status = "✓ Fits" if fits else "✗ Too small"
        print(f"  {name:15s} ({paper.height:5.2f}\" × {paper.width:5.2f}\"): {status}")

def test_visualization():
    """Create a test visualization"""
    print("\n" + "=" * 50)
    print("Creating Test Visualization")
    print("=" * 50)
    print("\nGenerating rainbow visualization...")
    
    rainbow = FingerprintRainbow(fingerprint_width=0.4, fingerprint_height=0.6,
                                 band_spacing_percent=100.0, min_inner_prints=5)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Render on Letter paper with 1.5" margins in portrait
    rainbow.render(ax, paper_width=8.5, paper_height=11, margin=1.5, orientation="portrait")
    
    # Save to file
    output_file = "test_rainbow.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Saved visualization to: {output_file}")
    
    print("\nVisualization complete!")
    print("(Close the plot window to continue)")
    
    # Show plot
    plt.show()

if __name__ == "__main__":
    print("\nFingerprint Rainbow - Test Suite\n")
    
    test_allocation()
    test_paper_sizes()
    
    # Ask if user wants to see visualization
    try:
        response = input("\nWould you like to see a test visualization? (y/n): ")
        if response.lower() in ['y', 'yes']:
            test_visualization()
        else:
            print("\nSkipping visualization. Run the full GUI with:")
            print("  python3 fingerprint_rainbow.py")
    except (EOFError, KeyboardInterrupt):
        print("\n\nTest complete. Run the full GUI with:")
        print("  python3 fingerprint_rainbow.py")
    
    print("\n" + "=" * 50)
    print("All tests complete!")
    print("=" * 50)
