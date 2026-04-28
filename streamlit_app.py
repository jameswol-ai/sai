# sai/streamlit_app.py

import streamlit as st
import threading, time, logging, subprocess, json, os, pickle, random
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from prometheus_client import Gauge, Counter, start_http_server

# --- Registry Imports ---
from sai.models.registry.register_model import register_model
from sai.models.registry.list_models import list_models
from sai.models.registry.rollback_model import rollback_model

# --- Logging Setup ---
logging.basicConfig(filename="sai_app.log", level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

# --- Session State ---
if "bot" not in st.session_state:
    st.session_state.bot = None  # placeholder for TradingBot
if "running" not in st.session_state:
    st.session_state.running = False
if "trades" not in st.session_state:
    st.session_state.trades = []
if "prices" not in st.session_state:
    st.session_state.prices = pd.DataFrame()

# --- Prometheus Metrics ---
trade_counter = Counter("sai_trades_total", "Total number of trades executed")
pnl_gauge = Gauge("sai_pnl", "Current profit and loss")
price_gauge = Gauge("sai_price", "Latest market price")
start_http_server(8000)

# --- Trading Loop ---
def run_trading_loop():
    while st.session_state.running:
        price = 100 + (time.time() % 10)  # dummy price
        action = st.session_state.bot.decide(price) if st.session_state.bot else "HOLD"
        trade = {"time": time.time(), "price": price, "action": action,
                 "pnl": (1 if action == "BUY" else -1)}
        st.session_state.trades.append(trade)
        st.session_state.prices = pd.concat([st.session_state.prices,
                                             pd.DataFrame([{"time": trade["time"], "price": price}])])
        logging.info(f"Trade executed: {trade}")

        # Prometheus metrics update
        trade_counter.inc()
        pnl = sum([t["pnl"] for t in st.session_state.trades])
        pnl_gauge.set(pnl)
        price_gauge.set(price)

        time.sleep(2)

# --- Tabs ---
st.set_page_config(page_title="SAI Trading Bot", layout="wide")
tabs = st.tabs([
    "📊 Dashboard", "⚙️ Strategy Config", "📝 Logs", "🧪 Model Testing",
    "📚 Model Registry", "📈 Monitoring", "🧪 UI Tests", "🚀 CI/CD",
    "🐞 Debug", "📂 WorkFile"
])

# --- Dashboard ---
with tabs[0]:
    st.header("Live Trading Dashboard")
    if st.session_state.running:
        st.success("Bot is running…")
    else:
        st.warning("Bot is stopped.")
    if st.button("Start Bot"):
        st.session_state.running = True
        threading.Thread(target=run_trading_loop, daemon=True).start()
    if st.button("Stop Bot"):
        st.session_state.running = False

    if not st.session_state.prices.empty:
        fig, ax = plt.subplots()
        ax.plot(st.session_state.prices["time"], st.session_state.prices["price"], label="Price")
        ax.legend()
        st.pyplot(fig)

    st.metric("Total Trades", len(st.session_state.trades))
    if st.session_state.trades:
        pnl = sum([t["pnl"] for t in st.session_state.trades])
        st.metric("PnL", f"{pnl:.2f}")

# --- Strategy Config ---
with tabs[1]:
    st.header("Strategy Configuration")
    risk = st.slider("Risk Level", 0.0, 1.0, 0.5)
    st.write("Current risk:", risk)

# --- Logs ---
with tabs[2]:
    st.header("Application Logs")
    try:
        with open("sai_app.log") as f:
            st.text_area("Logs", f.read(), height=400)
    except FileNotFoundError:
        st.warning("No logs yet.")

# --- Model Testing ---
with tabs[3]:
    st.header("Model Testing")
    models = list_models()
    model_options = [m["id"] for m in models] if models else []
    active_model = next((m for m in models if m.get("active")), None)
    selected_model_id = st.selectbox("Select a model to test", options=model_options) if model_options else None
    if selected_model_id:
        selected_model_path = next(m["path"] for m in models if m["id"] == selected_model_id)
        st.success(f"Selected model: {selected_model_id} ({selected_model_path})")
        if st.button("Set Active Model"):
            rollback_model(selected_model_id)
            st.success(f"Model {selected_model_id} is now active.")

# --- Model Registry ---
with tabs[4]:
    st.header("Model Registry")
    models = list_models()
    if models:
        st.table(models)
    else:
        st.warning("No models registered yet.")

# --- Monitoring ---
with tabs[5]:
    st.header("Monitoring & Metrics")
    st.write("Prometheus scrape config: monitoring/prometheus.yml")
    st.write("Grafana dashboards: monitoring/grafana/dashboards.json")

# --- UI Tests ---
with tabs[6]:
    st.header("UI Tests")
    if st.button("Run UI Tests"):
        result = subprocess.run(["pytest", "tests/ui"], capture_output=True, text=True)
        st.text_area("Test Results", result.stdout + result.stderr, height=300)

# --- CI/CD ---
with tabs[7]:
    st.header("CI/CD Status")
    st.write("GitHub Actions workflow: ci_cd/github_actions/test_deploy.yml")
    st.write("Dockerfile staging: ci_cd/docker/Dockerfile.staging")
    st.write("Kubernetes manifests: ci_cd/k8s/deployment.yaml, service.yaml, probes.yaml")

# --- Debug ---
with tabs[8]:
    st.header("Debug Tools")
    st.json(st.session_state)

# --- WorkFile ---
with tabs[9]:
    st.header("📂 WorkFile")
    st.write("Manage workflow notes, guides, and operational checklists here.")
    uploaded_file = st.file_uploader("Upload a WorkFile (Markdown or TXT)", type=["md", "txt"])
    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
        st.text_area("WorkFile Content", content, height=400)
        if st.button("Save WorkFile"):
            with open("workfile.md", "w") as f:
                f.write(content)
            st.success("WorkFile saved as workfile.md")

    try:
        with open("workfile.md") as f:
            st.subheader("Current WorkFile")
            st.text_area("WorkFile", f.read(), height=400)
    except FileNotFoundError:
        st.info("No WorkFile saved yet.")
