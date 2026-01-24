# Smart Building Energy Prediction Backend - Configuration Guide

## Environment Variables (Optional)

You can configure the backend behavior using environment variables:

### Server Configuration
- `HOST`: Server bind address (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `RELOAD`: Enable auto-reload (default: false)
- `WORKERS`: Number of worker processes (default: 1)

### Model Configuration
- `MODEL_PATH`: Path to trained model (default: mlruns/.../model.pkl)
- `FEATURE_NAMES_PATH`: Path to feature names JSON (default: models/feature_names.json)

### Calculation Constants
- `COST_FACTOR_INR_PER_KWH`: Cost per kWh in INR (default: 5.0)
- `CO2_FACTOR_KG_PER_KWH`: CO2 emissions per kWh (default: 0.82)

### CORS Configuration
- `CORS_ORIGINS`: Allowed origins (default: *)
- `CORS_CREDENTIALS`: Allow credentials (default: true)

### Logging
- `LOG_LEVEL`: Logging level (default: INFO)

## Example .env File

```bash
# Server
HOST=0.0.0.0
PORT=8000
RELOAD=false
WORKERS=1

# Model
MODEL_PATH=mlruns/1/models/m-ddcc4d73d7fa47349323f0cf17eb32fb/artifacts/model.pkl
FEATURE_NAMES_PATH=models/feature_names.json

# Constants
COST_FACTOR_INR_PER_KWH=5.0
CO2_FACTOR_KG_PER_KWH=0.82

# Logging
LOG_LEVEL=INFO
```

## Quick Start Commands

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Backend
```bash
# Default (localhost:8000)
python run.py

# Custom port
python run.py --port 8001

# With auto-reload (development)
python run.py --reload

# Multiple workers (production)
python run.py --workers 4
```

### 3. Run Tests
```bash
# In another terminal, with server running
python test.py

# Test against custom endpoint
python test.py --endpoint http://localhost:8001
```

### 4. View API Documentation
Open in browser:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Production Deployment

### Using Gunicorn + Uvicorn

```bash
pip install gunicorn

gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

### Using Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "run.py", "--host", "0.0.0.0", "--port", "8000"]
```

## Testing Direct Model Loading

You can test the model loading without the HTTP server:

```python
from app.predict import get_predictor
from app.schemas import PredictRequest

predictor = get_predictor()
req = PredictRequest(
    RH_6=50,
    Windspeed=5,
    Visibility=40,
    Tdewpoint=5,
    rv1=100,
    hour=14,
    hour_sin=0.95,
    hour_cos=-0.309
)
result = predictor.predict(req)
print(f"Energy: {result.energy_wh} Wh")
```

## Troubleshooting

### Model Loading Fails
- Check that MLflow artifacts exist at the configured path
- Verify `models/feature_names.json` exists
- Ensure joblib and scikit-learn are installed

### Port Already in Use
- Use `--port` flag with a different port
- Or kill the process: `lsof -ti:8000 | xargs kill -9` (Linux/Mac)

### Import Errors
- Ensure you're in the backend directory
- Run: `pip install -r requirements.txt`
- Check PYTHONPATH includes the project root

### Slow Predictions
- This is normal for the first prediction (model loading)
- Subsequent predictions should be < 1ms
- Consider using multiple workers for production

## API Response Examples

### Successful Prediction
```json
{
  "energy_wh": 45.3,
  "cost_inr": 0.226,
  "co2_kg": 0.037
}
```

### Insights
```json
{
  "top_drivers": ["RH_6", "Visibility", "Tdewpoint"],
  "descriptions": ["...", "...", "..."]
}
```

### Stats
```json
{
  "model_type": "Ridge Regression (α=1.0)",
  "features_used": ["RH_6", "Windspeed", ...],
  "co2_factor": 0.82
}
```

## Support & Documentation

- Interactive API docs: http://localhost:8000/docs
- Full README: [backend/README.md](README.md)
- Training script: [src/models/train.py](../src/models/train.py)
- Feature engineering: [src/features/build_features.py](../src/features/build_features.py)
