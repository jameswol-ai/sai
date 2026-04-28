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

# --- Model Registry ---
from sai.models.registry.register_model import register_model
from sai.models.registry.list_models import list_models
from sai.models.registry.rollback_model import rollback_model
import json, os
from datetime import datetime

REGISTRY_FILE = os.path.join(os.path.dirname(__file__), "../models/registry/models_registry.json")

def delete_model(model_id: str):
    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE, "r") as f:
            registry = json.load(f)
    else:
        registry = []
    registry = [m for m in registry if m["id"] != model_id]
    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=2)
    return {"status": "deleted", "model_id": model_id}

def clear_registry():
    with open(REGISTRY_FILE, "w") as f:
        json.dump([], f, indent=2)
    return {"status": "cleared"}

def register_model_with_timestamp(path: str):
    entry = register_model(path)
    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE, "r") as f:
            registry = json.load(f)
    else:
        registry = []
    for m in registry:
        if m["id"] == entry["id"]:
            m["registered_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=2)
    return entry

def rollback_model_with_timestamp(model_id: str):
    rollback_model(model_id)
    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE, "r") as f:
            registry = json.load(f)
    else:
        registry = []
    for m in registry:
        if m["id"] == model_id:
            m["last_active_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=2)

with tabs[4]:
    st.header("Model Registry")

    # --- Registry Stats ---
    models = list_models()
    if models:
        total_models = len(models)
        active_models = [m for m in models if m.get("active")]
        active_count = len(active_models)
        inactive_count = total_models - active_count
        last_registered = max(
            (m.get("registered_at") for m in models if m.get("registered_at")), 
            default="N/A"
        )

        st.subheader("📊 Registry Stats")
        st.markdown(f"- **Total Models:** {total_models}")
        st.markdown(f"- **Active Models:** {active_count}")
        st.markdown(f"- **Last Registered At:** {last_registered}")

        # ✅ Pie chart visualization
        chart_data = pd.DataFrame({
            "Status": ["Active", "Inactive"],
            "Count": [active_count, inactive_count]
        })
        st.subheader("Model Status Overview")
        st.bar_chart(chart_data.set_index("Status"))  # bar chart
        st.write("Or view as pie chart below:")
        st.pyplot(chart_data.plot.pie(y="Count", labels=chart_data["Status"], autopct='%1.0f%%').figure)

        st.subheader("📊 Registry Stats")
        st.markdown(f"- **Total Models:** {total_models}")
        st.markdown(f"- **Active Models:** {active_count}")
        st.markdown(f"- **Last Registered At:** {last_registered}")

    # Register current model
    if st.button("Register Current Model"):
        register_model_with_timestamp("model.pkl")
        st.success("Model registered.")
        st.experimental_rerun()

    if st.button("Refresh Registry"):
        st.experimental_rerun()

    if models:
        table_data = []
        for m in models:
            table_data.append({
                "Model ID": m["id"],
                "Path": m["path"],
                "Active": "✅" if m.get("active") else "",
                "Registered At": m.get("registered_at", "N/A"),
                "Last Active At": m.get("last_active_at", "N/A")
            })
        st.table(table_data)

        active_id = st.selectbox("Select a model to set active", options=[m["id"] for m in models])
        if st.button("Set Active Model"):
            rollback_model_with_timestamp(active_id)
            st.success(f"Model {active_id} is now active.")
            st.experimental_rerun()

        delete_id = st.selectbox("Select a model to delete", options=[m["id"] for m in models])
        if st.button("Delete Selected Model"):
            result = delete_model(delete_id)
            st.success(f"Model {delete_id} deleted from registry.")
            st.experimental_rerun()

        # Download registry JSON
        if os.path.exists(REGISTRY_FILE):
            with open(REGISTRY_FILE, "r") as f:
                registry_data = f.read()
            st.download_button(
                label="Download Registry JSON",
                data=registry_data,
                file_name="models_registry.json",
                mime="application/json"
            )

        # Upload registry JSON
        uploaded_file = st.file_uploader("Upload Registry JSON", type=["json"])
        if uploaded_file is not None:
            try:
                registry_data = json.load(uploaded_file)
                with open(REGISTRY_FILE, "w") as f:
                    json.dump(registry_data, f, indent=2)
                st.success("Registry restored from uploaded file.")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Failed to load registry: {e}")

        # Clear registry with confirmation
        if st.button("Clear Registry"):
            if st.checkbox("Confirm clear registry (this cannot be undone)"):
                clear_registry()
                st.success("Registry cleared.")
                st.experimental_rerun()
            else:
                st.warning("Please check the confirmation box before clearing the registry.")

    else:
        st.warning("No models registered yet.")

import pandas as pd

# --- Active Model History timeline ---
active_events = [(m["id"], m.get("last_active_at")) for m in models if m.get("last_active_at")]
if active_events:
    df_active = pd.DataFrame(active_events, columns=["Model ID", "Last Active At"])
    df_active["Last Active At"] = pd.to_datetime(df_active["Last Active At"])
    df_active = df_active.sort_values("Last Active At")

    st.subheader("🕒 Active Model History")

    # Filters
    model_filter = st.selectbox("Filter by Model ID", options=["All"] + list(df_active["Model ID"].unique()))
    start_date = st.date_input("Start Date", value=df_active["Last Active At"].min().date())
    end_date = st.date_input("End Date", value=df_active["Last Active At"].max().date())

    filtered = df_active.copy()
    if model_filter != "All":
        filtered = filtered[filtered["Model ID"] == model_filter]
    filtered = filtered[(filtered["Last Active At"].dt.date >= start_date) & 
                        (filtered["Last Active At"].dt.date <= end_date)]

    st.write("Timeline of when models were last promoted to active:")
    st.table(filtered)

    if not filtered.empty:
        filtered["Date"] = filtered["Last Active At"].dt.date
        active_trend = filtered.groupby("Date").size().reset_index(name="Activations")
        st.line_chart(active_trend.set_index("Date"))

        # Export filtered history
        st.download_button(
            label="Download Filtered History (CSV)",
            data=filtered.to_csv(index=False),
            file_name="active_model_history.csv",
            mime="text/csv"
        )
        st.download_button(
            label="Download Filtered History (JSON)",
            data=filtered.to_json(orient="records", indent=2, date_format="iso"),
            file_name="active_model_history.json",
            mime="application/json"
        )

        # ✅ Replay promotion: roll back to any previously active model
        replay_id = st.selectbox("Replay activation: choose a model", options=filtered["Model ID"].unique())
        if st.button("Promote Selected Historical Model"):
            rollback_model_with_timestamp(replay_id)
            st.success(f"Model {replay_id} has been re‑promoted from history.")
            st.experimental_rerun()
    else:
        st.info("No activation events found for the selected filters.")      

import pandas as pd

# --- Compare Models ---
if models and len(models) > 1:
    st.subheader("🔍 Compare Models")

    # Select two models to compare
    model_a = st.selectbox("Select first model", options=[m["id"] for m in models], key="compare_a")
    model_b = st.selectbox("Select second model", options=[m["id"] for m in models], key="compare_b")

    if model_a and model_b and model_a != model_b:
        # Extract details
        details = {}
        for m in models:
            if m["id"] == model_a:
                details["A"] = {
                    "Model ID": m["id"],
                    "Path": m["path"],
                    "Active": "✅" if m.get("active") else "",
                    "Registered At": m.get("registered_at", "N/A"),
                    "Last Active At": m.get("last_active_at", "N/A")
                }
            if m["id"] == model_b:
                details["B"] = {
                    "Model ID": m["id"],
                    "Path": m["path"],
                    "Active": "✅" if m.get("active") else "",
                    "Registered At": m.get("registered_at", "N/A"),
                    "Last Active At": m.get("last_active_at", "N/A")
                }

        # ✅ Diff view: highlight differences only
        diffs = []
        for key in details["A"].keys():
            if details["A"][key] != details["B"][key]:
                diffs.append({
                    "Field": key,
                    f"{model_a}": details["A"][key],
                    f"{model_b}": details["B"][key]
                })

        if diffs:
            st.subheader("⚡ Differences Between Models")
            st.table(pd.DataFrame(diffs))
        else:
            st.info("No differences found — both models have identical metadata.")

        # ✅ Promote newer model shortcut
        try:
            reg_a = pd.to_datetime(details["A"]["Registered At"]) if details["A"]["Registered At"] != "N/A" else None
            reg_b = pd.to_datetime(details["B"]["Registered At"]) if details["B"]["Registered At"] != "N/A" else None
            act_a = pd.to_datetime(details["A"]["Last Active At"]) if details["A"]["Last Active At"] != "N/A" else None
            act_b = pd.to_datetime(details["B"]["Last Active At"]) if details["B"]["Last Active At"] != "N/A" else None

            # Decide which is newer (prefer activation timestamp, fallback to registration)
            newer_model = None
            if act_a and act_b:
                newer_model = model_a if act_a > act_b else model_b
            elif reg_a and reg_b:
                newer_model = model_a if reg_a > reg_b else model_b

            if newer_model:
                if st.button(f"Promote Newer Model ({newer_model})"):
                    rollback_model_with_timestamp(newer_model)
                    st.success(f"Model {newer_model} promoted to active (newer timestamp).")
                    st.experimental_rerun()
        except Exception as e:
            st.error(f"Could not determine newer model: {e}")
    else:
        st.info("Select two different models to compare.")

import json, os
from datetime import datetime

AUDIT_FILE = os.path.join(os.path.dirname(__file__), "../models/registry/audit_log.json")

def log_action(action: str, model_id: str = None):
    """Append an action with timestamp to the audit log."""
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "model_id": model_id if model_id else "N/A"
    }
    if os.path.exists(AUDIT_FILE):
        with open(AUDIT_FILE, "r") as f:
            log = json.load(f)
    else:
        log = []
    log.append(entry)
    with open(AUDIT_FILE, "w") as f:
        json.dump(log, f, indent=2)

