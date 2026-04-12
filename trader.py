def decide_action(prediction, current_price):
    if prediction > current_price:
        return "BUY"
    elif prediction < current_price:
        return "SELL"
    return "HOLD"
