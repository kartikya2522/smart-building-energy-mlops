# Streamlit Cloud Deployment Guide

## For Streamlit Cloud (streamlit.app)

If deploying to Streamlit Cloud, follow these steps:

### 1. Ensure `requirements.txt` Exists
The project has `requirements.txt` in the root directory with all dependencies, including:
- `joblib==1.5.3` ✅
- `scikit-learn==1.7.2` ✅
- `streamlit>=1.28.0` ✅
- `plotly>=5.17.0` ✅
- `pandas>=2.0.0` ✅
- `numpy>=1.24.0` ✅

Streamlit Cloud will automatically install from this file.

### 2. Alternative: Use `requirements_streamlit.txt`
For a minimal deployment with only essential dependencies:
```bash
streamlit run app.py --logger.level=debug
```

### 3. Verify in Streamlit Cloud
- Go to **Streamlit Cloud** (https://share.streamlit.io)
- Connect your GitHub repository
- Select the branch (main)
- Set the main file path: `app.py`
- Advanced settings → Requirements file: `requirements.txt` (default)
- Click "Deploy"

### 4. If ModuleNotFoundError Occurs

**Local Testing:**
```bash
# Install from requirements_streamlit.txt for minimal setup
pip install -r requirements_streamlit.txt

# Or from main requirements.txt
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

**On Streamlit Cloud:**
- Check app logs (click "Manage app" → "View logs")
- Verify `requirements.txt` is in the repository root
- Try redeploying (Settings → Reboot app)

### 5. Manual Installation (if needed)
```bash
python install_dependencies.py
```

## File Structure for Deployment

```
smart-building-energy-mlops/
├── app.py                          # Main Streamlit app
├── requirements.txt                # Full requirements (used by default)
├── requirements_streamlit.txt      # Minimal Streamlit requirements
├── pyproject.toml                  # Alternative dependency declaration
├── install_dependencies.py         # Manual installation script
├── .streamlit/
│   └── config.toml                # Streamlit configuration
├── models/
│   ├── ridge_model.pkl            # Trained model
│   └── feature_names.json         # Feature names mapping
├── src/
│   ├── data/
│   ├── features/
│   │   └── build_features.py
│   └── models/
│       ├── train.py
│       └── evaluate.py
├── data/
│   ├── raw/
│   │   └── energydata_complete.csv
│   └── processed/
└── notebooks/
    └── 01_eda.ipynb
```

## Troubleshooting

### Issue: ModuleNotFoundError for joblib
**Solution:** Ensure `requirements.txt` includes `joblib==1.5.3`

### Issue: FileNotFoundError for feature_names.json
**Solution:** Already fixed - uses absolute path with `Path(__file__).parent`

### Issue: Model file not found
**Solution:** Verify `models/ridge_model.pkl` exists in the repository

### Issue: Slow first load
**Solution:** Model is cached with `@st.cache_resource` - first load will be slow (~2-3s), subsequent predictions <500ms

## Environment Variables (if needed)

Create `.streamlit/secrets.toml` in your local repo (not committed):
```toml
# Example secrets file (not needed for basic deployment)
model_path = "models/ridge_model.pkl"
```

## Docker Deployment (Alternative)

A `Dockerfile` is included for Docker-based deployments:
```bash
docker build -t smart-building-energy-app .
docker run -p 8501:8501 smart-building-energy-app
```

## Support

For issues:
1. Check `.streamlit/config.toml` for configuration
2. Review `requirements_streamlit.txt` for minimal dependencies
3. Verify all model files are committed to git
4. Check Streamlit Cloud logs for detailed error messages
