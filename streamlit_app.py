import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Proper absolute imports from sai package
from sai.bot.main import run_bot(), get_data, decide_action, SimpleModel
from sai.utils import setup_logger

logger = setup_logger("sai_streamlit")

def main():
    st.set_page_config(page_title="SAI Trading Bot Dashboard", layout="wide")
    st.title("📈 SAI Trading Bot Dashboard")

    # Sidebar controls
    st.sidebar.header("Controls")
    if st.sidebar.button("Run Bot"):
        action = run_bot()
        st.success(f"Bot Action: {action}")
        logger.info(f"Bot executed action: {action}")

    if st.sidebar.button("Refresh Data"):
        data = get_data()
        st.write("Latest Market Data Snapshot:", data)
        logger.info("Market data refreshed")

    if st.sidebar.button("Decide Action"):
        data = get_data()
        action = decide_action(data)
        st.info(f"Bot Decision: {action}")
        logger.info(f"Bot decision: {action}")

    if st.sidebar.button("Test Model"):
        model = SimpleModel()
        sample_data = get_data()
        prediction = model.predict(sample_data)
        st.write("Model Prediction:", prediction)
        logger.info(f"Model prediction: {prediction}")

    # Dashboard sections
    st.header("Market Data")
    data = get_data()
    if isinstance(data, pd.DataFrame):
        st.dataframe(data)
        st.line_chart(data)
    else:
        st.write(data)

    st.header("Trading Decisions")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Predictions")
        model = SimpleModel()
        sample_data = get_data()
        prediction = model.predict(sample_data)
        st.write(prediction)

    with col2:
        st.subheader("Action Distribution")
        actions = [decide_action(get_data()) for _ in range(10)]
        action_counts = pd.Series(actions).value_counts()
        st.bar_chart(action_counts)

    st.header("Logs")
    st.text("Check your logs in the console or log file for detailed traces.")

if __name__ == "__main__":
    main()# sai/streamlit_app.py 
