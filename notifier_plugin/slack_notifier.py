import requests
from .base_notifier import BaseNotifier

class SlackNotifier(BaseNotifier):
    def __init__(self, webhook_url):
        super().__init__("Slack")
        self.webhook_url = webhook_url

    def send(self, message):
        payload = {"text": message}
        requests.post(self.webhook_url, json=payload)

    def test_ping(self):
        self.send("Test ping from SAI cockpit ✅")
