def run_bot():
    """
    Called by the bot thread. Scans all available currencies and returns
    a list of trade signals (or empty list). Executes trades if auto_trade is on.
    """
    with st.session_state.live_rates_lock:
        rates = st.session_state.live_rates_data.get("rates", {})
    if not rates:
        return []

    df_hist = st.session_state.history
    if df_hist is None or df_hist.empty:
        return []

    # Only process East African currencies that exist in live rates
    available = [c for c in EAST_AFRICAN_CURRENCIES if c in rates]
    if not available:
        return []

    signals = []

    for cur in available:
        cur_data = df_hist[df_hist["Currency"] == cur].tail(100).copy()
        cur_data["Time_dt"] = pd.to_datetime(cur_data["Time"])
        cur_data = cur_data.sort_values("Time_dt")

        if len(cur_data) < 50:
            continue   # not enough data for indicators

        trade_signal = compute_trade_signal(cur_data, st.session_state.risk_level)
        if trade_signal:
            trade_signal["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            trade_signal["amount"] = max(100, trade_signal["amount"])
            signals.append(trade_signal)

            # Auto‑trade if enabled
            if st.session_state.auto_trade:
                trading_api = get_trading_api()
                try:
                    units = trade_signal["amount"] if trade_signal["trade"] == "BUY" else -trade_signal["amount"]
                    trading_api.place_order(
                        symbol=trade_signal["symbol"],
                        units=units
                    )
                    logger.info(f"Bot auto‑trade: {trade_signal}")
                except Exception as e:
                    logger.error(f"Bot trade failed for {cur}: {e}")
                    trade_signal["error"] = str(e)

    return signals
