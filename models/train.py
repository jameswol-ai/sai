# train.py
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from utils import load_config, setup_logger

logger = setup_logger("train")

def load_data(path: str) -> pd.DataFrame:
    """Load CSV data for training."""
    return pd.read_csv(path)

def train_model(data_path: str, model_path: str = "models/model.pkl"):
    """Train and save model."""
    # Load data
    df = load_data(data_path)
    X = df.drop("target", axis=1)
    y = df["target"]

    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save model
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    logger.info(f"Model trained and saved to {model_path}")

    return model, (X_test, y_test)

if __name__ == "__main__":
    config = load_config("configs/train_config.json")
    train_model(config["data_path"], config["model_path"])
