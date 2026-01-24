# Smart Building Energy Prediction - FastAPI Backend

A production-quality FastAPI backend that exposes the trained Ridge Regression ML model for real-time energy consumption predictions.

## 📋 Overview

This backend provides three REST endpoints:

- **POST /predict** - Predict building energy consumption based on environmental features
- **GET /insights** - Get information about top drivers of energy consumption  
- **GET /stats** - Get model metadata and configuration

The backend reuses the existing trained Ridge Regression model from MLflow artifacts and does not reimplement any ML logic.

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── __init__.py           # Package initialization
│   ├── main.py               # FastAPI app & routing
│   ├── schemas.py            # Pydantic request/response models
│   ├── predict.py            # Prediction logic & model loading
│   ├── insights.py           # GET /insights endpoint
│   └── stats.py              # GET /stats endpoint
└── requirements.txt          # Python dependencies
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Run the Server

```bash
cd app
python main.py
```

The API will be available at: **http://localhost:8000**

Interactive API documentation: **http://localhost:8000/docs**

### 3. Test Endpoints

#### Health Check
```bash
curl http://localhost:8000/
```

#### Make a Prediction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "RH_6": 50,
    "Windspeed": 5.0,
    "Visibility": 40,
    "Tdewpoint": 5,
    "rv1": 100,
    "hour": 14,
    "hour_sin": 0.95,
    "hour_cos": -0.309
  }'
```

Expected response:
```json
{
  "energy_wh": 45.3,
  "cost_inr": 0.226,
  "co2_kg": 0.037
}
```

#### Get Insights
```bash
curl http://localhost:8000/insights
```

#### Get Stats
```bash
curl http://localhost:8000/stats
```

## 📊 API Endpoints

### POST /predict

**Purpose**: Make energy consumption predictions

**Request Body**:
```json
{
  "RH_6": float,        // Relative humidity (%) - required, 0-100
  "Windspeed": float,   // Wind speed (m/s) - required, ≥0
  "Visibility": float,  // Visibility (km) - required, ≥0
  "Tdewpoint": float,   // Dew point temperature (°C) - required, -50 to 50
  "rv1": float,         // Solar radiation (Wh/m²) - required, ≥0
  "hour": float,        // Hour of day - required, 0-23
  "hour_sin": float,    // Sine-encoded hour - required, -1 to 1
  "hour_cos": float     // Cosine-encoded hour - required, -1 to 1
}
```

**Response**:
```json
{
  "energy_wh": float,   // Predicted energy consumption (Wh)
  "cost_inr": float,    // Estimated cost (INR at 5 INR/kWh)
  "co2_kg": float       // CO2 emissions (kg at 0.82 kg CO2/kWh)
}
```

**Status Codes**:
- `200 OK` - Prediction successful
- `422 Unprocessable Entity` - Invalid input features
- `500 Internal Server Error` - Model or server error

---

### GET /insights

**Purpose**: Get information about top drivers of energy consumption

**Response**:
```json
{
  "top_drivers": [
    "RH_6",
    "Visibility", 
    "Tdewpoint",
    "rv1",
    "Windspeed"
  ],
  "descriptions": [
    "Outdoor humidity (RH_6) directly affects HVAC equipment operation...",
    "Visibility correlates with cloud cover; lower visibility means...",
    "Dew point temperature indicates atmospheric moisture...",
    "Solar radiation (rv1) directly influences building cooling...",
    "Wind speed affects heat transfer through the building envelope..."
  ]
}
```

---

### GET /stats

**Purpose**: Get model metadata and configuration

**Response**:
```json
{
  "model_type": "Ridge Regression (α=1.0)",
  "features_used": [
    "RH_6",
    "Windspeed",
    "Visibility",
    "Tdewpoint",
    "rv1",
    "hour",
    "hour_sin",
    "hour_cos"
  ],
  "co2_factor": 0.82
}
```

## 🔧 Configuration

### Constants

The backend uses the following constants for calculations:

| Constant | Value | Purpose |
|----------|-------|---------|
| `COST_FACTOR_INR_PER_KWH` | 5.0 | Convert energy to cost |
| `CO2_FACTOR_KG_PER_KWH` | 0.82 | Convert energy to CO2 emissions |

These can be modified in `app/predict.py` if needed.

### Model Path

The backend loads the trained Ridge Regression model from:
```
mlruns/1/models/m-ddcc4d73d7fa47349323f0cf17eb32fb/artifacts/model.pkl
```

To use a different model, update the `MODEL_PATH` variable in `app/predict.py`.

## 📝 Feature Engineering

The model expects features in this exact order:
1. **RH_6** - Outdoor relative humidity (%)
2. **Windspeed** - Wind speed (m/s)
3. **Visibility** - Visibility (km)
4. **Tdewpoint** - Dew point temperature (°C)
5. **rv1** - Solar radiation (Wh/m²)
6. **hour** - Hour of day (0-23)
7. **hour_sin** - Sine-encoded hour cyclical feature
8. **hour_cos** - Cosine-encoded hour cyclical feature

These features are derived from the original energy data through:
- Time-based feature extraction (hour, hour_sin, hour_cos)
- Feature engineering pipeline (`src/features/build_features.py`)
- VIF-based multicollinearity removal
- Ridge Regression training with α=1.0

## 🔐 Security & Constraints

The backend is built with the following constraints:
- ✅ **No authentication** - Open endpoints for simplicity
- ✅ **No database** - Stateless predictions only
- ✅ **No ML modifications** - Uses pre-trained model as-is
- ✅ **No dummy data** - All predictions are real model outputs
- ✅ **Input validation** - Pydantic automatic validation
- ✅ **CORS enabled** - Allows frontend requests

## 📚 Model Information

- **Model Type**: Ridge Regression with L2 regularization
- **Alpha (λ)**: 1.0
- **Training Samples**: 11,532
- **Test Samples**: 2,883
- **Features**: 8
- **Target**: Appliances energy (Wh)

### Model Performance

| Metric | Training | Test |
|--------|----------|------|
| RMSE | ~49.3 Wh | ~56.2 Wh |
| R² | ~0.38 | ~0.38 |

## 🚨 Error Handling

The backend includes comprehensive error handling:

| Error | Status | Response |
|-------|--------|----------|
| Invalid input | 422 | Pydantic validation error details |
| Model not loaded | 500 | "Model not loaded. Cannot make predictions." |
| Prediction failure | 500 | Detailed exception message |
| Server error | 500 | Generic error message |

All errors are logged for debugging.

## 📦 Dependencies

See `backend/requirements.txt` for version specifications:
- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **pydantic** - Data validation
- **pandas** - Data manipulation
- **numpy** - Numerical operations
- **scikit-learn** - Model loading
- **joblib** - Model serialization

## 🧪 Testing

Run a quick prediction test:

```bash
python -c "
from app.predict import get_predictor
from app.schemas import PredictRequest

