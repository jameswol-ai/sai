import requests
import datetime

CURRENCIES = ["KES", "UGX", "TZS", "ETB", "RWF", "BIF", "SSP", "SOS"]

def get_rates(base="USD"):
    url = f"https://api.exchangerate.host/latest?base={base}&symbols={','.join(CURRENCIES)}"
    resp = requests.get(url)
    data = resp.json()
    return {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "base": base,
        "rates": data.get("rates", {})
    }
