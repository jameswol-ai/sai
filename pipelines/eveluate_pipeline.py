# pipelines/evaluate_pipeline.py
from models.evaluate import load_model, evaluate_model
from utils import load_config
import pandas as pd

def run_evaluation_pipeline():
    # Load config
    config = load_config("configs/evaluate_config.json")

    # Load test dataset
    df = pd.read_csv(config["data_path"])
    X_test = df.drop("target", axis=1)
    y_test = df["target"]

    # Load trained model
    model = load_model(config["model_path"])

    # Evaluate
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    run_evaluation_pipeline()
