# scripts/plot_metrics.py
import json
import matplotlib.pyplot as plt
from datetime import datetime

def load_evaluation_log(log_path="logs/evaluation.json"):
    with open(log_path, "r") as f:
        return json.load(f)

def plot_metrics(log_path="logs/evaluation.json"):
    history = load_evaluation_log(log_path)

    # Extract timestamps and metrics
    timestamps = [datetime.fromisoformat(entry["timestamp"]) for entry in history]
    accuracy = [entry["metrics"].get("accuracy") for entry in history]
    precision = [entry["metrics"].get("precision") for entry in history]
    recall = [entry["metrics"].get("recall") for entry in history]
    f1 = [entry["metrics"].get("f1_score") for entry in history]

    # Plot each metric
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, accuracy, marker="o", label="Accuracy")
    plt.plot(timestamps, precision, marker="o", label="Precision")
    plt.plot(timestamps, recall, marker="o", label="Recall")
    plt.plot(timestamps, f1, marker="o", label="F1 Score")

    plt.title("Model Evaluation Metrics Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("Score")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    plot_metrics()
