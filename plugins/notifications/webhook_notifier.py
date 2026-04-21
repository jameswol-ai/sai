# plugins/notifications/webhook_notifier.py
"""
Webhook Notifier
----------------
Implements BaseNotifier for sending notifications via generic webhooks.
Useful for integrating with custom services, dashboards, or automation tools.
"""

import requests
from plugins.notifications.base_notifier import BaseNotifier


class WebhookNotifier(BaseNotifier):
    def __init__(self, webhook_url: str, headers: dict = None):
        self.webhook_url = webhook_url
        self.headers = headers or {"Content-Type": "application/json"}

    def _send(self, payload: dict) -> None:
        """Internal helper to send a JSON payload to the webhook."""
        response = requests.post(self.webhook_url, json=payload, headers=self.headers)
        response.raise_for_status()

    def send_message(self, message: str) -> None:
        self._send({"type": "notification", "message": message})

    def send_alert(self, message: str) -> None:
        self._send({"type": "alert", "message": message})

    def send_error(self, message: str) -> None:
        self._send({"type": "error", "message": message})
