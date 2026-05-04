# sai/streamlit_app.py

import os
print("Working directory:", os.getcwd())
print("FILESYSTEM:", os.listdir("/mount/src/sai"))
print("CORE:", os.listdir("/mount/src/sai/core"))
import streamlit as st
import threading
import time
import logging
import pandas as pd
from sai.bot.maim import Sai

# Configure logging
logging.basicConfig(
    filename="sai_app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Initialize session state
if "bot" not in st.session_state:
    st.session_state.bot = Sai()
if "running" not in st.session_state:
    st.session_state.running = False
if "logs" not in st.session_state:
    st.session_state.logs = []

# Background trading loop
def run_trading_loop():
    while st.session_state.running:
        try:
            trade_info = st.session_state.bot.run_once()
            if trade_info:
                st.session_state.logs.append(trade_info)
                logging.info(trade_info)
        except Exception as e:
            logging.error(f"Trading loop error: {e}")
        time.sleep(1)

# Dashboard tab
def dashboard_tab():
    st.header("📊 Dashboard")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Start Trading") and not st.session_state.running:
            st.session_state.running = True
            threading.Thread(target=run_trading_loop, daemon=True).start()
    with col2:
        if st.button("⏹ Stop Trading"):
            st.session_state.running = False

    st.subheader("Live Trades")
    if st.session_state.logs:
        df = pd.DataFrame(st.session_state.logs)
        st.dataframe(df)

        # Quick metrics
        st.metric("Total Trades", len(df))
        st.metric("Last Action", df["action"].iloc[-1])
        st.metric("Latest Price", round(df["latest_price"].iloc[-1], 2))

        # CSV export
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Trades CSV",
            data=csv,
            file_name="trades.csv",
            mime="text/csv"
        )
    else:
        st.info("No trades yet. Start trading to see activity.")

# Logs tab
def logs_tab():
    st.header("📝 Logs")
    try:
        with open("sai_app.log", "r") as f:
            st.text(f.read())
    except FileNotFoundError:
        st.warning("No log file found yet.")

# Main app
def main():
    st.title("SAI Trading Bot Dashboard")

    tab = st.sidebar.radio("Navigation", ["Dashboard", "Logs"])
    if tab == "Dashboard":
        dashboard_tab()
    elif tab == "Logs":
        logs_tab()

if __name__ == "__main__":
    main()
