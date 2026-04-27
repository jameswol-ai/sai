import json, os

REGISTRY_FILE = os.path.join(os.path.dirname(__file__), "models_registry.json")

def list_models():
    """List all registered models from the JSON registry file."""
    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE, "r") as f:
            registry = json.load(f)
    else:
        registry = []

    print("[Registry] Listing models")
    return registry
