# sai/bot/run_bot.py

import logging
import yaml
from sai.bot.main import get_data, decide_action, SimpleModel
from sai.bot.trader import Trader

def load_config(path="sai/configs/config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def run_bot():
    # Load config
    config = load_config()

    # Configure logging
    logging.basicConfig(
        filename=config["logging"]["file"],
        level=getattr(logging, config["logging"]["level"]),
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    logging.info("Starting trading bot...")
    model = SimpleModel()
    trader = Trader(broker=config["broker"])

    try:
        while True:
            for symbol in config["symbols"]:
                # Fetch market data
                data = get_data(symbol=symbol)

                # Decide action
                action = decide_action(model, data)

                # Log and execute
                logging.info(f"Symbol: {symbol} | Data: {data} | Action: {action}")
                print(f"{symbol} decision: {action}")

                if action in ["BUY", "SELL"]:
                    data["symbol"] = symbol
                    data["qty"] = config["position_sizing"]["default_qty"]
                    result = trader.execute(action, data)
                    logging.info(f"Execution result: {result}")
                    print(f"Executed: {result}")

    except KeyboardInterrupt:
        logging.info("Bot stopped manually.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}", exc_info=True)

if __name__ == "__main__":
    run_bot()
