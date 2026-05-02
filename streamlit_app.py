import streamlit as st
import threading
import time
import logging
from sai.core.engine import Sai   # imports your own class

logging.basicConfig(
    filename="sai_app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

if "bot" not in st.session_state:
    st.session_state.bot = Sai()
if "running" not in st.session_state:
    st.session_state.running = False
if "logs" not in st.session_state:
    st.session_state.logs = []

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

def dashboard_tab():
    st.header("📊 Dashboard")
    if st.button("Start Trading") and not st.session_state.running:
        st.session_state.running = True
        threading.Thread(target=run_trading_loop, daemon=True).start()
    if st.button("Stop Trading"):
        st.session_state.running = False

    st.metric("Balance", f"${st.session_state.bot.balance:.2f}")
    st.metric("Open Trades", len(st.session_state.bot.open_trades))

def strategy_config_tab():
    st.header("⚙️ Strategy Config")
    risk = st.slider("Risk Level", 1, 10, st.session_state.bot.risk)
    st.session_state.bot.risk = risk
    st.write("Strategy updated.")

def logs_tab():
    st.header("📝 Logs")
    for log in st.session_state.logs[-50:]:
        st.text(log)

def model_testing_tab():
    st.header("🧪 Model Testing")
    st.write("Placeholder for ML model evaluation.")

def debug_tab():
    st.header("🐞 Debug")
    st.write("Session State:", st.session_state)

def main():
    st.title("SAI Trading Bot")
    tab = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Strategy Config", "Logs", "Model Testing", "Debug"]
    )

    if tab == "Dashboard":
        dashboard_tab()
    elif tab == "Strategy Config":
        strategy_config_tab()
    elif tab == "Logs":
        logs_tab()
    elif tab == "Model Testing":
        model_testing_tab()
    elif tab == "Debug":
        debug_tab()

if __name__ == "__main__":
    main()
