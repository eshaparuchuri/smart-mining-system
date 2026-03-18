import numpy as np
import pandas as pd

def generate_data():
    return {
        "temperature": np.random.normal(60, 5),
        "vibration": np.random.normal(5, 1),
        "load": np.random.normal(70, 10),
        "pressure": np.random.normal(30, 5)
    }

def generate_sequence(seq_len=50):
    data = [generate_data() for _ in range(seq_len)]
    return pd.DataFrame(data)