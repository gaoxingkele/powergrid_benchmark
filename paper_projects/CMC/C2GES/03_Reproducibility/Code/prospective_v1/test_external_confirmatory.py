from __future__ import annotations

import json
import importlib.metadata
import platform
import tempfile
import unittest
from pathlib import Path

import numpy as np

from external_confirmatory import (
    METHODS,
    build_graph_v03,
    claim_attempt,
    find_seen_overlaps,
    preflight,
    score_channels,
    semantic_mmr_select,
    system_select,
    validate_config,
)


class Node:
    def __init__(self, sid: str, position: int) -> None:
        self.sid = sid
        self.position = position
        self.text = "short unit"


class ExternalConfirmatoryTests(unittest.TestCase):
    def valid_config(self) -> dict:
        return {
            "status": "FROZEN",
            "mode": "EXTERNAL_CONFIRMATORY_ONE_ATTEMPT",
            "execution_allowed": True,
            "external_test_accessed": False,
            "methods": list(METHODS),
            "recommended_method": "C2GES-NO-PATH",
            "word_budgets": [110, 260],
            "long_unit_policy": "chunk_mean_254",
            "model_revision": "1" * 40,
            "bootstrap_samples": 10000,
            "bootstrap_seed": 7,
            "base_positive_weights": {"relevance": 0.4, "role": 0.2, "graph": 0.15, "path": 0.15, "position": 0.1},
            "semantic_mmr_lambda": 0.9,
            "textrank_alpha": 0.65,
            "pacsum": {"lambda_preceding": -1.0, "lambda_following": 1.0, "beta": 0.3},
            "expected_reports": 8,
            "expected_series": 8,
            "runtime": {
                "python": platform.python_version(),
                "packages": {"numpy": importlib.metadata.version("numpy")},
            },
        }

    def test_config_identity_is_strict(self) -> None:
        config = self.valid_config()
        validate_config(config)
        config["word_budgets"] = [100, 250]
        with self.assertRaisesRegex(ValueError, "word budgets"):
            validate_config(config)

    def test_attempt_claim_is_atomic_and_nonrepeatable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            authorization = root / "authorization.json"
            authorization.write_text("{}\n", encoding="utf-8")
            registry = root / "durable" / "attempt.json"
            payload = {"run_id": "formal-1"}
            claim_attempt(registry, authorization, payload)
            with self.assertRaisesRegex(RuntimeError, "already claimed"):
                claim_attempt(registry, authorization, payload)
            recorded = json.loads(registry.read_text(encoding="utf-8"))
            self.assertEqual(recorded["status"], "CLAIMED")
            self.assertFalse(recorded["external_dataset_opened"])

    def test_draft_authorization_fails_before_attempt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            authorization = root / "authorization.json"
            authorization.write_text(json.dumps({"schema": "c2ges-external-confirmatory-authorization-v1", "status": "DRAFT_NOT_AUTHORIZED"}), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "authorization schema/status"):
                preflight(authorization, root / "output")
            self.assertFalse((root / "attempt.json").exists())

    def test_seen_inventory_overlap_is_detected_by_url_or_hash(self) -> None:
        inventory = [
            {"doc_id": "by-url", "source_url": "https://example.org/seen.pdf", "source_pdf_sha256": "1" * 64},
            {"doc_id": "by-hash", "source_url": "https://example.org/new.pdf", "source_pdf_sha256": "A" * 64},
            {"doc_id": "clean", "source_url": "https://example.org/clean.pdf", "source_pdf_sha256": "B" * 64},
        ]
        exclusions = [
            {"source_url": "https://example.org/seen.pdf", "source_pdf_sha256": ""},
            {"source_url": "", "source_pdf_sha256": "a" * 64},
        ]
        self.assertEqual(find_seen_overlaps(inventory, exclusions), ["by-url", "by-hash"])

    def test_semantic_mmr_tie_prefers_earlier_then_smaller_id(self) -> None:
        nodes = [Node("b", 0), Node("a", 0), Node("c", 1)]
        embeddings = np.asarray([[1.0, 0.0], [1.0, 0.0], [1.0, 0.0]])
        _, order = semantic_mmr_select(nodes, embeddings, 2, 0.5)
        self.assertEqual(order[0], "a")

    def test_all_eight_systems_obey_the_same_word_budget(self) -> None:
        sentences = [
            {"sid": "s1", "text": "A relay fault triggered the outage."},
            {"sid": "s2", "text": "Voltage response propagated across the system."},
            {"sid": "s3", "text": "Customers lost 100 MW for two hours."},
            {"sid": "s4", "text": "Operators recommend corrective protection settings."},
            {"sid": "s5", "text": "The root cause was a failed splice."},
        ]
        config = {**self.valid_config(), "max_distance": 12, "path_min_edges": 2, "path_max_edges": 4, "path_max_paths": 250000, "path_max_expansions": 2000000, "redundancy_penalty": 0.5}
        graph = build_graph_v03(sentences, max_distance=12)
        raw = score_channels(graph, path_min_edges=2, path_max_edges=4, path_max_paths=250000, path_max_expansions=2000000)
        channels = {"relevance": raw["relevance"], "role": raw["role"], "graph": raw["graph"], "path": raw["counterfactual"], "position": raw["position"]}
        embeddings = np.eye(len(sentences), dtype=float)
        for method in METHODS:
            selected, _ = system_select(method, graph, channels, embeddings, config, 12)
            used = sum(len(node.text.replace(".", "").split()) for node in selected)
            self.assertGreater(len(selected), 0, method)
            self.assertLessEqual(used, 12, method)


if __name__ == "__main__":
    unittest.main()
