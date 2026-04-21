"""
Unit tests for trader module.

Covers:
- Trade decision logic (BUY/SELL/HOLD)
- Order placement
- Balance updates
- Edge cases (invalid inputs, insufficient funds)
"""

import pytest
from bot.trader import Trader

@pytest.fixture
def trader():
    return Trader(balance={"USD": 10000, "BTC": 1})

def test_buy_signal(trader):
    action = trader.decide_action(prediction=105, current_price=100)
    assert action == "BUY"

def test_sell_signal(trader):
    action = trader.decide_action(prediction=95, current_price=100)
    assert action == "SELL"

def test_hold_signal(trader):
    action = trader.decide_action(prediction=100, current_price=100)
    assert action == "HOLD"

def test_place_buy_order(trader):
    trader.place_order("BUY", amount=0.1, price=10000)
    assert trader.balance["BTC"] > 1
    assert trader.balance["USD"] < 10000

def test_place_sell_order(trader):
    trader.place_order("SELL", amount=0.1, price=10000)
    assert trader.balance["BTC"] < 1
    assert trader.balance["USD"] > 10000

def test_invalid_action_raises_error(trader):
    with pytest.raises(ValueError):
        trader.place_order("INVALID", amount=0.1, price=10000)

def test_insufficient_funds(trader):
    with pytest.raises(RuntimeError):
        trader.place_order("SELL", amount=10, price=10000)
