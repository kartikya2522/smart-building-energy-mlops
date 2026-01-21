"""
Training Script with MLflow Experiment Tracking

This script implements a complete machine learning pipeline for smart building energy prediction:

1. Loads and engineers features using the build_features pipeline
2. Performs time-based train-test split (80% train, 20% test)
3. Trains two models: Linear Regression (baseline) and Ridge Regression (with hyperparameter tuning)
4. Evaluates both models using RMSE and R² metrics
5. Tracks all experiments and metrics with MLflow
6. Saves the best model (Ridge) to disk using joblib

Author: ML Pipeline
Date: 2025
"""

import os
import sys
import numpy as np
import pandas as pd
from pathlib import Path

# Machine Learning Libraries
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, r2_score

# Model Serialization
import joblib

# Experiment Tracking
import mlflow
import mlflow.sklearn

# Add src directory to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import feature engineering pipeline
from src.features.build_features import build_features


def create_output_directories():
    """
    Create necessary output directories if they don't exist.
    
    Ensures 'models' directory exists for saving trained models.
    """
    models_dir = project_root / "models"
    models_dir.mkdir(exist_ok=True)
    print(f"✓ Models directory ready: {models_dir}")


def load_and_engineer_features(data_path):
    """
    Load raw data and perform feature engineering.
    
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
    print("STEP 1: FEATURE ENGINEERING")
    print("="*70)
    
    X, y = build_features(str(data_path))
    
    print(f"\n✓ Feature engineering complete!")
    print(f"  - Features (X): {X.shape}")
    print(f"  - Target (y): {y.shape}")
    print(f"  - Feature names: {list(X.columns)}")
    
    return X, y


def time_based_split(X, y, train_size=0.8):
    """
    Perform time-based train-test split to avoid temporal data leakage.
    
    For time series data, it's crucial to split by time rather than randomly.
    This ensures the test set represents future data the model hasn't seen.
    
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
    print("STEP 2: TIME-BASED TRAIN-TEST SPLIT")
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


def train_linear_regression(X_train, y_train):
    """
    Train a baseline Linear Regression model.
    
    Linear Regression serves as a simple baseline model to compare against
    more sophisticated approaches like Ridge Regression.
    
    Parameters:
    -----------
    X_train : pd.DataFrame
        Training feature matrix
    y_train : pd.Series
        Training target variable
        
    Returns:
    --------
    model : LinearRegression
        Trained Linear Regression model
    """
    print("\n" + "-"*70)
    print("BASELINE MODEL: Linear Regression")
    print("-"*70)
    
    # Initialize and train model
    model_lr = LinearRegression()
    model_lr.fit(X_train, y_train)
    
    print(f"✓ Linear Regression model trained")
    print(f"  - Number of features: {len(model_lr.coef_)}")
    print(f"  - Model intercept: {model_lr.intercept_:.4f}")
    
    return model_lr


def train_ridge_regression(X_train, y_train, alpha=1.0):
    """
    Train a Ridge Regression model with L2 regularization.
    
    Ridge Regression adds L2 penalty to prevent overfitting:
    - Higher alpha: stronger regularization, simpler model
    - Lower alpha: weaker regularization, more complex model
    - alpha=0: equivalent to Linear Regression
    
    Parameters:
    -----------
    X_train : pd.DataFrame
        Training feature matrix
    y_train : pd.Series
        Training target variable
    alpha : float
        Regularization strength parameter (default: 1.0)
        
    Returns:
    --------
    model : Ridge
        Trained Ridge Regression model
    """
    print("\n" + "-"*70)
    print("PRIMARY MODEL: Ridge Regression")
    print("-"*70)
    
    # Initialize and train model with specified alpha
    model_ridge = Ridge(alpha=alpha, random_state=42)
    model_ridge.fit(X_train, y_train)
    
    print(f"✓ Ridge Regression model trained")
    print(f"  - Regularization parameter (alpha): {alpha}")
    print(f"  - Number of features: {len(model_ridge.coef_)}")
    print(f"  - Model intercept: {model_ridge.intercept_:.4f}")
    
    return model_ridge


