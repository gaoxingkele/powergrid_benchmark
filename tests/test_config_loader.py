from pathlib import Path

from powergrid_benchmark.config import load_experiment_config


def test_load_sample_experiment_config() -> None:
    config = load_experiment_config(
        Path("configs/experiments/ieee14_load_forecast_smoke.json")
    )

    assert config["id"] == "ieee14_load_forecast_smoke"
    assert config["task"] == "load_forecasting"
