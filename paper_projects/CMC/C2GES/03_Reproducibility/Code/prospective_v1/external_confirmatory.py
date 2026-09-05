#!/usr/bin/env python3
"""One-attempt, hash-bound external E1/E3 runner for C2GES.

The entry point is intentionally unusable with the protocol-ready draft.  It
requires a separately authored authorization record binding frozen protocols,
configuration, tuning decision, rights-safe inventory, private dataset, code,
model snapshot, output directory, and durable attempt registry.  The attempt is
claimed atomically before the private external dataset is opened.

No network access is performed.  Public outputs contain identifiers, page
locators, metrics, hashes, and diagnostics but no candidate/reference text.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
import math
import os
import platform
import re
import statistics
import sys
import time
import tracemalloc
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import networkx as nx
import numpy as np
import psutil
from rouge_score import rouge_scorer

from experiment import (
    CONDITIONS,
    analyze as analyze_factorial,
    contrast_summary,
    holm,
    role_coverage,
    select_word_budget as select_c2ges_word_budget,
    sha256,
    typed_edge_coverage,
    untyped_graph_signal,
    word_count,
)
from pacsum_minilm import pacsum_scores


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
WORKSPACE = PROJECT.parents[2]
CORE_ROOT = PROJECT / "03_Reproducibility/Code/core"
CORE = CORE_ROOT / "R2_v0_3"
for import_root in (CORE_ROOT, CORE):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from v031_methods import RedundancyCache, build_graph_v03, score_channels  # noqa: E402


SCHEMA = "c2ges-external-confirmatory-authorization-v1"
MODE = "EXTERNAL_CONFIRMATORY_ONE_ATTEMPT"
METHODS = (
    "Lead",
    "Centroid",
    "TextRank",
    "Semantic-MMR",
    "Role-only",
    "C2GES-NO-PATH",
    "C2GES-FULL",
    "PacSum-MiniLM",
)
PUBLIC_E1_FILES = (
    "rights_safe_external_metadata.csv",
    "layout_candidate_audit.csv",
    "layout_candidate_audit_summary.json",
    "balanced_tuning_grid.csv",
    "TUNING_DECISION.json",
    "external_item_metrics.csv",
    "external_aggregate_metrics.csv",
    "external_paired_contrasts.csv",
    "external_series_cluster_results.json",
    "external_loso.csv",
    "selected_page_locator.csv",
    "RUN_MANIFEST.json",
)
PUBLIC_E3_FILES = (
    "ablation_config_registry.json",
    "factorial_item_metrics.csv",
    "factorial_aggregate_metrics.csv",
    "factorial_series_effects.csv",
    "factorial_interactions.json",
    "factorial_selection_jaccard.csv",
    "factorial_runtime_resources.csv",
    "FACTORIAL_REPORT.md",
)
REQUIRED_CODE_FILES = {
    "paper_projects/CMC/C2GES/03_Reproducibility/Code/prospective_v1/external_confirmatory.py",
    "paper_projects/CMC/C2GES/03_Reproducibility/Code/prospective_v1/experiment.py",
    "paper_projects/CMC/C2GES/03_Reproducibility/Code/prospective_v1/pacsum_minilm.py",
    "paper_projects/CMC/C2GES/03_Reproducibility/Code/core/c2ges_offline.py",
    "paper_projects/CMC/C2GES/03_Reproducibility/Code/core/R2_v0_3/v03_methods.py",
    "paper_projects/CMC/C2GES/03_Reproducibility/Code/core/R2_v0_3/v031_methods.py",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8-sig") as stream:
        for number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"JSONL line {number} is not an object")
            rows.append(row)
    return rows


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path.name}")
    fields = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def resolve_bound_path(value: str, *, base: Path = WORKSPACE) -> Path:
    path = Path(value)
    return path.resolve() if path.is_absolute() else (base / path).resolve()


def verify_hash(path: Path, expected: str, label: str) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"{label} is missing: {path}")
    actual = sha256(path)
    if actual != str(expected).upper():
        raise RuntimeError(f"{label} hash mismatch: expected {expected}, found {actual}")


def validate_config(config: Mapping[str, Any]) -> None:
    if config.get("mode") != MODE or config.get("status") != "FROZEN":
        raise ValueError("formal config must be FROZEN in external confirmatory mode")
    if config.get("execution_allowed") is not True or config.get("external_test_accessed") is not False:
        raise ValueError("formal config must authorize execution while recording no external-test access")
    if config.get("word_budgets") != [110, 260]:
        raise ValueError("formal word budgets must be exactly [110, 260]")
    if tuple(config.get("methods", ())) != METHODS:
        raise ValueError(f"formal methods must be exactly {METHODS}")
    if config.get("recommended_method") not in {"C2GES-NO-PATH", "C2GES-FULL"}:
        raise ValueError("recommended_method must be frozen before external access")
    if config.get("long_unit_policy") not in {"production_256", "chunk_mean_254"}:
        raise ValueError("long_unit_policy must be frozen")
    if not re.fullmatch(r"[0-9a-f]{40}", str(config.get("model_revision", "")), re.I):
        raise ValueError("model_revision must be a frozen 40-hex revision")
    if int(config.get("bootstrap_samples", 0)) < 10000:
        raise ValueError("at least 10000 cluster-bootstrap samples are required")
    if not isinstance(config.get("bootstrap_seed"), int):
        raise ValueError("bootstrap_seed must be an integer")
    weight_keys = {"relevance", "role", "graph", "path", "position"}
    if set(config.get("base_positive_weights", {})) != weight_keys:
        raise ValueError(f"base positive weights require exactly {sorted(weight_keys)}")
    if not math.isclose(sum(float(value) for value in config["base_positive_weights"].values()), 1.0, abs_tol=1e-9):
        raise ValueError("base positive weights must sum to one")
    if not 0.0 <= float(config["semantic_mmr_lambda"]) <= 1.0:
        raise ValueError("semantic_mmr_lambda must lie in [0,1]")
    if not 0.0 < float(config["textrank_alpha"]) < 1.0:
        raise ValueError("textrank_alpha must lie in (0,1)")
    pacsum = config.get("pacsum", {})
    if set(pacsum) != {"lambda_preceding", "lambda_following", "beta"}:
        raise ValueError("PacSum parameter identity is incomplete")
    if not 0.0 <= float(pacsum["beta"]) <= 1.0:
        raise ValueError("PacSum beta must lie in [0,1]")
    if int(config.get("expected_series", 0)) < 8 or int(config.get("expected_reports", 0)) < int(config.get("expected_series", 0)):
        raise ValueError("frozen report/series counts are invalid")
    runtime = config.get("runtime", {})
    if runtime.get("python") != platform.python_version():
        raise ValueError(f"Python runtime differs from freeze: {platform.python_version()}")
    for package, expected in runtime.get("packages", {}).items():
        actual = importlib.metadata.version(package)
        if actual != expected:
            raise ValueError(f"package runtime differs from freeze: {package} expected {expected}, found {actual}")


def validate_ablation_registry(record: Mapping[str, Any], config: Mapping[str, Any]) -> None:
    if record.get("status") != "FROZEN":
        raise RuntimeError("ablation registry must be FROZEN before authorization")
    if record.get("budgets_words") != [110, 260]:
        raise RuntimeError("ablation registry budgets must be [110, 260]")
    if record.get("positive_weights") != config.get("base_positive_weights"):
        raise RuntimeError("ablation registry positive weights differ from formal config")
    if float(record.get("redundancy_penalty")) != float(config.get("redundancy_penalty")):
        raise RuntimeError("ablation registry redundancy penalty differs from formal config")
    if config.get("bootstrap_seed") not in record.get("required_seeds", []):
        raise RuntimeError("ablation registry does not bind the formal bootstrap seed")
    if not re.fullmatch(r"[0-9a-f]{40}", str(record.get("code_revision", "")), re.I):
        raise RuntimeError("ablation registry requires a frozen 40-hex code revision")


def read_inventory(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        rows = list(csv.DictReader(stream))
    required = {"doc_id", "report_series_id", "split", "rights_status", "source_pdf_sha256", "source_url"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError(f"inventory requires columns {sorted(required)}")
    if len({row["doc_id"] for row in rows}) != len(rows):
        raise ValueError("inventory doc_id values must be unique")
    if any(row["split"] != "external_test" for row in rows):
        raise ValueError("formal inventory may contain only external_test rows")
    allowed_rights = {"CLEARED", "PUBLIC_OFFICIAL", "AUTHORIZED"}
    if any(row["rights_status"].upper() not in allowed_rights for row in rows):
        raise ValueError("every report requires a cleared rights_status")
    if any(not row["source_url"].strip().startswith("https://") for row in rows):
        raise ValueError("every formal inventory row requires an HTTPS source_url")
    if any(not re.fullmatch(r"[0-9a-f]{64}", row["source_pdf_sha256"].strip(), re.I) for row in rows):
        raise ValueError("every formal inventory row requires a 64-hex source_pdf_sha256")
    if len({row["report_series_id"] for row in rows}) < 8:
        raise ValueError("at least eight independent external series are required")
    return rows


def read_seen_exclusions(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        rows = list(csv.DictReader(stream))
    required = {"exposure_class", "source_url", "source_pdf_sha256", "disposition"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("seen-exclusion registry is empty or missing required columns")
    if any(row["disposition"] != "EXCLUDE_FROM_CONFIRMATORY_EXTERNAL" for row in rows):
        raise ValueError("every seen-exclusion row must be excluded from confirmatory external evaluation")
    urls = [row["source_url"].strip() for row in rows if row["source_url"].strip()]
    if len(urls) != len(set(urls)):
        raise ValueError("seen-exclusion source_url values must be unique")
    return rows


def find_seen_overlaps(
    inventory: Iterable[Mapping[str, str]], exclusions: Iterable[Mapping[str, str]]
) -> list[str]:
    excluded_urls = {
        row.get("source_url", "").strip()
        for row in exclusions if row.get("source_url", "").strip()
    }
    excluded_hashes = {
        row.get("source_pdf_sha256", "").strip().upper()
        for row in exclusions if row.get("source_pdf_sha256", "").strip()
    }
    return [
        row["doc_id"] for row in inventory
        if row["source_url"].strip() in excluded_urls
        or row["source_pdf_sha256"].strip().upper() in excluded_hashes
    ]


def preflight(authorization_path: Path, requested_out: Path) -> dict[str, Any]:
    auth = load_json(authorization_path)
    if auth.get("schema") != SCHEMA or auth.get("status") != "AUTHORIZED":
        raise RuntimeError("authorization schema/status is not valid")
    if auth.get("execution_allowed") is not True or auth.get("external_test_accessed") is not False:
        raise RuntimeError("authorization must allow execution and record no prior external access")
    if auth.get("mode") != MODE:
        raise RuntimeError("authorization mode mismatch")

    paths = {name: resolve_bound_path(value) for name, value in auth["paths"].items()}
    expected_out = paths["output_dir"]
    if requested_out.resolve() != expected_out:
        raise RuntimeError(f"output directory is not authorization-bound: {requested_out}")
    if requested_out.exists():
        raise FileExistsError(f"refusing existing output directory: {requested_out}")
    registry_within_output = True
    try:
        paths["attempt_registry"].relative_to(expected_out)
    except ValueError:
        registry_within_output = False
    if registry_within_output:
        raise RuntimeError("durable attempt registry must be outside the output directory")

    # Everything except the private dataset is verified before an attempt is
    # claimed. Hashing the private dataset itself constitutes external access.
    for name in ("config", "external_protocol", "factorial_protocol", "tuning_decision", "tuning_grid", "inventory", "seen_exclusion_registry", "layout_candidate_audit", "layout_audit_summary", "ablation_registry"):
        verify_hash(paths[name], auth["sha256"][name], name)
    code_records = auth.get("code_files", [])
    declared_code = {str(item.get("path", "")).replace("\\", "/") for item in code_records}
    if not REQUIRED_CODE_FILES.issubset(declared_code):
        raise RuntimeError(f"authorization omits required code bindings: {sorted(REQUIRED_CODE_FILES - declared_code)}")
    for item in code_records:
        code_path = resolve_bound_path(item["path"])
        verify_hash(code_path, item["sha256"], f"code:{item['path']}")

    config = load_json(paths["config"])
    validate_config(config)
    if paths["model_snapshot"].name != config["model_revision"] or not paths["model_snapshot"].is_dir():
        raise RuntimeError("local model snapshot is missing or its revision differs from the frozen config")
    model_records = auth.get("model_snapshot_files", [])
    declared_model = {str(item.get("path", "")).replace("\\", "/") for item in model_records}
    actual_model = {path.relative_to(paths["model_snapshot"]).as_posix() for path in paths["model_snapshot"].rglob("*") if path.is_file()}
    if not actual_model or declared_model != actual_model:
        raise RuntimeError("authorization must hash-bind every and only every local model-snapshot file")
    for item in model_records:
        verify_hash(paths["model_snapshot"] / item["path"], item["sha256"], f"model:{item['path']}")
    external_protocol = load_json(paths["external_protocol"])
    factorial_protocol = load_json(paths["factorial_protocol"])
    tuning = load_json(paths["tuning_decision"])
    ablation_registry = load_json(paths["ablation_registry"])
    if external_protocol.get("protocol_status") != "FROZEN" or external_protocol.get("execution_allowed") is not True:
        raise RuntimeError("external protocol is not frozen/authorized")
    if external_protocol.get("external_test_accessed") is not False:
        raise RuntimeError("external protocol does not preserve the pre-run access boundary")
    if factorial_protocol.get("protocol_status") != "FROZEN" or factorial_protocol.get("execution_allowed") is not True:
        raise RuntimeError("factorial protocol is not frozen/authorized")
    if tuning.get("status") != "FROZEN" or tuning.get("external_test_accessed") is not False:
        raise RuntimeError("tuning decision must be frozen without external-test access")
    if tuning.get("selected") != config.get("tuning_selected"):
        raise RuntimeError("formal config does not exactly match the frozen tuning decision")
    validate_ablation_registry(ablation_registry, config)
    expected_bindings = {
        "config_sha256": auth["sha256"]["config"],
        "dataset_sha256": auth["sha256"]["dataset"],
        "inventory_sha256": auth["sha256"]["inventory"],
        "seen_exclusion_registry_sha256": auth["sha256"]["seen_exclusion_registry"],
        "layout_candidate_audit_sha256": auth["sha256"]["layout_candidate_audit"],
        "layout_audit_summary_sha256": auth["sha256"]["layout_audit_summary"],
        "tuning_grid_sha256": auth["sha256"]["tuning_grid"],
        "tuning_decision_sha256": auth["sha256"]["tuning_decision"],
    }
    if external_protocol.get("freeze_bindings") != expected_bindings:
        raise RuntimeError("external protocol freeze bindings differ from the authorization")
    expected_factorial_bindings = {
        "config_sha256": auth["sha256"]["config"],
        "ablation_registry_sha256": auth["sha256"]["ablation_registry"],
    }
    if factorial_protocol.get("freeze_bindings") != expected_factorial_bindings:
        raise RuntimeError("factorial protocol freeze bindings differ from the authorization")
    inventory = read_inventory(paths["inventory"])
    exclusions = read_seen_exclusions(paths["seen_exclusion_registry"])
    overlaps = find_seen_overlaps(inventory, exclusions)
    if overlaps:
        raise RuntimeError(f"external inventory overlaps the seen-exclusion registry: {overlaps}")

    return {"authorization": auth, "paths": paths, "config": config, "inventory": inventory}


def claim_attempt(registry: Path, authorization_path: Path, authorization: Mapping[str, Any]) -> dict[str, Any]:
    registry.parent.mkdir(parents=True, exist_ok=True)
    claim = {
        "schema": "c2ges-external-attempt-v1",
        "run_id": authorization["run_id"],
        "mode": MODE,
        "claimed_at": utc_now(),
        "pid": os.getpid(),
        "authorization_path": str(authorization_path),
        "authorization_sha256": sha256(authorization_path),
        "external_dataset_opened": False,
        "status": "CLAIMED",
    }
    try:
        with registry.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(claim, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
    except FileExistsError as exc:
        raise RuntimeError(f"external attempt already claimed; refusing rerun: {registry}") from exc
    return claim


def update_attempt(registry: Path, claim: Mapping[str, Any], **changes: Any) -> None:
    updated = {**claim, **changes, "updated_at": utc_now()}
    temporary = registry.with_suffix(registry.suffix + ".tmp")
    temporary.write_text(json.dumps(updated, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, registry)


def validate_private_dataset(rows: Sequence[Mapping[str, Any]], inventory: Sequence[Mapping[str, str]], config: Mapping[str, Any]) -> None:
    if len(rows) != len(inventory):
        raise RuntimeError("private dataset/report inventory row counts differ")
    by_doc = {row["doc_id"]: row for row in inventory}
    if {str(row.get("doc_id")) for row in rows} != set(by_doc):
        raise RuntimeError("private dataset doc_ids differ from frozen inventory")
    if len({str(row.get("report_series_id")) for row in rows}) < 8:
        raise RuntimeError("private dataset contains fewer than eight external series")
    for row in rows:
        doc_id = str(row["doc_id"])
        meta = by_doc[doc_id]
        if row.get("split") != "external_test" or str(row.get("report_series_id")) != meta["report_series_id"]:
            raise RuntimeError(f"split/series mismatch for {doc_id}")
        if str(row.get("source_pdf_sha256", "")).upper() != meta["source_pdf_sha256"].upper():
            raise RuntimeError(f"source PDF identity mismatch for {doc_id}")
        candidates = row.get("candidate_sentences")
        if not isinstance(candidates, list) or not candidates or not str(row.get("reference_summary", "")).strip():
            raise RuntimeError(f"missing candidates/reference for {doc_id}")
        ids = [str(unit.get("sid", "")) for unit in candidates]
        if any(not sid for sid in ids) or len(ids) != len(set(ids)):
            raise RuntimeError(f"invalid candidate ids for {doc_id}")
    expected_reports = int(config["expected_reports"])
    expected_series = int(config["expected_series"])
    if len(rows) != expected_reports or len({str(row["report_series_id"]) for row in rows}) != expected_series:
        raise RuntimeError("private dataset counts differ from frozen config")


def normalize_rows(matrix: np.ndarray) -> np.ndarray:
    values = np.asarray(matrix, dtype=np.float64)
    norms = np.linalg.norm(values, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return values / norms


def load_embeddings(texts: Sequence[str], snapshot: Path, policy: str) -> tuple[np.ndarray, dict[str, Any]]:
    from sentence_transformers import SentenceTransformer
    from transformers import AutoTokenizer

    model = SentenceTransformer(str(snapshot), device="cpu", local_files_only=True)
    tokenizer = AutoTokenizer.from_pretrained(snapshot, local_files_only=True)
    production = normalize_rows(np.asarray(model.encode(list(texts), batch_size=32, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False)))
    lengths = tokenizer(list(texts), add_special_tokens=True, truncation=False, padding=False)["input_ids"]
    token_counts = [len(value) for value in lengths]
    if policy == "production_256":
        return production, {"over_256": sum(value > 256 for value in token_counts), "max_tokens": max(token_counts), "policy": policy}
    output = production.copy()
    for index, count in enumerate(token_counts):
        if count <= 256:
            continue
        content_ids = tokenizer(texts[index], add_special_tokens=False, truncation=False)["input_ids"]
        chunks = [content_ids[start : start + 254] for start in range(0, len(content_ids), 254)]
        decoded = [tokenizer.decode(chunk, skip_special_tokens=True, clean_up_tokenization_spaces=False) for chunk in chunks]
        chunk_vectors = normalize_rows(np.asarray(model.encode(decoded, batch_size=32, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False)))
        output[index] = normalize_rows(chunk_vectors.mean(axis=0, keepdims=True))[0]
    return output, {"over_256": sum(value > 256 for value in token_counts), "max_tokens": max(token_counts), "policy": policy}


def complete_rank_select(nodes: Sequence[Any], scores: Sequence[float], budget: int) -> tuple[list[Any], list[str]]:
    ranked = sorted(zip(nodes, scores), key=lambda pair: (-float(pair[1]), pair[0].position, pair[0].sid))
    selected: list[Any] = []
    order: list[str] = []
    used = 0
    for node, _ in ranked:
        words = word_count(node.text)
        if words <= budget - used:
            selected.append(node)
            order.append(node.sid)
            used += words
    return sorted(selected, key=lambda node: node.position), order


def lexical_textrank(nodes: Sequence[Any], alpha: float) -> np.ndarray:
    graph = nx.Graph()
    graph.add_nodes_from(range(len(nodes)))
    token_sets = [set(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", node.text.lower())) for node in nodes]
    for left in range(len(nodes)):
        for right in range(left + 1, len(nodes)):
            union = token_sets[left] | token_sets[right]
            similarity = len(token_sets[left] & token_sets[right]) / len(union) if union else 0.0
            if similarity > 0:
                graph.add_edge(left, right, weight=similarity)
    scores = nx.pagerank(graph, alpha=alpha, weight="weight")
    return np.asarray([scores[index] for index in range(len(nodes))], dtype=np.float64)


def semantic_mmr_select(nodes: Sequence[Any], embeddings: np.ndarray, budget: int, coefficient: float) -> tuple[list[Any], list[str]]:
    centroid = embeddings.mean(axis=0)
    norm = np.linalg.norm(centroid)
    if norm:
        centroid = centroid / norm
    relevance = embeddings @ centroid
    similarity = embeddings @ embeddings.T
    selected: list[int] = []
    order: list[str] = []
    used = 0
    while True:
        candidates = []
        for index, node in enumerate(nodes):
            if index in selected or word_count(node.text) > budget - used:
                continue
            redundancy = max((float(similarity[index, prior]) for prior in selected), default=0.0)
            score = coefficient * float(relevance[index]) - (1.0 - coefficient) * redundancy
            candidates.append((score, node.position, node.sid, index))
        if not candidates:
            break
        winner = sorted(candidates, key=lambda item: (-item[0], item[1], item[2]))[0][3]
        selected.append(winner)
        order.append(nodes[winner].sid)
        used += word_count(nodes[winner].text)
    return sorted((nodes[index] for index in selected), key=lambda node: node.position), order


def selection_metrics(graph: Any, selected: Sequence[Any], cache: RedundancyCache, budget: int) -> dict[str, Any]:
    words = sum(word_count(node.text) for node in selected)
    pairs = [cache.get(left.sid, right.sid) for index, left in enumerate(selected) for right in selected[index + 1 :]]
    return {
        "redundancy": statistics.fmean(pairs) if pairs else 0.0,
        "role_coverage": role_coverage(selected),
        "typed_edge_coverage": typed_edge_coverage(graph, selected),
        "actual_words": words,
        "budget_utilization": words / budget,
        "selected_units": len(selected),
    }


def process_peak_mb() -> float:
    memory = psutil.Process().memory_info()
    return float(getattr(memory, "peak_wset", memory.rss)) / (1024 * 1024)


def system_select(method: str, graph: Any, channels: Mapping[str, Mapping[str, float]], embeddings: np.ndarray,
                  config: Mapping[str, Any], budget: int) -> tuple[list[Any], list[str]]:
    nodes = list(graph.nodes)
    if method == "Lead":
        return complete_rank_select(nodes, [-node.position for node in nodes], budget)
    if method == "Centroid":
        return complete_rank_select(nodes, [channels["relevance"][node.sid] for node in nodes], budget)
    if method == "TextRank":
        return complete_rank_select(nodes, lexical_textrank(nodes, float(config["textrank_alpha"])), budget)
    if method == "Role-only":
        return complete_rank_select(nodes, [channels["role"][node.sid] for node in nodes], budget)
    if method == "Semantic-MMR":
        return semantic_mmr_select(nodes, embeddings, budget, float(config["semantic_mmr_lambda"]))
    if method == "PacSum-MiniLM":
        settings = config["pacsum"]
        scores = pacsum_scores(embeddings, lambda_preceding=float(settings["lambda_preceding"]), lambda_following=float(settings["lambda_following"]), beta=float(settings["beta"]))
        return complete_rank_select(nodes, scores, budget)
    condition = "AB-6" if method == "C2GES-NO-PATH" else "AB-5" if method == "C2GES-FULL" else None
    if condition:
        selected, audit = select_c2ges_word_budget(graph, channels, CONDITIONS[condition], config["base_positive_weights"], budget, float(config["redundancy_penalty"]))
        return selected, list(audit["selection_order"])
    raise ValueError(f"unknown method: {method}")


def paired_series_deltas(rows: Sequence[Mapping[str, Any]], metric: str, budget: int, left: str, right: str) -> dict[str, float]:
    grouped: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in rows:
        if row["status"] == "PASS" and int(row["word_budget"]) == budget and row["method"] in {left, right}:
            grouped[(str(row["report_series_id"]), str(row["method"]))].append(float(row[metric]))
    series = sorted({key[0] for key in grouped})
    if any((series_id, method) not in grouped for series_id in series for method in (left, right)):
        raise RuntimeError(f"incomplete paired series for {left} vs {right}")
    return {series_id: statistics.fmean(grouped[(series_id, left)]) - statistics.fmean(grouped[(series_id, right)]) for series_id in series}


def analyze_systems(rows: Sequence[Mapping[str, Any]], config: Mapping[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    recommended = str(config["recommended_method"])
    families: dict[str, list[dict[str, Any]]] = {"system_comparison": []}
    loso: list[dict[str, Any]] = []
    flattened: list[dict[str, Any]] = []
    for budget in config["word_budgets"]:
        for index, baseline in enumerate(("Semantic-MMR", "TextRank", "PacSum-MiniLM")):
            deltas = paired_series_deltas(rows, "rougeL_f1", int(budget), recommended, baseline)
            summary = contrast_summary(deltas, samples=int(config["bootstrap_samples"]), seed=int(config["bootstrap_seed"]) + int(budget) * 100 + index)
            record = {"word_budget": int(budget), "left": recommended, "right": baseline, "contrast": f"{recommended}_minus_{baseline}", **summary}
            families["system_comparison"].append(record)
            for series_id, delta in summary["series_deltas"].items():
                flattened.append({"family": "system_comparison", "word_budget": budget, "contrast": record["contrast"], "report_series_id": series_id, "series_delta": delta})
            for held_out in sorted(deltas):
                retained = [value for series_id, value in deltas.items() if series_id != held_out]
                loso.append({"word_budget": budget, "contrast": record["contrast"], "held_out_series": held_out, "mean_delta": statistics.fmean(retained), "direction_positive": statistics.fmean(retained) > 0})
    holm(families["system_comparison"])
    for record in families["system_comparison"]:
        for row in flattened:
            if row["word_budget"] == record["word_budget"] and row["contrast"] == record["contrast"]:
                row["holm_adjusted_p"] = record.get("holm_adjusted_p")
                row["cluster_low"] = record["cluster_bootstrap_95"][0]
                row["cluster_high"] = record["cluster_bootstrap_95"][1]
                row["effect_size"] = record["paired_standardized_mean_difference"]
    return families, flattened, loso


def jaccard_ids(left: Sequence[str], right: Sequence[str]) -> float:
    a, b = set(left), set(right)
    return len(a & b) / len(a | b) if a or b else 1.0


def flatten_factorial(families: Mapping[str, Sequence[Mapping[str, Any]]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    interactions: dict[str, list[dict[str, Any]]] = {"reservation_main": [], "path_main": [], "reservation_by_path_interaction": []}
    for family, records in families.items():
        for record in records:
            for series_id, delta in record["series_deltas"].items():
                rows.append({"family": family, "word_budget": record["word_budget"], "contrast": record["contrast"], "report_series_id": series_id, "series_delta": delta, "cluster_low": record["cluster_bootstrap_95"][0], "cluster_high": record["cluster_bootstrap_95"][1], "exact_p": record["exact_series_signflip_p"], "holm_adjusted_p": record.get("holm_adjusted_p"), "effect_size": record["paired_standardized_mean_difference"]})
            if family == "reservation_path_factorial":
                key = "reservation_by_path_interaction" if record["contrast"] == "interaction" else record["contrast"]
                interactions[key].append({key: value for key, value in record.items() if key != "series_deltas"})
    return rows, interactions


def run(authorization_path: Path, out_dir: Path) -> dict[str, Any]:
    prepared = preflight(authorization_path, out_dir)
    auth, paths, config, inventory = prepared["authorization"], prepared["paths"], prepared["config"], prepared["inventory"]
    registry = paths["attempt_registry"]
    claim = claim_attempt(registry, authorization_path, auth)
    try:
        update_attempt(registry, claim, status="DATASET_HASHING", external_dataset_opened=True)
        verify_hash(paths["dataset"], auth["sha256"]["dataset"], "private external dataset")
        reports = load_jsonl(paths["dataset"])
        validate_private_dataset(reports, inventory, config)
        out_dir.mkdir(parents=True)
        e1_dir = out_dir / "prospective_external_v1"
        e3_dir = out_dir / "component_factorial_v1"
        e1_dir.mkdir()
        e3_dir.mkdir()
        for name, source_key in (("rights_safe_external_metadata.csv", "inventory"), ("layout_candidate_audit.csv", "layout_candidate_audit"), ("layout_candidate_audit_summary.json", "layout_audit_summary"), ("balanced_tuning_grid.csv", "tuning_grid"), ("TUNING_DECISION.json", "tuning_decision")):
            source = paths[source_key]
            (e1_dir / name).write_bytes(source.read_bytes())
        (e3_dir / "ablation_config_registry.json").write_bytes(paths["ablation_registry"].read_bytes())

        scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
        e1_rows: list[dict[str, Any]] = []
        e3_rows: list[dict[str, Any]] = []
        locators: list[dict[str, Any]] = []
        selections: dict[tuple[str, int, str], list[str]] = {}
        embedding_diagnostics: list[dict[str, Any]] = []

        for report_number, report in enumerate(reports, 1):
            print(f"[{report_number}/{len(reports)}] formal E1/E3 evaluation: {report['doc_id']}")
            graph_start = time.perf_counter()
            graph = build_graph_v03(report["candidate_sentences"], max_distance=int(config["max_distance"]))
            channels_raw = score_channels(graph, path_min_edges=int(config["path_min_edges"]), path_max_edges=int(config["path_max_edges"]), path_max_paths=int(config["path_max_paths"]), path_max_expansions=int(config["path_max_expansions"]))
            channels = {"relevance": channels_raw["relevance"], "role": channels_raw["role"], "graph": channels_raw["graph"], "path": channels_raw["counterfactual"], "position": channels_raw["position"]}
            graph_seconds = time.perf_counter() - graph_start
            embeddings, embedding_info = load_embeddings([node.text for node in graph.nodes], paths["model_snapshot"], str(config["long_unit_policy"]))
            embedding_diagnostics.append({"doc_id": report["doc_id"], **embedding_info})
            untyped_signal = untyped_graph_signal(graph, int(config["max_distance"]))
            cache = RedundancyCache(graph.nodes)
            page_by_sid = {str(unit["sid"]): unit.get("page", "") for unit in report["candidate_sentences"]}

            for budget in config["word_budgets"]:
                for method in METHODS:
                    tracemalloc.start(); started = time.perf_counter()
                    selected, order = system_select(method, graph, channels, embeddings, config, int(budget))
                    prediction = " ".join(node.text for node in selected)
                    scores = scorer.score(str(report["reference_summary"]), prediction)
                    elapsed = time.perf_counter() - started; _, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
                    row = {"doc_id": report["doc_id"], "report_series_id": report["report_series_id"], "word_budget": int(budget), "method": method, "status": "PASS", "rouge1_f1": scores["rouge1"].fmeasure, "rouge2_f1": scores["rouge2"].fmeasure, "rougeL_f1": scores["rougeL"].fmeasure, **selection_metrics(graph, selected, cache, int(budget)), "shared_graph_seconds": graph_seconds, "selection_scoring_seconds": elapsed, "python_peak_memory_mb": peak / (1024 * 1024), "process_peak_working_set_mb_observed": process_peak_mb()}
                    e1_rows.append(row)
                    selections[(str(report["doc_id"]), int(budget), method)] = [node.sid for node in selected]
                    for rank, node in enumerate(selected, 1):
                        locators.append({"doc_id": report["doc_id"], "report_series_id": report["report_series_id"], "word_budget": budget, "condition": method, "selection_rank_source_order": rank, "sid": node.sid, "page": page_by_sid.get(node.sid, "")})

                for condition_name, condition in CONDITIONS.items():
                    condition_channels = dict(channels)
                    if condition["graph"] == "untyped":
                        condition_channels["graph"] = untyped_signal
                    tracemalloc.start(); started = time.perf_counter()
                    selected, audit = select_c2ges_word_budget(graph, condition_channels, condition, config["base_positive_weights"], int(budget), float(config["redundancy_penalty"]))
                    prediction = " ".join(node.text for node in selected)
                    scores = scorer.score(str(report["reference_summary"]), prediction)
                    elapsed = time.perf_counter() - started; _, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
                    e3_rows.append({"doc_id": report["doc_id"], "report_series_id": report["report_series_id"], "word_budget": int(budget), "condition": condition_name, "status": "PASS", "rouge1_f1": scores["rouge1"].fmeasure, "rouge2_f1": scores["rouge2"].fmeasure, "rougeL_f1": scores["rougeL"].fmeasure, **selection_metrics(graph, selected, cache, int(budget)), "shared_graph_seconds": graph_seconds, "selection_scoring_seconds": elapsed, "python_peak_memory_mb": peak / (1024 * 1024), "process_peak_working_set_mb_observed": process_peak_mb()})
                    selections[(str(report["doc_id"]), int(budget), condition_name)] = [node.sid for node in selected]

        write_csv(e1_dir / "external_item_metrics.csv", e1_rows)
        write_csv(e1_dir / "selected_page_locator.csv", locators)
        e1_aggregates = []
        for budget in config["word_budgets"]:
            for method in METHODS:
                subset = [row for row in e1_rows if row["word_budget"] == budget and row["method"] == method]
                series_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
                for row in subset:
                    series_groups[str(row["report_series_id"])].append(row)
                aggregate = {"word_budget": budget, "method": method, "reports": len(subset), "series": len(series_groups)}
                for metric in ("rouge1_f1", "rouge2_f1", "rougeL_f1", "redundancy", "role_coverage", "typed_edge_coverage", "actual_words", "budget_utilization", "selection_scoring_seconds", "python_peak_memory_mb"):
                    aggregate[f"report_equal_{metric}"] = statistics.fmean(float(row[metric]) for row in subset)
                    aggregate[f"series_equal_{metric}"] = statistics.fmean(statistics.fmean(float(row[metric]) for row in group) for group in series_groups.values())
                e1_aggregates.append(aggregate)
        write_csv(e1_dir / "external_aggregate_metrics.csv", e1_aggregates)
        e1_families, e1_contrasts, loso = analyze_systems(e1_rows, config)
        write_json(e1_dir / "external_series_cluster_results.json", e1_families)
        write_csv(e1_dir / "external_paired_contrasts.csv", e1_contrasts)
        write_csv(e1_dir / "external_loso.csv", loso)

        write_csv(e3_dir / "factorial_item_metrics.csv", e3_rows)
        factorial_aggregates = []
        for budget in config["word_budgets"]:
            for condition in CONDITIONS:
                subset = [row for row in e3_rows if row["word_budget"] == budget and row["condition"] == condition]
                factorial_aggregates.append({"word_budget": budget, "condition": condition, "reports": len(subset), **{metric: statistics.fmean(float(row[metric]) for row in subset) for metric in ("rougeL_f1", "redundancy", "role_coverage", "typed_edge_coverage", "actual_words", "budget_utilization", "selection_scoring_seconds", "python_peak_memory_mb")}})
        write_csv(e3_dir / "factorial_aggregate_metrics.csv", factorial_aggregates)
        factorial_families = analyze_factorial(e3_rows, config)
        series_effects, interactions = flatten_factorial(factorial_families)
        write_csv(e3_dir / "factorial_series_effects.csv", series_effects)
        write_json(e3_dir / "factorial_interactions.json", interactions)
        jaccard_rows = []
        pairs = (("AB-5", "AB-6"), ("RP-10", "RP-00"), ("RP-01", "RP-00"), ("RP-11", "RP-10"), ("G-T", "G-U"))
        for report in reports:
            for budget in config["word_budgets"]:
                for left, right in pairs:
                    jaccard_rows.append({"doc_id": report["doc_id"], "report_series_id": report["report_series_id"], "word_budget": budget, "contrast": f"{left}_vs_{right}", "selection_jaccard": jaccard_ids(selections[(report["doc_id"], budget, left)], selections[(report["doc_id"], budget, right)])})
        write_csv(e3_dir / "factorial_selection_jaccard.csv", jaccard_rows)
        write_csv(e3_dir / "factorial_runtime_resources.csv", [{key: row[key] for key in ("doc_id", "report_series_id", "word_budget", "condition", "status", "shared_graph_seconds", "selection_scoring_seconds", "python_peak_memory_mb", "process_peak_working_set_mb_observed")} for row in e3_rows])
        (e3_dir / "FACTORIAL_REPORT.md").write_text("# C2GES confirmatory component-factorial execution record\n\nFormal run ID: `" + str(auth["run_id"]) + "`  \nReports: " + str(len(reports)) + "  \nSeries: " + str(len({row["report_series_id"] for row in reports})) + "  \nBudgets: 110 and 260 words  \nConditions: AB-0--AB-6, RP-00/RP-10/RP-01/RP-11, G-U/G-T\n\nThis execution record is descriptive. Scientific interpretation and manuscript claims require the frozen statistical outputs and, for human structure metrics, completed E2 annotations.\n", encoding="utf-8")

        manifest = {"schema": "c2ges-external-run-manifest-v1", "status": "COMPLETE", "mode": MODE, "run_id": auth["run_id"], "external_test_accessed": True, "confirmatory_claims_allowed": True, "reports": len(reports), "series": len({row["report_series_id"] for row in reports}), "failed_rows": 0, "word_budgets": config["word_budgets"], "methods": list(METHODS), "conditions": list(CONDITIONS), "dataset_sha256": sha256(paths["dataset"]), "inventory_sha256": sha256(paths["inventory"]), "seen_exclusion_registry_sha256": sha256(paths["seen_exclusion_registry"]), "authorization_sha256": sha256(authorization_path), "config_sha256": sha256(paths["config"]), "external_protocol_sha256": sha256(paths["external_protocol"]), "factorial_protocol_sha256": sha256(paths["factorial_protocol"]), "tuning_decision_sha256": sha256(paths["tuning_decision"]), "model_revision": paths["model_snapshot"].name, "embedding_diagnostics": embedding_diagnostics, "python": platform.python_version(), "numpy": np.__version__, "networkx": nx.__version__, "completed_at": utc_now()}
        write_json(e1_dir / "RUN_MANIFEST.json", manifest)
        checksum_targets = [e1_dir / name for name in PUBLIC_E1_FILES] + [e3_dir / name for name in PUBLIC_E3_FILES]
        (e1_dir / "OUTPUT_SHA256SUMS.txt").write_text("".join(f"{sha256(path)}  {path.relative_to(e1_dir).as_posix()}\n" for path in checksum_targets), encoding="utf-8")
        update_attempt(registry, claim, status="COMPLETE", external_dataset_opened=True, output_dir=str(out_dir), output_checksum_sha256=sha256(e1_dir / "OUTPUT_SHA256SUMS.txt"))
        return manifest
    except Exception as exc:
        update_attempt(registry, claim, status="FAILED_AFTER_CLAIM", external_dataset_opened=True, error_type=type(exc).__name__, error=str(exc))
        raise


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authorization", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.authorization.resolve(), args.out_dir.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
