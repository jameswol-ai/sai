def register_model(model_path: str):
    """
    Minimal stub for registering a model.
    Replace with MLflow or custom registry logic.
    """
    print(f"[Registry] Registered model from {model_path}")
    return {"status": "success", "model_path": model_path}
