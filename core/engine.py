from datetime import datetime

class TradingEngine:
    def __init__(self):
        self.trades = []

    def record_trade(self, trade):
        self.trades.append(trade)

    def current_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"TradingEngine(trades={len(self.trades)})"
