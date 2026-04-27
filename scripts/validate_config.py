# sai/scripts/validate_config.py

import sys
import yaml

REQUIRED_KEYS = {
    "broker": ["alpaca", "binance"],
    "symbols": list,
    "position_sizing": dict,
    "logging": dict,
}

def validate_config(path="sai/configs/config.yaml"):
    try:
        with open(path, "r") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Failed to load config: {e}")
        sys.exit(1)

    # Check required keys
    for key, expected in REQUIRED_KEYS.items():
        if key not in config:
            print(f"❌ Missing required key: {key}")
            sys.exit(1)
        if isinstance(expected, list) and config[key] not in expected:
            print(f"❌ Invalid value for {key}: {config[key]}")
            sys.exit(1)
        if isinstance(expected, type) and not isinstance(config[key], expected):
            print(f"❌ {key} must be of type {expected.__name__}")
            sys.exit(1)

    # Extra checks
    if "default_qty" not in config["position_sizing"]:
        print("❌ position_sizing must include default_qty")
        sys.exit(1)

    print("✅ Config validation passed")

if __name__ == "__main__":
    validate_config()
