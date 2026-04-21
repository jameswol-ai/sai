# plugins/notifications/email_notifier.py
"""
Email Notifier
--------------
Implements BaseNotifier for sending notifications via email (SMTP).
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from plugins.notifications.base_notifier import BaseNotifier


class EmailNotifier(BaseNotifier):
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str, from_addr: str, to_addr: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.from_addr = from_addr
        self.to_addr = to_addr

    def _send(self, subject: str, body: str) -> None:
        """Internal helper to send an email."""
        msg = MIMEMultipart()
        msg["From"] = self.from_addr
        msg["To"] = self.to_addr
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)

    def send_message(self, message: str) -> None:
        self._send(subject="Notification", body=message)

    def send_alert(self, message: str) -> None:
        self._send(subject="ALERT", body=message)

    def send_error(self, message: str) -> None:
        self._send(subject="ERROR", body=message)
