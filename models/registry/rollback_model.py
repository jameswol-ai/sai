def rollback_model(model_id: str):
    """
    Minimal stub for rolling back to a previous model.
    Replace with MLflow or custom rollback logic.
    """
    print(f"[Registry] Rolled back to {model_id}")
    return {"status": "success", "rolled_back_to": model_id}
