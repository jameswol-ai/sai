# evaluate.py
import pickle
from sklearn.metrics import accuracy_score, classification_report
from utils import setup_logger

logger = setup_logger("evaluate")

def load_model(model_path: str = "models/model.pkl"):
    """Load trained model from pickle."""
    with open(model_path, "rb") as f:
        return pickle.load(f)

def evaluate_model(model, X_test, y_test):
    """Evaluate model performance."""
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    logger.info(f"Accuracy: {acc:.4f}")
    logger.info(f"Classification Report:\n{report}")

    print(f"Accuracy: {acc:.4f}")
    print(report)

if __name__ == "__main__":
    # Example usage: load test data from train.py output
    from train import train_model
    model, (X_test, y_test) = train_model("data/training_data.csv")
    evaluate_model(model, X_test, y_test)
