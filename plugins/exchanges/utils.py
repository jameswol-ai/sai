# plugins/indicators/utils.py
"""
Indicator Utilities
-------------------
Helper functions used across indicator modules
(e.g., SMA, RSI, Bollinger Bands, MACD).

Keeps indicator code DRY and consistent.
"""

import numpy as np
import pandas as pd


def validate_series(series) -> pd.Series:
    """
    Ensure input is a Pandas Series.
    Converts lists/arrays to Series if needed.
    """
    if isinstance(series, pd.Series):
        return series
    return pd.Series(series)


def rolling_window(series: pd.Series, window: int) -> pd.Series:
    """
    Apply rolling window with mean.
    Used for moving averages and Bollinger Bands.
    """
    return series.rolling(window=window, min_periods=1)


def normalize(series: pd.Series) -> pd.Series:
    """
    Normalize values between 0 and 1.
    Useful for oscillators like RSI.
    """
    return (series - series.min()) / (series.max() - series.min())


def difference(series: pd.Series, periods: int = 1) -> pd.Series:
    """
    Compute difference between values separated by `periods`.
    Used in momentum indicators.
    """
    return series.diff(periods=periods)


def ema(series: pd.Series, span: int) -> pd.Series:
    """
    Exponential Moving Average (EMA).
    """
    return series.ewm(span=span, adjust=False).mean()
