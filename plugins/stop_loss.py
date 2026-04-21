"""
Stop-Loss Plugin for SAI Trading Bot.

Provides functionality to calculate and enforce stop-loss levels
based on fixed percentage or volatility-based rules.
"""

from typing import Optional
import pandas as pd

class StopLoss:
    def __init__(self, stop_loss_pct: float = 0.02):
        """
        Initialize StopLoss plugin.
        
        Args:
            stop_loss_pct (float): Fixed stop-loss percentage (e.g., 0.02 = 2%).
        """
        self.stop_loss_pct = stop_loss_pct

    def calculate_level(self, entry_price: float, direction: str = "LONG") -> float:
        """
        Calculate stop-loss level for a trade.
        
        Args:
            entry_price (float): Price at which trade was entered.
            direction (str): "LONG" or "SHORT".
        
        Returns:
            float: Stop-loss price level.
        """
        if direction.upper() == "LONG":
            return entry_price * (1 - self.stop_loss_pct)
        elif direction.upper() == "SHORT":
            return entry_price * (1 + self.stop_loss_pct)
        else:
            raise ValueError("Direction must be 'LONG' or 'SHORT'.")

    def check_trigger(self, current_price: float, stop_loss_level: float, direction: str = "LONG") -> Optional[str]:
        """
        Check if stop-loss should be triggered.
        
        Args:
            current_price (float): Current market price.
            stop_loss_level (float): Predefined stop-loss level.
            direction (str): "LONG" or "SHORT".
        
        Returns:
            str: "EXIT" if stop-loss triggered, None otherwise.
        """
        if direction.upper() == "LONG" and current_price <= stop_loss_level:
            return "EXIT"
        elif direction.upper() == "SHORT" and current_price >= stop_loss_level:
            return "EXIT"
        return None
