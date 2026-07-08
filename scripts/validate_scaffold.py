from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "ara_artifacts/_template/PAPER.md",
    "configs/experiments/ieee14_load_forecast_smoke.json",
    "docs/benchmark_design/config_schema.md",
    "external_repos/repo_candidates.csv",
    "paper_projects/_template/README.md",
    "papers/metadata/paper_registry.csv",
    "src/powergrid_benchmark/__init__.py",
]

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


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_required_paths() -> list[str]:
    errors: list[str] = []
    for rel_path in REQUIRED_PATHS:
        if not (ROOT / rel_path).exists():
            errors.append(f"Missing required path: {rel_path}")
    return errors


def validate_experiment_config(path: Path) -> list[str]:
    errors: list[str] = []
    config = load_json(path)
    missing = sorted(REQUIRED_EXPERIMENT_FIELDS - set(config))
    if missing:
        errors.append(f"{path.relative_to(ROOT)} missing fields: {', '.join(missing)}")
    for field in ["system", "dataset", "split", "model", "metrics"]:
        rel = config.get(field)
        if isinstance(rel, str) and not (ROOT / rel).exists():
            errors.append(f"{path.relative_to(ROOT)} points to missing {field}: {rel}")
    return errors


def main() -> int:
    errors = validate_required_paths()
    for config_path in sorted((ROOT / "configs" / "experiments").glob("*.json")):
        errors.extend(validate_experiment_config(config_path))

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Scaffold validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
