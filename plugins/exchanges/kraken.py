# plugins/exchanges/kraken.py
"""
Kraken Exchange Plugin
----------------------
Provides integration with Kraken's REST API for trading and market data.

Example:
    from plugins.exchanges.kraken import KrakenExchange

    kraken = KrakenExchange(api_key="...", api_secret="...")
    ticker = kraken.get_ticker("XBT/USD")
    order = kraken.place_order("XBT/USD", "buy", 0.01, 30000)
"""

import requests
import time
import hashlib
import hmac
import base64


class KrakenExchange:
    BASE_URL = "https://api.kraken.com"

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

    def _sign(self, urlpath: str, data: dict) -> str:
        """
        Sign request for private endpoints.
        """
        postdata = data
        encoded = (str(data['nonce']) + str(postdata)).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()
        secret = base64.b64decode(self.api_secret)
        signature = hmac.new(secret, message, hashlib.sha512)
        return base64.b64encode(signature.digest())

    def get_ticker(self, pair: str = "XBT/USD") -> dict:
        """
        Get ticker information for a trading pair.
        """
        url = f"{self.BASE_URL}/0/public/Ticker"
        response = requests.get(url, params={"pair": pair})
        response.raise_for_status()
        return response.json()

    def get_order_book(self, pair: str = "XBT/USD", depth: int = 10) -> dict:
        """
        Get order book for a trading pair.
        """
        url = f"{self.BASE_URL}/0/public/Depth"
        response = requests.get(url, params={"pair": pair, "count": depth})
        response.raise_for_status()
        return response.json()

    def place_order(self, pair: str, side: str, volume: float, price: float) -> dict:
        """
        Place a limit order.
        """
        url = f"{self.BASE_URL}/0/private/AddOrder"
        data = {
            "nonce": int(time.time() * 1000),
            "ordertype": "limit",
            "type": side,
            "volume": str(volume),
            "pair": pair,
            "price": str(price),
        }
        headers = {
            "API-Key": self.api_key,
            "API-Sign": self._sign("/0/private/AddOrder", data),
        }
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        return response.json()
