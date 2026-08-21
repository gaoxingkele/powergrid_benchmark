"""Frozen v0.2 C2GES run: strict CF ablation, K sensitivity, semantic baseline.

This module imports, but does not modify, the frozen v0.1 primitives.  It uses a
fully local MiniLM snapshot and never permits a model download.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
import platform
import random
import statistics
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer

import run_formal_experiment as v01
from c2ges_offline import CausalEventGraph


ROOT = Path(__file__).resolve().parents[4]
CONDITIONS = (
    "lead",
    "centroid",
    "textrank",
    "semantic_centroid",
    "role",
    "graph_no_cf_strict",
    "c2ges_full",
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    return v01.sha256(path)


def write_json(path: Path, payload: object) -> None:
    v01.write_json(path, payload)


def hash_tree(root: Path) -> dict[str, Any]:
    if not root.is_dir():
        raise FileNotFoundError(f"model snapshot not found: {root}")
    digest = hashlib.sha256()
    files = []
    for path in sorted((path for path in root.rglob("*") if path.is_file()), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        file_hash = sha256(path)
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(file_hash.encode("ascii"))
        files.append({"path": relative, "sha256": file_hash, "bytes": path.stat().st_size})
    if not files:
        raise ValueError(f"model snapshot contains no files: {root}")
    return {"sha256": digest.hexdigest(), "file_count": len(files), "files": files}


def validate_config(config: Mapping[str, Any]) -> None:
    if tuple(config.get("conditions", ())) != CONDITIONS:
        raise ValueError(f"conditions must be exactly {CONDITIONS}")
    if tuple(config.get("selection_budgets", ())) != (5, 10):
        raise ValueError("selection_budgets must be exactly [5, 10]")
    full = config["c2ges_full_weights"]
    strict = config["graph_no_cf_strict_weights"]
    keys = ("relevance", "role", "graph", "counterfactual", "position")
    if not math.isclose(sum(float(full[key]) for key in keys), 1.0, abs_tol=1e-12):
        raise ValueError("full channel weights must sum to one")
    if float(strict["counterfactual"]) != 0.0:
        raise ValueError("strict no-CF counterfactual weight must be zero")
    retained = sum(float(full[key]) for key in keys if key != "counterfactual")
    for key in keys:
        expected = 0.0 if key == "counterfactual" else float(full[key]) / retained
        if not math.isclose(float(strict[key]), expected, abs_tol=1e-12):
            raise ValueError(f"strict no-CF weight for {key} is not proportional to full")
    if float(strict["redundancy_penalty"]) != float(full["redundancy_penalty"]):
        raise ValueError("strict no-CF must retain the full redundancy penalty")
    if not bool(config["semantic_model"].get("local_files_only")):
        raise ValueError("semantic model must be local-files-only")


def verify_freeze(freeze_path: Path, config_path: Path, dataset_path: Path) -> dict[str, Any]:
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    checks: dict[str, dict[str, Any]] = {
        "config": {"expected": freeze["config_sha256"], "actual": sha256(config_path)},
        "dataset": {"expected": freeze["dataset_sha256"], "actual": sha256(dataset_path)},
    }
    for item in freeze["code_files"]:
        path = ROOT / item["path"]
        checks[item["path"]] = {"expected": item["sha256"], "actual": sha256(path) if path.is_file() else None}
    runtime = freeze["runtime"]
    checks["runtime:python"] = {"expected": runtime["python"], "actual": platform.python_version()}
    for package, expected in runtime["packages"].items():
        try:
            actual = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            actual = None
        checks[f"runtime:{package}"] = {"expected": expected, "actual": actual}
    model_root = Path(freeze["semantic_model_snapshot"]["path"])
    model_inventory = hash_tree(model_root)
    checks["semantic_model_snapshot"] = {
        "expected": freeze["semantic_model_snapshot"]["sha256"],
        "actual": model_inventory["sha256"],
    }
    failures = []
    for name, check in checks.items():
        check["passed"] = str(check["expected"]).lower() == str(check["actual"]).lower()
        if not check["passed"]:
            failures.append(name)
    if failures:
        raise RuntimeError(f"freeze verification failed: {failures}")
    return {
        "freeze_sha256": sha256(freeze_path),
        "checks": checks,
        "model_inventory": model_inventory,
    }


def semantic_centroid_scores(nodes: Sequence[Any], model: Any) -> dict[str, float]:
    embeddings = np.asarray(
        model.encode(
            [node.text for node in nodes],
            batch_size=32,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        ),
        dtype=float,
    )
    centroid = embeddings.mean(axis=0)
    norm = float(np.linalg.norm(centroid))
    if norm > 0:
        centroid = centroid / norm
    scores = embeddings @ centroid
    scaled = v01.minmax(scores.tolist())
    return {node.sid: value for node, value in zip(nodes, scaled)}


def selected_for_condition(
    condition: str,
    graph: CausalEventGraph,
    config: Mapping[str, Any],
    budget: int,
    semantic_scores: Mapping[str, float],
) -> tuple[list[Any], dict[str, Any]]:
    local = dict(config)
    local["selection_budget"] = budget
    local["graph_no_cf_weights"] = config["graph_no_cf_strict_weights"]
    if condition == "semantic_centroid":
        return v01.top_k(graph.nodes, semantic_scores, min(budget, len(graph.nodes))), {
            "implementation": "local_all_MiniLM_L6_v2_semantic_centroid",
            "scores": dict(semantic_scores),
        }
    translated = "graph_no_cf" if condition == "graph_no_cf_strict" else condition
    return v01.select_condition(translated, graph, local)


def evaluate_document(row: Mapping[str, Any], config: Mapping[str, Any], scorer: Any, model: Any) -> list[dict[str, Any]]:
    graph = CausalEventGraph.from_sentences(row["candidate_sentences"], row.get("silver_role_evidence", {}))
    semantic_scores = semantic_centroid_scores(graph.nodes, model)
    outputs = []
    for budget in config["selection_budgets"]:
        for condition in CONDITIONS:
            selected, audit = selected_for_condition(condition, graph, config, int(budget), semantic_scores)
            prediction = " ".join(node.text for node in selected)
            rouge = scorer.score(str(row["reference_summary"]), prediction)
            coverage, by_role = v01.silver_role_coverage(
                {node.sid for node in selected}, row.get("silver_role_evidence", {})
            )
            outputs.append({
                "doc_id": row["doc_id"],
                "split": row["split"],
                "budget": int(budget),
                "condition": condition,
                "selected_sentence_ids": [node.sid for node in selected],
                "selected_sentences": [node.text for node in selected],
                "prediction": prediction,
                "reference_provenance": row["reference_provenance"],
                "silver_label_provenance": row["silver_label_provenance"],
                "metrics": {
                    "rouge1_f1": float(rouge["rouge1"].fmeasure),
                    "rouge2_f1": float(rouge["rouge2"].fmeasure),
                    "rougeL_f1": float(rouge["rougeL"].fmeasure),
                    "silver_role_coverage": float(coverage),
                    "redundancy": float(v01.redundancy(selected)),
                },
                "silver_role_hits": by_role,
                "selection_audit": audit,
            })
    return outputs


def aggregate(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    metrics = ("rouge1_f1", "rouge2_f1", "rougeL_f1", "silver_role_coverage", "redundancy")
    result = {}
    for budget in (5, 10):
        result[str(budget)] = {}
        for condition in CONDITIONS:
            subset = [row for row in rows if row["budget"] == budget and row["condition"] == condition]
            result[str(budget)][condition] = {
                "n_reports": len(subset),
                **{metric: statistics.fmean(float(row["metrics"][metric]) for row in subset) for metric in metrics},
            }
    return result


def paired_bootstrap(
    rows: Sequence[Mapping[str, Any]], budget: int, baseline: str, metric: str, *, samples: int, seed: int
) -> dict[str, Any]:
    subset = [row for row in rows if row["budget"] == budget]
    by_key = {(row["doc_id"], row["condition"]): float(row["metrics"][metric]) for row in subset}
    docs = sorted({row["doc_id"] for row in subset})
    deltas = [by_key[(doc, "c2ges_full")] - by_key[(doc, baseline)] for doc in docs]
    rng = random.Random(seed)
    draws = [statistics.fmean(deltas[rng.randrange(len(deltas))] for _ in deltas) for _ in range(samples)]
    ordered = sorted(draws)
    lower = ordered[math.floor(0.025 * (samples - 1))]
    upper = ordered[math.ceil(0.975 * (samples - 1))]
    return {
        "budget": budget,
        "contrast": f"c2ges_full_minus_{baseline}",
        "metric": metric,
        "n_reports": len(docs),
        "observed_mean_delta": statistics.fmean(deltas),
        "ci95_percentile": [lower, upper],
        "p_two_sided_bootstrap": min(
            1.0,
            2.0 * min(sum(value <= 0 for value in draws) / samples, sum(value >= 0 for value in draws) / samples),
        ),
        "samples": samples,
        "seed": seed,
        "resampling_unit": "report",
    }


def run(config_path: Path, freeze_path: Path, dataset_path: Path, output_dir: Path) -> dict[str, Any]:
    if output_dir.exists():
        raise FileExistsError(f"output directory already exists: {output_dir}")
    output_dir.mkdir(parents=True)
    state = output_dir / "run_state.json"
    write_json(state, {"status": "RUNNING", "started_utc": now()})
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
        validate_config(config)
        verification = verify_freeze(freeze_path, config_path, dataset_path)
        dataset = v01.load_jsonl(dataset_path)
        test_rows = sorted((row for row in dataset if row.get("split") == "test"), key=lambda row: row["doc_id"])
        if not test_rows:
            raise ValueError("dataset contains no test reports")
        model_path = Path(config["semantic_model"]["snapshot_path"])
        model = SentenceTransformer(str(model_path), device=config["semantic_model"]["device"], local_files_only=True)
        scorer = rouge_scorer.RougeScorer(
            ["rouge1", "rouge2", "rougeL"], use_stemmer=bool(config["rouge_use_stemmer"])
        )
        predictions = []
        for row in test_rows:
            predictions.extend(evaluate_document(row, config, scorer, model))
        predictions_path = output_dir / "predictions.jsonl"
        with predictions_path.open("w", encoding="utf-8", newline="\n") as handle:
            for row in predictions:
                handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        write_json(output_dir / "aggregate_metrics.json", aggregate(predictions))
        bootstrap = [
            paired_bootstrap(
                predictions,
                budget,
                baseline,
                metric,
                samples=int(config["bootstrap_samples"]),
                seed=int(config["bootstrap_seed"]) + budget * 100 + baseline_index * 10 + metric_index,
            )
            for budget in config["selection_budgets"]
            for baseline_index, baseline in enumerate(CONDITIONS[:-1])
            for metric_index, metric in enumerate(("rouge1_f1", "rouge2_f1", "rougeL_f1"))
        ]
        write_json(output_dir / "paired_bootstrap.json", bootstrap)
        started = json.loads(state.read_text(encoding="utf-8"))["started_utc"]
        manifest = {
            "protocol": config["protocol"],
            "status": "COMPLETE",
            "started_utc": started,
            "completed_utc": now(),
            "offline_only": True,
            "test_report_count": len(test_rows),
            "conditions": list(CONDITIONS),
            "budgets": list(config["selection_budgets"]),
            "prediction_row_count": len(predictions),
            "strict_cf_ablation": True,
            "semantic_model": config["semantic_model"],
            "silver_label_boundary": "machine_verified_candidate_not_human_or_expert_gold",
            "runtime": {"python": sys.version, "platform": platform.platform()},
            "freeze_verification": verification,
            "artifacts": {
                name: sha256(output_dir / name)
                for name in ("predictions.jsonl", "aggregate_metrics.json", "paired_bootstrap.json")
            },
        }
        write_json(output_dir / "manifest.json", manifest)
        write_json(state, {"status": "COMPLETE", "started_utc": started, "completed_utc": manifest["completed_utc"]})
        return manifest
    except Exception as exc:
        failure = {
            "status": "FAILED",
            "failed_utc": now(),
            "error_type": type(exc).__name__,
            "error": str(exc),
            "traceback": traceback.format_exc(),
        }
        write_json(output_dir / "failure.json", failure)
        write_json(state, failure)
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--freeze", type=Path, required=True)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = run(args.config.resolve(), args.freeze.resolve(), args.dataset.resolve(), args.output.resolve())
    print(json.dumps({key: manifest[key] for key in ("status", "test_report_count", "prediction_row_count")}, indent=2))


if __name__ == "__main__":
    main()
