import streamlit as st
from streamlit.testing import TestSession

def test_dashboard_loads():
    session = TestSession()
    session.run_app("app.py")
    assert "Dashboard" in session.get_page_titles()
