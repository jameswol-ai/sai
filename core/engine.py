from sai.core.engine import WorkflowEngine

def run_bot():
    engine = WorkflowEngine()
    return engine.run("sample bot data")

if __name__ == "__main__":
    print(run_bot())
