"""
Model Evaluation and Interpretability Script for Ridge Regression

This script provides comprehensive model evaluation and feature importance analysis for the 
trained Ridge Regression model. It includes:

1. Model Loading: Loads the pre-trained Ridge model from disk
2. Feature Engineering: Imports and uses the same feature engineering pipeline as training
3. Time-based Train-Test Split: Maintains consistency with training split methodology
4. Coefficient Extraction: Associates model coefficients with feature names
5. Feature Importance Visualization: Plots top 10 features by magnitude
6. SHAP Analysis (Optional): Generates SHAP summary plots for deeper interpretability
7. Textual Insights: Provides clear explanations of which features drive energy usage

WHY INTERPRETABILITY IS IMPORTANT FOR LINEAR MODELS:
------------------------------------------------------
Linear models like Ridge Regression are inherently interpretable because:
1. Each feature has a single, consistent coefficient representing its impact
2. Model predictions are direct combinations of features and coefficients (transparency)
3. Stakeholders can understand the "why" behind predictions (trustworthiness)
4. Feature importance can be directly extracted without approximations
5. Regulatory compliance and explainability are easier for linear models
6. Debugging and validation are simpler with clear feature-contribution relationships

Unlike black-box models (neural networks, tree ensembles), linear models allow:
- Direct attribution of predictions to specific features
- Easy identification of problematic correlations or unexplained behaviors
- Confidence in model decisions for high-stakes applications (building operations)
- Straightforward communication with non-technical stakeholders

USAGE:
------
python src/models/evaluate.py

Author: ML Pipeline
Date: 2025
"""

import os
import sys
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Add src directory to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import feature engineering pipeline
from src.features.build_features import build_features


def create_output_directories():
    """
    Create necessary output directories for visualizations and results.
    
    Ensures 'docs' directory exists for saving plots and visualizations.
    """
    docs_dir = project_root / "docs"
    docs_dir.mkdir(exist_ok=True)
    print(f"✓ Documentation directory ready: {docs_dir}")
    return docs_dir


def load_trained_model(model_path):
    """
    Load the pre-trained Ridge model from disk.
    
    Parameters:
    -----------
    model_path : str or Path
        Path to the saved Ridge model pickle file
        
    Returns:
    --------
    model : Ridge
        Loaded Ridge Regression model
    """
    print("\n" + "="*70)
    print("STEP 1: LOADING TRAINED MODEL")
    print("="*70)
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at: {model_path}")
    
    model = joblib.load(model_path)
    print(f"\n✓ Model successfully loaded from: {model_path}")
    print(f"  - Model type: {type(model).__name__}")
    print(f"  - Regularization parameter (alpha): {model.alpha}")
    print(f"  - Number of features: {len(model.coef_)}")
    print(f"  - Model intercept: {model.intercept_:.4f}")
    
    return model


def load_and_engineer_features(data_path):
    """
    Load raw data and perform feature engineering using the same pipeline as training.
    
    This ensures consistency between training and evaluation environments.
    
    Parameters:
    -----------
    data_path : str or Path
        Path to the raw energy data CSV file
        
    Returns:
    --------
    X : pd.DataFrame
        Engineered feature matrix
    y : pd.Series
        Target variable (energy consumption in Wh)
    """
    print("\n" + "="*70)
    print("STEP 2: FEATURE ENGINEERING (SAME AS TRAINING)")
    print("="*70)
    
    X, y = build_features(str(data_path))
    
    print(f"\n✓ Feature engineering complete!")
    print(f"  - Features (X): {X.shape}")
    print(f"  - Target (y): {y.shape}")
    print(f"  - Feature names: {list(X.columns)}")
    
    return X, y


