import smtplib
from email.mime.text import MIMEText
from .base_notifier import BaseNotifier

class EmailNotifier(BaseNotifier):
    def __init__(self, smtp_server, from_addr, to_addr):
        super().__init__("Email")
        self.smtp_server = smtp_server
        self.from_addr = from_addr
        self.to_addr = to_addr

    def send(self, message):
        msg = MIMEText(message)
        msg["Subject"] = "SAI Alert Notification"
        msg["From"] = self.from_addr
        msg["To"] = self.to_addr
        with smtplib.SMTP(self.smtp_server) as server:
            server.sendmail(self.from_addr, [self.to_addr], msg.as_string())

    def test_ping(self):
        self.send("Test ping from SAI cockpit ✅")
