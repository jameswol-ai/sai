import streamlit as st
import threading
import time
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import random
import logging
import yaml
from binance.client import Client

# --- Logging Setup ---
logging.basicConfig(filename="workflow.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# --- Binance Client Setup ---
def init_binance():
    try:
        with open("sai/configs/binance.yaml", "r") as f:
            cfg = yaml.safe_load(f)
        api_key = cfg.get("api_key", "")
        api_secret = cfg.get("api_secret", "")
        if api_key and api_secret:
            return Client(api_key, api_secret)
        else:
            st.warning("Binance API keys missing in configs/binance.yaml")
    except FileNotFoundError:
        st.warning("Binance config file not found at sai/configs/binance.yaml")
    except Exception as e:
        logging.error(f"Failed to load Binance config: {e}")
        st.warning("Error loading Binance configuration.")
    return None

def get_live_price(symbol="BTCUSDT"):
    client = init_binance()
    if client:
        try:
            ticker = client.get_symbol_ticker(symbol=symbol)
            return float(ticker["price"])
        except Exception as e:
            logging.error(f"Binance price feed error: {e}")
            st.warning(f"Could not fetch live price for {symbol}, using fallback.")
    return round(random.uniform(95, 110), 2)

# --- Trade Generator ---
def generate_trade():
    symbol = st.session_state.get("symbol", "BTCUSDT")
    price = get_live_price(symbol)
    balance = st.session_state.get("balance", 10000.0)
    positions = st.session_state.get("positions", [])

    active_model_name = st.session_state.get("active_model")
    if active_model_name:
        model = st.session_state["models"][active_model_name]
        try:
            decision = model.predict([[price]])[0]
        except Exception as e:
            logging.error(f"Model prediction failed: {e}")
            decision = random.choice(["BUY", "SELL", "HOLD"])
    else:
        decision = random.choice(["BUY", "SELL", "HOLD"])

    buy_threshold = st.session_state.get("buy_threshold", 100.0)
    sell_threshold = st.session_state.get("sell_threshold", 105.0)

    if decision == "BUY" and price < buy_threshold and balance >= price:
        balance -= price
        positions.append(price)
    elif decision == "SELL" and price > sell_threshold and positions:
        positions.pop()
        balance += price

    st.session_state["balance"] = balance
    st.session_state["positions"] = positions

    result = {"decision": decision, "price": price,
              "balance": balance, "positions": positions.copy()}
    logging.info(f"Trade executed: {result}")
    return result

# --- Live Trading Loop ---
def trading_loop():
    while st.session_state.get("running", False):
        result = generate_trade()
        st.session_state["last_result"] = result
        if "history" not in st.session_state:
            st.session_state["history"] = []
        st.session_state["history"].append(result)
        time.sleep(5)

def start_trading():
    if not st.session_state.get("running", False):
        st.session_state["running"] = True
        thread = threading.Thread(target=trading_loop, daemon=True)
        thread.start()

def stop_trading():
    st.session_state["running"] = False

# --- Dashboard Tab ---
def dashboard_tab():
    st.header("Dashboard")
    client = init_binance()
    if client:
        try:
            client.ping()
            st.success("✅ Binance connection active")
        except Exception as e:
            logging.error(f"Binance ping failed: {e}")
            st.error("❌ Binance connection failed")
    else:
        st.warning("⚠️ Binance client not initialized")

    col1, col2 = st.columns(2)
    if col1.button("Start Live Trading"):
        start_trading()
    if col2.button("Stop Live Trading"):
        stop_trading()

    result = st.session_state.get("last_result")
    if result:
        st.metric("Decision", result["decision"])
        st.metric("Price", result["price"])
        st.metric("Balance", result["balance"])
        st.write("Positions:", result["positions"])

# --- Strategy Config Tab ---
def strategy_config_tab():
    st.header("Strategy Config")
    buy_threshold = st.number_input("Buy threshold", value=100.0)
    sell_threshold = st.number_input("Sell threshold", value=105.0)
    symbol = st.text_input("Trading Symbol", value=st.session_state.get("symbol", "BTCUSDT"))
    if st.button("Update Strategy"):
        st.session_state["buy_threshold"] = buy_threshold
        st.session_state["sell_threshold"] = sell_threshold
        st.session_state["symbol"] = symbol
        st.success(f"Updated strategy: BUY<{buy_threshold}, SELL>{sell_threshold}, Symbol={symbol}")

# --- Logs Tab ---
def logs_tab():
