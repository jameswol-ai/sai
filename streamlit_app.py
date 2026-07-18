# ============================================================
# SAI AI Forex Trading Bot - Full Streamlit Dashboard
# Merged Version: UI from PART 4/4 + Backend from v3.0
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import hashlib
import random
import time
from pathlib import Path
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="SAI AI Forex Bot",
    page_icon="📈",
    layout="wide"
)

BASE_DIR = Path(__file__).parent
USER_DB = BASE_DIR / "sai_users.db"
TRADE_DB = BASE_DIR / "sai_trading.db"

# ============================================================
# DATABASE SETUP
# ============================================================
def connect(db_path):
    return sqlite3.connect(db_path, check_same_thread=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_database():
    conn = connect(USER_DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            password TEXT,
            role TEXT
        )
    """)
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if count == 0:
        conn.execute(
            "INSERT INTO users VALUES(?,?,?)",
            ("admin", hash_password("admin123"), "admin")
        )
    conn.commit()
    conn.close()

    conn = connect(TRADE_DB)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS trades(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            time TEXT,
            symbol TEXT,
            action TEXT,
            price REAL,
            pnl REAL
        );
        CREATE TABLE IF NOT EXISTS balance(
            username TEXT PRIMARY KEY,
            amount REAL
        );
    """)
    # Initialize balance for admin if not exist
    cur = conn.execute("SELECT amount FROM balance WHERE username='admin'")
    if cur.fetchone() is None:
        conn.execute("INSERT INTO balance VALUES(?,?)", ("admin", 10000.0))
    conn.commit()
    conn.close()

init_database()

# ============================================================
# USER SYSTEM
# ============================================================
def login(username, password):
    conn = connect(USER_DB)
    row = conn.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    ).fetchone()
    conn.close()
    if row:
        return True, row[0]
    return False, None

def register(username, password):
    try:
        conn = connect(USER_DB)
        conn.execute(
            "INSERT INTO users VALUES(?,?,?)",
            (username, hash_password(password), "user")
        )
        conn.commit()
        conn.close()
        # also create a default balance
        conn = connect(TRADE_DB)
        conn.execute("INSERT OR IGNORE INTO balance VALUES(?,?)", (username, 10000.0))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def get_users():
    conn = connect(USER_DB)
    df = pd.read_sql("SELECT username, role FROM users", conn)
    conn.close()
    return df

def remove_user(username):
    if username == "admin":
        return False
    conn = connect(USER_DB)
    conn.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()
    conn.close()
    conn = connect(TRADE_DB)
    conn.execute("DELETE FROM balance WHERE username=?", (username,))
    conn.execute("DELETE FROM trades WHERE username=?", (username,))
    conn.commit()
    conn.close()
    return True

