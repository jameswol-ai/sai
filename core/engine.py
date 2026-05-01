# sai/core/engine.py

import logging
import random
from datetime import datetime

class WorkflowEngine:
    def __init__(self, buy_threshold=100.0, sell_threshold=105.0):
        self.logger = logging.getLogger("WorkflowEngine")
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler("workflow.log")
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(handler)

        self.balance = 10000.0
        self.positions = []
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold

    def set_thresholds(self, buy, sell):
        self.buy_threshold = buy
        self.sell_threshold = sell
        self.logger.info(f"Thresholds updated: BUY<{buy}, SELL>{sell}")

    def fetch_data(self):
        price = round(random.uniform(90, 110), 2)
        self.logger.info(f"Fetched price: {price}")
        return {"timestamp": datetime.now(), "price": price}

    def decide(self, market_data):
        price = market_data["price"]
        if price < self.buy_threshold:
            decision = "BUY"
        elif price > self.sell_threshold:
            decision = "SELL"
        else:
            decision = "HOLD"
        self.logger.info(f"Decision: {decision} at {price}")
        return decision

    def execute(self, decision, market_data):
        price = market_data["price"]
        if decision == "BUY":
            self.positions.append(price)
            self.balance -= price
        elif decision == "SELL" and self.positions:
            entry = self.positions.pop(0)
            profit = price - entry
            self.balance += price
            self.logger.info(f"Executed SELL. Profit: {profit:.2f}")
        self.logger.info(f"Balance: {self.balance:.2f}, Positions: {self.positions}")

    def run(self, data=None):
        market_data = self.fetch_data()
        decision = self.decide(market_data)
        self.execute(decision, market_data)
        return {
            "decision": decision,
            "price": market_data["price"],
            "balance": self.balance,
            "positions": self.positions,
        }
