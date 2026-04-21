"""
Moving Average Indicators for SAI Trading Bot.

Provides functions for calculating:
- Simple Moving Average (SMA)
- Exponential Moving Average (EMA)
"""

from typing import List, Optional

def sma(prices: List[float], window: int = 20) -> Optional[float]:
    """
    Calculate Simple Moving Average (SMA).
    
    Args:
        prices (List[float]): List of price values.
        window (int): Number of periods to average.
    
    Returns:
        float: SMA value, or None if insufficient data.
    """
    if len(prices) < window:
        return None
    return sum(prices[-window:]) / window


def ema(prices: List[float], window: int = 20) -> Optional[float]:
    """
    Calculate Exponential Moving Average (EMA).
    
    Args:
        prices (List[float]): List of price values.
        window (int): Number of periods for EMA.
    
    Returns:
        float: EMA value, or None if insufficient data.
    """
    if len(prices) < window:
        return None
    
    k = 2 / (window + 1)
    ema_values = [prices[0]]
    for price in prices[1:]:
        ema_values.append(price * k + ema_values[-1] * (1 - k))
    return ema_values[-1]
