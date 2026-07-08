from __future__ import annotations

from math import sqrt
from typing import Sequence


def _validate_equal_length(y_true: Sequence[float], y_pred: Sequence[float]) -> None:
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length")
    if not y_true:
        raise ValueError("metric inputs must not be empty")


def mae(y_true: Sequence[float], y_pred: Sequence[float]) -> float:
    _validate_equal_length(y_true, y_pred)
    return sum(abs(a - b) for a, b in zip(y_true, y_pred)) / len(y_true)


def rmse(y_true: Sequence[float], y_pred: Sequence[float]) -> float:
    _validate_equal_length(y_true, y_pred)
    return sqrt(sum((a - b) ** 2 for a, b in zip(y_true, y_pred)) / len(y_true))
