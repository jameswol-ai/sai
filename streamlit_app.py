import streamlit as st
import threading
import logging
from plugins import risk_plugins, notifier_plugins, strategy_plugins

# Configure logging
logging.basicConfig(filename="trading_logs.log", level=logging.INFO)

def render_dashboard():
    st.title("Dashboard")
    st.write("Live trading loop, charts, and metrics here.")
    # Example threaded loop
    if "trading_thread" not in st.session_state:
        st.session_state.trading_thread = threading.Thread(target=run_trading_loop, daemon=True)
        st.session_state.trading_thread.start()

def run_trading_loop():
    while True:
        # Replace with trading logic
        logging.info("Trade executed")
        # Update charts/metrics here

def render_strategy_config():
    st.title("Strategy Config")
    st.write("Configure strategy parameters here.")

def render_logs():
    st.title("Logs")
    with open("trading_logs.log") as f:
        st.text(f.read())

def render_model_testing():
    st.title("Model Testing")
    st.write("Backtest and model evaluation here.")

def render_plugins_tab():
    st.title("Plugin Control Center")

    # Risk Management Plugins
    st.header("Risk Management")
    for plugin in risk_plugins:
        enabled = st.checkbox(f"Enable {plugin.name}", value=plugin.enabled, key=f"{plugin.name}_enabled")
        param = st.slider(
            f"{plugin.name} threshold",
            plugin.min_val,
            plugin.max_val,
            plugin.default,
            key=f"{plugin.name}_param"
        )
        plugin.update(enabled=enabled, param=param)

    # Strategy Switcher
    st.header("Strategy")
    strategy_choice = st.selectbox("Select Strategy", [s.name for s in strategy_plugins], key="strategy_choice")
    strategy_plugins[strategy_choice].activate()

    # Notifier Controls
    st.header("Notifications")
    for notifier in notifier_plugins:
        active = st.checkbox(f"Enable {notifier.name}", value=notifier.active, key=f"{notifier.name}_active")
        if st.button(f"Test {notifier.name}", key=f"{notifier.name}_test"):
            notifier.test_ping()
        notifier.update(active=active)

    # Audit Log
    st.header("Audit Log")
    st.write("Recent plugin actions and parameter changes will appear here.")

def main():
    st.sidebar.title("SAI Cockpit")
    tab = st.sidebar.radio("Navigate", ["Dashboard", "Strategy Config", "Logs", "Model Testing", "Plugins"])

    if tab == "Dashboard":
        render_dashboard()
    elif tab == "Strategy Config":
        render_strategy_config()
    elif tab == "Logs":
        render_logs()
    elif tab == "Model Testing":
        render_model_testing()
    elif tab == "Plugins":
        render_plugins_tab()

if __name__ == "__main__":
    main()
