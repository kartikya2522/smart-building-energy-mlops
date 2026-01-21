#!/usr/bin/env python
"""Setup script for Smart Building Energy Prediction Streamlit App"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="smart-building-energy-mlops",
    version="1.0.0",
    author="ML Pipeline",
    description="Smart Building Energy Consumption Prediction with MLOps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kartikya2522/smart-building-energy-mlops",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "streamlit>=1.28.0",
        "plotly>=5.17.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.7.0",
        "joblib>=1.5.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
