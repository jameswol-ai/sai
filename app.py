import streamlit as st
import pandas as pd
import time
import threading
from prometheus_client import Gauge, Counter, start_http_server

# Define Prometheus metrics
pnl_total = Gauge("sai_pnl_total", "Total Profit and Loss")
trades_per_minute = Gauge("sai_trades_per_minute", "Trades executed per minute")
trade_latency = Gauge("sai_trade_latency_seconds", "Latency per trade in seconds")
open_positions = Gauge("sai_open_positions", "Number of open positions")
model_version = Gauge("sai_model_version", "Current ML model version")
trade_counter = Counter("sai_trade_count", "Total trades executed")

# Data storage for charts
pnl_history, trade_freq_history, timestamps = [], [], []

# Background metrics server
def start_metrics_server():
    start_http_server(8000)
    while True:
        # Replace with live trading loop values
        pnl_value = 1250.75
        trades_value = 5
        latency_value = 0.85
        positions_value = 3
        model_value = 20260427

        pnl_total.set(pnl_value)
        trades_per_minute.set(trades_value)
        trade_latency.set(latency_value)
        open_positions.set(positions_value)
        model_version.set(model_value)
        trade_counter.inc()

        # Append to history for charts
        timestamps.append(time.strftime("%H:%M:%S"))
        pnl_history.append(pnl_value)
        trade_freq_history.append(trades_value)

        time.sleep(15)

threading.Thread(target=start_metrics_server, daemon=True).start()

# Streamlit UI
st.title("SAI Trading Bot Dashboard")

# Alerts
if pnl_total._value.get() < -1000:
    st.error("⚠️ ALERT: Losses exceed $1000! Immediate review required.")
if trade_latency._value.get() > 2.0:
    st.warning("⚠️ High latency detected (>2s per trade).")
if open_positions._value.get() > 10:
    st.warning("⚠️ Too many open positions. Risk exposure is high.")

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("PnL ($)", f"{pnl_total._value.get():.2f}")
col2.metric("Trades/min", f"{trades_per_minute._value.get():.0f}")
col3.metric("Latency (s)", f"{trade_latency._value.get():.2f}")

st.metric("Open Positions", f"{open_positions._value.get():.0f}")
st.metric("Model Version", f"{model_version._value.get():.0f}")
st.metric("Total Trades", f"{trade_counter._value.get():.0f}")

# Charts
if len(timestamps) > 1:
    df = pd.DataFrame({
        "Timestamp": timestamps,
        "PnL": pnl_history,
        "Trades/min": trade_freq_history
    })

    st.line_chart(df.set_index("Timestamp")[["PnL"]])
    st.line_chart(df.set_index("Timestamp")[["Trades/min"]])
