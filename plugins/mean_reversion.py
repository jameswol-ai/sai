"""
Mean Reversion Strategy Plugin for SAI Trading Bot.

This plugin checks whether the current price deviates significantly
from its moving average and generates trading signals based on
mean reversion logic.
"""

from typing import List, Optional
from plugins.moving_average import sma

class MeanReversion:
    def __init__(self, window: int = 20, threshold: float = 0.02):
        """
        Initialize Mean Reversion strategy.
        
        Args:
            window (int): Lookback window for SMA.
            threshold (float): Deviation threshold (e.g., 0.02 = 2%).
        """
        self.window = window
        self.threshold = threshold

    def signal(self, prices: List[float]) -> Optional[str]:
        """
        Generate a trading signal based on mean reversion.
        
        Args:
            prices (List[float]): List of historical prices.
        
        Returns:
            str: "BUY" if price is below SMA by threshold,
                 "SELL" if price is above SMA by threshold,
                 None if no signal.
        """
        ma = sma(prices, window=self.window)
        if ma is None:
            return None

        current_price = prices[-1]
        deviation = (current_price - ma) / ma

        if deviation <= -self.threshold:
            return "BUY"
        elif deviation >= self.threshold:
            return "SELL"
        return None
