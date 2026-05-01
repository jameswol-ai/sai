# sai/streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import threading
import logging
import time

# Import your bot core (adjust path if needed)
from sai.bot.main import TradingBot

# --- Logging setup ---
logging.basicConfig(
    filename="sai_app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# --- Session state init ---
if "bot" not in st.session_state:
    st.session_state.bot = TradingBot()
if "trades" not in st.session_state:
    st.session_state.trades = []
if "prices" not in st.session_state:
    st.session_state.prices = []
if "trading" not in st.session_state:
    st.session_state.trading = False

# --- Tabs ---
tabs = st.tabs(["Dashboard", "Strategy Config", "Logs", "Model Testing", "Debug"])

# --- Dashboard ---
with tabs[0]:
    st.header("📈 Live Trading Dashboard")

    def run_trading_loop():
        while st.session_state.trading:
            trade, price = st.session_state.bot.execute_trade()
            st.session_state.trades.append(trade)
            st.session_state.prices.append(price)
            logging.info(f"Trade: {trade}, Price: {price}")
            time.sleep(2)

    if st.button("Start Trading"):
        st.session_state.trading = True
        threading.Thread(target=run_trading_loop, daemon=True).start()

    if st.button("Stop Trading"):
        st.session_state.trading = False

    if st.session_state.prices:
        st.line_chart(st.session_state.prices)

# --- Strategy Config ---
with tabs[1]:
    st.header("⚙️ Strategy Configuration")
    risk = st.slider("Risk Level", 0.0, 1.0, 0.5)
    st.session_state.bot.set_param("risk", risk)
    st.write(f"Risk set to {risk}")

# --- Logs ---
with tabs[2]:
    st.header("📝 Logs")
    try:
        with open("sai_app.log") as f:
            st.text(f.read())
    except FileNotFoundError:
        st.warning("No logs yet.")

# --- Model Testing ---
with tabs[3]:
    st.header("🧪 Model Testing")

    if st.button("Show Feature Correlation Heatmap"):
        if hasattr(st.session_state.bot, "X_train"):
            df = pd.DataFrame(st.session_state.bot.X_train)
            corr = df.corr()
            fig, ax = plt.subplots(figsize=(8,6))
            sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)
        else:
            st.warning("No training data loaded.")

    if st.button("Residual Plot"):
        if hasattr(st.session_state.bot, "y_pred") and hasattr(st.session_state.bot, "y_true"):
            residuals = st.session_state.bot.y_true - st.session_state.bot.y_pred
            fig, ax = plt.subplots()
            sns.histplot(residuals, kde=True, ax=ax)
            ax.set_title("Residual Distribution")
            st.pyplot(fig)
        else:
            st.warning("No predictions available.")

# --- Debug ---
with tabs[4]:
    st.header("🐞 Debug Info")
    st.json({
        "trades_count": len(st.session_state.trades),
        "prices_count": len(st.session_state.prices),
        "bot_state": str(st.session_state.bot)
    })
