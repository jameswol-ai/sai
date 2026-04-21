# plugins/notifications/telegram_notifier.py
"""
Telegram Notifier
-----------------
Implements BaseNotifier for sending notifications via Telegram Bot API.
"""

import requests
from plugins.notifications.base_notifier import BaseNotifier


class TelegramNotifier(BaseNotifier):
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    def _send(self, text: str) -> None:
        """Internal helper to send a message to Telegram."""
        url = f"{self.base_url}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": text}
        response = requests.post(url, json=payload)
        response.raise_for_status()

    def send_message(self, message: str) -> None:
        self._send(f"Notification: {message}")

    def send_alert(self, message: str) -> None:
        self._send(f"🚨 ALERT: {message}")

    def send_error(self, message: str) -> None:
        self._send(f"❌ ERROR: {message}")
