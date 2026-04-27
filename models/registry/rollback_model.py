import shutil

def rollback_model(model_name, registry_dir="models/registry_store", active_model="models/model.pkl"):
    src = os.path.join(registry_dir, model_name)
    shutil.copy(src, active_model)
    print(f"Rolled back to {model_name}")

if __name__ == "__main__":
    rollback_model("model_20260427_220000.pkl")
