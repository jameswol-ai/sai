# sai/streamlit_app.py
import streamlit as st
import threading
import logging
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sai.bot.main import TradingBot

# --- Logging setup ---
logging.basicConfig(
    filename="sai_app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# --- Session state init ---
def init_state():
    if "bot" not in st.session_state:
        st.session_state.bot = TradingBot()
    if "trades" not in st.session_state:
        st.session_state.trades = []
    if "prices" not in st.session_state:
        st.session_state.prices = []
    if "trading" not in st.session_state:
        st.session_state.trading = False

init_state()

# --- Trading loop ---
def run_trading_loop():
    while st.session_state.trading:
        try:
            trade, price = st.session_state.bot.execute_trade()
            if trade is not None:
                st.session_state.trades.append(trade)
            if price is not None:
                st.session_state.prices.append(price)
            logging.info(f"Trade: {trade}, Price: {price}")
        except Exception as e:
            logging.error(f"Error in trading loop: {e}")
        time.sleep(2)

# --- Tabs ---
tab_dashboard, tab_strategy, tab_logs, tab_model, tab_debug = st.tabs(
    ["📈 Dashboard", "⚙️ Strategy Config", "📝 Logs", "🧪 Model Testing", "🐞 Debug"]
)

# --- Dashboard ---
with tab_dashboard:
    st.header("Live Trading Dashboard")
    col1, col2 = st.columns(2)
    if col1.button("Start Trading"):
        if not st.session_state.trading:
            st.session_state.trading = True
            threading.Thread(target=run_trading_loop, daemon=True).start()
    if col2.button("Stop Trading"):
        st.session_state.trading = False

    if st.session_state.prices:
        st.line_chart(st.session_state.prices)

    st.subheader("Metrics")
    st.metric("Trades Executed", len(st.session_state.trades))
    if st.session_state.prices:
        st.metric("Latest Price", st.session_state.prices[-1])

# --- Strategy Config ---
with tab_strategy:
    st.header("Strategy Configuration")
    risk = st.slider("Risk Level", 0.0, 1.0, 0.5)
    st.session_state.bot.set_param("risk", risk)
    st.success(f"Risk set to {risk}")

# --- Logs ---
with tab_logs:
    st.header("Trading Logs")
    try:
        with open("sai_app.log") as f:
            st.text(f.read())
    except FileNotFoundError:
        st.info("No logs yet.")

# --- Model Testing ---
with tab_model:
    st.header("Model Testing")

    if st.button("Feature Correlation Heatmap"):
        if hasattr(st.session_state.bot, "X_train"):
            df = pd.DataFrame(st.session_state.bot.X_train)
            corr = df.corr()
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.heatmap(corr, cmap="coolwarm", ax=ax)
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
with tab_debug:
    st.header("Debug Info")
    st.json({
        "trades_count": len(st.session_state.trades),
        "prices_count": len(st.session_state.prices),
        "bot_state": str(st.session_state.bot)
    })
