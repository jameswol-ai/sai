# plugins/exchanges/__init__.py

"""
Exchange plugins package initializer.
Provides unified imports for supported exchange integrations.
"""

from .base_exchange import BaseExchange
from .binance import BinanceExchange
from .coinbase import CoinbaseExchange
from .kraken import KrakenExchange
from .mock_exchange import MockExchange

__all__ = [
    "BaseExchange",
    "BinanceExchange",
    "CoinbaseExchange",
    "KrakenExchange",
    "MockExchange",
]
