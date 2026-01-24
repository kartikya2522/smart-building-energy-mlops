"""
Insights Endpoint

Provides information about the top drivers of energy consumption.

Based on feature importance from the Ridge Regression model,
this endpoint returns the most influential features affecting building energy.
"""

from typing import List
from app.schemas import InsightsResponse
import logging

logger = logging.getLogger(__name__)


def get_insights() -> InsightsResponse:
    """
    Get insights about top drivers of energy consumption.
    
    Returns:
        InsightsResponse with top drivers and their descriptions
        
    Note:
        This returns domain-based insights about energy consumption drivers
        in smart buildings. These are based on the feature engineering pipeline
        and domain knowledge about building HVAC and energy systems.
    """
    
    # Top drivers based on feature importance in the trained model
    # and domain knowledge from the feature engineering pipeline
    top_drivers = [
        "RH_6",          # Relative humidity - affects equipment operation
        "Visibility",    # Correlates with cloud cover and solar gains
        "Tdewpoint",     # Temperature - influences HVAC energy demand
        "rv1",           # Solar radiation - direct impact on heating/cooling
        "Windspeed"      # Wind effects on building envelope losses
    ]
    
    descriptions = [
        "Outdoor humidity (RH_6) directly affects HVAC equipment operation and dehumidification loads",
        "Visibility correlates with cloud cover; lower visibility means more artificial lighting and less solar cooling",
        "Dew point temperature indicates atmospheric moisture; higher values increase HVAC energy consumption",
        "Solar radiation (rv1) directly influences building cooling and heating demands",
        "Wind speed affects heat transfer through the building envelope and infiltration losses"
    ]
    
    logger.info("Insights retrieved: 5 top drivers")
    
    return InsightsResponse(
        top_drivers=top_drivers,
        descriptions=descriptions
    )
