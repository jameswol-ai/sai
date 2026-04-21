# models/evaluate.py
import argparse
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report

def load_data(data_path: str):
    """Load CSV data for evaluation."""
    df = pd.read_csv(data_path)
    X = df.drop(columns=['target'])
    y = df['target']
    return X, y

def load_model(model_path: str):
    """Load trained model from disk."""
    model = joblib.load(model_path)
    print(f"Model loaded from {model_path}")
    return model

def evaluate_model(model, X, y):
    """Run evaluation and print metrics."""
    y_pred = model.predict(X)
    acc = accuracy_score(y, y_pred)
    print(f"Evaluation Accuracy: {acc:.4f}")
    print("\nClassification Report:\n")
    print(classification_report(y, y_pred))

def main(args):
    X, y = load_data(args.data_path)
    model = load_model(args.model_path)
    evaluate_model(model, X, y)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate model.pkl on dataset")
    parser.add_argument("--data_path", type=str, required=True, help="Path to evaluation data CSV")
    parser.add_argument("--model_path", type=str, default="models/model.pkl", help="Path to trained model")
    args = parser.parse_args()
    main(args)
