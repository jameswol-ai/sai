import streamlit as st
import threading
import time
import random
import logging
import pandas as pd
from prometheus_client import Gauge, CollectorRegistry, start_http_server

# --- Logging Setup ---
logging.basicConfig(
    filename="trading.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# --- Prometheus Metrics ---
registry = CollectorRegistry()
equity_gauge = Gauge("sai_equity", "Current equity", registry=registry)
drawdown_gauge = Gauge("sai_drawdown", "Current drawdown", registry=registry)
sharpe_gauge = Gauge("sai_sharpe", "Sharpe ratio", registry=registry)
tracker_gauge = Gauge("sai_tracker_completion", "Project tracker completion", registry=registry)

def start_metrics_server(port=8000):
    if st.session_state.get("metrics_server_started", False):
        return
    try:
        start_http_server(port, registry=registry)
        st.session_state.metrics_server_started = True
        st.session_state.metrics_port = port
        st.write(f"✅ Prometheus metrics server running on port {port}")
    except OSError as e:
        st.warning(f"⚠️ Port {port} unavailable ({e}). Trying fallback port {port+1}...")
        try:
            start_http_server(port + 1, registry=registry)
            st.session_state.metrics_server_started = True
            st.session_state.metrics_port = port + 1
            st.write(f"✅ Prometheus metrics server running on port {port+1}")
        except OSError as e2:
            st.error(f"❌ Failed to start metrics server: {e2}")

# --- Risk Plugins (stubs) ---
class StopLossPlugin: 
    def __init__(self, threshold=0.05): self.threshold = threshold
    def check(self, trade, balance): return True

class MaxDrawdownPlugin: 
    def __init__(self, max_drawdown=0.2): self.max_drawdown = max_drawdown
    def check(self, trade, balance): return True

class PositionSizePlugin: 
    def __init__(self, max_fraction=0.1): self.max_fraction = max_fraction
    def check(self, trade, balance): return True

# --- Email Notifier (stub) ---
class EmailNotifier:
    def notify_pipeline(self, status, commit, branch):
        logging.info(f"EmailNotifier: {status} {commit} {branch}")

# --- Session State Defaults ---
def init_defaults():
    defaults = {
        "balance": 1000.0,
        "pnl": 0.0,
        "last_price": None,
        "last_action": None,
        "running": False,
        "prices": [],
        "trades": [],
        "alerts": [],
        "tracker_completion": 0,
        "risk_manager": [],
        "notifier": None,
        "metrics_server_started": False,
        "metrics_port": None
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def init_risk_manager():
    st.session_state.risk_manager = [
        StopLossPlugin(threshold
