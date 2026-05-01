import streamlit as st
import threading
import time
import logging
import sys
import os
from sai.bot.main import TradingBot

# Ensure parent directory is on sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ✅ Correct import
from sai.bot.main import TradingBot

# Configure logging
logging.basicConfig(
    filename="trading.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize session state
if "bot" not in st.session_state:
    st.session_state.bot = TradingBot()
if "trades" not in st.session_state:
    st.session_state.trades = []
if "running" not in st.session_state:
    st.session_state.running = False

# Background trading loop
def trading_loop():
    while st.session_state.running:
        price = int(time.time()) % 100  # dummy price
        action = st.session_state.bot.decide(price)
        trade = {"price": price, "action": action}
        st.session_state.trades.append(trade)
        logging.info(f"Trade executed: {trade}")
        time.sleep(2)

# Streamlit UI
st.title("SAI Trading Bot Dashboard")

if st.button("Start Trading"):
    if not st.session_state.running:
        st.session_state.running = True
        threading.Thread(target=trading_loop, daemon=True).start()

if st.button("Stop Trading"):
    st.session_state.running = False

st.subheader("Live Trades")
st.write(st.session_state.trades)

st.subheader("Logs")
try:
    with open("trading.log", "r") as f:
        st.text(f.read())
except FileNotFoundError:
    st.info("No logs yet.")
