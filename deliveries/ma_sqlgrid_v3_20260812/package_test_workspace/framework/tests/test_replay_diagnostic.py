import tempfile
from pathlib import Path
import unittest

from replay_diagnostic import LABEL, build_diagnostic, verify_inputs


def prediction(backbone, question, condition, sql):
    return {
        "question_id": question,
        "condition": condition,
        "status": "success",
        "predicted_sql": sql,
        "response_hash": f"{backbone}-{condition}",
    }


def snapshot(backbone, question, condition, ok=True, shape=True):
    return {
        "backbone": backbone,
        "question_id": question,
        "condition": condition,
        "state": "T0_snapshot",
        "prediction_ok": ok,
        "prediction_vs_metadata_header_match": shape,
        # This gold-relative field is intentionally present to prove it is ignored.
        "tolerant_denotation_agreement": True,
    }


class ReplayDiagnosticTests(unittest.TestCase):
    def test_two_frozen_candidates_are_adjudicated_without_cf_leakage(self):
        qwen = [
            prediction("qwen", "Q1", "F00_Full_NoShape", "SELECT asset_id FROM assets;"),
            prediction("qwen", "Q1", "F01_Full_WithShape", "SELECT asset_id, status FROM assets;"),
        ]
        granite = []
        atomic = [
            snapshot("qwen", "Q1", "F00_Full_NoShape", shape=False),
            snapshot("qwen", "Q1", "F01_Full_WithShape", shape=True),
        ]
        rows, summary = build_diagnostic(qwen, granite, atomic)
        self.assertEqual(rows[0]["status"], "retrospective_offline_adjudicated")
        self.assertEqual(rows[0]["selected_candidate_id"], "C001")
        self.assertEqual(rows[0]["counterfactual_eligible_candidate_count"], 0)
        self.assertEqual(summary["questions_with_reference_free_counterfactual_evidence"], 0)
        self.assertFalse(summary["accuracy_claim_authorized"])
        self.assertEqual(rows[0]["diagnostic_label"], LABEL)

    def test_one_unique_candidate_fails_closed(self):
        qwen = [prediction("qwen", "Q1", "F00_Full_NoShape", "SELECT 1;")]
        granite = [prediction("granite", "Q1", "F00_Full_NoShape", " SELECT 1 ")]
        atomic = [
            snapshot("qwen", "Q1", "F00_Full_NoShape"),
            snapshot("granite", "Q1", "F00_Full_NoShape"),
        ]
        rows, _ = build_diagnostic(qwen, granite, atomic)
        self.assertEqual(rows[0]["status"], "insufficient_unique_candidate_coverage")
        self.assertIsNone(rows[0]["selected_candidate_id"])

    def test_only_one_executable_candidate_fails_closed(self):
        qwen = [
            prediction("qwen", "Q1", "F00_Full_NoShape", "SELECT 1;"),
            prediction("qwen", "Q1", "F01_Full_WithShape", "SELECT 2;"),
        ]
        atomic = [
            snapshot("qwen", "Q1", "F00_Full_NoShape", ok=True),
            snapshot("qwen", "Q1", "F01_Full_WithShape", ok=False),
        ]
        rows, _ = build_diagnostic(qwen, [], atomic)
        self.assertEqual(rows[0]["status"], "insufficient_eligible_candidate_coverage")
        self.assertIsNone(rows[0]["selected_candidate_id"])

    def test_hash_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = {}
            for name in ("qwen_predictions", "granite_predictions", "atomic_scores"):
                path = Path(tmp) / name
                path.write_text("tampered", encoding="utf-8")
                paths[name] = path
            with self.assertRaises(ValueError):
                verify_inputs(paths)


if __name__ == "__main__":
    unittest.main()

