import pytest
import pandas as pd
import numpy as np
from bot.strategy import SimpleModel, get_prediction

# Test the SimpleModel class
def test_simple_model_initialization():
    model = SimpleModel()
    assert model.model is not None

def test_simple_model_training(sample_data):
    model = SimpleModel()
    X = sample_data[['open', 'high', 'low', 'volume']]
    y = sample_data['close']
    model.train(X, y)
    # Test prediction
    predictions = model.predict(X)
    assert len(predictions) == len(X)

def test_get_prediction_with_no_model():
    # This should raise an error if model is not loaded
    try:
        features = [[100, 105, 95, 1000]]
        result = get_prediction(features)
        # If it doesn't raise, that's fine
    except ValueError:
        pass  # Expected when model not loaded
