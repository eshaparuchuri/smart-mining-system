import numpy as np
import pickle
from tensorflow.keras.models import load_model

model = load_model("models/lstm_model.h5", compile=False)

with open("models/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

def predict(data):
    scaled = scaler.transform(data)
    reshaped = np.reshape(scaled, (1, scaled.shape[0], scaled.shape[1]))
    prediction = model.predict(reshaped)
    return float(prediction[0][0])