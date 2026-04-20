import os
import pandas as pd

api_key = os.getenv("API_KEY")

from data import get_data
from strategy import SimpleModel
from trader import decide_action

def backtest():
    # Load historical data
    df = get_data()

    # Features and target
    X = df[["open", "high", "low", "volume"]]
    y = df["close"]

    # Initialize model
    model = SimpleModel()

    # Track results
    actions = []
    predictions = []
    balance = 10000  # starting capital
    position = 0     # number of shares held

    # Walk-forward backtesting
    for i in range(50, len(df)):  # start after 50 rows to have training data
        X_train, y_train = X.iloc[:i], y.iloc[:i]
        X_test, y_test = X.iloc[i:i+1], y.iloc[i:i+1]

        # Train model on past data
        model.train(X_train, y_train)

        # Predict next close
        prediction = model.predict(X_test)[0]
        current_price = y_test.iloc[0]

        # Decide action
        action = decide_action(prediction, current_price)

        # Simulate trade
        if action == "BUY" and balance >= current_price:
            position += 1
            balance -= current_price
        elif action == "SELL" and position > 0:
            position -= 1
            balance += current_price

        predictions.append(prediction)
        actions.append(action)

    # Final portfolio value
    final_value = balance + position * y.iloc[-1]

    print("Final Portfolio Value:", final_value)
    print("Total Actions Taken:", len(actions))
    print("Sample Actions:", actions[:10])

if __name__ == "__main__":
    backtest()
