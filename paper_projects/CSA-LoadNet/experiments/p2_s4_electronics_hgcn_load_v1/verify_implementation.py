"""Deterministic invariant checks; this is not an experiment run."""

from __future__ import annotations

import json
from pathlib import Path

import torch

try:  # package import
    from .graph_data import hierarchy_graph, training_correlation_graph
    from .models import (
        EuclideanGCNForecaster,
        HyperbolicGCNForecaster,
        PoincareBall,
        matched_parameter_audit,
    )
except ImportError:  # direct script execution
    from graph_data import hierarchy_graph, training_correlation_graph
    from models import (
        EuclideanGCNForecaster,
        HyperbolicGCNForecaster,
        PoincareBall,
        matched_parameter_audit,
    )


ROOT = Path(__file__).resolve().parent


def check() -> dict[str, object]:
    contract = json.loads((ROOT / "implementation_contract.json").read_text(encoding="utf-8"))
    assert contract["status"] == "IMPLEMENTATION_CONTRACT_FROZEN_NO_RESULTS"

    torch.manual_seed(20260904)
    training = torch.randn(240, 6, dtype=torch.float64)
    future_a = torch.randn(40, 6, dtype=torch.float64)
    future_b = torch.randn(40, 6, dtype=torch.float64) * 1000
    nodes = ("DE", "FR", "IT", "ES", "NL", "PL")
    graph_a, provenance_a = training_correlation_graph(
        torch.cat((training, future_a)), nodes, train_stop_exclusive=240,
        source_manifest_sha256="0" * 64,
    )
    graph_b, provenance_b = training_correlation_graph(
        torch.cat((training, future_b)), nodes, train_stop_exclusive=240,
        source_manifest_sha256="0" * 64,
    )
    assert torch.equal(graph_a, graph_b)
    assert provenance_a.adjacency_sha256 == provenance_b.adjacency_sha256

    hierarchy, hierarchy_provenance = hierarchy_graph(
        ("root", "region", "leaf"),
        {"region": "root", "leaf": "region"},
        train_stop_exclusive=240,
        source_manifest_sha256="0" * 64,
    )
    assert int(hierarchy.sum().item()) == 4
    assert hierarchy_provenance.graph_kind == "documented_hierarchy"

    ball = PoincareBall()
    tangent = torch.randn(4, 3, dtype=torch.float64) * 0.05
    curvature = torch.tensor(1.0, dtype=torch.float64)
    recovered = ball.logmap0(ball.expmap0(tangent, curvature), curvature)
    assert torch.allclose(tangent, recovered, atol=1e-8, rtol=1e-6)

    adjacency = torch.tensor(
        [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]],
        dtype=torch.float32,
    )
    windows = torch.randn(3, 4, 168)
    calendar = torch.randn(3, 4)
    reports: dict[str, object] = {}
    for layers in (1, 2):
        for name, model in (
            ("euclidean", EuclideanGCNForecaster(4, layers)),
            ("hyperbolic_fixed", HyperbolicGCNForecaster(4, layers, "fixed_1")),
            ("hyperbolic_learnable", HyperbolicGCNForecaster(4, layers, "learnable")),
        ):
            prediction = model(windows, calendar, adjacency)
            identity_prediction = model(windows, calendar, torch.zeros_like(adjacency))
            assert prediction.shape == (3, 4)
            assert torch.isfinite(prediction).all()
            assert not torch.allclose(prediction, identity_prediction)
            assert not any("attention" in module_name.lower() for module_name, _ in model.named_modules())
            prediction.square().mean().backward()
            assert all(parameter.grad is None or torch.isfinite(parameter.grad).all() for parameter in model.parameters())
            reports[f"{name}_{layers}_layer_output_shape"] = list(prediction.shape)
        audit = matched_parameter_audit(4, layers, "learnable")
        assert float(audit["relative_difference"]) <= 0.10
        reports[f"parameter_audit_{layers}_layer"] = audit

    return {
        "status": "PASS",
        "scope": "implementation invariants only; NO_RESULTS",
        "train_only_graph_future_perturbation_invariant": True,
        "poincare_exp_log_round_trip": True,
        "adjacency_message_path_active_without_attention": True,
        "finite_forward_backward": True,
        "reports": reports,
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2, sort_keys=True))
