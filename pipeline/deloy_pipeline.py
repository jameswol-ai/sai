# pipelines/deploy_pipeline.py
import subprocess
from utils import load_config, setup_logger

logger = setup_logger("deploy")

def build_docker_image(config):
    """Build Docker image for the trading bot."""
    image_name = config["docker"]["image_name"]
    tag = config["docker"]["tag"]

    cmd = ["docker", "build", "-t", f"{image_name}:{tag}", "."]
    logger.info(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    logger.info(f"Docker image {image_name}:{tag} built successfully.")

def push_docker_image(config):
    """Push Docker image to registry."""
    image_name = config["docker"]["image_name"]
    tag = config["docker"]["tag"]

    cmd = ["docker", "push", f"{image_name}:{tag}"]
    logger.info(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    logger.info(f"Docker image {image_name}:{tag} pushed successfully.")

def run_deploy_pipeline():
    config = load_config("configs/deploy_config.json")

    # Step 1: Build image
    build_docker_image(config)

    # Step 2: Push image (optional)
    if config["docker"].get("push", False):
        push_docker_image(config)

    # Step 3: Deployment target (e.g., Kubernetes, cloud)
    if "k8s" in config:
        logger.info("Kubernetes deployment step would run here.")
        # Example: subprocess.run(["kubectl", "apply", "-f", config["k8s"]["manifest"]])

if __name__ == "__main__":
    run_deploy_pipeline()
