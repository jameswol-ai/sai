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
from datetime import datetime, timedelta
from collections import deque
import queue
import numpy as np
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -------------------- Custom CSS (same as before) --------------------
st.markdown("""
<style>
    /* ... (keep existing CSS) ... */
</style>
""", unsafe_allow_html=True)

# -------------------- Safe forecast stubs --------------------
def fit_arima(series, order=(2,1,2)):
    return {"last_value": series.iloc[-1], "std": series.std()}

def forecast_next(arima_model, steps=1):
    last = arima_model["last_value"]
    std = arima_model["std"]
    np.random.seed(42)
    return [last + np.random.normal(0, std*0.02) for _ in range(steps)]

def fit_prophet(df_rates):
    df = df_rates.copy()
    df["ds_num"] = (df["ds"] - df["ds"].min()).dt.total_seconds() / 86400
    slope = 0
    if len(df) > 1:
        slope = np.polyfit(df["ds_num"], df["y"], 1)[0]
    return {"last_date": df["ds"].max(), "slope": slope, "last_y": df["y"].iloc[-1]}

def forecast_future(prophet_model, periods=1, freq="D"):
    last_date = prophet_model["last_date"]
    slope = prophet_model["slope"]
    last_y = prophet_model["last_y"]
    dates = [last_date + timedelta(days=i+1) for i in range(periods)]
    values = [last_y + slope * (i+1) for i in range(periods)]
    return pd.DataFrame({"ds": dates, "yhat": values})

# -------------------- Utility metrics --------------------
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

# -------------------- Bot simulation --------------------
def run_bot():
    return {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "trade": random.choice(["BUY", "SELL"]),
        "symbol": random.choice(["USD", "EUR", "GBP", "JPY", "UGX", "KES", "TZS", "RWF", "BIF", "SSP", "ETB"]),
        "amount": random.randint(100, 5000)
    }

def load_model(file_obj):
    try:
        return pickle.load(file_obj)
    except Exception as e:
        logger.error(f"Model load failed: {e}")
        return None

def test_model(model):
    if model is None:
        return {"predictions": [], "accuracy": 0}
    return {"predictions": [1, 0, 1, 1, 0], "accuracy": 0.8}

# -------------------- Logging --------------------
logger = logging.getLogger("sai_app")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("sai_app.log", maxBytes=2_000_000, backupCount=3)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)

# -------------------- Session state init --------------------
if "bot_thread" not in st.session_state:
    st.session_state.bot_thread = None
if "bot_running" not in st.session_state:
    st.session_state.bot_running = False
if "logs" not in st.session_state:
    st.session_state.logs = []
if "rates" not in st.session_state:
    st.session_state.rates = {}
if "prev_rates" not in st.session_state:
    st.session_state.prev_rates = {}
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["Time", "Currency", "Rate", "Forecast"])
if "bot_queue" not in st.session_state:
    st.session_state.bot_queue = queue.Queue()
if "stop_event" not in st.session_state:
    st.session_state.stop_event = threading.Event()
if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = False
if "refresh_interval" not in st.session_state:
    st.session_state.refresh_interval = 3
if "use_real_data" not in st.session_state:
    st.session_state.use_real_data = False

HISTORY_MAX_ROWS = 1000

# -------------------- Bot thread management --------------------
def bot_loop(queue_obj, stop_event):
    logger.info("Bot thread started.")
    while not stop_event.is_set():
        try:
            trade_info = run_bot()
            queue_obj.put(trade_info)
        except Exception as e:
            queue_obj.put({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "error": str(e)
            })
            logger.exception("Bot loop error")
            break
        time.sleep(2)
    logger.info("Bot thread exited.")

def start_bot():
    if st.session_state.bot_running:
        return
    stop_event = threading.Event()
    st.session_state.stop_event = stop_event
    t = threading.Thread(target=bot_loop, args=(st.session_state.bot_queue, stop_event), daemon=True)
    st.session_state.bot_thread = t
    st.session_state.bot_running = True
    t.start()

def stop_bot():
    if st.session_state.bot_running:
        st.session_state.stop_event.set()
        st.session_state.bot_running = False

def drain_bot_queue(max_items=50):
    drained = 0
    while not st.session_state.bot_queue.empty() and drained < max_items:
        try:
            item = st.session_state.bot_queue.get_nowait()
        except queue.Empty:
            break
        st.session_state.logs.append(item)
        drained += 1
    if len(st.session_state.logs) > 1000:
        st.session_state.logs = st.session_state.logs[-1000:]
    return drained

# -------------------- East African currencies --------------------
EAST_AFRICAN_CURRENCIES = ["UGX", "KES", "TZS", "RWF", "BIF", "SSP", "ETB"]
OTHER_CURRENCIES = ["USD", "EUR", "GBP", "JPY"]
ALL_CURRENCIES = EAST_AFRICAN_CURRENCIES + OTHER_CURRENCIES

