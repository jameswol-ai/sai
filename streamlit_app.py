# streamlit_app.py
import streamlit as st
import pandas as pd
import logging

logging.basicConfig(filename="logs/app.log", level=logging.INFO)

tabs = st.tabs(["Dashboard", "Strategy Config", "Logs", "Forecast", "Debug"])

# Strategy Config
with tabs[1]:
    st.header("Strategy Config")
    base_currency = st.selectbox("Base Currency", ["USD", "EUR", "GBP"])
    st.write("Selected base:", base_currency)

# Logs
with tabs[2]:
    st.header("System Logs")
    try:
        with open("logs/app.log") as f:
            st.text(f.read())
    except FileNotFoundError:
        st.warning("No logs yet.")

# Debug
with tabs[4]:
    st.header("Debug Tools")
    st.write("Session State:", st.session_state)
