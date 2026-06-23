import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def forecast(series, steps=7):
    model = ARIMA(series, order=(1,1,1))
    model_fit = model.fit()
    preds = model_fit.forecast(steps=steps)
    return preds.tolist()
