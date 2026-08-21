"""Tests for the independent C2GES W3/W4 recomputation artifacts."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

import recompute


HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class IndependentRecomputeTests(unittest.TestCase):
    def test_summary_statistics_and_sign_flip(self) -> None:
        result = recompute.summarize([1.0, 2.0, 3.0, 4.0, 5.0])
        self.assertEqual(result["mean"], 3.0)
        self.assertAlmostEqual(result["sample_std"], 2.5 ** 0.5)
        self.assertEqual(recompute.exact_sign_flip_p([1.0] * 5), 0.0625)

    def test_diff_has_no_mismatch_and_no_failures(self) -> None:
        diff = json.loads((HERE / "diff.json").read_text(encoding="utf-8"))
        result = json.loads((HERE / "independent_recompute.json").read_text(encoding="utf-8"))
        self.assertTrue(diff["passed"])
        self.assertEqual(diff["mismatch_count"], 0)
        self.assertEqual(diff["matched_cells"], diff["cell_count"])
        self.assertLessEqual(diff["max_numeric_difference"], diff["tolerance"])
        self.assertEqual(result["failure_counts"]["hard_failure_total"], 0)
        self.assertEqual(result["failure_counts"]["successful_resource_runs"], 15)

    def test_manifest_hashes(self) -> None:
        manifest = json.loads((HERE / "artifact_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["script"]["sha256"], digest(HERE / manifest["script"]["path"]))
        for item in manifest["outputs"]:
            path = HERE / item["path"]
            self.assertEqual(item["sha256"], digest(path))
            self.assertEqual(item["bytes"], path.stat().st_size)

    def test_input_policy_and_coverage(self) -> None:
        result = json.loads((HERE / "independent_recompute.json").read_text(encoding="utf-8"))
        self.assertIn("excluded until post-calculation", result["calculation_input_policy"])
        self.assertEqual(len(result["input_manifest"]), 15)
        self.assertTrue(all(item["prediction_rows"] == recompute.EXPECTED_ROWS for item in result["input_manifest"]))
        self.assertTrue(all(set(item["files"]) == {"predictions.jsonl", "summary.json", "resource_usage.json"}
                            for item in result["input_manifest"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
