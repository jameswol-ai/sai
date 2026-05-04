import random
import time

class SimulatedBroker:
    def __init__(
        self,
        starting_balance=1000.0,
        spread=0.02,            # 2 cents spread
        slippage_pct=0.0005,    # 0.05% slippage
        latency_ms=80,          # 80ms latency
        fill_probability=0.98   # 98% chance order fills
    ):
        self.balance = starting_balance
        self.position = 0
        self.entry_price = None

        self.spread = spread
        self.slippage_pct = slippage_pct
        self.latency_ms = latency_ms
        self.fill_probability = fill_probability

        self.last_price = 100.0

    def get_price(self):
        # Simulate small random walk
        change = random.uniform(-0.2, 0.2)
        self.last_price += change
        return round(self.last_price, 4)

    def _apply_latency(self):
        time.sleep(self.latency_ms / 1000)

    def _apply_spread(self, price, side):
        if side == "BUY":
            return price + self.spread
        elif side == "SELL":
            return price - self.spread
        return price

    def _apply_slippage(self, price):
        slip = price * self.slippage_pct
        direction = random.choice([-1, 1])
        return price + (direction * slip)

    def _order_fills(self):
        return random.random() <= self.fill_probability

    def execute(self, signal):
        price = self.get_price()

        if signal == "HOLD":
            pnl = 0
            return self.position, pnl, self.balance

        self._apply_latency()

        # Spread + slippage
        exec_price = self._apply_spread(price, signal)
        exec_price = self._apply_slippage(exec_price)

        if not self._order_fills():
            # No fill → no position change
            pnl = 0
            return self.position, pnl, self.balance

        # BUY
        if signal == "BUY":
            if self.position == 0:
                self.position = 1
                self.entry_price = exec_price
            pnl = 0

        # SELL
        elif signal == "SELL":
            if self.position == 1:
                pnl = exec_price - self.entry_price
                self.balance += pnl
                self.position = 0
                self.entry_price = None
            else:
                pnl = 0

        return self.position, pnl, self.balance
