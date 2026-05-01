class TradingBot:
    def __init__(self):
        self.risk = 0.5

    def decide(self, price: float) -> str:
        # Dummy decision logic
        if price % 2 == 0:
            return "BUY"
        else:
            return "SELL"

    def set_param(self, key, value):
        setattr(self, key, value)
