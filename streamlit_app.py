# sai/streamlit_app.py
import streamlit as st
import time
import threading
import logging

# ✅ Correct import path
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
        price = time.time() % 100  # dummy price
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
        st.success("Trading started!")

if st.button("Stop Trading"):
    st.session_state.running = False
    st.warning("Trading stopped.")

st.subheader("Live Trades")
for trade in st.session_state.trades[-10:]:
    st.write(trade)

st.subheader("Logs")
with open("trading.log", "r") as f:
    logs = f.readlines()
st.text("".join(logs[-10:]))
