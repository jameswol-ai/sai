# sai/streamlit_app.py
import streamlit as st
import threading
import time

from sai.bot.main import run_bot, get_data, decide_action, SimpleModel
from sai.utils import setup_logger

# Initialize logger
logger = setup_logger("streamlit_app")

# Tabs
tabs = ["Dashboard", "Strategy Config", "Logs", "Model Testing", "Debug"]
selected_tab = st.sidebar.radio("Navigation", tabs)

# Shared state
if "trading_thread" not in st.session_state:
    st.session_state.trading_thread = None
if "logs" not in st.session_state:
    st.session_state.logs = []

def trading_loop():
    while True:
        try:
            data = get_data()
            action = decide_action(data)
            result = run_bot(action)
            st.session_state.logs.append(f"{time.ctime()}: {result}")
            time.sleep(2)
        except Exception as e:
            logger.error(f"Trading loop error: {e}")
            break

# Dashboard tab
if selected_tab == "Dashboard":
    st.title("SAI Trading Bot Dashboard")
    if st.button("Start Live Trading"):
        if st.session_state.trading_thread is None or not st.session_state.trading_thread.is_alive():
            st.session_state.trading_thread = threading.Thread(target=trading_loop, daemon=True)
            st.session_state.trading_thread.start()
            st.success("Live trading started.")
    st.line_chart([1, 2, 3, 4])  # placeholder chart

# Strategy Config tab
elif selected_tab == "Strategy Config":
    st.title("Configure Strategy")
    param = st.text_input("Parameter")
    st.write(f"Current parameter: {param}")

# Logs tab
elif selected_tab == "Logs":
    st.title("Logs")
    for log in st.session_state.logs[-50:]:
        st.text(log)

# Model Testing tab
elif selected_tab == "Model Testing":
    st.title("Test Model")
    model = SimpleModel()
    st.write("Model prediction:", model.predict([[1, 2, 3]]))

# Debug tab
elif selected_tab == "Debug":
    st.title("Debug Info")
    st.write(st.session_state)
