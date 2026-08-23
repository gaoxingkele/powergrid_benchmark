from __future__ import annotations

import sys
import unittest
from pathlib import Path

R1_CORE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R1_CORE))

from c2ges_offline import CausalEdge, CausalEventGraph, SentenceNode
from counterfactual_paths import (
    PathEnumerationLimitError,
    assert_not_identical_to_graph_signal,
    path_counterfactual_sensitivity,
    path_utility,
    qualified_typed_paths,
    raw_path_counterfactual_loss,
)


def node(sid: str, position: int, role: str) -> SentenceNode:
    roles = ("trigger_event", "root_cause", "propagation_or_response", "impact", "mitigation")
    return SentenceNode(
        sid=sid,
        text=f"Synthetic {sid} sentence contains deterministic engineering evidence.",
        position=position,
        role_scores=tuple((name, 1.0 if name == role else 0.0) for name in roles),
        dominant_role=role,
    )


class CounterfactualPathTests(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = CausalEventGraph(
            [
                node("r", 0, "root_cause"),
                node("t", 1, "trigger_event"),
                node("p", 2, "propagation_or_response"),
                node("i", 3, "impact"),
                node("x", 4, "root_cause"),
                node("m", 5, "mitigation"),
            ],
            [
                CausalEdge("r", "t", "causes", 1.0),
                CausalEdge("t", "p", "propagates_to", 1.0),
                CausalEdge("p", "i", "results_in", 1.0),
                # One-edge shortcut contributes degree but is intentionally not
                # a qualified multi-stage counterfactual path.
                CausalEdge("x", "m", "addressed_by", 1.0),
            ],
        )

    def test_equal_degree_can_have_different_cf_loss(self) -> None:
        graph_signal = self.graph.graph_signal()
        raw_cf = raw_path_counterfactual_loss(self.graph)
        self.assertEqual(graph_signal["r"], graph_signal["x"])
        self.assertGreater(raw_cf["r"], 0.0)
        self.assertEqual(raw_cf["x"], 0.0)
        assert_not_identical_to_graph_signal(self.graph)

    def test_only_multiedge_typed_paths_count(self) -> None:
        paths = qualified_typed_paths(self.graph)
        self.assertTrue(any(path.nodes == ("r", "t", "p", "i") for path in paths))
        self.assertFalse(any(path.nodes == ("x", "m") for path in paths))

    def test_intervention_loss_matches_paths_containing_node(self) -> None:
        baseline = path_utility(self.graph)
        for sid, raw_loss in raw_path_counterfactual_loss(self.graph).items():
            after = path_utility(self.graph.intervene(remove_nodes=[sid]))
            self.assertAlmostEqual(baseline - after, raw_loss, places=12)

    def test_signal_is_deterministic_and_bounded(self) -> None:
        first = path_counterfactual_sensitivity(self.graph)
        second = path_counterfactual_sensitivity(self.graph)
        self.assertEqual(first, second)
        self.assertTrue(all(0.0 <= value <= 1.0 for value in first.values()))

    def test_invalid_path_limits_fail(self) -> None:
        with self.assertRaises(ValueError):
            qualified_typed_paths(self.graph, min_edges=1)

    def test_deterministic_work_guard_fails_closed(self) -> None:
        with self.assertRaises(PathEnumerationLimitError):
            qualified_typed_paths(self.graph, max_expansions=1)
        branched = CausalEventGraph(
            self.graph.nodes,
            list(self.graph.edges) + [CausalEdge("p", "m", "mitigated_by", 1.0)],
        )
        with self.assertRaises(PathEnumerationLimitError):
            qualified_typed_paths(branched, max_paths=1)


if __name__ == "__main__":
    unittest.main()
