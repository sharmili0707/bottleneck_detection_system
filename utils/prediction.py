import pickle
import numpy as np

# Load model
with open("models/model.pkl", "rb") as f:
    model = pickle.load(f)

def predict_bottleneck(values):
    values = np.array(values).reshape(1, -1)
    prediction = model.predict(values)[0]

    return prediction