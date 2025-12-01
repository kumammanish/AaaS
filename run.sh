#!/bin/bash
# Quick start script for Azure Architecture Diagram Generator Web App

echo "================================================================================"
echo " Azure Architecture Diagram Generator - Web Application"
echo "================================================================================"
echo ""

# Check if GraphViz is installed
if ! command -v dot &> /dev/null; then
    echo " GraphViz is not installed"
    echo "   Please install it first:"
    echo "   macOS: brew install graphviz"
    echo "   Linux: sudo apt-get install graphviz"
    exit 1
fi

echo " GraphViz found"

# Check if virtual environment exists
if [ ! -d "venv" ] && [ ! -d "../Arch_Diagrams/venv" ]; then
    echo " Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
if [ -d "venv" ]; then
    echo " Activating virtual environment (webapp/venv)..."
    source venv/bin/activate
elif [ -d "../Arch_Diagrams/venv" ]; then
    echo " Activating virtual environment (Arch_Diagrams/venv)..."
    source ../Arch_Diagrams/venv/bin/activate
fi

# Install dependencies
echo " Installing dependencies..."
pip install -q -r requirements.txt

# Create output directory
mkdir -p output

echo ""
echo " Setup complete!"
echo ""
echo "================================================================================"
echo " Starting web application..."
echo "================================================================================"
echo ""
echo "   Access the application at: http://localhost:5000"
echo ""
echo "   Press Ctrl+C to stop the server"
echo ""
echo "================================================================================"
echo ""

# Run the application
python app.py
