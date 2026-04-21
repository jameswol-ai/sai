# tests/test_trader.py

import pytest
from bot.trader import decide_action

def test_buy_signal():
    action = decide_action(prediction=105, current_price=100)
    assert action == "BUY"

def test_sell_signal():
    action = decide_action(prediction=95, current_price=100)
    assert action == "SELL"

def test_hold_signal():
    action = decide_action(prediction=100, current_price=100)
    assert action == "HOLD"
