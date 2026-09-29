"""Shared RSI helpers: protocol load, overwrite guard, word-budget selection, ROUGE."""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from rouge_score import rouge_scorer

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]  # C2GES release root
CORE = PROJECT / "03_Reproducibility" / "Code" / "core"
R2 = CORE / "R2_v0_3"
for path in (CORE, R2):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from counterfactual_paths import raw_path_counterfactual_loss  # noqa: E402
from v03_methods import (  # noqa: E402
    RedundancyCache,
    build_graph_v03,
    minmax,
    score_channels,
)
from path_utilities import apply_utility  # noqa: E402

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*")
PROTOCOL_PATH = HERE / "PROTOCOL.json"
DATA_ROOT = PROJECT / "03_Reproducibility" / "Data" / "rsi_path_v1"
RUN_DIR = DATA_ROOT / "run"
EVOLUTION_DIR = DATA_ROOT / "evolution"
DEV_JSONL = (
    PROJECT.parents[1]
    / "applied_sciences_dual_rebuild"
    / "C2GES"
    / "original_title_rebuild"
    / "R2_v0_3"
    / "diagnostic_build_08"
    / "nerc_full_pdf_dev_v0_3.jsonl"
)
TEST_JSONL = DEV_JSONL.with_name("nerc_full_pdf_test_v0_3.jsonl")
NO_PATH_BASE = {
    "relevance": 0.40,
    "role": 0.20,
    "graph": 0.15,
    "path": 0.0,
    "position": 0.10,
}
ROLE_GROUPS = {
    "cause_or_trigger": ("root_cause", "trigger_event"),
    "propagation_or_impact": ("propagation_or_response", "impact"),
    "mitigation": ("mitigation",),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load_protocol() -> dict[str, Any]:
    return json.loads(PROTOCOL_PATH.read_text(encoding="utf-8"))


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def word_count(text: str) -> int:
    return len(WORD_RE.findall(text or ""))


def rouge_l_f1(hypothesis: str, reference: str, *, use_stemmer: bool = True) -> float:
    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=use_stemmer)
    return float(scorer.score(reference or "", hypothesis or "")["rougeL"].fmeasure)


def assert_run_dir_writable(run_dir: Path) -> None:
    """Refuse to overwrite a sealed RSI evaluation directory."""
    if (run_dir / "SEALED").is_file() or (run_dir / "EVALUATION.json").is_file():
        raise FileExistsError(f"refusing to overwrite sealed RSI run: {run_dir}")


def channel_weights(path_weight: float) -> dict[str, float]:
    weights = dict(NO_PATH_BASE)
    weights["path"] = float(path_weight)
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("weights must be positive in total")
    return {name: value / total for name, value in weights.items()}


def textrank_scores(nodes: Sequence[Any], settings: Mapping[str, Any]) -> dict[str, float]:
    from v03_methods import jaccard

    similarities = {
        (left.sid, right.sid): jaccard(left.text, right.text)
        for index, left in enumerate(nodes)
        for right in nodes[index + 1 :]
    }
    try:
        import networkx as nx

        graph = nx.Graph()
        graph.add_nodes_from(node.sid for node in nodes)
        graph.add_weighted_edges_from(
            (left, right, value) for (left, right), value in similarities.items() if value > 0
        )
        scores = nx.pagerank(
            graph,
            alpha=float(settings["alpha"]),
            max_iter=int(settings["max_iter"]),
            tol=float(settings["tolerance"]),
            weight="weight",
        )
        raw = [float(scores.get(node.sid, 0.0)) for node in nodes]
    except (ImportError, ModuleNotFoundError):
        degree = {
            node.sid: sum(value for pair, value in similarities.items() if node.sid in pair)
            for node in nodes
        }
        raw = [degree[node.sid] for node in nodes]
    scaled = minmax(raw)
    return {node.sid: value for node, value in zip(nodes, scaled)}


