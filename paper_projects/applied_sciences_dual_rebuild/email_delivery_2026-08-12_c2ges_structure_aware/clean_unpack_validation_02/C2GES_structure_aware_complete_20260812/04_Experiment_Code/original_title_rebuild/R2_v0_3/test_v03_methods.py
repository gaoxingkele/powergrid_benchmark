from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from v03_methods import ROLE_GROUPS, RedundancyCache, build_graph_v03, constrained_select, jaccard, score_channels


class V03MethodTests(unittest.TestCase):
    def setUp(self) -> None:
        sentences = [
            {"sid": "s1", "text": "A root cause failure caused the relay event and outage."},
            {"sid": "s2", "text": "The relay tripped and voltage propagated across the system."},
            {"sid": "s3", "text": "The impact affected 100 MW of load and customers."},
            {"sid": "s4", "text": "The recommendation requires corrective mitigation action."},
        ]
        self.graph = build_graph_v03(sentences, max_distance=12)
        self.channels = score_channels(self.graph, path_max_edges=4)
        self.weights = {"relevance": 0.3, "role": 0.2, "graph": 0.2, "counterfactual": 0.25, "position": 0.05}

    def test_strict_no_cf_changes_only_cf_coefficient(self) -> None:
        _, audit = constrained_select(self.graph, self.channels, self.weights, budget=3, redundancy_penalty=0.35, remove_cf_only=True)
        expected = dict(self.weights)
        expected["counterfactual"] = 0.0
        self.assertEqual(audit["effective_weights"], expected)

    def test_full_weights_must_sum_one(self) -> None:
        bad = dict(self.weights)
        bad["position"] = 0.0
        with self.assertRaises(ValueError):
            constrained_select(self.graph, self.channels, bad, budget=3, redundancy_penalty=0.35)

    def _uncached_reference(self, *, remove_cf_only: bool):
        effective = dict(self.weights)
        if remove_cf_only:
            effective["counterfactual"] = 0.0
        names = ("relevance", "role", "graph", "counterfactual", "position")
        base = {
            node.sid: sum(effective[name] * self.channels[name][node.sid] for name in names)
            for node in self.graph.nodes
        }
        selected = []
        by_sid = {node.sid: node for node in self.graph.nodes}
        for _, roles in ROLE_GROUPS.items():
            eligible = [node for node in self.graph.nodes if node.sid not in selected and node.dominant_role in roles]
            if eligible:
                winner = max(eligible, key=lambda node: (base[node.sid], -node.position, node.sid))
                selected.append(winner.sid)
        while len(selected) < 3:
            eligible = [node for node in self.graph.nodes if node.sid not in selected]
            winner = max(
                eligible,
                key=lambda node: (
                    base[node.sid] - 0.35 * max((jaccard(node.text, by_sid[sid].text) for sid in selected), default=0.0),
                    -node.position,
                    node.sid,
                ),
            )
            selected.append(winner.sid)
        return selected, base

    def test_cached_and_uncached_outputs_are_byte_equivalent(self) -> None:
        cache = RedundancyCache(self.graph.nodes)
        for remove_cf in (False, True):
            selected, audit = constrained_select(
                self.graph,
                self.channels,
                self.weights,
                budget=3,
                redundancy_penalty=0.35,
                remove_cf_only=remove_cf,
                redundancy_cache=cache,
            )
            reference_order, reference_scores = self._uncached_reference(remove_cf_only=remove_cf)
            self.assertEqual(audit["selection_order"], reference_order)
            self.assertEqual(audit["base_scores"], reference_scores)
            self.assertEqual([node.sid for node in selected], sorted(reference_order, key=lambda sid: self.graph.node(sid).position))

    def test_positive_role_tie_abstains_and_creates_no_edges(self) -> None:
        graph = build_graph_v03(
            [
                {"sid": "tie", "text": "A fault outage occurred and affected customers."},
                {"sid": "mit", "text": "The recommendation requires corrective mitigation action."},
            ]
        )
        tied = graph.node("tie")
        scores = dict(tied.role_scores)
        self.assertGreater(max(scores.values()), 0.0)
        self.assertGreaterEqual(sum(abs(value - max(scores.values())) <= 1e-12 for value in scores.values()), 2)
        self.assertIsNone(tied.dominant_role)
        self.assertFalse(any(edge.source == "tie" or edge.target == "tie" for edge in graph.edges))


if __name__ == "__main__":
    unittest.main()
