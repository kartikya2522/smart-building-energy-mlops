# Model Evaluation Script - Visual Overview

## 📊 Execution Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│         SMART BUILDING ENERGY - MODEL EVALUATION PIPELINE           │
└─────────────────────────────────────────────────────────────────────┘

START
  │
  ├─→ [STEP 1] Load Trained Model
  │   └─ Input: models/ridge_model.pkl
  │   └─ Output: Ridge model object with coefficients
  │
  ├─→ [STEP 2] Feature Engineering
  │   └─ Input: data/raw/energydata_complete.csv
  │   └─ Process: Build features (same pipeline as training)
  │   └─ Output: X (features), y (target)
  │
  ├─→ [STEP 3] Time-Based Train-Test Split
  │   └─ Process: 80% historical → train, 20% recent → test
  │   └─ Output: X_train, X_test, y_train, y_test
  │
  ├─→ [STEP 4] Extract Feature Importance
  │   └─ Process: Coefficients → Feature names mapping
  │   └─ Calculate: Absolute magnitudes
  │   └─ Output: importance_df (sorted by magnitude)
  │
  ├─→ [STEP 5] Evaluate Model Performance
  │   └─ Calculate: RMSE, R², MAE (train & test)
  │   └─ Detect: Overfitting
  │   └─ Output: metrics dictionary
  │
  ├─→ [STEP 6] Plot Top Features
  │   └─ Create: Horizontal bar chart
  │   └─ Color: Green (↑energy), Red (↓energy)
  │   └─ Save: docs/feature_importance.png (300 DPI)
  │
  ├─→ [STEP 7] Generate Textual Insights
  │   └─ Print: Top positive/negative features
  │   └─ Explain: Feature interpretations
  │   └─ Output: Model reliability, recommendations
  │
  ├─→ [STEP 8] SHAP Analysis (Optional)
  │   └─ Check: Is shap library installed?
  │   ├─ YES: Create SHAP summary plot
  │   │       Save: docs/shap_summary.png
  │   └─ NO: Skip gracefully
  │
  └─→ COMPLETE
      └─ All outputs saved to docs/
      └─ Print: Success message
```

## 🎯 Input/Output Mapping

```
INPUTS (Required)
├── models/ridge_model.pkl ........... Trained Ridge model
├── data/raw/energydata_complete.csv  Energy consumption data
└── src/features/build_features.py .. Feature engineering code

PROCESSING
├── Load model
├── Engineer features
├── Time-based split
├── Calculate metrics
├── Extract importance
└── Generate visualizations

OUTPUTS (Generated)
├── docs/feature_importance.png ...... Feature importance plot
├── docs/shap_summary.png ........... SHAP analysis plot (optional)
└── Console output .................. Insights and metrics
```

## 🔄 Data Flow Through Functions

```
                    ridge_model.pkl
                          │
                          ▼
                  load_trained_model()
                          │
                          ▼
                    Ridge model object
                    (coefficients, intercept)
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
   energydata_  build_features()   extract_feature_
   complete.csv       function       importance()
        │                 │                 │
        ▼                 ▼                 ▼
        X, y        Feature pipeline    importance_df
                         │              (sorted by magnitude)
                         │                 │
                         ▼                 ▼
                   time_based_split()  plot_top_features()
                         │                 │
        ┌────────────────┼────────────┬────▼──────────────┐
        │                │            │                  │
        ▼                ▼            ▼                  ▼
    X_train  evaluate_model_  generate_textual_  feature_importance.png
    X_test   performance()    insights()
    y_train       │                │
    y_test        ▼                ▼
    metrics   Console:         Console:
             • RMSE          • Top drivers
             • R²            • Interpretations
             • MAE           • Recommendations
                │
                ▼ (if shap available)
           perform_shap_analysis()
                │
                ▼
           shap_summary.png
```

## 📈 Visualization Examples

### Feature Importance Plot Structure

```
Top 10 Feature Importance (Ridge Regression Coefficients)
┌─────────────────────────────────────────────────────┐
│                                                     │
│ T_out           ████████████████ 0.0456 GREEN      │
│ RH_out_lag1     ═══════════════ -0.0234 RED        │
│ hour_sin        ════════ 0.0189 GREEN              │
│ T_in            ═════════ 0.0156 GREEN             │
│ hour_cos        ═══════ 0.0145 GREEN               │
│ RH_in           ═════ -0.0123 RED                  │
│ T_out_lag1      ═════ 0.0098 GREEN                 │
│ Tdew_out        ════ 0.0087 GREEN                  │
│ Visibility      ═══ -0.0076 RED                    │
│ Press_mm_hg     ══ 0.0065 GREEN                    │
│                                                     │
│ ← Decreases Energy  │ 0 │  Increases Energy →      │
│                (RED)│   │(GREEN)                   │
└─────────────────────────────────────────────────────┘
```

### Console Output Structure

```
═══════════════════════════════════════════════════════════════════════
STEP 1: LOADING TRAINED MODEL
═══════════════════════════════════════════════════════════════════════

