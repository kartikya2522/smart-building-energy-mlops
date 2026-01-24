"""
Pydantic Request/Response Models for Smart Building Energy Prediction API

This module defines the data structures for API endpoints using Pydantic,
providing automatic validation, serialization, and documentation.
"""

from pydantic import BaseModel, Field
from typing import List


class PredictRequest(BaseModel):
    """
    Request body for POST /predict endpoint.
    
    Contains all numerical features required by the trained Ridge Regression model.
    All features are required for a valid prediction.
    
    Features (based on VIF-filtered engineering pipeline):
    - RH_6: Relative humidity measured at outdoor reference station (%)
    - Windspeed: Wind speed (m/s)
    - Visibility: Visibility (km)
    - Tdewpoint: Dew point temperature (°C)
    - rv1: Extraterrestrial radiation - horizontal component (Wh/m²)
    - hour: Hour of day (0-23)
    - hour_sin: Cyclical sine encoding of hour
    - hour_cos: Cyclical cosine encoding of hour
    """
    
    RH_6: float = Field(
        ..., 
        description="Relative humidity measured at outdoor reference station (%)",
        ge=0.0,
        le=100.0
    )
    Windspeed: float = Field(
        ...,
        description="Wind speed (m/s)",
        ge=0.0
    )
    Visibility: float = Field(
        ...,
        description="Visibility (km)",
        ge=0.0
    )
    Tdewpoint: float = Field(
        ...,
        description="Dew point temperature (°C)",
        ge=-50.0,
        le=50.0
    )
    rv1: float = Field(
        ...,
        description="Extraterrestrial radiation - horizontal component (Wh/m²)",
        ge=0.0
    )
    hour: float = Field(
        ...,
        description="Hour of day (0-23)",
        ge=0.0,
        le=23.0
    )
    hour_sin: float = Field(
        ...,
        description="Sine-encoded cyclical hour for time-based patterns",
        ge=-1.0,
        le=1.0
    )
    hour_cos: float = Field(
        ...,
        description="Cosine-encoded cyclical hour for time-based patterns",
        ge=-1.0,
        le=1.0
    )


class PredictResponse(BaseModel):
    """
    Response body for POST /predict endpoint.
    
    Contains predicted energy consumption with derived metrics.
    """
    
    energy_wh: float = Field(
        ...,
        description="Predicted energy consumption in Watt-hours (Wh)"
    )
    cost_inr: float = Field(
        ...,
        description="Estimated energy cost in Indian Rupees (INR) at 5 INR/kWh"
    )
    co2_kg: float = Field(
        ...,
        description="Estimated CO2 emissions in kilograms at 0.82 kg CO2/kWh"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "energy_wh": 45.3,
                "cost_inr": 0.226,
                "co2_kg": 0.037
            }
        }


class InsightsResponse(BaseModel):
    """
    Response body for GET /insights endpoint.
    
    Provides key drivers of energy consumption and their descriptions.
    """
    
    top_drivers: List[str] = Field(
        ...,
        description="List of top feature drivers affecting energy consumption"
    )
    descriptions: List[str] = Field(
        ...,
        description="Descriptions explaining the impact of each driver"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "top_drivers": ["RH_6", "Visibility", "Tdewpoint"],
                "descriptions": [
                    "Outdoor humidity affects equipment operation",
                    "Visibility correlates with cloud cover and solar gains",
                    "Dew point temperature influences HVAC energy"
                ]
            }
        }


class StatsResponse(BaseModel):
    """
    Response body for GET /stats endpoint.
    
    Provides metadata about the deployed model and its configuration.
    """
    
    model_type: str = Field(
        ...,
        description="Type of machine learning model used for predictions"
    )
    features_used: List[str] = Field(
        ...,
        description="List of input features used by the model"
    )
    co2_factor: float = Field(
        ...,
        description="CO2 emissions factor in kg per kWh"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "model_type": "Ridge Regression (α=1.0)",
                "features_used": ["RH_6", "Windspeed", "Visibility", "Tdewpoint", "rv1", "hour", "hour_sin", "hour_cos"],
                "co2_factor": 0.82
            }
        }
