# sai/streamlit_app.py

import streamlit as st
import sys
import os
import traceback

# --------------------------------------------------
# 🧭 PATH FIX
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSSIBLE_PATHS = [
    BASE_DIR,
    os.path.join(BASE_DIR, "src"),
    os.path.join(BASE_DIR, "src", "core"),
]
for path in POSSIBLE_PATHS:
    if path not in sys.path:
        sys.path.insert(0, path)

# --------------------------------------------------
# 🎛 PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="AI Trading Bot", layout="wide")

st.title("AI Trading Bot")
st.caption("Resilient Workflow Engine • Debug Mode Enabled")

# --------------------------------------------------
# 📑 MULTI-TAB LAYOUT
# --------------------------------------------------
tabs = st.tabs(["📊 Dashboard", "⚙️ Strategy Config", "📝 Logs", "🧪 Model Testing", "⚙️ Debug"])

# --- Dashboard ---
import time
import pandas as pd

# --- Dashboard ---
with tabs[0]:
    st.header("📊 Trading Dashboard")
    st.write("Live bot performance, trades, and PnL.")

    # Containers for dynamic updates
    price_chart = st.empty()
    trade_log = st.empty()
    pnl_display = st.empty()

    # Example live loop (replace with real bot data)
    if st.button("▶️ Start Live Bot"):
        for i in range(20):  # simulate 20 ticks
            # Simulated market data
            prices = [100 + j*0.5 for j in range(i+1)]
            df = pd.DataFrame({"Price": prices})

            # Update chart
            price_chart.line_chart(df)

            # Update trade log
            trade_log.text(f"Tick {i} | TRADE | BUY BTCUSD @ {prices[-1]}")

            # Update PnL
            pnl_display.metric("PnL", f"${round((prices[-1]-100)*10,2)}")

            time.sleep(1)  # refresh every second
with tabs[0]:
    st.header("📊 Trading Dashboard")
    st.write("Overview of bot performance, PnL, and market data.")
    # Example chart placeholder
    st.line_chart({"Price": [100, 102, 105, 103, 108]})

# --- Strategy Config ---
with tabs[1]:
    st.header("⚙️ Strategy Configuration")
    st.write("Adjust parameters for trading strategies.")
    risk = st.slider("Risk Level", 0.0, 1.0, 0.5)
    leverage = st.number_input("Leverage", min_value=1, max_value=10, value=2)
    st.button("Apply Strategy Settings")

# --- Logs ---
with tabs[2]:
    st.header("📝 Bot Logs")
    st.write("Real-time log streaming or file tail.")
    # Example log lines
    st.text("2026-04-27 14:15:01 | INFO | Bot started\n2026-04-27 14:15:05 | TRADE | BUY BTCUSD")

# --- Model Testing ---
with tabs[3]:
    st.header("🧪 Model Testing")
    st.write("Run ML models against test datasets.")
    uploaded_file = st.file_uploader("Upload test dataset (CSV)", type="csv")
    if uploaded_file:
        st.success("Dataset uploaded successfully!")
        # Placeholder for model evaluation
        st.write("Model accuracy: 92%")

# --- Debug ---
with tabs[4]:
    st.header("⚙️ System Debug Info")
    st.write("📁 Base Dir:", BASE_DIR)
    for path in POSSIBLE_PATHS:
        exists = os.path.exists(path)
        st.write(f"Path: {path} | Exists: {exists}")
    st.write("🔗 sys.path entries:", sys.path[:5])
    st.write("🐍 Python Version:", sys.version)
    st.write("📂 Working Dir:", os.getcwd())
    try:
        # Example import test
        from sai.bot.main import run_bot
        st.success("Bot module imported successfully")
    except Exception:
        st.error("❌ Import failed")
        st.code(traceback.format_exc())



import streamlit as st
import threading
import time
import pandas as pd

# Shared state
if "running" not in st.session_state:
    st.session_state.running = False
if "prices" not in st.session_state:
    st.session_state.prices = []

def trading_loop():
    """Background loop simulating live trading."""
    while st.session_state.running:
        # Replace with real market feed
        next_price = 100 + len(st.session_state.prices) * 0.5
        st.session_state.prices.append(next_price)

        # Simulate trade event
        print(f"TRADE | BUY BTCUSD @ {next_price}")

        time.sleep(1)  # tick interval

# --- Dashboard Tab ---
st.header("📊 Trading Dashboard")

start_btn = st.button("▶️ Start Live Bot")
stop_btn = st.button("⏹ Stop Bot")

if start_btn and not st.session_state.running:
    st.session_state.running = True
    threading.Thread(target=trading_loop, daemon=True).start()

if stop_btn:
    st.session_state.running = False

# Render live data
if st.session_state.prices:
    df = pd.DataFrame({"Price": st.session_state.prices})
    st.line_chart(df)
    st.metric("PnL", f"${round((st.session_state.prices[-1]-100)*10,2)}")
