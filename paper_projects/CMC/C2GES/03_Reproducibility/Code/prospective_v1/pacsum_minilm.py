"""Clean-room PacSum-style scorer for the prospective C2GES comparison.

This module is derived from the equations in Zheng and Lapata (ACL 2019), not
from the authors' unlicensed source repository. Embeddings are supplied by the
caller so the same frozen encoder and long-unit policy can be shared across
PacSum-MiniLM and Semantic-MMR.
"""

from __future__ import annotations

import re
from typing import Any, Mapping, Sequence

import numpy as np


WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*")
TUNING_GRID = tuple(
    {"lambda_preceding": preceding, "lambda_following": 1.0, "beta": beta}
    for preceding in (-2.0, -1.0, 0.0)
    for beta in (0.0, 0.3, 0.6)
)


def pacsum_scores(
    embeddings: np.ndarray,
    *,
    lambda_preceding: float,
    lambda_following: float,
    beta: float,
) -> np.ndarray:
    """Compute thresholded, position-augmented directed degree centrality."""
    matrix = np.asarray(embeddings, dtype=np.float64)
    if matrix.ndim != 2 or matrix.shape[0] == 0:
        raise ValueError("embeddings must be a non-empty two-dimensional array")
    if not 0.0 <= beta <= 1.0:
        raise ValueError("beta must lie in [0, 1]")
    count = matrix.shape[0]
    if count == 1:
        return np.zeros(1, dtype=np.float64)
    similarity = matrix @ matrix.T
    off_diagonal = similarity[~np.eye(count, dtype=bool)]
    threshold = float(off_diagonal.min() + beta * (off_diagonal.max() - off_diagonal.min()))
    edges = np.maximum(similarity - threshold, 0.0)
    np.fill_diagonal(edges, 0.0)
    scores = np.empty(count, dtype=np.float64)
    for index in range(count):
        preceding = float(edges[index, :index].sum())
        following = float(edges[index, index + 1 :].sum())
        scores[index] = lambda_preceding * preceding + lambda_following * following
    return scores


def select_word_budget(
    units: Sequence[Mapping[str, Any]], scores: Sequence[float], word_budget: int
) -> list[Mapping[str, Any]]:
    """Rank once and select complete units without truncation or top-k capping."""
    if len(units) != len(scores):
        raise ValueError("unit and score counts differ")
    if word_budget <= 0:
        raise ValueError("word budget must be positive")
    ranked = sorted(
        zip(units, scores),
        key=lambda pair: (-float(pair[1]), int(pair[0].get("source_order", 0)), str(pair[0]["sid"])),
    )
    selected: list[Mapping[str, Any]] = []
    used = 0
    for unit, _ in ranked:
        words = int(unit.get("word_count") or len(WORD_RE.findall(str(unit["text"]))))
        if words <= word_budget - used:
            selected.append(unit)
            used += words
    return selected
