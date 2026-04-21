"""
Market Data Plugin for SAI Trading Bot.

Provides unified access to market data sources (e.g., Binance, Yahoo Finance).
Supports fetching OHLCV (Open, High, Low, Close, Volume) data and streaming updates.
"""

import pandas as pd
import datetime
from typing import Optional, Dict, Any

class MarketData:
    def __init__(self, source: str = "binance", client: Optional[Any] = None):
        """
        Initialize MarketData plugin.
        
        Args:
            source (str): Data source identifier ("binance", "yahoo", etc.)
            client (Any): Optional API client instance (e.g., python-binance client).
        """
        self.source = source
        self.client = client

    def get_historical_data(self, symbol: str, interval: str = "1h", limit: int = 100) -> pd.DataFrame:
        """
        Fetch historical OHLCV data.
        
        Args:
            symbol (str): Trading pair (e.g., "BTCUSDT").
            interval (str): Candle interval (e.g., "1m", "1h", "1d").
            limit (int): Number of data points to fetch.
        
        Returns:
            pd.DataFrame: DataFrame with columns [open, high, low, close, volume, timestamp].
        """
        if self.source == "binance" and self.client:
            klines = self.client.get_klines(symbol=symbol, interval=interval, limit=limit)
            df = pd.DataFrame(klines, columns=[
                "timestamp", "open", "high", "low", "close", "volume",
                "close_time", "quote_asset_volume", "num_trades",
                "taker_buy_base", "taker_buy_quote", "ignore"
            ])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            return df[["timestamp", "open", "high", "low", "close", "volume"]].astype(float)
        
        raise NotImplementedError(f"Source {self.source} not implemented.")

    def get_latest_price(self, symbol: str) -> float:
        """
        Fetch the latest price for a symbol.
        
        Args:
            symbol (str): Trading pair (e.g., "BTCUSDT").
        
        Returns:
            float: Latest price.
        """
        if self.source == "binance" and self.client:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return float(ticker["price"])
        
        raise NotImplementedError(f"Source {self.source} not implemented.")
