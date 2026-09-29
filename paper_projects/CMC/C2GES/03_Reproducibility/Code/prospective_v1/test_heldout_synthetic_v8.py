from __future__ import annotations

import random
import unittest

import csv
import json
import re
from pathlib import Path

from build_heldout_synthetic_v8 import HELD_OUT_THEMES, local_pair
from generate_deepseek_synthetic import validate_core, validate_dataset, expand_report, words

V8 = Path(__file__).resolve().parents[2] / "Data" / "synthetic_stress_v1" / "run_20260918_heldout_v8"


class HeldoutSyntheticV8Tests(unittest.TestCase):
    def test_four_unused_themes(self) -> None:
        self.assertEqual(len(HELD_OUT_THEMES), 4)
        used_v6 = {
            "protection-setting mismatch during feeder restoration",
            "telemetry delay during reserve activation",
            "islanding detection delay at a fictional microgrid",
        }
        themes = {theme for _, theme in HELD_OUT_THEMES}
        self.assertTrue(themes.isdisjoint(used_v6))

    def test_local_pair_validates_and_expands(self) -> None:
        rng = random.Random(20260918)
        cores = validate_core(local_pair(12, HELD_OUT_THEMES[0][1], rng), require_distractor_seeds=True)
        self.assertEqual(len(cores), 2)
        profile = {
            "page_count": 20,
            "candidate_count": 80,
            "reference_words": 140,
            "units_over_256_tokens": 1,
            "body": 55,
            "heading": 5,
            "list_item": 10,
            "table_unit": 7,
            "caption": 2,
            "footnote": 1,
        }
        rows = [
            expand_report(core, profile, f"d{i}", "synthetic_series_12", "explicit", HELD_OUT_THEMES[0][1], rng)
            for i, core in enumerate(cores, 1)
        ]
        self.assertEqual(validate_dataset(rows)["two_reports_per_series"], True)
        self.assertTrue(all(110 <= words(row["reference_summary"]) <= 180 for row in rows))
        self.assertTrue(all(row["synthetic"] is True and row["confirmatory_claims_allowed"] is False for row in rows))

    def test_v8_run_passes_gates_and_matches_manuscript_cells(self) -> None:
        evaluation = json.loads((V8 / "evaluation" / "distribution_evaluation.json").read_text(encoding="utf-8"))
        self.assertTrue(evaluation["deterministic_gate_pass"])
        self.assertFalse(evaluation["confirmatory_claims_allowed"])
        supplement = (
            Path(__file__).resolve().parents[3] / "01_Manuscript" / "Supplementary" / "supplementary_materials.tex"
        ).read_text(encoding="utf-8")
        data_root = Path(__file__).resolve().parents[2] / "Data" / "synthetic_stress_v1"
        for run_label, run_dir in (
            ("Parent", "run_20260927_gendata_parent_v3r1"),
            ("Held-out", "run_20260927_gendata_heldout_v2r3"),
        ):
            rows = list(
                csv.DictReader(
                    (data_root / run_dir / "e3_factorial_pilot" / "factorial_aggregate_metrics.csv").open(
                        encoding="utf-8-sig"
                    )
                )
            )
            lookup = {(int(row["word_budget"]), row["condition"]): float(row["rougeL_f1"]) for row in rows}
            for condition, prefix in (("AB-5", "Full"), ("AB-6", "No-path")):
                match = re.search(rf"{run_label} & {prefix}[^&]*& ([0-9.]+) & ([0-9.]+)", supplement)
                self.assertIsNotNone(match, (run_label, prefix))
                self.assertAlmostEqual(round(lookup[(110, condition)], 4), float(match.group(1)), places=4)
                self.assertAlmostEqual(round(lookup[(260, condition)], 4), float(match.group(2)), places=4)


if __name__ == "__main__":
    unittest.main()
