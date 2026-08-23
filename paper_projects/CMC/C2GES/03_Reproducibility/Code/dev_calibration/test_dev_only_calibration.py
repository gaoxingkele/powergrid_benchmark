from __future__ import annotations

import json
import math
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import run_dev_only_calibration as calibration


class CalibrationTests(unittest.TestCase):
    def test_grid_is_finite_and_deduplicated(self):
        grid = calibration.candidate_grid()
        self.assertEqual(len(grid), 147)
        semantic = [{k: v for k, v in item.items() if k != "candidate_id"} for item in grid]
        self.assertEqual(len({json.dumps(item, sort_keys=True) for item in semantic}), len(grid))

    def test_required_cf_weights_are_present(self):
        self.assertEqual({float(item["cf_weight"]) for item in calibration.candidate_grid()}, set(calibration.CF_WEIGHTS))

    def test_full_weights_always_sum_to_one(self):
        for item in calibration.candidate_grid():
            self.assertTrue(math.isclose(sum(item["weights"].values()), 1.0, abs_tol=1e-12))
            self.assertTrue(all(value >= 0 for value in item["weights"].values()))

    def test_formal_vector_is_recovered_at_point_fifteen(self):
        expected = {"relevance": .4, "role": .2, "graph": .15, "counterfactual": .15, "position": .1}
        for family in calibration.ALLOCATION_FAMILIES:
            self.assertEqual(calibration.weights(.15, family), expected)

    def test_normalized_no_cf_sums_to_one_and_zeroes_cf(self):
        for item in calibration.candidate_grid():
            result = calibration.normalized_no_cf_weights(item["weights"], item["allocation"])
            self.assertEqual(result["counterfactual"], 0)
            self.assertTrue(math.isclose(sum(result.values()), 1.0, abs_tol=1e-12))

    def test_input_guard_rejects_every_unlisted_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            forbidden = Path(tmp) / "anything.jsonl"
            forbidden.write_text("{}\n", encoding="utf-8")
            with self.assertRaises(PermissionError):
                calibration._read_allowed(forbidden)

    def test_gate_definitions(self):
        diagnostic = {"coverage_pass": True, "stability_pass": False}
        self.assertTrue(calibration.gate_enabled("none", diagnostic))
        self.assertTrue(calibration.gate_enabled("coverage", diagnostic))
        self.assertFalse(calibration.gate_enabled("coverage_stability", diagnostic))

    def test_spearman_identity_and_reversal(self):
        self.assertAlmostEqual(calibration.spearman([1, 2, 3], [1, 2, 3]), 1.0)
        self.assertAlmostEqual(calibration.spearman([1, 2, 3], [3, 2, 1]), -1.0)

    def test_output_directory_refuses_overwrite_before_data_read(self):
        with patch.object(calibration, "OUTPUT_DIR", Path(__file__).resolve().parent):
            with self.assertRaises(FileExistsError):
                calibration.run()

    def test_dev_hash_is_pinned(self):
        if not calibration.DEV_PATH.exists():
            self.skipTest("restricted development JSONL is not distributed")
        self.assertEqual(calibration.sha256(calibration.DEV_PATH), calibration.EXPECTED_DEV_SHA256)


if __name__ == "__main__":
    unittest.main()
