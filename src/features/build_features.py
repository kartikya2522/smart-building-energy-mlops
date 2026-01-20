"""
Feature Engineering Module for Smart Building Energy Prediction

This module loads raw energy data, performs feature engineering including:
- Time-based cyclical feature extraction
- Lag feature creation for selected variables
- Variance Inflation Factor (VIF) analysis for multicollinearity detection
- Iterative removal of high-VIF features

The output is a clean feature matrix X and target variable y suitable for modeling.
"""

import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor
import os


def load_and_prepare_data(data_path):
    """
    Load raw energy data and prepare for feature engineering.
    
    Parameters:
    -----------
    data_path : str
        Path to the raw CSV file containing energy data
        
    Returns:
    --------
    df : pd.DataFrame
        DataFrame with parsed datetime and loaded data
    """
    # Load the raw CSV file
    df = pd.read_csv(data_path)
    
    # Parse the date column to datetime format for time-based feature extraction
    df['date'] = pd.to_datetime(df['date'])
    
    return df


def drop_non_feature_columns(df):
    """
    Remove non-feature columns while preserving the target variable 'Appliances' and 'date'.
    
    Columns retained: numeric features, the target 'Appliances', and 'date' (for feature extraction)
    Columns dropped: 'lights' and other non-predictive columns
    
    Parameters:
    -----------
    df : pd.DataFrame
        Raw energy DataFrame
        
    Returns:
    --------
    df : pd.DataFrame
        DataFrame with non-feature columns removed (except 'Appliances' target and 'date')
    """
    # Get list of numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Ensure 'Appliances' (target) is present
    if 'Appliances' not in numeric_cols:
        raise ValueError("Target column 'Appliances' not found in dataset")
    
    # Build column list: numeric features + date (for time feature extraction)
    cols_to_keep = numeric_cols + ['date']
    df = df[cols_to_keep]
    
    # Remove 'lights' (often considered a proxy for occupancy, not independent feature)
    if 'lights' in df.columns:
        df = df.drop(columns=['lights'])
    if 'Lights' in df.columns:
        df = df.drop(columns=['Lights'])
    
    return df


def create_time_features(df):
    """
    Create time-based features from the date column.
    
    Features created:
    - hour: Hour of day (0-23) for capturing daily patterns
    - hour_sin: Sine-encoded hour for cyclical representation
    - hour_cos: Cosine-encoded hour for cyclical representation
    
    Cyclical encoding preserves the circular nature of time (hour 23 is close to hour 0).
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with 'date' column in datetime format
        
    Returns:
    --------
    df : pd.DataFrame
        DataFrame with added time-based features
    """
    # Extract hour from date column
    df['hour'] = df['date'].dt.hour
    
    # Create cyclical encoding of hour using sine and cosine transforms
    # This captures the circular nature of hours in a day
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    
    return df


def create_lag_features(df):
    """
    Create lag features for selected external variables only.
    
    IMPORTANT: Only create lags for temperature and humidity features,
    NOT for the target variable 'Appliances' to avoid data leakage.
    
    Features lagged:
    - T_out_lag1: 1-hour lagged outdoor temperature
    - RH_out_lag1: 1-hour lagged outdoor relative humidity
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with features
        
    Returns:
    --------
    df : pd.DataFrame
        DataFrame with lag features added
    """
    # Create 1-hour lag for outdoor temperature (T_out)
    if 'T_out' in df.columns:
        df['T_out_lag1'] = df['T_out'].shift(1)
    
    # Create 1-hour lag for outdoor relative humidity (RH_out)
    if 'RH_out' in df.columns:
        df['RH_out_lag1'] = df['RH_out'].shift(1)
    
    return df


def handle_missing_values(df):
    """
    Drop rows with NaN values created by lagging operations.
    
    Lagging inherently creates NaN values in the first row(s).
    This function removes those rows to prepare clean data for modeling.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with potential NaN values from lagging
        
    Returns:
    --------
    df : pd.DataFrame
        DataFrame with NaN rows removed
    """
    # Drop rows with any NaN values (created by lagging operations)
    df = df.dropna()
    
    # Reset index for clean indexing
    df = df.reset_index(drop=True)
    
    return df


def compute_vif(df):
    """
    Compute Variance Inflation Factor (VIF) for numeric features.
    
    VIF measures multicollinearity in regression models.
    VIF > 10 typically indicates problematic multicollinearity.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with numeric features only
        
    Returns:
    --------
    vif_df : pd.DataFrame
        DataFrame with Feature names and their corresponding VIF values
    """
    # Create empty list to store VIF results
    vif_data = []
    
    # Compute VIF for each numeric column
    for i, col in enumerate(df.columns):
        vif_value = variance_inflation_factor(df.values, i)
        vif_data.append({
            'Feature': col,
            'VIF': vif_value
        })
    
    vif_df = pd.DataFrame(vif_data)
    vif_df = vif_df.sort_values('VIF', ascending=False)
    
    return vif_df


