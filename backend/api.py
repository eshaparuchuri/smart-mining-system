from flask import Flask, jsonify
from data_simulator.simulator import generate_sequence
from backend.twin import predict
import pandas as pd
import random
import requests

app = Flask(__name__)

# ✅ 🔥 DIRECT TELEMETRY URLS (NO CONFUSION NOW)
DEVICE_URLS = {
    "EXCAVATOR_01": "https://thingsboard.cloud/api/v1/m8LfHhnjXpPOxeiHUzAs/telemetry",
    "DRILL_02": "https://thingsboard.cloud/api/v1/eK6tlTtPHtJ5IOMSdDUO/telemetry",
    "TRUCK_03": "https://thingsboard.cloud/api/v1/FnimYZFklxe3Hi86MRL0/telemetry"
}

HEADERS = {
    "Content-Type": "application/json"
}

@app.route("/")
def home():
    return "Smart Mining Digital Twin API Running 🚀"

@app.route("/data")
def data():
    sequence = generate_sequence(50)
    latest = sequence.iloc[-1]

    return jsonify({
        "machine_id": "EXCAVATOR_01",
        "timestamp": str(pd.Timestamp.now()),
        "data": {
            "temperature": float(latest["temperature"]),
            "vibration": float(latest["vibration"]),
            "load": float(latest["load"]),
            "pressure": float(latest["pressure"])
        }
    })

@app.route("/predict")
def predict_api():

    machine_ids = ["EXCAVATOR_01", "DRILL_02", "TRUCK_03"]

    response = {}
    future_steps = 10

    for machine_id in machine_ids:

        # ✅ Get correct URL
        url = DEVICE_URLS[machine_id]

        # 🔹 Generate simulated data
        sequence = generate_sequence(50)
        latest = sequence.iloc[-1]

        # 🔹 ML prediction
        prediction = predict(sequence)

        # 🔹 Add randomness
        prediction += random.uniform(-0.1, 0.1)
        prediction = max(0, min(1, prediction))

        # 🔹 Rule-based anomaly
        rule_anomaly = (
            latest["temperature"] > 75 or
            latest["vibration"] > 7
        )

        final_score = (prediction + (0.3 if rule_anomaly else 0)) / 1.3

        # ✅ TELEMETRY PAYLOAD
        payload = {
            "machine_id": machine_id,
            "temperature": float(latest["temperature"]),
            "vibration": float(latest["vibration"]),
            "load": float(latest["load"]),
            "pressure": float(latest["pressure"]),
            "anomaly": final_score > 0.5,
            "health_score": float(final_score)*100,
        }

        # ✅ SEND DATA
        try:
            res = requests.post(url, json=payload, headers=HEADERS)
            print(f"{machine_id} →", res.status_code, res.text)
        except Exception as e:
            print(f"Error sending data for {machine_id}:", e)

        # 🔹 Status
        status = "ANOMALY ⚠️" if final_score > 0.5 else "NORMAL ✅"

        # 🔮 Future forecast
        future = []
        last = latest.copy()

        for _ in range(future_steps):
            next_point = {
                "temperature": float(last["temperature"] + (final_score * 2)),
                "vibration": float(last["vibration"] + (final_score * 0.2)),
                "load": float(last["load"] + (final_score * 1.5)),
                "pressure": float(last["pressure"] + (final_score * 0.5))
            }
            future.append(next_point)
            last = pd.Series(next_point)

        response[machine_id] = {
            "data": {
                "temperature": float(latest["temperature"]),
                "vibration": float(latest["vibration"]),
                "load": float(latest["load"]),
                "pressure": float(latest["pressure"]),
                "timestamp": str(pd.Timestamp.now())
            },
            "prediction_score": float(final_score),
            "status": status,
            "anomaly": bool(final_score > 0.5),
            "forecast": future
        }

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)

import threading
import time

def auto_push():
    while True:
        try:
            requests.get("http://127.0.0.1:5000/predict")
        except:
            pass
        time.sleep(5)   # sends data every 5 sec

if __name__ == "__main__":
    threading.Thread(target=auto_push).start()
    app.run(debug=True)