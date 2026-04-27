"""
Tests for strategy configuration files.

Focus:
- Schema validation (required fields, types)
- Default values and ranges
- Dry-run loading into Strategy class
"""

import pytest
import yaml
from pathlib import Path
from bot.strategy import Strategy

CONFIG_PATH = Path("configs/strategies/example_strategy.yaml")

@pytest.fixture
def strategy_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def test_config_has_required_fields(strategy_config):
    required = ["name", "params"]
    for field in required:
        assert field in strategy_config, f"Missing required field: {field}"

def test_params_have_valid_types(strategy_config):
    params = strategy_config["params"]
    assert isinstance(params, dict)
    assert "window" in params
    assert isinstance(params["window"], int)
    assert params["window"] > 0

def test_strategy_can_initialize(strategy_config):
    s = Strategy(name=strategy_config["name"], params=strategy_config["params"])
    assert s.name == strategy_config["name"]
    assert s.params == strategy_config["params"]

def test_invalid_window_raises_error(strategy_config):
    bad_config = dict(strategy_config)
    bad_config["params"]["window"] = -10
    with pytest.raises(ValueError):
        Strategy(name=bad_config["name"], params=bad_config["params"])
