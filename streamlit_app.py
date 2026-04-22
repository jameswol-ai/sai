import streamlit as st

# Proper absolute import from sai package
from main.py import run_bot, get_data, decide_action, SimpleModel
from utils.py import setup_logger

logger = setup_logger("sai_streamlit")

def main():
    st.title("SAI Trading Bot Dashboard")

    if st.sidebar.button("Run Bot"):
        action = run_bot()
        st.write("Bot Action:", action)

    if st.sidebar.button("Refresh Data"):
        data = get_data()
        st.write("Latest Data:", data)

    if st.sidebar.button("Decide Action"):
        data = get_data()
        action = decide_action(data)
        st.write("Bot Decision:", action)

    if st.sidebar.button("Test Model"):
        model = SimpleModel()
        sample_data = get_data()
        prediction = model.predict(sample_data)
        st.write("Model Prediction:", prediction)

if __name__ == "__main__":
    main()
