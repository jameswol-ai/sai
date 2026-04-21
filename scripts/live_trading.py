# scripts/live_trading.py
import argparse
import time
import joblib
from bot.data import get_data
from bot.strategy import get_prediction
from bot.trader import decide_action, execute_trade
from plugins.exchanges.binance import BinanceExchange

MODEL_PATH = "models/model.pkl"

def main():
    parser = argparse.ArgumentParser(description="Run live trading loop")
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Polling interval in seconds"
    )
    args = parser.parse_args()

    # Load trained model
    print("Loading model...")
    model = joblib.load(MODEL_PATH)

    # Initialize exchange client
    config = {
        "api_key": "your_api_key",  # Should be from env
        "api_secret": "your_api_secret"
    }
    exchange = BinanceExchange(config)
    exchange.connect()
    client = exchange.client

    print("Starting live trading loop...")
    while True:
        try:
            # Fetch latest market data
            df = get_data(limit=100)

            # Prepare features (simplified)
            X = df[["open", "high", "low", "volume"]].tail(1)
            current_price = df["close"].iloc[-1]

            # Predict next price
            prediction = model.predict(X)[0]

            # Decide action
            action = decide_action(prediction, current_price)

            # Execute trade if needed
            if action in ["BUY", "SELL"]:
                execute_trade(client, action, current_price)

            print(f"Prediction: {prediction:.2f}, Current: {current_price:.2f}, Action: {action}")

        except Exception as e:
            print(f"Error in live loop: {e}")

        time.sleep(args.interval)

if __name__ == "__main__":
    main()
    main()
