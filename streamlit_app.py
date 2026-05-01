import streamlit as st
import threading
import time
import sai
import pandas as pd
import matplotlib.pyplot as plt
import pickle
from sai.core.engine import WorkflowEngine

# Initialize engine once
if "engine" not in st.session_state:
    st.session_state["engine"] = WorkflowEngine()
engine = st.session_state["engine"]

# --- Live Trading Loop ---
def trading_loop():
    while st.session_state.get("running", False):
        result = engine.run()
        st.session_state["last_result"] = result
        time.sleep(2)

def start_trading():
    if not st.session_state.get("running", False):
        st.session_state["running"] = True
        thread = threading.Thread(target=trading_loop, daemon=True)
        thread.start()

def stop_trading():
    st.session_state["running"] = False

# --- Dashboard Tab ---
def dashboard_tab():
    st.header("Dashboard")
    col1, col2 = st.columns(2)
    if col1.button("Start Live Trading"):
        start_trading()
    if col2.button("Stop Live Trading"):
        stop_trading()

    result = st.session_state.get("last_result")
    if result:
        st.metric("Decision", result["decision"])
        st.metric("Price", result["price"])
        st.metric("Balance", result["balance"])
        st.write("Positions:", result["positions"])

    if "history" not in st.session_state:
        st.session_state["history"] = []
    if result:
        st.session_state["history"].append(result)

# --- Strategy Config Tab ---
def strategy_config_tab():
    st.header("Strategy Config")
    buy_threshold = st.number_input("Buy threshold", value=engine.buy_threshold)
    sell_threshold = st.number_input("Sell threshold", value=engine.sell_threshold)
    if st.button("Update Strategy"):
        engine.set_thresholds(buy_threshold, sell_threshold)
        st.success(f"Updated thresholds: BUY<{buy_threshold}, SELL>{sell_threshold}")

# --- Logs Tab ---
def logs_tab():
    st.header("Logs")
    try:
        with open("workflow.log", "r") as f:
            logs = f.read()
        st.text_area("Workflow Logs", logs, height=300)
    except FileNotFoundError:
        st.warning("No logs yet. Run the workflow first.")

# --- Model Testing Tab ---
def model_testing_tab():
    st.header("Model Testing")
    st.write("Placeholder for ML model evaluation")

# --- Debug Tab ---
def debug_tab():
    st.header("Debug")
    st.json({
        "balance": engine.balance,
        "positions": engine.positions,
        "buy_threshold": engine.buy_threshold,
        "sell_threshold": engine.sell_threshold,
    })

# --- Analytics Tab ---
def analytics_tab():
    st.header("Analytics")
    if "history" not in st.session_state or not st.session_state["history"]:
        st.warning("No trading history yet. Run the bot first.")
        return
    df = pd.DataFrame(st.session_state["history"])
    st.subheader("Quick Metrics")
    total_trades = len(df)
    buys = (df["decision"] == "BUY").sum()
    sells = (df["decision"] == "SELL").sum()
    holds = (df["decision"] == "HOLD").sum()
    avg_price = df["price"].mean()
    win_rate = sells / total_trades if total_trades > 0 else 0
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Trades", total_trades)
    col2.metric("Buys / Sells / Holds", f"{buys}/{sells}/{holds}")
    col3.metric("Win Rate", f"{win_rate:.2%}")
    st.metric("Average Price", f"{avg_price:.2f}")
    # Charts
    fig, ax = plt.subplots()
    ax.plot(df.index, df["price"], marker="o", label="Price")
    st.pyplot(fig)
    fig2, ax2 = plt.subplots()
    ax2.plot(df.index, df["balance"], marker="o", color="green", label="Balance")
    st.pyplot(fig2)
    # CSV Export
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Trading History CSV", csv, "trading_history.csv", "text/csv")

# --- Model Registry Tab ---
def model_registry_tab():
    st.header("Model Registry")
    if "models" not in st.session_state:
        st.session_state["models"] = {}
    uploaded_file = st.file_uploader("Upload ML Model (.pkl)", type=["pkl"])
    if uploaded_file is not None:
        try:
            model = pickle.load(uploaded_file)
            st.session_state["models"][uploaded_file.name] = model
            st.success(f"Model '{uploaded_file.name}' added to registry")
        except Exception as e:
            st.error(f"Failed to load model: {e}")
    if st.session_state["models"]:
        active_model = st.selectbox("Select Active Model", list(st.session_state["models"].keys()))
        st.session_state["active_model"] = active_model
        st.info(f"Active model: {active_model}")

# --- Main App ---
def main():
    st.title("SAI Trading Bot")
    if "running" not in st.session_state:
        st.session_state["running"] = False
    if "last_result" not in st.session_state:
        st.session_state["last_result"] = None
    tab = st.sidebar.radio("Navigation",
        ["Dashboard", "Strategy Config", "Logs", "Model Testing", "Debug", "Analytics", "Model Registry"])
    if tab == "Dashboard": dashboard_tab()
    elif tab == "Strategy Config": strategy_config_tab()
    elif tab == "Logs": logs_tab()
    elif tab == "Model Testing": model_testing_tab()
    elif tab == "Debug": debug_tab()
    elif tab == "Analytics": analytics_tab()
    elif tab == "Model Registry": model_registry_tab()

if __name__ == "__main__":
    main()
