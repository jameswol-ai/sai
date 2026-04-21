"""
Broker API Plugin for SAI Trading Bot.

Provides a standardized interface for interacting with broker/exchange APIs.
Supports placing orders, canceling orders, and checking balances.
"""

from typing import Dict, Any, Optional

class BrokerAPI:
    def __init__(self, client: Any, name: str = "binance"):
        """
        Initialize BrokerAPI.
        
        Args:
            client (Any): API client instance (e.g., python-binance client).
            name (str): Broker/exchange identifier.
        """
        self.client = client
        self.name = name

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None) -> Dict[str, Any]:
        """
        Place an order on the broker.
        
        Args:
            symbol (str): Trading pair (e.g., "BTCUSDT").
            side (str): "BUY" or "SELL".
            order_type (str): "MARKET" or "LIMIT".
            quantity (float): Order quantity.
            price (float, optional): Price for LIMIT orders.
        
        Returns:
            Dict[str, Any]: Order response.
        """
        if self.name == "binance":
            if order_type.upper() == "MARKET":
                return self.client.order_market(symbol=symbol, side=side, quantity=quantity)
            elif order_type.upper() == "LIMIT":
                return self.client.order_limit(symbol=symbol, side=side, quantity=quantity, price=price, timeInForce="GTC")
        raise NotImplementedError(f"Broker {self.name} not implemented.")

    def cancel_order(self, symbol: str, order_id: str) -> Dict[str, Any]:
        """
        Cancel an existing order.
        
        Args:
            symbol (str): Trading pair.
            order_id (str): Order ID to cancel.
        
        Returns:
            Dict[str, Any]: Cancel response.
        """
        if self.name == "binance":
            return self.client.cancel_order(symbol=symbol, orderId=order_id)
        raise NotImplementedError(f"Broker {self.name} not implemented.")

    def get_balance(self, asset: str) -> float:
        """
        Get account balance for a specific asset.
        
        Args:
            asset (str): Asset symbol (e.g., "USDT").
        
        Returns:
            float: Balance amount.
        """
        if self.name == "binance":
            balances = self.client.get_account()["balances"]
            for b in balances:
                if b["asset"] == asset:
                    return float(b["free"])
        raise NotImplementedError(f"Broker {self.name} not implemented.")
