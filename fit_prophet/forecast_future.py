def fit_prophet(df_rates):
    try:
        from prophet import Prophet
        m = Prophet()
        m.fit(df_rates.rename(columns={"ds": "ds", "y": "y"}))
        return {"model": m, "fitted": True, "last_y": df_rates["y"].iloc[-1], ...}
    except ImportError:
        # fallback stub (your existing code)
        ...