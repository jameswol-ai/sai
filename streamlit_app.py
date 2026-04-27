# sai/streamlit_app.py

from random.core.intent_engine import IntentEngine
from random.core.city import City   # or memory, depending on your design

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from sai.bot.main import run_bot, get_data, load_model, test_model

def main():
    st.title("SAI Trading Bot Dashboard")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Dashboard", "Strategy Config", "Logs", "Model Testing", "Debug"]
    )

    with tab1:
        st.header("Live Trading")
        if st.button("Start Bot"):
            run_bot()

    with tab2:
        st.header("Configure Strategy")
        st.write("Strategy parameters go here.")

    with tab3:
        st.header("Logs")
        st.write("Logs will be displayed here.")

    with tab4:
        st.header("Model Testing")
        data = get_data()
        model = load_model()
        results = test_model(model, data)
        st.write(results)

    with tab5:
        st.header("Debug")
        st.write("Debugging info here.")

if __name__ == "__main__":
    main()
