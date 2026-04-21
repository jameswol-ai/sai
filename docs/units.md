# Units, Conversions, and Position Sizing

## Overview
This document explains how the SAI trading bot handles:
- Currency units
- Value conversions
- Position sizing
- Practical examples

---

## Currency Units
- **Base Currency**: The primary currency used for account balance (e.g., USD).
- **Quote Currency**: The currency used to price assets (e.g., BTC/USD → USD is the quote).
- **Supported Units**: USD, EUR, GBP, JPY, BTC, ETH (extendable via plugins).

---

## Conversions
Conversions are handled through a utility function (`utils/conversions.py`) that:
- Normalizes values across different currencies.
- Uses exchange rate feeds (from APIs or static configs).
- Ensures precision with `Decimal` for financial safety.

**Example:**
```python
from utils.conversions import convert

usd_value = convert(amount=100, from_unit="EUR", to_unit="USD")
