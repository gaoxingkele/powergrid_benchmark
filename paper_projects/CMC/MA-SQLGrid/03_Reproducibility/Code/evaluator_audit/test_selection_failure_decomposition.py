import csv
import json
import unittest

from run_role_ablation_audit import REPRO_ROOT
from run_selection_failure_decomposition import classify


class FailurePartitionTests(unittest.TestCase):
    def test_five_exclusive_stages(self):
        cases = {
            (False, False, False, False): "no_correct_candidate",
            (True, False, False, False): "all_correct_candidates_gated_out",
            (True, True, False, False): "correct_candidates_below_top_score",
            (True, True, True, False): "correct_top_candidate_lost_by_tie_order",
            (True, True, True, True): "selected_correct",
        }
        self.assertEqual({classify(*k) for k in cases}, set(cases.values()))
        for k, v in cases.items():
            self.assertEqual(classify(*k), v)

    def test_invalid_nesting_rejected(self):
        with self.assertRaises(ValueError):
            classify(False, True, False, False)
        with self.assertRaises(ValueError):
            classify(True, False, True, False)
        with self.assertRaises(ValueError):
            classify(True, True, False, True)

    def test_retained_tie_audit_agrees_per_question(self):
        artifact = REPRO_ROOT / "Data/selection_failure_decomposition/information_r1/selection_failure_decomposition.json"
        rows = json.loads(artifact.read_text(encoding="utf-8"))["items"]
        prior = REPRO_ROOT / "Data/evaluator_audit/order_sensitivity_unified_v1/per_question_ties.csv"
        with prior.open(encoding="utf-8", newline="") as f:
            old = {r["question_id"]: r for r in csv.DictReader(f)}
        self.assertEqual(len(rows), 360)
        self.assertEqual(len({(r['question_id'], r['selector']) for r in rows}), 360)
        for r in rows:
            p = old[r["question_id"]]
            stem = r["selector"] + "_"
            self.assertEqual(r["selected_correct"], bool(int(p[stem + "original_correct"])))
            self.assertEqual(r["top_slots"], int(p[stem + "top_tie_size"]))
            self.assertEqual(r["correct_top_slots"] > 0, bool(int(p[stem + "any_top_correct"])))
            self.assertEqual(r["mixed_correctness_top"],
                bool(int(p[stem + "any_top_correct"])) and not bool(int(p[stem + "all_top_correct"])))


if __name__ == "__main__":
    unittest.main()
