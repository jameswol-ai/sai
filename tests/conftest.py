# tests/conftest.py
import pytest
from unittest.mock import MagicMock
from bot.trader import Trader
from bot.data import DataHandler
from plugins.exchanges.mock_exchange import MockExchange
from plugins.notifications.mock_notifier import MockNotifier

@pytest.fixture
def mock_exchange():
    """Fixture for a mock exchange with fake balances and prices."""
    exchange = MockExchange()
    exchange.get_balance = MagicMock(return_value={"USD": 10000, "BTC": 2})
    exchange.get_price = MagicMock(return_value=50000.0)
    return exchange

@pytest.fixture
def mock_notifier():
    """Fixture for a mock notifier (no external calls)."""
    return MockNotifier()

@pytest.fixture
def data_handler():
    """Fixture for a data handler with sample OHLCV data."""
    return DataHandler(source="tests/configs/mock_data.json")

@pytest.fixture
def trader(mock_exchange, mock_notifier):
    """Fixture for a trader wired with mock exchange + notifier."""
    return Trader(exchange=mock_exchange, notifier=mock_notifier)
