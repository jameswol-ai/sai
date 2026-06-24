class StrategyPlugin:
    def __init__(self, name):
        self.name = name

    def activate(self):
        # Replace with real strategy activation logic
        print(f"Strategy {self.name} activated")

# Registry of strategy plugins
strategy_plugins = {
    "Momentum": StrategyPlugin("Momentum"),
    "MeanReversion": StrategyPlugin("MeanReversion"),
}
