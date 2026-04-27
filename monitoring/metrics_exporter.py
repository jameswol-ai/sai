from prometheus_client import start_http_server, Gauge, Counter
import time

# Define metrics
pnl_total = Gauge("sai_pnl_total", "Total Profit and Loss")
trades_per_minute = Gauge("sai_trades_per_minute", "Trades executed per minute")
trade_latency = Gauge("sai_trade_latency_seconds", "Latency per trade in seconds")
open_positions = Gauge("sai_open_positions", "Number of open positions")
model_version = Gauge("sai_model_version", "Current ML model version")

trade_counter = Counter("sai_trade_count", "Total trades executed")

def expose_metrics():
    # Start Prometheus metrics server on port 8000
    start_http_server(8000)
    print("Prometheus metrics server running on http://localhost:8000/metrics")

    # Example loop to update metrics
    while True:
        # Replace with real trading bot values
        pnl_total.set(1250.75)              # Example PnL
        trades_per_minute.set(5)            # Example trade frequency
        trade_latency.set(0.85)             # Example latency
        open_positions.set(3)               # Example open positions
        model_version.set(20260427)         # Example model version ID
        trade_counter.inc()                 # Increment trade count

        time.sleep(15)  # Update every 15s

if __name__ == "__main__":
    expose_metrics()
