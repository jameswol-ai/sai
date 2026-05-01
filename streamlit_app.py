import streamlit as st
import logging

# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

st.title("SAI Trading Bot Dashboard")

# Try importing WorkflowEngine and run_bot safely
try:
    from sai.core.engine import WorkflowEngine
    from sai.bot.main import run_bot
except ModuleNotFoundError as e:
    st.error("Import error: Could not load WorkflowEngine or run_bot. "
             "Check that your repo has the correct structure and __init__.py files.")
    st.stop()

# Initialize engine once
if "engine" not in st.session_state:
    st.session_state.engine = WorkflowEngine()

# Tabs
tab_dashboard, tab_strategy, tab_logs = st.tabs(["Dashboard", "Strategy Config", "Logs"])

with tab_dashboard:
    st.header("Live Trading")
    if st.button("Run Workflow"):
        result = st.session_state.engine.run({"sample": "data"})
        st.write("Workflow result:", result)
        logging.info("Workflow run: %s", result)

    if st.button("Run Bot"):
        output = run_bot()
        st.write("Bot output:", output)
        logging.info("Bot run: %s", output)

with tab_strategy:
    st.header("Strategy Configuration")
    st.text_input("Parameter A", key="param_a")
    st.text_input("Parameter B", key="param_b")

with tab_logs:
    st.header("Logs")
    try:
        with open("app.log") as f:
            st.text(f.read())
    except FileNotFoundError:
        st.write("No logs yet.")
