# Risk Management Guide

This document outlines the risk management framework for the AI Trading Bot. Proper risk controls ensure consistent performance and protect capital.

---

## 1. Core Principles

- **Capital Preservation**: Protect the trading account from large drawdowns.
- **Consistency**: Apply rules uniformly across strategies.
- **Risk/Reward Balance**: Target favorable ratios (e.g., 1:2 or higher).
- **Diversification**: Avoid overexposure to a single asset or strategy.

---

## 2. Position Sizing

Formula:

\[
\text{Position Size} = \frac{\text{Account Risk per Trade}}{\text{Stop-Loss Distance}}
\]

Example:
- Account size: \$10,000
- Risk per trade: 1% (\$100)
- Stop-loss distance: 2% (\$0.20 on a \$10 stock)
- Position size = \$100 / 0.20 = **500 shares**

---

## 3. Stop-Loss Rules

- **Fixed % Stop-Loss**: Exit if price moves against position by X%.
- **Volatility-Based Stop-Loss**: Use ATR (Average True Range) to set dynamic stops.
- **Trailing Stop-Loss**: Adjust stop upward as price moves in favor.

---

## 4. Take-Profit Rules

- **Fixed % Target**: Exit at predefined profit level (e.g., 5%).
- **Risk/Reward Target**: Exit when reward = 2 × risk.
- **Partial Profit Taking**: Close half position at target, let remainder run.

---

## 5. Risk Controls

- **Max Daily Loss**: Stop trading if losses exceed 3% of account.
- **Max Open Positions**: Limit concurrent trades (e.g., 5).
- **Correlation Check**: Avoid multiple trades in highly correlated assets.

---

## 6. Example Implementation

```python
def calculate_position(account_size, risk_pct, stop_loss_pct, price):
    risk_amount = account_size * risk_pct
    stop_loss_distance = price * stop_loss_pct
    position_size = risk_amount / stop_loss_distance
    return int(position_size)

# Example usage
account_size = 10000
risk_pct = 0.01   # 1%
stop_loss_pct = 0.02  # 2%
price = 10.0

size = calculate_position(account_size, risk_pct, stop_loss_pct, price)
print(f"Position size: {size} shares")
