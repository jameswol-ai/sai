# models/pipelines/__init__.py
"""
Pipelines package initializer for SAI trading bot.
Exposes training, evaluation, backtesting, and deployment workflows.
"""

from .train_pipeline import run_training_pipeline
from .evaluate_pipeline import run_evaluation_pipeline
from .backtest_pipeline import run_backtest_pipeline
from .deploy_pipeline import run_deploy_pipeline

__all__ = [
    "run_training_pipeline",
    "run_evaluation_pipeline",
    "run_backtest_pipeline",
    "run_deploy_pipeline",
]
