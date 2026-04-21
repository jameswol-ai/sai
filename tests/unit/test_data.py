"""
Unit tests for data module.

Covers:
- Data loading from CSV
- Handling missing values
- Type conversions
- Basic preprocessing
"""

import pytest
import pandas as pd
from bot.data import load_data, preprocess_data

@pytest.fixture
def sample_csv(tmp_path):
    file = tmp_path / "sample.csv"
    df = pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=5, freq="D"),
        "close": [100, 102, None, 105, 107],
        "volume": [1000, 1100, 1200, None, 1400],
    })
    df.to_csv(file, index=False)
    return file

def test_load_data_returns_dataframe(sample_csv):
    df = load_data(sample_csv)
    assert isinstance(df, pd.DataFrame)
    assert "close" in df.columns
    assert "volume" in df.columns

def test_preprocess_data_fills_missing_values(sample_csv):
    df = load_data(sample_csv)
    processed = preprocess_data(df)
    assert not processed.isnull().any().any()

def test_preprocess_data_types(sample_csv):
    df = load_data(sample_csv)
    processed = preprocess_data(df)
    assert pd.api.types.is_numeric_dtype(processed["close"])
    assert pd.api.types.is_numeric_dtype(processed["volume"])

def test_empty_file_returns_empty_dataframe(tmp_path):
    file = tmp_path / "empty.csv"
    pd.DataFrame().to_csv(file, index=False)
    df = load_data(file)
    assert df.empty
