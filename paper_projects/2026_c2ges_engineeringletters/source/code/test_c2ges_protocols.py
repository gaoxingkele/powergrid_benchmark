"""Offline regression tests for the Applied Sciences C2GES protocols."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

import c2ges_learnable as c2
import audit_fever_title_aliases as title_audit
import aggregate_c2_w4_five_seed as five_seed
import w4_freeze_guard as freeze_guard
import prepare_fever_benchmark as prep
import predict_fever_labels as labeler


def row(claim_id: int = 7, document_id: str = "Shared_Page", label: str = "SUPPORTS") -> dict:
    return {
        "id": claim_id,
        "document_id": document_id,
        "label": label,
        "claim": "A shared page exists.",
        "lines": "0\tA shared page exists.\n1\tAn unrelated sentence.",
        "evidence_lines": "0",
    }


class FakeEncoder:
    def get_sentence_embedding_dimension(self):
        return 4

    def encode(self, texts, **_kwargs):
        vectors = []
        for text in texts:
            seed = sum(ord(ch) for ch in text)
            vectors.append([(seed % 7) / 7, (seed % 11) / 11, len(text) / 50, 1.0])
        return np.asarray(vectors, dtype=np.float32)


class PrepareTests(unittest.TestCase):
    def test_preserves_original_document_identifiers(self):
        converted = prep.convert_row(row(document_id="Camden,_New_Jersey"), "train", source_split="dev")
        self.assertEqual(converted["document_id"], "Camden,_New_Jersey")
        self.assertEqual(converted["underlying_document_id"], "Camden,_New_Jersey")
        self.assertEqual(converted["wikipedia_title"], "Camden,_New_Jersey")
        self.assertEqual(converted["source_split"], "dev")

    def test_document_assignment_is_stable(self):
        first = prep.assigned_split("Same_Page", 0.8, 0.1)
        self.assertEqual(first, prep.assigned_split("Same_Page", 0.8, 0.1))

    def test_leakage_audit_uses_underlying_document(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for split, underlying in (("train", "shared"), ("dev", "shared"), ("test", "other")):
                (root / split).mkdir()
                (root / split / "instance.json").write_text(
                    json.dumps({"doc_id": f"{split}-claim", "underlying_document_id": underlying}),
                    encoding="utf-8",
                )
            audit = prep.leakage_audit(root)
            self.assertFalse(audit["passed"])
            self.assertEqual(audit["pairwise_overlap"]["train_vs_dev"]["document_ids"], ["shared"])

    def test_grouped_writer_keeps_all_claims_for_page_in_one_split(self):
        dataset = {
            "train": [row(1, "Repeated_Page"), row(2, "Train_Only")],
            "dev": [row(3, "Repeated_Page", "REFUTES")],
            "test": [row(4, "Test_Only")],
        }
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            prep.write_document_grouped(
                dataset,
                root,
                {"train": None, "dev": None, "test": None},
                0.8,
                0.1,
            )
            audit = prep.leakage_audit(root)
            self.assertTrue(audit["passed"])
            locations = []
            for split in ("train", "dev", "test"):
                for path in (root / split).glob("*.json"):
                    doc = json.loads(path.read_text(encoding="utf-8"))
                    if doc["underlying_document_id"] == "Repeated_Page":
                        locations.append(split)
            self.assertEqual(len(locations), 2)
            self.assertEqual(len(set(locations)), 1)

    def test_title_normalization_and_near_duplicate_candidates(self):
        self.assertEqual(
            title_audit.normalized_title("Game_of_Thrones"),
            title_audit.normalized_title("Game%20of%20Thrones"),
        )
        candidates = title_audit.audit_pairs(
            {"train": [], "dev": ["A_Game_of_Thrones"], "test": ["Game_of_Thrones"]},
            similarity_threshold=0.92,
            ngram_threshold=0.72,
        )
        self.assertEqual(len(candidates), 1)
        self.assertIn("high_title_string_similarity", candidates[0]["reasons"])

    def test_grouped_writer_never_truncates_a_document_at_limit(self):
        dataset = {
            "train": [row(1, "Repeated_Page"), row(2, "Repeated_Page")],
            "dev": [],
            "test": [],
        }
        target = prep.assigned_split("Repeated_Page", 0.8, 0.1)
        limits = {"train": None, "dev": None, "test": None}
        limits[target] = 1
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            counts = prep.write_document_grouped(dataset, root, limits, 0.8, 0.1)
            self.assertEqual(counts[target], 0)
            self.assertEqual(list((root / target).glob("*.json")), [])


class ProtocolTests(unittest.TestCase):
    def test_output_directory_requires_explicit_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            artifact = root / "summary.json"
            artifact.write_text("old", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                c2.prepare_output_directory(root)
            removed = c2.prepare_output_directory(root, overwrite=True)
            self.assertEqual(removed, [artifact])
            self.assertFalse(artifact.exists())

    def test_protocol_roles_and_oracle_scope(self):
        q = {"qid": "q1", "role": "supports"}
        self.assertEqual(c2.protocol_role(q, "oracle-label", {}), "supports")
        self.assertFalse(c2.PROTOCOLS["oracle-label"]["is_end_to_end"])
        self.assertEqual(c2.protocol_role(q, "label-blind", {}), "unknown")
        self.assertEqual(c2.protocol_role(q, "predicted-label", {"q1": "refutes"}), "refutes")
        with self.assertRaises(ValueError):
            c2.protocol_role(q, "predicted-label", {})

    def test_legacy_title_recovers_underlying_id(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "x.json"
            path.write_text(json.dumps({"doc_id": "claim-specific", "title": "Original_Page"}), encoding="utf-8")
            docs = c2.load_docs(Path(temp))
            self.assertEqual(docs[0]["underlying_document_id"], "Original_Page")

    def test_offline_tiny_training_and_predictions(self):
        docs = []
        for index, label in enumerate(("SUPPORTS", "REFUTES", "SUPPORTS")):
            obj = prep.convert_row(row(index + 1, f"page-{index}", label), "train")
            docs.append(obj)
        examples = c2.build_examples(
            docs,
            FakeEncoder(),
            {role: idx for idx, role in enumerate(c2.ROLES)},
            protocol="label-blind",
        )
        head, mix, _best = c2.train_model(examples, examples, 4, 1, 1e-3, "cpu", 3, 1)
        metrics = c2.evaluate(examples, head, mix, "cpu", ["full", "bm25"], 1)
        rows = list(c2.prediction_rows(examples, head, mix, "cpu", ["full"], [1]))
        self.assertEqual(metrics["full"]["n"], 3)
        self.assertEqual(len(rows), 3)
        self.assertIn("candidate_scores", rows[0])
        self.assertTrue(all(item["selector_role"] == "unknown" for item in rows))

    def test_bootstrap_clusters_claims_by_wikipedia_document(self):
        examples = [
            {"doc_id": "claim-1", "underlying_document_id": "page-A", "sids": ["s0"], "gold": ["s0"]},
            {"doc_id": "claim-2", "underlying_document_id": "page-A", "sids": ["s0"], "gold": ["s0"]},
            {"doc_id": "claim-3", "underlying_document_id": "page-B", "sids": ["s0"], "gold": ["s0"]},
        ]
        with patch.object(c2, "predict_scores", return_value=np.asarray([1.0])):
            result = c2.bootstrap_delta(examples, None, None, "cpu", "a", "b", k=1, samples=10)
        self.assertEqual(result["cluster_unit"], "underlying_wikipedia_document")
        self.assertEqual(result["cluster_count"], 2)


class UpstreamLabelPredictorTests(unittest.TestCase):
    def _write_split(self, root: Path, split: str, count: int, offset: int) -> None:
        split_dir = root / split
        split_dir.mkdir(parents=True)
        for index in range(count):
            label = "SUPPORTS" if index % 2 == 0 else "REFUTES"
            obj = prep.convert_row(row(offset + index, f"{split}_page_{index}", label), split)
            (split_dir / f"{obj['doc_id']}.json").write_text(json.dumps(obj), encoding="utf-8")

    def test_oof_predictor_writes_reproducible_audit_artifacts(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            data = root / "data"
            out = root / "out"
            self._write_split(data, "train", 12, 0)
            self._write_split(data, "dev", 4, 100)
            self._write_split(data, "test", 4, 200)
            argv = [
                "predict_fever_labels.py",
                "--data", str(data),
                "--out", str(out),
                "--folds", "3",
                "--min-df", "1",
                "--max-features", "100",
                "--seed", "9",
            ]
            with patch.object(sys, "argv", argv):
                self.assertEqual(labeler.main(), 0)
            predictions = [json.loads(line) for line in (out / "predictions.jsonl").read_text(encoding="utf-8").splitlines()]
            train_rows = [item for item in predictions if item["split"] == "train"]
            self.assertTrue(all("train_oof_group_fold_" in item["prediction_source"] for item in train_rows))
            self.assertTrue(all(item["prediction_source"] == "full_train_only_model" for item in predictions if item["split"] != "train"))
            provenance = json.loads((out / "provenance.json").read_text(encoding="utf-8"))
            self.assertTrue(provenance["document_leakage_audit"]["passed"])
            self.assertIn("output_predicted_labels_sha256", provenance)


class FiveSeedAggregationTests(unittest.TestCase):
    def test_common_config_only_removes_allowed_seed_protocol_fields(self):
        config = {"seed": 1, "protocol": "x", "out": "a", "epochs": 4, "eval_k": [1, 3, 5, 10]}
        self.assertEqual(freeze_guard.common_config(config), {"epochs": 4, "eval_k": [1, 3, 5, 10]})

    def test_exact_sign_flip_is_deterministic_and_small_n_explicit(self):
        # With five positive differences, the smallest attainable two-sided
        # exact sign-flip p-value is 2/32 = 0.0625.
        self.assertEqual(five_seed.exact_sign_flip_p([1, 1, 1, 1, 1]), 0.0625)

    def test_hierarchical_bootstrap_reports_both_sampling_units(self):
        values = {
            1: {"doc-a": [0.1, 0.2], "doc-b": [0.0]},
            2: {"doc-c": [0.3], "doc-d": [0.1, 0.1]},
        }
        result = five_seed.hierarchical_bootstrap(values, samples=20, seed=4)
        self.assertEqual(result["outer_unit"], "training_seed")
        self.assertEqual(result["inner_unit"], "underlying_wikipedia_document")
        self.assertEqual(result["seed_count"], 2)


if __name__ == "__main__":
    unittest.main()
