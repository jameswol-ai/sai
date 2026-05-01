# sai/streamlit_app.py

import streamlit as st
from sai.core.engine import WorkflowEngine

def main():
    st.title("SAI Trading Bot Dashboard")

    engine = WorkflowEngine()

    st.header("Run Workflow")
    user_input = st.text_input("Enter data for workflow:")

    if st.button("Run"):
        result = engine.run(user_input)
        st.write("Result:", result)

if __name__ == "__main__":
    main()
