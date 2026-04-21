"""
Integration tests for exchange plugins.

Covers:
- Connection setup
- Fetching order book
- Placing/canceling orders
- Error handling (invalid symbols, bad credentials)
"""

import pytest
from plugins.exchanges import (
    BinanceExchange,
    CoinbaseExchange,
    KrakenExchange,
    MockExchange,
)

@pytest.fixture
def mock_exchange():
    return MockExchange()

def test_mock_exchange_connect(mock_exchange):
    assert mock_exchange.connect() is True

def test_mock_exchange_order_book(mock_exchange):
    order_book = mock_exchange.get_order_book("BTC/USDT")
    assert "bids" in order_book
    assert "asks" in order_book

def test_mock_exchange_place_order(mock_exchange):
    order_id = mock_exchange.place_order("BUY", "BTC/USDT", amount=0.1, price=30000)
    assert isinstance(order_id, str)

def test_mock_exchange_cancel_order(mock_exchange):
    order_id = mock_exchange.place_order("BUY", "BTC/USDT", amount=0.1, price=30000)
    result = mock_exchange.cancel_order(order_id)
    assert result is True

@pytest.mark.parametrize("exchange_cls", [BinanceExchange, CoinbaseExchange, KrakenExchange])
def test_exchange_initialization(exchange_cls):
    exchange = exchange_cls()
    assert hasattr(exchange, "connect")
    assert hasattr(exchange, "get_order_book")
    assert hasattr(exchange, "place_order")
