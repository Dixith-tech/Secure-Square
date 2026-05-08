import joblib
import pandas as pd
from pathlib import Path

_model_path = Path(__file__).resolve().parent.parent / "ml" / "model.pkl"

# Lazy-load the model for faster serverless cold starts
_model = None

def _get_model():
    global _model
    if _model is None:
        _model = joblib.load(str(_model_path))
    return _model


def detect_anomaly(login_attempts, location_change, device_change):
    model = _get_model()
    data = pd.DataFrame({
        "login_attempts": [login_attempts],
        "location_change": [location_change],
        "device_change": [device_change]
    })

    prediction = model.predict(data)

    return prediction[0]