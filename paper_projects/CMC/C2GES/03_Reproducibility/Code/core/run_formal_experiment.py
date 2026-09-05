"""Run the frozen offline six-condition C2GES report summarization experiment.

The runner never calls a network service or LLM.  It refuses an existing output
directory and verifies the frozen configuration, dataset, and code hashes before
writing predictions.  Machine-verified role evidence is used only for a clearly
labelled silver diagnostic.
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
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from rouge_score import rouge_scorer

from c2ges_offline import (
    ROLES,
    CausalEventGraph,
    ConstrainedExtractiveSummarizer,
    SentenceNode,
)


def find_repository_root(start: Path) -> Path:
    """Find the workspace root without depending on archive directory depth."""
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


ROOT = find_repository_root(Path(__file__).resolve().parent)
EXPECTED_CONDITIONS = (
    "lead",
    "centroid",
    "textrank",
    "role",
    "graph_no_cf",
    "c2ges_full",
)
TOKEN_RE = re.compile(r"[a-z0-9]+(?:[-'][a-z0-9]+)?", re.I)
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in",
    "is", "it", "of", "on", "or", "that", "the", "their", "this", "to",
    "was", "were", "with",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def tokens(text: str) -> set[str]:
    return {token.lower() for token in TOKEN_RE.findall(text) if token.lower() not in STOPWORDS}


def jaccard(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a | b) if a or b else 0.0


def minmax(values: Sequence[float]) -> list[float]:
    if not values:
        return []
    low, high = min(values), max(values)
    if math.isclose(low, high):
        return [0.0 for _ in values]
    return [(value - low) / (high - low) for value in values]


def validate_config(config: Mapping[str, Any]) -> None:
    if tuple(config.get("conditions", ())) != EXPECTED_CONDITIONS:
        raise ValueError(f"conditions must be exactly {EXPECTED_CONDITIONS}")
    if int(config.get("selection_budget", 0)) < 1:
        raise ValueError("selection_budget must be positive")
    if int(config.get("bootstrap_samples", 0)) < 1:
        raise ValueError("bootstrap_samples must be positive")
    for name in ("graph_no_cf_weights", "c2ges_full_weights"):
        weights = config[name]
        values = [float(weights[key]) for key in ("relevance", "role", "graph", "counterfactual", "position")]
        if any(value < 0 for value in values) or not math.isclose(sum(values), 1.0, abs_tol=1e-9):
            raise ValueError(f"{name} channel weights must be non-negative and sum to one")
    if float(config["graph_no_cf_weights"]["counterfactual"]) != 0.0:
        raise ValueError("graph_no_cf must have zero counterfactual weight")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"line {line_number} is not an object")
            rows.append(row)
    return rows


def verify_freeze(freeze_path: Path, config_path: Path, dataset_path: Path) -> dict[str, Any]:
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    failures = []
    checks = {
        "config": {"expected": freeze["config_sha256"], "actual": sha256(config_path)},
        "dataset": {"expected": freeze["dataset_sha256"], "actual": sha256(dataset_path)},
    }
    for item in freeze["code_files"]:
        path = ROOT / item["path"]
        actual = sha256(path) if path.is_file() else None
        checks[item["path"]] = {"expected": item["sha256"], "actual": actual}
    runtime = freeze.get("runtime", {})
    if runtime:
        actual_python = platform.python_version()
        checks["runtime:python"] = {"expected": runtime["python"], "actual": actual_python}
        for package, expected in runtime.get("packages", {}).items():
            try:
                actual = importlib.metadata.version(package)
            except importlib.metadata.PackageNotFoundError:
                actual = None
            checks[f"runtime:{package}"] = {"expected": expected, "actual": actual}
    for name, check in checks.items():
        check["passed"] = check["expected"].lower() == str(check["actual"]).lower()
        if not check["passed"]:
            failures.append(name)
    if failures:
        raise RuntimeError(f"freeze verification failed: {failures}")
    return {"freeze": freeze, "checks": checks, "freeze_sha256": sha256(freeze_path)}


def centroid_scores(nodes: Sequence[SentenceNode]) -> dict[str, float]:
    focus = Counter(token for node in nodes for token in tokens(node.text))
    raw = []
    for node in nodes:
        terms = tokens(node.text)
        denominator = math.sqrt(max(1, len(terms))) * math.sqrt(max(1, sum(focus.values())))
        raw.append(sum(focus[token] for token in terms) / denominator)
    return {node.sid: score for node, score in zip(nodes, minmax(raw))}


def textrank_scores(nodes: Sequence[SentenceNode], settings: Mapping[str, Any]) -> tuple[dict[str, float], str]:
    similarities = {
        (left.sid, right.sid): jaccard(left.text, right.text)
        for index, left in enumerate(nodes)
        for right in nodes[index + 1 :]
    }
    try:
        import networkx as nx

        graph = nx.Graph()
        graph.add_nodes_from(node.sid for node in nodes)
        graph.add_weighted_edges_from((left, right, value) for (left, right), value in similarities.items() if value > 0)
        scores = nx.pagerank(
            graph,
            alpha=float(settings["alpha"]),
            max_iter=int(settings["max_iter"]),
            tol=float(settings["tolerance"]),
            weight="weight",
        )
        return {node.sid: float(scores[node.sid]) for node in nodes}, f"networkx_pagerank_{nx.__version__}"
    except (ImportError, ModuleNotFoundError):
        degree = {
            node.sid: sum(value for pair, value in similarities.items() if node.sid in pair)
            for node in nodes
        }
        scaled = minmax([degree[node.sid] for node in nodes])
        return {node.sid: value for node, value in zip(nodes, scaled)}, "weighted_degree_fallback"


def role_scores(nodes: Sequence[SentenceNode]) -> dict[str, float]:
    return {node.sid: max(dict(node.role_scores).values()) for node in nodes}


def top_k(nodes: Sequence[SentenceNode], scores: Mapping[str, float], budget: int) -> list[SentenceNode]:
    ranked = sorted(nodes, key=lambda node: (-float(scores[node.sid]), node.position, node.sid))[:budget]
    return sorted(ranked, key=lambda node: node.position)


def summarizer_from_config(weights: Mapping[str, Any]) -> ConstrainedExtractiveSummarizer:
    return ConstrainedExtractiveSummarizer(
        relevance_weight=float(weights["relevance"]),
        role_weight=float(weights["role"]),
        graph_weight=float(weights["graph"]),
        counterfactual_weight=float(weights["counterfactual"]),
        position_weight=float(weights["position"]),
        redundancy_penalty=float(weights["redundancy_penalty"]),
    )


def select_condition(
    condition: str,
    graph: CausalEventGraph,
    config: Mapping[str, Any],
) -> tuple[list[SentenceNode], dict[str, Any]]:
    nodes = graph.nodes
    budget = min(int(config["selection_budget"]), len(nodes))
    if condition == "lead":
        selected = list(nodes[:budget])
        return selected, {"implementation": "document_order", "scores": {node.sid: 1.0 / (1 + node.position) for node in nodes}}
    if condition == "centroid":
        scores = centroid_scores(nodes)
        return top_k(nodes, scores, budget), {"implementation": "offline_document_centroid", "scores": scores}
    if condition == "textrank":
        scores, implementation = textrank_scores(nodes, config["textrank"])
        return top_k(nodes, scores, budget), {"implementation": implementation, "scores": scores}
    if condition == "role":
        scores = role_scores(nodes)
        return top_k(nodes, scores, budget), {"implementation": "five_role_lexical_plus_optional_silver_projection", "scores": scores}
    if condition in {"graph_no_cf", "c2ges_full"}:
        key = "graph_no_cf_weights" if condition == "graph_no_cf" else "c2ges_full_weights"
        result = summarizer_from_config(config[key]).summarize(graph, budget=budget)
        selected = [graph.node(sentence.sid) for sentence in result.sentences]
        return selected, {
            "implementation": "constrained_causal_graph_summarizer",
            "scores": {sentence.sid: sentence.score for sentence in result.sentences},
            "selection_order": list(result.selection_order),
            "selection_reasons": {sentence.sid: sentence.selection_reason for sentence in result.sentences},
            "covered_predicted_role_groups": list(result.covered_role_groups),
            "weights": dict(config[key]),
        }
    raise ValueError(f"unknown condition: {condition}")


def silver_role_coverage(selected_ids: set[str], silver: Mapping[str, Sequence[Any]]) -> tuple[float, dict[str, bool]]:
    available = {}
    for role in ROLES:
        evidence = {
            str(record.get("sid", "")) if isinstance(record, Mapping) else str(record)
            for record in silver.get(role, ())
        }
        evidence.discard("")
        if evidence:
            available[role] = bool(selected_ids & evidence)
    return (sum(available.values()) / len(available) if available else 0.0), available


def redundancy(selected: Sequence[SentenceNode]) -> float:
    pairs = [
        jaccard(left.text, right.text)
        for index, left in enumerate(selected)
        for right in selected[index + 1 :]
    ]
    return statistics.fmean(pairs) if pairs else 0.0


def evaluate_document(row: Mapping[str, Any], config: Mapping[str, Any], scorer: Any) -> list[dict[str, Any]]:
    graph = CausalEventGraph.from_sentences(row["candidate_sentences"], row.get("silver_role_evidence", {}))
    outputs = []
    for condition in EXPECTED_CONDITIONS:
        selected, audit = select_condition(condition, graph, config)
        prediction = " ".join(node.text for node in selected)
        rouge = scorer.score(str(row["reference_summary"]), prediction)
        selected_ids = {node.sid for node in selected}
        coverage, by_role = silver_role_coverage(selected_ids, row.get("silver_role_evidence", {}))
        outputs.append({
            "doc_id": row["doc_id"],
            "split": row["split"],
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
                "redundancy": float(redundancy(selected)),
            },
            "silver_role_hits": by_role,
            "graph": {
                "node_count": len(graph.nodes),
                "edge_count": len(graph.edges),
                "causal_flow": graph.causal_flow(),
            },
            "selection_audit": audit,
        })
    return outputs


def aggregate(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    metrics = ("rouge1_f1", "rouge2_f1", "rougeL_f1", "silver_role_coverage", "redundancy")
    return {
        condition: {
            "n_reports": len(subset),
            **{metric: statistics.fmean(row["metrics"][metric] for row in subset) for metric in metrics},
        }
        for condition in EXPECTED_CONDITIONS
        for subset in [[row for row in rows if row["condition"] == condition]]
    }


def paired_bootstrap(
    rows: Sequence[Mapping[str, Any]],
    baseline: str,
    metric: str,
    *,
    samples: int,
    seed: int,
) -> dict[str, Any]:
    by_key = {(row["doc_id"], row["condition"]): float(row["metrics"][metric]) for row in rows}
    doc_ids = sorted({row["doc_id"] for row in rows})
    observed = [by_key[(doc_id, "c2ges_full")] - by_key[(doc_id, baseline)] for doc_id in doc_ids]
    rng = random.Random(seed)
    draws = []
    for _ in range(samples):
        sampled = [observed[rng.randrange(len(observed))] for _ in observed]
        draws.append(statistics.fmean(sampled))
    ordered = sorted(draws)
    low_index = max(0, math.floor(0.025 * (samples - 1)))
    high_index = min(samples - 1, math.ceil(0.975 * (samples - 1)))
    p_lower = sum(value <= 0 for value in draws) / samples
    p_upper = sum(value >= 0 for value in draws) / samples
    return {
        "contrast": f"c2ges_full_minus_{baseline}",
        "metric": metric,
        "n_reports": len(doc_ids),
        "observed_mean_delta": statistics.fmean(observed),
        "ci95_percentile": [ordered[low_index], ordered[high_index]],
        "p_two_sided_bootstrap": min(1.0, 2.0 * min(p_lower, p_upper)),
        "samples": samples,
        "seed": seed,
        "resampling_unit": "report",
    }


def run(config_path: Path, freeze_path: Path, dataset_path: Path, output_dir: Path) -> dict[str, Any]:
    if output_dir.exists():
        raise FileExistsError(f"output directory already exists: {output_dir}")
    output_dir.mkdir(parents=True)
    state_path = output_dir / "run_state.json"
    write_json(state_path, {"status": "RUNNING", "started_utc": utc_now()})
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
        validate_config(config)
        verification = verify_freeze(freeze_path, config_path, dataset_path)
        dataset = load_jsonl(dataset_path)
        test_rows = [row for row in dataset if row.get("split") == "test"]
        if not test_rows:
            raise ValueError("dataset contains no test reports")
        scorer = rouge_scorer.RougeScorer(
            ["rouge1", "rouge2", "rougeL"],
            use_stemmer=bool(config["rouge_use_stemmer"]),
        )
        predictions = []
        for row in sorted(test_rows, key=lambda item: item["doc_id"]):
            predictions.extend(evaluate_document(row, config, scorer))
        prediction_path = output_dir / "predictions.jsonl"
        with prediction_path.open("w", encoding="utf-8", newline="\n") as handle:
            for row in predictions:
                handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        summary = aggregate(predictions)
        write_json(output_dir / "aggregate_metrics.json", summary)
        bootstrap = [
            paired_bootstrap(
                predictions,
                baseline,
                metric,
                samples=int(config["bootstrap_samples"]),
                seed=int(config["bootstrap_seed"]) + baseline_index * 10 + metric_index,
            )
            for baseline_index, baseline in enumerate(EXPECTED_CONDITIONS[:-1])
            for metric_index, metric in enumerate(("rouge1_f1", "rouge2_f1", "rougeL_f1"))
        ]
        write_json(output_dir / "paired_bootstrap.json", bootstrap)
        textrank_implementations = sorted({
            row["selection_audit"]["implementation"]
            for row in predictions if row["condition"] == "textrank"
        })
        manifest = {
            "protocol": config["protocol"],
            "status": "COMPLETE",
            "started_utc": json.loads(state_path.read_text(encoding="utf-8"))["started_utc"],
            "completed_utc": utc_now(),
            "offline_only": True,
            "conditions": list(EXPECTED_CONDITIONS),
            "test_report_count": len(test_rows),
            "prediction_row_count": len(predictions),
            "selection_budget": config["selection_budget"],
            "silver_label_boundary": "machine_verified_candidate_not_human_or_expert_gold",
            "textrank_implementation": textrank_implementations,
            "runtime": {
                "python": sys.version,
                "platform": platform.platform(),
            },
            "freeze_verification": verification,
            "artifacts": {
                "predictions.jsonl": sha256(prediction_path),
                "aggregate_metrics.json": sha256(output_dir / "aggregate_metrics.json"),
                "paired_bootstrap.json": sha256(output_dir / "paired_bootstrap.json"),
            },
        }
        write_json(output_dir / "manifest.json", manifest)
        write_json(state_path, {"status": "COMPLETE", "started_utc": manifest["started_utc"], "completed_utc": manifest["completed_utc"]})
        return manifest
    except Exception as exc:
        failure = {
            "status": "FAILED",
            "failed_utc": utc_now(),
            "error_type": type(exc).__name__,
            "error": str(exc),
            "traceback": traceback.format_exc(),
        }
        write_json(output_dir / "failure.json", failure)
        write_json(state_path, failure)
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--freeze", type=Path, required=True)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = run(args.config.resolve(), args.freeze.resolve(), args.dataset.resolve(), args.output.resolve())
    print(json.dumps({
        "status": manifest["status"],
        "test_report_count": manifest["test_report_count"],
        "prediction_row_count": manifest["prediction_row_count"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
