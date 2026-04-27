# tests/test_config.py

import pytest
import yaml
import subprocess

CONFIG_PATH = "sai/configs/config.yaml"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def test_config_schema():
    config = load_config()

    # Required keys
    assert "broker" in config
    assert config["broker"] in ["alpaca", "binance"]

    assert "symbols" in config and isinstance(config["symbols"], list)
    assert len(config["symbols"]) > 0

    assert "position_sizing" in config and isinstance(config["position_sizing"], dict)
    assert "default_qty" in config["position_sizing"]

    assert "logging" in config and isinstance(config["logging"], dict)
    assert "file" in config["logging"]

def test_dry_run_execution():
    # Run bot in dry-run mode for a few iterations
    result = subprocess.run(
        ["python", "sai/bot/run_bot.py", "--dry-run"],
        capture_output=True,
        text=True,
        timeout=10
    )
    assert result.returncode == 0
    assert "dry-run" in result.stdout or "Result" in result.stdout
