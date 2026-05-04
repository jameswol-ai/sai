import csv
import os
from datetime import datetime

class PerformanceSnapshot:
    def __init__(self, filepath="data/performance_log.csv"):
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp",
                    "cycle",
                    "price",
                    "signal",
                    "position",
                    "pnl",
                    "balance"
                ])

    def log(self, cycle, price, signal, position, pnl, balance):
        timestamp = datetime.utcnow().isoformat()

        with open(self.filepath, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                cycle,
                price,
                signal,
                position,
                pnl,
                balance
            ])

        return {
            "timestamp": timestamp,
            "cycle": cycle,
            "price": price,
            "signal": signal,
            "position": position,
            "pnl": pnl,
            "balance": balance
        }
