"""Shared deterministic selection methods for C2GES v0.3."""

from __future__ import annotations

import math
import sys
from collections import Counter
from pathlib import Path
from typing import Mapping, Sequence

R1_CORE = Path(__file__).resolve().parents[1]
if str(R1_CORE) not in sys.path:
    sys.path.insert(0, str(R1_CORE))

from c2ges_offline import (
    CAUSAL_TRANSITIONS,
    ROLES,
    CausalEdge,
    CausalEventGraph,
    SentenceNode,
    _jaccard,
    _role_hits,
    _unit_scale,
)
from counterfactual_paths import path_counterfactual_sensitivity


STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in", "is", "it",
    "of", "on", "or", "that", "the", "their", "this", "to", "was", "were", "with",
}


def build_graph_v03(sentences: Sequence[Mapping[str, object]], *, max_distance: int = 12) -> CausalEventGraph:
    """Build the v0.3 lexical proxy graph, abstaining on every top-score tie.

    v0.3 intentionally accepts no silver role input.  A sentence with two or
    more equal positive maxima receives ``dominant_role=None`` and therefore
    cannot create a directed causal edge.
    """
    if max_distance < 1:
        raise ValueError("max_distance must be positive")
    parsed: list[tuple[str, str, int]] = []
    for position, sentence in enumerate(sentences):
        sid = str(sentence.get("sid", "")).strip()
        text = str(sentence.get("text", "")).strip()
        if not sid or not text:
            raise ValueError("every sentence requires non-empty sid and text")
        parsed.append((sid, text, position))
    if len({sid for sid, _, _ in parsed}) != len(parsed):
        raise ValueError("sentence ids must be unique")
    if not parsed:
        return CausalEventGraph([], [])

    raw = {role: [_role_hits(text, role) for _, text, _ in parsed] for role in ROLES}
    normalized = {role: _unit_scale(values) for role, values in raw.items()}
    nodes: list[SentenceNode] = []
    for index, (sid, text, position) in enumerate(parsed):
        scores = {role: normalized[role][index] for role in ROLES}
        best = max(scores.values())
        maxima = [role for role in ROLES if best > 0 and math.isclose(scores[role], best, abs_tol=1e-12)]
        dominant = maxima[0] if len(maxima) == 1 else None
        nodes.append(
            SentenceNode(
                sid=sid,
                text=text,
                position=position,
                role_scores=tuple((role, scores[role]) for role in ROLES),
                dominant_role=dominant,
            )
        )

    edges: list[CausalEdge] = []
    for source in nodes:
        if source.dominant_role is None:
            continue
        for target in nodes:
            if source.sid == target.sid or target.dominant_role is None:
                continue
            relation = CAUSAL_TRANSITIONS.get((source.dominant_role, target.dominant_role))
            distance = abs(source.position - target.position)
            if relation is None or distance > max_distance:
                continue
            proximity = math.exp(-distance / 5.0)
            overlap = _jaccard(source.text, target.text)
            confidence = min(
                source.role_score(source.dominant_role), target.role_score(target.dominant_role)
            )
            weight = 0.45 * proximity + 0.30 * overlap + 0.25 * confidence
            edges.append(CausalEdge(source.sid, target.sid, relation, round(weight, 12)))
    return CausalEventGraph(nodes, edges)


def tokens(text: str) -> set[str]:
    import re

    return {token.lower() for token in re.findall(r"[a-z0-9]+(?:[-'][a-z0-9]+)?", text, re.I) if token.lower() not in STOPWORDS}


def jaccard(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a | b) if a or b else 0.0


class RedundancyCache:
    """Per-graph lazy Jaccard cache shared across development grid records."""

    def __init__(self, nodes: Sequence[SentenceNode]):
        self._tokens = {node.sid: tokens(node.text) for node in nodes}
        self._values: dict[tuple[str, str], float] = {}

    def get(self, left_sid: str, right_sid: str) -> float:
        key = tuple(sorted((left_sid, right_sid)))
        if key not in self._values:
            left, right = self._tokens[left_sid], self._tokens[right_sid]
            self._values[key] = len(left & right) / len(left | right) if left or right else 0.0
        return self._values[key]


