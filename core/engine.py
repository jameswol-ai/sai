# sai/core/engine.py

import sai

class TradingBot:
    def __init__(self, starting_balance: float = 10000.0, risk: int = 5):
        self.balance = starting_balance
        self.risk = risk
        self.open_trades = []

    def run_once(self):
        if random.random() < 0.3:
            trade = {
                "id": len(self.open_trades) + 1,
                "amount": round(random.uniform(100, 500), 2),
                "direction": random.choice(["BUY", "SELL"])
            }
            self.open_trades.append(trade)
            self.balance += random.uniform(-50, 50)
            return f"Trade {trade['id']}: {trade['direction']} ${trade['amount']} | Balance: ${self.balance:.2f}"
        return None
