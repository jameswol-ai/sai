# sai/streamlit_app.py

import streamlit as st
import matplotlib.pyplot as plt

from sai.bot.main import run_bot, get_data, decide_action, SimpleModel
from sai.utils import setup_logger

logger = setup_logger("sai_streamlit")

def main():
    st.title("SAI Trading Bot Dashboard")

    # Sidebar controls
    st.sidebar.header("Controls")
    if st.sidebar.button("Run Bot"):
        action = run_bot()
        st.success(f"Bot Action: {action}")
        logger.info(f"Bot executed action: {action}")

    if st.sidebar.button("Refresh Data"):
        data = get_data()
        st.write("Latest Data Snapshot:", data)
        logger.info("Data refreshed")

        # Plot numeric data
        if isinstance(data, (list, tuple)) and all(isinstance(x, (int, float)) for x in data):
            fig, ax = plt.subplots()
            ax.plot(data, marker="o", linestyle="-", color="blue")
            ax.set_title("Market Data Trend")
            ax.set_xlabel("Index")
            ax.set_ylabel("Value")
            st.pyplot(fig)

    if st.sidebar.button("Decide Action"):
        data = get_data()
        action = decide_action(data)
        st.info(f"Bot Decision: {action}")
        logger.info(f"Decision made: {action}")

    if st.sidebar.button("Test Model"):
        model = SimpleModel()
        sample_data = get_data()
        prediction = model.predict(sample_data)
        st.write("Model Prediction:", prediction)
        logger.info(f"Model prediction: {prediction}")

    # Extra visualization: distribution of actions
    st.subheader("Action Distribution Example")
    actions = ["BUY", "SELL", "HOLD"]
    counts = [5, 3, 7]  # Replace with real metrics if available
    fig, ax = plt.subplots()
    ax.bar(actions, counts, color=["green", "red", "gray"])
    ax.set_title("Action Distribution")
    st.pyplot(fig)

if __name__ == "__main__":
    main()
