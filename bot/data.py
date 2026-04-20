import ccxt
import pandas as pd

def get_data(symbol="BTC/USDT", limit=100):
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe="1h", limit=limit)

    df = pd.DataFrame(ohlcv, columns=[
        "timestamp", "open", "high", "low", "close", "volume"
    ])
    return df
