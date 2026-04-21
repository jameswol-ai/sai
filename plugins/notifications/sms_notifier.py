# plugins/notifications/sms_notifier.py
"""
SMS Notifier
------------
Implements BaseNotifier for sending notifications via SMS.
Uses Twilio API (or compatible SMS provider).
"""

from plugins.notifications.base_notifier import BaseNotifier
from twilio.rest import Client


class SMSNotifier(BaseNotifier):
    def __init__(self, account_sid: str, auth_token: str, from_number: str, to_number: str):
        self.client = Client(account_sid, auth_token)
        self.from_number = from_number
        self.to_number = to_number

    def _send(self, body: str) -> None:
        """Internal helper to send an SMS message."""
        self.client.messages.create(
            body=body,
            from_=self.from_number,
            to=self.to_number
        )

    def send_message(self, message: str) -> None:
        self._send(f"Notification: {message}")

    def send_alert(self, message: str) -> None:
        self._send(f"ALERT: {message}")

    def send_error(self, message: str) -> None:
        self._send(f"ERROR: {message}")
