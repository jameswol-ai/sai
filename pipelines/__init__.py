# __init__.py
"""
SAI Trading Bot
Modular AI trading framework with bot logic, ML models, and pipelines.
"""

# Expose key submodules for clean imports
from .bot import main, strategy, trader, data
from .models import train_model, evaluate_model, load_model
from .pipelines import (
    run_training_pipeline,
    run_evaluation_pipeline,
    run_backtest,
    run_deploy_pipeline
)

__version__ = "0.1.0"
