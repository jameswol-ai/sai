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

def test_register_and_delete_model():
    entry = register_model("dummy_model.pkl")
    models = list_models()
    assert any(m["id"] == entry["id"] for m in models)

    result = delete_model(entry["id"])
    assert result["status"] == "deleted"

    models_after = list_models()
    assert all(m["id"] != entry["id"] for m in models_after)

def test_set_active_and_delete_model():
    m1 = register_model("model1.pkl")
    m2 = register_model("model2.pkl")

    rollback_model(m1["id"])
    models = list_models()
    active = next((m for m in models if m.get("active")), None)
    assert active and active["id"] == m1["id"]

    delete_model(m1["id"])
    models_after = list_models()
    assert all(m["id"] != m1["id"] for m in models_after)

    # ✅ Verify no model remains active after deleting the active one
    active_after = next((m for m in models_after if m.get("active")), None)
    assert active_after is None
