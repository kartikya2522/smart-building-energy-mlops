# Model Evaluation & Interpretability Guide

## Overview

The `evaluate.py` script provides comprehensive model evaluation and feature importance analysis for the trained Ridge Regression model used in smart building energy prediction. It demonstrates best practices for linear model interpretability and provides actionable insights for building operations teams.

## Key Features

### 1. **Model Evaluation**
- Loads the pre-trained Ridge model from `models/ridge_model.pkl`
- Evaluates performance on training and test sets
- Computes RMSE, MAE, and R² metrics
- Detects potential overfitting

### 2. **Feature Importance Analysis**
- Extracts model coefficients and associates them with feature names
- Identifies features that increase/decrease energy consumption
- Ranks features by absolute coefficient magnitude
- Creates interpretable bar plots

### 3. **Visualizations**
- **Feature Importance Plot** (`docs/feature_importance.png`)
  - Top 10 features by absolute coefficient magnitude
  - Color-coded by impact direction (green = increase, red = decrease)
  - Coefficient values displayed on bars
  
- **SHAP Summary Plot** (`docs/shap_summary.png`) - Optional
  - Advanced interpretability using game theory
  - Considers feature interactions
  - Provides per-sample explanations

### 4. **Textual Insights**
- Clear explanations of energy usage drivers
- Actionable recommendations for building operations
- Model reliability assessment
- Interpretation of positive and negative coefficients

## Usage

### Basic Usage

```bash
cd d:\smart-building-energy-mlops
python src/models/evaluate.py
```

### Output

The script generates the following outputs:

1. **Console Output**
   - Model loading confirmation
   - Feature engineering summary
   - Train-test split details
   - Performance metrics (RMSE, MAE, R²)
   - Top 10 feature importance ranking
   - Energy usage insights and recommendations
   - SHAP analysis status

2. **Saved Visualizations**
   - `docs/feature_importance.png` - Feature importance bar plot
   - `docs/shap_summary.png` - SHAP summary plot (if shap library is installed)

## Understanding the Outputs

### Feature Importance Plot

The horizontal bar plot shows:

- **X-axis**: Coefficient value (positive/negative)
- **Y-axis**: Feature names
- **Green bars**: Positive coefficients → increase energy consumption
- **Red bars**: Negative coefficients → decrease energy consumption
- **Bar length**: Magnitude of impact on model predictions

**Example Interpretation:**
- If `T_out` (outdoor temperature) has a large positive coefficient, it means higher outdoor temperature increases predicted energy usage
- If `RH_out_lag1` (lagged humidity) has a negative coefficient, it means historical humidity patterns help reduce energy predictions

### Performance Metrics

- **RMSE (Root Mean Squared Error)**
  - Measured in Wh (watt-hours)
  - Lower is better
  - Indicates average prediction error magnitude

- **R² Score**
  - Ranges from 0 to 1
  - Represents proportion of variance explained by the model
  - > 0.8: Strong model
  - 0.6-0.8: Good model
  - < 0.6: Moderate model requiring further investigation

- **MAE (Mean Absolute Error)**
  - Average absolute difference between predictions and actual values
  - Same units as target variable (Wh)

### Overfitting Analysis

The script automatically detects overfitting by comparing train/test performance:
- If test R² is significantly lower than train R², the model may be overfitting
- Ridge regularization helps prevent this through coefficient shrinkage

## Why Interpretability Matters for Linear Models

### 1. **Transparency**
Linear models are inherently interpretable—each feature has a single coefficient representing its impact. Unlike neural networks or tree ensembles, there's no "black box."

### 2. **Stakeholder Communication**
Building operators and facility managers can understand *why* the model predicts certain energy levels, enabling trust and adoption.

### 3. **Regulatory Compliance**
Many regulations (e.g., building energy codes, GDPR) require explainable AI decisions. Linear models naturally satisfy these requirements.

### 4. **Debugging and Validation**
If predictions seem wrong, you can directly inspect which features contributed and investigate data quality or feature engineering issues.

### 5. **Decision Making**
Feature importance guides operational decisions:
- Which factors most strongly affect energy usage?
- Which parameters can be optimized for energy savings?
- Where should monitoring focus?

## Workflow

```
Load Model
    ↓
Load & Engineer Features (same pipeline as training)
    ↓
Time-based Train-Test Split (80% train, 20% test)
    ↓
Extract Model Coefficients
    ↓
Evaluate Performance (RMSE, R², MAE)
    ↓
Generate Visualizations
    ↓
Generate Textual Insights
    ↓
(Optional) SHAP Analysis
    ↓
Save Outputs to docs/
```

