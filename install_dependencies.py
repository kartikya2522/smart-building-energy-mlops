#!/usr/bin/env python
"""
Installation script for Smart Building Energy Prediction Streamlit App

This script ensures all required dependencies are installed for the Streamlit application.

Usage:
    python install_dependencies.py
"""

import subprocess
import sys

def install_requirements():
    """Install dependencies from requirements.txt"""
    print("Installing dependencies for Streamlit app...")
    
    # Essential packages for the app
    essential_packages = [
        "streamlit>=1.28.0",
        "plotly>=5.17.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.7.0",
        "joblib>=1.5.0",
    ]
    
    for package in essential_packages:
        print(f"\nInstalling {package}...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package],
            capture_output=False
        )
        if result.returncode != 0:
            print(f"Warning: Failed to install {package}")
    
    print("\n✅ Installation complete!")

if __name__ == "__main__":
    install_requirements()
