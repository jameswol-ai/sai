# plugins/notifications/utils.py
"""
Notification Utilities
----------------------
Shared helper functions for notification plugins
(e.g., Email, SMS, Slack, Telegram, Webhook, Mock).
"""

import logging
import time
import functools


def setup_logger(name: str, log_file: str, level: str = "INFO") -> logging.Logger:
    """
    Configure and return a logger for notifications.
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    fh = logging.FileHandler(log_file)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(fh)

    return logger


def retry(exceptions, tries: int = 3, delay: int = 2, backoff: int = 2):
    """
    Retry decorator for transient errors (e.g., network issues).
    Args:
        exceptions (tuple): Exception types to catch.
        tries (int): Number of attempts.
        delay (int): Initial delay between retries.
        backoff (int): Multiplier for delay.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _tries, _delay = tries, delay
            while _tries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logging.warning(f"{func.__name__} failed with {e}, retrying in {_delay}s...")
                    time.sleep(_delay)
                    _tries -= 1
                    _delay *= backoff
            return func(*args, **kwargs)
        return wrapper
    return decorator


def format_message(prefix: str, message: str) -> str:
    """
    Format a message with a prefix (e.g., ALERT, ERROR).
    """
    return f"[{prefix.upper()}] {message}"
