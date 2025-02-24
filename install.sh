#!/bin/bash

if [ ! -d ".venv" ]; then
    echo "Creating the virtual environment..."
    python3 -m venv .venv
fi

echo "Activating the virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Installation completed!"
