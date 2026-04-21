# plugins/exchanges/mock_exchange.py
"""
Mock Exchange Plugin
--------------------
Provides a simulated exchange environment for testing strategies and trader logic
without making real API calls.

Features:
- Static balances
- Configurable prices
- Simple order placement and tracking
"""

import uuid
import random


class MockExchange:
    def __init__(self):
        # Initialize with fake balances
        self.balances = {"USD": 10000.0, "BTC": 2.0}
        self.prices = {"BTC-USD": 50000.0, "ETH-USD": 3000.0}
        self.orders = {}

    def get_balance(self) -> dict:
        """Return current balances."""
        return self.balances

    def get_price(self, pair: str = "BTC-USD") -> float:
        """Return a mock price for the given trading pair."""
        return self.prices.get(pair, random.uniform(100.0, 100000.0))

    def place_order(self, pair: str, side: str, volume: float, price: float) -> dict:
        """Simulate placing an order."""
        order_id = str(uuid.uuid4())
        order = {
            "id": order_id,
            "pair": pair,
            "side": side,
            "volume": volume,
            "price": price,
            "status": "filled",  # Always filled instantly for simplicity
        }
        self.orders[order_id] = order

        # Adjust balances
        if side == "buy":
            cost = volume * price
            if self.balances["USD"] >= cost:
                self.balances["USD"] -= cost
                self.balances["BTC"] += volume
        elif side == "sell":
            if self.balances["BTC"] >= volume:
                self.balances["BTC"] -= volume
                self.balances["USD"] += volume * price

        return order

    def get_order(self, order_id: str) -> dict:
        """Retrieve a simulated order by ID."""
        return self.orders.get(order_id, {})

    def get_order_book(self, pair: str = "BTC-USD") -> dict:
        """Return a fake order book."""
        price = self.get_price(pair)
        return {
            "bids": [[price - 100, 1.0], [price - 200, 2.0]],
            "asks": [[price + 100, 1.0], [price + 200, 2.0]],
        }
