# sai/bot/main.py

import logging
from sai.utils import setup_logger

logger = setup_logger("sai_bot")

class SimpleModel:
    """Basic demo model for trading decisions."""
    def predict(self, data):
        if not data:
            return "HOLD"
        avg = sum(data) / len(data)
        return "BUY" if avg > 0 else "SELL"

def get_data():
    """Stub for fetching market data. Replace with real pipeline later."""
    return [10, -5, 15, 20, -2]

def decide_action(data):
    """Decide trading action based on average value."""
    if not data:
        return "HOLD"
    avg = sum(data) / len(data)
    if avg > 5:
        return "BUY"
    elif avg < -5:
        return "SELL"
    return "HOLD"

def run_bot():
    """Run the trading bot once."""
    data = get_data()
    action = decide_action(data)
    logger.info(f"Bot decided action: {action}")
    return action
    
