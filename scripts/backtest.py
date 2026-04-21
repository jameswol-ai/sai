# scripts/backtest.py
import argparse
from models.pipelines.backtest_pipeline import run_backtest_pipeline

def main():
    parser = argparse.ArgumentParser(description="Run backtest pipeline")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/backtest_config.json",
        help="Path to backtest configuration file"
    )
    args = parser.parse_args()

    results = run_backtest_pipeline(config_path=args.config)

    print("\n=== Backtest Results ===")
    for k, v in results.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
