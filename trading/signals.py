import pandas as pd
from typing import Optional, Dict

def compute_trade_signal(rates_df: pd.DataFrame, risk_level: int) -> Optional[Dict]:
    if len(rates_df) < 50:
        return None
    close = rates_df["Rate"].astype(float)
    sma20 = close.rolling(20).mean().iloc[-1]
    sma50 = close.rolling(50).mean().iloc[-1]
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean().iloc[-1]
    avg_loss = loss.rolling(14).mean().iloc[-1]
    rsi = 100.0 if avg_loss == 0 else 100 - (100 / (1 + avg_gain / avg_loss))
    trade = "BUY" if sma20 > sma50 and rsi < 30 else "SELL" if sma20 < sma50 and rsi > 70 else None
    if trade:
        risk_fraction = risk_level / 100.0
        amount = int(1000 * risk_fraction) if risk_fraction else 1000
        return {"trade": trade, "amount": amount, "symbol": rates_df.iloc[-1]["Currency"],
                "price": close.iloc[-1]}
    return None

def generate_trade_signal(current_rate, forecast_value, threshold=0.01):
    if forecast_value is None:
        return "HOLD"
    change_pct = (forecast_value - current_rate) / current_rate
    if change_pct > threshold:
        return "BUY"
    elif change_pct < -threshold:
        return "SELL"
    return "HOLD"
