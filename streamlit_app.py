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

# --- Safe stubs (replace with real implementations later) ---
def run_bot():
    """Simulate a trading decision from a bot."""
    return {"time": datetime.now().strftime("%H:%M:%S"), "trade": "BUY", "symbol": "EURUSD", "amount": 1000}

def load_model(file_obj):
    """Load a pickled model safely."""
    # Real implementation should validate model type and contents
    return pickle.load(file_obj)

def test_model(model):
    """Run a quick smoke test on the model."""
    return {"predictions": [1, 0, 1, 1, 0], "accuracy": 0.8}

# --- Logging configuration with rotation ---
logger = logging.getLogger("sai_app")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("sai_app.log", maxBytes=2_000_000, backupCount=3)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# --- Session state initialization ---
if "bot_thread" not in st.session_state:
    st.session_state.bot_thread = None
if "bot_running" not in st.session_state:
    st.session_state.bot_running = False
if "logs" not in st.session_state:
    st.session_state.logs = []  # list of dicts or strings
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
    st.session_state.refresh_interval = 3  # seconds

HISTORY_MAX_ROWS = 500

# --- Bot thread management using queue for safe cross-thread comms ---
def bot_loop(queue_obj, stop_event):
    logger.info("Bot thread started.")
    try:
        while not stop_event.is_set():
            try:
                trade_info = run_bot()
                # Put a copy into the queue for the main thread to consume
                queue_obj.put(trade_info)
                logger.debug("Bot produced: %s", trade_info)
            except Exception as e:
                err = {"time": datetime.now().strftime("%H:%M:%S"), "error": str(e), "trace": traceback.format_exc()}
                queue_obj.put(err)
                logger.exception("Exception in bot loop")
                break
            # Sleep a short while to simulate work
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

# --- Currency & Forecast Helpers ---
@st.cache_data(ttl=2)
def sample_currency_rates():
    """Return a sample set of currency rates. Cached briefly to avoid re-sampling on every rerun."""
    currencies = ["USD", "EUR", "GBP", "JPY", "UGX", "KES", "TZS", "RWF", "SSP"]
    rates = {cur: round(random.uniform(0.5, 1500), 2) for cur in currencies}
    return rates

def fetch_currency_data():
    """Fetch or sample currency rates and store in session state."""
    rates = sample_currency_rates()
    st.session_state.rates = rates
    return rates

def forecast_rates(rates):
    """Create a simple randomized forecast based on current rates."""
    forecast = {cur: round(val * (1 + random.uniform(-0.05, 0.05)), 2) for cur, val in rates.items()}
    return forecast

def update_history(rates, forecast):
    """Append current snapshot to history and cap its size."""
    now = datetime.now().strftime("%H:%M:%S")
    rows = []
    for cur in rates.keys():
        rows.append({"Time": now, "Currency": cur, "Rate": rates[cur], "Forecast": forecast[cur]})
    if rows:
        st.session_state.history = pd.concat([st.session_state.history, pd.DataFrame(rows)], ignore_index=True)
        # Cap history size
        if len(st.session_state.history) > HISTORY_MAX_ROWS:
            st.session_state.history = st.session_state.history.iloc[-HISTORY_MAX_ROWS:].reset_index(drop=True)

def drain_bot_queue():
    """Move all items from the bot queue into session_state.logs and history where appropriate."""
    drained = 0
    while not st.session_state.bot_queue.empty():
        try:
            item = st.session_state.bot_queue.get_nowait()
        except queue.Empty:
            break
        drained += 1
        # Normalize and store
        if isinstance(item, dict) and "trade" in item:
            st.session_state.logs.append(item)
        else:
            # store errors or other messages as strings for display
            st.session_state.logs.append(item)
        # keep logs bounded
        if len(st.session_state.logs) > 1000:
            st.session_state.logs = st.session_state.logs[-1000:]
    if drained:
        logger.info("Drained %d items from bot queue.", drained)
    return drained

# --- Streamlit UI ---
st.set_page_config(page_title="SAI Trading Bot", layout="wide")
st.title("📈 SAI Trading Bot Dashboard")

tabs = st.tabs(["Dashboard", "Strategy Config", "Logs", "Model Testing", "Debug"])

