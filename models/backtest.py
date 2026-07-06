import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict
from models.arima_model import fit_arima, forecast_next
from models.prophet_model import fit_prophet, forecast_future

def backtest_strategy(currency: str, df_full: pd.DataFrame, strategy: str,
                      start_date: datetime, end_date: datetime, steps: int = 1) -> Dict:
    df = df_full[(df_full["Currency"] == currency) &
                 (df_full["Time_dt"] >= start_date) &
                 (df_full["Time_dt"] <= end_date)].sort_values("Time_dt").reset_index(drop=True)
    if len(df) < 50:
        return {"error": "Not enough data in date range."}
    initial_balance = 10000.0
    balance = initial_balance
    position = None
    equity_curve = []
    trades = []
    for i in range(50, len(df) - steps):
        train = df.iloc[:i]
        current_rate = df.iloc[i]["Rate"]
        if strategy == "ARIMA":
            try:
                arima_res = fit_arima(train["Rate"])
                pred, _ = forecast_next(arima_res, steps=steps)
                forecast = pred[0]
            except:
                forecast = current_rate
        else:
            try:
                prophet_df = pd.DataFrame({"ds": train["Time_dt"], "y": train["Rate"]})
                prophet_m = fit_prophet(prophet_df)
                fc_df, _ = forecast_future(prophet_m, periods=steps)
                forecast = fc_df["yhat"].iloc[0] if not fc_df.empty else current_rate
            except:
                forecast = current_rate
        signal = "BUY" if forecast > current_rate * 1.005 else "SELL" if forecast < current_rate * 0.995 else "HOLD"
        if position is None and signal != "HOLD":
            position = {"type": signal, "entry": current_rate, "units": 1000}
        elif position is not None:
            if (position["type"] == "BUY" and signal == "SELL") or (position["type"] == "SELL" and signal == "BUY"):
                exit_rate = current_rate
                pnl = (exit_rate - position["entry"]) * position["units"] if position["type"] == "BUY" else (position["entry"] - exit_rate) * position["units"]
                balance += pnl
                trades.append({"entry_time": train.iloc[-1]["Time_dt"], "exit_time": df.iloc[i]["Time_dt"],
                               "type": position["type"], "pnl": pnl})
                position = None
        equity_curve.append(balance)
    if position is not None:
        exit_rate = df.iloc[-1]["Rate"]
        pnl = (exit_rate - position["entry"]) * position["units"] if position["type"] == "BUY" else (position["entry"] - exit_rate) * position["units"]
        balance += pnl
        trades.append({"entry_time": position["entry_time"], "exit_time": df.iloc[-1]["Time_dt"],
                       "type": position["type"], "pnl": pnl})
        equity_curve.append(balance)
    total_return = (balance - initial_balance) / initial_balance * 100
    returns = pd.Series(equity_curve).pct_change().dropna()
    sharpe = (returns.mean() / returns.std() * np.sqrt(252)) if returns.std() != 0 else 0
    max_drawdown = (pd.Series(equity_curve).cummax() - pd.Series(equity_curve)).max() / pd.Series(equity_curve).cummax().max() * 100
    win_rate = (sum(1 for t in trades if t["pnl"] > 0) / len(trades) * 100) if trades else 0
    return {
        "total_return": total_return,
        "sharpe": sharpe,
        "max_drawdown": max_drawdown,
        "win_rate": win_rate,
        "trades": trades,
        "equity_curve": equity_curve,
        "final_balance": balance
      }
