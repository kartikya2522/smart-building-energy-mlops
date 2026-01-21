"""
Smart Building Energy Prediction - Streamlit Application

This application uses a trained Ridge Regression model to predict building energy consumption
based on environmental factors. It provides real-time predictions, cost estimation, and 
sustainability impact analysis.

Features:
- Interactive sidebar for input parameters
- Real-time energy consumption prediction
- Cost and CO₂ emissions calculation
- Interactive visualizations using Plotly
- Sustainability impact explanation
- Professional KPI-style layout

Run with: streamlit run app.py

Author: ML Pipeline
Date: 2025
"""
import json
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# Load feature names from JSON file
feature_names_path = Path(__file__).parent / "models" / "feature_names.json"
with open(feature_names_path, "r") as f:
    FEATURE_NAMES = json.load(f)

# Page configuration
st.set_page_config(
    page_title="Smart Building Energy Prediction",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .metric-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .header-container {
        text-align: center;
        padding: 20px 0;
        margin-bottom: 30px;
    }
    .sustainability-section {
        background-color: #e8f5e9;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #4caf50;
    }
    .prediction-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_resource
def load_model():
    """
    Load the pre-trained Ridge Regression model from disk.
    
    Model is cached to avoid reloading on every interaction.
    
    Returns:
    --------
    model : Ridge
        Trained Ridge Regression model
    """
    model_path = Path(__file__).parent / "models" / "ridge_model.pkl"
    
    if not model_path.exists():
        st.error(f"❌ Model file not found at: {model_path}")
        st.stop()
    
    try:
        model = joblib.load(model_path)
        return model
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        st.stop()


def create_features_from_inputs(rh_6, windspeed, visibility, tdewpoint, rv1, hour):
    """
    Create required features for the model from user inputs.
    
    This function generates engineered features including cyclical hour encoding
    (hour_sin, hour_cos) that are expected by the trained model.
    
    Parameters:
    -----------
    rh_6 : float
        Relative Humidity at 6 PM (%)
    windspeed : float
        Wind speed (km/h)
    visibility : float
        Visibility (km)
    tdewpoint : float
        Dew point temperature (°C)
    rv1 : float
        Relative Humidity (%)
    hour : int
        Hour of day (0-23)
        
    Returns:
    --------
    features_array : np.ndarray
        Array with features in correct order for model prediction
    """
    # Create cyclical hour encoding
    # sine and cosine transformations preserve circular nature of hours
    hour_sin = np.sin(2 * np.pi * hour / 24)
    hour_cos = np.cos(2 * np.pi * hour / 24)
    
    # Create feature array in the order expected by the model
    # Order must match: ["RH_6", "Windspeed", "Visibility", "Tdewpoint", "rv1", "hour", "hour_sin", "hour_cos"]
    features_array = np.array([rh_6, windspeed, visibility, tdewpoint, rv1, hour, hour_sin, hour_cos])
    
    return features_array


def predict_energy(model, features_array):
    """
    Predict energy consumption using the trained model.
    
    The model expects features in a specific order. This function handles
    feature ordering and returns the prediction.
    
    Parameters:
    -----------
    model : Ridge
        Trained Ridge Regression model
    features_array : np.ndarray
        Array of feature values in correct order
        
    Returns:
    --------
    prediction : float
        Predicted energy consumption in Wh
    """
    # Reshape for model prediction (1 sample, 8 features)
    feature_array = features_array.reshape(1, -1)
    
    # Convert to DataFrame with proper feature names to suppress sklearn warnings
    feature_df = pd.DataFrame(
        feature_array,
        columns=FEATURE_NAMES
    )
    
    # Make prediction
    prediction = model.predict(feature_df)[0]
    
    # Ensure prediction is non-negative
    prediction = max(0, prediction)
    
    return prediction


def calculate_cost(energy_wh, cost_per_kwh=6):
    """
    Calculate energy cost in Indian Rupees (₹).
    
    Parameters:
    -----------
    energy_wh : float
        Energy consumption in Watt-hours
    cost_per_kwh : float
        Cost per kilowatt-hour in ₹ (default: 6)
        
    Returns:
    --------
    cost : float
        Energy cost in ₹
    """
    energy_kwh = energy_wh / 1000  # Convert Wh to kWh
    cost = energy_kwh * cost_per_kwh
    return cost


def calculate_co2_emissions(energy_wh, emission_factor=0.82):
    """
    Calculate CO₂ emissions from energy consumption.
    
    Uses the Indian energy mix emission factor.
    
    Parameters:
    -----------
    energy_wh : float
        Energy consumption in Watt-hours
    emission_factor : float
        CO₂ emissions in kg per kWh (default: 0.82 for India)
        
    Returns:
    --------
    co2_kg : float
        CO₂ emissions in kilograms
    """
    energy_kwh = energy_wh / 1000  # Convert Wh to kWh
    co2_kg = energy_kwh * emission_factor
    return co2_kg


def create_hourly_prediction_chart(model):
    """
    Create an interactive Plotly chart showing energy predictions across all hours.
    
    This visualization helps understand how energy consumption varies throughout the day
    for the given temperature, humidity, and wind speed conditions.
    
    Parameters:
    -----------
    model : Ridge
        Trained Ridge Regression model
        
    Returns:
    --------
    fig : plotly.graph_objects.Figure
        Interactive Plotly figure
    """
    # Get current input values from sidebar
    rh_6 = st.session_state.get('rh_6', 60)
    windspeed = st.session_state.get('windspeed', 5)
    visibility = st.session_state.get('visibility', 10)
    tdewpoint = st.session_state.get('tdewpoint', 10)
    rv1 = st.session_state.get('rv1', 50)
    
    # Generate predictions for each hour
    hours = np.arange(0, 24)
    predictions = []
    
    for h in hours:
        features = create_features_from_inputs(
            rh_6, windspeed, visibility, tdewpoint, rv1, h
        )
        energy = predict_energy(model, features)
        predictions.append(energy)
    
    # Create interactive Plotly figure
    fig = go.Figure()
    
    # Add main line
    fig.add_trace(go.Scatter(
        x=hours,
        y=predictions,
        mode='lines+markers',
        name='Energy Prediction',
        line=dict(color='#667eea', width=3),
        marker=dict(size=8, color='#667eea'),
        hovertemplate='<b>Hour %{x}:00</b><br>Energy: %{y:.2f} Wh<extra></extra>'
    ))
    
    # Add shaded area under the curve
    fig.add_trace(go.Scatter(
        x=hours,
        y=predictions,
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Highlight current hour
    current_hour = st.session_state.get('hour', 12)
    fig.add_vline(
        x=current_hour,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Current Hour: {current_hour}",
        annotation_position="top right"
    )
    
    # Update layout
    fig.update_layout(
        title={
            'text': "Energy Consumption Prediction - 24 Hour Profile",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18}
        },
        xaxis=dict(
            title='Hour of Day',
            tickmode='linear',
            tick0=0,
            dtick=1
        ),
        yaxis=dict(title='Energy (Wh)'),
        hovermode='x unified',
        template='plotly_white',
        height=400,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    return fig


def create_comparison_chart(energy_wh, cost, co2):
    """
    Create a gauge chart comparing energy metrics.
    
    Parameters:
    -----------
    energy_wh : float
        Energy in Wh
    cost : float
        Cost in ₹
    co2 : float
        CO₂ in kg
        
    Returns:
    --------
    fig : plotly.graph_objects.Figure
        Gauge chart
    """
    # Create subplots for three gauges
    fig = go.Figure()
    
    # Energy gauge
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=energy_wh,
        title={'text': "Energy (Wh)"},
        delta={'reference': 100},
        gauge={'axis': {'range': [0, 200]},
               'bar': {'color': '#667eea'},
               'steps': [
                   {'range': [0, 50], 'color': '#e8eaf6'},
                   {'range': [50, 150], 'color': '#c5cae9'},
                   {'range': [150, 200], 'color': '#5e35b1'}],
               'threshold': {
                   'line': {'color': 'red', 'width': 4},
                   'thickness': 0.75,
                   'value': 150}},
        domain={'x': [0, 0.33], 'y': [0, 1]}
    ))
    
    # Cost gauge
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=cost,
        title={'text': "Cost (₹)"},
        gauge={'axis': {'range': [0, 1.5]},
               'bar': {'color': '#4caf50'},
               'steps': [
                   {'range': [0, 0.3], 'color': '#e8f5e9'},
                   {'range': [0.3, 1.0], 'color': '#a5d6a7'},
                   {'range': [1.0, 1.5], 'color': '#2e7d32'}]},
        domain={'x': [0.33, 0.66], 'y': [0, 1]}
    ))
    
    # CO₂ gauge
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=co2,
        title={'text': "CO₂ (kg)"},
        gauge={'axis': {'range': [0, 0.2]},
               'bar': {'color': '#ff9800'},
               'steps': [
                   {'range': [0, 0.05], 'color': '#fff3e0'},
                   {'range': [0.05, 0.15], 'color': '#ffe0b2'},
                   {'range': [0.15, 0.2], 'color': '#e65100'}]},
        domain={'x': [0.66, 1], 'y': [0, 1]}
    ))
    
    fig.update_layout(
        template='plotly_white',
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig


def main():
    """
    Main application function that orchestrates the Streamlit UI and predictions.
    """
    
    # Header
    st.markdown("""
        <div class="header-container">
            <h1>⚡ Smart Building Energy Prediction</h1>
            <p style="color: #666; font-size: 16px;">
                Predict energy consumption and sustainability impact using AI
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Load model
    model = load_model()
    
    # ========================================================================
    # SIDEBAR: Input Controls
    # ========================================================================
    st.sidebar.header("📊 Input Parameters")
    st.sidebar.markdown("---")
    
    # RH_6 input (Relative Humidity at 6 PM)
    rh_6 = st.sidebar.slider(
        "💧 Relative Humidity at 6 PM (%)",
        min_value=0.0,
        max_value=100.0,
        value=60.0,
        step=1.0,
        help="Relative humidity measurement at 6 PM"
    )
    st.session_state.rh_6 = rh_6
    
    # Wind Speed input
    windspeed = st.sidebar.slider(
        "💨 Wind Speed (m/s)",
        min_value=0.0,
        max_value=20.0,
        value=5.0,
        step=0.5,
        help="Wind speed in meters per second"
    )
    st.session_state.windspeed = windspeed
    
    # Visibility input
    visibility = st.sidebar.slider(
        "👁️ Visibility (km)",
        min_value=0.0,
        max_value=50.0,
        value=10.0,
        step=0.5,
        help="Visibility distance in kilometers"
    )
    st.session_state.visibility = visibility
    
    # Dew point temperature input
    tdewpoint = st.sidebar.slider(
        "🌡️ Dew Point Temperature (°C)",
        min_value=-20.0,
        max_value=35.0,
        value=10.0,
        step=0.5,
        help="Dew point temperature in Celsius"
    )
    st.session_state.tdewpoint = tdewpoint
    
    # Relative Humidity input (rv1)
    rv1 = st.sidebar.slider(
        "💧 Relative Humidity (%)",
        min_value=0.0,
        max_value=100.0,
        value=50.0,
        step=1.0,
        help="General relative humidity as percentage"
    )
    st.session_state.rv1 = rv1
    
    # Hour input
    hour = st.sidebar.slider(
        "🕐 Hour of Day",
        min_value=0,
        max_value=23,
        value=12,
        step=1,
        help="Hour of day (0-23, where 0 is midnight)"
    )
    st.session_state.hour = hour
    
    st.sidebar.markdown("---")
    
    # Information box in sidebar
    with st.sidebar.expander("ℹ️ How It Works", expanded=False):
        st.write("""
        This application uses a trained Ridge Regression model to predict
        building energy consumption based on environmental factors:
        
        - **Humidity & Temperature**: External weather conditions
        - **Wind Speed & Visibility**: Atmospheric conditions
        - **Hour of Day**: Captures daily usage patterns
        
        The model generates real-time predictions and calculates associated costs
        and environmental impact.
        """)
    
    # ========================================================================
    # MAIN CONTENT: Predictions and Visualizations
    # ========================================================================
    
    # Create features from user inputs
    features = create_features_from_inputs(rh_6, windspeed, visibility, tdewpoint, rv1, hour)
    
    # Make prediction
    predicted_energy = predict_energy(model, features)
    
    # Calculate cost and emissions
    cost_rupees = calculate_cost(predicted_energy, cost_per_kwh=6)
    co2_emissions = calculate_co2_emissions(predicted_energy, emission_factor=0.82)
    
    # ========================================================================
    # SECTION 1: KPI Metrics
    # ========================================================================
    st.header("📈 Prediction Results")
    
    # Create three columns for metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="⚡ Predicted Energy",
            value=f"{predicted_energy:.2f}",
            delta="Wh",
            delta_color="off"
        )
    
    with col2:
        st.metric(
            label="💰 Estimated Cost",
            value=f"₹ {cost_rupees:.2f}",
            delta="per unit",
            delta_color="off"
        )
    
    with col3:
        st.metric(
            label="🌱 CO₂ Emissions",
            value=f"{co2_emissions:.4f}",
            delta="kg",
            delta_color="inverse"
        )
    
    st.markdown("---")
    
    # ========================================================================
    # SECTION 2: Interactive Visualizations
    # ========================================================================
    st.header("📊 Visualizations")
    
    # Create two columns for visualizations
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Hourly prediction chart
        st.subheader("24-Hour Energy Profile")
        hourly_chart = create_hourly_prediction_chart(model)
        st.plotly_chart(hourly_chart, use_container_width=True)
    
    with col2:
        # Comparison gauges
        st.subheader("Metrics Overview")
        st.write("")  # Add spacing
        comparison_fig = create_comparison_chart(predicted_energy, cost_rupees, co2_emissions)
        st.plotly_chart(comparison_fig, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # SECTION 3: Input Summary
    # ========================================================================
    st.header("🔍 Current Input Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("""
        **Weather Conditions:**
        - Humidity (6 PM): {:.1f} %
        - Wind Speed: {:.1f} m/s
        - Visibility: {:.1f} km
        - Dew Point: {:.1f} °C
        """.format(rh_6, windspeed, visibility, tdewpoint))
    
    with col2:
        st.write("""
        **Other Factors:**
        - Relative Humidity (rv1): {:.1f} %
        - Hour of Day: {} ({}:00)
        """.format(rv1, hour, f"{hour:02d}"))
    
    st.markdown("---")
    
    # ========================================================================
    # SECTION 4: Sustainability Impact
    # ========================================================================
    st.header("🌍 Sustainability Impact")
    
    st.markdown("""
        <div class="sustainability-section">
        <h3>Understanding the Environmental Impact</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # Calculate key metrics
    daily_energy = predicted_energy * 24  # Extrapolate to daily
    daily_cost = calculate_cost(daily_energy, cost_per_kwh=6)
    daily_co2 = calculate_co2_emissions(daily_energy, emission_factor=0.82)
    
    monthly_energy = daily_energy * 30
    monthly_cost = daily_cost * 30
    monthly_co2 = daily_co2 * 30
    
    # Display impact information
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write(f"""
        **Daily Impact (Projected)**
        - Energy: {daily_energy:.2f} Wh
        - Cost: ₹ {daily_cost:.2f}
        - CO₂: {daily_co2:.4f} kg
        """)
    
    with col2:
        st.write(f"""
        **Monthly Impact (Projected)**
        - Energy: {monthly_energy:.2f} Wh
        - Cost: ₹ {monthly_cost:.2f}
        - CO₂: {monthly_co2:.4f} kg
        """)
    
    with col3:
        # Tree equivalent
        trees_to_offset = monthly_co2 / 20  # 1 tree absorbs ~20kg CO₂/year
        st.write(f"""
        **Environmental Equivalents**
        - Trees needed to offset: {trees_to_offset:.2f}
        - Equivalent driving: {monthly_co2 * 10:.2f} km
        - Light bulbs (60W/hr): {monthly_energy / 60:.2f} hours
        """)
    
    st.markdown("""
        <div class="sustainability-section">
        <h4>💡 Sustainability Tips</h4>
        <ul>
            <li><strong>Peak Hours (9-18):</strong> Utilize natural lighting and ventilation during daylight</li>
            <li><strong>Off-Peak Hours:</strong> Schedule heavy machinery during early morning or evening</li>
            <li><strong>Temperature Control:</strong> Optimize HVAC settings based on outdoor conditions</li>
            <li><strong>Renewable Energy:</strong> Consider solar panels to offset CO₂ emissions</li>
            <li><strong>Smart Controls:</strong> Use automation to reduce energy waste</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================================================
    # SECTION 5: Model Information
    # ========================================================================
    with st.expander("ℹ️ Model Information", expanded=False):
        st.write("""
        **Model Details:**
        - **Algorithm:** Ridge Regression
        - **Purpose:** Predict building energy consumption based on environmental factors
        - **Features:** Outdoor temperature, humidity, wind speed, hour of day
        - **Training Data:** Smart building IoT sensor data
        - **Output:** Energy consumption in Watt-hours (Wh)
        
        **How Predictions Work:**
        1. Environmental inputs are collected via the sidebar
        2. Cyclical features (sin/cos) are generated for hour of day
        3. All features are passed to the Ridge model
        4. Model outputs predicted energy consumption
        5. Cost and CO₂ are calculated based on the prediction
        
        **Cost Calculation:**
        - Energy Cost (₹) = Energy (kWh) × 6 (₹/kWh)
        
        **CO₂ Calculation:**
        - CO₂ Emissions (kg) = Energy (kWh) × 0.82 (kg/kWh)
        - Factor represents Indian energy grid emission intensity
        """)
    
    # Footer
    st.markdown("""
        <hr style="border: none; height: 1px; background-color: #e0e0e0; margin: 30px 0;">
        <p style="text-align: center; color: #999; font-size: 12px;">
            Smart Building Energy Prediction System | Powered by Ridge Regression ML Model
        </p>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
