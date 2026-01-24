# Backend API Integration Guide for Frontend

This guide explains how to integrate the FastAPI backend with your frontend application.

## Quick Start

The backend exposes a simple REST API with three main endpoints:

```
POST   /predict   - Get energy predictions
GET    /insights  - Get top drivers of energy consumption
GET    /stats     - Get model metadata
```

## 1. Making Predictions

### HTTP Request

```http
POST http://localhost:8000/predict
Content-Type: application/json

{
  "RH_6": 50.0,
  "Windspeed": 5.0,
  "Visibility": 40.0,
  "Tdewpoint": 5.0,
  "rv1": 100.0,
  "hour": 14.0,
  "hour_sin": 0.951,
  "hour_cos": -0.309
}
```

### JavaScript/Fetch Example

```javascript
async function getPrediction() {
  const features = {
    RH_6: 50.0,
    Windspeed: 5.0,
    Visibility: 40.0,
    Tdewpoint: 5.0,
    rv1: 100.0,
    hour: 14.0,
    hour_sin: 0.951,
    hour_cos: -0.309
  };

  try {
    const response = await fetch('http://localhost:8000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(features)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const prediction = await response.json();
    console.log('Energy:', prediction.energy_wh, 'Wh');
    console.log('Cost:', prediction.cost_inr, 'INR');
    console.log('CO2:', prediction.co2_kg, 'kg');

    return prediction;
  } catch (error) {
    console.error('Prediction failed:', error);
  }
}
```

### Python Example

```python
import requests

features = {
    "RH_6": 50.0,
    "Windspeed": 5.0,
    "Visibility": 40.0,
    "Tdewpoint": 5.0,
    "rv1": 100.0,
    "hour": 14.0,
    "hour_sin": 0.951,
    "hour_cos": -0.309
}

response = requests.post(
    'http://localhost:8000/predict',
    json=features
)

if response.status_code == 200:
    prediction = response.json()
    print(f"Energy: {prediction['energy_wh']} Wh")
    print(f"Cost: {prediction['cost_inr']} INR")
    print(f"CO2: {prediction['co2_kg']} kg")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

### cURL Example

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "RH_6": 50.0,
    "Windspeed": 5.0,
    "Visibility": 40.0,
    "Tdewpoint": 5.0,
    "rv1": 100.0,
    "hour": 14.0,
    "hour_sin": 0.951,
    "hour_cos": -0.309
  }'
```

## 2. Response Format

### Successful Response (200 OK)

```json
{
  "energy_wh": 45.3,
  "cost_inr": 0.226,
  "co2_kg": 0.037
}
```

### Error Response (422 Unprocessable Entity)

```json
{
  "detail": [
    {
      "type": "float_parsing",
      "loc": ["body", "RH_6"],
      "msg": "Input should be a valid number",
      "input": "invalid"
    }
  ]
}
```

## 3. Getting Insights

### HTTP Request

```http
GET http://localhost:8000/insights
```

### JavaScript Example

```javascript
async function getInsights() {
  try {
    const response = await fetch('http://localhost:8000/insights');
    const insights = await response.json();
    
    console.log('Top Drivers:', insights.top_drivers);
    console.log('Descriptions:', insights.descriptions);
    
    return insights;
  } catch (error) {
    console.error('Failed to get insights:', error);
  }
}
```

### Response

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

## 4. Getting Model Statistics

### HTTP Request

```http
GET http://localhost:8000/stats
```

### JavaScript Example

```javascript
async function getStats() {
  try {
    const response = await fetch('http://localhost:8000/stats');
    const stats = await response.json();
    
    console.log('Model Type:', stats.model_type);
    console.log('Features:', stats.features_used);
    console.log('CO2 Factor:', stats.co2_factor);
    
    return stats;
  } catch (error) {
    console.error('Failed to get stats:', error);
  }
}
```

### Response

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

## 5. Feature Input Validation

The backend automatically validates input features:

| Feature | Type | Range | Unit | Description |
|---------|------|-------|------|-------------|
| RH_6 | float | 0-100 | % | Outdoor relative humidity |
| Windspeed | float | ≥0 | m/s | Wind speed |
| Visibility | float | ≥0 | km | Visibility distance |
| Tdewpoint | float | -50 to 50 | °C | Dew point temperature |
| rv1 | float | ≥0 | Wh/m² | Solar radiation |
| hour | float | 0-23 | - | Hour of day (0=midnight) |
| hour_sin | float | -1 to 1 | - | sin(2π*hour/24) |
| hour_cos | float | -1 to 1 | - | cos(2π*hour/24) |

