#!/usr/bin/env python3
"""Analyze the frozen C2GES 5x5 upstream--downstream matrix."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
FREEZE = HERE / "PROTOCOL_FREEZE.json"
MODES = ("full", "no_role", "bm25")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def load_run(path: Path, upstream_seed: int, downstream_seed: int, cutoffs: list[int]):
    predictions = path / "predictions.jsonl"
    if not predictions.is_file():
        raise RuntimeError(f"missing prediction ledger: {predictions}")
    selected = []
    total = 0
    with predictions.open(encoding="utf-8") as handle:
        for line in handle:
            total += 1
            row = json.loads(line)
            if row["mode"] in MODES and int(row["k"]) in cutoffs:
                selected.append(
                    {
                        "upstream_seed": upstream_seed,
                        "downstream_seed": downstream_seed,
                        "qid": row["qid"],
                        "document": row.get("underlying_document_id", row["doc_id"]),
                        "mode": row["mode"],
                        "k": int(row["k"]),
                        "f1": float(row["f1"]),
                    }
                )
    if total != 54000:
        raise RuntimeError(f"expected 54,000 rows, found {total}: {predictions}")
    expected = 1500 * len(cutoffs) * len(MODES)
    if len(selected) != expected:
        raise RuntimeError(f"expected {expected} selected rows, found {len(selected)}: {predictions}")
    return selected, {"path": str(predictions), "bytes": predictions.stat().st_size, "sha256": sha256(predictions)}


def two_way_components(matrix: np.ndarray) -> dict:
    n_up, n_down = matrix.shape
    grand = float(matrix.mean())
    up_means = matrix.mean(axis=1)
    down_means = matrix.mean(axis=0)
    residual = matrix - up_means[:, None] - down_means[None, :] + grand
    ms_up = float(n_down * np.square(up_means - grand).sum() / (n_up - 1))
    ms_down = float(n_up * np.square(down_means - grand).sum() / (n_down - 1))
    ms_residual = float(np.square(residual).sum() / ((n_up - 1) * (n_down - 1)))
    return {
        "grand_mean": grand,
        "upstream_means": up_means.tolist(),
        "downstream_means": down_means.tolist(),
        "descriptive_variance_components": {
            "upstream": max(0.0, (ms_up - ms_residual) / n_down),
            "downstream": max(0.0, (ms_down - ms_residual) / n_up),
            "interaction_residual": ms_residual,
        },
        "mean_squares": {"upstream": ms_up, "downstream": ms_down, "interaction_residual": ms_residual},
        "boundary": "descriptive method-of-moments decomposition over five fixed upstream and five fixed downstream seeds",
    }


def clustered_interval(rows: list[dict], bootstrap_draws: int, seed: int) -> dict:
    documents = sorted({row["document"] for row in rows})
    cells = sorted({(row["upstream_seed"], row["downstream_seed"]) for row in rows})
    cell_index = {cell: index for index, cell in enumerate(cells)}
    doc_index = {doc: index for index, doc in enumerate(documents)}
    sums = np.zeros((len(documents), len(cells)), dtype=np.float64)
    counts = np.zeros((len(documents), len(cells)), dtype=np.int64)
    for row in rows:
        di = doc_index[row["document"]]
        ci = cell_index[(row["upstream_seed"], row["downstream_seed"])]
        sums[di, ci] += row["f1"]
        counts[di, ci] += 1
    if np.any(counts.sum(axis=0) != 1500):
        raise RuntimeError("each cell must contain exactly 1,500 claims")
    rng = np.random.default_rng(seed)
    draws = np.empty(bootstrap_draws, dtype=np.float64)
    for index in range(bootstrap_draws):
        sampled = rng.integers(0, len(documents), size=len(documents))
        per_cell = sums[sampled].sum(axis=0) / counts[sampled].sum(axis=0)
        draws[index] = per_cell.mean()
    point = float(sums.sum(axis=0).sum() / counts.sum(axis=0).sum())
    return {
        "point": point,
        "composition_interval_95": [float(np.quantile(draws, 0.025)), float(np.quantile(draws, 0.975))],
        "documents": len(documents),
        "cells": len(cells),
        "draws": bootstrap_draws,
        "seed": seed,
        "boundary": "document-composition sensitivity interval; not a population confidence interval",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    freeze = read_json(FREEZE)
    run_root = args.run_root.resolve()
    if not (run_root / "SUCCESS.json").is_file():
        raise RuntimeError("formal matrix has no SUCCESS.json")
    out = args.out.resolve()
    if out.exists():
        raise RuntimeError(f"refusing existing analysis output: {out}")
    out.mkdir(parents=True)

    all_rows = []
    ledgers = []
    for up in freeze["upstream_seeds"]:
        for down in freeze["downstream_seeds"]:
            rows, ledger = load_run(run_root / "runs" / f"up_{up}" / f"down_{down}", up, down, freeze["cutoffs"])
            all_rows.extend(rows)
            ledgers.append(ledger)

    grouped = defaultdict(list)
    for row in all_rows:
        grouped[(row["upstream_seed"], row["downstream_seed"], row["mode"], row["k"])].append(row["f1"])
    cells = []
    for (up, down, mode, k), values in sorted(grouped.items()):
        if len(values) != 1500:
            raise RuntimeError("cell cardinality mismatch")
        cells.append({"upstream_seed": up, "downstream_seed": down, "mode": mode, "k": k, "n": len(values), "mean_f1": float(np.mean(values))})
    write_csv(out / "cell_summary.csv", cells, ["upstream_seed", "downstream_seed", "mode", "k", "n", "mean_f1"])

    primary_cells = [row for row in cells if row["mode"] == "full" and row["k"] == freeze["primary_k"]]
    matrix = np.asarray(
        [[next(row["mean_f1"] for row in primary_cells if row["upstream_seed"] == up and row["downstream_seed"] == down) for down in freeze["downstream_seeds"]] for up in freeze["upstream_seeds"]],
        dtype=np.float64,
    )
    primary_rows = [row for row in all_rows if row["mode"] == "full" and row["k"] == freeze["primary_k"]]
    result = {
        "protocol_id": freeze["protocol_id"],
        "freeze_sha256": sha256(FREEZE),
        "run_success_sha256": sha256(run_root / "SUCCESS.json"),
        "prediction_ledgers": ledgers,
        "rows_loaded": len(all_rows),
        "primary": {
            "mode": "full",
            "k": freeze["primary_k"],
            "variance_decomposition": two_way_components(matrix),
            "document_clustered_composition_sensitivity": clustered_interval(
                primary_rows, int(freeze["analysis"]["bootstrap_draws"]), 20260806
            ),
        },
        "no_role_boundary": "The no_role mode is an inference ablation, not a separately retrained label-blind model.",
    }
    write_json(out / "results.json", result)
    write_json(
        out / "validation.json",
        {
            "status": "PASS",
            "ledgers": len(ledgers),
            "selected_rows": len(all_rows),
            "cells": len(cells),
            "primary_cells": len(primary_cells),
            "documents": result["primary"]["document_clustered_composition_sensitivity"]["documents"],
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
