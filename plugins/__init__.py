"""
Plugins package for SAI trading bot.

This package contains modular plugin integrations such as:
- indicators (technical analysis tools)
- exchanges (API connectors for trading platforms)
- notifications (alerting and messaging systems)

Importing `plugins` will expose these subpackages for cleaner usage.
"""

# Expose subpackages for direct import
from . import indicators
from . import exchanges
from . import notifications

__all__ = ["indicators", "exchanges", "notifications"]
