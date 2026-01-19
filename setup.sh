#!/bin/bash

# Quick Start Script for Linux/Mac

echo "=================================="
echo "Fingerprint Automation System"
echo "Quick Start Script"
echo "=================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "   Install Python 3 first: https://www.python.org/downloads/"
    exit 1
fi

echo "✓ Python 3 found"

# Install requirements
echo ""
echo "Installing Python requirements..."

# Check if python_backend directory exists
if [ ! -d "python_backend" ]; then
    echo "❌ Error: python_backend directory not found!"
    echo "   Make sure you're running this from the repository root."
    exit 1
fi

cd python_backend
pip3 install -r requirements.txt

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Upload arduino_fingerprint.ino to your Arduino"
echo "2. Connect fingerprint sensor to Arduino"
echo "3. Run: python3 fingerprint_app.py -p /dev/ttyUSB0"
echo "   (Replace /dev/ttyUSB0 with your Arduino port)"
echo ""
echo "For detailed instructions, see docs/GUIDE.md"
echo ""
