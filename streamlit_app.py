import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import time
import threading

# Initialize session state
if "trades" not in st.session_state:
    np.random.seed(42)
    st.session_state.trades = pd.DataFrame({
        "timestamp": pd.date_range("2026-01-01", periods=50, freq="h"),
        "pnl": np.random.normal(0, 50, 50),
        "trade_size": np.random.randint(1, 10, 50),
        "volatility": np.random.uniform(0.1, 2.0, 50),
        "model_accuracy": np.random.uniform(0.5, 1.0, 50)
    })

def stream_new_trade():
    while True:
        new_row = {
            "timestamp": pd.Timestamp.now(),
            "pnl": np.random.normal(0, 50),
            "trade_size": np.random.randint(1, 10),
            "volatility": np.random.uniform(0.1, 2.0),
            "model_accuracy": np.random.uniform(0.5, 1.0)
        }
        st.session_state.trades = pd.concat(
            [st.session_state.trades, pd.DataFrame([new_row])],
            ignore_index=True
        )
        time.sleep(5)  # simulate trade every 5 seconds

# Start background thread once
if "thread_started" not in st.session_state:
    threading.Thread(target=stream_new_trade, daemon=True).start()
    st.session_state.thread_started = True

st.title("📊 Advanced Visualizations Cockpit (Live)")

tab1, tab2, tab3, tab4 = st.tabs(["Heatmap", "Correlation", "Timeline", "PnL Trends"])

with tab1:
    st.subheader("Trade Outcome Heatmap")
    trades = st.session_state.trades.copy()
    trades["hour"] = trades["timestamp"].dt.hour
    trades["day"] = trades["timestamp"].dt.day
    heatmap_data = trades.pivot_table(values="pnl", index="day", columns="hour", aggfunc="mean")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(heatmap_data, cmap="RdYlGn", center=0, ax=ax)
    st.pyplot(fig)

with tab2:
    st.subheader("Correlation Matrix")
    corr = st.session_state.trades[["pnl", "trade_size", "volatility", "model_accuracy"]].corr()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

with tab3:
    st.subheader("Unified Timeline Overlay")
    fig = px.line(
        st.session_state.trades,
        x="timestamp",
        y=["pnl", "volatility", "model_accuracy"],
        labels={"value": "Metric Value", "timestamp": "Time"},
        title="Trades, Volatility & Model Accuracy Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("PnL & Trade Size Trends")
    fig = px.line(
        st.session_state.trades,
        x="timestamp",
        y=["pnl", "trade_size"],
        labels={"value": "Metric Value", "timestamp": "Time"},
        title="PnL & Trade Size Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)
