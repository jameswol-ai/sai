# scripts/plot_backtest.py
import json
import matplotlib.pyplot as plt
from datetime import datetime

def load_backtest_log(log_path="logs/backtest.json"):
    with open(log_path, "r") as f:
        return json.load(f)

def plot_backtest(log_path="logs/backtest.json"):
    history = load_backtest_log(log_path)

    # Extract timestamps and metrics
    timestamps = [datetime.fromisoformat(entry["timestamp"]) for entry in history]
    pnl = [entry["metrics"]["pnl"] for entry in history]
    avg_return = [entry["metrics"]["avg_return"] for entry in history]
    max_drawdown = [entry["metrics"]["max_drawdown"] for entry in history]

    # Plot equity curve (PnL over time)
    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, pnl, marker="o", label="PnL (Equity Curve)")
    plt.title("Backtest Equity Curve")
    plt.xlabel("Timestamp")
    plt.ylabel("PnL")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Plot average returns
    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, avg_return, marker="o", color="green", label="Average Return")
    plt.title("Average Return Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("Return")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Plot max drawdown
    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, max_drawdown, marker="o", color="red", label="Max Drawdown")
    plt.title("Max Drawdown Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("Drawdown")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_backtest()
