# sai/streamlit_app.py

import streamlit as st
import logging
import threading
import time
import matplotlib.pyplot as plt

# Correct imports from sai.bot.main
from sai.bot.main import run_bot, get_data, decide_action, SimpleModel

# Configure logging
logging.basicConfig(
    filename="sai_streamlit.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize session state
if "trading" not in st.session_state:
    st.session_state.trading = False
if "model" not in st.session_state:
    st.session_state.model = SimpleModel()

# Dashboard tab
def dashboard_tab():
    st.header("📊 Live Trading Dashboard")

    if st.button("Start Trading"):
        st.session_state.trading = True
        threading.Thread(target=live_trading_loop, daemon=True).start()

    if st.button("Stop Trading"):
        st.session_state.trading = False

    st.line_chart(st.session_state.get("prices", []))

# Strategy Config tab
def strategy_tab():
    st.header("⚙️ Strategy Configuration")
    param = st.slider("Decision Threshold", 0.0, 1.0, 0.5)
    st.session_state.model.threshold = param
    st.write(f"Model threshold set to {param}")

# Logs tab
def logs_tab():
    st.header("📝 Logs")
    try:
        with open("sai_streamlit.log", "r") as f:
            st.text(f.read())
    except FileNotFoundError:
        st.write("No logs yet.")

# Model Testing tab
def model_tab():
    st.header("🧪 Model Testing")
    data = get_data()
    prediction = st.session_state.model.predict(data)
    st.write(f"Prediction: {prediction}")

# Debug tab
def debug_tab():
    st.header("🐞 Debug Info")
    st.json({
        "trading": st.session_state.trading,
        "model_params": vars(st.session_state.model)
    })

# Live trading loop
def live_trading_loop():
    while st.session_state.trading:
        data = get_data()
        action = decide_action(data, st.session_state.model)
        run_bot(action)
        logging.info(f"Action taken: {action}")
        prices = st.session_state.get("prices", [])
        prices.append(data["price"])
        st.session_state["prices"] = prices[-50:]  # keep last 50
        time.sleep(2)

# Main app
def main():
    st.title("SAI Trading Bot")
    tab = st.sidebar.radio("Navigation", ["Dashboard", "Strategy Config", "Logs", "Model Testing", "Debug"])

    if tab == "Dashboard":
        dashboard_tab()
    elif tab == "Strategy Config":
        strategy_tab()
    elif tab == "Logs":
        logs_tab()
    elif tab == "Model Testing":
        model_tab()
    elif tab == "Debug":
        debug_tab()

if __name__ == "__main__":
    main()
