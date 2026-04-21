"""
Tests for notification plugins.

Covers:
- Base notifier interface compliance
- Sending messages via mock notifier
- Error handling for invalid channels
"""

import pytest
from plugins.notifications import (
    BaseNotifier,
    MockNotifier,
    EmailNotifier,
    SlackNotifier,
)

@pytest.fixture
def mock_notifier():
    return MockNotifier()

def test_base_notifier_has_required_methods():
    methods = ["send_message", "send_alert", "send_error"]
    for m in methods:
        assert hasattr(BaseNotifier, m)

def test_mock_notifier_send_message(mock_notifier):
    result = mock_notifier.send_message("Test message")
    assert result is True

def test_mock_notifier_send_alert(mock_notifier):
    result = mock_notifier.send_alert("Critical alert")
    assert result is True

def test_mock_notifier_send_error(mock_notifier):
    result = mock_notifier.send_error("Error occurred")
    assert result is True

@pytest.mark.parametrize("notifier_cls", [EmailNotifier, SlackNotifier])
def test_real_notifiers_have_interface(notifier_cls):
    notifier = notifier_cls(config={})
    assert hasattr(notifier, "send_message")
    assert hasattr(notifier, "send_alert")
    assert hasattr(notifier, "send_error")

def test_invalid_channel_raises_error(mock_notifier):
    with pytest.raises(ValueError):
        mock_notifier.send_message("", channel="INVALID")
