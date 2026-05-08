import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# Example dataset

data = {
    "login_attempts": [1, 2, 3, 50, 2, 1, 70],
    "location_change": [0, 0, 0, 1, 0, 0, 1],
    "device_change": [0, 0, 0, 1, 0, 0, 1]
}


df = pd.DataFrame(data)

model = IsolationForest(contamination=0.2)
model.fit(df)

joblib.dump(model, "app/ml/model.pkl")

print("Model trained successfully")