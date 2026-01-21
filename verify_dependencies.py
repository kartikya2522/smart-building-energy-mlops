#!/usr/bin/env python
"""
Dependency verification script for Streamlit Cloud deployment.

This script verifies that all required packages can be installed and imported successfully.
Run this locally before deploying to ensure the deployment will succeed.

Usage:
    python verify_dependencies.py
"""

import sys
import subprocess

def test_imports():
    """Test that all required modules can be imported."""
    packages = {
        'streamlit': 'Streamlit framework',
        'plotly': 'Plotly visualization',
        'pandas': 'Pandas data processing',
        'numpy': 'NumPy numerical computing',
        'sklearn': 'Scikit-learn machine learning',
        'joblib': 'Joblib serialization',
    }
    
    print("Testing imports...")
    all_ok = True
    
    for module_name, description in packages.items():
        try:
            __import__(module_name)
            print(f"  [OK] {module_name}: {description}")
        except ImportError as e:
            print(f"  [FAIL] {module_name}: {e}")
            all_ok = False
    
    return all_ok

def verify_model():
    """Test that the model can be loaded."""
    print("\nVerifying model...")
    try:
        import joblib
        from pathlib import Path
        
        model_path = Path("models/ridge_model.pkl")
        if not model_path.exists():
            print(f"  [FAIL] Model file not found: {model_path}")
            return False
        
        model = joblib.load(model_path)
        print(f"  [OK] Model loaded successfully: {type(model)}")
        return True
    except Exception as e:
        print(f"  [FAIL] Model loading failed: {e}")
        return False

def verify_config():
    """Test that the configuration files exist."""
    print("\nVerifying configuration files...")
    from pathlib import Path
    
    required_files = [
        "models/ridge_model.pkl",
        "models/feature_names.json",
        ".streamlit/config.toml",
        "requirements.txt",
    ]
    
    all_ok = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"  [OK] {file_path}")
        else:
            print(f"  [FAIL] {file_path} - NOT FOUND")
            all_ok = False
    
    return all_ok

def main():
    """Run all verification tests."""
    print("=" * 60)
    print("Streamlit Cloud Deployment Verification")
    print("=" * 60)
    
    imports_ok = test_imports()
    model_ok = verify_model()
    config_ok = verify_config()
    
    print("\n" + "=" * 60)
    if imports_ok and model_ok and config_ok:
        print("[OK] ALL CHECKS PASSED - Ready for deployment!")
        print("=" * 60)
        return 0
    else:
        print("[FAIL] SOME CHECKS FAILED - See details above")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
