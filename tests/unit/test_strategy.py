"""
Unit tests for strategy module.

Covers:
- Signal generation (buy/sell/hold)
- Indicator calculations
- Edge cases (empty data, NaN values)
"""

import pytest
import pandas as pd
from bot.strategy import Strategy

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "close": [100, 102, 101, 105, 107],
        "volume": [1000, 1100, 1200, 1300, 1400],
    })

@pytest.fixture
def strategy():
    return Strategy(name="RSI", params={"window": 14, "overbought": 70, "oversold": 30})

def test_strategy_initialization(strategy):
    assert strategy.name == "RSI"
    assert "window" in strategy.params

def test_generate_signals(strategy, sample_data):
    signals = strategy.generate_signals(sample_data)
    assert isinstance(signals, pd.Series)
    assert set(signals.unique()).issubset({-1, 0, 1})  # short, hold, long

def test_empty_data(strategy):
    empty_df = pd.DataFrame({"close": [], "volume": []})
    signals = strategy.generate_signals(empty_df)
    assert signals.empty

def test_nan_handling(strategy):
    df = pd.DataFrame({"close": [100, None, 102], "volume": [1000, 1100, 1200]})
    signals = strategy.generate_signals(df)
    assert not signals.isnull().any()
