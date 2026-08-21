import unittest

from c2ges_offline import CausalEventGraph, ConstrainedExtractiveSummarizer, build_and_summarize


SENTENCES = [
    {"sid": "s0", "text": "A frozen protection setting caused the relay to misoperate."},
    {"sid": "s1", "text": "The relay fault initiated the transmission outage."},
    {"sid": "s2", "text": "The line trip propagated a voltage decline through the area."},
    {"sid": "s3", "text": "Approximately 500 MW of load was lost and customers were affected."},
    {"sid": "s4", "text": "Operators recommend corrective relay settings to prevent recurrence."},
    {"sid": "s5", "text": "The report also describes the regional weather."},
]

SILVER = {
    "root_cause": [{"sid": "s0"}],
    "trigger_event": [{"sid": "s1"}],
    "propagation_or_response": [{"sid": "s2"}],
    "impact": [{"sid": "s3"}],
    "mitigation": [{"sid": "s4"}],
}


class C2GESOfflineTests(unittest.TestCase):
    def test_graph_construction_is_deterministic_and_typed(self) -> None:
        first = CausalEventGraph.from_sentences(SENTENCES, SILVER)
        second = CausalEventGraph.from_sentences(SENTENCES, SILVER)
        self.assertEqual(first.nodes, second.nodes)
        self.assertEqual(first.edges, second.edges)
        self.assertTrue(any(
            edge.source == "s0" and edge.target == "s1" and edge.relation == "causes"
            for edge in first.edges
        ))
        self.assertTrue(any(
            edge.source == "s2" and edge.target == "s3" and edge.relation == "results_in"
            for edge in first.edges
        ))
        self.assertIsNone(first.node("s5").dominant_role)

    def test_node_intervention_is_immutable_and_reduces_causal_flow(self) -> None:
        graph = CausalEventGraph.from_sentences(SENTENCES, SILVER)
        original_nodes = tuple(node.sid for node in graph.nodes)
        intervened = graph.intervene(remove_nodes=["s2"])
        self.assertEqual(tuple(node.sid for node in graph.nodes), original_nodes)
        self.assertNotIn("s2", {node.sid for node in intervened.nodes})
        self.assertLess(intervened.causal_flow(), graph.causal_flow())
        self.assertGreater(graph.counterfactual_sensitivity()["s2"], 0.0)

    def test_edge_intervention_removes_only_registered_edge(self) -> None:
        graph = CausalEventGraph.from_sentences(SENTENCES, SILVER)
        edge = graph.edges[0]
        intervened = graph.intervene(remove_edges=[edge.key])
        self.assertIn(edge, graph.edges)
        self.assertNotIn(edge, intervened.edges)
        self.assertEqual(len(intervened.edges), len(graph.edges) - 1)

    def test_constrained_summary_covers_causal_functions_and_restores_order(self) -> None:
        graph, summary = build_and_summarize(SENTENCES, silver_role_evidence=SILVER, budget=3)
        self.assertEqual(len(summary.sentences), 3)
        self.assertEqual(summary.covered_role_groups, (
            "cause_or_trigger",
            "propagation_or_impact",
            "mitigation",
        ))
        self.assertEqual(
            [sentence.position for sentence in summary.sentences],
            sorted(sentence.position for sentence in summary.sentences),
        )
        self.assertEqual(set(summary.selection_order), {sentence.sid for sentence in summary.sentences})
        self.assertTrue(graph.nodes)

    def test_input_and_weight_contracts_fail_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "unique"):
            CausalEventGraph.from_sentences([
                {"sid": "same", "text": "First sentence."},
                {"sid": "same", "text": "Second sentence."},
            ])
        with self.assertRaisesRegex(ValueError, "sum to one"):
            ConstrainedExtractiveSummarizer(relevance_weight=0.5)
        with self.assertRaisesRegex(KeyError, "unknown intervention"):
            CausalEventGraph.from_sentences(SENTENCES, SILVER).intervene(remove_nodes=["missing"])

    def test_empty_graph_and_budget_contract(self) -> None:
        graph = CausalEventGraph.from_sentences([])
        summary = ConstrainedExtractiveSummarizer().summarize(graph, budget=2)
        self.assertEqual(summary.text, "")
        with self.assertRaisesRegex(ValueError, "positive"):
            ConstrainedExtractiveSummarizer().summarize(graph, budget=0)


if __name__ == "__main__":
    unittest.main()
