import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data(num_rows=1000):
    """Generate synthetic OHLCV data for training/testing."""
    np.random.seed(42)

    # Start from a recent date
    start_date = datetime(2023, 1, 1)

    # Generate timestamps
    timestamps = [start_date + timedelta(hours=i) for i in range(num_rows)]

    # Generate synthetic price data
    prices = []
    current_price = 50000  # Starting BTC price

    for i in range(num_rows):
        # Random walk with some trend
        change = np.random.normal(0, 0.01)  # 1% volatility
        current_price *= (1 + change)
        prices.append(current_price)

    # Create OHLCV from prices
    data = []
    for i, price in enumerate(prices):
        # Add some noise to create OHLC
        high = price * (1 + abs(np.random.normal(0, 0.005)))
        low = price * (1 - abs(np.random.normal(0, 0.005)))
        open_price = prices[i-1] if i > 0 else price
        volume = np.random.uniform(100, 1000)

        data.append({
            'timestamp': timestamps[i],
            'open': open_price,
            'high': high,
            'low': low,
            'close': price,
            'volume': volume
        })

    df = pd.DataFrame(data)

    # Create target: 1 if next close > current close, 0 otherwise
    df['target'] = (df['close'].shift(-1) > df['close']).astype(int)

    # Drop last row (no target)
    df = df.dropna()

    return df

if __name__ == "__main__":
    # Generate training data
    train_df = generate_sample_data(800)
    train_df.to_csv('data/train.csv', index=False)

    # Generate test data
    test_df = generate_sample_data(200)
    test_df.to_csv('data/test.csv', index=False)

    # Generate backtest data
    backtest_df = generate_sample_data(500)
    backtest_df.to_csv('data/backtest_data.csv', index=False)

    print("Sample data generated:")
    print("- data/train.csv")
    print("- data/test.csv")
    print("- data/backtest_data.csv")