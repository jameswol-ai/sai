import os
import logging
import time
from bot.core import SaiBot
from bot.utils import load_config, connect_broker

# --- Logging setup ---
logging.basicConfig(
    filename="logs/live_trading.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def main():
    # Load environment variables
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    broker_url = os.getenv("BROKER_URL")
    mode = os.getenv("MODE", "live")

    if not all([api_key, api_secret, broker_url]):
        raise RuntimeError("Missing broker credentials in .env")

    # Load risk configs
    config = load_config("configs/risk.json")

    # Connect to broker
    broker = connect_broker(api_key, api_secret, broker_url)

    # Initialize Sai bot
    bot = SaiBot(broker=broker, config=config, mode=mode)

    logging.info("Sai live trading started.")

    try:
        while True:
            bot.run_cycle()  # one trading loop
            time.sleep(1)    # throttle loop
    except KeyboardInterrupt:
        logging.info("Sai live trading stopped manually.")
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)

if __name__ == "__main__":
    main()
