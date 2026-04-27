# sai/streamlit_app.py

import streamlit as st
import threading, time, logging, subprocess, json
import pandas as pd
import matplotlib.pyplot as plt

from sai.models.registry.register_model import register_model
from sai.models.registry.list_models import list_models
from sai.models.registry.rollback_model import rollback_model

# --- Logging Setup ---
logging.basicConfig(filename="sai_app.log", level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

# --- Session State ---
if "bot" not in st.session_state:
    st.session_state.bot = TradingBot()
if "running" not in st.session_state:
    st.session_state.running = False
if "trades" not in st.session_state:
    st.session_state.trades = []
if "prices" not in st.session_state:
    st.session_state.prices = pd.DataFrame()

# --- Trading Loop ---
def run_trading_loop():
    while st.session_state.running:
        price = 100 + (time.time() % 10)  # dummy price
        action = st.session_state.bot.decide(price)
        trade = {"time": time.time(), "price": price, "action": action, "pnl": (1 if action=="BUY" else -1)}
        st.session_state.trades.append(trade)
        st.session_state.prices = pd.concat([st.session_state.prices,
                                             pd.DataFrame([{"time": trade["time"], "price": price}])])
        logging.info(f"Trade executed: {trade}")
        time.sleep(2)

# --- Tabs ---
st.set_page_config(page_title="SAI Trading Bot", layout="wide")
tabs = st.tabs(["📊 Dashboard", "⚙️ Strategy Config", "📝 Logs", "🧪 Model Testing",
                "📚 Model Registry", "📈 Monitoring", "🧪 UI Tests", "🚀 CI/CD", "🐞 Debug"])

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
    risk = st.slider("Risk Level", 0.0, 1.0, st.session_state.bot.risk)
    st.session_state.bot.risk = risk
    st.write("Current risk:", risk)

# --- Logs ---
with tabs[2]:
    st.header("Application Logs")
    with open("sai_app.log") as f:
        st.text_area("Logs", f.read(), height=400)

# --- Model Testing ---
from sai.models.registry.list_models import list_models
from sai.models.registry.rollback_model import rollback_model

with tabs[3]:
    st.header("Model Testing")

    # Load all models from registry
    models = list_models()
    model_options = [m["id"] for m in models] if models else []
    active_model = next((m for m in models if m.get("active")), None)

    # Dropdown for model selection
    selected_model_id = st.selectbox(
        "Select a model to test",
        options=model_options,
        index=model_options.index(active_model["id"]) if active_model else 0
    ) if model_options else None

    if selected_model_id:
        selected_model_path = next(m["path"] for m in models if m["id"] == selected_model_id)
        st.success(f"Selected model: {selected_model_id} ({selected_model_path})")

        # Button to set selected model as active
        if st.button("Set Active Model"):
            rollback_model(selected_model_id)
            st.success(f"Model {selected_model_id} is now active.")

    else:
        st.warning("No models registered. Defaulting to model.pkl")
        selected_model_path = "model.pkl"

    # Upload dataset and run predictions
    uploaded = st.file_uploader("Upload CSV dataset", type="csv")
    if uploaded:
        df = pd.read_csv(uploaded)
        model = load_model(selected_model_path)
        preds = model.predict(df.drop("target", axis=1))
        st.line_chart(preds)

    if st.button("Save Current Model"):
        save_model(st.session_state.bot.model, "model.pkl")
        st.success("Model saved and ready for registration.")

    # Upload dataset and run predictions
    uploaded = st.file_uploader("Upload CSV dataset", type="csv")
    if uploaded:
        df = pd.read_csv(uploaded)
        model = load_model(selected_model_path)
        preds = model.predict(df.drop("target", axis=1))
        st.line_chart(preds)

    if st.button("Save Current Model"):
        save_model(st.session_state.bot.model, "model.pkl")
        st.success("Model saved and ready for registration.")

# --- Model Testing ---
from sai.models.registry.list_models import list_models
from sai.models.registry.rollback_model import rollback_model

with tabs[3]:
    st.header("Model Testing")

    # Load all models from registry
    models = list_models()
    model_options = []
    active_model = next((m for m in models if m.get("active")), None)

    # Build dropdown options with checkmark for active model
    for m in models:
        label = f"{m['id']} ✅" if m.get("active") else m["id"]
        model_options.append(label)

    # Dropdown for model selection
    selected_label = st.selectbox(
        "Select a model to test",
        options=model_options,
        index=model_options.index(f"{active_model['id']} ✅") if active_model else 0
    ) if model_options else None

    # Resolve selected model path
    if selected_label:
        selected_id = selected_label.replace(" ✅", "")
        selected_model_path = next(m["path"] for m in models if m["id"] == selected_id)
        st.success(f"Selected model: {selected_id} ({selected_model_path})")

        # Button to set selected model as active
        if st.button("Set Active Model"):
            rollback_model(selected_id)
            st.success(f"Model {selected_id} is now active.")
    else:
        st.warning("No models registered. Defaulting to model.pkl")
        selected_model_path = "model.pkl"

    # Upload dataset and run predictions
    uploaded = st.file_uploader("Upload CSV dataset", type="csv")
    if uploaded:
        df = pd.read_csv(uploaded)
        model = load_model(selected_model_path)
        preds = model.predict(df.drop("target", axis=1))
        st.line_chart(preds)

    if st.button("Save Current Model"):
        save_model(st.session_state.bot.model, "model.pkl")
        st.success("Model saved and ready for registration.")
# --- Monitoring ---
with tabs[5]:
    st.header("Monitoring & Metrics")
    st.write("Prometheus scrape config: `monitoring/prometheus.yml`")
    st.write("Grafana dashboards: `monitoring/grafana/dashboards.json`")
    try:
        with open("monitoring/alerts/trading_alerts.yml") as f:
            st.text_area("Alerts Config", f.read(), height=200)
    except FileNotFoundError:
        st.warning("Alerts config not found.")

# --- UI Tests ---
with tabs[6]:
    st.header("UI Tests")
    if st.button("Run UI Tests"):
        result = subprocess.run(["pytest", "tests/ui"], capture_output=True, text=True)
        st.text_area("Test Results", result.stdout + result.stderr, height=300)

# --- CI/CD ---
with tabs[7]:
    st.header("CI/CD Status")
    st.write("GitHub Actions workflow: `ci_cd/github_actions/test_deploy.yml`")
    st.write("Dockerfile staging: `ci_cd/docker/Dockerfile.staging`")
    st.write("Kubernetes manifests: `ci_cd/k8s/deployment.yaml`, `service.yaml`, `probes.yaml`")

# --- Debug ---
with tabs[8]:
    st.header("Debug Tools")
    st.json(st.session_state)

from prometheus_client import Gauge, Counter, start_http_server

# Prometheus metrics
trade_counter = Counter("sai_trades_total", "Total number of trades executed")
pnl_gauge = Gauge("sai_pnl", "Current profit and loss")
price_gauge = Gauge("sai_price", "Latest market price")

# Start Prometheus exporter on port 8000
start_http_server(8000)

def run_trading_loop():
    while st.session_state.running:
        price = 100 + (time.time() % 10)  # dummy price
        action = st.session_state.bot.decide(price)
        trade = {"time": time.time(), "price": price, "action": action, "pnl": (1 if action=="BUY" else -1)}
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
