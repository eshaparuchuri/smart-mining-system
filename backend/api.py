from flask import Flask, jsonify
from data_simulator.simulator import generate_sequence
from backend.twin import predict
import pandas as pd
import random

app = Flask(__name__)

@app.route("/")
def home():
    return "Smart Mining Digital Twin API Running 🚀"


@app.route("/predict")
def predict_api():

    machine_ids = ["EXCAVATOR_01", "DRILL_02", "TRUCK_03"]

    response = {}
    future_steps = 10

    for machine_id in machine_ids:

        # 🔹 Generate sequence (Digital Twin state simulation)
        sequence = generate_sequence(50)
        latest = sequence.iloc[-1]

        # 🔹 ML Prediction
        prediction = predict(sequence)

        # 🔹 Add controlled randomness (real-world simulation)
        prediction += random.uniform(-0.1, 0.1)
        prediction = max(0, min(1, prediction))

        # 🔹 Rule-based anomaly boost (hybrid twin logic)
        rule_anomaly = (
            latest["temperature"] > 75 or
            latest["vibration"] > 7
        )

        final_score = (prediction + (0.3 if rule_anomaly else 0)) / 1.3

        status = "ANOMALY ⚠️" if final_score > 0.5 else "NORMAL ✅"

        # 🔮 FUTURE FORECAST (Digital Twin projection)
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
            "anomaly": final_score > 0.5,
            "forecast": future
        }

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)