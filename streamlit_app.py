# streamlit_app.py
import streamlit as st
import pandas as pd
import logging

# Try imports safely
try:
    from plugins.exchanges import east_africa
except ImportError:
    east_africa = None
    logging.warning("east_africa plugin not found")

try:
    from plugins.prediction import fx_arima, fx_lstm
except ImportError:
    fx_arima, fx_lstm = None, None
    logging.warning("prediction plugins not found")

# Configure logging
logging.basicConfig(filename="logs/app.log", level=logging.INFO)

# Tabs
tabs = st.tabs(["Dashboard", "Strategy Config", "Logs", "Forecast", "Debug"])

# Dashboard Tab
with tabs[0]:
    st.header("Live FX Dashboard")
    if east_africa:
        rates = east_africa.get_rates()
        df = pd.DataFrame(rates["rates"].items(), columns=["Currency", "Rate"])
        st.write("Base:", rates["base"], "Timestamp:", rates["timestamp"])
        st.dataframe(df)
        st.bar_chart(df.set_index("Currency"))
    else:
        st.error("East Africa FX plugin not available")

# Strategy Config Tab
with tabs[1]:
    st.header("Strategy Config")
    base_currency = st.selectbox("Base Currency", ["USD", "EUR", "GBP"])
    st.write("Selected base:", base_currency)

# Logs Tab
with tabs[2]:
    st.header("System Logs")
    try:
        with open("logs/app.log") as f:
            st.text(f.read())
    except FileNotFoundError:
        st.warning("No logs yet.")

# Forecast Tab
with tabs[3]:
    st.header("FX Forecasts")
    if east_africa and fx_arima and fx_lstm:
        currency = st.selectbox("Select Currency", east_africa.CURRENCIES)
        horizon = st.slider("Forecast Horizon (days)", 7, 30, 7)

        # Prepare series
        series = pd.Series(list(east_africa.get_rates()["rates"].values()))

        # ARIMA forecast
        arima_preds = fx_arima.forecast(series, steps=horizon)
        st.line_chart(pd.Series(arima_preds, name="ARIMA Forecast"))

        # LSTM forecast
        lstm_model = fx_lstm.train_lstm(series.values, epochs=5)
        lstm_preds = fx_lstm.forecast(lstm_model, series.values, steps=horizon)
        st.line_chart(pd.Series(lstm_preds, name="LSTM Forecast"))
    else:
        st.error("Prediction modules not available")

# Debug Tab
with tabs[4]:
    st.header("Debug Tools")
    st.write("Session State:", st.session_state)
