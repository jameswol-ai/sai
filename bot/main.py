import random
import sai

snap, metrics, chart = engine.run_cycle()

print(
    f"[{snap['cycle']}] "
    f"Price: {snap['price']} | "
    f"Signal: {snap['signal']} | "
    f"PnL: {snap['pnl']} | "
    f"Bal: {snap['balance']} | "
    f"Sharpe: {metrics['sharpe']} | "
    f"WinRate: {metrics['win_rate']}"
)

print(chart)

def get_data():
    """Simulate fetching a price feed (replace with real API)."""
    return round(100 + random.uniform(-1, 1), 2)

def run_bot(engine, price):
    """Run a simple trading decision (replace with strategy logic)."""
    decision = "BUY" if price < 100 else "SELL"
    trade = {"time": engine.current_time(), "price": price, "decision": decision}
    engine.record_trade(trade)
    return trade
