"""Unit tests for run_descriptive_addenda (synthetic fixtures only)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from run_descriptive_addenda import (  # noqa: E402
    dominant_roles_for_texts,
    q1_error_profile,
    q6_per_role,
    split_reference_sentences,
)


def _candidates(texts: list[str]) -> list[dict]:
    return [{"sid": f"u{i:05d}", "text": t, "page": 1} for i, t in enumerate(texts)]


class TestHelpers(unittest.TestCase):
    def test_split_reference_sentences(self) -> None:
        text = "The fault occurred at 09:12. Mitigation was recommended. Final note."
        self.assertEqual(split_reference_sentences(text), [
            "The fault occurred at 09:12.", "Mitigation was recommended.", "Final note."])

    def test_dominant_role_abstains_on_empty(self) -> None:
        self.assertEqual(dominant_roles_for_texts(["lorem ipsum dolor"]), [None])

    def test_dominant_role_fires_on_cue(self) -> None:
        roles = dominant_roles_for_texts(["the root cause failure mode was identified",
                                          "recommendation corrective preventive standard action"])
        self.assertEqual(roles[0], "root_cause")
        self.assertEqual(roles[1], "mitigation")


class TestQ1(unittest.TestCase):
    def test_blocked_beyond_window_pair_counted(self) -> None:
        # 16 candidates: root-cause cue at position 0, mitigation cue at 15 (distance 15 > 12)
        texts = ["filler text number %d" % i for i in range(16)]
        texts[0] = "the root cause failure was a protection setting"
        texts[15] = "recommendation corrective preventive measure standard"
        reports = [{"doc_id": "d1", "candidate_sentences": _candidates(texts)}]
        selections = {("d1", 110, "AB-5"): {"u00000"}, ("d1", 110, "AB-6"): {"u00015"},
                      ("d1", 260, "AB-5"): {"u00000"}, ("d1", 260, "AB-6"): {"u00015"}}
        deltas = {("d1", 110): -0.01, ("d1", 260): -0.01}
        cells, agg = q1_error_profile(reports, selections, deltas)
        self.assertEqual(len(cells), 4)
        by_unit = {r["unit"]: r for r in cells if r["word_budget"] == 110}
        self.assertEqual(by_unit["u00000"]["blocked_beyond_window_pairs"], 1)
        self.assertEqual(by_unit["u00015"]["blocked_beyond_window_pairs"], 1)
        self.assertEqual(by_unit["u00000"]["direction"], "added_by_full")
        self.assertEqual(by_unit["u00015"]["direction"], "dropped_by_full")
        neg = [r for r in agg if r["delta_sign"] == "negative" and r["word_budget"] == 110]
        self.assertEqual(len(neg), 1)
        self.assertEqual(neg[0]["changed_units"], 2)


class TestQ6(unittest.TestCase):
    def test_precision_and_coverage(self) -> None:
        cand = _candidates([
            "the root cause failure was a degraded protection setting",
            "a corrective recommendation was issued for the breaker",
            "unrelated background text without cues",
        ])
        reports = [{
            "doc_id": "d1",
            "candidate_sentences": cand,
            "reference_summary": "A corrective recommendation was issued for the breaker. Nothing else.",
        }]
        selections = {("d1", 110, "AB-5"): {"u00001"}, ("d1", 110, "AB-6"): {"u00002"}}
        rows = q6_per_role(reports, selections)
        mit = [r for r in rows if r["condition"] == "AB-5" and r["role"] == "mitigation"
               and r["word_budget"] == 110]
        self.assertEqual(len(mit), 1)
        self.assertEqual(mit[0]["selected_units_with_role"], 1)
        self.assertEqual(mit[0]["token_precision"], 1.0)
        self.assertEqual(mit[0]["token_coverage"], 1.0)


if __name__ == "__main__":
    unittest.main()