def minmax(values: Sequence[float]) -> list[float]:
    if not values:
        return []
    low, high = min(values), max(values)
    if math.isclose(low, high):
        return [0.0 for _ in values]
    return [(value - low) / (high - low) for value in values]


def relevance_scores(nodes: Sequence[SentenceNode]) -> dict[str, float]:
    focus = Counter(token for node in nodes for token in tokens(node.text))
    raw = []
    for node in nodes:
        terms = tokens(node.text)
        denominator = math.sqrt(max(1, len(terms))) * math.sqrt(max(1, sum(focus.values())))
        raw.append(sum(focus[token] for token in terms) / denominator)
    return {node.sid: value for node, value in zip(nodes, minmax(raw))}


ROLE_GROUPS = {
    "cause_or_trigger": ("root_cause", "trigger_event"),
    "propagation_or_impact": ("propagation_or_response", "impact"),
    "mitigation": ("mitigation",),
}


def score_channels(graph: CausalEventGraph, *, path_max_edges: int) -> dict[str, dict[str, float]]:
    return {
        "relevance": relevance_scores(graph.nodes),
        "role": {node.sid: max(dict(node.role_scores).values()) for node in graph.nodes},
        "graph": graph.graph_signal(),
        "counterfactual": path_counterfactual_sensitivity(graph, min_edges=2, max_edges=path_max_edges),
        "position": {node.sid: 1.0 / (1.0 + node.position) for node in graph.nodes},
    }


def constrained_select(
    graph: CausalEventGraph,
    channels: Mapping[str, Mapping[str, float]],
    weights: Mapping[str, float],
    *,
    budget: int,
    redundancy_penalty: float,
    remove_cf_only: bool = False,
    redundancy_cache: RedundancyCache | None = None,
) -> tuple[list[SentenceNode], dict]:
    """Select with identical coefficients in strict no-CF except CF is set to zero."""
    if budget < 1:
        raise ValueError("budget must be positive")
    channel_names = ("relevance", "role", "graph", "counterfactual", "position")
    if any(float(weights[name]) < 0 for name in channel_names):
        raise ValueError("channel weights must be non-negative")
    if not math.isclose(sum(float(weights[name]) for name in channel_names), 1.0, abs_tol=1e-12):
        raise ValueError("Full weights must sum to one")
    nodes = list(graph.nodes)
    budget = min(budget, len(nodes))
    effective = dict(weights)
    if remove_cf_only:
        effective["counterfactual"] = 0.0
    base = {
        node.sid: sum(float(effective[name]) * float(channels[name][node.sid]) for name in channel_names)
        for node in nodes
    }
    selected: list[str] = []
    reasons: dict[str, str] = {}
    by_sid = {node.sid: node for node in nodes}
    similarity = redundancy_cache or RedundancyCache(nodes)
    if budget >= len(ROLE_GROUPS):
        for group, roles in ROLE_GROUPS.items():
            eligible = [node for node in nodes if node.sid not in selected and node.dominant_role in roles]
            if eligible:
                winner = max(eligible, key=lambda node: (base[node.sid], -node.position, node.sid))
                selected.append(winner.sid)
                reasons[winner.sid] = f"required_role_group:{group}"
    while len(selected) < budget:
        eligible = [node for node in nodes if node.sid not in selected]
        winner = max(
            eligible,
            key=lambda node: (
                base[node.sid]
                - redundancy_penalty * max((similarity.get(node.sid, sid) for sid in selected), default=0.0),
                -node.position,
                node.sid,
            ),
        )
        selected.append(winner.sid)
        reasons[winner.sid] = "highest_adjusted_score"
    ordered = sorted((by_sid[sid] for sid in selected), key=lambda node: node.position)
    return ordered, {
        "base_scores": base,
        "effective_weights": effective,
        "selection_order": selected,
        "selection_reasons": reasons,
        "strict_single_factor_cf_removal": remove_cf_only,
    }


def redundancy(selected: Sequence[SentenceNode]) -> float:
    values = [jaccard(left.text, right.text) for index, left in enumerate(selected) for right in selected[index + 1 :]]
    return sum(values) / len(values) if values else 0.0
