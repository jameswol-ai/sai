import streamlit as st
from sai.bot.trader import TradingBot
from sai.monitoring import grafana_overlay, prometheus_exporter
import logging
import threading

# --- Logging setup ---
logging.basicConfig(
    filename="sai.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- Session state init ---
if "trading_thread" not in st.session_state:
    st.session_state.trading_thread = None
if "bot" not in st.session_state:
    st.session_state.bot = TradingBot()

# --- Tabs ---
tab_dashboard, tab_config, tab_logs, tab_testing, tab_debug = st.tabs(
    ["Dashboard", "Strategy Config", "Logs", "Model Testing", "Debug"]
)

with tab_dashboard:
    st.header("📊 Live Dashboard")
    if st.button("Start Trading"):
        if st.session_state.trading_thread is None or not st.session_state.trading_thread.is_alive():
            def run_bot():
                st.session_state.bot.run()
            st.session_state.trading_thread = threading.Thread(target=run_bot, daemon=True)
            st.session_state.trading_thread.start()
            logging.info("Trading loop started.")
    grafana_overlay()
    prometheus_exporter()

with tab_config:
    st.header("⚙️ Strategy Config")
    st.session_state.bot.config_ui()

with tab_logs:
    st.header("📜 Logs")
    with open("sai.log") as f:
        st.text(f.read())

with tab_testing:
    st.header("🧪 Model Testing")
    st.session_state.bot.test_models()

with tab_debug:
    st.header("🐞 Debug")
    st.write("Debugging tools here...")
