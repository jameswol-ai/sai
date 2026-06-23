#sai - Plugins Package
---------------------------------
This package contains modular plugin integrations for:
- Exchanges
- Indicators
- Strategies
- Broker APIs
- Notifications
- Market Data

Each submodule is designed to be self-contained and reusable.
"""

# Expose key submodules for clean imports
from . import exchanges
from . import indicators
from . import strategies
from . import broker_api
from . import notifications
from . import market_data

__all__ = [
    "exchanges",
    "indicators",
    "strategies",
    "broker_api",
    "notifications",
    "market_data",
]

# Optional: versioning for plugins package
__version__ = "0.1.0"

# plugins/__init__.py

# Only import modules that exist
from . import exchanges
from . import prediction

# If you don’t yet have strategies.py, comment this out:
# from . import strategies
