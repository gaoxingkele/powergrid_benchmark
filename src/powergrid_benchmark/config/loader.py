from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REQUIRED_EXPERIMENT_FIELDS = {
    "id",
    "task",
    "domain",
    "system",
    "dataset",
    "split",
    "model",
    "metrics",
    "outputs",
}


def load_experiment_config(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as f:
        config: dict[str, Any] = json.load(f)

    missing = REQUIRED_EXPERIMENT_FIELDS - set(config)
    if missing:
        raise ValueError(f"Experiment config missing fields: {sorted(missing)}")
    return config
