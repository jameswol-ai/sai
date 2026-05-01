# sai/core/engine.py

class WorkflowEngine:
    def __init__(self):
        self.counter = 0

    def run(self, data: dict):
        """
        Minimal workflow execution stub.
        Replace with trading workflow logic later.
        """
        self.counter += 1
        return {
            "status": "ok",
            "runs": self.counter,
            "input": data
        }
