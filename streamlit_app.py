import streamlit as st
import threading
import time
import logging
import pandas as pd
from prometheus_client import Counter, Gauge, start_http_server

# --- Prometheus Metrics ---
trade_counter = Counter("sai_trades_total", "Total trades executed")
price_gauge = Gauge("sai_last_price", "Last trade price")
exposure_gauge = Gauge("sai_exposure", "Current exposure")
loss_gauge = Gauge("sai_loss", "Current loss")

# Start Prometheus metrics server on port 8000
start_http_server(8000)

# --- Logging ---
logging.basicConfig(
    filename="sai_trading.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- Session State ---
defaults = {
    "trades": [],
    "prices": [],
    "running": False,
    "risk_limits": {"max_loss": 50, "max_exposure": 1000}
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# --- Trading Loop ---
def trading_loop():
    while st.session_state.running:
        price = 100 + (time.time() % 10)
        trade = {"time": time.strftime("%H:%M:%S"), "price": price}
        st.session_state.prices.append(price)

        # Prometheus metrics update
        price_gauge.set(price)
        exposure_gauge.set(len(st.session_state.trades))

        if len(st.session_state.trades) < st.session_state["risk_limits"]["max_exposure"]:
            st.session_state.trades.append(trade)
            trade_counter.inc()
            logging.info(f"Trade executed: {trade}")
        else:
            loss_gauge.set(st.session_state["risk_limits"]["max_loss"])
            logging.warning("Exposure limit reached, trade skipped.")

        time.sleep(2)
