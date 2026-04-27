# sai/streamlit_app.py
import streamlit as st
import threading
import time
import logging
import sys
import os
from sai.core.trading_bot import TradingBot
from sai.core.model_utils import load_model, test_model

# --- Logging Setup ---
LOG_FILE = "sai_logs.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- Session State Init ---
if "running" not in st.session_state:
    st.session_state.running = False
if "prices" not in st.session_state:
    st.session_state.prices = []
if "trades" not in st.session_state:
    st.session_state.trades = []

# --- Live Trading Loop ---
def run_bot_loop(bot: TradingBot):
    while st.session_state.running:
        price, trade = bot.step()
        st.session_state.prices.append(price)
        if trade:
            st.session_state.trades.append(trade)
            logging.info(f"Trade executed: {trade}")
        time.sleep(1)

# --- Tabs ---
tab_dashboard, tab_strategy, tab_logs, tab_model, tab_debug = st.tabs(
    ["📊 Dashboard", "⚙️ Strategy Config", "📝 Logs", "🤖 Model Testing", "🐞 Debug"]
)

# --- Dashboard ---
with tab_dashboard:
    st.header("Live Trading Dashboard")
    bot = TradingBot()
    if st.button("Start Bot"):
        if not st.session_state.running:
            st.session_state.running = True
            threading.Thread(target=run_bot_loop, args=(bot,), daemon=True).start()
    if st.button("Stop Bot"):
        st.session_state.running = False

    st.line_chart(st.session_state.prices)
    st.write("Executed Trades:", st.session_state.trades)

# --- Strategy Config ---
with tab_strategy:
    st.header("Strategy Configuration")
    risk = st.slider("Risk Level", 0.0, 1.0, 0.5)
    st.write(f"Current risk setting: {risk}")

# --- Logs ---
with tab_logs:
    st.header("Trading Logs")
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            st.text(f.read())
    else:
        st.write("No logs yet.")

# --- Model Testing ---
with tab_model:
    st.header("Model Testing")
    uploaded_model = st.file_uploader("Upload model.pkl", type=["pkl"])
    if uploaded_model:
        model = load_model(uploaded_model)
        st.success("Model loaded successfully.")
        test_results = test_model(model)
        st.write("Test Results:", test_results)

# --- Debug ---
with tab_debug:
    st.header("Debug Info")
    st.write("Python version:", sys.version)
    st.write("Working directory:", os.getcwd())
    st.write("Session state:", st.session_state)
