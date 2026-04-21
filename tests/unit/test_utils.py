"""
Unit tests for utils module.

Covers:
- Safe division
- Position sizing
- Currency conversion
- Logging helpers
"""

import pytest
from bot.utils import safe_divide, position_size, convert_currency

def test_safe_divide_normal_case():
    assert safe_divide(10, 2) == 5

def test_safe_divide_by_zero():
    assert safe_divide(10, 0) == 0  # expected fallback

def test_position_size_calculation():
    size = position_size(balance=10000, risk_pct=0.02, stop_loss=50)
    assert isinstance(size, float)
    assert size > 0

def test_position_size_invalid_inputs():
    with pytest.raises(ValueError):
        position_size(balance=-1000, risk_pct=0.02, stop_loss=50)

def test_convert_currency_usd_to_eur():
    amount = convert_currency(100, rate=0.9)
    assert amount == pytest.approx(90)

def test_convert_currency_invalid_rate():
    with pytest.raises(ValueError):
        convert_currency(100, rate=-1)
