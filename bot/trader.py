def decide_action(prediction, current_price):
    if prediction > current_price:
        return "BUY"
    elif prediction < current_price:
        return "SELL"
    return "HOLD"

def execute_trade(client, action, price, quantity=0.001):
    """Execute a trade on the exchange."""
    if action == "BUY":
        # Place buy order
        order = client.create_order(
            symbol="BTCUSDT",
            side="BUY",
            type="MARKET",
            quantity=quantity
        )
        print(f"Placed BUY order: {order}")
    elif action == "SELL":
        # Place sell order
        order = client.create_order(
            symbol="BTCUSDT",
            side="SELL",
            type="MARKET",
            quantity=quantity
        )
        print(f"Placed SELL order: {order}")
    else:
        print("No trade executed (HOLD)")

def get_balance(client):
    """Get account balance."""
    return client.get_account()

def get_positions(client):
    """Get current positions."""
    return client.get_account()["balances"]