## Sample Output Interpretation

### Console Output Example

```
TOP 10 MOST IMPORTANT FEATURES
Feature              Coefficient  Abs_Coefficient
T_out                    0.0456           0.0456
RH_out_lag1             -0.0234           0.0234
hour_sin                 0.0189           0.0189
T_in                     0.0156           0.0156
hour_cos                 0.0145           0.0145
...

FEATURES THAT INCREASE ENERGY CONSUMPTION:
📈 T_out (coefficient: 0.0456)
   → Higher temperature increases energy use (likely cooling/HVAC demand)

FEATURES THAT DECREASE ENERGY CONSUMPTION:
📉 RH_out_lag1 (coefficient: -0.0234)
   → Lower humidity reduces energy use (less dehumidification needed)

MODEL PERFORMANCE:
Test Set R² Score: 0.8234
  → Model explains 82.34% of variance in energy consumption
Test Set RMSE: 12.5634 Wh
  → Average prediction error: 12.56 Wh
```

### Actionable Insights

From the above example, we can conclude:

1. **Primary Driver**: Outdoor temperature (`T_out`) has the strongest impact
   - Action: Monitor outdoor temperature forecasts for predictive energy management
   
2. **Secondary Factor**: Historical humidity affects energy patterns
   - Action: Consider humidity trends when optimizing HVAC settings

3. **Model Reliability**: R² of 0.82 indicates strong predictive power
   - Action: Use model predictions for operational decisions with confidence

## Installation Requirements

### Core Requirements
```bash
pip install numpy pandas scikit-learn joblib matplotlib seaborn
```

### Optional: SHAP Analysis
```bash
pip install shap
```

If shap is not installed, the script will skip SHAP analysis and continue with other evaluations.

## File Structure

```
smart-building-energy-mlops/
├── data/
│   └── raw/
│       └── energydata_complete.csv       ← Input data
├── docs/                                  ← Output directory (created if needed)
│   ├── feature_importance.png             ← Feature importance plot
│   └── shap_summary.png                   ← SHAP summary plot (optional)
├── models/
│   └── ridge_model.pkl                    ← Trained model
└── src/
    ├── features/
    │   └── build_features.py              ← Feature engineering pipeline
    └── models/
        ├── train.py                       ← Training script
        └── evaluate.py                    ← This evaluation script
```

## Advanced Usage

### Using evaluate.py in Custom Scripts

```python
from src.models.evaluate import (
    load_trained_model,
    load_and_engineer_features,
    time_based_split,
    extract_feature_importance,
    evaluate_model_performance
)

# Load model and data
model = load_trained_model('models/ridge_model.pkl')
X, y = load_and_engineer_features('data/raw/energydata_complete.csv')

# Custom analysis
X_train, X_test, y_train, y_test = time_based_split(X, y)
metrics = evaluate_model_performance(model, X_train, y_train, X_test, y_test)
importance_df = extract_feature_importance(model, X.columns.tolist())

# Your custom code here
print(importance_df.head(10))
```

## Troubleshooting

### Model File Not Found
- Ensure `models/ridge_model.pkl` exists (run training script first)
- Check the full path is correct

### Data File Not Found
- Ensure `data/raw/energydata_complete.csv` exists
- Verify file hasn't been moved or renamed

### SHAP Analysis Fails
- SHAP is optional; the script continues without it
- To enable SHAP: `pip install shap`

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that you're running from the project root directory

## Performance Benchmarks

Typical Ridge model performance on energy data:

| Metric | Typical Range |
|--------|--------------|
| R² Score | 0.75 - 0.90 |
| RMSE | 8 - 20 Wh |
| MAE | 6 - 15 Wh |

Values depend on data quality, feature engineering, and hyperparameters.

## Next Steps

After evaluation, you can:

1. **Improve the Model**
   - Adjust Ridge alpha parameter in train.py
   - Add/remove features in build_features.py
   - Experiment with different algorithms

2. **Deploy for Operations**
   - Use the model for real-time energy predictions
   - Implement energy optimization strategies based on feature importance
   - Monitor model performance over time

3. **Deeper Analysis**
   - Perform SHAP analysis for individual predictions
   - Analyze prediction errors to identify failure modes
   - Study seasonal patterns in feature importance

## References

- Ridge Regression: https://scikit-learn.org/stable/modules/linear_model.html#ridge-regression
- SHAP: https://shap.readthedocs.io/
- Model Interpretability: https://christophm.github.io/interpretable-ml-book/
- Time Series Validation: https://robjhyndman.com/hyndsight/tscv/

---

**For questions or improvements, refer to the project documentation in README.md**