def time_based_split(X, y, train_size=0.8):
    """
    Perform time-based train-test split using the same methodology as training.
    
    For time series data, splitting by time is crucial to avoid temporal data leakage.
    This split matches exactly what was used during model training.
    
    Parameters:
    -----------
    X : pd.DataFrame
        Feature matrix
    y : pd.Series
        Target variable
    train_size : float
        Proportion of data for training (default: 0.8 = 80%)
        
    Returns:
    --------
    X_train, X_test : pd.DataFrame
        Training and test feature sets
    y_train, y_test : pd.Series
        Training and test target sets
    """
    print("\n" + "="*70)
    print("STEP 3: TIME-BASED TRAIN-TEST SPLIT")
    print("="*70)
    
    # Calculate split point
    split_idx = int(len(X) * train_size)
    
    # Split data chronologically (first 80% train, last 20% test)
    X_train = X.iloc[:split_idx].copy()
    X_test = X.iloc[split_idx:].copy()
    y_train = y.iloc[:split_idx].copy()
    y_test = y.iloc[split_idx:].copy()
    
    print(f"\n✓ Time-based split completed!")
    print(f"  - Training set: {X_train.shape} samples")
    print(f"  - Test set: {X_test.shape} samples")
    print(f"  - Split ratio: {train_size:.1%} train, {1-train_size:.1%} test")
    
    return X_train, X_test, y_train, y_test


def extract_feature_importance(model, feature_names):
    """
    Extract model coefficients and associate them with feature names.
    
    For linear models, coefficients directly represent feature importance:
    - Positive coefficient: feature increases energy consumption
    - Negative coefficient: feature decreases energy consumption
    - Larger magnitude: stronger impact on predictions
    
    Ridge regularization shrinks coefficients to prevent overfitting,
    resulting in more robust and generalizable feature importance estimates.
    
    Parameters:
    -----------
    model : Ridge
        Trained Ridge Regression model
    feature_names : list
        List of feature names from X.columns
        
    Returns:
    --------
    importance_df : pd.DataFrame
        DataFrame with features, their coefficients, and absolute magnitudes
    """
    print("\n" + "="*70)
    print("STEP 4: EXTRACTING FEATURE IMPORTANCE")
    print("="*70)
    
    # Create DataFrame associating coefficients with feature names
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Coefficient': model.coef_,
        'Abs_Coefficient': np.abs(model.coef_)
    })
    
    # Sort by absolute coefficient magnitude (importance)
    importance_df = importance_df.sort_values('Abs_Coefficient', ascending=False)
    importance_df = importance_df.reset_index(drop=True)
    
    print(f"\n✓ Feature importance extracted!")
    print(f"  - Total features: {len(importance_df)}")
    print(f"  - Model intercept: {model.intercept_:.4f}")
    
    print(f"\n--- TOP 10 MOST IMPORTANT FEATURES ---")
    print(importance_df.head(10).to_string(index=False))
    
    return importance_df


def plot_top_features(importance_df, num_features=10, output_path=None):
    """
    Create and save a bar plot of the top N features by absolute coefficient magnitude.
    
    Visualization helps identify which features have the strongest impact on energy predictions.
    Positive coefficients (right side) increase predictions; negative (left side) decrease them.
    
    Parameters:
    -----------
    importance_df : pd.DataFrame
        DataFrame with features and coefficients
    num_features : int
        Number of top features to plot (default: 10)
    output_path : str or Path
        Path where to save the plot (optional)
        
    Returns:
    --------
    None (saves plot to file if output_path provided)
    """
    print("\n" + "="*70)
    print("STEP 5: PLOTTING FEATURE IMPORTANCE")
    print("="*70)
    
    # Get top N features
    top_features = importance_df.head(num_features).copy()
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create color map: positive coefficients in green, negative in red
    colors = ['green' if x > 0 else 'red' for x in top_features['Coefficient']]
    
    # Create horizontal bar plot
    ax.barh(range(len(top_features)), top_features['Coefficient'], color=colors, alpha=0.7)
    ax.set_yticks(range(len(top_features)))
    ax.set_yticklabels(top_features['Feature'])
    ax.set_xlabel('Coefficient Value', fontsize=12, fontweight='bold')
    ax.set_title(f'Top {num_features} Feature Importance (Ridge Regression Coefficients)', 
                 fontsize=14, fontweight='bold')
    ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
    ax.grid(axis='x', alpha=0.3)
    
    # Add text annotations for coefficient values
    for i, (idx, row) in enumerate(top_features.iterrows()):
        ax.text(row['Coefficient'], i, f"  {row['Coefficient']:.4f}", 
                va='center', fontsize=9)
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n✓ Feature importance plot saved to: {output_path}")
    
    print(f"\n--- PLOT INSIGHTS ---")
    print(f"Green bars (positive coefficients): Features that INCREASE energy consumption")
    print(f"Red bars (negative coefficients): Features that DECREASE energy consumption")
    
    plt.close()