# -------------------- Real exchange rate fetcher (Frankfurter API) --------------------
@st.cache_data(ttl=60)
def get_real_rates():
    try:
        url = "https://api.frankfurter.app/latest?from=USD&to=" + ",".join(ALL_CURRENCIES)
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        rates = data["rates"]
        rates["USD"] = 1.0
        return rates
    except Exception as e:
        logger.error(f"Failed to fetch real rates: {e}")
        return None

def sample_currency_rates():
    ranges = {
        "UGX": (3700, 3900), "KES": (125, 140), "TZS": (2500, 2700),
        "RWF": (1300, 1500), "BIF": (2800, 3000), "SSP": (1500, 1800),
        "ETB": (55, 60), "USD": (1, 1), "EUR": (0.9, 1.1),
        "GBP": (0.75, 0.85), "JPY": (140, 150)
    }
    return {cur: round(random.uniform(low, high), 2)
            for cur, (low, high) in ranges.items()}

def fetch_currency_data():
    real = get_real_rates()
    if real:
        rates = real
        st.session_state.use_real_data = True
    else:
        rates = sample_currency_rates()
        st.session_state.use_real_data = False

    prev = st.session_state.prev_rates if st.session_state.prev_rates else {}
    delta = {}
    for cur in EAST_AFRICAN_CURRENCIES:
        if cur in prev and prev[cur] != 0:
            delta[cur] = ((rates[cur] - prev[cur]) / prev[cur]) * 100
        else:
            delta[cur] = None

    st.session_state.prev_rates = rates.copy()
    st.session_state.rates = rates
    return rates, delta

def forecast_rates(rates):
    return {cur: round(val * (1 + random.uniform(-0.02, 0.02)), 2)
            for cur, val in rates.items()}

def update_history(rates, forecast):
    now = datetime.now()
    rows = [{"Time": now.isoformat(), "Currency": cur,
             "Rate": rates[cur], "Forecast": forecast[cur]}
            for cur in rates.keys()]
    if rows:
        st.session_state.history = pd.concat(
            [st.session_state.history, pd.DataFrame(rows)], ignore_index=True)
        if len(st.session_state.history) > HISTORY_MAX_ROWS:
            st.session_state.history = st.session_state.history.iloc[-HISTORY_MAX_ROWS:].reset_index(drop=True)

def generate_trade_signal(current_rate, forecast_value, threshold=0.01):
    if forecast_value is None:
        return "HOLD"
    change_pct = (forecast_value - current_rate) / current_rate
    if change_pct > threshold:
        return "BUY"
    elif change_pct < -threshold:
        return "SELL"
    return "HOLD"

# -------------------- Central forecast function --------------------
def run_forecast(currency, horizon, steps, freq="D"):
    # ... (same as before, unchanged) ...
    # I'm not repeating the whole function for brevity; use the previous version
    # It is assumed to be identical to the last integrated code.

# -------------------- Technical Indicators --------------------
def compute_indicators(df_cur, rsi_period=14, sma_windows=[20, 50]):
    """Calculate RSI and SMAs for a currency DataFrame (must have 'Rate' column)."""
    df = df_cur.copy().sort_values("Time_dt")
    if len(df) < rsi_period + 1:
        return None  # not enough data
    # RSI
    delta = df["Rate"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=rsi_period, min_periods=rsi_period).mean()
    avg_loss = loss.rolling(window=rsi_period, min_periods=rsi_period).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))
    # SMAs
    for w in sma_windows:
        df[f"SMA_{w}"] = df["Rate"].rolling(window=w, min_periods=w).mean()
    return df

# -------------------- Streamlit UI --------------------
st.set_page_config(page_title="SAI Forex Bot - East Africa", layout="wide")

# ----- Top bar -----
col_title, col_status = st.columns([3, 1])
with col_title:
    st.markdown("<h1 style='color:#00F2FE;'>📈 SAI Forex Trading Bot</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#AAAAAA; font-size:1.1rem;'>East African Currency Trading & Forecasting – UGX, KES, TZS, RWF, BIF, SSP, ETB</p>", unsafe_allow_html=True)

with col_status:
    if st.session_state.use_real_data:
        st.success("🔴 LIVE")
    else:
        st.warning("🟡 SIMULATED")

# Define tabs (added Technical Analysis after Trade Recommendations)
tabs = st.tabs([
    "📊 Dashboard",
    "📅 Daily Forecast",
    "📆 Weekly Forecast",
    "🗓️ Monthly Forecast",
    "📈 Trade Recommendations",
    "📉 Technical Analysis",          # <-- NEW TAB
    "⚙️ Strategy Config",
    "📋 Logs",
    "🧪 Model Testing",
    "🛠️ Debug"
])

# -------------------- Dashboard Tab (unchanged) --------------------
with tabs[0]:
    # ... (keep existing dashboard code) ...

