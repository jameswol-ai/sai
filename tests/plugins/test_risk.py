"""
Tests for risk control plugins.

Covers:
- Stop-loss plugin
- Take-profit plugin
- Position sizing plugin
- Error handling for invalid inputs
"""

import pytest
import pandas as pd
from plugins.risk_controls import StopLoss, TakeProfit, PositionSizer

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "close": [100, 102, 101, 98, 95],
        "volume": [1000, 1100, 1200, 1300, 1400],
    })

def test_stop_loss_triggers(sample_data):
    sl = StopLoss(threshold=0.05)  # 5% stop-loss
    signals = sl.apply(sample_data)
    assert isinstance(signals, pd.Series)
    assert set(signals.unique()).issubset({0, -1})  # hold or sell

def test_take_profit_triggers(sample_data):
    tp = TakeProfit(threshold=0.05)  # 5% take-profit
    signals = tp.apply(sample_data)
    assert isinstance(signals, pd.Series)
    assert set(signals.unique()).issubset({0, 1})  # hold or buy

def test_position_sizer_valid():
    ps = PositionSizer(balance=10000, risk_pct=0.02, stop_loss=50)
    size = ps.calculate()
    assert isinstance(size, float)
    assert size > 0

def test_position_sizer_invalid_inputs():
    with pytest.raises(ValueError):
        PositionSizer(balance=-1000, risk_pct=0.02, stop_loss=50).calculate()

def test_combined_risk_controls(sample_data):
    sl = StopLoss(threshold=0.05)
    tp = TakeProfit(threshold=0.05)
    signals_sl = sl.apply(sample_data)
    signals_tp = tp.apply(sample_data)
    assert len(signals_sl) == len(signals_tp)
