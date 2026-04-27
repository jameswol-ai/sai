# sai/bot/run_bot.py

import logging
from sai.bot.main import get_data, decide_action, SimpleModel
from sai.bot.trader import Trader   # <-- your execution module

# Configure logging
logging.basicConfig(
    filename="trading.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def run_bot():
    """Main trading loop for SAI bot with execution."""
    logging.info("Starting trading bot...")
    model = SimpleModel()
    trader = Trader()   # initialize broker/exchange connection

    try:
        while True:
            # Fetch market data
            data = get_data()

            # Decide action based on strategy/model
            action = decide_action(model, data)

            # Log and execute action
            logging.info(f"Data: {data} | Action: {action}")
            print(f"Trade decision: {action}")

            if action in ["BUY", "SELL"]:
                result = trader.execute(action, data)
                logging.info(f"Execution result: {result}")
                print(f"Executed: {result}")

    except KeyboardInterrupt:
        logging.info("Bot stopped manually.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}", exc_info=True)

if __name__ == "__main__":
    run_bot()
