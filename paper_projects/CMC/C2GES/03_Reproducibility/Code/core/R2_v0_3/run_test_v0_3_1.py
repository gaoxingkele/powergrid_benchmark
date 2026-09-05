"""Unauthorized-by-default one-attempt runner for C2GES v0.3.1.

The module may be imported for regression testing.  Formal test content is
decoded only after freeze verification, independent-audit verification,
hash-bound authorization, and an atomic durable attempt reservation.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
import os
import platform
import random
import re
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


def find_repository_root(start: Path) -> Path:
    """Find the workspace root without assuming the original archive layout."""
    configured = os.environ.get("C2GES_WORKSPACE_ROOT")
    if configured:
        root = Path(configured).resolve()
        if not root.is_dir():
            raise RuntimeError(f"C2GES_WORKSPACE_ROOT is not a directory: {root}")
        return root
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    for candidate in (start, *start.parents):
        if (candidate / "C2GES_RELEASE_MARKER.json").is_file():
            return candidate
    raise RuntimeError("repository root not found from script location")


REPO_ROOT = find_repository_root(R2)
R1 = R2.parent
if str(R1) not in sys.path:
    sys.path.insert(0, str(R1))

import run_formal_experiment as legacy_baselines
from v031_methods import build_graph_v03, constrained_select, redundancy, score_channels


CONDITIONS = (
    "lead", "centroid", "textrank", "semantic_mmr", "role",
    "graph_no_cf_strict", "c2ges_full",
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_json_atomic(path: Path, payload: object) -> None:
    temporary = path.with_name(path.name + f".tmp-{os.getpid()}")
    write_json(temporary, payload)
    os.replace(temporary, path)


def resolve_repo(relative: str) -> Path:
    candidate = (REPO_ROOT / Path(relative)).resolve()
    try:
        candidate.relative_to(REPO_ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"path escapes repository root: {relative}") from exc
    return candidate


def repo_relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def hash_tree(root: Path) -> dict[str, Any]:
    digest = hashlib.sha256()
    files = []
    for path in sorted(
        (item for item in root.rglob("*") if item.is_file()),
        key=lambda item: item.relative_to(root).as_posix(),
    ):
        relative = path.relative_to(root).as_posix()
        file_hash = sha256(path)
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(file_hash.encode("ascii"))
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
    channels = ("relevance", "role", "graph", "counterfactual", "position")
    if not math.isclose(sum(float(weights[name]) for name in channels), 1.0, abs_tol=1e-12):
        raise ValueError("full weights must sum to one")
    if tuple(config["primary_contrasts"]) != (
        "graph_no_cf_strict", "semantic_mmr", "textrank"
    ):
        raise ValueError("primary contrast family changed")
    if not config["semantic_model"].get("local_files_only"):
        raise ValueError("semantic model must be local-only")
    mmr_lambda = float(config["semantic_mmr"]["lambda"])
    if not 0.0 <= mmr_lambda <= 1.0:
        raise ValueError("Semantic-MMR lambda must be in [0,1]")
    if not math.isclose(float(config["semantic_mmr"]["relevance_weight"]), mmr_lambda):
        raise ValueError("Semantic-MMR relevance weight must equal lambda")
    if not math.isclose(float(config["semantic_mmr"]["redundancy_penalty"]), 1.0 - mmr_lambda):
        raise ValueError("Semantic-MMR redundancy penalty must equal 1-lambda")
    path_values = tuple(int(config[name]) for name in (
        "path_min_edges", "path_max_edges", "path_max_paths", "path_max_expansions"
    ))
    if path_values[0] < 2 or path_values[1] < path_values[0] or min(path_values[2:]) < 1:
        raise ValueError("invalid counterfactual path configuration")


def verify_freeze(freeze_path: Path) -> dict[str, Any]:
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    if freeze.get("path_resolution") != "repository_root":
        raise RuntimeError("freeze must declare repository_root path resolution")
    checks: dict[str, tuple[Any, Any]] = {}
    for section in ("bound_files", "code_files", "test_files"):
        for item in freeze[section]:
            checks[f"{section}:{item['path']}"] = (
                item["sha256"], sha256(resolve_repo(item["path"])),
            )
    lock_path = resolve_repo(freeze["runtime"]["dependency_lock_path"])
    checks["runtime:dependency_lock_file"] = (
        freeze["runtime"]["dependency_lock_sha256"], sha256(lock_path),
    )
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    checks["runtime:python"] = (lock["python"], platform.python_version())
    for package, expected in lock["packages"].items():
        try:
            actual = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            actual = None
        checks[f"runtime:{package}"] = (expected, actual)
    model = hash_tree(Path(freeze["semantic_model_snapshot"]["path"]))
    checks["semantic_model"] = (freeze["semantic_model_snapshot"]["sha256"], model["sha256"])
    ledger = {
        name: {
            "expected": expected,
            "actual": actual,
            "passed": str(expected).lower() == str(actual).lower(),
        }
        for name, (expected, actual) in checks.items()
    }
    failed = [name for name, row in ledger.items() if not row["passed"]]
    if failed:
        raise RuntimeError(f"freeze verification failed: {failed}")
    return {
        "freeze_sha256": sha256(freeze_path),
        "checks": ledger,
        "model_file_count": model["file_count"],
        "freeze": freeze,
    }


def verify_authorization(
    freeze_path: Path,
    freeze: Mapping[str, Any],
    authorization_path: Path,
    output: Path,
) -> dict[str, Any]:
    required = resolve_repo(freeze["authorization"]["artifact_path"])
    if authorization_path.resolve() != required:
        raise RuntimeError("authorization path is not the freeze-declared artifact")
    authorization = json.loads(authorization_path.read_text(encoding="utf-8"))
    freeze_hash = sha256(freeze_path)
    if authorization.get("authorized") is not True:
        raise RuntimeError("formal test is not explicitly authorized")
    if str(authorization.get("freeze_sha256", "")).upper() != freeze_hash:
        raise RuntimeError("authorization does not bind the current freeze hash")
    run_id = str(authorization.get("run_id", ""))
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{7,63}", run_id):
        raise RuntimeError("authorization run_id is missing or invalid")
    expected_relative = f"{freeze['run_control']['canonical_output_root'].rstrip('/')}/{run_id}"
    if authorization.get("output_path") != expected_relative:
        raise RuntimeError("authorization output path is not canonical for run_id")
    if output.resolve() != resolve_repo(expected_relative):
        raise RuntimeError("CLI output is not the authorized canonical output")
    audit_path = resolve_repo(str(authorization.get("audit_decision_path", "")))
    audit_hash = sha256(audit_path)
    if str(authorization.get("audit_decision_sha256", "")).upper() != audit_hash:
        raise RuntimeError("authorization audit-decision hash mismatch")
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    if audit.get("verdict") != "PASS" or str(audit.get("freeze_sha256", "")).upper() != freeze_hash:
        raise RuntimeError("independent pretest decision is not PASS for this freeze")
    if not str(authorization.get("approver", "")).strip() or not str(
        authorization.get("approved_at", "")
    ).strip():
        raise RuntimeError("authorization requires approver and approval timestamp")
    return authorization


def reserve_attempt(
    freeze: Mapping[str, Any], authorization: Mapping[str, Any], freeze_hash: str
) -> tuple[Path, dict[str, Any]]:
    registry = resolve_repo(freeze["run_control"]["registry_path"])
    try:
        registry.mkdir()
    except FileExistsError as exc:
        raise RuntimeError(
            f"durable run registry already exists; no additional attempt permitted: {registry}"
        ) from exc
    claim = {
        "status": "CLAIMED",
        "claimed_utc": now(),
        "run_id": authorization["run_id"],
        "freeze_sha256": freeze_hash,
        "authorization_sha256": sha256(resolve_repo(freeze["authorization"]["artifact_path"])),
        "output_path": authorization["output_path"],
        "pid": os.getpid(),
        "test_content_decoded": False,
    }
    claim_path = registry / "attempt.json"
    with claim_path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(claim, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    return claim_path, claim


def semantic_embeddings(nodes: Sequence[Any], model: Any) -> np.ndarray:
    return np.asarray(
        model.encode(
            [node.text for node in nodes],
            batch_size=32,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        ),
        dtype=float,
    )


def semantic_mmr_select(
    nodes: Sequence[Any], embeddings: np.ndarray, budget: int, mmr_lambda: float
) -> tuple[list[Any], dict[str, Any]]:
    """Greedy MMR using the same normalized MiniLM vectors for both terms."""
    nodes = list(nodes)
    if embeddings.shape[0] != len(nodes) or embeddings.ndim != 2:
        raise ValueError("embedding matrix does not align with sentence nodes")
    if not 0.0 <= mmr_lambda <= 1.0 or budget < 1:
        raise ValueError("invalid Semantic-MMR setting")
    budget = min(budget, len(nodes))
    centroid = embeddings.mean(axis=0)
    norm = float(np.linalg.norm(centroid))
    if norm:
        centroid = centroid / norm
    relevance = embeddings @ centroid
    similarity = embeddings @ embeddings.T
    selected: list[int] = []
    selection_audit = []
    while len(selected) < budget:
        candidates = []
        for index, node in enumerate(nodes):
            if index in selected:
                continue
            max_similarity = max((float(similarity[index, prior]) for prior in selected), default=0.0)
            adjusted = mmr_lambda * float(relevance[index]) - (1.0 - mmr_lambda) * max_similarity
            candidates.append((adjusted, -node.position, node.sid, index, max_similarity))
        adjusted, _, _, winner, max_similarity = max(candidates)
        selected.append(winner)
        selection_audit.append({
            "sid": nodes[winner].sid,
            "adjusted_score": adjusted,
            "centroid_relevance": float(relevance[winner]),
            "max_selected_cosine": max_similarity,
        })
    ordered = sorted((nodes[index] for index in selected), key=lambda node: node.position)
    return ordered, {
        "implementation": "local_MiniLM_Semantic_MMR",
        "lambda": mmr_lambda,
        "relevance_weight": mmr_lambda,
        "redundancy_penalty": 1.0 - mmr_lambda,
        "selection_order": [nodes[index].sid for index in selected],
        "steps": selection_audit,
    }


def choose(
    condition: str,
    graph: Any,
    channels: Mapping[str, Mapping[str, float]],
    embeddings: np.ndarray,
    config: Mapping[str, Any],
    budget: int,
) -> tuple[list[Any], dict]:
    if condition == "lead":
        return list(graph.nodes[:budget]), {"implementation": "document_order"}
    if condition == "centroid":
        scores = legacy_baselines.centroid_scores(graph.nodes)
        return legacy_baselines.top_k(graph.nodes, scores, budget), {
            "implementation": "lexical_centroid", "scores": scores
        }
    if condition == "textrank":
        scores, status = legacy_baselines.textrank_scores(graph.nodes, config["textrank"])
        return legacy_baselines.top_k(graph.nodes, scores, budget), {
            "implementation": "textrank", "status": status, "scores": scores
        }
    if condition == "semantic_mmr":
        return semantic_mmr_select(
            graph.nodes, embeddings, budget, float(config["semantic_mmr"]["lambda"])
        )
    if condition == "role":
        scores = channels["role"]
        return legacy_baselines.top_k(graph.nodes, scores, budget), {
            "implementation": "lexical_role_score", "scores": dict(scores)
        }
    selected, audit = constrained_select(
        graph,
        channels,
        config["c2ges_full_weights"],
        budget=budget,
        redundancy_penalty=float(config["redundancy_penalty"]),
        remove_cf_only=(condition == "graph_no_cf_strict"),
    )
    return selected, audit


def holm_adjust(records: list[dict]) -> None:
    ordered = sorted(
        range(len(records)),
        key=lambda index: (
            records[index]["p_two_sided_bootstrap"],
            records[index]["budget"],
            records[index]["contrast"],
        ),
    )
    running = 0.0
    total = len(records)
    for rank, index in enumerate(ordered):
        running = max(
            running,
            min(1.0, (total - rank) * records[index]["p_two_sided_bootstrap"]),
        )
        records[index]["p_holm"] = running
        records[index]["holm_family_size"] = total


def paired_bootstrap(
    predictions: Sequence[Mapping[str, Any]],
    budget: int,
    baseline: str,
    *,
    samples: int,
    seed: int,
) -> dict:
    by_key = {
        (row["doc_id"], row["condition"]): row["metrics"]["rougeL_f1"]
        for row in predictions if row["budget"] == budget
    }
    docs = sorted({doc for doc, _ in by_key})
    deltas = [float(by_key[(doc, "c2ges_full")]) - float(by_key[(doc, baseline)]) for doc in docs]
    rng = random.Random(seed)
    draws = [statistics.fmean(deltas[rng.randrange(len(deltas))] for _ in deltas) for _ in range(samples)]
    ordered = sorted(draws)
    return {
        "budget": budget,
        "contrast": f"c2ges_full_minus_{baseline}",
        "metric": "rougeL_f1",
        "n_reports": len(docs),
        "observed_mean_delta": statistics.fmean(deltas),
        "ci95_percentile": [
            ordered[math.floor(0.025 * (samples - 1))],
            ordered[math.ceil(0.975 * (samples - 1))],
        ],
        "p_two_sided_bootstrap": min(
            1.0,
            2.0 * min(
                sum(value <= 0 for value in draws) / samples,
                sum(value >= 0 for value in draws) / samples,
            ),
        ),
        "samples": samples,
        "seed": seed,
        "resampling_unit": "report",
    }


def run(
    config_path: Path,
    freeze_path: Path,
    test_path: Path,
    authorization_path: Path,
    output: Path,
) -> dict:
    verification = verify_freeze(freeze_path)
    freeze = verification.pop("freeze")
    if config_path.resolve() != resolve_repo(freeze["artifacts"]["config_path"]):
        raise RuntimeError("CLI config is not the frozen config")
    if test_path.resolve() != resolve_repo(freeze["datasets"]["test_path"]):
        raise RuntimeError("CLI test path is not the frozen test dataset")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    validate_config(config)
    authorization = verify_authorization(
        freeze_path, freeze, authorization_path, output
    )
    claim_path, claim = reserve_attempt(
        freeze, authorization, verification["freeze_sha256"]
    )
    if output.exists():
        failure = {**claim, "status": "FAILED", "failed_utc": now(), "error": "authorized output already exists"}
        write_json_atomic(claim_path, failure)
        raise FileExistsError(f"refusing existing authorized output: {output}")
    output.mkdir(parents=True)
    state = output / "run_state.json"
    write_json(state, {"status": "RUNNING", "started_utc": now(), "run_id": authorization["run_id"]})
    try:
        rows = jsonl(test_path)
        claim["test_content_decoded"] = True
        claim["content_decoded_utc"] = now()
        write_json_atomic(claim_path, claim)
        if len(rows) != 15 or any(row.get("split") != "test" for row in rows):
            raise RuntimeError("requires physically test-only 15-report build08 file")
        model = SentenceTransformer(
            config["semantic_model"]["snapshot_path"],
            device="cpu",
            local_files_only=True,
        )
        scorer = rouge_scorer.RougeScorer(
            ["rouge1", "rouge2", "rougeL"],
            use_stemmer=bool(config["rouge_use_stemmer"]),
        )
        predictions = []
        for row in rows:
            graph = build_graph_v03(
                row["candidate_sentences"], max_distance=int(config["max_distance"])
            )
            channels = score_channels(
                graph,
                path_min_edges=int(config["path_min_edges"]),
                path_max_edges=int(config["path_max_edges"]),
                path_max_paths=int(config["path_max_paths"]),
                path_max_expansions=int(config["path_max_expansions"]),
            )
            embeddings = semantic_embeddings(graph.nodes, model)
            for budget in config["selection_budgets"]:
                for condition in CONDITIONS:
                    selected, audit = choose(
                        condition, graph, channels, embeddings, config, int(budget)
                    )
                    prediction = " ".join(node.text for node in selected)
                    scores = scorer.score(row["reference_summary"], prediction)
                    predictions.append({
                        "doc_id": row["doc_id"],
                        "split": "test",
                        "budget": budget,
                        "condition": condition,
                        "selected_sentence_ids": [node.sid for node in selected],
                        "selected_sentences": [node.text for node in selected],
                        "prediction": prediction,
                        "metrics": {
                            "rouge1_f1": float(scores["rouge1"].fmeasure),
                            "rouge2_f1": float(scores["rouge2"].fmeasure),
                            "rougeL_f1": float(scores["rougeL"].fmeasure),
                            "redundancy": redundancy(selected),
                        },
                        "selection_audit": audit,
                    })
        with (output / "predictions.jsonl").open("w", encoding="utf-8", newline="\n") as stream:
            for row in predictions:
                stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        aggregate = {}
        for budget in config["selection_budgets"]:
            aggregate[str(budget)] = {}
            for condition in CONDITIONS:
                subset = [
                    row for row in predictions
                    if row["budget"] == budget and row["condition"] == condition
                ]
                aggregate[str(budget)][condition] = {
                    metric: statistics.fmean(row["metrics"][metric] for row in subset)
                    for metric in ("rouge1_f1", "rouge2_f1", "rougeL_f1", "redundancy")
                }
        write_json(output / "aggregate_metrics.json", aggregate)
        primary = [
            paired_bootstrap(
                predictions,
                budget,
                baseline,
                samples=int(config["bootstrap_samples"]),
                seed=int(config["bootstrap_seed"]) + 100 * budget + index,
            )
            for budget in (5, 10)
            for index, baseline in enumerate(config["primary_contrasts"])
        ]
        holm_adjust(primary)
        write_json(output / "primary_contrasts_holm.json", primary)
        manifest = {
            "status": "COMPLETE",
            "protocol": config["protocol"],
            "run_id": authorization["run_id"],
            "test_report_count": 15,
            "prediction_row_count": len(predictions),
            "one_attempt_corrective_execution": True,
            "freeze_verification": verification,
            "authorization_sha256": sha256(authorization_path),
            "artifacts": {
                name: sha256(output / name)
                for name in (
                    "predictions.jsonl", "aggregate_metrics.json", "primary_contrasts_holm.json"
                )
            },
        }
        write_json(output / "manifest.json", manifest)
        write_json(state, {"status": "COMPLETE", "completed_utc": now(), "run_id": authorization["run_id"]})
        write_json_atomic(claim_path, {
            **claim,
            "status": "COMPLETE",
            "completed_utc": now(),
            "output_manifest_sha256": sha256(output / "manifest.json"),
        })
        return manifest
    except Exception as exc:
        failure = {
            "status": "FAILED",
            "run_id": authorization["run_id"],
            "failed_utc": now(),
            "error_type": type(exc).__name__,
            "error": str(exc),
            "traceback": traceback.format_exc(),
        }
        write_json(output / "failure.json", failure)
        write_json(state, failure)
        write_json_atomic(claim_path, {**claim, **failure})
        raise


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--freeze", type=Path, required=True)
    parser.add_argument("--test", type=Path, required=True)
    parser.add_argument("--authorization", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(
        args.config.resolve(),
        args.freeze.resolve(),
        args.test.resolve(),
        args.authorization.resolve(),
        args.output.resolve(),
    ), indent=2))


if __name__ == "__main__":
    main()
