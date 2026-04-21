# models/__init__.py
"""
Models package for SAI trading bot.
Handles training, evaluation, and persistence of ML models.
"""

from .train import train_model
from .evaluate import load_model, evaluate_model
