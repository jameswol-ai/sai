# sai# sai/bot/run_bot.py

import logging
import yaml
import argparse
from sai.bot.main import get_data, decide_action, SimpleModel

class Trader:
    def __init__(self, broker):
        self.broker = broker
    def execute(self, action, data):
        return {"action": action, "data": data, "status": "executed"}

class MockTrader(Trader):
    def execute(self, action, data):
        return {"action": action, "data": data, "status": "mock executed"}

def load_config(path="sai/configs/config.yaml"):
    # Safe default config if file missing
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {
            "logging": {"file": "bot.log", "level": "INFO"},
            "broker": "demo",
            "symbols": ["TEST"],
            "position_sizing": {"default_qty": 1},
            "mode": "test"
        }

def run_bot(dry_run=False):
    config = load_config()

    logging.basicConfig(
        filename=config["logging"]["file"],
        level=getattr(logging, config["logging"]["level"]),
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    logging.info("Starting trading bot...")
    model = SimpleModel()

    trader = MockTrader(config["broker"]) if dry_run or config.get("mode") == "test" else Trader(config["broker"])

    for symbol in config["symbols"]:
        data = get_data(symbol=symbol)
        action = decide_action(model, data)
        logging.info(f"Symbol: {symbol} | Data: {data} | Action: {action}")
        if action in ["BUY", "SELL"]:
            data["qty"] = config["position_sizing"]["default_qty"]
            result = trader.execute(action, data)
            logging.info(f"Result: {result}")
            print(f"Result: {result}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SAI trading bot")
    parser.add_argument("--dry-run", action="store_true", help="Simulate trades without broker API calls")
    args = parser.parse_args()
    run_bot(dry_run=args.dry_run)
