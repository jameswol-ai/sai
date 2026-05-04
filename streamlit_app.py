import streamlit as st
import threading
import time
import json

# ---------------------------------------------------------
# Imports from your SAI modules
# ---------------------------------------------------------
from sai.model.simple_model import SimpleModel
from sai.broker.simulated_broker import SimulatedBroker
from sai.core.metrics import RollingMetrics
from sai.core.performance import PerformanceSnapshot
from sai.core.equity_chart import EquityCurveASCII


# ---------------------------------------------------------
# Inline Trading Engine (no engine.py required)
# ---------------------------------------------------------
class InlineTradingEngine:
    def __init__(self):
        self.model = SimpleModel()
        self.broker = SimulatedBroker()
        self.metrics = RollingMetrics()
        self.snapshot = PerformanceSnapshot()
        self.chart = EquityCurveASCII()
        self.cycle = 0

    def run_cycle(self):
        self.cycle += 1

        price = self.broker.get_price()
        signal = self.model.predict(price)
        position, pnl, balance = self.broker.execute(signal)

        snap = self.snapshot.log(
            cycle=self.cycle,
            price=price,
            signal=signal,
            position=position,
            pnl=pnl,
            balance=balance
        )

        metrics = self.metrics.update(balance)
        chart = self.chart.update(balance)

        return snap, metrics, chart


# ---------------------------------------------------------
# Initialize Streamlit Session State
# ---------------------------------------------------------
def init_state():
    if "engine" not in st.session_state:
        st.session_state.engine = InlineTradingEngine()

    if "running" not in st.session_state:
        st.session_state.running = False

    if "logs" not in st.session_state:
        st.session_state.logs = []

    if "last_snapshot" not in st.session_state:
        st.session_state.last_snapshot = None

    if "last_metrics" not in st.session_state:
        st.session_state.last_metrics = None

    if "last_chart" not in st.session_state:
        st.session_state.last_chart = None


# ---------------------------------------------------------
# Background Trading Thread
# ---------------------------------------------------------
def trading_loop():
    while st.session_state.running:
        snap, metrics, chart = st.session_state.engine.run_cycle()

        st.session_state.last_snapshot = snap
        st.session_state.last_metrics = metrics
        st.session_state.last_chart = chart

        st.session_state.logs.append(
            f"[{snap['cycle']}] Price={snap['price']} "
            f"Signal={snap['signal']} PnL={snap['pnl']} "
            f"Bal={snap['balance']}"
        )

        time.sleep(0.5)


# ---------------------------------------------------------
# Dashboard Tab
# ---------------------------------------------------------
def dashboard_tab():
    st.header("📊 SAI Live Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Start Trading"):
            if not st.session_state.running:
                st.session_state.running = True
                threading.Thread(target=trading_loop, daemon=True).start()

        if st.button("Stop Trading"):
            st.session_state.running = False

    with col2:
        st.write("Status:", "🟢 Running" if st.session_state.running else "🔴 Stopped")

    st.subheader("Latest Snapshot")
    st.json(st.session_state.last_snapshot or {})

    st.subheader("Rolling Metrics")
    st.json(st.session_state.last_metrics or {})

    st.subheader("Equity Curve (ASCII)")
    st.code(st.session_state.last_chart or "(waiting…)")


# ---------------------------------------------------------
# Logs Tab
# ---------------------------------------------------------
def logs_tab():
    st.header("📜 Logs")
    st.text("\n".join(st.session_state.logs[-200:]))


# ---------------------------------------------------------
# Strategy Tab
# ---------------------------------------------------------
def strategy_tab():
    st.header("⚙ Strategy Config")
    st.write("This version uses SimpleModel(). Strategy plugin loader coming soon.")


# ---------------------------------------------------------
# Debug Tab
# ---------------------------------------------------------
def debug_tab():
    st.header("🛠 Debug")
    st.code(json.dumps(dict(st.session_state), indent=2))


# ---------------------------------------------------------
# Main App
# ---------------------------------------------------------
def main():
    st.set_page_config(page_title="SAI Trading Bot", layout="wide")
    init_state()

    tabs = st.tabs(["Dashboard", "Logs", "Strategy", "Debug"])

    with tabs[0]:
        dashboard_tab()
    with tabs[1]:
        logs_tab()
    with tabs[2]:
        strategy_tab()
    with tabs[3]:
        debug_tab()


if __name__ == "__main__":
    main()
