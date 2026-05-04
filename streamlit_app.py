import streamlit as st
import pandas as pd
import time
import random
import logging
from datetime import datetime

# ---------------------------------------------------------
# Local Lightweight TradingBot Stub (No external imports)
# ---------------------------------------------------------
class TradingBot:
    def __init__(self):
        self.balance = 1000.0
        self.position = None
        self.trade_history = []
        self.last_price = None

    def get_price(self):
        # Simulated price feed
        price = round(100 + random.uniform(-1, 1), 4)
        self.last_price = price
        return price

    def decide(self, price):
        # Simple random strategy
        return random.choice(["BUY", "SELL", "HOLD"])

    def execute_trade(self, action, price):
        timestamp = datetime.utcnow().isoformat()

        if action == "BUY":
            self.position = price
            self.trade_history.append({"time": timestamp, "action": "BUY", "price": price})

        elif action == "SELL" and self.position is not None:
            pnl = price - self.position
            self.balance += pnl
            self.trade_history.append({"time": timestamp, "action": "SELL", "price": price, "pnl": pnl})
            self.position = None

        return True

# ---------------------------------------------------------
# Streamlit App
# ---------------------------------------------------------
def init_state():
    if "bot" not in st.session_state:
        st.session_state.bot = TradingBot()
    if "running" not in st.session_state:
        st.session_state.running = False
    if "logs" not in st.session_state:
        st.session_state.logs = []
    if "prices" not in st.session_state:
        st.session_state.prices = []

def log(msg):
    timestamp = datetime.utcnow().strftime("%H:%M:%S")
    st.session_state.logs.append(f"[{timestamp}] {msg}")

def run_trading_loop():
    bot = st.session_state.bot

    for _ in range(20):  # 20 cycles per click
        if not st.session_state.running:
            break

        price = bot.get_price()
        action = bot.decide(price)
        bot.execute_trade(action, price)

        st.session_state.prices.append(price)
        log(f"Price={price} | Action={action}")

        time.sleep(0.2)

# ---------------------------------------------------------
# UI Layout
# ---------------------------------------------------------
def dashboard_tab():
    st.header("📈 Live Trading Dashboard")

    col1, col2 = st.columns(2)
    col1.metric("Balance", f"${st.session_state.bot.balance:.2f}")
    col2.metric("Last Price", st.session_state.bot.last_price)

    if st.button("Start Trading"):
        st.session_state.running = True
        run_trading_loop()

    if st.button("Stop Trading"):
        st.session_state.running = False

    st.line_chart(st.session_state.prices)

def trades_tab():
    st.header("📜 Trade History")

    df = pd.DataFrame(st.session_state.bot.trade_history)
    if df.empty:
        st.info("No trades yet.")
    else:
        st.dataframe(df)

        csv = df.to_csv(index=False)
        st.download_button("Download CSV", csv, "trades.csv")

def logs_tab():
    st.header("🧾 Logs")
    st.text("\n".join(st.session_state.logs[-200:]))

# ---------------------------------------------------------
# Main App
# ---------------------------------------------------------
def main():
    st.set_page_config(page_title="SAI Trading Bot", layout="wide")
    init_state()

    tabs = st.tabs(["Dashboard", "Trades", "Logs"])

    with tabs[0]:
        dashboard_tab()

    with tabs[1]:
        trades_tab()

    with tabs[2]:
        logs_tab()

if __name__ == "__main__":
    main()
