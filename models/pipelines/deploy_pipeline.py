# models/pipelines/deploy_pipeline.py
import subprocess
import json
import os
from utils import setup_logger, load_config

logger = setup_logger("deploy_pipeline")

def run_command(cmd: list, cwd: str = None):
    """Run shell command with logging."""
    logger.info(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"Error: {result.stderr}")
        raise RuntimeError(result.stderr)
    logger.info(result.stdout)
    return result.stdout

def build_docker_image(config):
    """Build Docker image."""
    image_tag = f"{config['docker']['image_name']}:{config['docker']['tag']}"
    run_command(["docker", "build", "-t", image_tag, "."], cwd=config["docker"]["context"])
    return image_tag

def push_docker_image(config, image_tag):
    """Push Docker image to registry."""
    if config["docker"].get("push", False):
        run_command(["docker", "push", image_tag])
        logger.info(f"Pushed image {image_tag} to registry.")

def deploy_to_kubernetes(config, image_tag):
    """Deploy to Kubernetes cluster using kubectl."""
    if config["kubernetes"].get("enabled", False):
        manifest = config["kubernetes"]["manifest"]
        run_command(["kubectl", "apply", "-f", manifest])
        logger.info(f"Applied Kubernetes manifest {manifest}.")
        run_command(["kubectl", "set", "image", f"deployment/{config['kubernetes']['deployment']}",
                     f"{config['kubernetes']['container']}={image_tag}"])
        logger.info(f"Updated deployment {config['kubernetes']['deployment']} with image {image_tag}.")

def run_deploy_pipeline(config_path="configs/deploy_config.json"):
    """Main deployment pipeline."""
    config = load_config(config_path)
    logger.info("Starting deployment pipeline...")

    image_tag = build_docker_image(config)
    push_docker_image(config, image_tag)
    deploy_to_kubernetes(config, image_tag)

    logger.info("Deployment pipeline completed successfully.")

if __name__ == "__main__":
    run_deploy_pipeline()
