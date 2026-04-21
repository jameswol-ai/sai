# plugins/notifications/mock_notifier.py
"""
Mock Notifier
-------------
Implements BaseNotifier for testing purposes.
Instead of sending real notifications, it logs/prints them.
"""

from plugins.notifications.base_notifier import BaseNotifier


class MockNotifier(BaseNotifier):
    def __init__(self):
        self.sent_messages = []

    def _record(self, category: str, message: str) -> None:
        """Internal helper to record a message."""
        entry = {"category": category, "message": message}
        self.sent_messages.append(entry)
        print(f"[MOCK {category.upper()}] {message}")

    def send_message(self, message: str) -> None:
        self._record("notification", message)

    def send_alert(self, message: str) -> None:
        self._record("alert", message)

    def send_error(self, message: str) -> None:
        self._record("error", message)
