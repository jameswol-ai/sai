# plugins/notifications/slack_notifier.py
"""
Slack Notifier
--------------
Implements BaseNotifier for sending notifications to Slack channels
using incoming webhooks.
"""

import requests
from plugins.notifications.base_notifier import BaseNotifier


class SlackNotifier(BaseNotifier):
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def _send(self, text: str) -> None:
        """Internal helper to send a message to Slack."""
        payload = {"text": text}
        response = requests.post(self.webhook_url, json=payload)
        response.raise_for_status()

    def send_message(self, message: str) -> None:
        self._send(f"Notification: {message}")

    def send_alert(self, message: str) -> None:
        self._send(f":rotating_light: ALERT: {message}")

    def send_error(self, message: str) -> None:
        self._send(f":x: ERROR: {message}")
