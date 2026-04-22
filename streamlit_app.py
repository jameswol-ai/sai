# sai/streamlit_app.py 

import streamlit as st

from sai.core.engine import WorkflowEngine
from sai.stages.sample_stages import (
    ingest_stage,
    analysis_stage,
    decision_stage,
    execution_stage,
)

# Define workflow
workflow = {
    "trading_pipeline": [
        {"name": "ingest", "function": ingest_stage},
        {"name": "analysis", "function": analysis_stage},
        {"name": "decision", "function": decision_stage},
        {"name": "execution", "function": execution_stage},
    ]
}

# UI
st.title("📈 SAI Trading Bot Workflow")

user_input = st.text_input("Enter market symbol or dataset path:")

if st.button("Run Trading Workflow"):
    engine = WorkflowEngine(workflow)
    engine.set_context("input", user_input)

    results = engine.run_workflow("trading_pipeline")

    st.subheader("Workflow Results:")
    for r in results:
        st.write(f"Stage: {r['stage']} → Output: {r['output']}")
