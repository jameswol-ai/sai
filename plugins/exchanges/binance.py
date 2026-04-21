# plugins/exchanges/binance.py

"""
Binance exchange plugin implementation.
Provides methods to interact with Binance API using the BaseExchange interface.
"""

from binance.client import Client
from binance.exceptions import BinanceAPIException
from .base_exchange import BaseExchange


class BinanceExchange(BaseExchange):
    """
    BinanceExchange implements the BaseExchange interface
    using Binance's official Python client.
    """

    def __init__(self, config: dict):
        super().__init__(config)
        self.client = None

    def connect(self):
        """Authenticate with Binance using API keys."""
        api_key = self.config.get("api_key")
        api_secret = self.config.get("api_secret")
        self.client = Client(api_key, api_secret)

    def get_order_book(self, symbol: str):
        """Retrieve order book for a trading pair."""
        try:
            return self.client.get_order_book(symbol=symbol)
        except BinanceAPIException as e:
            return {"error": str(e)}

    def place_order(self, symbol: str, side: str, quantity: float, price: float = None):
        """Place a buy/sell order (market or limit)."""
        try:
            if price:
                return self.client.create_order(
                    symbol=symbol,
                    side=side.upper(),
                    type="LIMIT",
                    timeInForce="GTC",
                    quantity=quantity,
                    price=str(price),
                )
            else:
                return self.client.create_order(
                    symbol=symbol,
                    side=side.upper(),
                    type="MARKET",
                    quantity=quantity,
                )
        except BinanceAPIException as e:
            return {"error": str(e)}

    def cancel_order(self, order_id: str, symbol: str):
        """Cancel an existing order."""
        try:
            return self.client.cancel_order(symbol=symbol, orderId=order_id)
