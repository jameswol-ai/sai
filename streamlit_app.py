# sai/streamlit_app.py
import streamlit as st
import threading
import time
import logging
from sai.bot.main import run_bot, get_data, decide_action, SimpleModel

# Configure logging
logging.basicConfig(filename="sai.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize session state
if "trades" not in st.session_state:
    st.session_state.trades = []
if "running" not in st.session_state:
    st.session_state.running = False

def trading_loop():
    while st.session_state.running:
        result = run_bot()
        st.session_state.trades.append(result)
        time.sleep(2)

# Streamlit UI
st.title("SAI Trading Bot Dashboard")

tab_dashboard, tab_strategy, tab_logs, tab_testing, tab_debug = st.tabs(
    ["Dashboard", "Strategy Config", "Logs", "Model Testing", "Debug"]
)

with tab_dashboard:
    st.header("Live Trading")
    if st.button("Start Trading") and not st.session_state.running:
        st.session_state.running = True
        threading.Thread(target=trading_loop, daemon=True).start()
    if st.button("Stop Trading"):
        st.session_state.running = False

    st.subheader("Trade History")
    st.write(st.session_state.trades)

with tab_strategy:
    st.header("Strategy Configuration")
    risk_level = st.slider("Risk Level", 1, 10, 5)
    st.write(f"Current risk level: {risk_level}")

with tab_logs:
    st.header("Logs")
    try:
        with open("sai.log", "r") as f:
            st.text(f.read())
    except FileNotFoundError:
        st.write("No logs yet.")

with tab_testing:
    st.header("Model Testing")
    data = get_data()
    model = SimpleModel()
    action = decide_action(model, data)
    st.write("Test Data:", data)
    st.write("Model Action:", action)

with tab_debug:
    st.header("Debug Info")
    st.json(st.session_state)
