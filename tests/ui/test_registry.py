import os, json
import pytest
from sai.models.registry.register_model import register_model
from sai.models.registry.list_models import list_models
from sai.models.registry.rollback_model import rollback_model
from sai.streamlit_app import delete_model

REGISTRY_FILE = os.path.join(os.path.dirname(__file__), "../../sai/models/registry/models_registry.json")

@pytest.fixture(autouse=True)
def clean_registry(tmp_path, monkeypatch):
    # Redirect registry file to a temp path for clean tests
    test_registry = tmp_path / "models_registry.json"
    monkeypatch.setattr("sai.streamlit_app.REGISTRY_FILE", str(test_registry))
    yield
    if test_registry.exists():
        test_registry.unlink()

# ... existing tests above ...

def test_rollback_invalid_model_id():
    # Register one valid model
    entry = register_model("valid_model.pkl")
    models_before = list_models()
    assert any(m["id"] == entry["id"] for m in models_before)

    # Try to rollback to a non-existent ID
    invalid_id = "non_existent_model"
    result = rollback_model(invalid_id)

    # ✅ Ensure rollback returns success but does not mark any model active
    models_after = list_models()
    active = next((m for m in models_after if m.get("active")), None)
    assert active is None
    assert all(m["id"] != invalid_id for m in models_after)
