import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os

# Generate synthetic training data
X = []
for _ in range(1000):
    temp = np.random.uniform(60, 90)
    vib = np.random.uniform(0.1, 0.8)
    load = np.random.uniform(40, 90)
    pressure = np.random.uniform(20, 70)
    X.append([temp, vib, load, pressure])

model = IsolationForest(contamination=0.1)
model.fit(X)

# Create folder if not exists
os.makedirs("model", exist_ok=True)

# Save model in correct path
joblib.dump(model, "model/anomaly_model.pkl")

print("✅ Model trained and saved!")