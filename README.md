# Smart Building Energy Consumption Prediction

**Live App:** https://smart-building-energy-ml.streamlit.app

An end-to-end ML project predicting hourly building energy consumption from IoT sensor data, with cost and sustainability impact analysis.

---

## Problem Statement

Buildings account for ~28% of global energy-related CO₂ emissions. Accurate energy prediction enables:
- Proactive demand management
- Cost optimization  
- Sustainability tracking

This project predicts hourly energy consumption from environmental sensors and quantifies financial and environmental impact.

---

## Dataset

- **Source:** UCI Machine Learning Repository (Appliances Energy Prediction)
- **Size:** ~19,000 hourly records
- **Target:** Appliances (Wh)
- **Features:** 8 environmental sensors (temperature, humidity, pressure, visibility, wind speed)

---

## Approach

### 1. Feature Engineering
- **Time-based features:** Cyclical hour encoding (sin/cos) to capture daily patterns
- **Lag features:** 1-hour lagged temperature and humidity
- **VIF analysis:** Removed multicollinear features (>5 threshold)
- **Final features:** 8 selected features with minimal multicollinearity

### 2. Train-Test Split
- **Time-based:** First 80% for training, last 20% for testing
- **Prevents temporal leakage:** Respects temporal ordering of data

### 3. Models
- **Linear Regression:** Baseline model
- **Ridge Regression (α=1.0):** Final model with L2 regularization

### 4. Experiment Tracking
- MLflow logs all runs with hyperparameters and metrics
- Centralized comparison of model performance

---

## Results

| Metric | Train | Test |
|--------|-------|------|
| **RMSE** | 47.2 Wh | 52.1 Wh |
| **R²** | 0.78 | 0.75 |

**Key Insights:**
- Outdoor temperature is the strongest predictor of energy usage
- Humidity and time-of-day significantly impact consumption
- Ridge regularization prevents overfitting (minimal train-test gap)

---

## Project Structure

```
smart-building-energy-mlops/
├── app.py                        # Streamlit dashboard
├── src/
│   ├── models/
│   │   ├── train.py             # Model training pipeline
│   │   └── evaluate.py          # Model evaluation & interpretability
│   └── features/
│       └── build_features.py    # Feature engineering
├── models/
│   ├── ridge_model.pkl          # Trained Ridge model
│   └── feature_names.json       # Feature metadata
├── data/
│   └── raw/
│       └── energydata_complete.csv
├── notebooks/
│   └── 01_eda.ipynb             # Exploratory data analysis
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Container deployment
└── .streamlit/
    └── config.toml              # Streamlit UI configuration
```

---

## Quick Start

### 1. Local Setup
```bash
git clone https://github.com/kartikya2522/smart-building-energy-mlops.git
cd smart-building-energy-mlops

pip install -r requirements.txt

# Verify dependencies
python verify_dependencies.py
```

### 2. Training
```bash
# Train model and track experiments
python src/models/train.py

# View experiment results
mlflow ui  # Visit http://localhost:5000
```

### 3. Dashboard
```bash
# Run interactive Streamlit app
streamlit run app.py
# Opens at http://localhost:8501
```

---

## Deployment

### Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Visit https://share.streamlit.io
3. Connect repository and select main branch
4. Set main file to `app.py`
5. Click Deploy

**Troubleshooting:** If deployment fails, verify `requirements.txt` is in root directory and check Streamlit Cloud logs.

### Docker
```bash
docker build -t smart-building-app .
docker run -p 8501:8501 smart-building-app
```

---

## Features

### Interactive Dashboard
- **Sidebar Controls:** Adjust weather conditions and time-of-day
- **Real-time Predictions:** Updates instantly as you change inputs
- **24-Hour Profile:** Energy prediction across all hours
- **KPI Metrics:** Energy (Wh), Cost (₹), CO₂ emissions (kg)
- **Sustainability Impact:** Daily/monthly projections and environmental insights

### Model Evaluation
- Feature importance visualization
- SHAP interpretability analysis
- Performance metrics (RMSE, R², MAE)
- Overfitting detection

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Data Processing | pandas, NumPy |
| ML Framework | scikit-learn |
| Experiment Tracking | MLflow |
| Web App | Streamlit |
| Visualization | Plotly |
| Deployment | Docker, Streamlit Cloud |
| Version Control | Git/GitHub |

---

## Dependencies

```
streamlit>=1.28.0
plotly>=5.17.0
pandas>=2.0.0
numpy>=2.0.0
scikit-learn>=1.7.0
joblib>=1.5.0
```

---

## Usage Example

```python
import joblib
import pandas as pd
import numpy as np
import json

# Load model and features
model = joblib.load("models/ridge_model.pkl")
with open("models/feature_names.json") as f:
    feature_names = json.load(f)

# Create prediction
features = np.array([65, 7.5, 10.5, 8.0, 50, 14, -0.2, 0.9]).reshape(1, -1)
features_df = pd.DataFrame(features, columns=feature_names)
prediction = model.predict(features_df)[0]

print(f"Predicted energy: {prediction:.1f} Wh")
```

---

## Performance

| Metric | Value |
|--------|-------|
| Model Load Time | <100 ms |
| Prediction Time | <50 ms |
| App Startup | 2-3 seconds |
| Memory Usage | ~150 MB |

---

## Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/name`)
3. Commit changes (`git commit -m "Add feature"`)
4. Push branch (`git push origin feature/name`)
5. Open Pull Request

---

## License

MIT License

---

## Future Enhancements

- Time series models (LSTM, Prophet)
- Hyperparameter optimization (Optuna)
- Batch prediction API
- Real-time data ingestion
- Anomaly detection

---

**Live App:** https://smart-building-energy-ml.streamlit.app
