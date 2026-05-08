import joblib
import pandas as pd
from pathlib import Path

_model_path = Path(__file__).resolve().parent.parent / "ml" / "model.pkl"
model = joblib.load(str(_model_path))


def detect_anomaly(login_attempts, location_change, device_change):
    data = pd.DataFrame({
        "login_attempts": [login_attempts],
        "location_change": [location_change],
        "device_change": [device_change]
    })

    prediction = model.predict(data)

    return prediction[0]