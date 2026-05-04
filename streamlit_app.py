import streamlit as st
import threading
import time
import csv
import os
import random
from datetime import datetime

from engine.core_loop import SaiCoreLoop

if st.button("Start Trading"):
    if "loop" not in st.session_state:
        st.session_state.loop = SaiCoreLoop(
            bot=st.session_state.bot,
            metrics=st.session_state.metrics,
            csv_exporter=st.session_state.csv_exporter,
            sleep_time=1.0
        )

    def ui_update(price, action, trade, metrics):
        st.session_state.last_price = price
        st.session_state.last_action = action
        st.session_state.last_trade = trade
        st.session_state.metrics_snapshot = metrics.snapshot()

    threading.Thread(
        target=st.session_state.loop.start,
        args=(ui_update,),
        daemon=True
    ).start()

# ---------------------------------------------------------
# Minimal TradingBot (self-contained)
# ---------------------------------------------------------
class TradingBot:
    def __init__(self):
        self.position = 0
        self.balance = 1000

    def get_price(self):
        return round(100 + random.uniform(-1, 1), 4)

    def step(self, price):
        action = random.choice(["BUY", "SELL", "HOLD"])
        trade = None

        if action == "BUY":
            self.position += 1
            self.balance -= price
            trade = price

        elif action == "SELL" and self.position > 0:
            self.position -= 1
            self.balance += price
            trade = price

        return action, trade


# ---------------------------------------------------------
# Metrics tracker
# ---------------------------------------------------------
class Metrics:
    def __init__(self):
        self.prices = []
        self.actions = []
        self.trades = []
        self.balance = 1000
        self.pnl = 0

    def update(self, price, action, trade, bot):
        self.prices.append(price)
        self.actions.append(action)
        self.trades.append(trade)
        self.balance = bot.balance
        self.pnl = bot.balance - 1000

    def snapshot(self):
        return {
            "last_price": self.prices[-1] if self.prices else None,
            "last_action": self.actions[-1] if self.actions else None,
            "balance": self.balance,
            "pnl": self.pnl,
        }


# ---------------------------------------------------------
# CSV Exporter
# ---------------------------------------------------------
class CSVExporter:
    def __init__(self, filename="trades.csv"):
        self.filename = filename
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "price", "action", "trade", "balance", "pnl"])

    def write_row(self, row):
        with open(self.filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                row["timestamp"],
                row["price"],
                row["action"],
                row["trade"],
                row["balance"],
                row["pnl"],
            ])


# ---------------------------------------------------------
# Core Loop (self-contained)
# ---------------------------------------------------------
class CoreLoop:
    def __init__(self, bot, metrics, csv_exporter, sleep_time=1.0):
        self.bot = bot
        self.metrics = metrics
        self.csv_exporter = csv_exporter
        self.sleep_time = sleep_time
        self.running = False

    def start(self, ui_callback=None):
        self.running = True

        while self.running:
            try:
                price = self.bot.get_price()
                action, trade = self.bot.step(price)

                self.metrics.update(price, action, trade, self.bot)

                self.csv_exporter.write_row({
                    "timestamp": datetime.utcnow().isoformat(),
                    "price": price,
                    "action": action,
                    "trade": trade,
                    "balance": self.metrics.balance,
                    "pnl": self.metrics.pnl,
                })

                if ui_callback:
                    ui_callback()

                time.sleep(self.sleep_time)

            except Exception as e:
                print("Loop error:", e)
                time.sleep(1)

    def stop(self):
        self.running = False


# ---------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------
st.set_page_config(page_title="SAI Trading Dashboard", layout="wide")

st.title("SAI Trading Dashboard (Standalone Version)")

if "bot" not in st.session_state:
    st.session_state.bot = TradingBot()

if "metrics" not in st.session_state:
    st.session_state.metrics = Metrics()

if "csv" not in st.session_state:
    st.session_state.csv = CSVExporter()

if "loop" not in st.session_state:
    st.session_state.loop = None


# ---------------------------------------------------------
# UI Callback
# ---------------------------------------------------------
def update_ui():
    snap = st.session_state.metrics.snapshot()
    st.session_state.last_price = snap["last_price"]
    st.session_state.last_action = snap["last_action"]
    st.session_state.balance = snap["balance"]
    st.session_state.pnl = snap["pnl"]


# ---------------------------------------------------------
# Controls
# ---------------------------------------------------------
col1, col2 = st.columns(2)

if col1.button("Start Trading"):
    if st.session_state.loop is None or not st.session_state.loop.running:
        st.session_state.loop = CoreLoop(
            st.session_state.bot,
            st.session_state.metrics,
            st.session_state.csv,
            sleep_time=1.0
        )
        threading.Thread(
            target=st.session_state.loop.start,
            args=(update_ui,),
            daemon=True
        ).start()

if col2.button("Stop Trading"):
    if st.session_state.loop:
        st.session_state.loop.stop()


# ---------------------------------------------------------
# Live Metrics Display
# ---------------------------------------------------------
st.subheader("Live Metrics")

st.metric("Last Price", st.session_state.get("last_price", "—"))
st.metric("Last Action", st.session_state.get("last_action", "—"))
st.metric("Balance", st.session_state.get("balance", "—"))
st.metric("PnL", st.session_state.get("pnl", "—"))

st.line_chart(st.session_state.metrics.prices)
