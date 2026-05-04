import logging
import sys
import time
import csv
import os

from engine import Sai  # adjust import if needed

# --- Logging setup ---
logging.basicConfig(
    filename="sai_cli.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

CSV_FILE = "trades.csv"

def append_to_csv(result: dict):
    """Append trading cycle result to CSV file."""
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=result.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(result)

def main():
    logging.info("Starting Sai CLI runner with CSV export...")
    try:
        bot = TradingBot()
        logging.info("TradingBot initialized successfully.")

        while True:
            try:
                # Run one trading cycle
                result = bot.run_cycle()  # expect dict like {"timestamp":..., "trade":..., "profit":...}
                print(f"Cycle result: {result}")
                logging.info(f"Cycle result: {result}")

                # Save to CSV
                if isinstance(result, dict):
                    append_to_csv(result)

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
