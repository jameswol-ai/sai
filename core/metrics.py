import math

class RollingMetrics:
    def __init__(self):
        self.returns = []
        self.equity_curve = []
        self.last_balance = None

    def update(self, balance):
        if self.last_balance is None:
            self.last_balance = balance
            self.equity_curve.append(balance)
            return self.snapshot()

        ret = (balance - self.last_balance)
        self.returns.append(ret)
        self.last_balance = balance
        self.equity_curve.append(balance)

        return self.snapshot()

    def sharpe(self):
        if len(self.returns) < 2:
            return 0.0
        mean_ret = sum(self.returns) / len(self.returns)
        variance = sum((r - mean_ret) ** 2 for r in self.returns) / (len(self.returns) - 1)
        std = math.sqrt(variance)
        if std == 0:
            return 0.0
        return mean_ret / std

    def win_rate(self):
        if not self.returns:
            return 0.0
        wins = sum(1 for r in self.returns if r > 0)
        return wins / len(self.returns)

    def max_drawdown(self):
        if not self.equity_curve:
            return 0.0
        peak = self.equity_curve[0]
        max_dd = 0.0
        for x in self.equity_curve:
            if x > peak:
                peak = x
            dd = (peak - x)
            if dd > max_dd:
                max_dd = dd
        return max_dd

    def volatility(self):
        if len(self.returns) < 2:
            return 0.0
        mean_ret = sum(self.returns) / len(self.returns)
        variance = sum((r - mean_ret) ** 2 for r in self.returns) / (len(self.returns) - 1)
        return math.sqrt(variance)

    def snapshot(self):
        return {
            "sharpe": round(self.sharpe(), 4),
            "win_rate": round(self.win_rate(), 4),
            "max_drawdown": round(self.max_drawdown(), 4),
            "volatility": round(self.volatility(), 4),
            "trades": len(self.returns)
        }
