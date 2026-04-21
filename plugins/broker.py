import os
import requests

API_KEY = os.getenv("BROKER_API_KEY")
API_SECRET = os.getenv("BROKER_SECRET")
BASE_URL = "https://paper-api.alpaca.markets/v2"

def place_order(symbol, qty, side, order_type="market", time_in_force="gtc"):
    url = f"{BASE_URL}/orders"
    payload = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": order_type,
        "time_in_force": time_in_force
    }
    headers = {"APCA-API-KEY-ID": API_KEY, "APCA-API-SECRET-KEY": API_SECRET}
    return requests.post(url, json=payload, headers=headers).json()
