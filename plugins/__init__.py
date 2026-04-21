"""
Plugins package for SAI trading bot.

This package contains modular plugin integrations such as:
- indicators (technical analysis tools)
- exchanges (API connectors for trading platforms)

Importing `plugins` will expose these subpackages for cleaner usage.
"""

# Expose subpackages for direct import
from . import indicators
from . import exchanges

__all__ = ["indicators", "exchanges"]
