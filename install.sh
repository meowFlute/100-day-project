#!/bin/bash

# Fingerprint Rainbow Optimizer - Installation Script
# For Ubuntu/Debian-based systems

echo "=========================================="
echo "Fingerprint Rainbow Optimizer - Setup"
echo "=========================================="
echo ""

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "Warning: This script is designed for Ubuntu/Debian Linux systems."
    echo "You may need to manually install dependencies on other systems."
    echo ""
fi

# Update package list
echo "Step 1: Updating package list..."
sudo apt update

# Install Python3 and pip if not present
echo ""
echo "Step 2: Installing Python3 and pip..."
sudo apt install -y python3 python3-pip

# Install tkinter for GUI
echo ""
echo "Step 3: Installing Python tkinter (GUI library)..."
sudo apt install -y python3-tk

# Install Python dependencies
echo ""
echo "Step 4: Installing Python matplotlib numpy..."
sudo apt install -y python3-matplotlib python3-numpy

# Make the main script executable
echo ""
echo "Step 5: Making fingerprint_rainbow.py executable..."
chmod +x fingerprint_rainbow.py

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "To run the application, use:"
echo "  ./fingerprint_rainbow.py"
echo "or"
echo "  python3 fingerprint_rainbow.py"
echo ""
echo "Enjoy creating your fingerprint rainbow!"
echo ""
