# sai/bot/run_bot.py

import logging
import yaml
import argparse
from sai.bot.main import get_data, decide_action, SimpleModel
from sai.bot.trader import Trader
from sai.bot.mock_trader import MockTrader

def load_config(path="sai/configs/config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def run_bot(dry_run=False):
    config = load_config()

    # Configure logging
    logging.basicConfig(
        filename=config["logging"]["file"],
        level=getattr(logging, config["logging"]["level"]),
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    logging.info("Starting trading bot...")
    model = SimpleModel()

    # Dependency injection: choose trader class
    if dry_run or config.get("mode") == "test":
        trader = MockTrader(broker=config["broker"])
    else:
        trader = Trader(broker=config["broker"])

    try:
        while True:
            for symbol in config["symbols"]:
                data = get_data(symbol=symbol)
                action = decide_action(model, data)

                logging.info(f"Symbol: {symbol} | Data: {data} | Action: {action}")
                print(f"{symbol} decision: {action}")

                if action in ["BUY", "SELL"]:
                    data["symbol"] = symbol
                    data["qty"] = config["position_sizing"]["default_qty"]
                    result = trader.execute(action, data)
                    logging.info(f"Result: {result}")
                    print(f"Result: {result}")

    except KeyboardInterrupt:
        logging.info("Bot stopped manually.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}", exc_info=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SAI trading bot")
    parser.add_argument("--dry-run", action="store_true", help="Simulate trades without broker API calls")
    args = parser.parse_args()

    run_bot(dry_run=args.dry_run)
