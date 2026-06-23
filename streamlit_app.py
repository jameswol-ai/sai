# streamlit_app.py
import streamlit as st
import pandas as pd
import logging

# Import plugins safely
try:
    from plugins.exchanges import east_africa
except Exception as e:
    east_africa = None
    logging.error(f"Failed to import east_africa plugin: {e}")

try:
    from plugins.prediction import fx_arima, fx_lstm
except Exception as e:
    fx_arima, fx_lstm = None, None
    logging.error(f"Failed to import prediction plugins: {e}")

# Configure logging
logging.basicConfig(filename="logs/app.log", level=logging.INFO)

# Tabs
tabs = st.tabs(["Dashboard", "Strategy Config", "Logs", "Forecast", "Debug"])

# Dashboard Tab
with tabs[0]:
    st.header("Live FX Dashboard")
    if east_africa:
        try:
            rates = east_africa.get_rates()
            df = pd.DataFrame(rates["rates"].items(), columns=["Currency", "Rate"])
            st.write("Base:", rates["base"], "Timestamp:", rates["timestamp"])
            st.dataframe(df)
            st.bar_chart(df.set_index("Currency"))
        except Exception as e:
            st.error(f"Error fetching FX rates: {e}")
    else:
        st.warning("East Africa FX plugin not available.")

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
    except Exception as e:
        st.error(f"Error reading logs: {e}")

# Forecast Tab
with tabs[3]:
    st.header("FX Forecasts")
    if east_africa and fx_arima and fx_lstm:
        try:
            currency = st.selectbox("Select Currency", east_africa.CURRENCIES)
            horizon = st.slider("Forecast Horizon (days)", 7, 30, 7)

            series = pd.Series(list(east_africa.get_rates()["rates"].values()))

            # ARIMA forecast
            arima_preds = fx_arima.forecast(series, steps=horizon)
            st.line_chart(pd.Series(arima_preds, name="ARIMA Forecast"))

            # LSTM forecast
            lstm_model = fx_lstm.train_lstm(series.values, epochs=5)
            lstm_preds = fx_lstm.forecast(lstm_model, series.values, steps=horizon)
            st.line_chart(pd.Series(lstm_preds, name="LSTM Forecast"))
        except Exception as e:
            st.error(f"Error generating forecasts: {e}")
    else:
        st.warning("Prediction modules not available.")

# Debug Tab
with tabs[4]:
    st.header("Debug Tools")
    st.write("Session State:", st.session_state)
