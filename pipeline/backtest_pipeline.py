# pipelines/backtest_pipeline.py
import pandas as pd
from models.evaluate import load_model
from utils import setup_logger

logger = setup_logger("backtest")

def run_backtest(data_path: str, model_path: str = "models/model.pkl"):
    df = pd.read_csv(data_path)
    model = load_model(model_path)

    # Example: predict signals
    signals = model.predict(df.drop("target", axis=1))
    df["signals"] = signals

    # Simple PnL calc (long=1, short=0)
    df["returns"] = df["signals"].shift(1) * df["target"]
    pnl = df["returns"].sum()

    logger.info(f"Backtest PnL: {pnl}")
    print(f"Backtest PnL: {pnl}")

if __name__ == "__main__":
    run_backtest("data/backtest_data.csv")
