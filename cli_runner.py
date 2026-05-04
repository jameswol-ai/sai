import logging
import sys
import time
import csv
import os
import argparse
from statistics import mean

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

def show_summary():
    """Read trades.csv and print quick stats."""
    if not os.path.isfile(CSV_FILE):
        print("No trades.csv found yet.")
        return

    with open(CSV_FILE, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("No trade data available.")
        return

    profits = [float(r["profit"]) for r in rows if "profit" in r and r["profit"]]
    print(f"Total trades: {len(rows)}")
    print(f"Total profit: {sum(profits):.2f}")
    print(f"Average profit per trade: {mean(profits):.2f}")
    print(f"Max profit: {max(profits):.2f}")
    print(f"Min profit: {min(profits):.2f}")

def run_bot():
    logging.info("Starting Sai CLI runner with CSV export...")
    try:
        bot = TradingBot()
        logging.info("TradingBot initialized successfully.")

        while True:
            try:
                result = bot.run_cycle()  # expect dict like {"timestamp":..., "trade":..., "profit":...}
                print(f"Cycle result: {result}")
                logging.info(f"Cycle result: {result}")

                if isinstance(result, dict):
                    append_to_csv(result)

                time.sleep(5)

            except Exception as e:
                logging.error(f"Error in trading cycle: {e}", exc_info=True)
                print(f"Error: {e}", file=sys.stderr)
                time.sleep(2)

    except Exception as e:
        logging.critical(f"Fatal error starting Sai: {e}", exc_info=True)
        print(f"Fatal error: {e}", file=sys.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sai CLI Runner")
    parser.add_argument("--summary", action="store_true", help="Show summary stats from trades.csv")
    args = parser.parse_args()

    if args.summary:
        show_summary()
    else:
        run_bot()
