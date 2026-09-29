"""Redesigned typed-path utilities for the RSI freeze-before-eval study."""
from __future__ import annotations

import math
from typing import Mapping, Sequence

UTILITIES = (
    "historical",
    "gated_relevance",
    "end_stage",
    "length_damped",
    "gated_length",
)

STAGE_WEIGHT = {
    "root_cause": 0.75,
    "trigger_event": 0.75,
    "propagation_or_response": 1.0,
    "impact": 1.5,
    "mitigation": 1.5,
}


def minmax(values: Sequence[float]) -> list[float]:
    if not values:
        return []
    low, high = min(values), max(values)
    if math.isclose(low, high):
        return [0.0 for _ in values]
    return [(value - low) / (high - low) for value in values]


def _as_map(sids: Sequence[str], values: Sequence[float]) -> dict[str, float]:
    return {sid: value for sid, value in zip(sids, minmax(values))}


def apply_utility(
    name: str,
    raw_loss: Mapping[str, float],
    nodes: Sequence[object],
    relevance: Mapping[str, float],
    word_counts: Mapping[str, int],
) -> dict[str, float]:
    if name not in UTILITIES:
        raise ValueError(f"unknown path utility: {name}")
    sids = [node.sid for node in nodes]
    raw = [float(raw_loss.get(sid, 0.0)) for sid in sids]
    if name == "historical":
        scaled = raw
    elif name == "gated_relevance":
        scaled = [value * float(relevance.get(sid, 0.0)) for sid, value in zip(sids, raw)]
    elif name == "end_stage":
        scaled = []
        for node, value in zip(nodes, raw):
            weight = STAGE_WEIGHT.get(getattr(node, "dominant_role", None), 0.25)
            scaled.append(value * weight)
    elif name == "length_damped":
        scaled = [
            value / math.log(1.0 + max(1, int(word_counts.get(sid, 1))))
            for sid, value in zip(sids, raw)
        ]
    else:
        scaled = [
            value
            * float(relevance.get(sid, 0.0))
            / math.log(1.0 + max(1, int(word_counts.get(sid, 1))))
            for sid, value in zip(sids, raw)
        ]
    return _as_map(sids, scaled)
