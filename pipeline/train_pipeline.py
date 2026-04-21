# pipelines/train_pipeline.py
from models.train import train_model
from models.evaluate import evaluate_model
from utils import load_config

def run_training_pipeline():
    config = load_config("configs/train_config.json")
    model, (X_test, y_test) = train_model(
        data_path=config["data_path"],
        model_path=config["model_path"]
    )
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    run_training_pipeline()