✓ Model successfully loaded from: models/ridge_model.pkl
  - Model type: Ridge
  - Regularization parameter (alpha): 1.0
  - Number of features: 15
  - Model intercept: 45.2341

... (STEPS 2-5 output)

═══════════════════════════════════════════════════════════════════════
STEP 6: MODEL PERFORMANCE EVALUATION
═══════════════════════════════════════════════════════════════════════

Training Performance:
  RMSE: 12.1234 Wh
  MAE:  9.5678 Wh
  R²:   0.8345

Test Performance:
  RMSE: 12.8456 Wh
  MAE:  10.1234 Wh
  R²:   0.8156

Overfitting Analysis:
  RMSE difference (Test - Train): 0.7222 Wh
  R² difference (Train - Test): 0.0189
  ✓ Good generalization (consistent performance)

═══════════════════════════════════════════════════════════════════════
STEP 7: TEXTUAL INSIGHTS - ENERGY USAGE DRIVERS
═══════════════════════════════════════════════════════════════════════

FEATURES THAT INCREASE ENERGY CONSUMPTION (Positive Coefficients)
───────────────────────────────────────────────────────────────────

📈 T_out (coefficient: 0.0456)
   → Higher temperature increases energy use (likely cooling/HVAC demand)

📈 hour_sin (coefficient: 0.0189)
   → Time-of-day cyclic pattern affects energy consumption

📈 T_in (coefficient: 0.0156)
   → Indoor temperature increases energy use

FEATURES THAT DECREASE ENERGY CONSUMPTION (Negative Coefficients)
───────────────────────────────────────────────────────────────────

📉 RH_out_lag1 (coefficient: -0.0234)
   → Lower humidity reduces energy use (less dehumidification needed)

ACTIONABLE INSIGHTS FOR BUILDING OPERATIONS
───────────────────────────────────────────────────────────────────

1. PRIMARY ENERGY DRIVER: T_out
   - This is the strongest predictor of energy consumption
   - Focus on monitoring and controlling this factor for energy savings

2. ENERGY MITIGATOR: RH_out_lag1
   - This factor most effectively reduces energy demand
   - Strategies to leverage this factor could yield energy savings

3. MODEL RELIABILITY:
   ✓ Strong model - highly reliable for predictions and insights
```

## 🔍 Feature Interpretation Guide

```
COEFFICIENT MEANING
═════════════════════════════════════════════════════════════════════

Positive Coefficient (+)
├─ Meaning: Feature INCREASES energy consumption
├─ Size: Larger value = stronger impact
├─ Example: T_out = +0.0456 means
│  "Each 1°C increase in outdoor temperature
│   adds ~0.0456 Wh to energy consumption"
└─ Action: Monitor and minimize when possible

Negative Coefficient (-)
├─ Meaning: Feature DECREASES energy consumption
├─ Size: Larger magnitude = stronger impact
├─ Example: RH_out_lag1 = -0.0234 means
│  "Higher historical humidity reduces
│   energy consumption by ~0.0234 Wh per unit"
└─ Action: Leverage this factor for savings

MAGNITUDE RANKING
═════════════════════════════════════════════════════════════════════

|0.0456| > |0.0234| > |0.0189| > ... → Feature importance order

Highest to Lowest = Most to Least Important
```

## 🎓 Interpretability Benefits Hierarchy

```
WHY LINEAR MODELS EXCEL AT INTERPRETABILITY
═════════════════════════════════════════════════════════════════════

Level 1: BASIC TRANSPARENCY
├─ Prediction equation is explicit
├─ Can see exact coefficient values
└─ Direct coefficient → impact mapping

Level 2: STAKEHOLDER COMMUNICATION
├─ Non-technical people understand coefficients
├─ Can explain "why" to facility managers
└─ Supports decision-making approval

Level 3: REGULATORY COMPLIANCE
├─ Naturally satisfies explainability requirements
├─ Clear audit trail for energy decisions
└─ GDPR "right to explanation" compatible

Level 4: DEBUGGING & VALIDATION
├─ Unexpected predictions → trace to features
├─ Identify data quality issues directly
└─ Validate domain knowledge

