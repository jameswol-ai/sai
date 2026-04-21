# models/pipelines/train_pipeline.py
import os
from models.train import train_model
from models.evaluate import evaluate_model
from utils import load_config, setup_logger

logger = setup_logger("train_pipeline")

def run_training_pipeline(config_path: str = "configs/train_config.json"):
    # Load configuration
    config = load_config(config_path)
    data_path = config.get("data_path", "data/train.csv")
    model_path = config.get("model_path", "models/model.pkl")

    logger.info("Starting training pipeline...")
    logger.info(f"Data path: {data_path}")
    logger.info(f"Model output path: {model_path}")

    # Train model
    model, (X_test, y_test) = train_model(
        data_path=data_path,
        model_path=model_path
    )
    logger.info("Model training complete.")

    # Evaluate model
    metrics = evaluate_model(model, X_test, y_test)
    logger.info(f"Evaluation metrics: {metrics}")

    # Save model
    if not os.path.exists(os.path.dirname(model_path)):
        os.makedirs(os.path.dirname(model_path))
    logger.info(f"Model saved to {model_path}")

    return metrics

if __name__ == "__main__":
    results = run_training_pipeline()
    print("Training pipeline finished.")
    print("Evaluation results:", results)
