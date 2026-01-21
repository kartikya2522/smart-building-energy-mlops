**Live App:** https://smart-building-energy-ml.streamlit.app


# Smart Building Energy Consumption Prediction 

An end-to-end machine learning project that predicts smart building energy consumption using IoT sensor data and quantifies cost and CO₂ impact to support sustainable decision-making.

---

## Problem Statement
Buildings consume a large portion of electricity, leading to high energy costs and carbon emissions.  
This project predicts hourly energy consumption using sensor data and provides insights into sustainability impact.

---

## Dataset
- UCI Appliances Energy Prediction Dataset
- ~19,000 records of IoT sensor data
- Target: `Appliances` (energy consumption in Wh)

---

## Approach
- Feature engineering with time-based encoding and safe lag features
- VIF-based feature selection to reduce multicollinearity
- Models:
  - Linear Regression (baseline)
  - Ridge Regression (final)
- Metrics: RMSE, R²
- Experiment tracking using MLflow

---

## Results
- Ridge Regression achieved R² ≈ 0.75–0.80
- Outdoor temperature, humidity, and time-of-day were key drivers of energy usage

---

## Sustainability Impact
- Converts predicted energy (Wh → kWh)
- Cost estimation (₹6 / kWh)
- CO₂ emissions using India grid factor (0.82 kg CO₂ / kWh)

---

## Deployment
- Streamlit-based interactive dashboard
- User inputs environmental conditions
- Outputs predicted energy, cost, and CO₂ impact

---

## Tech Stack
Python, pandas, scikit-learn, MLflow, Streamlit, Plotly, GitHub

---

## How to Run
```bash
pip install -r requirements.txt
python src/models/train.py
streamlit run app.py