# Dashboard Tab
with tabs[0]:
    st.header("Live Trading Dashboard")
    col1, col2 = st.columns([1, 1])

    with col1:
        start_col, stop_col = st.columns(2)
        with start_col:
            if st.button("Start Bot", disabled=st.session_state.bot_running):
                start_bot()
        with stop_col:
            if st.button("Stop Bot", disabled=not st.session_state.bot_running):
                stop_bot()

        st.write("**Auto Refresh**")
        auto = st.checkbox("Enable auto refresh", value=st.session_state.auto_refresh)
        st.session_state.auto_refresh = auto
        if auto:
            interval = st.slider("Refresh interval seconds", 1, 10, st.session_state.refresh_interval)
            st.session_state.refresh_interval = interval
            # If auto-refresh is enabled, attempt to drain queue now
            drained = drain_bot_queue()
        else:
            if st.button("Refresh Now"):
                drained = drain_bot_queue()

    with col2:
        st.write("💱 Currency Rates")
        rates = fetch_currency_data()
        st.table(pd.DataFrame(rates.items(), columns=["Currency", "Rate"]))

        st.write("📊 Forecasted Rates")
        forecast = forecast_rates(rates)
        st.table(pd.DataFrame(forecast.items(), columns=["Currency", "Forecast"]))

        update_history(rates, forecast)

        # Graph visualization
        fig, ax = plt.subplots(figsize=(8, 4))
        x = list(rates.keys())
        current_vals = list(rates.values())
        forecast_vals = [forecast[k] for k in x]
        width = 0.35
        ax.bar([i - width/2 for i in range(len(x))], current_vals, width=width, alpha=0.7, label="Current")
        ax.bar([i + width/2 for i in range(len(x))], forecast_vals, width=width, alpha=0.7, label="Forecast")
        ax.set_ylabel("Rate")
        ax.set_title("Currency Rates vs Forecast")
        ax.set_xticks(range(len(x)))
        ax.set_xticklabels(x)
        ax.legend()
        st.pyplot(fig)

        # Daily trend graph
        if not st.session_state.history.empty:
            fig2, ax2 = plt.subplots(figsize=(10, 4))
            # Plot only a subset of currencies to keep the plot readable
            currencies_to_plot = list(rates.keys())[:6]
            for cur in currencies_to_plot:
                df_cur = st.session_state.history[st.session_state.history["Currency"] == cur]
                if not df_cur.empty:
                    ax2.plot(df_cur["Time"], df_cur["Rate"], label=f"{cur} Rate")
                    ax2.plot(df_cur["Time"], df_cur["Forecast"], linestyle="--", label=f"{cur} Forecast")
            ax2.set_title("Recent Currency Trends")
            ax2.set_xlabel("Time")
            ax2.set_ylabel("Value")
            ax2.legend(loc="upper left", bbox_to_anchor=(1.02, 1))
            plt.xticks(rotation=45)
            st.pyplot(fig2)

    st.write("Trade Logs (latest 10)")
    # Show last 10 logs in a friendly DataFrame if possible
    try:
        df_logs = pd.DataFrame(st.session_state.logs[-10:])
        st.table(df_logs)
    except Exception:
        st.write(st.session_state.logs[-10:])

# Strategy Config Tab
with tabs[1]:
    st.header("Strategy Configuration")
    risk_level = st.slider("Risk Level", 1, 10, 5)
    st.write(f"**Selected Risk Level:** {risk_level}")
    st.write("You can add more strategy parameters here such as stop loss, take profit, position sizing rules, and indicators.")

# Logs Tab
with tabs[2]:
    st.header("Application Logs")
    try:
        with open("sai_app.log", "r") as f:
            log_lines = f.readlines()[-200:]
        st.text("".join(log_lines))
    except FileNotFoundError:
        st.info("No logs yet.")
    except Exception:
        st.error("Unable to read log file. See debug tab for details.")
        logger.exception("Error reading log file")

# Model Testing Tab
with tabs[3]:
    st.header("Model Testing")
    uploaded_model = st.file_uploader("Upload model.pkl", type=["pkl"])
    if uploaded_model:
        try:
            # Ensure we read from the start
            uploaded_model.seek(0)
            model = load_model(uploaded_model)
            st.success("Model loaded successfully.")
            test_results = test_model(model)
            st.write("Test Results:", test_results)

            fig, ax = plt.subplots()
            ax.plot(test_results.get("predictions", []), marker="o", label="Predictions")
            ax.set_title("Model Predictions")
            ax.legend()
            st.pyplot(fig)
        except (pickle.UnpicklingError, EOFError) as e:
            st.error("Uploaded file is not a valid pickle model.")
            logger.exception("Model load error")
        except Exception as e:
            st.error("An error occurred while loading or testing the model.")
            logger.exception("Unexpected model test error")

# Debug Tab
with tabs[4]:
    st.header("Debug Information")
    st.write("**Session State Keys:**", list(st.session_state.keys()))
    st.write("**Bot Running:**", st.session_state.bot_running)
    st.write("**Queue Size:**", st.session_state.bot_queue.qsize())
    st.write("**History Rows:**", len(st.session_state.history))
    if st.button("Drain Bot Queue (debug)"):
        drained = drain_bot_queue()
        st.write(f"Drained {drained} items from queue.")
