import json
from datetime import datetime
from pathlib import Path

class TradeMemory:
    def __init__(self, path="memory/trade_log.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

        if not self.path.exists():
            self.path.write_text("[]")

    def log(self, trade):
        data = self.load()
        trade["timestamp"] = datetime.utcnow().isoformat()
        data.append(trade)
        self.save(data)

    def load(self):
        return json.loads(self.path.read_text())

    def save(self, data):
        self.path.write_text(json.dumps(data, indent=2))
