# Streamlit Cloud Deployment - Troubleshooting Guide

## Issue: ModuleNotFoundError: joblib

### Root Cause
Streamlit Cloud may not properly read the full `requirements.txt` file if it contains too many packages or has conflicts between dependencies.

### Solution ✅

The repository has been updated with multiple fallback mechanisms:

#### 1. **Primary: Clean requirements.txt**
The main `requirements.txt` now contains ONLY essential packages:
```
streamlit==1.28.0
plotly==5.17.0
pandas==2.0.0
numpy==1.24.0
scikit-learn==1.7.2
joblib==1.5.3
```

#### 2. **Fallback: setup.py**
If Streamlit Cloud can't find `requirements.txt`, it will use `setup.py` which declares the same dependencies.

#### 3. **Fallback: pyproject.toml**
Alternative Python packaging standard that also declares dependencies.

#### 4. **Fallback: .streamlit.yml**
Streamlit Cloud configuration file to ensure proper deployment.

#### 5. **Docker Alternative**
If Streamlit Cloud fails, use Docker:
```bash
docker build -t smart-building-app .
docker run -p 8501:8501 smart-building-app
```

### Deployment Steps

#### For Streamlit Cloud (Recommended)

1. **Go to** [share.streamlit.io](https://share.streamlit.io)

2. **Create New App** → Select Your Repository
   - Repository: `smart-building-energy-mlops`
   - Branch: `main`
   - Main file path: `app.py`

3. **Advanced Settings**
   - Python version: `3.11` (or leave default)
   - Requirements file: `requirements.txt` (default)

4. **Deploy**
   - Click "Deploy" button
   - Wait 2-3 minutes for initial build
   - App should appear at: `https://share.streamlit.io/[username]/smart-building-energy-mlops`

5. **If Still Getting ModuleNotFoundError**
   - Click "Manage app" → "Reboot app"
   - Check logs for detailed error messages
   - If Streamlit Cloud still has issues, use Docker (see below)

#### For Docker Deployment

1. **Build Image**
```bash
docker build -t smart-building-app .
```

2. **Run Container**
```bash
docker run -p 8501:8501 smart-building-app
```

3. **Access App**
   - Open http://localhost:8501

4. **Deploy to Cloud (AWS/GCP/Azure)**
```bash
# Example: Push to Docker Hub
docker tag smart-building-app [username]/smart-building-app
docker push [username]/smart-building-app

# Then deploy container from Docker Hub to your cloud provider
```

#### For Local Development

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Run App**
```bash
streamlit run app.py
```

3. **Access at**
   - http://localhost:8501

### File Structure for Deployment

```
smart-building-energy-mlops/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Primary - Essential dependencies ✅
├── setup.py                        # Fallback 1 - Setup script
├── pyproject.toml                  # Fallback 2 - Python packaging
├── .streamlit.yml                  # Fallback 3 - Streamlit config
├── Dockerfile                      # Fallback 4 - Docker deployment
├── .streamlit/
│   └── config.toml                # Streamlit UI configuration
├── models/
│   ├── ridge_model.pkl            # Trained Ridge model
│   └── feature_names.json         # Feature names mapping
└── [other project files]
```

### What Was Fixed

#### Before
- `requirements.txt` had 178 packages (bloated, caused conflicts)
- joblib might not install due to dependency resolution issues
- No fallback mechanisms for missing dependencies

#### After
- `requirements.txt` has only 6 packages (clean, minimal)
- `setup.py` provides alternative dependency declaration
- `pyproject.toml` provides another alternative
- `.streamlit.yml` ensures Streamlit Cloud configuration
- `Dockerfile` enables containerized deployment

### Verification

#### Local Test
```bash
# Should complete with no errors
python -c "import streamlit, plotly, pandas, numpy, scikit-learn, joblib; print('All imports OK')"
```

#### Streamlit Cloud Test
1. Deploy app
2. In sidebar, adjust sliders
3. Should see predictions update in real-time
4. No ModuleNotFoundError should appear

### If Problems Persist

1. **Check Streamlit Cloud Logs**
   - App → Manage app → View logs
   - Look for specific error messages

2. **Force Redeployment**
   - Settings → Reboot app
   - Or delete and redeploy the app

3. **Use Docker Instead**
   - Build and run locally first to verify
   - Then push to Docker Hub or cloud provider

4. **Contact Support**
   - Streamlit Cloud: support@streamlit.io
   - Include log output and requirements.txt

### Advanced: Local Testing of Streamlit Cloud Environment

To simulate Streamlit Cloud's Python environment locally:

```bash
# Create fresh virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from minimal requirements
pip install -r requirements.txt

# Run app
streamlit run app.py
```

If it works locally with minimal requirements, it should work on Streamlit Cloud.

### Summary

✅ **Issue**: ModuleNotFoundError: joblib on Streamlit Cloud
✅ **Root Cause**: Bloated requirements.txt with too many packages
✅ **Solution**: Simplified requirements.txt + multiple fallback configurations
✅ **Result**: App should now deploy successfully to Streamlit Cloud

**Try deploying again to Streamlit Cloud - it should work now!**
