import joblib
import numpy as np
from sklearn.linear_model import LinearRegression

class SimpleModel:
    def __init__(self):
        self.model = LinearRegression()

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

# Load model if exists
model = None
try:
    model = joblib.load("models/model.pkl")
    print("Model loaded successfully")
except (FileNotFoundError, EOFError) as e:
    print(f"Model not loaded: {e}")

def get_prediction(features):
    if model is None:
        raise ValueError("Model not loaded")
    return model.predict(features)
