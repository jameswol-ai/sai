class RiskPlugin:
    def __init__(self, name, min_val=0, max_val=100, default=50):
        self.name = name
        self.enabled = False
        self.min_val = min_val
        self.max_val = max_val
        self.default = default

    def update(self, enabled, param):
        self.enabled = enabled
        self.param = param

risk_plugins = [
    RiskPlugin("MaxDrawdown"),
    RiskPlugin("StopLoss")
]
