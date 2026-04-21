# plugins/indicators/bollinger_bands.py
import statistics

def bollinger_bands(prices, window=20, num_std=2):
    if len(prices) < window:
        return None
    sma = sum(prices[-window:]) / window
    std_dev = statistics.stdev(prices[-window:])
    upper_band = sma + num_std * std_dev
    lower_band = sma - num_std * std_dev
    return upper_band, sma, lower_band
