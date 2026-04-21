# models/pipelines/evaluate_pipeline.py

# models/pipelines/evaluate_pipeline.py
import os
import json
import pandas as pd
from datetime import datetime
from models.evaluate import load_model, evaluate_model
from utils import load_config, setup_logger

logger = setup_logger("evaluate_pipeline")

def run_evaluation_pipeline(config_path: str = "configs/evaluate_config.json"):
    # Load configuration
    config = load_config(config_path)
    data_path = config.get("data_path", "data/test.csv")
    model_path = config.get("model_path", "models/model.pkl")
    log_path = config.get("log_path", "logs/evaluation.json")

    logger.info("Starting evaluation pipeline...")
    logger.info(f"Data path: {data_path}")
    logger.info(f"Model path: {model_path}")
    logger.info(f"Log path: {log_path}")

    # Load test dataset
    df = pd.read_csv(data_path)
    X_test = df.drop(["target", "timestamp"], axis=1, errors='ignore')
    y_test = df["target"]

    # Load trained model
    model = load_model(model_path)

    # Evaluate model
    metrics = evaluate_model(model, X_test, y_test)
    logger.info(f"Evaluation metrics: {metrics}")

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

    logger.info(f"Metrics logged to {log_path}")

    return metrics

if __name__ == "__main__":
    results = run_evaluation_pipeline()
    print("Evaluation pipeline finished.")
    print("Results:", results)
