# models/pipelines/evaluate_pipeline.py
import pandas as pd
from models.evaluate import load_model, evaluate_model
from utils import load_config, setup_logger

logger = setup_logger("evaluate_pipeline")

def run_evaluation_pipeline(config_path: str = "configs/evaluate_config.json"):
    # Load configuration
    config = load_config(config_path)
    data_path = config.get("data_path", "data/test.csv")
    model_path = config.get("model_path", "models/model.pkl")

    logger.info("Starting evaluation pipeline...")
    logger.info(f"Data path: {data_path}")
    logger.info(f"Model path: {model_path}")

    # Load test dataset
    df = pd.read_csv(data_path)
    X_test = df.drop("target", axis=1)
    y_test = df["target"]

    # Load trained model
    model = load_model(model_path)

    # Evaluate model
    metrics = evaluate_model(model, X_test, y_test)
    logger.info(f"Evaluation metrics: {metrics}")

    return metrics

if __name__ == "__main__":
    results = run_evaluation_pipeline()
    print("Evaluation pipeline finished.")
    print("Results:", results)