def remove_high_vif_features(df, vif_threshold=10):
    """
    Iteratively remove features with VIF > threshold.
    
    This process reduces multicollinearity by removing correlated features.
    Iterative removal is necessary because removing one feature affects VIF values of others.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with numeric features
    vif_threshold : float
        VIF threshold above which features are removed (default: 10)
        
    Returns:
    --------
    df_clean : pd.DataFrame
        DataFrame with high-VIF features removed
    removed_features : list
        List of features that were removed
    """
    removed_features = []
    iteration = 0
    
    print(f"\n--- Starting VIF-based Feature Removal (threshold={vif_threshold}) ---")
    
    while True:
        iteration += 1
        
        # Compute VIF for current features
        vif_df = compute_vif(df)
        max_vif = vif_df['VIF'].max()
        
        # Print current status
        print(f"\nIteration {iteration}:")
        print(f"Max VIF: {max_vif:.4f}, Features: {len(df.columns)}")
        
        # If max VIF is below threshold, stop iteration
        if max_vif <= vif_threshold:
            print(f"Max VIF ({max_vif:.4f}) below threshold ({vif_threshold}). Stopping.")
            break
        
        # Remove feature with highest VIF
        feature_to_remove = vif_df.iloc[0]['Feature']
        removed_features.append(feature_to_remove)
        print(f"Removing '{feature_to_remove}' with VIF={vif_df.iloc[0]['VIF']:.4f}")
        
        df = df.drop(columns=[feature_to_remove])
    
    print(f"\nTotal features removed: {len(removed_features)}")
    print(f"Removed features: {removed_features}")
    print(f"Remaining features: {df.columns.tolist()}")
    
    return df, removed_features


def build_features(data_path):
    """
    Main feature engineering pipeline.
    
    Orchestrates the entire feature engineering process:
    1. Load and parse raw data
    2. Drop non-feature columns
    3. Create time-based features
    4. Create lag features
    5. Handle missing values
    6. Remove high-VIF features for multicollinearity mitigation
    
    Parameters:
    -----------
    data_path : str
        Path to raw energy data CSV file
        
    Returns:
    --------
    X : pd.DataFrame
        Feature matrix (all columns except 'Appliances')
    y : pd.Series
        Target variable (Appliances)
    """
    print("=" * 70)
    print("FEATURE ENGINEERING PIPELINE")
    print("=" * 70)
    
    # Step 1: Load and prepare data
    print("\n[Step 1] Loading and parsing data...")
    df = load_and_prepare_data(data_path)
    print(f"Loaded data shape: {df.shape}")
    
    # Step 2: Drop non-feature columns (keep only numerics and target)
    print("\n[Step 2] Dropping non-feature columns...")
    df = drop_non_feature_columns(df)
    print(f"After dropping non-features: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Step 3: Create time-based features
    print("\n[Step 3] Creating time-based features...")
    df = create_time_features(df)
    print(f"Added features: hour, hour_sin, hour_cos")
    print(f"Current shape: {df.shape}")
    
    # Step 4: Create lag features (for T_out and RH_out only, NOT target)
    print("\n[Step 4] Creating lag features...")
    df = create_lag_features(df)
    print(f"Added lag features for T_out and RH_out")
    print(f"Current shape: {df.shape}")
    
    # Step 5: Handle missing values from lagging
    print("\n[Step 5] Handling missing values from lagging...")
    initial_rows = len(df)
    df = handle_missing_values(df)
    rows_dropped = initial_rows - len(df)
    print(f"Dropped {rows_dropped} rows with NaN values")
    print(f"Final data shape: {df.shape}")
    
    # Step 6: Separate features and target
    print("\n[Step 6] Separating features and target...")
    y = df['Appliances'].copy()
    X = df.drop(columns=['Appliances', 'date'])  # Drop date (already used for features)
    print(f"Target (y) shape: {y.shape}")
    print(f"Features (X) before VIF removal: {X.shape}")
    print(f"Features: {X.columns.tolist()}")
    
    # Step 7: Remove high-VIF features
    print("\n[Step 7] Removing high-VIF features for multicollinearity mitigation...")
    X, removed_features = remove_high_vif_features(X, vif_threshold=10)
    print(f"Features (X) after VIF removal: {X.shape}")
    print(f"Final feature list: {X.columns.tolist()}")
    
    print("\n" + "=" * 70)
    print("FEATURE ENGINEERING COMPLETE")
    print("=" * 70)
    
    return X, y


# Main block for independent execution
if __name__ == "__main__":
    # Define path to raw data
    # Assumes script is run from project root directory
    data_path = os.path.join('data', 'raw', 'energydata_complete.csv')
    
    # Check if file exists
    if not os.path.exists(data_path):
        print(f"Error: Data file not found at {data_path}")
        print(f"Current working directory: {os.getcwd()}")
    else:
        # Run feature engineering pipeline
        X, y = build_features(data_path)
        
        # Display final results
        print("\n" + "-" * 70)
        print("FINAL RESULTS")
        print("-" * 70)
        print(f"\nFeature Matrix (X):")
        print(f"  Shape: {X.shape}")
        print(f"  Columns: {X.columns.tolist()}")
        print(f"  Data types:\n{X.dtypes}")
        print(f"\nTarget Vector (y):")
        print(f"  Shape: {y.shape}")
        print(f"  Data type: {y.dtype}")
        print(f"\nFirst few rows of X:")
        print(X.head())
        print(f"\nFirst few values of y:")
        print(y.head())
