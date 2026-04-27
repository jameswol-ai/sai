import json, os

REGISTRY_FILE = os.path.join(os.path.dirname(__file__), "models_registry.json")

def rollback_model(model_id: str):
    """Rollback to a specific model ID by marking it as active in the registry."""
    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE, "r") as f:
            registry = json.load(f)
    else:
        registry = []

    for model in registry:
        model["active"] = (model["id"] == model_id)

    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=2)

    print(f"[Registry] Rolled back to {model_id}")
    return {"status": "success", "rolled_back_to": model_id}
