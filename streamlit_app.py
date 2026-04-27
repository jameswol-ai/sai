# sai/streamlit_app.py
import streamlit as st
import sys
import os
import traceback

# --------------------------------------------------
# 🧭 PATH FIX (handles Streamlit Cloud + local)
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

POSSIBLE_PATHS = [
    BASE_DIR,
    os.path.join(BASE_DIR, "src"),
    os.path.join(BASE_DIR, "src", "core"),
]

for path in POSSIBLE_PATHS:
    if path not in sys.path:
        sys.path.insert(0, path)

# --------------------------------------------------
# 🎛 PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="AI Trading Bot", layout="wide")

st.title("AI Trading Bot")
st.caption("Resilient Workflow Engine • Debug Mode Enabled")

# --------------------------------------------------
# 🔍 DEBUG PANEL
# --------------------------------------------------
with st.expander("⚙️ System Debug Info", expanded=False):
    st.write("📁 Base Dir:", BASE_DIR)

    for path in POSSIBLE_PATHS:
        exists = os.path.exists(path)
