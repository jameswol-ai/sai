# sai/streamlit_app.py 

import streamlit as st
from sai.core.engine import WorkflowEngine
from sai.plugins.moving_average import MovingAverageStrategy
from sai.plugins.stop_loss import StopLoss

# Initialize engine with strategies and risk modules
engine = WorkflowEngine(
    strategies=[MovingAverageStrategy()],
    risk_modules=[StopLoss()]
)

st.title("SAI Trading Bot")

market_data = {"price": 100, "history": [95, 97, 99, 100]}
decision = engine.run(market_data)

st.write("Decision:", decision)
