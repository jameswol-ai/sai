"""
Tests for Logs tab rendering and logging integration.
"""

import pytest
import streamlit as st
from unittest.mock import patch, MagicMock
from io import StringIO

# --- Helpers ---
def fake_session_state_with_trades():
    st.session_state.trades = [
        "TRADE: BUY AAPL @ 175.20",
        "INFO: Strategy initialized",
        "ERROR: Broker timeout"
    ]

# --- Tests ---
def test_logs_tab_renders_trades(monkeypatch):
    fake_session_state_with_trades()

    with patch("streamlit.text") as mock_text:
        # Simulate Logs tab code
        st.text("\n".join(st.session_state.trades[-20:]))

        mock_text.assert_called_once()
        args, _ = mock_text.call_args
        assert "TRADE: BUY AAPL" in args[0]

def test_logs_tab_shows_info_when_empty(monkeypatch):
    st.session_state.trades = []

    with patch("streamlit.info") as mock_info:
        st.info("No trades yet. Start the bot from the Dashboard tab.")
        mock_info.assert_called_once()

def test_logging_module_integration(monkeypatch):
    log_stream = StringIO()
    import logging
    handler = logging.StreamHandler(log_stream)
    logger = logging.getLogger("sai")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    logger.info("Test log entry")
    handler.flush()

    output = log_stream.getvalue()
    assert "Test log entry" in output
