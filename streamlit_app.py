# =========================================================
# SAI Forex Bot – CLEAN STABLE ARCHITECTURE BUILD
# =========================================================

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
import os
import warnings
import sqlite3
from typing import Dict, List, Optional, Any, Tuple

# =========================================================
# PAGE CONFIG (ONLY ONCE)
# =========================================================
st.set_page_config(page_title="SAI Forex Bot", layout="wide")

# =========================================================
# LOGGER (MUST BE FIRST – FIXED CRASH SOURCE)
# =========================================================
logger = logging.getLogger("sai_app")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler("sai_app.log", maxBytes=2_000_000, backupCount=3)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(handler)

# =========================================================
# OPTIONAL IMPORTS (SAFE MODE)
# =========================================================
try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except:
    PLOTLY_AVAILABLE = False

try:
    from newsapi import NewsApiClient
    from textblob import TextBlob
    SENTIMENT_AVAILABLE = True
except:
    SENTIMENT_AVAILABLE = False

try:
    from streamlit_autorefresh import st_autorefresh
    AUTOREFRESH_AVAILABLE = True
except:
    AUTOREFRESH_AVAILABLE = False

# =========================================================
# GLOBAL STATE
# =========================================================
BOT_CONFIG = {
    "alert_errors": False,
    "lock": threading.Lock()
}

DB_PATH = "sai_trading.db"
DB_LOCK = threading.Lock()

ALL_CURRENCIES = ["UGX","KES","TZS","RWF","BIF","SSP","ETB","USD","EUR","GBP","JPY"]
EAST_AFRICAN_CURRENCIES = ["UGX","KES","TZS","RWF","BIF","SSP","ETB"]

# =========================================================
# DB INIT
# =========================================================
def db_connect():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db():
    conn = db_connect()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            currency TEXT,
            rate REAL,
            forecast REAL
        );
    """)
    conn.commit()
    conn.close()

# =========================================================
# SAFE RATE ENGINE
# =========================================================
@st.cache_data(ttl=5)
def get_real_rates():
    try:
        url = "https://api.frankfurter.app/latest?from=USD&to=" + ",".join(ALL_CURRENCIES)
        r = requests.get(url, timeout=5)
        data = r.json()
        rates = data.get("rates", {})
        rates["USD"] = 1.0
        return rates
    except Exception as e:
        logger.warning(f"Rate fetch failed: {e}")
        return {}

def sample_rates():
    return {c: round(random.uniform(1, 1000), 2) for c in ALL_CURRENCIES}

# =========================================================
# LIVE STATE
# =========================================================
if "live" not in st.session_state:
    st.session_state.live = {"rates": {}, "prev": {}, "lock": threading.Lock()}

def live_fetch():
    while True:
        rates = get_real_rates() or sample_rates()
        with st.session_state.live["lock"]:
            st.session_state.live["prev"] = st.session_state.live["rates"]
            st.session_state.live["rates"] = rates
        time.sleep(3)

if "thread_started" not in st.session_state:
    t = threading.Thread(target=live_fetch, daemon=True)
    t.start()
    st.session_state.thread_started = True

def get_rates():
    with st.session_state.live["lock"]:
        return (
            st.session_state.live["rates"],
            st.session_state.live["prev"]
        )

# =========================================================
# BOT SIMULATION (SAFE)
# =========================================================
def run_bot():
    return {
        "time": datetime.now().isoformat(),
        "trade": random.choice(["BUY","SELL"]),
        "symbol": random.choice(ALL_CURRENCIES),
        "amount": random.randint(100,5000)
    }

# =========================================================
# UI
# =========================================================
st.title("📊 SAI Forex Bot (Clean Core)")

rates, prev = get_rates()

cols = st.columns(4)

for i, c in enumerate(EAST_AFRICAN_CURRENCIES):
    with cols[i % 4]:
        r = rates.get(c, 0)
        p = prev.get(c, r)
        delta = ((r - p) / p * 100) if p else 0

        st.metric(
            label=f"USD/{c}",
            value=f"{r:.2f}",
            delta=f"{delta:.2f}%"
        )

st.markdown("---")

# =========================================================
# SIMPLE BOT TRIGGER
# =========================================================
if st.button("Run Bot Tick"):
    result = run_bot()
    st.json(result)

# =========================================================
# DEBUG
# =========================================================
with st.expander("Debug State"):
    st.json({
        "rates": rates,
        "prev": prev
    })