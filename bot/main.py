# bot/main.py
import argparse
from utils import setup_logger
from models.pipelines.train_pipeline import run_training_pipeline
from models.pipelines.evaluate_pipeline import run_evaluation_pipeline

logger = setup_logger("main")

def main():
    parser = argparse.ArgumentParser(description="SAI Trading Bot")
    parser.add_argument(
        "--mode",
        choices=["train", "evaluate"],
        required=True,
        help="Choose whether to train or evaluate the model"
    )
    parser.add_argument(
        "--config",
        default=None,
        help="Path to config file (JSON)"
    )
    args = parser.parse_args()

    if args.mode == "train":
        logger.info("Running training pipeline...")
        results = run_training_pipeline(config_path=args.config or "configs/train_config.json")
        print("Training finished. Metrics:", results)

    elif args.mode == "evaluate":
        logger.info("Running evaluation pipeline...")
        results = run_evaluation_pipeline(config_path=args.config or "configs/evaluate_config.json")
        print("Evaluation finished. Metrics:", results)

if __name__ == "__main__":
    main()
