RELATIVE STRENGTH INDEX

# plugins/indicators/rsi.py
def rsi(prices, window=14):
    if len(prices) < window + 1:
        return None
    gains = []
    losses = []
    for i in range(1, window+1):
        delta = prices[-i] - prices[-i-1]
        gains.append(max(delta, 0))
        losses.append(abs(min(delta, 0)))
    avg_gain = sum(gains) / window
    avg_loss = sum(losses) / window
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))
