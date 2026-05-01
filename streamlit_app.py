import streamlit as st
import threading
import time
import logging
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from prometheus_client import Gauge, start_http_server

# --- Setup logging ---
logging.basicConfig(filename="sai.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

# --- Prometheus metrics ---
trade_metric = Gauge("sai_trades_total", "Total trades executed", ["action"])
prediction_metric = Gauge("sai_last_prediction", "Last prediction value")
accuracy_metric = Gauge("sai_model_accuracy", "Model accuracy")

# Start Prometheus exporter on port 8000
start_http_server(8000)

# --- Session state init ---
if "running" not in st.session_state:
    st.session_state.running = False
if "model" not in st.session_state:
    try:
        with open("models/model.pkl", "rb") as f:
            st.session_state.model = pickle.load(f)
    except Exception:
        st.session_state.model = None

# --- Placeholder functions ---
def get_latest_features():
    # Replace with real market data fetch
    return pd.DataFrame([[0.5, 0.2]], columns=["feature1", "feature2"])

def execute_trade(action, features):
    logging.info(f"Trade executed: {action} with features {features.to_dict()}")
    trade_metric.labels(action=action).inc()

def update_dashboard():
    st.write("Dashboard updated with latest trades/metrics")

# --- Trading loop ---
def trading_loop():
    while st.session_state.running:
        features = get_latest_features()
        if st.session_state.model:
            prediction = st.session_state.model.predict(features)[0]
            prediction_metric.set(prediction)
            if prediction == 1:
                execute_trade("BUY", features)
            elif prediction == -1:
                execute_trade("SELL", features)
            else:
                logging.info("Hold position")
            st.session_state.last_prediction = prediction
        else:
            logging.warning("No model loaded")
        time.sleep(5)

# --- Streamlit UI ---
st.title("SAI Trading Bot")

tab_dashboard, tab_strategy, tab_logs, tab_model_testing, tab_debug = st.tabs(
    ["Dashboard", "Strategy Config", "Logs", "Model Testing", "Debug"]
)

# --- Dashboard Tab ---
with tab_dashboard:
    st.header("Live Dashboard")
    if st.button("Start Trading"):
        if not st.session_state.running:
            st.session_state.running = True
            threading.Thread(target=trading_loop, daemon=True).start()
    if st.button("Stop Trading"):
        st.session_state.running = False

    if "last_prediction" in st.session_state:
        st.metric("Last Prediction", st.session_state.last_prediction)

    # Grafana integration
    st.subheader("Grafana Metrics Overlay")
    grafana_url = "http://localhost:3000/d/your_dashboard_id/trading-performance"
    st.markdown(f"[Open Grafana Dashboard]({grafana_url})")
    st.components.v1.iframe(grafana_url, height=600)

# --- Strategy Config Tab ---
with tab_strategy:
    st.header("Strategy Configuration")
    st.text_input("Parameter A")
    st.text_input("Parameter B")
    st.button("Save Config")

# --- Logs Tab ---
with tab_logs:
    st.header("Logs")
    try:
        with open("sai.log") as f:
            st.text(f.read())
    except FileNotFoundError:
        st.write("No logs yet.")

# --- Model Testing Tab ---
with tab_model_testing:
    st.header("Model Testing")
    uploaded_file = st.file_uploader("Upload CSV for testing", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        if "target" in data.columns:
            X_test = data.drop("target", axis=1)
            y_test = data["target"]
            if st.session_state.model:
                predictions = st.session_state.model.predict(X_test)
                accuracy = st.session_state.model.score(X_test, y_test)
                accuracy_metric.set(accuracy)
                st.metric("Accuracy", f"{accuracy:.2f}")
                results = pd.DataFrame({"Prediction": predictions, "Actual": y_test})
                st.dataframe(results)

                cm = confusion_matrix(y_test, predictions)
                fig, ax = plt.subplots()
                sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
                st.pyplot(fig)

                if st.button("Promote Model to Active Trading"):
                    st.session_state.model = st.session_state.model
                    st.success("Model promoted to active trading.")
            else:
                st.warning("No model.pkl loaded.")
        else:
            st.error("CSV must contain a 'target' column.")

# --- Debug Tab ---
with tab_debug:
    st.header("Debug Tools")
    st.write("Session State:", st.session_state)
