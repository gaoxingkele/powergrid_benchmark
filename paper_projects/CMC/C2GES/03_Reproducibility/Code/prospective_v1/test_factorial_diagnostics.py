"""Integrity tests for the generated exploratory factorial diagnostics."""

from __future__ import annotations

import csv
import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RUN_DIR = ROOT / "03_Reproducibility" / "Data" / "exploratory_external_v0" / "e3_factorial_exploratory_v3"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest().upper()


class FactorialDiagnosticsTest(unittest.TestCase):
    def test_manifest_hashes_and_counts(self) -> None:
        manifest = json.loads((RUN_DIR / "FACTORIAL_DIAGNOSTICS_MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["status"], "COMPLETE")
        self.assertFalse(manifest["confirmatory_claims_allowed"])
        expected_counts = {
            "selection_jaccard_rows": 154,
            "series_effect_rows": 140,
            "loso_rows": 140,
            "runtime_rows": 26,
            "human_metric_rows": 1,
        }
        self.assertEqual(manifest["counts"], expected_counts)
        for filename, expected_hash in manifest["source_hashes"].items():
            self.assertEqual(sha256(RUN_DIR / filename), expected_hash)
        for filename, expected_hash in manifest["generated_hashes"].items():
            self.assertEqual(sha256(RUN_DIR / filename), expected_hash)

    def test_jaccard_and_loso_invariants(self) -> None:
        with (RUN_DIR / "factorial_selection_jaccard.csv").open(newline="", encoding="utf-8") as stream:
            jaccard = list(csv.DictReader(stream))
        self.assertEqual(len(jaccard), 154)
        for row in jaccard:
            intersection = int(row["intersection"])
            union = int(row["union"])
            observed = float(row["selection_jaccard"])
            expected = 1.0 if union == 0 else intersection / union
            self.assertAlmostEqual(observed, expected, places=14)
            self.assertGreaterEqual(observed, 0.0)
            self.assertLessEqual(observed, 1.0)

        with (RUN_DIR / "factorial_loso.csv").open(newline="", encoding="utf-8") as stream:
            loso = list(csv.DictReader(stream))
        self.assertEqual(len(loso), 140)
        path_rows = [row for row in loso if row["contrast"] == "AB-5_minus_AB-6"]
        self.assertEqual(len(path_rows), 14)
        self.assertTrue(all(row["full_direction"] == "negative" for row in path_rows))
        self.assertTrue(all(row["loso_direction"] == "negative" for row in path_rows))

    def test_human_validation_is_explicitly_not_run(self) -> None:
        with (RUN_DIR / "factorial_human_metrics.csv").open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["status"], "NOT_RUN")
        self.assertEqual(rows[0]["counts_as_human_validation"].upper(), "FALSE")
        self.assertEqual(int(rows[0]["human_annotators"]), 0)


if __name__ == "__main__":
    unittest.main()
