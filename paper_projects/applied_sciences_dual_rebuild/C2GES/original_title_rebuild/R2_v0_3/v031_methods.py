"""v0.3.1 method closure with explicit counterfactual work parameters."""

from __future__ import annotations

from v03_methods import (  # frozen v0.3 functions reused without modification
    RedundancyCache,
    build_graph_v03,
    constrained_select,
    redundancy,
    relevance_scores,
)
from counterfactual_paths_v031 import path_counterfactual_sensitivity


def score_channels(
    graph,
    *,
    path_min_edges: int,
    path_max_edges: int,
    path_max_paths: int,
    path_max_expansions: int,
) -> dict[str, dict[str, float]]:
    """Return all channels while consuming every registered CF parameter."""
    return {
        "relevance": relevance_scores(graph.nodes),
        "role": {node.sid: max(dict(node.role_scores).values()) for node in graph.nodes},
        "graph": graph.graph_signal(),
        "counterfactual": path_counterfactual_sensitivity(
            graph,
            min_edges=path_min_edges,
            max_edges=path_max_edges,
            max_paths=path_max_paths,
            max_expansions=path_max_expansions,
        ),
        "position": {node.sid: 1.0 / (1.0 + node.position) for node in graph.nodes},
    }


__all__ = [
    "RedundancyCache",
    "build_graph_v03",
    "constrained_select",
    "redundancy",
    "score_channels",
]