def evaluate_model(model, X_train, y_train, X_test, y_test, model_name):
    """
    Evaluate model performance on both training and test sets.
    
    Calculates RMSE (Root Mean Squared Error) and R² score:
    - RMSE: Average prediction error in same units as target (lower is better)
    - R²: Proportion of variance explained (0 to 1, higher is better)
    
    Parameters:
    -----------
    model : sklearn estimator
        Trained model object
    X_train, X_test : pd.DataFrame
        Training and test feature matrices
    y_train, y_test : pd.Series
        Training and test target variables
    model_name : str
        Name of the model for display
        
    Returns:
    --------
    metrics : dict
        Dictionary containing all calculated metrics
    """
    print(f"\n{model_name} Evaluation:")
    print("-" * 50)
    
    # Predictions on training set
    y_pred_train = model.predict(X_train)
    
    # Predictions on test set
    y_pred_test = model.predict(X_test)
    
    # Calculate training metrics
    rmse_train = np.sqrt(mean_squared_error(y_train, y_pred_train))
    r2_train = r2_score(y_train, y_pred_train)
    
    # Calculate test metrics
    rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
    r2_test = r2_score(y_test, y_pred_test)
    
    # Store metrics
    metrics = {
        'rmse_train': rmse_train,
        'r2_train': r2_train,
        'rmse_test': rmse_test,
        'r2_test': r2_test
    }
    
    # Print metrics clearly
    print(f"Training Performance:")
    print(f"  RMSE: {rmse_train:.4f} Wh")
    print(f"  R²:   {r2_train:.4f}")
    print(f"\nTest Performance:")
    print(f"  RMSE: {rmse_test:.4f} Wh")
    print(f"  R²:   {r2_test:.4f}")
    
    return metrics


