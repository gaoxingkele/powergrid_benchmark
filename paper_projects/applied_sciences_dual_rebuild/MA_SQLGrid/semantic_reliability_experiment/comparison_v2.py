"""Frozen v2 result-comparison contract (no filesystem access)."""

from __future__ import annotations

import math
import re
from collections import defaultdict
from typing import Any

ABS_TOL = 1e-6
REL_TOL = 1e-9
COLUMN_POLICY = "headers_are_diagnostic_only_denotation_is_primary"


def numeric(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def value_equal(a: Any, b: Any, *, strict_numeric: bool = False) -> bool:
    if a is None or b is None:
        return a is None and b is None
    if numeric(a) and numeric(b):
        if not math.isfinite(float(a)) or not math.isfinite(float(b)):
            return False
        return a == b if strict_numeric else math.isclose(float(a), float(b), rel_tol=REL_TOL, abs_tol=ABS_TOL)
    return type(a) is type(b) and a == b


def row_equal(a: tuple[Any, ...], b: tuple[Any, ...], *, strict_numeric: bool = False) -> bool:
    return len(a) == len(b) and all(value_equal(x, y, strict_numeric=strict_numeric) for x, y in zip(a, b))


def nonnumeric_signature(row: tuple[Any, ...]) -> tuple[Any, ...]:
    # Numeric positions use one common marker; exact nonnumeric fields define groups.
    return tuple(("__NUMERIC__",) if numeric(v) else (type(v).__name__, v) for v in row)


def _perfect_bipartite(left: list[tuple[Any, ...]], right: list[tuple[Any, ...]], *, strict_numeric: bool) -> bool:
    if len(left) != len(right): return False
    edges = [[j for j, b in enumerate(right) if row_equal(a, b, strict_numeric=strict_numeric)] for a in left]
    if any(not e for e in edges): return False
    match = [-1] * len(right)
    def augment(i: int, seen: set[int]) -> bool:
        for j in edges[i]:
            if j in seen: continue
            seen.add(j)
            if match[j] < 0 or augment(match[j], seen): match[j] = i; return True
        return False
    # Fewest-candidate rows first makes matching deterministic and reduces work.
    for i in sorted(range(len(left)), key=lambda k: (len(edges[k]), k)):
        if not augment(i, set()): return False
    return True


def rows_equal(pred: list[tuple[Any, ...]], gold: list[tuple[Any, ...]], *, ordered: bool, strict_numeric: bool = False) -> bool:
    if len(pred) != len(gold): return False
    if ordered:
        return all(row_equal(a, b, strict_numeric=strict_numeric) for a, b in zip(pred, gold))
    lp: dict[tuple[Any, ...], list[tuple[Any, ...]]] = defaultdict(list)
    lg: dict[tuple[Any, ...], list[tuple[Any, ...]]] = defaultdict(list)
    for row in pred: lp[nonnumeric_signature(row)].append(row)
    for row in gold: lg[nonnumeric_signature(row)].append(row)
    if set(lp) != set(lg): return False
    return all(_perfect_bipartite(lp[key], lg[key], strict_numeric=strict_numeric) for key in sorted(lp, key=repr))


def normalize_header(label: str) -> str:
    return re.sub(r"\s+", "", label.strip().strip('`\"[]')).lower()


def header_diagnostics(predicted: list[str], gold: list[str], metadata: list[str]) -> dict[str, bool]:
    p, g, m = map(lambda xs: [normalize_header(x.split(".")[-1]) for x in xs], (predicted, gold, metadata))
    return {"prediction_vs_gold_header_match": p == g, "prediction_vs_metadata_header_match": p == m, "gold_vs_metadata_header_match": g == m}

