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
from prometheus_client import Gauge, start_http_server, CollectorRegistry

# --- Logging Setup ---
logging.basicConfig(filename="workflow.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# --- Initialize defaults ---
def init_defaults():
    defaults = {
        "balance": 10000.0,
        "positions": [],
        "buy_threshold": 100.0,
        "sell_threshold": 105.0,
        "symbol": "BTCUSDT",
        "models": {},
        "history": []
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# --- Binance Client Setup ---
def init_binance():
    try:
        with open("sai/configs/binance.yaml", "r") as f:
            cfg = yaml.safe_load(f)
        api_key, api_secret = cfg.get("api_key", ""), cfg.get("api_secret", "")
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
    symbol = st.session_state["symbol"]
    price = get_live_price(symbol)
    balance = st.session_state["balance"]
    positions = st.session_state["positions"]

    decision = random.choice(["BUY", "SELL", "HOLD"])
    active_model = st.session_state.get("active_model")
    if active_model and active_model in st.session_state["models"]:
        try:
            decision = st.session_state["models"][active_model].predict([[price]])[0]
        except Exception as e:
            logging.error(f"Model prediction failed: {e}")

    if decision == "BUY" and price < st.session_state["buy_threshold"] and balance >= price:
        balance -= price
        positions.append(price)
    elif decision == "SELL" and price > st.session_state["sell_threshold"] and positions:
        positions.pop()
        balance += price

    st.session_state["balance"] = balance
    st.session_state["positions"] = positions

    result = {"decision": decision, "price": price,
              "balance": balance, "positions": positions.copy()}
    logging.info(f"Trade executed: {result}")
    return result

# --- Prometheus Metrics ---
if "prom_registry" not in st.session_state:
    st.session_state["prom_registry"] = CollectorRegistry()
    st.session_state["trade_price_gauge"] = Gauge("sai_trade_price", "Latest trade price", registry=st.session_state["prom_registry"])
    st.session_state["balance_gauge"] = Gauge("sai_balance", "Current account balance", registry=st.session_state["prom_registry"])
    st.session_state["positions_gauge"] = Gauge("sai_positions", "Number of open positions", registry=st.session_state["prom_registry"])
    st.session_state["decision_gauge"] = Gauge("sai_decision", "Decision encoded as BUY=1, SELL=2, HOLD=3", registry=st.session_state["prom_registry"])
    st.session_state["win_rate_gauge"] = Gauge("sai_win_rate", "Win rate of trades", registry=st.session_state["prom_registry"])
    st.session_state["sharpe_ratio_gauge"] = Gauge("sai_sharpe_ratio", "Sharpe ratio of trading performance", registry=st.session_state["prom_registry"])
    start_http_server(8000, registry=st.session_state["prom_registry"])

def update_metrics(result):
    st.session_state["trade_price_gauge"].set(result["price"])
    st.session_state["balance_gauge"].set(result["balance"])
    st.session_state["positions_gauge"].set(len(result["positions"]))
    st.session_state["decision_gauge"].set({"BUY": 1, "SELL": 2, "HOLD": 3}[result["decision"]])

    if st.session_state["history"]:
        df = pd.DataFrame(st.session_state["history"])
        total_trades = len(df)
        sells = (df["decision"] == "SELL").sum()
        win_rate = sells / total_trades if total_trades > 0 else 0
        returns = df["balance"].pct_change().fillna(0)
        sharpe = (returns.mean() / returns.std()) * (252**0.5) if returns.std() > 0 else 0
        st.session_state["win_rate_gauge"].set(win_rate)
        st.session_state["sharpe_ratio_gauge"].set(sharpe)

# --- Live Trading Loop ---
def trading_loop():
    while st.session_state.get("running", False):
        result = generate_trade()
        st.session_state["last_result"] = result
        st.session_state["history"].append(result)
        update_metrics(result)
        time.sleep(5)

def start_trading():
    if not st.session_state.get("running", False):
        st.session_state["running"] = True
        threading.Thread(target=trading_loop, daemon=True).start()

def stop_trading():
    st.session_state["running"] = False

# --- Tabs ---
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

# (Other tab functions unchanged: strategy_config_tab, logs_tab, model_testing_tab, debug_tab, analytics_tab, model_registry_tab)

# --- Main App ---
def main():
    init_defaults()
    st.title("Trading Bot Dashboard_tab)

# --- Main App ---
def main():
    init_defaults()
    st.title("Trading Bot Dashboard")
    tabs = st.tabs([
        "📊 Dashboard",
        "⚙️ Strategy Config",
        "📝 Logs",
        "🧪 Model Testing",
        "🐞 Debug",
        "📈 Analytics",
        "📂 Model Registry"
    ])
    with tabs[0]: dashboard_tab()
    with tabs[1]: strategy_config_tab()
    with tabs[2]: logs_tab()
    with tabs[3]: model_testing_tab()
    with tabs[4]: debug_tab()
    with tabs[5]: analytics_tab()
    with tabs[6]: model_registry_tab()

if __name__ == "__main__":
    main()
