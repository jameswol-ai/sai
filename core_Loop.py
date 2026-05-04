import time
import logging
from datetime import datetime

class SaiCoreLoop:
    def __init__(self, bot, metrics, csv_exporter, sleep_time=1.0):
        self.bot = bot
        self.metrics = metrics
        self.csv_exporter = csv_exporter
        self.sleep_time = sleep_time
        self.running = False

    def start(self, on_update=None):
        """
        on_update: callback for UI updates (Streamlit)
        """
        self.running = True
        logging.info("SAI core loop started")

        while self.running:
            try:
                price = self.bot.get_price()
                action, trade = self.bot.step(price)

                # Update metrics
                self.metrics.update(price, trade)

                # Export to CSV
                self.csv_exporter.write_row({
                    "timestamp": datetime.utcnow().isoformat(),
                    "price": price,
                    "action": action,
                    "trade": trade,
                    "balance": self.metrics.balance,
                    "pnl": self.metrics.pnl
                })

                # Streamlit callback
                if on_update:
                    on_update(price, action, trade, self.metrics)

                time.sleep(self.sleep_time)

            except Exception as e:
                logging.exception(f"Error in SAI core loop: {e}")
                time.sleep(1)

        logging.info("SAI core loop stopped")

    def stop(self):
        self.running = False
