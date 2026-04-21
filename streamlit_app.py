import streamlit as st
import pandas as pd
import datetime
import logging
from bot.main import run_bot, get_data, decide_action, SimpleModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sidebar controls
st.sidebar.title("SAI Trading Bot Controls")
run_button = st.sidebar.button("Run Bot")
refresh_button = st.sidebar.button("Refresh Data")

# Main dashboard
st.title("📈 SAI Trading Bot Dashboard")
st.write("Monitor and control your AI trading bot in real-time.")

# Load data
if refresh_button:
    try:
        data = get_data()
        st.session_state["data"] = data
        st.success("Data refreshed successfully.")
    except Exception as e:
        st.error(f"Error refreshing data: {e}")

# Display data
if "data" in st.session_state:
    st.subheader("Market Data Snapshot")
    st.dataframe(st.session_state["data"].tail(10))

# Run bot
if run_button:
    try:
        model = SimpleModel()
        data = st.session_state.get("data", get_data())
        predictions = model.predict(data)
        actions = [decide_action(pred) for pred in predictions]

        results_df = pd.DataFrame({
            "Timestamp": [datetime.datetime.now()] * len(actions),
            "Prediction": predictions,
            "Action": actions
        })

        st.subheader("Trading Decisions")
        st.dataframe(results_df)

        st.line_chart(results_df["Prediction"])
        st.bar_chart(results_df["Action"].value_counts())

        st.success("Bot executed successfully.")
    except Exception as e:
        st.error(f"Error running bot: {e}")
