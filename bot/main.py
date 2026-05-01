import logging
import sai
from datetime import datetime

class TradingBot:
    def __init__(self, risk=0.5):
        self.risk = risk
        self.trades = []
        self.logger = logging.getLogger("TradingBot")
        self.logger.setLevel(logging.INFO)

    def decide(self, price: float) -> str:
        """Simple placeholder decision logic."""
        action = "BUY" if random.random() < 0.5 else "SELL"
        self.logger.info(f"Decision: {action} at {price}")
        return action

    def execute_trade(self, price: float):
        """Simulate trade execution and record metrics."""
        action = self.decide(price)
        trade = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "price": price,
            "action": action
        }
        self.trades.append(trade)
        return trade

    def get_metrics(self):
        """Return quick metrics for dashboard panels."""
        buys = sum(1 for t in self.trades if t["action"] == "BUY")
        sells = sum(1 for t in self.trades if t["action"] == "SELL")
        return {
            "total_trades": len(self.trades),
            "buys": buys,
            "sells": sells
        }
