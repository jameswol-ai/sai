import pytest
import pandas as pd
import numpy as np
import os
from bot.strategy import Strategy

# 1. Setup a fixture to initialize the strategy
@pytest.fixture
def strategy():
    # Points to the model you have in your repo structure
    model_path = os.path.join("models", "model.pkl")
    # Note: For testing, ensure a dummy model.pkl exists or mock the loader
    return Strategy(model_path=model_path)

# 2. Test if the strategy loads the model correctly
def test_model_loading(strategy):
    assert strategy.model is not None, "Model failed to load."

# 3. Test the 'Hold' logic (when data is insufficient or neutral)
def test_neutral_market_behavior(strategy):
    # Creating a dummy dataframe with flat prices
    data = pd.DataFrame({
        'close': [100, 100, 100, 100, 100],
        'volume': [0, 0, 0, 0, 0]
    })
    signal = strategy.analyze(data)
    # Ensure it returns None or "HOLD" instead of a random trade
    assert signal is None or signal == "HOLD"

# 4. Test the 'Buy' signal logic
def test_buy_signal_generation(strategy, monkeypatch):
    # We "monkeypatch" the model's predict method to force a 'Buy' (e.g., 1)
    def mock_predict(features):
        return np.array([1]) 
    
    monkeypatch.setattr(strategy.model, "predict", mock_predict)
    
    data = pd.DataFrame({'close': [100, 101, 102], 'volume': [10, 20, 30]})
    signal = strategy.analyze(data)
    
    assert signal == "BUY", f"Expected BUY signal, got {signal}"

# 5. Test handling of empty or corrupt data
def test_empty_data_handling(strategy):
    empty_data = pd.DataFrame()
    with pytest.raises(ValueError): # Or however your strategy handles errors
        strategy.analyze(empty_data)