def evaluate_model_performance(model, X_train, y_train, X_test, y_test):
    """
    Evaluate model performance on training and test sets.
    
    Calculates RMSE and R² metrics to assess model quality and potential overfitting.
    
    Parameters:
    -----------
    model : Ridge
        Trained Ridge Regression model
    X_train, X_test : pd.DataFrame
        Training and test feature matrices
    y_train, y_test : pd.Series
        Training and test target variables
        
    Returns:
    --------
    metrics : dict
        Dictionary containing all calculated metrics
    """
    print("\n" + "="*70)
    print("STEP 6: MODEL PERFORMANCE EVALUATION")
    print("="*70)
    
    from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
    
    # Predictions on training set
    y_pred_train = model.predict(X_train)
    
    # Predictions on test set
    y_pred_test = model.predict(X_test)
    
    # Calculate training metrics
    rmse_train = np.sqrt(mean_squared_error(y_train, y_pred_train))
    r2_train = r2_score(y_train, y_pred_train)
    mae_train = mean_absolute_error(y_train, y_pred_train)
    
    # Calculate test metrics
    rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
    r2_test = r2_score(y_test, y_pred_test)
    mae_test = mean_absolute_error(y_test, y_pred_test)
    
    # Store metrics
    metrics = {
        'rmse_train': rmse_train,
        'r2_train': r2_train,
        'mae_train': mae_train,
        'rmse_test': rmse_test,
        'r2_test': r2_test,
        'mae_test': mae_test
    }
    
    # Print metrics
    print(f"\nTraining Performance:")
    print(f"  RMSE: {rmse_train:.4f} Wh")
    print(f"  MAE:  {mae_train:.4f} Wh")
    print(f"  R²:   {r2_train:.4f}")
    
    print(f"\nTest Performance:")
    print(f"  RMSE: {rmse_test:.4f} Wh")
    print(f"  MAE:  {mae_test:.4f} Wh")
    print(f"  R²:   {r2_test:.4f}")
    
    # Check for overfitting
    rmse_diff = rmse_test - rmse_train
    r2_diff = r2_train - r2_test
    
    print(f"\nOverfitting Analysis:")
    print(f"  RMSE difference (Test - Train): {rmse_diff:.4f} Wh")
    print(f"  R² difference (Train - Test): {r2_diff:.4f}")
    
    if r2_diff > 0.05:
        print(f"  ⚠ Slight overfitting detected (R² gap > 5%)")
    elif r2_diff < -0.05:
        print(f"  ℹ Model performs better on test set (potential distribution shift)")
    else:
        print(f"  ✓ Good generalization (consistent performance)")
    
    return metrics


