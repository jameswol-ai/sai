# sai/streamlit_app.py

import streamlit as st
import threading
import time
import logging
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# --- Logging setup ---
logging.basicConfig(
    filename="sai_app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# --- Session state init ---
if "trades" not in st.session_state:
    st.session_state.trades = []
if "running" not in st.session_state:
    st.session_state.running = False

# --- Dummy trading loop ---
def trading_loop():
    while st.session_state.running:
        start = time.time()
        price = np.random.randn() * 10 + 100
        trade = {"time": time.strftime("%H:%M:%S"), "price": price}
        st.session_state.trades.append(trade)

        # Update metrics
        trade_counter.inc()
        last_price_gauge.set(price)
        trade_latency_hist.observe(time.time() - start)

        logging.info(f"Trade executed: {trade}")
        time.sleep(2)

# --- Tabs ---
tabs = st.tabs(["📊 Dashboard", "⚙️ Strategy Config", "📝 Logs", "🧪 Model Testing", "🐞 Debug"])

# --- Dashboard ---
with tabs[0]:
    st.header("Live Trading Dashboard")
    if st.button("Start Trading", disabled=st.session_state.running):
        st.session_state.running = True
        threading.Thread(target=trading_loop, daemon=True).start()

    import pickle

# Load trained model once at startup
if "model" not in st.session_state:
    with open("models/model.pkl", "rb") as f:
        st.session_state.model = pickle.load(f)
    if st.button("Stop Trading", disabled=not st.session_state.running):
        st.session_state.running = False

    if st.session_state.trades:
        df = pd.DataFrame(st.session_state.trades)
        st.line_chart(df.set_index("time")["price"])
        st.metric("Total Trades", len(df))
        st.metric("Last Price", df["price"].iloc[-1])

# --- Strategy Config ---
with tabs[1]:
    st.header("Strategy Configuration")
    risk = st.slider("Risk Level", 1, 10, 5)
    capital = st.number_input("Capital Allocation", value=1000)
    st.write(f"Configured risk: {risk}, capital: {capital}")

# --- Logs ---
with tabs[2]:
    st.header("Application Logs")
    try:
        with open("sai_app.log") as f:
            logs = f.read()
        st.text_area("Logs", logs, height=300)
    except FileNotFoundError:
        st.info("No logs yet.")

# --- Model Testing ---
with tabs[3]:
    st.header("Model Testing")
    st.write("Upload a model.pkl to test predictions.")
    uploaded = st.file_uploader("Upload model file", type=["pkl"])
    if uploaded:
        st.success("Model uploaded (placeholder).")

# --- Debug ---
with tabs[4]:
    st.header("Debug Tools")
    st.write("Session State:", st.session_state)

def trading_loop():
    while st.session_state.running:
        # Example: get latest market features
        features = get_latest_features()  # returns DataFrame row

        # Predict action
        prediction = st.session_state.model.predict(features)[0]

        if prediction == 1:  # Buy signal
            execute_trade("BUY", features)
            logging.info("Executed BUY trade")
        elif prediction == -1:  # Sell signal
            execute_trade("SELL", features)
            logging.info("Executed SELL trade")
        else:
            logging.info("Hold position")

        # Update charts/metrics
        update_dashboard()
        time.sleep(5)  # loop interval