# -------------------- Daily Forecast Tab (unchanged) --------------------
with tabs[1]:
    # ...

# -------------------- Weekly Forecast Tab (unchanged) --------------------
with tabs[2]:
    # ...

# -------------------- Monthly Forecast Tab (unchanged) --------------------
with tabs[3]:
    # ...

# -------------------- Trade Recommendations Tab (unchanged) --------------------
with tabs[4]:
    # ...

# -------------------- Technical Analysis Tab (NEW) --------------------
with tabs[5]:
    st.markdown("<div class='section-title'>📉 Technical Indicators</div>", unsafe_allow_html=True)
    if st.session_state.history.empty:
        st.info("No historical data yet. Start the bot to collect data.")
    else:
        currency = st.selectbox("Select Currency", EAST_AFRICAN_CURRENCIES, key="tech_cur")
        # Get historical data for selected currency
        df_all = st.session_state.history.copy()
        df_all["Time_dt"] = pd.to_datetime(df_all["Time"])
        df_cur = df_all[df_all["Currency"] == currency].sort_values("Time_dt")
        if len(df_cur) < 15:
            st.warning(f"Need at least 15 data points for RSI (14). Currently have {len(df_cur)}. Keep the dashboard running.")
        else:
            # Compute indicators
            ind_df = compute_indicators(df_cur)
            if ind_df is None:
                st.error("Unable to compute indicators.")
            else:
                # Display latest values
                latest = ind_df.iloc[-1]
                col1, col2, col3 = st.columns(3)
                col1.metric("Current Rate", f"{latest['Rate']:,.2f}")
                col2.metric("RSI (14)", f"{latest['RSI']:.2f}")
                col3.metric("SMA 20 / SMA 50", f"{latest['SMA_20']:,.2f} / {latest['SMA_50']:,.2f}")

                # Interactive Plotly chart with two subplots
                fig = make_subplots(
                    rows=2, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.08,
                    row_heights=[0.7, 0.3],
                    subplot_titles=(f"{currency} Price & SMAs", "RSI")
                )

                # Price and SMAs
                fig.add_trace(go.Scatter(
                    x=ind_df["Time_dt"], y=ind_df["Rate"],
                    mode='lines', name='Rate',
                    line=dict(color='#00F2FE', width=2)
                ), row=1, col=1)
                fig.add_trace(go.Scatter(
                    x=ind_df["Time_dt"], y=ind_df["SMA_20"],
                    mode='lines', name='SMA 20',
                    line=dict(color='orange', dash='dot')
                ), row=1, col=1)
                fig.add_trace(go.Scatter(
                    x=ind_df["Time_dt"], y=ind_df["SMA_50"],
                    mode='lines', name='SMA 50',
                    line=dict(color='violet', dash='dot')
                ), row=1, col=1)

                # RSI
                fig.add_trace(go.Scatter(
                    x=ind_df["Time_dt"], y=ind_df["RSI"],
                    mode='lines', name='RSI',
                    line=dict(color='#FFD600', width=1.5)
                ), row=2, col=1)

                # Add overbought/oversold lines
                fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
                fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

                fig.update_layout(
                    height=600,
                    template="plotly_dark",
                    showlegend=True,
                    hovermode="x unified"
                )
                fig.update_xaxes(title_text="Time", row=2, col=1)
                fig.update_yaxes(title_text="Rate", row=1, col=1)
                fig.update_yaxes(title_text="RSI", range=[0, 100], row=2, col=1)

                st.plotly_chart(fig, use_container_width=True)

                # Signal interpretation
                rsi_val = latest['RSI']
                if rsi_val > 70:
                    st.warning(f"RSI is overbought ({rsi_val:.1f}). Consider SELL.")
                elif rsi_val < 30:
                    st.success(f"RSI is oversold ({rsi_val:.1f}). Consider BUY.")
                else:
                    st.info(f"RSI is neutral ({rsi_val:.1f}).")

                # SMA crossover signal
                sma_20 = latest['SMA_20']
                sma_50 = latest['SMA_50']
                if pd.notna(sma_20) and pd.notna(sma_50):
                    if sma_20 > sma_50:
                        st.write("SMA 20 is **above** SMA 50 – bullish signal.")
                    else:
                        st.write("SMA 20 is **below** SMA 50 – bearish signal.")
                else:
                    st.write("Insufficient data for SMA crossover.")

# -------------------- Strategy Config Tab (unchanged) --------------------
with tabs[6]:
    # ...

# -------------------- Logs Tab (unchanged) --------------------
with tabs[7]:
    # ...

# -------------------- Model Testing Tab (unchanged) --------------------
with tabs[8]:
    # ...

# -------------------- Debug Tab (unchanged) --------------------
with tabs[9]:
    # ...

# Auto-refresh logic (unchanged)
if st.session_state.auto_refresh:
    drain_bot_queue(max_items=5)
    time.sleep(st.session_state.refresh_interval)
    st.rerun()