# ============================================================
# SESSION STATE DEFAULTS
# ============================================================
defaults = {
    "logged": False,
    "username": "",
    "role": "",
    "bot_running": False,
    "risk": 2,
    "auto_trade": False,
    "balance": 10000.0,
    "trades": [],
    "signals": []
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================
# CURRENCY CONFIG
# ============================================================
CURRENCIES = {
    "UGX": 3800,
    "KES": 130,
    "TZS": 2600,
    "SSP": 1600,
    "RWF": 1350,
    "USD": 1,
    "EUR": 0.92
}

def get_market():
    """Return live market rates (simulated)."""
    data = {}
    for currency, base in CURRENCIES.items():
        data[currency] = round(base + random.uniform(-5, 5), 2)
    return data

def save_market(prices):
    # Placeholder: in production would save to a time-series DB
    pass

# ============================================================
# AI ENGINE (SIMULATED)
# ============================================================
def run_ai(prices):
    """Return AI analysis for each currency."""
    results = {}
    for currency, rate in prices.items():
        rsi = round(random.uniform(20, 80), 1)
        if rsi < 30:
            signal = "BUY"
        elif rsi > 70:
            signal = "SELL"
        else:
            signal = random.choice(["BUY", "SELL", "HOLD"])
        confidence = round(random.uniform(50, 99), 1)
        forecast = round(rate + random.uniform(-3, 3), 2)
        results[currency] = {
            "signal": signal,
            "confidence": confidence,
            "rsi": rsi,
            "forecast": forecast
        }
    return results

def forecast_currency(currency, days):
    """Return a list of forecasted rates for the given number of days."""
    current = CURRENCIES.get(currency, 1)
    forecast = []
    value = current
    for _ in range(days):
        change = random.uniform(-0.02, 0.02) * value
        value += change
        forecast.append(round(value, 2))
    return forecast

def read_bot_queue():
    """Read pending signals from the AI bot queue (simulated)."""
    return st.session_state.signals

def load_ai_memory():
    """Return a DataFrame of AI memory (dummy)."""
    return pd.DataFrame(columns=["timestamp", "event", "data"])

# ============================================================
# TRADING SYSTEM
# ============================================================
def get_account():
    """Get the current user's balance."""
    username = st.session_state.username
    conn = connect(TRADE_DB)
    row = conn.execute("SELECT amount FROM balance WHERE username=?", (username,)).fetchone()
    conn.close()
    if row:
        st.session_state.balance = row[0]
    return {"balance": st.session_state.balance}

def execute_trade(symbol, action, price):
    """Execute a trade and return PnL (simulated)."""
    username = st.session_state.username
    pnl = random.uniform(-30, 80) if action == "BUY" else random.uniform(-30, 80)

    # Update balance
    new_balance = st.session_state.balance + pnl
    st.session_state.balance = new_balance

    conn = connect(TRADE_DB)
    conn.execute(
        "UPDATE balance SET amount=? WHERE username=?",
        (new_balance, username)
    )
    conn.execute(
        "INSERT INTO trades(username, time, symbol, action, price, pnl) VALUES(?,?,?,?,?,?)",
        (username, datetime.now().isoformat(), symbol, action, price, pnl)
    )
    conn.commit()
    conn.close()
    return pnl

def get_trade_history():
    """Return trade history for the current user."""
    conn = connect(TRADE_DB)
    df = pd.read_sql(
        "SELECT * FROM trades WHERE username=? ORDER BY id DESC",
        conn,
        params=[st.session_state.username]
    )
    conn.close()
    return df

def system_status():
    return {
        "app_version": "6.0",
        "bot_running": st.session_state.bot_running,
        "auto_trade": st.session_state.auto_trade,
        "risk_level": st.session_state.risk,
        "time": datetime.now().isoformat(),
        "database": str(TRADE_DB)
    }

# ============================================================
# BOT CONTROL (SIMULATED)
# ============================================================
def start_bot():
    st.session_state.bot_running = True
    # In a real app, you would start a background thread here

def stop_bot():
    st.session_state.bot_running = False

# ============================================================
# LOGIN PAGE
# ============================================================
if not st.session_state.logged:
    st.title("🔐 SAI AI Forex Login")
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("Login"):
            ok, role = login(user, pw)
            if ok:
                st.session_state.logged = True
                st.session_state.username = user
                st.session_state.role = role
                # Load balance
                conn = connect(TRADE_DB)
                row = conn.execute("SELECT amount FROM balance WHERE username=?", (user,)).fetchone()
                if row:
                    st.session_state.balance = row[0]
                conn.close()
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        new_user = st.text_input("New Username")
        new_pw = st.text_input("New Password", type="password")
        if st.button("Create Account"):
            if register(new_user, new_pw):
                st.success("Account created! Please login.")
            else:
                st.error("Username already exists")
    st.stop()

# ============================================================
# SIDEBAR CONTROL CENTER
# ============================================================
with st.sidebar:
    st.title("⚙️ SAI Control Center")
    st.write(f"👤 {st.session_state.username}")
    st.write(f"Role: {st.session_state.role}")
    st.divider()

    st.session_state.risk = st.slider("Risk Level %", 1, 20, st.session_state.risk)
    st.session_state.auto_trade = st.checkbox("Enable AI Auto Trading", value=st.session_state.auto_trade)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶ Start"):
            start_bot()
    with col2:
        if st.button("⏹ Stop"):
            stop_bot()

    st.divider()

    if st.session_state.role == "admin":
        st.subheader("👥 Users")
        user_df = get_users()
        st.dataframe(user_df, hide_index=True, use_container_width=True)

        delete_name = st.selectbox(
            "Delete User",
            user_df["username"].tolist() if not user_df.empty else []
        )
        if st.button("Delete User"):
            if delete_name != "admin":
                remove_user(delete_name)
                st.success("User removed")
                st.rerun()
            else:
                st.error("Cannot delete admin")

    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()

# ============================================================
# HEADER
# ============================================================
st.title("📈 SAI Autonomous Forex Intelligence")
st.caption("AI Market Brain | East Africa Currency Intelligence")

# ============================================================
# ACCOUNT METRICS
# ============================================================
account = get_account()
signals = read_bot_queue()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Balance", f"${account['balance']:,.2f}")
m2.metric("Bot Status", "RUNNING" if st.session_state.bot_running else "STOPPED")
m3.metric("Risk", f"{st.session_state.risk}%")
m4.metric("Signals", len(signals))

# ============================================================
# DASHBOARD TABS
# ============================================================
tabs = st.tabs([
    "🌍 Market",
    "🧠 AI Brain",
    "🔮 Forecast",
    "💹 Trading",
    "📜 History",
    "🧬 AI Memory",
    "⚙ System"
])

# ---------------------------------------------------------
# MARKET TAB
# ---------------------------------------------------------
with tabs[0]:
    st.subheader("🌍 Live Market")
    prices = get_market()
    save_market(prices)

    market_df = pd.DataFrame({"Currency": list(prices.keys()), "Rate": list(prices.values())})
    st.dataframe(market_df, hide_index=True)

    fig = px.bar(market_df, x="Currency", y="Rate", title="Currency Rates")
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# AI BRAIN TAB
# ---------------------------------------------------------
with tabs[1]:
    st.subheader("🧠 SAI AI Decision Brain")
    prices = get_market()
    results = run_ai(prices)

    rows = []
    for currency, data in results.items():
        rows.append({
            "Currency": currency,
            "Signal": data["signal"],
            "Confidence %": data["confidence"],
            "RSI": data["rsi"],
            "Forecast": data["forecast"]
        })
    ai_df = pd.DataFrame(rows)
    st.dataframe(ai_df, hide_index=True, use_container_width=True)

    for item in rows:
        if item["Signal"] == "BUY":
            st.success(f"🟢 BUY {item['Currency']} | Confidence {item['Confidence %']}%")
        elif item["Signal"] == "SELL":
            st.error(f"🔴 SELL {item['Currency']} | Confidence {item['Confidence %']}%")

# ---------------------------------------------------------
# FORECAST TAB
# ---------------------------------------------------------
with tabs[2]:
    st.subheader("🔮 AI Forecast Engine")
    currency = st.selectbox("Currency", list(CURRENCIES.keys()))
    days = st.slider("Days", 1, 30, 7)
    prediction = forecast_currency(currency, days)

    forecast_df = pd.DataFrame({"Day": range(1, days+1), "Forecast": prediction})
    st.line_chart(forecast_df.set_index("Day"))
    st.dataframe(forecast_df, hide_index=True)

# ---------------------------------------------------------
# TRADING TAB
# ---------------------------------------------------------
with tabs[3]:
    st.subheader("💹 Manual Trading")
    symbol = st.selectbox("Currency", list(CURRENCIES.keys()), key="trade_sym")
    action = st.radio("Action", ["BUY", "SELL"])
    price = get_market()[symbol]
    st.metric("Current Price", price)

    if st.button("Execute AI Trade"):
        pnl = execute_trade(symbol, action, price)
        st.success(f"Trade completed | PnL ${pnl:.2f}")

# ---------------------------------------------------------
# HISTORY TAB
# ---------------------------------------------------------
with tabs[4]:
    st.subheader("📜 Trade History")
    history = get_trade_history()
    st.dataframe(history, hide_index=True, use_container_width=True)

    if not history.empty:
        st.metric("Total Trades", len(history))
        st.metric("Total PnL", f"${history['pnl'].sum():.2f}")

# ---------------------------------------------------------
# AI MEMORY TAB
# ---------------------------------------------------------
with tabs[5]:
    st.subheader("🧬 AI Memory Database")
    memory = load_ai_memory()
    st.dataframe(memory, hide_index=True, use_container_width=True)

# ---------------------------------------------------------
# SYSTEM TAB
# ---------------------------------------------------------
with tabs[6]:
    st.subheader("⚙ System Diagnostics")
    st.json(system_status())

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.caption("SAI AI Forex Intelligence v6.0 | Autonomous Trading Simulation")