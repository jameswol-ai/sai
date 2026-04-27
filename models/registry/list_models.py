import os

def list_models(registry_dir="models/registry_store"):
    return sorted(os.listdir(registry_dir))

if __name__ == "__main__":
    print(list_models())
