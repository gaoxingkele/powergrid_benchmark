"""Derive clipping direction/counts from the preserved P3 S3 front archive."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "evidence" / "runs" / "p3_s3_planning_validation_20260813"
OBJECTIVES = ("cost", "loss", "voltage", "negative_hosting", "negative_reliability")


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> int:
    archive = np.load(RUN / "optimizer_rerun" / "front_objectives.npz")
    objectives = archive["objectives"]
    index = rows(RUN / "optimizer_rerun" / "front_index.csv")
    bounds_rows = rows(RUN / "hv_diagnostics" / "normalization_bounds.csv")
    bounds: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    for experiment in sorted({row["experiment_id"] for row in bounds_rows}):
        selected = [row for row in bounds_rows if row["experiment_id"] == experiment]
        bounds[experiment] = (
            np.array([float(row["sampled_lower"]) for row in selected]),
            np.array([float(row["sampled_upper"]) for row in selected]),
        )

    counts = {
        (experiment, objective): [0, 0]
        for experiment in bounds
        for objective in OBJECTIVES
    }
    for run in index:
        front = objectives[int(run["front_start"]) : int(run["front_stop"])]
        lower, upper = bounds[run["experiment_id"]]
        normalized = (front - lower) / (upper - lower)
        for column, objective in enumerate(OBJECTIVES):
            counts[(run["experiment_id"], objective)][0] += int(
                np.sum(normalized[:, column] < -1e-12)
            )
            counts[(run["experiment_id"], objective)][1] += int(
                np.sum(normalized[:, column] > 1.0 + 1e-12)
            )

    output = RUN / "hv_diagnostics" / "clipping_direction_audit.csv"
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            ["experiment_id", "objective", "below_zero_coordinates", "above_one_coordinates"]
        )
        for (experiment, objective), (below, above) in sorted(counts.items()):
            writer.writerow([experiment, objective, below, above])

    manifest = {
        "source_front_archive_sha256": sha256(
            RUN / "optimizer_rerun" / "front_objectives.npz"
        ),
        "source_bounds_sha256": sha256(
            RUN / "hv_diagnostics" / "normalization_bounds.csv"
        ),
        "postprocessor_sha256": sha256(Path(__file__).resolve()),
        "output_sha256": sha256(output),
        "below_zero_total": sum(value[0] for value in counts.values()),
        "above_one_total": sum(value[1] for value in counts.values()),
    }
    (RUN / "hv_diagnostics" / "clipping_postprocess_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