# Wrap existing actions with logging
def register_model_with_timestamp(path: str):
    entry = register_model(path)
    log_action("register", entry["id"])
    ...
    return entry

def rollback_model_with_timestamp(model_id: str):
    rollback_model(model_id)
    log_action("activate", model_id)
    ...
    
def delete_model(model_id: str):
    ...
    log_action("delete", model_id)
    return {"status": "deleted", "model_id": model_id}

def clear_registry():
    ...
    log_action("clear")
    return {"status": "cleared"}

# Replay promotion
if st.button("Promote Selected Historical Model"):
    rollback_model_with_timestamp(replay_id)
    log_action("replay_activate", replay_id)
    st.success(f"Model {replay_id} has been re‑promoted from history.")
    st.experimental_rerun()

# --- Audit Log Section ---
if os.path.exists(AUDIT_FILE):
    with open(AUDIT_FILE, "r") as f:
        audit_data = json.load(f)
    st.subheader("📜 Audit Log")
    st.table(audit_data)

    # Export audit log
    st.download_button(
        label="Download Audit Log (JSON)",
        data=json.dumps(audit_data, indent=2),
        file_name="audit_log.json",
        mime="application/json"
    )
else:
    st.info("No audit log entries yet.")

import pandas as pd

# --- Audit Log Section ---
if os.path.exists(AUDIT_FILE):
    with open(AUDIT_FILE, "r") as f:
        audit_data = json.load(f)

    df_audit = pd.DataFrame(audit_data)
    df_audit["timestamp"] = pd.to_datetime(df_audit["timestamp"])

    st.subheader("📜 Audit Log")

    # Filters
    action_filter = st.selectbox("Filter by Action", options=["All"] + list(df_audit["action"].unique()))
    model_filter = st.selectbox("Filter by Model ID", options=["All"] + list(df_audit["model_id"].unique()))

    filtered_audit = df_audit.copy()
    if action_filter != "All":
        filtered_audit = filtered_audit[filtered_audit["action"] == action_filter]
    if model_filter != "All":
        filtered_audit = filtered_audit[filtered_audit["model_id"] == model_filter]

    st.table(filtered_audit)

    # Export filtered log
    if not filtered_audit.empty:
        st.download_button(
            label="Download Filtered Audit Log (CSV)",
            data=filtered_audit.to_csv(index=False),
            file_name="audit_log_filtered.csv",
            mime="text/csv"
        )
        st.download_button(
            label="Download Filtered Audit Log (JSON)",
            data=filtered_audit.to_json(orient="records", indent=2),
            file_name="audit_log_filtered.json",
            mime="application/json"
        )

        # ✅ Timeline visualization
        st.subheader("📈 Audit Timeline Visualization")
        timeline = filtered_audit.groupby(["timestamp", "action"]).size().reset_index(name="Count")
        st.line_chart(timeline.set_index("timestamp"))

        # Optional scatter plot for clarity
        st.write("Event scatter plot:")
        st.pyplot(
            filtered_audit.plot.scatter(x="timestamp", y="action", title="Audit Events Timeline").figure
        )
    else:
        st.info("No audit entries found for the selected filters.")
else:
    st.info("No audit log entries yet.")

