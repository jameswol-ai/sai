# Examples

## Overview
This document provides practical examples of how to use the SAI trading bot modules, including:
- Currency conversions
- Position sizing
- Strategy execution
- End-to-end pipeline usage

---

## Currency Conversion Example
```python
from utils.conversions import convert

# Convert 100 EUR to USD
usd_value = convert(amount=100, from_unit="EUR", to_unit="USD")
print(f"Converted value: {usd_value} USD")
