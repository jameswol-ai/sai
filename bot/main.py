import random
import sai

def get_data():
    """Simulate fetching a price feed (replace with real API)."""
    return round(100 + random.uniform(-1, 1), 2)

def run_bot(engine, price):
    """Run a simple trading decision (replace with strategy logic)."""
    decision = "BUY" if price < 100 else "SELL"
    trade = {"time": engine.current_time(), "price": price, "decision": decision}
    engine.record_trade(trade)
    return trade
