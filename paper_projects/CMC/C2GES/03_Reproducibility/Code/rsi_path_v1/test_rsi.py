"""Freeze-and-recompute tests for the RSI path-utility study."""
from __future__ import annotations

import json
import statistics
import tempfile
import unittest
from pathlib import Path

import re

from path_utilities import apply_utility
from rsi_common import PROJECT, assert_run_dir_writable, rouge_l_f1, word_count
from rsi_common import HERE, RUN_DIR

MANUSCRIPT = PROJECT / "01_Manuscript" / "LaTeX" / "paper_information.tex"
TABLE_LABEL = "tab:rsi-heldout"
CONDITION_ROWS = {
    "no_path_c2ges": "No-path",
    "redesigned_path": "Redesigned path",
    "textrank": "TextRank",
}


def manuscript_table_means(tex: str) -> dict[str, dict[int, float]]:
    match = re.search(
        r"\\label\{tab:rsi-heldout\}.*?\\begin\{tabular\}.*?\\midrule\n(.*?)\\bottomrule",
        tex,
        re.S,
    )
    if not match:
        raise AssertionError("tab:rsi-heldout tabular body not found")
    body = match.group(1)
    parsed: dict[str, dict[int, float]] = {}
    for condition, prefix in CONDITION_ROWS.items():
        row = re.search(
            rf"{re.escape(prefix)}[^&]*&\s*([0-9.]+)\s*&\s*([0-9.]+)\s*\\\\",
            body,
        )
        if not row:
            raise AssertionError(f"missing {condition} row in {TABLE_LABEL}")
        parsed[condition] = {110: float(row.group(1)), 260: float(row.group(2))}
    return parsed


class OverwriteGuardTests(unittest.TestCase):
    def test_refuses_existing_evaluation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            (run_dir / "EVALUATION.json").write_text("{}\n", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                assert_run_dir_writable(run_dir)

    def test_refuses_sealed_marker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            (run_dir / "SEALED").write_text("sealed\n", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                assert_run_dir_writable(run_dir)

    def test_empty_dir_is_writable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            assert_run_dir_writable(Path(tmp))


class UtilityUnitTests(unittest.TestCase):
    def test_gated_relevance_zeros_irrelevant_hub(self) -> None:
        class Node:
            def __init__(self, sid: str, role: str | None = None) -> None:
                self.sid = sid
                self.dominant_role = role

        nodes = [Node("a", "impact"), Node("b", "mitigation")]
        raw = {"a": 1.0, "b": 1.0}
        relevance = {"a": 1.0, "b": 0.0}
        words = {"a": 10, "b": 10}
        gated = apply_utility("gated_relevance", raw, nodes, relevance, words)
        self.assertGreater(gated["a"], gated["b"])
        historical = apply_utility("historical", raw, nodes, relevance, words)
        self.assertEqual(historical["a"], historical["b"])


class RecomputeSealedTests(unittest.TestCase):
    def test_recompute_mean_rougel_from_sealed_choices(self) -> None:
        sealed = RUN_DIR / "SEALED_CHOICES.jsonl"
        summary_path = RUN_DIR / "SUMMARY.json"
        self.assertTrue(sealed.is_file(), "sealed choices missing; run RSI first")
        self.assertTrue(MANUSCRIPT.is_file(), "paper_information.tex missing")
        rows = [json.loads(line) for line in sealed.read_text(encoding="utf-8").splitlines() if line.strip()]
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        paper = manuscript_table_means(MANUSCRIPT.read_text(encoding="utf-8"))
        self.assertEqual(len(rows), 15 * 2 * 3)
        cells = 0
        for condition in ("no_path_c2ges", "redesigned_path", "textrank"):
            for budget in (110, 260):
                values = []
                for row in rows:
                    if row["condition"] != condition or int(row["word_budget"]) != budget:
                        continue
                    recomputed = rouge_l_f1(row["selected_text"], row["reference_text"])
                    self.assertAlmostEqual(recomputed, float(row["rougeL_f1"]), places=12)
                    values.append(recomputed)
                self.assertEqual(len(values), 15)
                mean = statistics.fmean(values)
                self.assertAlmostEqual(mean, float(summary["means"][condition][str(budget)]), places=10)
                self.assertAlmostEqual(round(mean, 4), paper[condition][budget], places=4)
                cells += 1
        self.assertEqual(cells, 6)

    def test_protocol_predates_evaluation(self) -> None:
        protocol = HERE / "PROTOCOL.json"
        evaluation = RUN_DIR / "EVALUATION.json"
        self.assertTrue(protocol.is_file())
        self.assertTrue(evaluation.is_file())
        self.assertLess(protocol.stat().st_mtime, evaluation.stat().st_mtime)

    def test_word_count_is_shipped_counter(self) -> None:
        self.assertEqual(word_count("A 110-word test isn't truncated."), 5)


if __name__ == "__main__":
    unittest.main()