def main():
    """
    Main execution function that orchestrates the entire training pipeline.
    
    Workflow:
    1. Setup MLflow experiment
    2. Load and engineer features
    3. Perform time-based train-test split
    4. Train baseline Linear Regression model
    5. Train Ridge Regression model with regularization
    6. Evaluate both models
    7. Log all experiments and metrics to MLflow
    8. Save Ridge model to disk
    """
    
    print("\n" + "#"*70)
    print("# SMART BUILDING ENERGY PREDICTION - TRAINING PIPELINE")
    print("#"*70)
    
    # ========================================================================
    # SETUP: Initialize MLflow Experiment
    # ========================================================================
    print("\n" + "="*70)
    print("SETUP: MLFLOW EXPERIMENT TRACKING")
    print("="*70)
    
    experiment_name = "SmartBuildingEnergy"
    
    # Set the experiment
    mlflow.set_experiment(experiment_name)
    
    # Get experiment info
    experiment = mlflow.get_experiment_by_name(experiment_name)
    print(f"\n✓ MLflow Experiment: {experiment_name}")
    print(f"  - Experiment ID: {experiment.experiment_id}")
    
    # ========================================================================
    # STEP 1: Load and Engineer Features
    # ========================================================================
    data_path = project_root / "data" / "raw" / "energydata_complete.csv"
    
    if not data_path.exists():
        print(f"\n✗ ERROR: Data file not found at {data_path}")
        print(f"  Current directory: {os.getcwd()}")
        sys.exit(1)
    
    X, y = load_and_engineer_features(data_path)
    
    # ========================================================================
    # STEP 2: Time-Based Train-Test Split
    # ========================================================================
    X_train, X_test, y_train, y_test = time_based_split(X, y, train_size=0.8)
    
    # ========================================================================
    # STEP 3: Train Baseline Model (Linear Regression)
    # ========================================================================
    print("\n" + "="*70)
    print("STEP 3: MODEL TRAINING")
    print("="*70)
    
    model_lr = train_linear_regression(X_train, y_train)
    
    # ========================================================================
    # STEP 4: Train Primary Model (Ridge Regression)
    # ========================================================================
    # Ridge Regression hyperparameter
    alpha_ridge = 1.0
    
    model_ridge = train_ridge_regression(X_train, y_train, alpha=alpha_ridge)
    
    # ========================================================================
    # STEP 5: Evaluate Both Models
    # ========================================================================
    print("\n" + "="*70)
    print("STEP 4: MODEL EVALUATION")
    print("="*70)
    
    # Evaluate Linear Regression
    metrics_lr = evaluate_model(
        model_lr, X_train, y_train, X_test, y_test,
        "LINEAR REGRESSION"
    )
    
    # Evaluate Ridge Regression
    metrics_ridge = evaluate_model(
        model_ridge, X_train, y_train, X_test, y_test,
        "RIDGE REGRESSION"
    )
    
    # ========================================================================
    # STEP 6: MLflow Experiment Tracking
    # ========================================================================
    print("\n" + "="*70)
    print("STEP 5: MLFLOW LOGGING")
    print("="*70)
    
    # --- Linear Regression Run ---
    print("\nLogging Linear Regression run...")
    with mlflow.start_run(run_name="LinearRegression_Baseline"):
        # Log model type
        mlflow.log_param("model_type", "LinearRegression")
        mlflow.log_param("alpha", "N/A (No regularization)")
        
        # Log metrics
        mlflow.log_metric("train_rmse", metrics_lr['rmse_train'])
        mlflow.log_metric("train_r2", metrics_lr['r2_train'])
        mlflow.log_metric("test_rmse", metrics_lr['rmse_test'])
        mlflow.log_metric("test_r2", metrics_lr['r2_test'])
        
        # Log model to MLflow
        mlflow.sklearn.log_model(model_lr, "linear_regression_model")
        
        print("  ✓ Linear Regression metrics logged to MLflow")
    
    # --- Ridge Regression Run ---
    print("Logging Ridge Regression run...")
    with mlflow.start_run(run_name="RidgeRegression_Alpha1"):
        # Log model type and hyperparameters
        mlflow.log_param("model_type", "Ridge")
        mlflow.log_param("alpha", alpha_ridge)
        mlflow.log_param("train_size_ratio", 0.8)
        mlflow.log_param("num_features", X_train.shape[1])
        
        # Log metrics
        mlflow.log_metric("train_rmse", metrics_ridge['rmse_train'])
        mlflow.log_metric("train_r2", metrics_ridge['r2_train'])
        mlflow.log_metric("test_rmse", metrics_ridge['rmse_test'])
        mlflow.log_metric("test_r2", metrics_ridge['r2_test'])
        
        # Log model to MLflow
        mlflow.sklearn.log_model(model_ridge, "ridge_regression_model")
        
        print("  ✓ Ridge Regression metrics logged to MLflow")
    
    # ========================================================================
    # STEP 7: Save Ridge Model to Disk
    # ========================================================================
    print("\n" + "="*70)
    print("STEP 6: MODEL PERSISTENCE")
    print("="*70)
    
    create_output_directories()
    
    model_path = project_root / "models" / "ridge_model.pkl"
    joblib.dump(model_ridge, model_path)
    
    print(f"\n✓ Ridge model saved to: {model_path}")
    
    # ========================================================================
    # SUMMARY: Print Final Results
    # ========================================================================
    print("\n" + "="*70)
    print("TRAINING PIPELINE SUMMARY")
    print("="*70)
    
    print("\n📊 RESULTS COMPARISON:")
    print("-" * 70)
    print(f"{'Metric':<20} {'Linear Regression':<20} {'Ridge (α={:.1f})':<20}".format(alpha_ridge))
    print("-" * 70)
    print(f"{'Train RMSE':<20} {metrics_lr['rmse_train']:<20.4f} {metrics_ridge['rmse_train']:<20.4f}")
    print(f"{'Test RMSE':<20} {metrics_lr['rmse_test']:<20.4f} {metrics_ridge['rmse_test']:<20.4f}")
    print(f"{'Train R²':<20} {metrics_lr['r2_train']:<20.4f} {metrics_ridge['r2_train']:<20.4f}")
    print(f"{'Test R²':<20} {metrics_lr['r2_test']:<20.4f} {metrics_ridge['r2_test']:<20.4f}")
    print("-" * 70)
    
    print("\n✓ EXPERIMENT TRACKING:")
    print(f"  - MLflow Experiment: {experiment_name}")
    print(f"  - Experiment ID: {experiment.experiment_id}")
    print(f"  - Runs logged: 2 (Linear Regression, Ridge Regression)")
    
    print("\n✓ MODEL SAVED:")
    print(f"  - Path: {model_path}")
    print(f"  - Format: pickle (.pkl)")
    
    print("\n✓ FEATURE ENGINEERING:")
    print(f"  - Training samples: {X_train.shape[0]}")
    print(f"  - Test samples: {X_test.shape[0]}")
    print(f"  - Number of features: {X_train.shape[1]}")
    print(f"  - Features: {list(X_train.columns)}")
    
    print("\n" + "#"*70)
    print("# TRAINING PIPELINE COMPLETED SUCCESSFULLY")
    print("#"*70 + "\n")


if __name__ == "__main__":
    """
    Entry point: Execute the complete training pipeline when script is run directly.
    
    Usage:
        python src/models/train.py
    """
    main()
