"""Matched Euclidean and hyperbolic graph-convolution forecasting models.

The HGCN uses the Poincare ball with sectional curvature ``-c`` (``c > 0``).
Each hyperbolic layer maps points to the origin tangent space, applies a shared
linear transform and adjacency message aggregation there, then maps the result
back to the ball.  It is therefore graph convolution, not dense attention.
"""

from __future__ import annotations

import math
from typing import Literal

import torch
from torch import nn
from torch.nn import functional as F

try:  # package import
    from .graph_data import normalise_adjacency
except ImportError:  # direct execution from this directory
    from graph_data import normalise_adjacency


CurvatureMode = Literal["fixed_1", "learnable"]


def count_parameters(module: nn.Module) -> int:
    return sum(parameter.numel() for parameter in module.parameters() if parameter.requires_grad)


class PoincareBall:
    """Origin maps for the Poincare ball of curvature ``-c``."""

    def __init__(self, *, eps: float = 1e-5, max_tangent_norm: float = 15.0) -> None:
        self.eps = float(eps)
        self.max_tangent_norm = float(max_tangent_norm)

    @staticmethod
    def _c(c: torch.Tensor, reference: torch.Tensor) -> torch.Tensor:
        return c.to(dtype=reference.dtype, device=reference.device).clamp_min(1e-8)

    def clip_tangent(self, value: torch.Tensor) -> torch.Tensor:
        norm = torch.linalg.vector_norm(value, dim=-1, keepdim=True).clamp_min(self.eps)
        scale = torch.clamp(self.max_tangent_norm / norm, max=1.0)
        return value * scale

    def project(self, point: torch.Tensor, c: torch.Tensor) -> torch.Tensor:
        curvature = self._c(c, point)
        radius = (1.0 - self.eps) / torch.sqrt(curvature)
        norm = torch.linalg.vector_norm(point, dim=-1, keepdim=True).clamp_min(self.eps)
        return point * torch.clamp(radius / norm, max=1.0)

    def expmap0(self, tangent: torch.Tensor, c: torch.Tensor) -> torch.Tensor:
        tangent = self.clip_tangent(tangent)
        curvature = self._c(c, tangent)
        root = torch.sqrt(curvature)
        norm = torch.linalg.vector_norm(tangent, dim=-1, keepdim=True).clamp_min(self.eps)
        mapped = torch.tanh(root * norm) * tangent / (root * norm)
        return self.project(mapped, curvature)

    def logmap0(self, point: torch.Tensor, c: torch.Tensor) -> torch.Tensor:
        curvature = self._c(c, point)
        point = self.project(point, curvature)
        root = torch.sqrt(curvature)
        norm = torch.linalg.vector_norm(point, dim=-1, keepdim=True).clamp_min(self.eps)
        argument = (root * norm).clamp(max=1.0 - self.eps)
        return torch.atanh(argument) * point / (root * norm)


class Curvature(nn.Module):
    """Positive ``c`` where the manifold sectional curvature is ``-c``."""

    def __init__(self, mode: CurvatureMode) -> None:
        super().__init__()
        self.mode = mode
        if mode == "fixed_1":
            self.register_buffer("fixed", torch.tensor(1.0))
            self.raw = None
        elif mode == "learnable":
            initial = math.log(math.expm1(1.0 - 1e-4))
            self.raw = nn.Parameter(torch.tensor(initial))
            self.register_buffer("fixed", torch.tensor(float("nan")))
        else:
            raise ValueError(f"unsupported curvature mode: {mode}")

    def forward(self) -> torch.Tensor:
        if self.raw is None:
            return self.fixed
        return F.softplus(self.raw) + 1e-4


class TemporalEncoder(nn.Module):
    """Shared 168-96-48 encoder inherited from the accepted CSA predecessor."""

    def __init__(self, window: int = 168, hidden: int = 48) -> None:
        super().__init__()
        if window != 168 or hidden != 48:
            raise ValueError("the identification pair freezes window=168 and hidden=48")
        self.network = nn.Sequential(nn.Linear(168, 96), nn.ReLU(), nn.Linear(96, 48), nn.ReLU())

    def forward(self, windows: torch.Tensor) -> torch.Tensor:
        return self.network(windows)


class PredictionHead(nn.Module):
    """Common 100-64-1 head: temporal, graph context, and four calendar terms."""

    def __init__(self) -> None:
        super().__init__()
        self.network = nn.Sequential(nn.Linear(100, 64), nn.ReLU(), nn.Linear(64, 1))

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        return self.network(features).squeeze(-1)


