import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import pickle

from data_simulator.simulator import generate_sequence

# Generate training data
df = generate_sequence(2000)

scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df)

with open("models/scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

def create_sequences(data, seq_len=50):
    X, y = [], []
    for i in range(len(data) - seq_len):
        X.append(data[i:i+seq_len])
        y.append(data[i+seq_len])
    return np.array(X), np.array(y)

X, y = create_sequences(scaled_data)

model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(X.shape[1], X.shape[2])),
    LSTM(32),
    Dense(4)
])

model.compile(optimizer='adam', loss='mse')
model.fit(X, y, epochs=5, batch_size=32)

model.save("models/lstm_model.h5")

print("LSTM Model Ready ✅")