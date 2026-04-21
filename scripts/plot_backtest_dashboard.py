# scripts/plot_backtest_dashboard.py
import json
import matplotlib.pyplot as plt
from datetime import datetime

def load_backtest_log(log_path="logs/backtest.json"):
    with open(log_path, "r") as f:
        return json.load(f)

def plot_backtest_dashboard(log_path="logs/backtest.json"):
    history = load_backtest_log(log_path)

    # Extract timestamps and metrics
    timestamps = [datetime.fromisoformat(entry["timestamp"]) for entry in history]
    pnl = [entry["metrics"]["pnl"] for entry in history]
    avg_return = [entry["metrics"]["avg_return"] for entry in history]
    max_drawdown = [entry["metrics"]["max_drawdown"] for entry in history]

    # Create subplots
    fig, axes = plt.subplots(3, 1, figsize=(12, 12), sharex=True)

    # Equity curve (PnL)
    axes[0].plot(timestamps, pnl, marker="o", label="PnL (Equity Curve)")
    axes[0].set_title("Equity Curve (PnL)")
    axes[0].set_ylabel("PnL")
    axes[0].grid(True)
    axes[0].legend()

    # Average return
    axes[1].plot(timestamps, avg_return, marker="o", color="green", label="Average Return")
    axes[1].set_title("Average Return Over Time")
    axes[1].set_ylabel("Return")
    axes[1].grid(True)
    axes[1].legend()

    # Max drawdown
    axes[2].plot(timestamps, max_drawdown, marker="o", color="red", label="Max Drawdown")
    axes[2].set_title("Max Drawdown Over Time")
    axes[2].set_ylabel("Drawdown")
    axes[2].set_xlabel("Timestamp")
    axes[2].grid(True)
    axes[2].legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_backtest_dashboard()
