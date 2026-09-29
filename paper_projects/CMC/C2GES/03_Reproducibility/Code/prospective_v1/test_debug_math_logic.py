"""Debug-only checks of kappa arithmetic and the typed-path accounting identity.

Fixture labels are software agents. They are not human or expert gold.
"""
from __future__ import annotations

import json
import math
import sys
import tempfile
import unittest
from pathlib import Path

from human_validation import FORM_FIELDS, cohen_kappa, freeze_pre, write_csv

CORE = Path(__file__).resolve().parents[1] / "core"
if str(CORE) not in sys.path:
    sys.path.insert(0, str(CORE))
R2 = CORE / "R2_v0_3"
if str(R2) not in sys.path:
    sys.path.insert(0, str(R2))

from c2ges_offline import CausalEdge, CausalEventGraph, SentenceNode
from counterfactual_paths import path_utility, qualified_typed_paths, raw_path_counterfactual_loss


def toy_node(sid: str, position: int, role: str) -> SentenceNode:
    roles = ("root_cause", "trigger_event", "propagation_or_response", "impact", "mitigation")
    return SentenceNode(
        sid=sid,
        text=f"Debug {sid} unit for path-identity arithmetic only.",
        position=position,
        role_scores=tuple((name, 1.0 if name == role else 0.0) for name in roles),
        dominant_role=role,
    )


class KappaArithmeticTests(unittest.TestCase):
    def test_perfect_and_chance_agreement(self) -> None:
        self.assertAlmostEqual(cohen_kappa(["y", "y", "n", "n"], ["y", "y", "n", "n"]), 1.0)
        self.assertAlmostEqual(cohen_kappa(["y", "y", "n", "n"], ["y", "n", "y", "n"]), 0.0)

    def test_hand_computed_two_by_two(self) -> None:
        a = ["yes"] * 10 + ["no"] * 10
        b = ["yes"] * 8 + ["no"] * 2 + ["yes"] * 2 + ["no"] * 8
        observed = 16 / 20
        expected = 0.5
        self.assertAlmostEqual(cohen_kappa(a, b), (observed - expected) / (1.0 - expected))


class PathIdentityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = CausalEventGraph(
            [
                toy_node("r", 0, "root_cause"),
                toy_node("t", 1, "trigger_event"),
                toy_node("q", 2, "propagation_or_response"),
                toy_node("i", 3, "impact"),
                toy_node("m", 4, "mitigation"),
            ],
            [
                CausalEdge("r", "t", "causes", 0.8),
                CausalEdge("t", "q", "propagates_to", 0.6),
                CausalEdge("q", "i", "results_in", 0.9),
                CausalEdge("i", "m", "motivates_mitigation", 0.7),
            ],
        )

    def test_manuscript_toy_path_strengths(self) -> None:
        by_nodes = {path.nodes: path.strength for path in qualified_typed_paths(self.graph)}
        self.assertAlmostEqual(by_nodes[("r", "t", "q", "i")], 0.566964, places=5)
        self.assertAlmostEqual(by_nodes[("r", "t", "q", "i", "m")], 0.741559, places=5)
        self.assertAlmostEqual(by_nodes[("t", "q", "i")], 0.367423, places=5)
        self.assertAlmostEqual(by_nodes[("t", "q", "i", "m")], 0.542282, places=5)
        self.assertAlmostEqual(path_utility(self.graph), 2.218228, places=5)

    def test_deletion_loss_equals_sum_of_incident_path_strengths(self) -> None:
        raw = raw_path_counterfactual_loss(self.graph)
        self.assertAlmostEqual(raw["q"], path_utility(self.graph), places=5)
        self.assertAlmostEqual(raw["r"], 1.308523, places=5)
        baseline = path_utility(self.graph)
        for sid, loss in raw.items():
            after = path_utility(self.graph.intervene(remove_nodes=[sid]))
            self.assertAlmostEqual(baseline - after, loss, places=12)


class DebugFixturePipelineTests(unittest.TestCase):
    def test_freeze_pre_kappa_matches_shipped_function(self) -> None:
        schema = {
            "schema": "debug-fixture-not-human",
            "tasks": {
                "role": {
                    "fields": ["role_label"],
                    "labels": {
                        "role_label": [
                            "root_cause",
                            "trigger_event",
                            "impact",
                            "cannot_judge",
                        ]
                    },
                }
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            schema_path = root / "schema.json"
            schema_path.write_text(json.dumps(schema), encoding="utf-8")
            manifest_rows = [
                {
                    "sample_id": f"d{i}",
                    "task": "role",
                    "report_series_id": "debug",
                    "system_condition": "DEBUG_FIXTURE",
                    "automated_role_label": "root_cause",
                }
                for i in range(4)
            ]
            write_csv(
                root / "manifest.csv",
                ["sample_id", "task", "report_series_id", "system_condition", "automated_role_label"],
                manifest_rows,
            )
            labels_a = ["root_cause", "root_cause", "impact", "impact"]
            labels_b = ["root_cause", "trigger_event", "impact", "impact"]
            for name, labels in (("agent_a", labels_a), ("agent_b", labels_b)):
                rows = []
                for sample, label in zip(manifest_rows, labels):
                    row = {field: "" for field in FORM_FIELDS}
                    row.update(
                        sample_id=sample["sample_id"],
                        task="role",
                        annotator_id=name,
                        role_label=label,
                    )
                    rows.append(row)
                write_csv(root / f"{name}.csv", FORM_FIELDS, rows)
            freeze_pre(
                schema_path,
                root / "manifest.csv",
                root / "agent_a.csv",
                root / "agent_b.csv",
                root / "pre.json",
            )
            pre = json.loads((root / "pre.json").read_text(encoding="utf-8"))
            self.assertEqual(pre["status"], "PRE_ADJUDICATION_FROZEN")
            expected = cohen_kappa(labels_a, labels_b)
            self.assertAlmostEqual(pre["agreement"]["role.role_label"]["cohen_kappa"], expected)
            self.assertEqual(pre["annotator_ids"]["a"], "agent_a")
            self.assertNotEqual(pre["annotator_ids"]["a"], "human")


if __name__ == "__main__":
    unittest.main()
