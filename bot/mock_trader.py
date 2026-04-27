# sai/bot/mock_trader.py

class MockTrader:
    def __init__(self, broker="alpaca"):
        self.broker = broker

    def execute(self, action, data):
        symbol = data.get("symbol", "TEST")
        qty = data.get("qty", 1)

        if action not in ["BUY", "SELL"]:
            return {"status": "ignored", "action": action}

        # Simulated response
        return {
            "status": "success",
            "broker": self.broker,
            "action": action,
            "symbol": symbol,
            "qty": qty,
            "order_id": "MOCK123"
        }
