# models/pipelines/backtest_pipeline.py
import os
import json
import pandas as pd
from datetime import datetime
from models.evaluate import load_model
from utils import load_config, setup_logger

logger = setup_logger("backtest_pipeline")

def run_backtest_pipeline(config_path: str = "configs/backtest_config.json"):
    # Load configuration
    config = load_config(config_path)
    data_path = config.get("data_path", "data/backtest_data.csv")
    model_path = config.get("model_path", "models/model.pkl")
    log_path = config.get("log_path", "logs/backtest.json")

    logger.info("Starting backtest pipeline...")
    logger.info(f"Data path: {data_path}")
    logger.info(f"Model path: {model_path}")
    logger.info(f"Log path: {log_path}")

    # Load historical data
    df = pd.read_csv(data_path)
    X = df.drop(["target", "timestamp"], axis=1, errors='ignore')
    y = df["target"]

    # Load trained model
    model = load_model(model_path)

    # Predict signals (1 = long, 0 = short/flat)
    df["signals"] = model.predict(X)

    # Calculate returns (simple PnL: signal * target)
    df["returns"] = df["signals"].shift(1) * y
    pnl = df["returns"].sum()

    metrics = {
        "pnl": pnl,
        "total_trades": int(df["signals"].sum()),
        "avg_return": df["returns"].mean(),
        "max_drawdown": df["returns"].min()
    }

    logger.info(f"Backtest metrics: {metrics}")

    # Append metrics to log file with timestamp
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "model_path": model_path,
        "data_path": data_path,
        "metrics": metrics
    }

    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            history = json.load(f)
    else:
        history = []

    history.append(log_entry)

    with open(log_path, "w") as f:
        json.dump(history, f, indent=4)

    logger.info(f"Backtest results logged to {log_path}")

    return metrics

if __name__ == "__main__":
    results = run_backtest_pipeline()
    print("Backtest pipeline finished.")
    print("Results:", results)
