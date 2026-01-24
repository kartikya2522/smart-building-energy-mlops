"""
FastAPI Application for Smart Building Energy Prediction

Main entry point for the energy prediction backend.

Exposes three endpoints:
- POST /predict: Make energy predictions based on environmental features
- GET /insights: Get information about top drivers of energy consumption
- GET /stats: Get model metadata and configuration

The application reuses the trained Ridge Regression model from MLflow artifacts
and does not reimplement any ML logic.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.schemas import PredictRequest, PredictResponse, InsightsResponse, StatsResponse
from app.predict import get_predictor
from app.insights import get_insights
from app.stats import get_stats

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Smart Building Energy Prediction API",
    description="Predicts building energy consumption using Ridge Regression model",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """
    Initialize resources on application startup.
    
    Loads the trained model and verifies it's ready for predictions.
    """
    try:
        predictor = get_predictor()
        logger.info("✓ Application startup: Model loaded successfully")
    except Exception as e:
        logger.error(f"✗ Application startup failed: {e}")
        raise


@app.get("/", tags=["Health"])
async def root():
    """
    Health check endpoint.
    
    Returns:
        dict: Application status and version information
    """
    return {
        "status": "healthy",
        "message": "Smart Building Energy Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "predict": "POST /predict",
            "insights": "GET /insights",
            "stats": "GET /stats",
            "docs": "/docs"
        }
    }


@app.post("/predict", response_model=PredictResponse, tags=["Predictions"])
async def predict(request: PredictRequest) -> PredictResponse:
    """
    Predict energy consumption based on environmental features.
    
    Makes a prediction using the trained Ridge Regression model.
    Returns predicted energy consumption in Wh, cost in INR, and CO2 emissions.
    
    Args:
        request: PredictRequest containing:
            - RH_6: Relative humidity (%)
            - Windspeed: Wind speed (m/s)
            - Visibility: Visibility (km)
            - Tdewpoint: Dew point temperature (°C)
            - rv1: Solar radiation (Wh/m²)
            - hour: Hour of day (0-23)
            - hour_sin: Sine-encoded hour
            - hour_cos: Cosine-encoded hour
    
    Returns:
        PredictResponse containing:
            - energy_wh: Predicted energy consumption (Wh)
            - cost_inr: Estimated cost (INR at 5 INR/kWh)
            - co2_kg: Estimated CO2 emissions (kg at 0.82 kg CO2/kWh)
    
    Raises:
        HTTPException: If prediction fails
    """
    try:
        predictor = get_predictor()
        prediction = predictor.predict(request)
        logger.info(f"Prediction successful: {prediction.energy_wh} Wh")
        return prediction
    
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@app.get("/insights", response_model=InsightsResponse, tags=["Analysis"])
async def insights() -> InsightsResponse:
    """
    Get insights about top drivers of energy consumption.
    
    Returns information about the most influential environmental factors
    affecting building energy consumption based on the trained model.
    
    Returns:
        InsightsResponse containing:
            - top_drivers: List of most influential features
            - descriptions: Explanations of each driver's impact
    """
    try:
        insights_data = get_insights()
        logger.info("Insights retrieved successfully")
        return insights_data
    
    except Exception as e:
        logger.error(f"Failed to retrieve insights: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve insights: {str(e)}"
        )


@app.get("/stats", response_model=StatsResponse, tags=["Analysis"])
async def stats() -> StatsResponse:
    """
    Get model statistics and configuration information.
    
    Returns metadata about the deployed model, features used, and
    constants used for cost and emissions calculations.
    
    Returns:
        StatsResponse containing:
            - model_type: Type and configuration of the model
            - features_used: List of input features
            - co2_factor: CO2 emissions factor (kg CO2/kWh)
    """
    try:
        stats_data = get_stats()
        logger.info("Stats retrieved successfully")
        return stats_data
    
    except Exception as e:
        logger.error(f"Failed to retrieve stats: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve stats: {str(e)}"
        )


@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle ValueError exceptions with appropriate HTTP response."""
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn
    
    # Run the FastAPI application
    # Usage: python main.py
    # API will be available at http://localhost:8000
    # Interactive docs available at http://localhost:8000/docs
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
