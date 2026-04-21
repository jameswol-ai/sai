# Position Sizing

## Overview
Position sizing is a critical component of risk management in trading. It determines how much capital to allocate to each trade, balancing potential reward with acceptable risk.

---

## Core Approaches

### 1. Fixed Fractional
- Risk a fixed percentage of account equity per trade.
- Simple and widely used.
- Keeps risk proportional to account size.

**Formula:**
\[
\text{Position Size} = \frac{\text{Risk %} \times \text{Account Balance}}{\text{Stop Loss Distance}}
\]

---

### 2. Volatility-Based
- Adjusts position size according to asset volatility.
- Larger positions in stable assets, smaller in volatile ones.
- Uses indicators like ATR (Average True Range).

**Formula:**
\[
\text{Position Size} = \frac{\text{Risk Capital}}{\text{ATR} \times \text{Multiplier}}
\]

---

### 3. Kelly Criterion (Optional/Advanced)
- Maximizes long-term growth rate.
- Requires accurate win probability and payoff ratio.
- More aggressive; best used with caution.

**Formula:**
\[
f^* = \frac{bp - q}{b}
\]
Where:
- \(f^*\) = fraction of capital to risk  
- \(b\) = odds received (reward/risk ratio)  
- \(p\) = probability of winning  
- \(q\) = probability of losing (1 - p)

---

## Practical Examples

1. **Fixed Fractional**
   - Account Balance: $10,000  
   - Risk: 2% ($200)  
   - Stop Loss Distance: $5  
   - Position Size = $200 / $5 = 40 units

2. **Volatility-Based**
   - Risk Capital: $500  
   - ATR: $2  
   - Multiplier: 2  
   - Position Size = $500 / (2 × 2) = 125 units

---

## Best Practices
- Always define risk per trade before entering.
- Use `Decimal` for monetary calculations to avoid floating-point errors.
- Document chosen method in strategy guides (`docs/strategies.md`).
- Test different sizing methods in backtests before live trading.

---

## Implementation Notes
- Core logic lives in `plugins/position_sizing.py`.
- Configurable via `configs/risk_config.json`.
- Extendable: add custom sizing strategies as plugins.

---