Level 5: ACTIONABLE INSIGHTS
├─ Clear guidance on optimization targets
├─ Quantified impact enables ROI calculations
└─ Evidence-based operational strategies
```

## 📊 Metrics Interpretation Map

```
R² SCORE INTERPRETATION
═════════════════════════════════════════════════════════════════════

[0.90-1.00] ▓▓▓▓▓▓▓▓▓▓ EXCELLENT
            → Model explains 90%+ of variance
            → Use for critical decisions with confidence

[0.80-0.89] ▓▓▓▓▓▓▓▓░░ STRONG
            → Model explains 80-89% of variance
            → Use for operational predictions
            → Standard for building energy models

[0.60-0.79] ▓▓▓▓▓▓░░░░ GOOD
            → Model explains 60-79% of variance
            → Use with validation checks
            → Consider feature improvements

[0.40-0.59] ▓▓▓░░░░░░░ MODERATE
            → Model explains 40-59% of variance
            → Use for trend analysis only
            → Requires significant validation

[0.00-0.39] ░░░░░░░░░░ POOR
            → Model explains <40% of variance
            → Not suitable for predictions
            → Requires major improvements
```

## 🚀 Usage Quick Diagram

```
USER ACTION                 SCRIPT EXECUTES
═════════════════════════════════════════════════════════════════════

python src/models/evaluate.py
  │
  ├─ Loads model from disk
  │
  ├─ Loads & processes data
  │  ├─ Feature engineering
  │  └─ Time-based split
  │
  ├─ Evaluates performance
  │  ├─ Calculates RMSE, R², MAE
  │  └─ Detects overfitting
  │
  ├─ Creates visualizations
  │  ├─ Feature importance plot
  │  └─ SHAP plot (optional)
  │
  └─ Generates insights
     ├─ Prints metrics
     ├─ Explains features
     └─ Recommends actions

OUTPUTS AVAILABLE
═════════════════════════════════════════════════════════════════════

1. Visualization Files
   ├─ docs/feature_importance.png (300 DPI)
   └─ docs/shap_summary.png (optional)

2. Console Output
   ├─ Model performance metrics
   ├─ Feature ranking
   └─ Actionable insights

3. Ready for Sharing
   ├─ Stakeholder presentations
   ├─ Operations team briefings
   └─ Executive summaries
```

## 🔗 Integration Points

```
SMART BUILDING ENERGY PROJECT STRUCTURE
═════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────┐
│          TRAINING PIPELINE              │
│   (src/models/train.py)                 │
│  ✓ Feature engineering                  │
│  ✓ Time-based split                     │
│  ✓ Model training                       │
│  ✓ Save model → models/ridge_model.pkl  │
└────────────────┬────────────────────────┘
                 │
                 │ (model file)
                 ▼
        ┌─────────────────┐
        │  Ridge Model    │
        └────────┬────────┘
                 │
                 │ (loads from disk)
                 ▼
┌─────────────────────────────────────────┐
│      EVALUATION PIPELINE                │
│    (src/models/evaluate.py)             │
│  ✓ Load model                           │
│  ✓ Feature engineering (same pipeline)  │
│  ✓ Time-based split (same methodology)  │
│  ✓ Performance evaluation               │
│  ✓ Feature importance analysis          │
│  ✓ Visualizations & insights            │
└────────────────┬────────────────────────┘
                 │
                 │ (outputs)
                 ├─ feature_importance.png
                 ├─ shap_summary.png
                 └─ Console insights
```

## ✨ Key Features Overview

```
FEATURE                          STATUS    DESCRIPTION
═════════════════════════════════════════════════════════════════════

1. Model Loading                ✅ DONE   Loads pre-trained Ridge model
2. Feature Engineering          ✅ DONE   Same pipeline as training
3. Time-Based Split             ✅ DONE   No temporal data leakage
4. Coefficient Extraction       ✅ DONE   Features → Importance mapping
5. Feature Importance Plot      ✅ DONE   300 DPI, color-coded bars
6. Auto-Create docs/ Folder     ✅ DONE   Handles missing directories
7. SHAP Analysis (Optional)     ✅ DONE   Game theory-based importance
8. Textual Insights             ✅ DONE   Rich, actionable explanations
9. Interpretability Comments    ✅ DONE   40+ lines of documentation

METRICS CALCULATED              STATUS    VALUES
─────────────────────────────────────────────────────────────────────
RMSE (Root Mean Squared Error)  ✅ DONE   Wh (watt-hours)
R² (Coefficient of Determin.)   ✅ DONE   0-1 scale
MAE (Mean Absolute Error)       ✅ DONE   Wh (watt-hours)
Overfitting Detection           ✅ DONE   Train/test comparison
```

---

**Complete visual reference for the model evaluation pipeline.**
