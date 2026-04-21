"""
Integration tests for model integration.

Covers:
- Loading serialized model (model.pkl)
- Making predictions on sample data
- Ensuring predictions trigger trading actions
- End-to-end loop: data → model → trader
"""

import pytest
import pandas as pd
import joblib
from bot.trader import Trader
from bot.strategy import Strategy

MODEL_PATH = "models/model.pkl"

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "close": [100, 102, 101, 105, 107],
        "volume": [1000, 1100, 1200, 1300, 1400],
    })

@pytest.fixture
def model():
    return joblib.load(MODEL_PATH)

@pytest.fixture
def trader():
    return Trader(balance={"USD": 10000, "BTC": 1})

def test_model_loads_correctly(model):
    assert model is not None

def test_model_predicts(sample_data, model):
    preds = model.predict(sample_data[["close", "volume"]])
    assert len(preds) == len(sample_data)
    assert set(preds).issubset({-1, 0, 1})  # short, hold, long

def test_predictions_trigger_trader_actions(sample_data, model, trader):
    preds = model.predict(sample_data[["close", "volume"]])
    for price, signal in zip(sample_data["close"], preds):
        if signal == 1:
            trader.place_order("BUY", amount=0.1, price=price)
        elif signal == -1:
            trader.place_order("SELL", amount=0.1, price=price)
    assert trader.balance["USD"] != 10000 or trader.balance["BTC"] != 1

def test_strategy_and_model_consistency(sample_data, model):
    strategy = Strategy(name="RSI", params={"window": 14})
    signals = strategy.generate_signals(sample_data)
    preds = model.predict(sample_data[["close", "volume"]])
    assert len(signals) == len(preds)
