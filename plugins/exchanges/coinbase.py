# plugins/indicators/coinbase.py
"""
Coinbase Market Data Plugin
---------------------------
Provides helper functions to fetch price and market data from Coinbase API
for use in indicators and strategies.

Example:
    from plugins.indicators import coinbase
    price = coinbase.get_spot_price("BTC-USD")
"""

import requests

BASE_URL = "https://api.coinbase.com/v2"


def get_spot_price(pair: str = "BTC-USD") -> float:
    """
    Fetch the current spot price for a given trading pair.

    Args:
        pair (str): Trading pair symbol, e.g. "BTC-USD"

    Returns:
        float: Current spot price
    """
    url = f"{BASE_URL}/prices/{pair}/spot"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return float(data["data"]["amount"])


def get_historic_rates(pair: str = "BTC-USD", granularity: int = 3600):
    """
    Fetch historical rates for a given trading pair.

    Args:
        pair (str): Trading pair symbol, e.g. "BTC-USD"
        granularity (int): Candle size in seconds (60, 300, 900, 3600, 21600, 86400)

    Returns:
        list: List of OHLCV candles [time, low, high, open, close, volume]
    """
    url = f"https://api.exchange.coinbase.com/products/{pair}/candles"
    params = {"granularity": granularity}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
