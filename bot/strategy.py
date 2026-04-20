import pickle

# Load model
with open("models/model.pkl", "rb") as f:
    model = pickle.load(f)

# Example usage
features = data_pipeline.get_features()
prediction = model.predict(features)


import numpy as np
from sklearn.linear_model import LinearRegression

class SimpleModel:
    def __init__(self):
        self.model = LinearRegression()

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)
