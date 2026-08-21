from __future__ import annotations

import json
import platform
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from c2ges_offline import CausalEdge, CausalEventGraph, SentenceNode
from counterfactual_paths_v031 import PathEnumerationLimitError, qualified_typed_paths
import run_test_v0_3_1 as runner
import v031_methods


def node(sid: str, position: int, role: str) -> SentenceNode:
    roles = ("trigger_event", "root_cause", "propagation_or_response", "impact", "mitigation")
    return SentenceNode(
        sid=sid,
        text=f"Synthetic {sid} engineering sentence.",
        position=position,
        role_scores=tuple((name, 1.0 if name == role else 0.0) for name in roles),
        dominant_role=role,
    )


class V031RepairTests(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = CausalEventGraph(
            [
                node("r", 0, "root_cause"),
                node("t", 1, "trigger_event"),
                node("p", 2, "propagation_or_response"),
                node("i", 3, "impact"),
                node("m", 4, "mitigation"),
            ],
            [
                CausalEdge("r", "t", "causes", 1.0),
                CausalEdge("t", "p", "propagates_to", 1.0),
                CausalEdge("p", "i", "results_in", 1.0),
                CausalEdge("p", "m", "mitigated_by", 1.0),
            ],
        )

    def test_all_four_cf_parameters_are_threaded(self) -> None:
        with patch.object(v031_methods, "path_counterfactual_sensitivity", return_value={n.sid: 0.0 for n in self.graph.nodes}) as mocked:
            v031_methods.score_channels(
                self.graph,
                path_min_edges=3,
                path_max_edges=5,
                path_max_paths=17,
                path_max_expansions=29,
            )
        mocked.assert_called_once_with(
            self.graph,
            min_edges=3,
            max_edges=5,
            max_paths=17,
            max_expansions=29,
        )

    def test_each_cf_limit_is_behaviorally_operative_and_fail_closed(self) -> None:
        two_edge = qualified_typed_paths(
            self.graph, min_edges=2, max_edges=2, max_paths=10, max_expansions=100
        )
        three_edge = qualified_typed_paths(
            self.graph, min_edges=3, max_edges=3, max_paths=10, max_expansions=100
        )
        self.assertTrue(all(len(path.weights) == 2 for path in two_edge))
        self.assertTrue(all(len(path.weights) == 3 for path in three_edge))
        with self.assertRaises(PathEnumerationLimitError):
            qualified_typed_paths(
                self.graph, min_edges=2, max_edges=4, max_paths=1, max_expansions=100
            )
        with self.assertRaises(PathEnumerationLimitError):
            qualified_typed_paths(
                self.graph, min_edges=2, max_edges=4, max_paths=100, max_expansions=1
            )

    def test_semantic_mmr_uses_minilm_space_for_relevance_and_redundancy(self) -> None:
        nodes = [
            SimpleNamespace(sid="a", position=0),
            SimpleNamespace(sid="b", position=1),
            SimpleNamespace(sid="c", position=2),
        ]
        embeddings = np.asarray([[1.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
        selected, audit = runner.semantic_mmr_select(nodes, embeddings, 2, 0.5)
        self.assertEqual(audit["selection_order"], ["a", "c"])
        self.assertEqual([item.sid for item in selected], ["a", "c"])
        self.assertEqual(audit["relevance_weight"], 0.5)
        self.assertEqual(audit["redundancy_penalty"], 0.5)

    def test_config_preserves_seven_conditions_and_six_primary_tests(self) -> None:
        config = json.loads((Path(__file__).parent / "formal_config_v0_3_1.json").read_text(encoding="utf-8"))
        runner.validate_config(config)
        self.assertEqual(len(config["conditions"]), 7)
        self.assertEqual(len(config["primary_contrasts"]) * len(config["selection_budgets"]), 6)
        self.assertEqual(config["primary_contrasts"][1], "semantic_mmr")

    def test_verify_freeze_checks_test_files_as_repo_relative_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in ("bound.txt", "code.py", "test.py"):
                (root / name).write_text(name, encoding="utf-8")
            lock = root / "lock.json"
            lock.write_text(json.dumps({"python": platform.python_version(), "packages": {}}), encoding="utf-8")
            freeze = {
                "path_resolution": "repository_root",
                "bound_files": [{"path": "bound.txt", "sha256": runner.sha256(root / "bound.txt")}],
                "code_files": [{"path": "code.py", "sha256": runner.sha256(root / "code.py")}],
                "test_files": [{"path": "test.py", "sha256": runner.sha256(root / "test.py")}],
                "runtime": {"dependency_lock_path": "lock.json", "dependency_lock_sha256": runner.sha256(lock)},
                "semantic_model_snapshot": {"path": str(root), "sha256": "MODEL"},
            }
            freeze_path = root / "freeze.json"
            freeze_path.write_text(json.dumps(freeze), encoding="utf-8")
            with patch.object(runner, "REPO_ROOT", root), patch.object(
                runner, "hash_tree", return_value={"sha256": "MODEL", "file_count": 1}
            ):
                runner.verify_freeze(freeze_path)
                (root / "test.py").write_text("changed", encoding="utf-8")
                with self.assertRaises(RuntimeError):
                    runner.verify_freeze(freeze_path)

    def test_hash_bound_authorization_and_durable_single_attempt_registry(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            freeze_path = root / "freeze.json"
            freeze = {
                "authorization": {"artifact_path": "authorization.json"},
                "run_control": {
                    "canonical_output_root": "runs",
                    "registry_path": "registry",
                },
            }
            freeze_path.write_text(json.dumps(freeze), encoding="utf-8")
            audit_path = root / "audit.json"
            audit_path.write_text(json.dumps({"verdict": "PASS", "freeze_sha256": runner.sha256(freeze_path)}), encoding="utf-8")
            authorization = {
                "authorized": True,
                "freeze_sha256": runner.sha256(freeze_path),
                "run_id": "formal_0001",
                "output_path": "runs/formal_0001",
                "audit_decision_path": "audit.json",
                "audit_decision_sha256": runner.sha256(audit_path),
                "approver": "test-approver",
                "approved_at": "2026-08-08T12:00:00+08:00",
            }
            auth_path = root / "authorization.json"
            auth_path.write_text(json.dumps(authorization), encoding="utf-8")
            with patch.object(runner, "REPO_ROOT", root):
                checked = runner.verify_authorization(
                    freeze_path, freeze, auth_path, root / "runs" / "formal_0001"
                )
                claim_path, claim = runner.reserve_attempt(
                    freeze, checked, runner.sha256(freeze_path)
                )
                self.assertEqual(claim["status"], "CLAIMED")
                self.assertTrue(claim_path.exists())
                with self.assertRaises(RuntimeError):
                    runner.reserve_attempt(freeze, checked, runner.sha256(freeze_path))

    def test_authorization_fails_on_audit_hash_or_output_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            freeze_path = root / "freeze.json"
            freeze = {
                "authorization": {"artifact_path": "authorization.json"},
                "run_control": {"canonical_output_root": "runs", "registry_path": "registry"},
            }
            freeze_path.write_text(json.dumps(freeze), encoding="utf-8")
            audit_path = root / "audit.json"
            audit_path.write_text(json.dumps({"verdict": "PASS", "freeze_sha256": runner.sha256(freeze_path)}), encoding="utf-8")
            authorization = {
                "authorized": True,
                "freeze_sha256": runner.sha256(freeze_path),
                "run_id": "formal_0001",
                "output_path": "runs/formal_0001",
                "audit_decision_path": "audit.json",
                "audit_decision_sha256": "0" * 64,
                "approver": "test-approver",
                "approved_at": "2026-08-08T12:00:00+08:00",
            }
            auth_path = root / "authorization.json"
            auth_path.write_text(json.dumps(authorization), encoding="utf-8")
            with patch.object(runner, "REPO_ROOT", root):
                with self.assertRaises(RuntimeError):
                    runner.verify_authorization(
                        freeze_path, freeze, auth_path, root / "runs" / "different"
                    )


if __name__ == "__main__":
    unittest.main()
