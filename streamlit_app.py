# ... [imports, TradingBot, Metrics, CSVExporter, RiskPlugin, CoreLoop as before] ...

# ---------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------
st.set_page_config(page_title="SAI Trading Dashboard", layout="wide")
st.title("SAI Trading Dashboard (Multi‑Currency)")

if "bot" not in st.session_state:
    st.session_state.bot = TradingBot()
if "metrics" not in st.session_state:
    st.session_state.metrics = Metrics()
if "csv" not in st.session_state:
    st.session_state.csv = CSVExporter()
if "risk_plugin" not in st.session_state:
    st.session_state.risk_plugin = RiskPlugin()
if "fx_rates" not in st.session_state:
    st.session_state.fx_rates = {c: 1.0 for c in CURRENCIES.keys()}
if "loop" not in st.session_state:
    st.session_state.loop = None

# Tabs
tab_dashboard, tab_strategy, tab_logs, tab_debug = st.tabs(
    ["📊 Dashboard", "🧠 Strategy", "📜 Logs", "🛠 Debug"]
)

# Dashboard
with tab_dashboard:
    st.subheader("Live Trading Controls")
    col1, col2, col3 = st.columns([1,1,1])

    if col1.button("Start Trading"):
        if st.session_state.loop is None or not st.session_state.loop.running:
            st.session_state.loop = CoreLoop(
                st.session_state.bot,
                st.session_state.metrics,
                st.session_state.csv,
                st.session_state.risk_plugin,
                sleep_time=1.0
            )
            threading.Thread(target=st.session_state.loop.start, daemon=True).start()

    if col2.button("Stop Trading"):
        if st.session_state.loop:
            st.session_state.loop.stop()

    currency_choice = col3.selectbox("Select Currency", list(CURRENCIES.keys()))
    st.session_state.bot.currency = currency_choice

    if col3.button("Update FX Rates"):
        st.session_state.fx_rates = {
            c: get_fx_rate("USD", c) or 1.0 for c in CURRENCIES.keys()
        }

    snap = st.session_state.metrics.snapshot(st.session_state.bot)
    st.subheader("Live Metrics")
    st.metric("Last Price", snap["last_price"])
    st.metric("Last Action", snap["last_action"])
    st.metric("Balance (USD)", snap["balance_usd"])
    st.metric(f"Balance ({snap['currency']})", f"{CURRENCIES[snap['currency']]['symbol']} {snap['balance_local']}")
    st.metric("PnL (USD)", snap["pnl_usd"])
    st.metric(f"PnL ({snap['currency']})", f"{CURRENCIES[snap['currency']]['symbol']} {snap['pnl_local']}")

    st.subheader("Price Chart")
    st.line_chart(snap["prices"])

# Strategy
with tab_strategy:
    st.subheader("Strategy Configuration (Placeholder)")
    st.text_area("Strategy Notes", placeholder="Describe or configure your strategy here...")

# Logs
with tab_logs:
    st.subheader("CSV Log Preview")
    if os.path.exists(st.session_state.csv.filename):
        with open(st.session_state.csv.filename, "rb") as f:
            data = f.read()
            st.download_button(
                label="Download trades.csv",
                data=data,
                file_name="trades.csv",
                mime="text/csv"
            )

        with open(st.session_state.csv.filename, "r", newline="") as f:
            rows = list(csv.reader(f))
            header, body = (rows[0], rows[1:]) if len(rows) > 1 else ([], [])
            preview = [header] + body[-20:] if header else []
            if preview:
                st.table(preview)
            else:
                st.write("No rows yet.")
    else:
        st.write("No logs yet.")

# Debug
with tab_debug:
    st.subheader("Debug Info")
    st.json({
        "loop_running": bool(st.session_state.loop.running) if st.session_state.loop else False,
        "last_price": st.session_state.metrics.prices[-1] if st.session_state.metrics.prices else None,
        "last_action": st.session_state.metrics.actions[-1] if st.session_state.metrics.actions else None,
        "balance": st.session_state.metrics.balance,
        "pnl": st.session_state.metrics.pnl,
        "total_prices": len(st.session_state.metrics.prices),
    })
