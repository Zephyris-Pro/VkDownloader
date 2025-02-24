#!/bin/bash

echo "Activating the virtual environment..."
source .venv/bin/activate

echo "Compiling..."
pyinstaller --onefile --console --icon=assets/icon.ico vk_downloader.py

echo "Compilation completed!"
