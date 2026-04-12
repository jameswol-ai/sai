from data import get_data
from strategy import SimpleModel
from trader import decide_action

def run():
    df = get_data()

    X = df[["open", "high", "low", "volume"]]
    y = df["close"]

    model = SimpleModel()
    model.train(X[:-1], y[:-1])

    prediction = model.predict(X.tail(1))[0]
    current_price = y.iloc[-1]

    action = decide_action(prediction, current_price)

    print("Prediction:", prediction)
    print("Action:", action)

if __name__ == "__main__":
    run()
