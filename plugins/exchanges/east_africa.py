# plugins/exchanges/east_africa.py
import requests
import datetime

CURRENCIES = ["KES", "UGX", "TZS", "ETB", "RWF", "BIF", "SSP", "SOS", "ERN", "DJF", "KMF"]

def get_rates(base="USD"):
    url = f"https://api.exchangerate.host/latest?base={base}&symbols={','.join(CURRENCIES)}"
    resp = requests.get(url)
    data = resp.json()
    return {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "base": base,
        "rates": data.get("rates", {})
    }

def get_daily_history(currency, base="USD", days=30):
    url = f"https://api.exchangerate.host/timeseries?base={base}&symbols={currency}&start_date={datetime.date.today().replace(day=1)}&end_date={datetime.date.today()}"
    resp = requests.get(url)
    data = resp.json()
    history = []
    if "rates" in data:
        for date, val in data["rates"].items():
            history.append((date, val.get(currency)))
    return history
