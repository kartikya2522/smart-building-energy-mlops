"""
Model Loading and Prediction Logic

This module handles:
1. Loading the trained Ridge Regression model from MLflow artifacts
2. Applying the feature engineering pipeline to input data
3. Making predictions and computing derived metrics (cost, CO2)

The module reuses the trained model and does not reimplement any ML logic.
"""

import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from typing import Dict, Tuple
import logging

from app.schemas import PredictRequest, PredictResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Model paths
MODEL_PATH = PROJECT_ROOT / "mlruns" / "1" / "models" / "m-ddcc4d73d7fa47349323f0cf17eb32fb" / "artifacts" / "model.pkl"
FEATURE_NAMES_PATH = PROJECT_ROOT / "models" / "feature_names.json"

# Constants for cost and CO2 calculations
COST_FACTOR_INR_PER_KWH = 5.0  # 5 INR per kWh
CO2_FACTOR_KG_PER_KWH = 0.82    # 0.82 kg CO2 per kWh


class ModelPredictor:
    """
    Handles model loading and prediction logic.
    
    Loads the trained Ridge Regression model from MLflow artifacts
    and provides methods to make predictions on new data.
    """
    
    def __init__(self):
        """Initialize the predictor by loading the trained model and feature names."""
        self.model = None
        self.feature_names = None
        self._load_model()
        self._load_feature_names()
    
    def _load_model(self):
        """Load the trained Ridge Regression model from disk."""
        try:
            if not MODEL_PATH.exists():
                raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
            
            self.model = joblib.load(str(MODEL_PATH))
            logger.info(f"✓ Model loaded from: {MODEL_PATH}")
        except Exception as e:
            logger.error(f"✗ Failed to load model: {e}")
            raise
    
    def _load_feature_names(self):
        """Load the feature names used during training."""
        try:
            import json
            if not FEATURE_NAMES_PATH.exists():
                raise FileNotFoundError(f"Feature names file not found at {FEATURE_NAMES_PATH}")
            
            with open(FEATURE_NAMES_PATH, 'r') as f:
                self.feature_names = json.load(f)
            
            logger.info(f"✓ Feature names loaded: {self.feature_names}")
        except Exception as e:
            logger.error(f"✗ Failed to load feature names: {e}")
            raise
    
    def prepare_features(self, request: PredictRequest) -> pd.DataFrame:
        """
        Convert request object to feature DataFrame in correct order.
        
        Args:
            request: PredictRequest containing input features
            
        Returns:
            pd.DataFrame with features in the exact order expected by the model
        """
        # Convert request to dictionary
        data_dict = request.dict()
        
        # Create DataFrame with single row
        df = pd.DataFrame([data_dict])
        
        # Reorder columns to match training order
        df = df[self.feature_names]
        
        logger.info(f"Features prepared: {df.shape}")
        return df
    
    def predict(self, request: PredictRequest) -> PredictResponse:
        """
        Make a prediction using the trained model.
        
        Args:
            request: PredictRequest containing input features
            
        Returns:
            PredictResponse with energy prediction and derived metrics
            
        Raises:
            ValueError: If model is not loaded or prediction fails
        """
        if self.model is None:
            raise ValueError("Model not loaded. Cannot make predictions.")
        
        try:
            # Prepare features
            X = self.prepare_features(request)
            
            # Make prediction (model returns energy in Wh)
            energy_wh = float(self.model.predict(X)[0])
            
            # Ensure non-negative prediction
            energy_wh = max(0.0, energy_wh)
            
            # Calculate derived metrics
            energy_kwh = energy_wh / 1000.0
            cost_inr = energy_kwh * COST_FACTOR_INR_PER_KWH
            co2_kg = energy_kwh * CO2_FACTOR_KG_PER_KWH
            
            logger.info(f"Prediction made: {energy_wh:.2f} Wh, {cost_inr:.3f} INR, {co2_kg:.4f} kg CO2")
            
            return PredictResponse(
                energy_wh=round(energy_wh, 2),
                cost_inr=round(cost_inr, 3),
                co2_kg=round(co2_kg, 4)
            )
        
        except Exception as e:
            logger.error(f"✗ Prediction failed: {e}")
            raise


# Global predictor instance (lazy loaded)
_predictor = None


def get_predictor() -> ModelPredictor:
    """
    Get or create the global predictor instance.
    
    Uses lazy loading to load the model only once at first use.
    
    Returns:
        ModelPredictor instance
    """
    global _predictor
    if _predictor is None:
        _predictor = ModelPredictor()
    return _predictor
