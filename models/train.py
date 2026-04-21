# models/train.py
import argparse
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def load_data(data_path: str):
    """Load CSV data for training."""
    df = pd.read_csv(data_path)
    # Example: assume 'features' columns and 'target' column exist
    X = df.drop(columns=['target'])
    y = df['target']
    return X, y

def train_model(X, y):
    """Train a simple RandomForest model."""
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_val)
    acc = accuracy_score(y_val, y_pred)
    print(f"Validation Accuracy: {acc:.4f}")

    return model

def save_model(model, model_path: str):
    """Save trained model to disk."""
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

def main(args):
    X, y = load_data(args.data_path)
    model = train_model(X, y)
    save_model(model, args.model_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train and save model.pkl")
    parser.add_argument("--data_path", type=str, required=True, help="Path to training data CSV")
    parser.add_argument("--model_path", type=str, default="models/model.pkl", help="Path to save model")
    args = parser.parse_args()
    main(args)