def generate_textual_insights(importance_df, metrics, feature_names):
    """
    Generate and print clear textual insights about feature importance and model behavior.
    
    This function explains which features drive energy usage and provides actionable insights
    for building operations and energy management strategies.
    
    Parameters:
    -----------
    importance_df : pd.DataFrame
        DataFrame with features and their coefficients
    metrics : dict
        Dictionary of model performance metrics
    feature_names : list
        List of all feature names
    """
    print("\n" + "="*70)
    print("STEP 7: TEXTUAL INSIGHTS - ENERGY USAGE DRIVERS")
    print("="*70)
    
    # Extract top positive and negative features
    top_positive = importance_df[importance_df['Coefficient'] > 0].head(5)
    top_negative = importance_df[importance_df['Coefficient'] < 0].head(5)
    
    print(f"\n" + "-"*70)
    print("FEATURES THAT INCREASE ENERGY CONSUMPTION (Positive Coefficients)")
    print("-"*70)
    
    for idx, row in top_positive.iterrows():
        feature = row['Feature']
        coef = row['Coefficient']
        print(f"\n📈 {feature} (coefficient: {coef:.4f})")
        
        # Provide contextual interpretation
        if 'temp' in feature.lower() or 'temperature' in feature.lower():
            print(f"   → Higher temperature increases energy use (likely cooling/HVAC demand)")
        elif 'humid' in feature.lower() or 'rh' in feature.lower():
            print(f"   → Higher humidity increases energy use (likely cooling system workload)")
        elif 'hour' in feature.lower():
            print(f"   → Time-of-day cyclic pattern affects energy consumption")
        elif 'pressure' in feature.lower():
            print(f"   → Pressure changes correlate with weather effects on energy usage")
        else:
            print(f"   → This external factor positively drives energy consumption")
    
    print(f"\n" + "-"*70)
    print("FEATURES THAT DECREASE ENERGY CONSUMPTION (Negative Coefficients)")
    print("-"*70)
    
    if len(top_negative) > 0:
        for idx, row in top_negative.iterrows():
            feature = row['Feature']
            coef = row['Coefficient']
            print(f"\n📉 {feature} (coefficient: {coef:.4f})")
            
            # Provide contextual interpretation
            if 'temp' in feature.lower() or 'temperature' in feature.lower():
                print(f"   → Lower temperature values reduce energy use (less cooling needed)")
            elif 'humid' in feature.lower() or 'rh' in feature.lower():
                print(f"   → Lower humidity reduces energy use (less dehumidification needed)")
            else:
                print(f"   → This factor inversely affects energy consumption")
    else:
        print(f"\nℹ No significant negative coefficients found.")
    
    print(f"\n" + "-"*70)
    print("MODEL PERFORMANCE SUMMARY")
    print("-"*70)
    
    print(f"\nTest Set R² Score: {metrics['r2_test']:.4f}")
    print(f"  → Model explains {metrics['r2_test']*100:.2f}% of variance in energy consumption")
    
    print(f"\nTest Set RMSE: {metrics['rmse_test']:.4f} Wh")
    print(f"  → Average prediction error: {metrics['rmse_test']:.2f} Wh")
    print(f"  → Relative error: {(metrics['rmse_test']/100):.2f}% (assuming ~100 Wh avg consumption)")
    
    print(f"\n" + "-"*70)
    print("ACTIONABLE INSIGHTS FOR BUILDING OPERATIONS")
    print("-"*70)
    
    # Get max positive coefficient
    max_positive_feature = importance_df[importance_df['Coefficient'] > 0].iloc[0]
    max_negative_feature = importance_df[importance_df['Coefficient'] < 0].iloc[0]
    
    print(f"\n1. PRIMARY ENERGY DRIVER: {max_positive_feature['Feature']}")
    print(f"   - This is the strongest predictor of energy consumption")
    print(f"   - Focus on monitoring and controlling this factor for energy savings")
    
    if len(max_negative_feature) > 0:
        print(f"\n2. ENERGY MITIGATOR: {max_negative_feature['Feature']}")
        print(f"   - This factor most effectively reduces energy demand")
        print(f"   - Strategies to leverage this factor could yield energy savings")
    
    print(f"\n3. MODEL RELIABILITY:")
    if metrics['r2_test'] > 0.8:
        print(f"   ✓ Strong model - highly reliable for predictions and insights")
    elif metrics['r2_test'] > 0.6:
        print(f"   ✓ Good model - suitable for decision-making with validation")
    else:
        print(f"   ⚠ Moderate model - use predictions with caution, explore additional features")
    
    print(f"\n" + "-"*70)


