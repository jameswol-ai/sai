# risk/plugins/stop_loss.py
from .base import RiskPlugin

class StopLossPlugin(RiskPlugin):
    def __init__(self, threshold=0.05):
        self.threshold = threshold

    def check(self, trade, balance):
        entry, price = trade["entry"], trade["price"]
        return (price - entry) / entry > -self.threshold