def select_word_budget(
    nodes: Sequence[Any],
    base_scores: Mapping[str, float],
    word_budget: int,
    *,
    reservation: bool,
    redundancy_penalty: float,
) -> tuple[list[Any], dict[str, Any]]:
    by_sid = {node.sid: node for node in nodes}
    cache = RedundancyCache(nodes)
    selected: list[str] = []
    used = 0

    def fitting(candidates: Iterable[Any]) -> list[Any]:
        return [node for node in candidates if word_count(node.text) <= word_budget - used]

    def choose(candidates: Sequence[Any], apply_redundancy: bool) -> Any:
        def adjusted(node: Any) -> float:
            penalty = 0.0
            if apply_redundancy and selected:
                penalty = redundancy_penalty * max(cache.get(node.sid, prior) for prior in selected)
            return float(base_scores[node.sid]) - penalty

        return sorted(candidates, key=lambda node: (-adjusted(node), node.position, node.sid))[0]

    if reservation:
        for group, roles in ROLE_GROUPS.items():
            eligible = fitting(
                node for node in nodes if node.sid not in selected and node.dominant_role in roles
            )
            if eligible:
                winner = choose(eligible, False)
                selected.append(winner.sid)
                used += word_count(winner.text)

    while True:
        eligible = fitting(node for node in nodes if node.sid not in selected)
        if not eligible:
            break
        winner = choose(eligible, True)
        selected.append(winner.sid)
        used += word_count(winner.text)

    ordered = sorted((by_sid[sid] for sid in selected), key=lambda node: node.position)
    return ordered, {"selection_order": selected, "actual_words": used}


def select_ranking_word_budget(
    nodes: Sequence[Any],
    scores: Mapping[str, float],
    word_budget: int,
) -> tuple[list[Any], dict[str, Any]]:
    order = sorted(nodes, key=lambda node: (-float(scores[node.sid]), node.position, node.sid))
    selected: list[Any] = []
    used = 0
    skipped = 0
    for node in order:
        words = word_count(node.text)
        if used + words <= word_budget:
            selected.append(node)
            used += words
        else:
            skipped += 1
    ordered = sorted(selected, key=lambda node: node.position)
    return ordered, {"actual_words": used, "skipped_unfit": skipped}


def prepare_report(row: Mapping[str, Any]) -> dict[str, Any]:
    graph = build_graph_v03(row["candidate_sentences"], max_distance=12)
    channels = score_channels(graph, path_max_edges=4)
    raw = raw_path_counterfactual_loss(graph, min_edges=2, max_edges=4)
    words = {node.sid: word_count(node.text) for node in graph.nodes}
    return {
        "doc_id": row["doc_id"],
        "report_series_id": row.get("report_series_id") or row["doc_id"],
        "reference": row.get("reference_summary") or "",
        "graph": graph,
        "channels": channels,
        "raw_path": raw,
        "word_counts": words,
    }


def c2ges_select(
    prepared: Mapping[str, Any],
    *,
    utility: str | None,
    path_weight: float,
    word_budget: int,
) -> dict[str, Any]:
    graph = prepared["graph"]
    channels = dict(prepared["channels"])
    if path_weight > 0:
        if utility is None:
            raise ValueError("path utility required when path_weight>0")
        channels["path"] = apply_utility(
            utility, prepared["raw_path"], graph.nodes, channels["relevance"], prepared["word_counts"]
        )
    else:
        channels["path"] = {node.sid: 0.0 for node in graph.nodes}
    weights = channel_weights(path_weight)
    base = {
        node.sid: sum(weights[name] * float(channels[name][node.sid]) for name in weights)
        for node in graph.nodes
    }
    selected, audit = select_word_budget(
        graph.nodes,
        base,
        word_budget,
        reservation=True,
        redundancy_penalty=0.50,
    )
    text = " ".join(node.text for node in selected)
    return {
        "selected_sids": [node.sid for node in selected],
        "selected_text": text,
        "actual_words": audit["actual_words"],
        "rougeL_f1": rouge_l_f1(text, prepared["reference"]),
        "weights": weights,
        "utility": utility,
        "path_weight": path_weight,
    }


def textrank_select(prepared: Mapping[str, Any], word_budget: int, settings: Mapping[str, Any]) -> dict[str, Any]:
    scores = textrank_scores(prepared["graph"].nodes, settings)
    selected, audit = select_ranking_word_budget(prepared["graph"].nodes, scores, word_budget)
    text = " ".join(node.text for node in selected)
    return {
        "selected_sids": [node.sid for node in selected],
        "selected_text": text,
        "actual_words": audit["actual_words"],
        "rougeL_f1": rouge_l_f1(text, prepared["reference"]),
        "utility": None,
        "path_weight": 0.0,
    }
