# sai/streamlit_app.py

import streamlit as st
import traceback

# --------------------------------------------------
# 🎛 PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="SAI Trading Bot Dashboard", layout="wide")

st.title("🏗️ SAI Trading Bot Dashboard")
st.caption("Resilient Workflow Engine • Debug Mode Enabled")

# --------------------------------------------------
# 🔌 IMPORTS FROM SAI PACKAGE
# --------------------------------------------------
from sai.bot.main import run_bot, get_data, decide_action, SimpleModel

# --------------------------------------------------
# 🔍 DEBUG PANEL
# --------------------------------------------------
with st.expander("⚙️ System Debug Info", expanded=False):
    st.write("Streamlit app is running inside the `sai` package.")
    try:
        st.write("Test run_bot():", run_bot())
    except Exception as e:
        st.error("Import or execution error:")
        st.code(traceback.format_exc())

# --------------------------------------------------
# 📊 MAIN DASHBOARD
# --------------------------------------------------
def main():
    if st.sidebar.button("Run Bot"):
        action = run_bot()
        st.write("Bot Action:", action)

    if st.sidebar.button("Refresh Data"):
        data = get_data()
        st.write("Latest Data:", data)

    if st.sidebar.button("Decide Action"):
        data = get_data()
        action = decide_action(data)
        st.write("Bot Decision:", action)

    if st.sidebar.button("Test Model"):
        model = SimpleModel()
        sample_data = get_data()
        prediction = model.predict(sample_data)
        st.write("Model Prediction:", prediction)

if __name__ == "__main__":
    main()
