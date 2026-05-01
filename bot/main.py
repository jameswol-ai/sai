# sai/bot/main.py

from sai.core.engine import WorkflowEngine

def run_bot():
    engine = WorkflowEngine()
    return engine.run("sample bot data")

if __name__ == "__main__":
    print(run_bot())

tab = st.sidebar.radio("Navigation", 
                       ["Dashboard", "Strategy Config", "Logs", "Model Testing", "Debug", "Analytics"])

if tab == "Dashboard":
    dashboard_tab()
elif tab == "Strategy Config":
    strategy_config_tab()
elif tab == "Logs":
    logs_tab()
elif tab == "Model Testing":
    model_testing_tab()
elif tab == "Debug":
    debug_tab()
elif tab == "Analytics":
    analytics_tab()
