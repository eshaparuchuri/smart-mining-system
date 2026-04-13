from fastapi import FastAPI
from database.db import SessionLocal, SensorData
import joblib
import numpy as np
from alerts.alert import check_alert
from pydantic import BaseModel

model = load_model("models/lstm_model.h5")
scaler = joblib.load("models/scaler.pkl")

app = FastAPI()

# ✅ Load ML model
model = joblib.load("models/anomaly_model.pkl")  # make sure this file exists

# ✅ Store latest machine status
latest_data = {}

# ✅ Input schema
class SensorInput(BaseModel):
    machine_id: int
    temperature: float
    vibration: float
    load: float
    pressure: float
    timestamp: str

# ✅ ROOT
@app.get("/")
def home():
    return {"message": "Smart Mining System API Running 🚀"}

# ✅ MAIN API (THIS FIXES YOUR 404)
@app.post("/data")
def receive_data(data: SensorInput):
    db = SessionLocal()

    # Convert to dict
    data_dict = data.dict()

    # Save to DB
    db_data = SensorData(**data_dict)
    db.add(db_data)
    db.commit()

    # ML Prediction
    X = np.array([[data.temperature, data.vibration, data.load, data.pressure]])
    pred = model.predict(X)

    anomaly = True if pred[0] == -1 else False

    # Alert check
    check_alert(data_dict, anomaly)

    # Store latest data
    latest_data[data.machine_id] = {
        "data": data_dict,
        "anomaly": anomaly
    }

    print("✅ Received:", data_dict, "Anomaly:", anomaly)

    return {"status": "received", "anomaly": anomaly}

# ✅ STATUS API
@app.get("/status")
def get_status():
    return latest_data