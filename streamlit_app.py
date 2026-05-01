# sai/streamlit_app.py
import streamlit as st
import time
import threading
import logging
from sai.bot.main import TradingBot   # ✅ fixed import

# Configure logging
logging.basicConfig(
    filename="trading.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize bot in session state
if "bot" not in st.session_state:
    st.session_state.bot = TradingBot(risk=0.5)

if "trades" not in st.session_state:
    st.session_state.trades = []

# Dashboard tab
def dashboard():
    st.title("SAI Trading Bot Dashboard")
    st.write("Live trading loop with dummy data")

    placeholder = st.empty()

    def run_loop():
        for price in range(100, 110):
            action = st.session_state.bot.decide(price)
            trade = {"price": price, "action": action}
            st.session_state.trades.append(trade)
            logging.info(f"Trade executed: {trade}")
            placeholder.write(trade)
            time.sleep(1)

    if st.button("Start Trading"):
        threading.Thread(target=run_loop, daemon=True).start()

    st.subheader("Trade History")
    st.write(st.session_state.trades)

# Logs tab
def logs():
    st.title("Logs")
    try:
        with open("trading.log") as f:
            st.text(f.read())
    except FileNotFoundError:
        st.write("No logs yet.")

# Sidebar navigation
tab = st.sidebar.radio("Navigation", ["Dashboard", "Logs"])

if tab == "Dashboard":
    dashboard()
elif tab == "Logs":
    logs()
