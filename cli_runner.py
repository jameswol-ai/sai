import logging
import sys
import time

from engine import Sai  # adjust import if your bot lives elsewhere

# --- Logging setup ---
logging.basicConfig(
    filename="sai_cli.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def main():
    logging.info("Starting Sai CLI runner...")
    try:
        bot = TradingBot()
        logging.info("TradingBot initialized successfully.")

        while True:
            try:
                # Run one trading cycle
                result = bot.run_cycle()
                print(f"Cycle result: {result}")
                logging.info(f"Cycle result: {result}")

                # Sleep between cycles
                time.sleep(5)

            except Exception as e:
                logging.error(f"Error in trading cycle: {e}", exc_info=True)
                print(f"Error: {e}", file=sys.stderr)
                time.sleep(2)

    except Exception as e:
        logging.critical(f"Fatal error starting Sai: {e}", exc_info=True)
        print(f"Fatal error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
