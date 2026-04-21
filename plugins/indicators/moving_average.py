SIMPLE MOVING INDICATORS

# plugins/indicators/moving_average.py
def sma(prices, window=20):
    if len(prices) < window:
        return None
    return sum(prices[-window:]) / window
