# sai/streamlit_app.py 

 import streamlit as st

# Correct imports using dot notation
from sai.bot.main import run_bot, get_data, decide_action, SimpleModel
from sai.utils import setup_logger

# Configure logger for Streamlit app
logger = setup_logger("sai_streamlit")

def main():
    st.title("📈 SAI Trading Bot Dashboard")
    st.sidebar.header("Controls")

    # Run bot
    if st.sidebar.button("Run Bot"):
        action = run_bot()
        st.success(f"Bot executed. Action: {action}")
        logger.info(f"Streamlit triggered bot run: {action}")

    # Refresh data
    if st.sidebar.button("Refresh Data"):
        data = get_data()
        st.subheader("Latest Market Data")
        st.write(data)
        logger.info("Data refreshed in Streamlit")

    # Decide action
    if st.sidebar.button("Decide Action"):
        data = get_data()
        action = decide_action(data)
        st.subheader("Bot Decision")
        st.write(action)
        logger.info(f"Decision made: {action}")

    # Test model
    if st.sidebar.button("Test Model"):
        model = SimpleModel()
        sample_data = get_data()
        prediction = model.predict(sample_data)
        st.subheader("Model Prediction")
        st.write(prediction)
        logger.info(f"Model tested: {prediction}")

if __name__ == "__main__":
    main()
