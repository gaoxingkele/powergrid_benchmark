"""Typed-path counterfactual signal with fully threaded v0.3.1 work limits.

This successor module leaves the v0.3 frozen implementation byte-for-byte
unchanged while making every registered enumeration parameter operative.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


ROLE_STAGE = {
    "root_cause": 0,
    "trigger_event": 1,
    "propagation_or_response": 2,
    "impact": 3,
    "mitigation": 4,
}
START_ROLES = {"root_cause", "trigger_event"}
END_ROLES = {"impact", "mitigation"}


@dataclass(frozen=True)
class TypedPath:
    nodes: tuple[str, ...]
    relations: tuple[str, ...]
    weights: tuple[float, ...]
    strength: float


class PathEnumerationLimitError(RuntimeError):
    """Raised before a graph can exceed registered deterministic work limits."""


def _minmax(values: list[float]) -> list[float]:
    if not values:
        return []
    low, high = min(values), max(values)
    if math.isclose(low, high):
        return [0.0 for _ in values]
    return [(value - low) / (high - low) for value in values]


def qualified_typed_paths(
    graph,
    *,
    min_edges: int,
    max_edges: int,
    max_paths: int,
    max_expansions: int,
) -> tuple[TypedPath, ...]:
    """Enumerate simple stage-monotone paths under explicit fail-closed limits."""
    if min_edges < 2 or max_edges < min_edges:
        raise ValueError("require 2 <= min_edges <= max_edges")
    if max_paths < 1 or max_expansions < 1:
        raise ValueError("path and expansion limits must be positive")
    by_sid = {node.sid: node for node in graph.nodes}
    outgoing: dict[str, list] = {sid: [] for sid in by_sid}
    for edge in graph.edges:
        source_role = by_sid[edge.source].dominant_role
        target_role = by_sid[edge.target].dominant_role
        if source_role not in ROLE_STAGE or target_role not in ROLE_STAGE:
            continue
        if ROLE_STAGE[target_role] <= ROLE_STAGE[source_role]:
            continue
        outgoing[edge.source].append(edge)
    for sid in outgoing:
        outgoing[sid].sort(key=lambda edge: edge.key)

    paths: list[TypedPath] = []
    expansions = 0

    def visit(
        node_sid: str,
        node_path: tuple[str, ...],
        relation_path: tuple[str, ...],
        weights: tuple[float, ...],
    ) -> None:
        nonlocal expansions
        expansions += 1
        if expansions > max_expansions:
            raise PathEnumerationLimitError(
                f"typed-path expansion limit exceeded ({max_expansions}); graph rejected fail-closed"
            )
        edge_count = len(weights)
        end_role = by_sid[node_sid].dominant_role
        if edge_count >= min_edges and end_role in END_ROLES:
            geometric = math.prod(weights) ** (1.0 / edge_count)
            stages = {ROLE_STAGE[by_sid[sid].dominant_role] for sid in node_path}
            coverage = (max(stages) - min(stages)) / 4.0
            if len(paths) >= max_paths:
                raise PathEnumerationLimitError(
                    f"typed-path count limit exceeded ({max_paths}); graph rejected fail-closed"
                )
            paths.append(TypedPath(node_path, relation_path, weights, geometric * coverage))
        if edge_count == max_edges:
            return
        for edge in outgoing.get(node_sid, []):
            if edge.target in node_path:
                continue
            visit(
                edge.target,
                node_path + (edge.target,),
                relation_path + (edge.relation,),
                weights + (float(edge.weight),),
            )

    for node in graph.nodes:
        if node.dominant_role in START_ROLES:
            visit(node.sid, (node.sid,), (), ())
    unique = {path.nodes: path for path in paths}
    return tuple(unique[key] for key in sorted(unique))


def path_counterfactual_sensitivity(
    graph,
    *,
    min_edges: int,
    max_edges: int,
    max_paths: int,
    max_expansions: int,
) -> dict[str, float]:
    """Marginal path-strength loss after deletion of each sentence node."""
    paths = qualified_typed_paths(
        graph,
        min_edges=min_edges,
        max_edges=max_edges,
        max_paths=max_paths,
        max_expansions=max_expansions,
    )
    raw = {
        node.sid: sum(path.strength for path in paths if node.sid in path.nodes)
        for node in graph.nodes
    }
    scaled = _minmax([raw[node.sid] for node in graph.nodes])
    return {node.sid: value for node, value in zip(graph.nodes, scaled)}
