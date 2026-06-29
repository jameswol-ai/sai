# sai/streamlit_app.py
import streamlit as st
import threading
import time
import logging
from logging.handlers import RotatingFileHandler
import matplotlib.pyplot as plt
import pandas as pd
import random
import pickle
from datetime import datetime
import queue
import traceback
import numpy as np

# --- Forecast plugin imports ---
try:
    from plugins.arima_forecast import fit_arima, forecast_next
except Exception:
    def fit_arima(series, order=(2, 1, 2)):
        raise RuntimeError("ARIMA plugin not available")
    def forecast_next(model_fit, steps=1):
        raise RuntimeError("ARIMA plugin not available")

try:
    from plugins.prophet_forecast import fit_prophet, forecast_future
except Exception:
    def fit_prophet(df_rates):
        raise RuntimeError("Prophet plugin not available")
    def forecast_future(model, periods=1, freq="D"):
        raise RuntimeError("Prophet plugin not available")

# --- Utility metrics ---
def compute_metrics(actual, predicted):
    actual = np.array(actual, dtype=float)
    predicted = np.array(predicted, dtype=float)
    if actual.size == 0 or predicted.size == 0:
        return {"RMSE": None, "MAPE": None}
    n = min(len(actual), len(predicted))
    actual = actual[-n:]
    predicted = predicted[:n]
    rmse = float(np.sqrt(np.mean((actual - predicted) ** 2)))
    denom = np.where(actual == 0, 1e-8, actual)
    mape = float(np.mean(np.abs((actual - predicted) / denom)) * 100)
    return {"RMSE": round(rmse, 6), "MAPE": round(mape, 4)}

# --- Bot stubs ---
def run_bot():
    return {
        "time": datetime.now().strftime("%H:%M:%S"),
        "trade": random.choice(["BUY", "SELL"]),
        "symbol": random.choice(["USD", "EUR", "GBP", "JPY", "UGX"]),
        "amount": random.randint(100, 5000)
    }

def load_model(file_obj):
    return pickle.load(file_obj)

def test_model(model):
    return {"predictions": [1, 0, 1, 1, 0], "accuracy": 0.8}

# --- Logging ---
logger = logging.getLogger("sai_app")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("sai_app.log", maxBytes=2_000_000, backupCount=3)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)

# --- Session state ---
if "bot_thread" not in st.session_state:
    st.session_state.bot_thread = None
if "bot_running" not in st.session_state:
    st.session_state.bot_running = False
if "logs" not in st.session_state:
    st.session_state.logs = []
if "rates" not in st.session_state:
    st.session_state.rates = {}
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["Time", "Currency", "Rate", "Forecast"])
if "bot_queue" not in st.session_state:
    st.session_state.bot_queue = queue.Queue()
if "bot_lock" not in st.session_state:
    st.session_state.bot_lock = threading.Lock()
if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = False
if "refresh_interval" not in st.session_state:
    st.session_state.refresh_interval = 3

HISTORY_MAX_ROWS = 500

# --- Bot thread ---
def bot_loop(queue_obj, stop_event):
    logger.info("Bot thread started.")
    try:
        while not stop_event.is_set():
            try:
                trade_info = run_bot()
                queue_obj.put(trade_info)
                logger.debug("Bot produced: %s", trade_info)
            except Exception as e:
                err = {"time": datetime.now().strftime("%H:%M:%S"), "error": str(e), "trace": traceback.format_exc()}
                queue_obj.put(err)
                logger.exception("Exception in bot loop")
                break
            time.sleep(2)
    finally:
        logger.info("Bot thread exiting.")

def start_bot():
    if st.session_state.bot_running:
        return
    stop_event = threading.Event()
    st.session_state.stop_event = stop_event
    t = threading.Thread(target=bot_loop, args=(st.session_state.bot_queue, stop_event), daemon=True)
    st.session_state.bot_thread = t
    st.session_state.bot_running = True
    t.start()
    logger.info("Bot start requested.")

def stop_bot():
    if not st.session_state.bot_running:
        return
    try:
        st.session_state.stop_event.set()
    except Exception:
        logger.exception("Error setting stop event")
    st.session_state.bot_running = False
    logger.info("Bot stop requested.")

def drain_bot_queue():
    drained = 0
    while not st.session_state.bot_queue.empty():
        try:
            item = st.session_state.bot_queue.get_nowait()
        except queue.Empty:
            break
        drained += 1
        st.session_state.logs.append(item)
        if isinstance(item, dict) and "trade" in item:
            st.session_state.history = pd.concat(
                [st.session_state.history,
                 pd.DataFrame([{"Time": item["time"], "Currency": item["symbol"], "Rate": item["amount"], "Forecast": None}])],
                ignore_index=True
            )
        if len(st.session_state.logs) > 1000:
            st.session_state.logs = st.session_state.logs[-1000:]
    if drained:
        logger.info("Drained %d items from bot queue.", drained)
    if len(st.session_state.history) > HISTORY_MAX_ROWS:
        st.session_state.history = st.session_state.history.iloc[-HISTORY_MAX_ROWS:].reset_index(drop=True)
    return drained

# --- Currency helpers ---
@st.cache_data(ttl=2)
def sample_currency_rates():
    currencies = ["USD", "EUR", "GBP", "JPY", "UGX", "KES", "TZS", "RWF", "SSP"]
    rates = {cur: round(random.uniform(0.5, 1500), 2) for cur in currencies}
    return rates

def fetch_currency_data():
    rates = sample_currency_rates()
    st.session_state.rates = rates
    return rates

def forecast_rates(rates):
    forecast = {cur: round(val * (1 + random.uniform(-0.05, 0.05)), 2) for cur, val in rates.items()}
    return forecast

# --- Streamlit UI ---
st.set_page_config(page_title="SAI Trading Bot", layout="wide")
st.title("📈 SAI Trading Bot Dashboard")

tabs = st.tabs([
    "Dashboard",
    "Strategy Config",
    "Logs",
    "Model Testing",
    "Debug",
    "Weekly Forecast",
    "Multi-Currency Forecasts"
])

# --- Dashboard Tab ---
with tabs[0]:
    st.header("Dashboard")

    # Sidebar controls
    st.sidebar.subheader("Controls")
    if st.sidebar.button("Start Bot"):
        start_bot()
    if st.sidebar.button("Stop Bot"):
        stop_bot()

    st.sidebar.checkbox("Auto Refresh", key="auto_refresh")
    st.sidebar.slider("Refresh Interval (sec)", 1, 10, st.session_state.refresh_interval, key="refresh_interval")

    # Auto refresh
    if st.session_state.auto_refresh:
        st_autorefresh(interval=st.session_state.refresh_interval * 1000)

    # Drain queue and update history
    drain_bot_queue()

    if not st.session_state.history.empty:
        st.subheader("Recent Trades")
        st.dataframe(st.session_state.history.tail(20))

        st.subheader("Trade Counts by Symbol")
        trade_counts = st.session_state.history["Currency"].value_counts()
        st.bar_chart(trade_counts)

# Other tabs (Strategy Config, Logs, Forecasts) can be extended similarly
