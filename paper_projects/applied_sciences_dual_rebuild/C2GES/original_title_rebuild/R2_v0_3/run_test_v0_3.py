"""Frozen one-shot test runner for the C2GES v0.3 corrective evaluation."""

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

R2 = Path(__file__).resolve().parent
R1 = R2.parent
if str(R1) not in sys.path:
    sys.path.insert(0, str(R1))

import run_formal_experiment as legacy_baselines
from build_full_pdf_dataset import sha256
from v03_methods import build_graph_v03, constrained_select, redundancy, score_channels


CONDITIONS = (
    "lead", "centroid", "textrank", "semantic_centroid", "role",
    "graph_no_cf_strict", "c2ges_full",
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def hash_tree(root: Path) -> dict[str, Any]:
    digest = hashlib.sha256()
    files = []
    for path in sorted((item for item in root.rglob("*") if item.is_file()), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        file_hash = sha256(path)
        digest.update(relative.encode("utf-8")); digest.update(b"\0"); digest.update(file_hash.encode("ascii"))
        files.append({"path": relative, "sha256": file_hash, "bytes": path.stat().st_size})
    if not files:
        raise ValueError("semantic model snapshot contains no files")
    return {"sha256": digest.hexdigest().upper(), "file_count": len(files), "files": files}


def validate_config(config: Mapping[str, Any]) -> None:
    if tuple(config["conditions"]) != CONDITIONS:
        raise ValueError("condition order changed")
    if tuple(config["selection_budgets"]) != (5, 10):
        raise ValueError("budgets must be [5, 10]")
    weights = config["c2ges_full_weights"]
    if not math.isclose(sum(float(weights[name]) for name in ("relevance", "role", "graph", "counterfactual", "position")), 1.0, abs_tol=1e-12):
        raise ValueError("full weights must sum to one")
    if tuple(config["primary_contrasts"]) != ("graph_no_cf_strict", "semantic_centroid", "textrank"):
        raise ValueError("primary contrast family changed")
    if not config["semantic_model"].get("local_files_only"):
        raise ValueError("semantic model must be local-only")


def verify_freeze(freeze_path: Path, config_path: Path, test_path: Path) -> dict[str, Any]:
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    checks = {
        "config": (freeze["artifacts"]["config_sha256"], sha256(config_path)),
        "test_dataset": (freeze["datasets"]["test_sha256"], sha256(test_path)),
        "dev_decision": (freeze["development"]["decision_sha256"], sha256(Path(freeze["development"]["decision_path"]))),
    }
    for item in freeze["bound_files"]:
        checks[f"bound:{item['path']}"] = (item["sha256"], sha256(Path(item["path"])))
    for item in freeze["code_files"]:
        checks[f"code:{item['path']}"] = (item["sha256"], sha256(Path(item["path"])))
    checks["runtime:python"] = (freeze["runtime"]["python"], platform.python_version())
    for package, expected in freeze["runtime"]["packages"].items():
        try:
            actual = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            actual = None
        checks[f"runtime:{package}"] = (expected, actual)
    model = hash_tree(Path(freeze["semantic_model_snapshot"]["path"]))
    checks["semantic_model"] = (freeze["semantic_model_snapshot"]["sha256"], model["sha256"])
    ledger = {name: {"expected": expected, "actual": actual, "passed": str(expected).lower() == str(actual).lower()} for name, (expected, actual) in checks.items()}
    failed = [name for name, row in ledger.items() if not row["passed"]]
    if failed:
        raise RuntimeError(f"freeze verification failed: {failed}")
    return {"freeze_sha256": sha256(freeze_path), "checks": ledger, "model_file_count": model["file_count"]}


def semantic_centroid_scores(nodes: Sequence[Any], model: Any) -> dict[str, float]:
    embeddings = np.asarray(model.encode([node.text for node in nodes], batch_size=32, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False), dtype=float)
    centroid = embeddings.mean(axis=0)
    norm = float(np.linalg.norm(centroid))
    if norm:
        centroid /= norm
    scaled = legacy_baselines.minmax((embeddings @ centroid).tolist())
    return {node.sid: value for node, value in zip(nodes, scaled)}


def choose(condition: str, graph: Any, channels: Mapping[str, Mapping[str, float]], semantic: Mapping[str, float], config: Mapping[str, Any], budget: int) -> tuple[list[Any], dict]:
    if condition == "lead":
        selected = list(graph.nodes[:budget]); return selected, {"implementation": "document_order"}
    if condition == "centroid":
        scores = legacy_baselines.centroid_scores(graph.nodes)
        return legacy_baselines.top_k(graph.nodes, scores, budget), {"implementation": "lexical_centroid", "scores": scores}
    if condition == "textrank":
        scores, status = legacy_baselines.textrank_scores(graph.nodes, config["textrank"])
        return legacy_baselines.top_k(graph.nodes, scores, budget), {"implementation": "textrank", "status": status, "scores": scores}
    if condition == "semantic_centroid":
        return legacy_baselines.top_k(graph.nodes, semantic, budget), {"implementation": "local_MiniLM_semantic_centroid", "scores": dict(semantic)}
    if condition == "role":
        scores = channels["role"]
        return legacy_baselines.top_k(graph.nodes, scores, budget), {"implementation": "lexical_role_score", "scores": dict(scores)}
    selected, audit = constrained_select(
        graph, channels, config["c2ges_full_weights"], budget=budget,
        redundancy_penalty=float(config["redundancy_penalty"]),
        remove_cf_only=(condition == "graph_no_cf_strict"),
    )
    return selected, audit


def holm_adjust(records: list[dict]) -> None:
    ordered = sorted(range(len(records)), key=lambda index: (records[index]["p_two_sided_bootstrap"], records[index]["budget"], records[index]["contrast"]))
    running = 0.0; total = len(records)
    for rank, index in enumerate(ordered):
        running = max(running, min(1.0, (total - rank) * records[index]["p_two_sided_bootstrap"]))
        records[index]["p_holm"] = running
        records[index]["holm_family_size"] = total


def paired_bootstrap(predictions: Sequence[Mapping[str, Any]], budget: int, baseline: str, *, samples: int, seed: int) -> dict:
    by_key = {(row["doc_id"], row["condition"]): row["metrics"]["rougeL_f1"] for row in predictions if row["budget"] == budget}
    docs = sorted({doc for doc, _ in by_key})
    deltas = [float(by_key[(doc, "c2ges_full")]) - float(by_key[(doc, baseline)]) for doc in docs]
    rng = random.Random(seed)
    draws = [statistics.fmean(deltas[rng.randrange(len(deltas))] for _ in deltas) for _ in range(samples)]
    ordered = sorted(draws)
    return {
        "budget": budget, "contrast": f"c2ges_full_minus_{baseline}", "metric": "rougeL_f1",
        "n_reports": len(docs), "observed_mean_delta": statistics.fmean(deltas),
        "ci95_percentile": [ordered[math.floor(0.025 * (samples - 1))], ordered[math.ceil(0.975 * (samples - 1))]],
        "p_two_sided_bootstrap": min(1.0, 2.0 * min(sum(value <= 0 for value in draws) / samples, sum(value >= 0 for value in draws) / samples)),
        "samples": samples, "seed": seed, "resampling_unit": "report",
    }


def run(config_path: Path, freeze_path: Path, test_path: Path, output: Path) -> dict:
    if output.exists():
        raise FileExistsError(f"refusing existing output: {output}")
    output.mkdir(parents=True)
    state = output / "run_state.json"; write_json(state, {"status": "RUNNING", "started_utc": now()})
    try:
        config = json.loads(config_path.read_text(encoding="utf-8")); validate_config(config)
        verification = verify_freeze(freeze_path, config_path, test_path)
        rows = jsonl(test_path)
        if len(rows) != 15 or any(row.get("split") != "test" for row in rows):
            raise RuntimeError("requires physically test-only 15-report build08 file")
        model = SentenceTransformer(config["semantic_model"]["snapshot_path"], device="cpu", local_files_only=True)
        scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
        predictions = []
        for row in rows:
            graph = build_graph_v03(row["candidate_sentences"], max_distance=int(config["max_distance"]))
            channels = score_channels(graph, path_max_edges=int(config["path_max_edges"]))
            semantic = semantic_centroid_scores(graph.nodes, model)
            for budget in config["selection_budgets"]:
                for condition in CONDITIONS:
                    selected, audit = choose(condition, graph, channels, semantic, config, int(budget))
                    prediction = " ".join(node.text for node in selected)
                    scores = scorer.score(row["reference_summary"], prediction)
                    predictions.append({
                        "doc_id": row["doc_id"], "split": "test", "budget": budget, "condition": condition,
                        "selected_sentence_ids": [node.sid for node in selected], "selected_sentences": [node.text for node in selected],
                        "prediction": prediction, "metrics": {"rouge1_f1": float(scores["rouge1"].fmeasure), "rouge2_f1": float(scores["rouge2"].fmeasure), "rougeL_f1": float(scores["rougeL"].fmeasure), "redundancy": redundancy(selected)},
                        "selection_audit": audit,
                    })
        with (output / "predictions.jsonl").open("w", encoding="utf-8", newline="\n") as stream:
            for row in predictions: stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        aggregate = {}
        for budget in config["selection_budgets"]:
            aggregate[str(budget)] = {}
            for condition in CONDITIONS:
                subset = [row for row in predictions if row["budget"] == budget and row["condition"] == condition]
                aggregate[str(budget)][condition] = {metric: statistics.fmean(row["metrics"][metric] for row in subset) for metric in ("rouge1_f1", "rouge2_f1", "rougeL_f1", "redundancy")}
        write_json(output / "aggregate_metrics.json", aggregate)
        primary = [paired_bootstrap(predictions, budget, baseline, samples=int(config["bootstrap_samples"]), seed=int(config["bootstrap_seed"]) + 100 * budget + index) for budget in (5, 10) for index, baseline in enumerate(config["primary_contrasts"])]
        holm_adjust(primary); write_json(output / "primary_contrasts_holm.json", primary)
        manifest = {"status": "COMPLETE", "protocol": config["protocol"], "test_report_count": 15, "prediction_row_count": len(predictions), "one_shot_corrective_execution": True, "freeze_verification": verification, "artifacts": {name: sha256(output / name) for name in ("predictions.jsonl", "aggregate_metrics.json", "primary_contrasts_holm.json")}}
        write_json(output / "manifest.json", manifest); write_json(state, {"status": "COMPLETE", "completed_utc": now()})
        return manifest
    except Exception as exc:
        failure = {"status": "FAILED", "failed_utc": now(), "error_type": type(exc).__name__, "error": str(exc), "traceback": traceback.format_exc()}
        write_json(output / "failure.json", failure); write_json(state, failure); raise


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--config", type=Path, required=True); parser.add_argument("--freeze", type=Path, required=True); parser.add_argument("--test", type=Path, required=True); parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(); print(json.dumps(run(args.config.resolve(), args.freeze.resolve(), args.test.resolve(), args.output.resolve()), indent=2))


if __name__ == "__main__":
    main()
