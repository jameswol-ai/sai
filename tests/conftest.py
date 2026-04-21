# tests/conftest.py
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def sample_data():
    """Fixture for sample trading data."""
    import pandas as pd
    data = {
        'open': [100, 101, 102],
        'high': [105, 106, 107],
        'low': [95, 96, 97],
        'close': [102, 103, 104],
        'volume': [1000, 1100, 1200]
    }
    return pd.DataFrame(data)

@pytest.fixture
def mock_model():
    """Fixture for a mock ML model."""
    model = MagicMock()
    model.predict.return_value = [1, 0, 1]  # Sample predictions
    return model
