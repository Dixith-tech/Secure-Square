import joblib
import pandas as pd

model = joblib.load("app/ml/model.pkl")


def detect_anomaly(login_attempts, location_change, device_change):
    data = pd.DataFrame({
        "login_attempts": [login_attempts],
        "location_change": [location_change],
        "device_change": [device_change]
    })

    prediction = model.predict(data)

    return prediction[0]