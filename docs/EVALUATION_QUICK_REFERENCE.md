# Quick Reference: Model Evaluation Script

## What It Does

Analyzes the trained Ridge regression model to understand which factors drive building energy consumption.

## Quick Start

```bash
python src/models/evaluate.py
```

## What Gets Created

| Output | Location | Description |
|--------|----------|-------------|
| Feature Importance Plot | `docs/feature_importance.png` | Top 10 features affecting energy usage |
| SHAP Plot (optional) | `docs/shap_summary.png` | Advanced feature importance analysis |
| Console Report | Terminal | Metrics, insights, and recommendations |

## Understanding the Results

### Feature Importance Plot

- **Green bars** = Features that INCREASE energy consumption
- **Red bars** = Features that DECREASE energy consumption
- **Bar length** = How much that feature impacts predictions

### Top Insights You'll Get

1. **What drives energy?** 
   - Example: "Temperature increases energy consumption"
   
2. **Model accuracy?**
   - Example: "R² = 0.82 → Model explains 82% of energy variation"
   
3. **What to optimize?**
   - Example: "Cool building when outdoor temperature is low"

## Key Metrics Explained

| Metric | Meaning | Goal |
|--------|---------|------|
| R² | % of energy variation explained | Higher = better (0.8+) |
| RMSE | Average prediction error (Wh) | Lower = better |
| MAE | Absolute prediction error (Wh) | Lower = better |

## 3-Step Interpretation

### Step 1: Look at Top Features
Check which features have the largest coefficients (bars).

### Step 2: Check the Direction
- **Positive coefficient**: Feature increases energy
- **Negative coefficient**: Feature decreases energy

### Step 3: Read the Insights
Console output explains what each top feature means for your building.

## Common Questions Answered

**Q: Should I optimize the top feature?**
A: Yes! It has the strongest impact on energy usage.

**Q: What if I see a negative coefficient?**
A: It means *higher values of that feature reduce energy* (e.g., lower humidity might reduce cooling needs).

**Q: What's a good R² score?**
A: 
- > 0.8 = Excellent model
- 0.6-0.8 = Good model
- < 0.6 = Model needs improvement

**Q: Can I show this plot to non-technical people?**
A: Yes! It's designed to be intuitive. Green increases, red decreases, bar length shows strength.

## Typical Output Example

```
✓ Feature importance plot saved to: docs/feature_importance.png

--- TOP 10 MOST IMPORTANT FEATURES ---
T_out                   +0.0456  (outdoor temp increases energy)
RH_out_lag1            -0.0234  (lagged humidity decreases energy)
hour_sin               +0.0189  (time-of-day effect)
T_in                   +0.0156  (indoor temp increases energy)
...

FEATURES THAT INCREASE ENERGY CONSUMPTION:
📈 T_out (coefficient: 0.0456)
   → Higher temperature increases energy use (cooling/HVAC demand)

MODEL PERFORMANCE:
Test R² Score: 0.8234 → Model explains 82.34% of variance
Test RMSE: 12.56 Wh → Average prediction error of 12.56 Wh

ACTIONABLE INSIGHTS:
1. PRIMARY ENERGY DRIVER: T_out (outdoor temperature)
   - Monitor temperature forecasts for predictive energy management
2. ENERGY MITIGATOR: RH_out_lag1 (historical humidity)
   - Consider humidity trends when optimizing HVAC
3. Model is highly reliable for predictions ✓
```

## Why This Matters

### For Building Operators
- Understand what drives energy costs
- Make data-driven decisions
- Target optimization efforts

### For Sustainability Teams
- Quantify environmental factor impacts
- Plan energy reduction strategies
- Track efficiency improvements

### For Facility Managers
- Explain energy patterns to leadership
- Support investment decisions
- Monitor model performance

## Installation Prerequisites

```bash
pip install scikit-learn pandas numpy matplotlib joblib
```

Optional (for advanced analysis):
```bash
pip install shap
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Model file not found | Run training script first: `python src/models/train.py` |
| Data file not found | Verify `data/raw/energydata_complete.csv` exists |
| Import errors | Install requirements: `pip install -r requirements.txt` |
| SHAP not working | It's optional. Script continues without it. Install with: `pip install shap` |

## File Dependencies

```
Input Files:
├── models/ridge_model.pkl ..................... Trained model
└── data/raw/energydata_complete.csv .......... Energy data

Code Used:
├── src/features/build_features.py ........... Feature engineering
└── src/models/evaluate.py ................... This script

Output Created:
├── docs/ .......... (created if missing)
├── feature_importance.png
└── shap_summary.png (optional)
```

## Next Steps

1. **Run it**: `python src/models/evaluate.py`
2. **Review plots**: Open `docs/feature_importance.png`
3. **Read insights**: Check console output
4. **Share results**: Use plots in stakeholder presentations
5. **Implement changes**: Use insights to optimize building operations

---

**For detailed information, see `docs/EVALUATION_GUIDE.md`**
