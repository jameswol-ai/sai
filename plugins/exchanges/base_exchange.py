# plugins/exchanges/base_exchange.py

"""
Abstract base class for exchange integrations.
Defines the standard interface that all exchange plugins must implement.
"""

from abc import ABC, abstractmethod


class BaseExchange(ABC):
    """
    BaseExchange provides a unified interface for all exchange plugins.
    Concrete implementations (Binance, Coinbase, Kraken, etc.) must
    implement these abstract methods.
    """

    def __init__(self, config: dict):
        """
        Initialize the exchange with configuration parameters.
        Args:
            config (dict): API keys, endpoints, trading pairs, etc.
        """
        self.config = config

    @abstractmethod
    def connect(self):
        """Establish connection/authentication with the exchange API."""
        pass

    @abstractmethod
    def get_order_book(self, symbol: str):
        """
        Retrieve the current order book for a trading pair.
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTC/USDT').
        Returns:
            dict: Order book data (bids, asks).
        """
        pass

    @abstractmethod
    def place_order(self, symbol: str, side: str, quantity: float, price: float = None):
        """
        Place a buy or sell order.
        Args:
            symbol (str): Trading pair symbol.
            side (str): 'buy' or 'sell'.
            quantity (float): Amount to trade.
            price (float, optional): Limit price. If None, place market order.
        Returns:
            dict: Order confirmation details.
        """
        pass

    @abstractmethod
    def cancel_order(self, order_id: str):
        """
        Cancel an existing order.
        Args:
            order_id (str): Unique identifier of the order.
        Returns:
            dict: Cancellation result.
        """
        pass

    @abstractmethod
    def get_balance(self):
        """
        Retrieve account balances.
        Returns:
            dict: Balances per currency.
        """
        pass

    @abstractmethod
    def get_trade_history(self, symbol: str, limit: int = 50):
        """
        Retrieve recent trades for a trading pair.
        Args:
            symbol (str): Trading pair symbol.
            limit (int): Number of trades to fetch.
        Returns:
            list: Trade history entries.
        """
        pass
