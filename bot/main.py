# bot/main.py
import argparse
from utils import setup_logger
from models.pipelines.train_pipeline import run_training_pipeline
from models.pipelines.evaluate_pipeline import run_evaluation_pipeline
from models.pipelines.backtest_pipeline import run_backtest_pipeline
from models.pipelines.deploy_pipeline import run_deploy_pipeline

logger = setup_logger("main")

def main():
    parser = argparse.ArgumentParser(description="SAI Trading Bot")
    parser.add_argument(
        "--mode",
        choices=["train", "evaluate", "backtest", "deploy", "live"],
        required=True,
        help="Choose the mode: train, evaluate, backtest, deploy, or live trading"
    )
    parser.add_argument(
        "--config",
        default=None,
        help="Path to config file (JSON)"
    )
    args = parser.parse_args()

    if args.mode == "train":
        logger.info("Running training pipeline...")
        config_path = args.config or "configs/train_config.json"
        results = run_training_pipeline(config_path=config_path)
        print("Training finished. Metrics:", results)

    elif args.mode == "evaluate":
        logger.info("Running evaluation pipeline...")
        config_path = args.config or "configs/evaluate_configs.json"
        results = run_evaluation_pipeline(config_path=config_path)
        print("Evaluation finished. Metrics:", results)

    elif args.mode == "backtest":
        logger.info("Running backtest pipeline...")
        config_path = args.config or "configs/backtest_config.json"
        results = run_backtest_pipeline(config_path=config_path)
        print("Backtest finished. Results:", results)

    elif args.mode == "deploy":
        logger.info("Running deployment pipeline...")
        config_path = args.config or "configs/deploy_config.json"
        run_deploy_pipeline(config_path=config_path)
        print("Deployment finished.")

    elif args.mode == "live":
        logger.info("Starting live trading...")
        from scripts.live_trading import main as live_main
        # Pass arguments to live_trading script
        import sys
        sys.argv = ['live_trading.py', '--interval', '60']  # Default interval
        live_main()

if __name__ == "__main__":
    main()
