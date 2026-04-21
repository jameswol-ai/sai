"""
Tests for bot.strategy module.

Focus:
- Strategy class initialization
- Parameter validation
- Signal generation logic
"""

import pytest
import pandas as pd
from bot import strategy

def test_strategy_class_exists():
    assert hasattr(strategy, "Strategy")

def test_strategy_init_with_params():
    s = strategy.Strategy(name="EMA", params={"window": 10})
    assert s.name == "EMA"
    assert s.params["window"] == 10

def test_generate_signals_returns_series():
    s = strategy.Strategy(name="EMA", params={"window": 3})
    df = pd.DataFrame({"close": [100, 102, 101, 105, 107]})
    signals = s.generate_signals(df)
    assert isinstance(signals, pd.Series)
    assert set(signals.unique()).issubset({-1, 0, 1})

def test_invalid_params_raise_error():
    with pytest.raises(ValueError):
        strategy.Strategy(name="EMA", params={"window": -5})

def test_empty_dataframe_returns_empty_series():
    s = strategy.Strategy(name="EMA", params={"window": 3})
    df = pd.DataFrame({"close": []})
    signals = s.generate_signals(df)
    assert signals.empty
