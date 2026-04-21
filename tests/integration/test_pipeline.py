"""
Integration tests for pipeline orchestration.

Covers:
- Training pipeline execution
- Evaluation pipeline execution
- Backtesting pipeline execution
- Deployment pipeline (dry-run mode)
"""

import pytest
import pathlib
from models.pipelines import (
    train_pipeline,
    evaluate_pipeline,
    backtest_pipeline,
    deploy_pipeline,
)

@pytest.fixture
def config_paths(tmp_path):
    return {
        "train": tmp_path / "train_config.json",
        "evaluate": tmp_path / "evaluate_config.json",
        "backtest": tmp_path / "backtest_config.json",
        "deploy": tmp_path / "deploy_config.json",
    }

def test_train_pipeline_runs(config_paths):
    result = train_pipeline.run(config_path=config_paths["train"])
    assert result is not None
    assert "model_path" in result

def test_evaluate_pipeline_runs(config_paths):
    result = evaluate_pipeline.run(config_path=config_paths["evaluate"])
    assert result is not None
    assert "metrics" in result
    assert isinstance(result["metrics"], dict)

def test_backtest_pipeline_runs(config_paths):
    result = backtest_pipeline.run(config_path=config_paths["backtest"])
    assert result is not None
    assert "performance" in result
    assert "sharpe_ratio" in result["performance"]

def test_deploy_pipeline_dry_run(config_paths):
    result = deploy_pipeline.run(config_path=config_paths["deploy"], dry_run=True)
    assert result is not None
    assert "status" in result
    assert result["status"] in {"success", "skipped"}
