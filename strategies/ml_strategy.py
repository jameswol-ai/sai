# ml_strategy.py
import numpy as np
from sklearn.linear_model import LogisticRegression

class Strategy:
    """
    Example ML strategy plugin.
    Trains a simple logistic regression model to predict BUY/SELL
    based on price features.
    """

    def __init__(self):
        # Dummy training data: price % 2 -> BUY/SELL
        X = np.array([[i] for i in range(100)])
        y = np.array(["BUY" if i % 2 == 0 else "SELL" for i in range(100)])

        self.model = LogisticRegression()
        self.model.fit(X, y)

    def generate_signal(self, market_data):
        # market_data is expected to be a price (float)
        X_test = np.array([[market_data]])
        return self.model.predict(X_test)[0]
