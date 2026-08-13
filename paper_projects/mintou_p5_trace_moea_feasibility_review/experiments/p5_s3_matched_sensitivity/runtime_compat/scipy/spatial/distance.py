"""NumPy implementations of the Euclidean distance calls used by pymoo 0.6.2."""

from __future__ import annotations

import numpy as np


def cdist(a, b, metric="euclidean", **kwargs):  # type: ignore[no-untyped-def]
    del kwargs
    left = np.asarray(a, dtype=float)
    right = np.asarray(b, dtype=float)
    delta = left[:, None, :] - right[None, :, :]
    squared = np.sum(delta * delta, axis=2)
    if metric in {"sqeuclidean", "sqe"}:
        return squared
    if metric in {"euclidean", "euclid", "eu"}:
        return np.sqrt(squared)
    raise NotImplementedError(f"metric {metric!r} is outside the p5_s3 compatibility surface")


def pdist(x, metric="euclidean", **kwargs):  # type: ignore[no-untyped-def]
    del kwargs
    values = np.asarray(x, dtype=float)
    n_rows = values.shape[0]
    out = []
    for i in range(n_rows - 1):
        delta = values[i + 1 :] - values[i]
        squared = np.sum(delta * delta, axis=1)
        if metric in {"sqeuclidean", "sqe"}:
            out.extend(squared.tolist())
        elif metric in {"euclidean", "euclid", "eu"}:
            out.extend(np.sqrt(squared).tolist())
        else:
            raise NotImplementedError(
                f"metric {metric!r} is outside the p5_s3 compatibility surface"
            )
    return np.asarray(out, dtype=float)


def squareform(values):  # type: ignore[no-untyped-def]
    array = np.asarray(values, dtype=float)
    if array.ndim == 2:
        if array.shape[0] != array.shape[1]:
            raise ValueError("distance matrix must be square")
        return array[np.triu_indices(array.shape[0], 1)]
    if array.ndim != 1:
        raise ValueError("squareform input must be a vector or square matrix")
    length = array.size
    n_rows = int((1 + np.sqrt(1 + 8 * length)) / 2)
    if n_rows * (n_rows - 1) // 2 != length:
        raise ValueError("invalid condensed distance-vector length")
    matrix = np.zeros((n_rows, n_rows), dtype=float)
    indices = np.triu_indices(n_rows, 1)
    matrix[indices] = array
    matrix[(indices[1], indices[0])] = array
    return matrix

