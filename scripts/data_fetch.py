# scripts/data_fetch.py
import argparse
import pandas as pd
from datetime import datetime
from plugins.market_data import get_market_data

def main():
    parser = argparse.ArgumentParser(description="Fetch market data and save to CSV")
    parser.add_argument(
        "--symbol",
        type=str,
        default="BTCUSDT",
        help="Trading pair symbol (e.g., BTCUSDT)"
    )
    parser.add_argument(
        "--interval",
        type=str,
        default="1h",
        help="Data interval (e.g., 1m, 5m, 1h, 1d)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=500,
        help="Number of data points to fetch"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/fetched_data.csv",
        help="Path to save CSV file"
    )
    args = parser.parse_args()

    print(f"Fetching {args.limit} candles for {args.symbol} at {args.interval} interval...")
    df = get_market_data(symbol=args.symbol, interval=args.interval, limit=args.limit)

    # Ensure DataFrame has proper datetime index
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)

    # Save to CSV
    df.to_csv(args.output)
    print(f"Data saved to {args.output} at {datetime.now()}")

if __name__ == "__main__":
    main()
