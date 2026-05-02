# sai/core/engine.py

class Sai:
    """
    Minimal trading bot stub for Streamlit integration.
    """

    def __init__(self, starting_balance: float = 10000.0, risk: int = 5):
        self.balance = starting_balance
        self.risk = risk
        self.open_trades = []
        self._counter = 0  # internal counter instead of random

    def run_once(self):
        """
        Simulates one trading step deterministically.
        Every 3rd call opens a trade.
        """
        self._counter += 1
        if self._counter % 3 == 0:
            trade = {
                "id": len(self.open_trades) + 1,
                "amount": 100 + 50 * (self._counter % 5),  # simple pattern
                "direction": "BUY" if self._counter % 2 == 0 else "SELL"
            }
            self.open_trades.append(trade)
            # balance oscillates up/down
            self.balance += (-25 if self._counter % 2 else 25)
            return f"Trade {trade['id']}: {trade['direction']} ${trade['amount']} | Balance: ${self.balance:.2f}"
        return None
