import streamlit as st
import threading
import time
import random
import logging
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- Local Imports ---
from monitoring.metrics import equity_gauge, drawdown_gauge, sharpe_gauge, tracker_gauge, start_metrics_server
from plugins.risk_controls.stop_loss import StopLossPlugin
from plugins.risk_controls.max_drawdown import MaxDrawdownPlugin
from plugins.risk_controls.position_size import PositionSizePlugin
from plugins.notifications.email_notifier import EmailNotifier

# --- Logging Setup ---
logging.basicConfig(
    filename="trading.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# --- Session State Defaults ---
def init_defaults():
    defaults = {
        "balance": 1000.0,
        "pnl": 0.0,
        "last_price": None,
        "last_action": None,
        "running": False,
        "prices": [],
        "trades": [],
        "alerts": [],
        "tracker_completion": 0,
        "risk_manager": None,
        "notifier": None
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

# --- Risk Manager Setup ---
def init_risk_manager():
    plugins = [
        StopLossPlugin(threshold=0.05),
        MaxDrawdownPlugin(max_drawdown=0.20),
        PositionSizePlugin(max_fraction=0.10)
    ]
    st.session_state.risk_manager = plugins

# --- Notifier Setup ---
def init_notifier():
    st.session_state.notifier = EmailNotifier()

# --- Trading Loop ---
def trading_loop(refresh):
    while st.session_state.running:
        price = round(random.uniform(90, 110), 2)
        action = random.choice(["BUY", "SELL", "HOLD"])
        pnl_change = random.uniform(-1, 1)

        trade = {"entry": price, "price": price, "size": 100, "action": action}
        balance = st.session_state.balance

        # Risk checks
        allowed = all(plugin.check(trade, balance) for plugin in st.session_state.risk_manager)
        if not allowed:
            st.session_state.alerts.append({"timestamp": pd.Timestamp.now(), "event": "Risk Block"})
            st.session_state.notifier.notify_pipeline("BLOCKED", "risk-check", "main")
            logging.warning("Trade blocked by Risk Manager")
        else:
            st.session_state.last_price = price
            st.session_state.last_action = action
            st.session_state.pnl += pnl_change
            st.session_state.balance += pnl_change
            st.session_state.prices.append(price)
            st.session_state.trades.append({
                "timestamp": pd.Timestamp.now(),
                "price": price,
                "action": action,
                "profit": pnl_change
            })

            equity_gauge.set(st.session_state.balance)
            drawdown_gauge.set(max(0, (1000 - st.session_state.balance) / 1000))
            sharpe_gauge.set(random.uniform(-1, 2))
            tracker_gauge.set(min(100, st.session_state.tracker_completion + random.uniform(0, 2)))

            logging.info(f"Price={price}, Action={action}, Balance={st.session_state.balance:.2f}, PnL={st.session_state.pnl:.2f}")

        time.sleep(refresh)

# --- Main App ---
def main():
    init_defaults()
    init_risk_manager()
    init_notifier()
    start_metrics_server(port=8000)

    st.title("SAI Trading Dashboard Cockpit")
    tabs = st.tabs([
        "📊 Dashboard", "🧠 Strategy", "📜 Logs", "🛠 Debug", "📈 Analytics", "📦 Registry", "🚨 Alerts"
    ])

    # (unchanged tab functions reused here)
    # dashboard_tab(), strategy_tab(), logs_tab(), debug_tab(), analytics_tab(), registry_tab(), alerts_tab()

if __name__ == "__main__":
    main()
