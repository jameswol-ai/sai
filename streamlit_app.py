import streamlit as st
import threading, time, logging, subprocess, json, os, pickle, random
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from prometheus_client import Gauge, Counter, start_http_server

--- Registry imports ---
from sai.models.registry.register_model import register_model
from sai.models.registry.list_models import list_models
from sai.models.registry.rollback_model import rollback_model

--- Logging Setup ---
logging.basicConfig(filename="sai_app.log", level=logging.INFO,
format="%(asctime)s [%(levelname)s] %(message)s")

--- TradingBot Stub ---
class TradingBot:
def init(self):
self.risk = 0.5
self.model = None
def decide(self, price):
return "BUY" if price % 2 == 0 else "SELL"

--- Model Helpers ---
def load_model(path):
with open(path, "rb") as f:
return pickle.load(f)

def save_model(model, path):
with open(path, "wb") as f:
pickle.dump(model, f)

--- Session State Init ---
if "bot" not in st.session_state:
st.session_state.bot = TradingBot()
if "running" not in st.session_state:
st.session_state.running = False
if "trades" not in st.session_state:
st.session_state.trades = []
if "prices" not in st.session_state:
st.session_state.prices = pd.DataFrame()
if "trade_log" not in st.session_state:
st.session_state.trade_log = []
if "pnl" not in st.session_state:
st.session_state.pnl = 0.0
if "wins" not in st.session_state:
st.session_state.wins = 0
if "losses" not in st.session_state:
st.session_state.losses = 0
if "peak_equity" not in st.session_state:
st.session_state.peak_equity = 0.0

--- Prometheus Metrics ---
trade_counter = Counter("sai_trades_total", "Total number of trades executed")
pnl_gauge = Gauge("sai_pnl", "Current profit and loss")
price_gauge = Gauge("sai_price", "Latest market price")
start_http_server(8000)

--- Trading Loop ---
def trading_loop():
while not st.session_state.get("stop_trading", False):
price = get_latest_price()
model = st.session_state.get("active_model", None)

if model:
prediction = model.predict([[price]]) # adjust input shape
outcome = 1 if prediction[0] > price else -1
else:
prediction = [price]
outcome = 0

st.session_state.pnl += outcome
if outcome > 0:
st.session_state.wins += 1
elif outcome < 0:
st.session_state.losses += 1
st.session_state.peak_equity = max(st.session_state.peak_equity, st.session_state.pnl)

st.session_state.trade_log.append({"price": price, "prediction": prediction[0]})
logging.info(f"Trade executed: price={price}, prediction={prediction[0]}, outcome={outcome}")

# Prometheus metrics update
trade_counter.inc()
pnl_gauge.set(st.session_state.pnl)
price_gauge.set(price)

time.sleep(2)

def get_latest_price():
return random.uniform(90, 110)

--- Streamlit Layout ---
st.set_page_config(page_title="SAI Trading Bot", layout="wide")
tabs = st.tabs(["📊 Dashboard", "⚙️ Strategy Config", "📝 Logs", "🧪 Model Testing",
"📚 Model Registry", "📈 Monitoring", "🧪 UI Tests", "🚀 CI/CD", "🐞 Debug"])

--- Dashboard ---
with tabs[0]:
st.header("Live Trading Dashboard")
if st.session_state.running:
st.success("Bot is running…")
else:
st.warning("Bot is stopped.")

if st.button("Start Bot"):
st.session_state.running = True
st.session_state.stop_trading = False
st.session_state.trading_thread = threading.Thread(target=trading_loop, daemon=True)
st.session_state.trading_thread.start()
st.success("Trading loop started.")

if st.button("Stop Bot"):
st.session_state.running = False
st.session_state.stop_trading = True
st.info("Trading loop stopped.")

if st.session_state.trade_log:
df = pd.DataFrame(st.session_state.trade_log)
st.line_chart(df[["price", "prediction"]])

st.subheader("📈 Performance Metrics")
total_trades = st.session_state.wins + st.session_state.losses
win_rate = (st.session_state.wins / total_trades * 100) if total_trades > 0 else 0
drawdown = st.session_state.peak_equity - st.session_state.pnl if st.session_state.pnl < st.session_state.peak_equity else 0.0

col1, col2, col3, col4 = st.columns(4)
col1.metric("PnL", f"{st.session_state.pnl:.2f}")
col2.metric("Win Rate", f"{win_rate:.1f}%")
col3.metric("Drawdown", f"{drawdown:.2f}")
col4.metric("Trades", str(total_trades))

--- Strategy Config ---
with tabs[1]:
st.header("Strategy Configuration")
risk = st.slider("Risk Level", 0.0, 1.0, st.session_state.bot.risk)
st.session_state.bot.risk = risk
st.write("Current risk:", risk)

--- Logs ---
with tabs[2]:
st.header("Application Logs")
if os.path.exists("sai_app.log"):
with open("sai_app.log") as f:
st.text_area("Logs", f.read(), height=400)
else:
st.info("No logs yet.")

--- Model Testing ---
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
else:
st.warning("No models registered. Defaulting to model.pkl")
selected_model_path = "model.pkl"

uploaded = st.file_uploader("Upload CSV dataset", type="csv")
if uploaded:
df = pd.read_csv(uploaded)
model = load_model(selected_model_path)
preds = model.predict(df.drop("target", axis=1))
st.line_chart(preds)

if st.button("Save Current Model"):
save_model(st.session_state.bot.model, "model.pkl")
st.success("Model saved and ready for registration.")

--- Model Registry (Enhanced) ---
REGISTRY_FILE = os.path.join(os.path.dirname(file), "../models/registry/models_registry.json")
AUDIT_FILE = os.path.join(os.path.dirname(file), "../models/registry/audit_log.json")

def log_action(action: str, model_id: str = None):
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

with tabs[4]:
st.header("📚 Model Registry")
models = list_models()
if models:
total_models = len(models)
active_models = [m for m in models if m.get("active")]
active_count = len(active_models)
inactive_count = total_models - active_count
last_registered = max((m.get("registered_at") for m in models if m.get("registered_at")), default="N/A")

st.subheader("📊 Registry Stats")
st.markdown(f"- Total Models: {total_models}")
st.markdown(f"- Active Models: {active_count}")
st.markdown(f"- Last Registered At: {last_registered}")

chart_data = pd.DataFrame({"Status": ["Active", "Inactive"], "Count": [active_count, inactive_count]})
st.bar_chart(chart_data.set_index("Status"))

st.table(models)

active_id = st.selectbox("Select a model to set active", options=[m["id"] for m in models])
if st.button("Set Active Model"):
rollback_model(active_id)
log_action("activate", active
