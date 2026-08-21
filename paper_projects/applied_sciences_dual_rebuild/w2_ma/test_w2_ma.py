"""Offline acceptance tests for the W2 MA-SQLGrid evidence bundle."""

from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path
from unittest import mock


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_w2_ma as w2  # noqa: E402


class W2MAAcceptanceTests(unittest.TestCase):
    def test_endpoint_audit_never_serializes_secret_values(self) -> None:
        marker = "DO_NOT_SERIALIZE_THIS_SECRET_91a2"
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": marker}):
            audit = w2.endpoint_audit()
        serialized = json.dumps(audit)
        self.assertNotIn(marker, serialized)
        item = next(row for row in audit["environment"] if row["name"] == "OPENAI_API_KEY")
        self.assertEqual(set(item), {"name", "present", "non_empty"})
        self.assertTrue(item["present"])
        self.assertTrue(item["non_empty"])
        self.assertFalse(audit["network_probe_performed"])
        self.assertFalse(audit["paid_call_performed"])

    def test_new_baseline_generation_does_not_require_test_gold(self) -> None:
        records = [dict(record) for record in w2.formal.load_questions(w2.formal.QUESTIONS_PATH)]
        for record in records:
            if record["split"] == "test":
                record.pop("gold_sql")
        empty_evaluation = {
            "strict_execution_correct": 0,
            "projection_contract_correct": 0,
            "sql_executable": 1,
            "safe_sql": 1,
            "error_type": "test_stub",
            "predicted_column_count": 1,
            "expected_column_count": 1,
        }
        with mock.patch.object(w2.formal, "load_questions", return_value=records), mock.patch.object(
            w2, "evaluate_sql", return_value=empty_evaluation
        ):
            first, _ = w2.new_deterministic_baselines()
            second, _ = w2.new_deterministic_baselines()
        self.assertEqual(len(first), 360)
        self.assertEqual(
            [(row["condition"], row["question_id"], row["predicted_sql"]) for row in first],
            [(row["condition"], row["question_id"], row["predicted_sql"]) for row in second],
        )

    def test_generated_bundle_passes_contracts_and_separates_evidence(self) -> None:
        completion = json.loads((HERE / "completion.json").read_text(encoding="utf-8"))
        self.assertEqual(completion["paid_calls"], 0)
        self.assertEqual(completion["network_probes"], 0)
        self.assertEqual(completion["factorial_cells"], 720)
        self.assertTrue(completion["new_baseline_audit_passed"])
        self.assertTrue(completion["factorial_audit_passed"])
        self.assertTrue(completion["legacy_and_new_separated"])

        new_rows = w2.stat_audit.load_records(HERE / "new_deterministic_predictions_scores.jsonl")[0]
        legacy_rows = w2.stat_audit.load_records(HERE / "legacy_rescored_rows.jsonl")[0]
        self.assertEqual(len(new_rows), 360)
        self.assertEqual(len(legacy_rows), 1980)
        self.assertEqual({row["evidence_origin"] for row in new_rows}, {"NEW_zero_cost_deterministic_baseline"})
        self.assertEqual(
            {row["evidence_origin"] for row in legacy_rows},
            {"LEGACY_model_prediction_rescored_no_new_inference"},
        )

    def test_inventory_has_required_provenance_and_hashes(self) -> None:
        inventory = json.loads((HERE / "dataset_inventory.json").read_text(encoding="utf-8"))
        by_id = {row["dataset_id"]: row for row in inventory["datasets"]}
        self.assertTrue({"griddb-maintenance-v2-v0.1", "griddb-maintenance-v2-x10", "rts-gmlc", "simbench"}.issubset(by_id))
        for dataset in by_id.values():
            self.assertTrue(dataset["present"])
            self.assertRegex(dataset["file_manifest_sha256"], r"^[0-9a-f]{64}$")
            self.assertGreater(dataset["file_count"], 0)
            self.assertTrue(all(item["present"] for item in dataset["provenance_evidence"]))


if __name__ == "__main__":
    unittest.main()
