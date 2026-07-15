import streamlit as st
import pandas as pd
import numpy as np
import time
import os
import subprocess

# Set up page configurations
st.set_page_config(
    page_title="Sai AI Trading Bot Control Center",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Sai AI Trading Bot Control Center")
st.write("A dashboard to monitor, configure, and execute your trading algorithms.")

# Sidebar for Configuration
st.sidebar.header("Configuration Settings")
api_key = st.sidebar.text_input("Exchange API Key", type="password")
api_secret = st.sidebar.text_input("Exchange Secret Key", type="password")
trading_pair = st.sidebar.selectbox("Trading Pair", ["BTC/USDT", "ETH/USDT", "SOL/USDT"])
timeframe = st.sidebar.selectbox("Timeframe", ["1m", "5m", "15m", "1h", "4h"])
risk_level = st.sidebar.slider("Risk Management (%)", 1.0, 10.0, 2.0)

# Main Dashboard Layout
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Current Balance", value="$1,245.50", delta="+3.2%")
with col2:
    st.metric(label="Open Positions", value="1", delta=None)
with col3:
    st.metric(label="Total Realized P&L", value="+$145.20", delta="11.6%")

# Market Data & Visualization Section
st.subheader("Market Trend Analysis")
# Generate dummy data for visualization (Replace this with real API data fetch from Sai's core modules)
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['Price', 'SMA_20', 'EMA_50']
)
st.line_chart(chart_data)

# Bot Execution Controller
st.subheader("Bot Execution")

if 'bot_process' not in st.session_state:
    st.session_state.bot_process = None

start_bot = st.button("Start AI Bot", type="primary")
stop_bot = st.button("Stop AI Bot")

# Replace 'main.py' with the actual entry-point script name in the repository
bot_entry_script = "main.py" 

if start_bot:
    if st.session_state.bot_process is None:
        st.write("Starting the bot process...")
        try:
            # Execute the core bot script in the background
            st.session_state.bot_process = subprocess.Popen(
                ["python", bot_entry_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            st.success("Sai AI Trading Bot is now running.")
        except Exception as e:
            st.error(f"Failed to start bot: {e}")
    else:
        st.warning("Bot is already running.")

if stop_bot:
    if st.session_state.bot_process is not None:
        st.session_state.bot_process.terminate()
        st.session_state.bot_process = None
        st.info("Sai AI Trading Bot has been stopped.")
    else:
        st.warning("No running bot process found.")

# Display Logs
st.subheader("System Logs")
log_placeholder = st.empty()
if st.session_state.bot_process is not None:
    # Read output lines dynamically
    output = st.session_state.bot_process.stdout.readline()
    if output:
        st.text(output.strip())
else:
    st.text("Bot offline. No live logs available.")
