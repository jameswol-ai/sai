# sai/streamlit_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Import from your package
from sai.bot.main import run_bot, get_data, decide_action, SimpleModel
from sai.utils import setup_logger

# Configure logging
logger = setup_logger("streamlit_app")

st.set_page_config(page_title="SAI Trading Bot Dashboard", layout="wide")

def main():
    st.title("📈 SAI Trading Bot Dashboard")

    # Sidebar controls
    st.sidebar.header("Controls")
    if st.sidebar.button("Run Bot"):
        logger.info("Running bot from Streamlit UI")
        run_bot()

    if st.sidebar.button("Refresh Data"):
        logger.info("Refreshing market data")
        data = get_data()
        st.session_state["data"] = data

    # Display market data
    if "data" in st.session_state:
        st.subheader("Market Data Snapshot")
        df = pd.DataFrame(st.session_state["data"])
        st.dataframe(df)

        # Predictions
        model = SimpleModel()
        predictions = model.predict(df)
        st.subheader("Predictions")
        st.line_chart(predictions)

        # Actions
        actions = [decide_action(p) for p in predictions]
        st.subheader("Trading Decisions")
        st.bar_chart(pd.Series(actions).value_counts())

if __name__ == "__main__":
    main()
