"""Exact integer binomial helper used by Das--Dennis directions."""

from __future__ import annotations

import math


def binom(n: float, k: float) -> float:
    n_int = int(n)
    k_int = int(k)
    if n_int != n or k_int != k or n_int < 0 or k_int < 0 or k_int > n_int:
        return float("nan")
    return float(math.comb(n_int, k_int))