predictor = get_predictor()
req = PredictRequest(
    RH_6=50, Windspeed=5, Visibility=40, 
    Tdewpoint=5, rv1=100, hour=14, 
    hour_sin=0.95, hour_cos=-0.309
)
result = predictor.predict(req)
print(f'Energy: {result.energy_wh} Wh')
print(f'Cost: {result.cost_inr} INR')
print(f'CO2: {result.co2_kg} kg')
"
```

## 📖 Documentation

Interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔍 Logging

All requests, predictions, and errors are logged to the console with timestamps and log levels. Adjust the logging level in `app/main.py` if needed.

## 🤝 Integration Notes

### For Frontend Integration
1. Point your frontend requests to `http://localhost:8000/predict`
2. Send POST requests with the required features
3. Parse the JSON response containing energy, cost, and CO2

### For Production Deployment
1. Replace `reload=True` with `reload=False` in `main.py`
2. Use a production ASGI server like Gunicorn + Uvicorn
3. Add authentication if needed
4. Configure CORS more restrictively
5. Add request rate limiting and monitoring
6. Enable HTTPS/TLS

## 📝 Notes

- **Model Reuse**: The backend loads and uses the existing trained model from MLflow artifacts without any modifications
- **Stateless**: Each prediction is independent; no state is maintained between requests
- **Real Predictions**: All outputs are generated by the trained Ridge Regression model, not dummy values
- **Cost Calculation**: Based on 5 INR/kWh (configurable)
- **CO2 Calculation**: Based on 0.82 kg CO2/kWh (configurable)

## 🐛 Troubleshooting

### Model not found error
- Ensure MLflow artifacts are present at the expected path
- Check that `models/feature_names.json` exists
- Verify the project root path is correctly set

### Port 8000 already in use
```bash
# Use a different port
cd app && python main.py --port 8001
```

### Import errors
- Ensure you're running from the `backend/app` directory
- Verify all dependencies are installed: `pip install -r ../requirements.txt`
- Check PYTHONPATH includes the backend directory

## 📞 Support

For issues or questions:
1. Check the error logs for detailed messages
2. Review the interactive API docs at `/docs`
3. Verify input features match the exact schema
4. Ensure the trained model file exists at the configured path
