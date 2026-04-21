MOVING AVERAGE CONVERGENCE DIVERGENCE

# plugins/indicators/macd.py
def ema(prices, window):
    k = 2 / (window + 1)
    ema_values = [prices[0]]
    for price in prices[1:]:
        ema_values.append(price * k + ema_values[-1] * (1 - k))
    return ema_values

def macd(prices, short_window=12, long_window=26, signal_window=9):
    if len(prices) < long_window:
        return None
    short_ema = ema(prices, short_window)
    long_ema = ema(prices, long_window)
    macd_line = [s - l for s, l in zip(short_ema[-len(long_ema):], long_ema)]
    signal_line = ema(macd_line, signal_window)
    return macd_line[-1], signal_line[-1]
