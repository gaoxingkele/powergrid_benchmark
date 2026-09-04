"""Leakage-audited graph construction for the P4 GCN/HGCN stage.

This module constructs graph structure only.  It deliberately does not load a
whole dataset or choose customer identities: those source-bound decisions must
be present in a frozen data manifest before a pilot or formal run.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Mapping, Sequence

import torch


@dataclass(frozen=True)
class EdgeProvenance:
    graph_kind: str
    node_ids: tuple[str, ...]
    train_start: int
    train_stop_exclusive: int
    source_rule: str
    source_manifest_sha256: str
    training_values_sha256: str | None
    threshold: float | None
    min_overlap: int | None
    add_self_loops_for_convolution: bool
    adjacency_sha256: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _validate_node_ids(node_ids: Sequence[str], n_nodes: int) -> tuple[str, ...]:
    frozen = tuple(str(item) for item in node_ids)
    if len(frozen) != n_nodes:
        raise ValueError(f"expected {n_nodes} node IDs, received {len(frozen)}")
    if any(not item.strip() for item in frozen) or len(set(frozen)) != len(frozen):
        raise ValueError("node IDs must be non-empty and unique")
    return frozen


def adjacency_sha256(adjacency: torch.Tensor) -> str:
    """Return a stable digest of an unnormalised binary adjacency matrix."""
    matrix = adjacency.detach().to(dtype=torch.uint8, device="cpu").contiguous()
    header = json.dumps(list(matrix.shape), separators=(",", ":")).encode("ascii")
    return sha256(header + b"\0" + bytes(matrix.numpy().tobytes())).hexdigest()


def _validate_sha256(value: str) -> str:
    digest = value.strip().lower()
    if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest):
        raise ValueError("source_manifest_sha256 must be a 64-character hexadecimal digest")
    return digest


def hierarchy_graph(
    node_ids: Sequence[str],
    parent_by_child: Mapping[str, str],
    *,
    train_stop_exclusive: int,
    source_manifest_sha256: str,
) -> tuple[torch.Tensor, EdgeProvenance]:
    """Build the undirected structural graph from an explicit parent mapping.

    The mapping is mandatory provenance.  No parent, region membership, or
    physical feeder edge is inferred from load values or node names.
    """
    ids = _validate_node_ids(node_ids, len(node_ids))
    index = {node_id: position for position, node_id in enumerate(ids)}
    adjacency = torch.zeros((len(ids), len(ids)), dtype=torch.float64)
    for child, parent in parent_by_child.items():
        if child not in index or parent not in index:
            raise ValueError(f"hierarchy edge references an unknown node: {child!r}->{parent!r}")
        if child == parent:
            raise ValueError("hierarchy provenance cannot contain self-parent edges")
        i, j = index[child], index[parent]
        adjacency[i, j] = adjacency[j, i] = 1.0
    if len(ids) > 1 and len(parent_by_child) != len(ids) - 1:
        raise ValueError("the frozen hierarchy must contain exactly n_nodes-1 child-parent edges")
    if len(ids) > 1:
        reached, frontier = {0}, [0]
        while frontier:
            current = frontier.pop()
            for neighbour in torch.nonzero(adjacency[current], as_tuple=False).flatten().tolist():
                if neighbour not in reached:
                    reached.add(neighbour)
                    frontier.append(neighbour)
        if len(reached) != len(ids):
            raise ValueError("the frozen hierarchy edges do not form one connected tree")
    provenance = EdgeProvenance(
        graph_kind="documented_hierarchy",
        node_ids=ids,
        train_start=0,
        train_stop_exclusive=int(train_stop_exclusive),
        source_rule="explicit source-manifest child-parent relationships; no value-derived edges",
        source_manifest_sha256=_validate_sha256(source_manifest_sha256),
        training_values_sha256=None,
        threshold=None,
        min_overlap=None,
        add_self_loops_for_convolution=True,
        adjacency_sha256=adjacency_sha256(adjacency),
    )
    return adjacency, provenance


def training_correlation_graph(
    values: torch.Tensor,
    node_ids: Sequence[str],
    *,
    train_stop_exclusive: int,
    source_manifest_sha256: str,
    threshold: float = 0.7,
    min_overlap: int = 168,
) -> tuple[torch.Tensor, EdgeProvenance]:
    """Construct an absolute-Pearson graph using rows before one cutoff only.

    ``values`` has shape [time, node].  Missing values are handled pairwise,
    but every retained edge must have ``min_overlap`` finite training rows.
    Validation/test values at or after the cutoff are never indexed.
    """
    if values.ndim != 2:
        raise ValueError("values must have shape [time, node]")
    if not 1 <= train_stop_exclusive <= values.shape[0]:
        raise ValueError("train_stop_exclusive must identify a non-empty prefix")
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold must be in [0, 1]")
    if min_overlap < 2:
        raise ValueError("min_overlap must be at least two")
    ids = _validate_node_ids(node_ids, values.shape[1])
    train = values[:train_stop_exclusive].detach().to(dtype=torch.float64, device="cpu")
    training_digest = sha256(bytes(train.contiguous().numpy().tobytes())).hexdigest()
    n_nodes = train.shape[1]
    adjacency = torch.zeros((n_nodes, n_nodes), dtype=torch.float64)
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            mask = torch.isfinite(train[:, i]) & torch.isfinite(train[:, j])
            if int(mask.sum()) < min_overlap:
                continue
            x, y = train[mask, i], train[mask, j]
            x, y = x - x.mean(), y - y.mean()
            denominator = torch.linalg.vector_norm(x) * torch.linalg.vector_norm(y)
            if float(denominator) == 0.0:
                continue
            correlation = torch.dot(x, y) / denominator
            if float(torch.abs(correlation)) >= threshold:
                adjacency[i, j] = adjacency[j, i] = 1.0
    provenance = EdgeProvenance(
        graph_kind="training_only_absolute_pearson",
        node_ids=ids,
        train_start=0,
        train_stop_exclusive=int(train_stop_exclusive),
        source_rule="pairwise finite training-prefix rows only; validation/test rows excluded",
        source_manifest_sha256=_validate_sha256(source_manifest_sha256),
        training_values_sha256=training_digest,
        threshold=float(threshold),
        min_overlap=int(min_overlap),
        add_self_loops_for_convolution=True,
        adjacency_sha256=adjacency_sha256(adjacency),
    )
    return adjacency, provenance


def normalise_adjacency(adjacency: torch.Tensor, *, add_self_loops: bool = True) -> torch.Tensor:
    """Return symmetric D^-1/2 (A+I) D^-1/2 after strict validation."""
    if adjacency.ndim != 2 or adjacency.shape[0] != adjacency.shape[1]:
        raise ValueError("adjacency must be square")
    if not torch.isfinite(adjacency).all() or (adjacency < 0).any():
        raise ValueError("adjacency must be finite and non-negative")
    if not torch.allclose(adjacency, adjacency.T, atol=1e-12, rtol=0.0):
        raise ValueError("adjacency must be symmetric")
    matrix = adjacency
    if add_self_loops:
        matrix = matrix + torch.eye(matrix.shape[0], dtype=matrix.dtype, device=matrix.device)
    degree = matrix.sum(dim=1)
    if (degree <= 0).any():
        raise ValueError("normalised adjacency cannot contain zero-degree nodes")
    inv_sqrt = degree.rsqrt()
    return inv_sqrt[:, None] * matrix * inv_sqrt[None, :]
