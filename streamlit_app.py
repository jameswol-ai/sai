# sai/streamlit_app.py 

import streamlit as st
from sai.core.engine import WorkflowEngine

# Dummy strategy for testing
class DummyStrategy:
    def evaluate(self, market_data):
        return "buy" if market_data.get("price", 0) > 50 else "sell"

# Dummy risk module
class DummyRisk:
    def apply(self, decision, market_data):
        if decision == "buy" and market_data.get("price", 0) > 100:
            return "hold"
        return decision

st.title("SAI Trading Bot Dashboard")

engine = WorkflowEngine(
    strategies=[DummyStrategy()],
    risk_modules=[DummyRisk()]
)

market_data = {"price": 120, "history": [95, 97, 99, 100]}
decision = engine.run(market_data)

st.write("Decision:", decision)