### Validation Examples

```javascript
// Invalid - RH_6 out of range
{
  "RH_6": 150,  // ✗ Must be 0-100
  "Windspeed": 5.0,
  ...
}

// Invalid - hour out of range
{
  "RH_6": 50,
  "Windspeed": 5.0,
  ...
  "hour": 25,  // ✗ Must be 0-23
  ...
}

// Invalid - Missing required field
{
  "RH_6": 50,
  "Windspeed": 5.0,
  // Missing other required fields
}
```

## 6. Common Integration Patterns

### React Component Example

```jsx
import React, { useState } from 'react';

function EnergyPredictor() {
  const [features, setFeatures] = useState({
    RH_6: 50,
    Windspeed: 5,
    Visibility: 40,
    Tdewpoint: 5,
    rv1: 100,
    hour: 14,
    hour_sin: 0.951,
    hour_cos: -0.309
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePredict = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(features)
      });

      if (!response.ok) throw new Error('Prediction failed');
      
      const data = await response.json();
      setPrediction(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input
        type="number"
        placeholder="RH_6"
        value={features.RH_6}
        onChange={(e) => setFeatures({
          ...features,
          RH_6: parseFloat(e.target.value)
        })}
      />
      {/* More input fields... */}
      
      <button onClick={handlePredict} disabled={loading}>
        {loading ? 'Predicting...' : 'Predict'}
      </button>

      {error && <div className="error">{error}</div>}
      
      {prediction && (
        <div className="results">
          <p>Energy: {prediction.energy_wh} Wh</p>
          <p>Cost: {prediction.cost_inr} INR</p>
          <p>CO2: {prediction.co2_kg} kg</p>
        </div>
      )}
    </div>
  );
}

export default EnergyPredictor;
```

## 7. Error Handling

### Common Errors

| Status | Error | Solution |
|--------|-------|----------|
| 422 | Invalid input | Check feature values match expected types and ranges |
| 500 | Model not loaded | Ensure backend started correctly, check logs |
| 500 | Prediction failed | Check model files exist, try restarting backend |
| Connection refused | Backend not running | Start backend with `python run.py` |

### Robust Error Handling

```javascript
async function predictWithErrorHandling(features) {
  try {
    const response = await fetch('http://localhost:8000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(features),
      timeout: 5000
    });

    if (response.status === 422) {
      const errorData = await response.json();
      throw new Error(`Validation error: ${JSON.stringify(errorData)}`);
    }

    if (response.status === 500) {
      throw new Error('Server error: Model unavailable');
    }

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    if (error.name === 'TypeError') {
      console.error('Connection refused: Backend not running');
    } else {
      console.error('Prediction error:', error.message);
    }
    throw error;
  }
}
```

## 8. CORS Configuration

The backend includes CORS support enabled for all origins by default. If you need to restrict origins for production:

Edit `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.com"],  # Restrict to specific domain
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## 9. Performance Notes

- First prediction may take 1-2 seconds (model loading)
- Subsequent predictions: < 1ms
- Optimal batch size: 1 request at a time (model designed for single instances)
- The backend is stateless; safe to reload/restart anytime

## 10. API Documentation

Full interactive API documentation available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide:
- Complete endpoint documentation
- Input/output schemas
- Example requests and responses
- Try it out interface

## Troubleshooting Integration

### "Failed to fetch" Error
- Check CORS is enabled on backend
- Verify correct backend URL/port
- Check browser console for specific errors

### Invalid Response
- Ensure Content-Type is application/json
- Check feature names spell exactly (case-sensitive)
- Validate all required fields are present

### Slow Responses
- First prediction slower due to model loading
- Verify network connectivity
- Check backend logs for slow operations

### Features Out of Range
- Use realistic environmental values
- hour should be 0-23
- RH_6 should be 0-100
- Calculate hour_sin/hour_cos correctly: sin/cos(2π*hour/24)

## Next Steps

1. Start the backend: `cd backend && python run.py`
2. Test with cURL or the interactive docs
3. Integrate endpoints into your frontend
4. Handle errors gracefully in your application
5. Deploy to production when ready

Need help? Check the [backend README](README.md) or [CONFIG guide](CONFIG.md).
