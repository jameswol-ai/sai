# sai/streamlit_app.py

import os
import streamlit as st

from sai.core.engine import WorkflowEngine
from sai.stages.sample_stages import (
    ingest_stage,
    analysis_stage,
    decision_stage,
    execution_stage,
)

# Registry file path
REGISTRY_FILE = "sai/models/registry.json"

def ensure_registry_file():
    """Ensure the model registry file exists."""
    if not os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE, "w") as f:
            f.write("{}")

def load_registry():
    """Load the model registry JSON as a string."""
    ensure_registry_file()
    with open(REGISTRY_FILE, "r") as f:
        return f.read()

def save_registry(content: str):
    """Save content back to the registry file."""
    with open(REGISTRY_FILE, "w") as f:
        f.write(content)

# Define workflow
workflow = {
    "trading_pipeline": [
        {"name": "ingest", "function": ingest_stage},
        {"name": "analysis", "function": analysis_stage},
        {"name": "decision", "function": decision_stage},
        {"name": "execution", "function": execution_stage},
    ]
}

# Streamlit UI
st.title("📈 SAI Trading Bot Workflow")

user_input = st.text_input("Enter market symbol or dataset path:")

if st.button("Run Trading Workflow"):
    engine = WorkflowEngine(workflow)
    engine.set_context("input", user_input)

    results = engine.run_workflow("trading_pipeline")

    st.subheader("Workflow Results:")
    for r in results:
        if isinstance(r, dict) and "stage" in r and "output" in r:
            st.write(f"Stage: {r['stage']} → Output: {r['output']}")
        else:
            st.write(r)
