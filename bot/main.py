# sai/bot/main.py

class TradingBot:
    def __init__(self, risk=0.5):
        self.risk = risk

    def decide(self, price):
        return "BUY" if price % 2 == 0 else "SELL"
