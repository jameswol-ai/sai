class StrategyLearner:
    def __init__(self):
        self.weights = {
            "rsi": 1.0,
            "ma": 1.0,
            "macd": 1.0
        }

    def update(self, signal, pnl):
        # reward good signals, punish bad ones
        for key in signal:
            if pnl > 0:
                self.weights[key] *= 1.05
            else:
                self.weights[key] *= 0.95

    def get_weights(self):
        return self.weights
