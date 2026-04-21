"""
Tests for bot.trader module.

Focus:
- Trader class initialization
- Action decision logic
- Order placement and balance updates
- Error handling (invalid actions, insufficient funds)
"""

import pytest
from bot import trader

@pytest.fixture
def sample_trader():
    return trader.Trader(balance={"USD": 10000, "BTC": 1})

def test_trader_class_exists():
    assert hasattr(trader, "Trader")

def test_trader_initialization(sample_trader):
    assert "USD" in sample_trader.balance
    assert "BTC" in sample_trader.balance

def test_decide_action_buy(sample_trader):
    action = sample_trader.decide_action(prediction=105, current_price=100)
    assert action == "BUY"

def test_decide_action_sell(sample_trader):
    action = sample_trader.decide_action(prediction=95, current_price=100)
    assert action == "SELL"

def test_decide_action_hold(sample_trader):
    action = sample_trader.decide_action(prediction=100, current_price=100)
    assert action == "HOLD"

def test_place_buy_order(sample_trader):
    sample_trader.place_order("BUY", amount=0.1, price=10000)
    assert sample_trader.balance["BTC"] > 1
    assert sample_trader.balance["USD"] < 10000

def test_place_sell_order(sample_trader):
    sample_trader.place_order("SELL", amount=0.1, price=10000)
    assert sample_trader.balance["BTC"] < 1
    assert sample_trader.balance["USD"] > 10000

def test_invalid_action_raises_error(sample_trader):
    with pytest.raises(ValueError):
        sample_trader.place_order("INVALID", amount=0.1, price=10000)

def test_insufficient_funds_raises_error(sample_trader):
    with pytest.raises(RuntimeError):
        sample_trader.place_order("SELL", amount=10, price=10000)
