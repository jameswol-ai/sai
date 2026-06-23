# tests/test_risk_plugins.py
import pytest
from sai.plugins.risk import MaxDrawdownRisk, VolatilityRisk

def test_max_drawdown_risk_trigger():
    risk = MaxDrawdownRisk(threshold=0.1)
    trades = [
        {"price": 100, "pnl": 0},
        {"price": 90, "pnl": -0.1},
        {"price": 85, "pnl": -0.15},
    ]
    assert risk.evaluate(trades) is True

def test_max_drawdown_risk_safe():
    risk = MaxDrawdownRisk(threshold=0.2)
    trades = [
        {"price": 100, "pnl": 0},
        {"price": 95, "pnl": -0.05},
    ]
    assert risk.evaluate(trades) is False

def test_volatility_risk_trigger():
    risk = VolatilityRisk(threshold=0.05)
    prices = [100, 102, 95, 110]
    assert risk.evaluate(prices) is True

def test_volatility_risk_safe():
    risk = VolatilityRisk(threshold=0.2)
    prices = [100, 101, 99, 102]
    assert risk.evaluate(prices) is False