class EuclideanGraphLayer(nn.Module):
    def __init__(self, width: int = 48) -> None:
        super().__init__()
        self.linear = nn.Linear(width, width)

    def forward(self, points: torch.Tensor, adjacency: torch.Tensor) -> torch.Tensor:
        return F.relu(torch.einsum("ij,bjf->bif", adjacency, self.linear(points)))


class HyperbolicGraphLayer(nn.Module):
    def __init__(self, width: int = 48) -> None:
        super().__init__()
        self.linear = nn.Linear(width, width)

    def forward(
        self,
        points: torch.Tensor,
        adjacency: torch.Tensor,
        ball: PoincareBall,
        curvature: torch.Tensor,
    ) -> torch.Tensor:
        tangent = ball.logmap0(points, curvature)
        messages = torch.einsum("ij,bjf->bif", adjacency, self.linear(tangent))
        return ball.expmap0(F.relu(messages), curvature)


class _GraphForecaster(nn.Module):
    def __init__(self, n_nodes: int, layers: int) -> None:
        super().__init__()
        if n_nodes < 1 or layers not in {1, 2}:
            raise ValueError("n_nodes must be positive and layers must be one or two")
        self.n_nodes = n_nodes
        self.encoder = TemporalEncoder()
        self.head = PredictionHead()

    def _inputs(
        self, windows: torch.Tensor, calendar: torch.Tensor, adjacency: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        if windows.ndim != 3 or windows.shape[1:] != (self.n_nodes, 168):
            raise ValueError(f"windows must have shape [batch, {self.n_nodes}, 168]")
        if calendar.ndim != 2 or calendar.shape != (windows.shape[0], 4):
            raise ValueError("calendar must have shape [batch, 4]")
        if adjacency.shape != (self.n_nodes, self.n_nodes):
            raise ValueError("adjacency shape does not match the frozen node set")
        encoded = self.encoder(windows)
        graph = normalise_adjacency(adjacency).to(dtype=encoded.dtype, device=encoded.device)
        calendar_nodes = calendar[:, None, :].expand(-1, self.n_nodes, -1)
        return encoded, calendar_nodes, graph


class EuclideanGCNForecaster(_GraphForecaster):
    """Kipf-Welling-style adjacency aggregation sanity baseline."""

    def __init__(self, n_nodes: int, layers: int = 1) -> None:
        super().__init__(n_nodes, layers)
        self.graph_layers = nn.ModuleList(EuclideanGraphLayer() for _ in range(layers))

    def forward(self, windows: torch.Tensor, calendar: torch.Tensor, adjacency: torch.Tensor) -> torch.Tensor:
        encoded, calendar_nodes, graph = self._inputs(windows, calendar, adjacency)
        context = encoded
        for layer in self.graph_layers:
            context = layer(context, graph)
        if not torch.isfinite(context).all():
            raise FloatingPointError("non-finite Euclidean graph state")
        return self.head(torch.cat((encoded, context, calendar_nodes), dim=-1))


class HyperbolicGCNForecaster(_GraphForecaster):
    """Poincare-ball HGCN with explicit maps, curvature, and safeguards."""

    def __init__(self, n_nodes: int, layers: int = 1, curvature_mode: CurvatureMode = "fixed_1") -> None:
        super().__init__(n_nodes, layers)
        self.ball = PoincareBall()
        self.curvature = Curvature(curvature_mode)
        self.graph_layers = nn.ModuleList(HyperbolicGraphLayer() for _ in range(layers))

    def forward(self, windows: torch.Tensor, calendar: torch.Tensor, adjacency: torch.Tensor) -> torch.Tensor:
        encoded, calendar_nodes, graph = self._inputs(windows, calendar, adjacency)
        curvature = self.curvature()
        points = self.ball.expmap0(encoded / math.sqrt(encoded.shape[-1]), curvature)
        for layer in self.graph_layers:
            points = layer(points, graph, self.ball, curvature)
        context = self.ball.logmap0(points, curvature)
        if not torch.isfinite(context).all():
            raise FloatingPointError("non-finite hyperbolic graph state")
        return self.head(torch.cat((encoded, context, calendar_nodes), dim=-1))


def matched_parameter_audit(n_nodes: int, layers: int, curvature_mode: CurvatureMode) -> dict[str, float | int]:
    euclidean = EuclideanGCNForecaster(n_nodes, layers)
    hyperbolic = HyperbolicGCNForecaster(n_nodes, layers, curvature_mode)
    e_count, h_count = count_parameters(euclidean), count_parameters(hyperbolic)
    relative = abs(h_count - e_count) / e_count
    return {
        "euclidean_trainable_parameters": e_count,
        "hyperbolic_trainable_parameters": h_count,
        "absolute_difference": abs(h_count - e_count),
        "relative_difference": relative,
    }
