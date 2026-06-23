import requests
from .base_notifier import BaseNotifier

class PagerDutyNotifier(BaseNotifier):
    def __init__(self, routing_key):
        super().__init__("PagerDuty")
        self.routing_key = routing_key

    def send(self, message):
        payload = {
            "routing_key": self.routing_key,
            "event_action": "trigger",
            "payload": {
                "summary": message,
                "severity": "error",
                "source": "SAI cockpit"
            }
        }
        requests.post("https://events.pagerduty.com/v2/enqueue", json=payload)

    def test_ping(self):
        self.send("Test ping from SAI cockpit ✅")
