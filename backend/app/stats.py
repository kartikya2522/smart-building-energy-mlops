"""
Stats Endpoint

Provides metadata about the deployed model and energy prediction constants.
"""

from app.schemas import StatsResponse
import logging

logger = logging.getLogger(__name__)


def get_stats() -> StatsResponse:
    """
    Get model statistics and configuration information.
    
    Returns:
        StatsResponse with model metadata and feature information
    """
    
    features_used = [
        "RH_6",         # Relative humidity at outdoor reference station (%)
        "Windspeed",    # Wind speed (m/s)
        "Visibility",   # Visibility (km)
        "Tdewpoint",    # Dew point temperature (°C)
        "rv1",          # Extraterrestrial radiation - horizontal component (Wh/m²)
        "hour",         # Hour of day (0-23)
        "hour_sin",     # Sine-encoded cyclical hour
        "hour_cos"      # Cosine-encoded cyclical hour
    ]
    
    co2_factor = 0.82  # kg CO2 per kWh
    
    logger.info(f"Stats retrieved: Ridge Regression model with {len(features_used)} features")
    
    return StatsResponse(
        model_type="Ridge Regression (α=1.0)",
        features_used=features_used,
        co2_factor=co2_factor
    )
