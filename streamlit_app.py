# sai/streamlit_app.py
import streamlit as st
import threading
import time
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sai.core.trading import TradingBot
from sai.core.models import load_model, save_model
from sai.core.utils import get_price_data, execute_trade

# --- Logging Setup ---
logging.basicConfig(
    filename="sai_app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# --- Session State Init ---
if "bot" not in st.session_state:
    st.session_state.bot = TradingBot()
if "running" not in st.session_state:
    st.session_state.running = False
if "trades" not in st.session_state:
    st.session_state.trades = []
if "prices" not in st.session_state:
    st.session_state.prices = pd.DataFrame()

# --- Live Trading Loop ---
def run_trading_loop():
    while st.session_state.running:
        price = get_price_data()
        action = st.session_state.bot.decide(price)
        trade = execute_trade(action, price)
        st.session_state.trades.append(trade)
        st.session_state.prices = pd.concat(
            [st.session_state.prices, pd.DataFrame([{"time": time.time(), "price": price}])]
        )
        logging.info(f"Trade executed: {trade}")
        time.sleep(2)

# --- Tabs ---
st.set_page_config(page_title="SAI Trading Bot", layout="wide")
tabs = st.tabs(["📊 Dashboard", "⚙️ Strategy Config", "📝 Logs", "🧪 Model Testing", "🐞 Debug"])

# --- Dashboard ---
with tabs[0]:
    st.header("Live Trading Dashboard")
    col1, col2 = st.columns([2,1])
    with col1:
        if st.session_state.running:
            st.success("Bot is running...")
        else:
            st.warning("Bot is stopped.")
        if st.button("Start Bot"):
            st.session_state.running = True
            threading.Thread(target=run_trading_loop, daemon=True).start()
        if st.button("Stop Bot"):
            st.session_state.running = False

        st.subheader("Price Chart")
        if not st.session_state.prices.empty:
            fig, ax = plt.subplots()
            ax.plot(st.session_state.prices["time"], st.session_state.prices["price"], label="Price")
            ax.legend()
            st.pyplot(fig)

    with col2:
        st.subheader("Metrics")
        st.metric("Total Trades", len(st.session_state.trades))
        if st.session_state.trades:
            pnl = sum([t["pnl"] for t in st.session_state.trades])
            st.metric("PnL", f"{pnl:.2f}")

# --- Strategy Config ---
with tabs[1]:
    st.header("Strategy Configuration")
    risk = st.slider("Risk Level", 0.0, 1.0, st.session_state.bot.risk)
    st.session_state.bot.risk = risk
    st.write("Current risk:", risk)

# --- Logs ---
with tabs[2]:
    st.header("Application Logs")
    with open("sai_app.log") as f:
        logs = f.read()
    st.text_area("Logs", logs, height=400)

# --- Model Testing ---
with tabs[3]:
    st.header("Model Testing")
    uploaded = st.file_uploader("Upload test dataset (CSV)", type="csv")
    if uploaded:
        df = pd.read_csv(uploaded)
        model = load_model("model.pkl")
        preds = model.predict(df.drop("target", axis=1))
        st.write("Predictions:", preds[:10])
        st.line_chart(preds)

    if st.button("Save Current Model"):
        save_model(st.session_state.bot.model, "model.pkl")
        st.success("Model saved.")

# --- Debug ---
with tabs[4]:
    st.header("Debug Tools")
    st.write("Session State:", st.session_state)
    st.write("Trades:", st.session_state.trades)
    st.write("Prices:", st.session_state.prices.tail())
