# sai/core/engine.py
# Dummy trading logic engine (WorkflowEngine excluded)

import random

def run_trade(balance=10000.0, positions=None):
    if positions is None:
        positions = []

    decision = random.choice(["BUY", "SELL", "HOLD"])
    price = round(random.uniform(95, 110), 2)

    if decision == "BUY":
        balance -= price
        positions.append(price)
    elif decision == "SELL" and positions:
        positions.pop()
        balance += price
    # HOLD does nothing

    return {
        "decision": decision,
        "price": price,
        "balance": balance,
        "positions": positions.copy()
    }
