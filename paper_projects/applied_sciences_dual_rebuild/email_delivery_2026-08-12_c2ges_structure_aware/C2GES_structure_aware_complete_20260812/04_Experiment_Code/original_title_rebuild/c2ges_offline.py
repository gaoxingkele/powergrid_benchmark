"""Offline causal-graph and constrained extractive summarization primitives.

This module is the minimum executable method core for the original-title
C2GES rebuild.  It makes no network or model API call.  The lexical role cues
and sentence-graph idea are adapted from the earlier audited C2GES evidence
selector, while graph interventions and report-level constrained selection are
new here.  Silver role evidence is optional and is never interpreted as human
gold.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence


ROLES = (
    "trigger_event",
    "root_cause",
    "propagation_or_response",
    "impact",
    "mitigation",
)

ROLE_TERMS = {
    "trigger_event": (
        "fault", "outage", "occurred", "initiated", "triggered", "relay",
        "fire", "tripped", "failed splice", "insulator",
    ),
    "root_cause": (
        "cause", "caused", "root cause", "attributed", "due to", "because",
        "failure", "failed", "settings", "protection", "misoperated",
        "frozen", "winterization",
    ),
    "propagation_or_response": (
        "respond", "response", "tripped", "trip", "propagated", "propagate",
        "voltage", "frequency", "island", "load shed", "ufls", "reserve",
        "controller", "flow",
    ),
    "impact": (
        "mw", "gw", "customers", "load shed", "loss", "lost", "outage",
        "unavailable", "affected", "reduction", "derate", "hours", "percent",
    ),
    "mitigation": (
        "recommend", "recommendation", "recommended", "mitigation", "mitigate",
        "corrective", "action", "should", "must", "prevent", "future",
        "guideline", "winterization", "reliability standard",
    ),
}

# Directed semantic transitions.  They are deliberately independent of report
# order: a report may state an impact before explaining its root cause.
CAUSAL_TRANSITIONS = {
    ("root_cause", "trigger_event"): "causes",
    ("root_cause", "propagation_or_response"): "enables_propagation",
    ("trigger_event", "propagation_or_response"): "propagates_to",
    ("trigger_event", "impact"): "results_in",
    ("propagation_or_response", "impact"): "results_in",
    ("impact", "mitigation"): "motivates_mitigation",
    ("root_cause", "mitigation"): "addressed_by",
}

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in",
    "is", "it", "of", "on", "or", "that", "the", "their", "this", "to",
    "was", "were", "with",
}
TOKEN_RE = re.compile(r"[a-z0-9]+(?:[-'][a-z0-9]+)?", re.I)
QUANTITY_RE = re.compile(r"\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:mw|gw|kv|hz|%)\b", re.I)


def _tokens(text: str) -> tuple[str, ...]:
    return tuple(token.lower() for token in TOKEN_RE.findall(text) if token.lower() not in STOPWORDS)


def _minmax(values: Sequence[float]) -> list[float]:
    if not values:
        return []
    low, high = min(values), max(values)
    if math.isclose(low, high):
        return [0.0 for _ in values]
    return [(value - low) / (high - low) for value in values]


def _unit_scale(values: Sequence[float]) -> list[float]:
    """Scale non-negative evidence without erasing a constant positive cue."""
    high = max(values, default=0.0)
    return [value / high for value in values] if high > 0 else [0.0 for _ in values]


def _jaccard(left: str, right: str) -> float:
    a, b = set(_tokens(left)), set(_tokens(right))
    return len(a & b) / len(a | b) if a or b else 0.0


def _role_hits(text: str, role: str) -> float:
    lower = text.lower()
    score = sum(1.0 + 0.15 * max(0, len(term.split()) - 1) for term in ROLE_TERMS[role] if term in lower)
    if role == "impact" and QUANTITY_RE.search(lower):
        score += 0.8
    return score


@dataclass(frozen=True)
class SentenceNode:
    sid: str
    text: str
    position: int
    role_scores: tuple[tuple[str, float], ...]
    dominant_role: str | None

    def role_score(self, role: str) -> float:
        return dict(self.role_scores).get(role, 0.0)


@dataclass(frozen=True)
class CausalEdge:
    source: str
    target: str
    relation: str
    weight: float

    @property
    def key(self) -> tuple[str, str, str]:
        return self.source, self.target, self.relation


class CausalEventGraph:
    """A deterministic sentence-level causal event graph.

    Nodes retain all role scores, but edges use each node's highest-confidence
    role to avoid manufacturing multiple contradictory transitions.  The graph
    is an auditable proxy graph, not a claim of ground-truth causality.
    """

    def __init__(self, nodes: Sequence[SentenceNode], edges: Sequence[CausalEdge]):
        ids = [node.sid for node in nodes]
        if len(ids) != len(set(ids)):
            raise ValueError("sentence ids must be unique")
        known = set(ids)
        if any(edge.source not in known or edge.target not in known for edge in edges):
            raise ValueError("every edge endpoint must reference an existing node")
        self.nodes = tuple(sorted(nodes, key=lambda node: node.position))
        self.edges = tuple(sorted(edges, key=lambda edge: edge.key))

    @classmethod
    def from_sentences(
        cls,
        sentences: Sequence[Mapping[str, object]],
        silver_role_evidence: Mapping[str, Sequence[object]] | None = None,
        *,
        max_distance: int = 12,
    ) -> "CausalEventGraph":
        if max_distance < 1:
            raise ValueError("max_distance must be positive")
        if not sentences:
            return cls([], [])

        parsed: list[tuple[str, str, int]] = []
        for position, sentence in enumerate(sentences):
            sid = str(sentence.get("sid", "")).strip()
            text = str(sentence.get("text", "")).strip()
            if not sid or not text:
                raise ValueError("every sentence requires non-empty sid and text")
            parsed.append((sid, text, position))
        if len({sid for sid, _, _ in parsed}) != len(parsed):
            raise ValueError("sentence ids must be unique")

        silver: dict[str, set[str]] = {role: set() for role in ROLES}
        for role, records in (silver_role_evidence or {}).items():
            if role not in silver:
                continue
            for record in records:
                sid = str(record.get("sid", "")) if isinstance(record, Mapping) else str(record)
                if sid:
                    silver[role].add(sid)

        raw_by_role = {
            role: [_role_hits(text, role) for _, text, _ in parsed]
            for role in ROLES
        }
        normalized = {role: _unit_scale(values) for role, values in raw_by_role.items()}
        nodes: list[SentenceNode] = []
        for index, (sid, text, position) in enumerate(parsed):
            scores = {
                role: max(normalized[role][index], 1.0 if sid in silver[role] else 0.0)
                for role in ROLES
            }
            silver_roles = [role for role in ROLES if sid in silver[role]]
            best_score = max(scores.values())
            # Explicit role evidence takes precedence over a lexical tie.  This
            # does not change its provenance: it remains optional silver input.
            dominant = silver_roles[0] if silver_roles else (
                next((role for role in ROLES if scores[role] == best_score), None)
                if best_score > 0 else None
            )
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
                    source.role_score(source.dominant_role),
                    target.role_score(target.dominant_role),
                )
                weight = 0.45 * proximity + 0.30 * overlap + 0.25 * confidence
                edges.append(CausalEdge(source.sid, target.sid, relation, round(weight, 12)))
        return cls(nodes, edges)

    def node(self, sid: str) -> SentenceNode:
        for node in self.nodes:
            if node.sid == sid:
                return node
        raise KeyError(sid)

    def intervene(
        self,
        *,
        remove_nodes: Iterable[str] = (),
        remove_edges: Iterable[tuple[str, str, str]] = (),
    ) -> "CausalEventGraph":
        """Return a new graph after a deterministic structural intervention."""
        removed_nodes = set(remove_nodes)
        unknown = removed_nodes - {node.sid for node in self.nodes}
        if unknown:
            raise KeyError(f"unknown intervention nodes: {sorted(unknown)}")
        removed_edges = set(remove_edges)
        return CausalEventGraph(
            [node for node in self.nodes if node.sid not in removed_nodes],
            [
                edge
                for edge in self.edges
                if edge.source not in removed_nodes
                and edge.target not in removed_nodes
                and edge.key not in removed_edges
            ],
        )

    def causal_flow(self) -> float:
        """Total typed causal support retained by the graph."""
        return sum(edge.weight for edge in self.edges)

    def graph_signal(self) -> dict[str, float]:
        weighted_degree = {node.sid: 0.0 for node in self.nodes}
        for edge in self.edges:
            weighted_degree[edge.source] += edge.weight
            weighted_degree[edge.target] += edge.weight
        scaled = _minmax([weighted_degree[node.sid] for node in self.nodes])
        return {node.sid: value for node, value in zip(self.nodes, scaled)}

    def counterfactual_sensitivity(self) -> dict[str, float]:
        """Normalize the causal-flow loss from deleting each sentence node."""
        original = self.causal_flow()
        if original <= 0:
            return {node.sid: 0.0 for node in self.nodes}
        raw = [max(0.0, original - self.intervene(remove_nodes=[node.sid]).causal_flow()) for node in self.nodes]
        scaled = _minmax(raw)
        return {node.sid: value for node, value in zip(self.nodes, scaled)}


@dataclass(frozen=True)
class SelectedSentence:
    sid: str
    text: str
    position: int
    dominant_role: str | None
    score: float
    selection_reason: str


@dataclass(frozen=True)
class SummaryResult:
    sentences: tuple[SelectedSentence, ...]
    selection_order: tuple[str, ...]
    covered_role_groups: tuple[str, ...]

    @property
    def text(self) -> str:
        return " ".join(sentence.text for sentence in self.sentences)


class ConstrainedExtractiveSummarizer:
    """Score graph nodes and select a non-redundant, role-covered summary."""

    ROLE_GROUPS = {
        "cause_or_trigger": ("root_cause", "trigger_event"),
        "propagation_or_impact": ("propagation_or_response", "impact"),
        "mitigation": ("mitigation",),
    }

    def __init__(
        self,
        *,
        relevance_weight: float = 0.30,
        role_weight: float = 0.20,
        graph_weight: float = 0.20,
        counterfactual_weight: float = 0.25,
        position_weight: float = 0.05,
        redundancy_penalty: float = 0.35,
    ) -> None:
        weights = (relevance_weight, role_weight, graph_weight, counterfactual_weight, position_weight)
        if any(weight < 0 for weight in weights) or not math.isclose(sum(weights), 1.0, abs_tol=1e-9):
            raise ValueError("non-redundancy weights must be non-negative and sum to one")
        if redundancy_penalty < 0:
            raise ValueError("redundancy_penalty must be non-negative")
        self.weights = weights
        self.redundancy_penalty = redundancy_penalty

    @staticmethod
    def _relevance(nodes: Sequence[SentenceNode], query: str | None) -> dict[str, float]:
        document_counts = Counter(token for node in nodes for token in set(_tokens(node.text)))
        if query:
            focus = Counter(_tokens(query))
        else:
            focus = document_counts
        raw = []
        for node in nodes:
            terms = set(_tokens(node.text))
            denominator = math.sqrt(max(1, len(terms))) * math.sqrt(max(1, sum(focus.values())))
            raw.append(sum(focus[token] for token in terms) / denominator)
        return {node.sid: value for node, value in zip(nodes, _minmax(raw))}

    def summarize(self, graph: CausalEventGraph, *, budget: int = 5, query: str | None = None) -> SummaryResult:
        if budget < 1:
            raise ValueError("budget must be positive")
        if not graph.nodes:
            return SummaryResult((), (), ())
        budget = min(budget, len(graph.nodes))
        relevance = self._relevance(graph.nodes, query)
        graph_signal = graph.graph_signal()
        counterfactual = graph.counterfactual_sensitivity()
        role = {node.sid: max(dict(node.role_scores).values()) for node in graph.nodes}
        position = {node.sid: 1.0 / (1.0 + node.position) for node in graph.nodes}
        rw, rolew, gw, cfw, pw = self.weights
        base = {
            node.sid: rw * relevance[node.sid]
            + rolew * role[node.sid]
            + gw * graph_signal[node.sid]
            + cfw * counterfactual[node.sid]
            + pw * position[node.sid]
            for node in graph.nodes
        }
        by_sid = {node.sid: node for node in graph.nodes}
        selected: list[str] = []
        reasons: dict[str, str] = {}

        # Reserve one sentence for each causal-function group when the budget
        # permits and a corresponding node exists.
        if budget >= len(self.ROLE_GROUPS):
            for group, group_roles in self.ROLE_GROUPS.items():
                candidates = [
                    node for node in graph.nodes
                    if node.sid not in selected and node.dominant_role in group_roles
                ]
                if candidates:
                    winner = max(candidates, key=lambda node: (base[node.sid], -node.position, node.sid))
                    selected.append(winner.sid)
                    reasons[winner.sid] = f"required_role_group:{group}"

        def adjusted(node: SentenceNode) -> tuple[float, int, str]:
            redundancy = max((_jaccard(node.text, by_sid[sid].text) for sid in selected), default=0.0)
            return base[node.sid] - self.redundancy_penalty * redundancy, -node.position, node.sid

        while len(selected) < budget:
            remaining = [node for node in graph.nodes if node.sid not in selected]
            winner = max(remaining, key=adjusted)
            selected.append(winner.sid)
            reasons[winner.sid] = "highest_adjusted_score"

        selection_order = tuple(selected)
        ordered = sorted((by_sid[sid] for sid in selected), key=lambda node: node.position)
        covered = tuple(
            group
            for group, roles in self.ROLE_GROUPS.items()
            if any(by_sid[sid].dominant_role in roles for sid in selected)
        )
        output = tuple(
            SelectedSentence(
                sid=node.sid,
                text=node.text,
                position=node.position,
                dominant_role=node.dominant_role,
                score=base[node.sid],
                selection_reason=reasons[node.sid],
            )
            for node in ordered
        )
        return SummaryResult(output, selection_order, covered)


def build_and_summarize(
    sentences: Sequence[Mapping[str, object]],
    *,
    silver_role_evidence: Mapping[str, Sequence[object]] | None = None,
    budget: int = 5,
    query: str | None = None,
) -> tuple[CausalEventGraph, SummaryResult]:
    """Convenience entry point used by future benchmark runners."""
    graph = CausalEventGraph.from_sentences(sentences, silver_role_evidence)
    return graph, ConstrainedExtractiveSummarizer().summarize(graph, budget=budget, query=query)
