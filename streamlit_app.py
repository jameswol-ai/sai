# sai/streamlit_app.py
import streamlit as st
import threading
import time
import logging
import pandas as pd
import matplotlib.pyplot as plt
from sai.bot.main import TradingBot   # assumes you have a TradingBot class in sai/bot/main.py

# --- Configure logging ---
logging.basicConfig(
    filename="sai_streamlit.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- Initialize session state ---
if "bot" not in st.session_state:
    st.session_state.bot = None
if "running" not in st.session_state:
    st.session_state.running = False
if "trades" not in st.session_state:
    st.session_state.trades = []
if "prices" not in st.session_state:
    st.session_state.prices = []

# --- Helper: Live trading loop ---
def run_bot():
    while st.session_state.running:
        try:
            price, trade = st.session_state.bot.step()
            st.session_state.prices.append(price)
            if trade:
                st.session_state.trades.append(trade)
                logging.info(f"Trade executed: {trade}")
        except Exception as e:
            logging.error(f"Error in trading loop: {e}")
        time.sleep(1)

# --- Dashboard Tab ---
def dashboard_tab():
    st.header("📊 Dashboard")
    if st.button("Start Bot"):
        if not st.session_state.running:
            st.session_state.bot = TradingBot()
            st.session_state.running = True
            threading.Thread(target=run_bot, daemon=True).start()
            st.success("Bot started.")
    if st.button("Stop Bot"):
        st.session_state.running = False
        st.warning("Bot stopped.")

    st.subheader("Price Chart")
    if st.session_state.prices:
        fig, ax = plt.subplots()
        ax.plot(st.session_state.prices, label="Price")
        ax.set_title("Live Prices")
        st.pyplot(fig)

    st.subheader("Trades")
    if st.session_state.trades:
        df = pd.DataFrame(st.session_state.trades)
        st.dataframe(df)

# --- Strategy Config Tab ---
def strategy_config_tab():
    st.header("⚙️ Strategy Config")
    param1 = st.number_input("Threshold", value=0.5)
    param2 = st.number_input("Window Size", value=10)
    if st.button("Update Strategy"):
        if st.session_state.bot:
            st.session_state.bot.update_strategy(param1, param2)
            st.success("Strategy updated.")

# --- Logs Tab ---
def logs_tab():
    st.header("📝 Logs")
    try:
        with open("sai_streamlit.log", "r") as f:
            logs = f.read()
        st.text_area("Log Output", logs, height=300)
    except FileNotFoundError:
        st.info("No logs yet.")

# --- Model Testing Tab ---
def model_testing_tab():
    st.header("🧪 Model Testing")
    uploaded = st.file_uploader("Upload test dataset (CSV)", type="csv")
    if uploaded:
        df = pd.read_csv(uploaded)
        st.write("Dataset preview:", df.head())
        if st.session_state.bot:
            results = st.session_state.bot.test_model(df)
            st.write("Test Results:", results)

# --- Debug Tab ---
def debug_tab():
    st.header("🐞 Debug Info")
    st.json({
        "running": st.session_state.running,
        "num_prices": len(st.session_state.prices),
        "num_trades": len(st.session_state.trades)
    })

# --- Main Layout ---
def main():
    st.title("SAI Trading Bot Dashboard")
    tabs = st.tabs(["Dashboard", "Strategy Config", "Logs", "Model Testing", "Debug"])
    with tabs[0]:
        dashboard_tab()
    with tabs[1]:
        strategy_config_tab()
    with tabs[2]:
        logs_tab()
    with tabs[3]:
        model_testing_tab()
    with tabs[4]:
        debug_tab()

if __name__ == "__main__":
    main()
