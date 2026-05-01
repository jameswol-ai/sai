# sai/bot/main.py
import TradingBot
import logging

logger = logging.getLogger("sai_streamlit")

class TradingBot:
    def __init__(self):
        # Core parameters
        self.params = {"risk": 0.5}
        self.trades = []
        self.latest_price = None

    def execute_trade(self):
        """Simulate a trade and update state."""
        action = self.decide(random.uniform(90, 110))
        trade = {
            "action": action,
            "amount": random.randint(1, 10),
            "price": round(random.uniform(90, 110), 2)
        }
        self.trades.append(trade)
        self.latest_price = trade["price"]
        logger.info(f"Executed trade: {trade}")
        return trade, self.latest_price

    def decide(self, price: float) -> str:
        """Dummy decision logic based on price parity."""
        return "BUY" if int(price) % 2 == 0 else "SELL"

    def set_param(self, key, value):
        """Update bot parameters dynamically."""
        self.params[key] = value
        logger.info(f"Parameter updated: {key}={value}")

    def get_metrics(self):
        """Return quick metrics for dashboard panel."""
        return {
            "trades_executed": len(self.trades),
            "latest_price": self.latest_price
        }

    def __str__(self):
        return f"TradingBot(params={self.params}, trades={len(self.trades)})"

streamlit run sai/streamlit_app.py
