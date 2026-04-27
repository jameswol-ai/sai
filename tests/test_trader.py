# tests/test_trader.py

import pytest
from sai.bot.mock_trader import MockTrader

def test_mock_buy_order():
    trader = MockTrader(broker="alpaca")
    result = trader.execute("BUY", {"symbol": "AAPL", "qty": 10})
    assert result["status"] == "success"
    assert result["action"] == "BUY"
    assert result["symbol"] == "AAPL"

def test_mock_sell_order():
    trader = MockTrader(broker="binance")
    result = trader.execute("SELL", {"symbol": "BTCUSDT", "qty": 0.01})
    assert result["status"] == "success"
    assert result["action"] == "SELL"
    assert result["symbol"] == "BTCUSDT"

def test_mock_invalid_action():
    trader = MockTrader()
    result = trader.execute("HOLD", {"symbol": "TSLA"})
    assert result["status"] == "ignored"
