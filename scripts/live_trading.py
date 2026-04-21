# scripts/live_trading.py
import argparse
import time
import joblib
from bot.data import get_data
from bot.strategy import SimpleModel
from bot.trader import decide_action, execute_trade
from plugins.exchanges import binance

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
    model: SimpleModel = joblib.load(MODEL_PATH)

    # Initialize exchange client
    client = binance.get_client()

    print("Starting live trading loop...")
    while True:
        try:
            # Fetch latest market data
            df = get_data(client=client, limit=100)

            X = df[["open", "high", "low", "volume"]]
            y = df["close"]

            # Predict next price
            prediction = model.predict(X.tail(1))[0]
            current_price = y.iloc[-1]

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
