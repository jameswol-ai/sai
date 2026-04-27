# sai/streamlit_app.py

import streamlit as st
import pandas as pd
import logging

# Import from your bot package
try:
    from sai.bot.main import run_bot, get_data, decide_action, SimpleModel, WorkflowEngine
except ImportError as e:
    st.error(f"Import failed: {e}")
    st.stop()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sidebar controls
st.sidebar.title("SAI Trading Bot Controls")
run_button = st.sidebar.button("Run Bot")
refresh_button = st.sidebar.button("Refresh Data")

# Main dashboard
st.title("📊 SAI Trading Bot Dashboard")

# Market Data Snapshot
st.header("Market Data Snapshot")
try:
    data = get_data()
    if isinstance(data, pd.DataFrame):
        st.dataframe(data.head())
    else:
        st.write(data)
except Exception as e:
    st.error(f"Error loading market data: {e}")

# Predictions & Actions
st.header("Trading Decisions")
try:
    model = SimpleModel()
    predictions = model.predict(data)
    actions = [decide_action(p) for p in predictions]

    df_results = pd.DataFrame({
        "Prediction": predictions,
        "Action": actions
    })
    st.dataframe(df_results)

    st.line_chart(df_results["Prediction"])
    st.bar_chart(df_results["Action"].value_counts())
except Exception as e:
    st.error(f"Error generating predictions: {e}")

# Workflow Engine Integration
st.header("Workflow Engine Status")
try:
    engine = WorkflowEngine()
    status = engine.status()
    st.write(status)
except Exception as e:
    st.error(f"WorkflowEngine error: {e}")

# Run Bot
if run_button:
    try:
        run_bot()
        st.success("Bot executed successfully.")
    except Exception as e:
        st.error(f"Error running bot: {e}")

# Refresh Data
if refresh_button:
    st.experimental_rerun()
