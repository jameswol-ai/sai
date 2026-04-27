# sai/streamlit_app.py

import logging

# Configure logging
LOG_FILE = "bot.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),   # persistent file
        logging.StreamHandler()          # console (shows in Streamlit logs)
    ]
)
logger = logging.getLogger(__name__)

def trading_loop():
    """Background loop using real bot feed."""
    run_bot()  # start bot core
    while st.session_state.running:
        snapshot = get_data()
        st.session_state.prices.append(snapshot["price"])
        st.session_state.trades.append(snapshot["trade"])

        # Log trade event
        logger.info(snapshot["trade"])

        time.sleep(1)

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

    # Controls
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

    # Show recent trades from session state
    if st.session_state.trades:
        st.subheader("Recent Trades")
        st.text("\n".join(st.session_state.trades[-20:]))

    # Show raw log file tail
    st.subheader("System Log File Tail")
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()[-20:]  # last 20 lines
        st.text("".join(lines))
    except FileNotFoundError:
        st.info("No log file yet. Start the bot to generate logs.")

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



