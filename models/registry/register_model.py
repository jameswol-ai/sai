import os
import shutil
from datetime import datetime

def register_model(model_path, registry_dir="models/registry_store"):
    os.makedirs(registry_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = os.path.join(registry_dir, f"model_{timestamp}.pkl")
    shutil.copy(model_path, dest)
    print(f"Model registered at {dest}")

if __name__ == "__main__":
    register_model("models/model.pkl")
