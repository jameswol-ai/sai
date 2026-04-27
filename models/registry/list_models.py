def list_models():
    """
    Minimal stub for listing models.
    Replace with MLflow or DB query logic.
    """
    models = [
        {"id": "model_v1", "path": "models/model_v1.pkl"},
        {"id": "model_v2", "path": "models/model_v2.pkl"}
    ]
    print("[Registry] Listing models")
    return models
