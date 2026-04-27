import json, os

REGISTRY_FILE = os.path.join(os.path.dirname(__file__), "models_registry.json")

def register_model(model_path: str):
    """Register a model by adding it to a JSON registry file."""
    entry = {"id": f"model_{int(os.path.getmtime(model_path))}", "path": model_path}
    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE, "r") as f:
            registry = json.load(f)
    else:
        registry = []

    registry.append(entry)
    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=2)

    print(f"[Registry] Registered model {entry['id']} at {model_path}")
    return entry