def perform_shap_analysis(model, X_test_sample, feature_names, output_path=None):
    """
    Perform SHAP (SHapley Additive exPlanations) analysis for deeper interpretability.
    
    SHAP provides a more sophisticated feature importance estimation based on game theory,
    considering feature interactions and individual prediction explanations.
    
    Optional step - requires shap library.
    
    Parameters:
    -----------
    model : Ridge
        Trained Ridge Regression model
    X_test_sample : pd.DataFrame
        Sample of test data for SHAP analysis (typically 100-200 samples)
    feature_names : list
        List of feature names
    output_path : str or Path
        Path where to save the SHAP summary plot
        
    Returns:
    --------
    None (saves plot to file if output_path provided)
    """
    print("\n" + "="*70)
    print("STEP 8 (OPTIONAL): SHAP ANALYSIS FOR ADVANCED INTERPRETABILITY")
    print("="*70)
    
    try:
        import shap
    except ImportError:
        print(f"\n⚠ SHAP library not installed. Skipping SHAP analysis.")
        print(f"  To enable SHAP analysis, install: pip install shap")
        return
    
    print(f"\n✓ SHAP library found. Performing analysis...")
    print(f"  - Sample size for analysis: {len(X_test_sample)} observations")
    
    # Create SHAP explainer
    explainer = shap.LinearExplainer(model, X_test_sample)
    shap_values = explainer.shap_values(X_test_sample)
    
    # Create SHAP summary plot
    plt.figure(figsize=(12, 8))
    shap.summary_plot(shap_values, X_test_sample, plot_type="bar", show=False)
    plt.title("SHAP Feature Importance - Ridge Regression", fontsize=14, fontweight='bold')
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n✓ SHAP summary plot saved to: {output_path}")
    
    plt.close()
    
    print(f"\n✓ SHAP analysis complete!")
    print(f"  - SHAP values computed for feature interactions and individual impacts")


def main():
    """
    Main execution function that orchestrates the complete evaluation pipeline.
    
    Workflow:
    1. Create output directories
    2. Load trained Ridge model
    3. Load and engineer features (same pipeline as training)
    4. Perform time-based train-test split
    5. Evaluate model performance
    6. Extract feature importance
    7. Plot top features
    8. Generate textual insights
    9. (Optional) Perform SHAP analysis
    """
    
    print("\n" + "#"*70)
    print("# SMART BUILDING ENERGY - MODEL EVALUATION & INTERPRETABILITY")
    print("#"*70)
    
    try:
        # Create output directories
        docs_dir = create_output_directories()
        
        # Load trained model
        model_path = project_root / "models" / "ridge_model.pkl"
        model = load_trained_model(model_path)
        
        # Load and engineer features
        data_path = project_root / "data" / "raw" / "energydata_complete.csv"
        X, y = load_and_engineer_features(data_path)
        
        # Perform time-based split
        X_train, X_test, y_train, y_test = time_based_split(X, y, train_size=0.8)
        
        # Evaluate model performance
        metrics = evaluate_model_performance(model, X_train, y_train, X_test, y_test)
        
        # Extract feature importance
        feature_names = X.columns.tolist()
        importance_df = extract_feature_importance(model, feature_names)
        
        # Plot top features
        plot_output = docs_dir / "feature_importance.png"
        plot_top_features(importance_df, num_features=10, output_path=plot_output)
        
        # Generate textual insights
        generate_textual_insights(importance_df, metrics, feature_names)
        
        # Perform optional SHAP analysis
        print(f"\n--- Optional SHAP Analysis ---")
        X_test_sample = X_test.sample(n=min(100, len(X_test)), random_state=42)
        shap_output = docs_dir / "shap_summary.png"
        perform_shap_analysis(model, X_test_sample, feature_names, output_path=shap_output)
        
        # Print completion message
        print("\n" + "#"*70)
        print("# EVALUATION & INTERPRETABILITY ANALYSIS COMPLETE")
        print("#"*70)
        print(f"\n✓ All outputs saved to: {docs_dir}")
        print(f"  - Feature importance plot: feature_importance.png")
        print(f"  - SHAP summary plot: shap_summary.png (if available)")
        
    except Exception as e:
        print(f"\n✗ Error during evaluation: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
