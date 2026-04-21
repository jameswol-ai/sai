"""
tests package initializer.

This file makes the tests/ directory a proper Python package.
It can be used to:
- Expose common test utilities
- Configure test-wide settings
- Provide versioning or metadata
"""

# Optional: expose fixtures or helpers
from .conftest import *  # noqa: F401,F403

__version__ = "0.1.0"
__all__ = [
    "conftest",
]
