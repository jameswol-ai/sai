# tests/test_data.py

import pytest
import pandas as pd
from bot.data import get_data

def test_get_data_returns_dataframe():
    df = get_data()
    assert isinstance(df, pd.DataFrame)

def test_dataframe_has_expected_columns():
    df = get_data()
    expected_cols = {"open", "high", "low", "close", "volume"}
    assert expected_cols.issubset(df.columns)

def test_no_missing_values():
    df = get_data()
    assert df.isnull().sum().sum() == 0
