# utils.py
import os
import json
import logging
from datetime import datetime
from typing import Any, Dict

# --- Logging Setup ---
def setup_logger(name: str, log_file: str = "logs/utils.log") -> logging.Logger:
    """Create and configure a logger."""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(log_file)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

# --- Config Loader ---
def load_config(path: str) -> Dict[str, Any]:
    """Load JSON or YAML config file."""
    if path.endswith(".json"):
        with open(path, "r") as f:
            return json.load(f)
    elif path.endswith(".yaml") or path.endswith(".yml"):
        import yaml
        with open(path, "r") as f:
            return yaml.safe_load(f)
    else:
        raise ValueError("Unsupported config format")

# --- Environment Variable Helper ---
def get_env_var(key: str, default: Any = None) -> Any:
    """Fetch environment variable safely."""
    return os.getenv(key, default)

# --- Timestamp Helper ---
def current_timestamp() -> str:
    """Return current timestamp as string."""
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

# --- Safe Division ---
def safe_divide(a: float, b: float) -> float:
    """Divide safely, return 0 if denominator is zero."""
    return a / b if b != 0 else 0.0
