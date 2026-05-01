# sai/bot/main.py
# Entry point for dummy trading bot (WorkflowEngine excluded)

import time
from sai.core.engine import run_trade

def run_bot():
    balance = 10000.0
    positions = []
    history = []

    for i in range(5):  # simulate 5 trades
        result = run_trade(balance, positions)
        balance = result["balance"]
        positions = result["positions"]
        history.append(result)
        print(f"Trade {i+1}: {result}")
        time.sleep(1)

    print("\nFinal Balance:", balance)
    print("Positions:", positions)

if __name__ == "__main__":
    run_bot()
