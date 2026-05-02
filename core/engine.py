# sai/engine.py

import random

class TradingBot:
    def __init__(self, starting_balance: float = 10000.0, risk: int = 5):
        self.balance = starting_balance
        self.risk = risk
        self.open_trades = []

    def run_once(self):
        """
        Simulates one trading step.
        Returns a string log entry if a trade occurs.
        """
        # Simple random trade simulation
        if random.random() < 0.3:  # 30% chance of trade
            trade = {
                "id": len(self.open_trades) + 1,
                "amount": round(random.uniform(100, 500), 2),
                "direction": random.choice(["BUY", "SELL"])
            }
            self.open_trades.append(trade)
            self.balance += random.uniform(-50, 50)  # simulate PnL impact
            return f"Trade {trade['id']}: {trade['direction']} ${trade['amount']} | Balance: ${self.balance:.2f}"
        else:
            return None
