# plugins/exchanges/__init__.py

"""
Exchange plugins package initializer.
Provides unified imports for supported exchange integrations.
"""

from .base_exchange import BaseExchange
from .binance import BinanceExchange

__all__ = [
    "BaseExchange",
    "BinanceExchange"
]
