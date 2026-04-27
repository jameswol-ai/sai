import streamlit as st
import pandas as pd
import time
import threading
import logging
from prometheus_client import Gauge, Counter, start_http_server

# --- Logging Setup ---
LOG_FILE = "logs/trading.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("sai_trading_bot")

# Example log generator (replace with real trading loop logs)
def generate_logs():
    while True:
        logger.info("Executed trade at simulated price 100.25")
        logger.warning("Latency spike detected: 2.3s")
        time.sleep(20)

threading.Thread(target=generate_logs, daemon=True).start()

# --- Prometheus Metrics ---
pnl_total = Gauge("sai_pnl_total", "Total Profit and Loss")
trades_per_minute = Gauge("sai_trades_per_minute", "Trades executed per minute")
trade_latency = Gauge("sai_trade_latency_seconds", "Latency per trade in seconds")
open_positions = Gauge("sai_open_positions", "Number of open positions")
model_version = Gauge("sai_model_version", "Current ML model version")
trade_counter = Counter("sai_trade_count", "Total trades executed")

pnl_history, trade_freq_history, timestamps = [], [], []

def start_metrics_server():
    start_http_server(8000)
    while True:
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

        timestamps.append(time.strftime("%H:%M:%S"))
        pnl_history.append(pnl_value)
        trade_freq_history.append(trades_value)

        time.sleep(15)

threading.Thread(target=start_metrics_server, daemon=True).start()

# --- Tabs Layout ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "⚠️ Risk Monitor", "📝 Logs", "⚙️ Config"])

with tab1:
    st.title("Trading Dashboard")
    col1, col2, col3 = st.columns(3)
    col1.metric("PnL ($)", f"{pnl_total._value.get():.2f}")
    col2.metric("Trades/min", f"{trades_per_minute._value.get():.0f}")
    col3.metric("Latency (s)", f"{trade_latency._value.get():.2f}")
    st.metric("Open Positions", f"{open_positions._value.get():.0f}")
    st.metric("Model Version", f"{model_version._value.get():.0f}")
    st.metric("Total Trades", f"{trade_counter._value.get():.0f}")

    if len(timestamps) > 1:
        df = pd.DataFrame({
            "Timestamp": timestamps,
            "PnL": pnl_history,
            "Trades/min": trade_freq_history
        })
        st.line_chart(df.set_index("Timestamp")[["PnL"]])
        st.line_chart(df.set_index("Timestamp")[["Trades/min"]])

with tab2:
    st.title("Risk Monitor")
    risk_status = "Healthy"
    risk_color = "✅ GREEN"
    if pnl_total._value.get() < -1000 or trade_latency._value.get() > 2.0 or open_positions._value.get() > 10:
        risk_status = "Critical"
        risk_color = "🚨 RED"
    elif pnl_total._value.get() < 0 or trade_latency._value.get() > 1.0 or open_positions._value.get() > 5:
        risk_status = "Warning"
        risk_color = "⚠️ YELLOW"
    st.subheader("Overall Risk Status")
    st.write(f"{risk_color} — {risk_status}")

    if pnl_total._value.get() < -1000:
        st.error("🚨 CRITICAL: Losses exceed $1000! Immediate action required.")
    elif pnl_total._value.get() < 0:
        st.warning("⚠️ Bot is currently running at a loss.")
    if trade_latency._value.get() > 2.0:
        st.warning("⚠️ High latency detected (>2s per trade).")
    if open_positions._value.get() > 10:
        st.warning("⚠️ Too many open positions. Risk exposure is high.")

with tab3:
    st.title("Logs")
    try:
        with open(LOG_FILE, "r") as f:
            logs = f.readlines()[-20:]  # Show last 20 log entries
        st.text_area("Recent Logs", "".join(logs), height=300)
    except FileNotFoundError:
        st.info("No logs available yet.")

with tab4:
    st.title("Config")
    st.write("⚙️ Strategy and risk configuration options go here.")
