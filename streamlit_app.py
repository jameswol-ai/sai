# sai/streamlit_app.py

import streamlit as st
import time
import pandas as pd
from bot.memory import TradeMemory
from bot.learning import StrategyLearner

# ─────────────────────────────
# INIT SAi CORE
# ─────────────────────────────
memory = TradeMemory()
learner = StrategyLearner()

st.set_page_config(page_title="SAi Evolution Dashboard", layout="wide")

st.title("🧠 SAi — Live Learning Dashboard")
st.caption("Watching intelligence evolve in real time")

# ─────────────────────────────
# LOAD DATA
# ─────────────────────────────
data = memory.load()

if not data:
    st.warning("No trades yet. SAi is waiting for experience...")
    st.stop()

df = pd.DataFrame(data)

# ─────────────────────────────
# SIDEBAR — SYSTEM STATE
# ─────────────────────────────
st.sidebar.header("⚙️ SAi State")

st.sidebar.metric("Total Trades", len(df))
st.sidebar.metric("Last PnL", df.iloc[-1]["pnl"])

win_rate = (df["pnl"] > 0).mean() * 100
st.sidebar.metric("Win Rate", f"{win_rate:.2f}%")

st.sidebar.markdown("### 🧠 Strategy Weights")
weights = learner.get_weights()
st.sidebar.json(weights)

# ─────────────────────────────
# MAIN VISUALIZATION
# ─────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Equity Evolution")
    df["cumulative_pnl"] = df["pnl"].cumsum()
    st.line_chart(df["cumulative_pnl"])

with col2:
    st.subheader("🎯 Trade Outcomes")
    st.bar_chart(df["pnl"])

# ─────────────────────────────
# SIGNAL EVOLUTION
# ─────────────────────────────
st.subheader("🔁 Signal Memory (How SAi is learning)")

if "signal_used" in df.columns:
    st.dataframe(df[["timestamp", "signal_used", "pnl"]].tail(20))

# ─────────────────────────────
# LIVE SIMULATION MODE
# ─────────────────────────────
st.subheader("⚡ Live Evolution Feed")

placeholder = st.empty()

for i in range(10):
    if len(df) > 0:
        latest = df.iloc[-1]

        placeholder.markdown(
            f"""
            ### 🧠 SAi Thinking…
            - Last action: `{latest.get('signal_used', 'N/A')}`
            - Outcome: `{latest['pnl']}`
            - Learning adjustment active: ✅
            """
        )

    time.sleep(1)

# ─────────────────────────────
# RAW MEMORY VIEW
# ─────────────────────────────
with st.expander("🧾 Raw Memory Log"):
    st.json(data)
