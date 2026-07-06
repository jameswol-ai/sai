import pandas as pd
import numpy as np
from typing import Tuple, Optional, Dict, Any
from datetime import timedelta
from config import logger

def fit_prophet(df_rates: pd.DataFrame) -> Dict[str, Any]:
    df = df_rates.copy()
    last_y = df["y"].iloc[-1]
    try:
        from prophet import Prophet
        m = Prophet()
        m.fit(df.rename(columns={"ds": "ds", "y": "y"}))
        return {"model": m, "fitted": True, "last_y": last_y, "last_date": df["ds"].max()}
    except ImportError:
        df["ds_num"] = (df["ds"] - df["ds"].min()).dt.total_seconds() / 86400
        slope = 0 if len(df) <= 1 else np.polyfit(df["ds_num"], df["y"], 1)[0]
        return {"last_date": df["ds"].max(), "slope": slope, "last_y": last_y, "fitted": False}
    except Exception as e:
        logger.warning(f"Prophet fitting failed ({e}), using stub.")
        df["ds_num"] = (df["ds"] - df["ds"].min()).dt.total_seconds() / 86400
        slope = 0 if len(df) <= 1 else np.polyfit(df["ds_num"], df["y"], 1)[0]
        return {"last_date": df["ds"].max(), "slope": slope, "last_y": last_y, "fitted": False}

def forecast_future(prophet_model: Dict[str, Any], periods: int = 1, freq: str = "D") -> Tuple[pd.DataFrame, Optional[Any]]:
    if prophet_model.get("fitted"):
        try:
            future = prophet_model["model"].make_future_dataframe(periods=periods, freq=freq)
            forecast = prophet_model["model"].predict(future)
            return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(periods), forecast
        except Exception as e:
            logger.warning(f"Prophet forecast failed ({e}), using stub.")
    last_date = prophet_model["last_date"]
    slope = prophet_model.get("slope", 0)
    last_y = prophet_model["last_y"]
    dates = [last_date + timedelta(days=i+1) for i in range(periods)]
    values = [last_y + slope * (i+1) for i in range(periods)]
    return pd.DataFrame({"ds": dates, "yhat": values}), None
