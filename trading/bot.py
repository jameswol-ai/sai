import streamlit as st
import threading, time, queue, pandas as pd
from datetime import datetime
from config import logger, BOT_CONFIG, EAST_AFRICAN_CURRENCIES
from trading.signals import compute_trade_signal
from trading.api import get_trading_api
from utils.telegram import send_telegram
from utils.sound import play_sound

def run_bot():
    with st.session_state.live_rates_lock:
        rates = st.session_state.live_rates_data.get("rates", {})
    if not rates:
        return []

    df_hist = st.session_state.history
    if df_hist is None or df_hist.empty:
        return []

    available = [c for c in EAST_AFRICAN_CURRENCIES if c in rates]
    if not available:
        return []

    signals = []
    for cur in available:
        cur_data = df_hist[df_hist["Currency"] == cur].tail(100).copy()
        cur_data["Time_dt"] = pd.to_datetime(cur_data["Time"])
        cur_data = cur_data.sort_values("Time_dt")
        if len(cur_data) < 50:
            continue
        trade_signal = compute_trade_signal(cur_data, st.session_state.risk_level)
        if trade_signal:
            trade_signal["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            trade_signal["amount"] = max(100, trade_signal["amount"])
            signals.append(trade_signal)
            if st.session_state.auto_trade:
                trading_api = get_trading_api()
                try:
                    units = trade_signal["amount"] if trade_signal["trade"] == "BUY" else -trade_signal["amount"]
                    trading_api.place_order(symbol=trade_signal["symbol"], units=units)
                    play_sound()   # 🔊 Audio alert
                    logger.info(f"Bot auto‑trade: {trade_signal}")
                except Exception as e:
                    logger.error(f"Bot trade failed for {cur}: {e}")
                    trade_signal["error"] = str(e)
    return signals

def bot_loop(queue_obj, stop_event):
    logger.info("Bot thread started.")
    while not stop_event.is_set():
        try:
            trades = run_bot()
            for trade_info in trades:
                queue_obj.put(trade_info)
                with BOT_CONFIG["lock"]:
                    if BOT_CONFIG.get("alert_signals"):
                        if trade_info["trade"] in ("BUY", "SELL"):
                            send_telegram(
                                f"🤖 Bot signal: {trade_info['trade']} {trade_info['symbol']} "
                                f"@ {trade_info['price']:.2f} (units: {trade_info['amount']})"
                            )
        except Exception as e:
            error_data = {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "error": str(e)}
            queue_obj.put(error_data)
            logger.exception("Bot loop error")
            with BOT_CONFIG["lock"]:
                if BOT_CONFIG["alert_errors"]:
                    send_telegram(f"🚨 Bot error: {e}")
            time.sleep(5)
            continue
        time.sleep(5)
    logger.info("Bot thread exited.")

def start_bot():
    if st.session_state.bot_running:
        return
    with BOT_CONFIG["lock"]:
        BOT_CONFIG["alert_errors"] = st.session_state.alert_errors
        BOT_CONFIG["alert_signals"] = st.session_state.alert_signals
    st.session_state.stop_event = threading.Event()
    t = threading.Thread(target=bot_loop, args=(st.session_state.bot_queue, st.session_state.stop_event), daemon=True)
    st.session_state.bot_thread = t
    st.session_state.bot_running = True
    t.start()

def stop_bot():
    if st.session_state.bot_running:
        st.session_state.stop_event.set()
        st.session_state.bot_running = False

def drain_bot_queue(max_items=50):
    drained = 0
    items = []
    while not st.session_state.bot_queue.empty() and drained < max_items:
        try:
            item = st.session_state.bot_queue.get_nowait()
        except queue.Empty:
            break
        st.session_state.logs.append(item)
        items.append(item)
        drained += 1
    if items:
        from data.database import insert_bot_logs
        insert_bot_logs(items)
    if len(st.session_state.logs) > 1000:
        st.session_state.logs = st.session_state.logs[-1000:]
    return drained
