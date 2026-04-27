# sai/streamlit_app.py 

# --------------------------------------------------
# 🔍 DEBUG PANEL
# --------------------------------------------------
with st.expander("⚙️ System Debug Info", expanded=False):
    st.write("📁 Base Dir:", BASE_DIR)

    for path in POSSIBLE_PATHS:
        exists = os.path.exists(path)
        st.write(f"{path} → {'✅ exists' if exists else '❌ missing'}")

    # --------------------------------------------------
    # 📖 How SAI Works
    # --------------------------------------------------
    st.markdown("""
    ### 🧠 SAI Trading Bot Workflow
    The **SAI engine** runs through a modular pipeline:
    1. **Data Ingestion** → Collects market data (prices, indicators, feeds).
    2. **Analysis** → Applies preprocessing, feature extraction, and ML models.
    3. **Decision Engine** → Chooses an action (buy, sell, hold) based on strategy rules.
    4. **Execution Layer** → Sends trades or logs simulated actions.
    5. **Monitoring & Logging** → Tracks performance, errors, and metrics in real time.

    **Key Components:**
    - `bot/main.py`: Core logic (run_bot, get_data, decide_action, SimpleModel).
    - `utils.py`: Logging, configuration, helper utilities.
    - `streamlit_app.py`: Dashboard interface for control and visualization.
    - `models/`: Serialized ML models (e.g., `model.pkl`).
    - `guides/`: Documentation for setup, strategies, risk, and deployment.

    This modular design ensures reproducibility, multi-environment support
    (Python CLI, Docker, Kubernetes, Termux, Streamlit), and production readiness.
    """)
