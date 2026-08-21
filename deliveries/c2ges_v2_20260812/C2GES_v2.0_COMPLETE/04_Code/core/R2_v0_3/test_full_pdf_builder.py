from __future__ import annotations

import json
import subprocess
import unittest

from build_full_pdf_dataset import (
    Line,
    SOURCE_MANIFEST,
    SOURCE_ROOT,
    deduplicate_candidates,
    locate_summary,
    longest_common_substring_at_least,
    pollution_counts,
    recurrent_line_keys,
    report_series,
    remove_reference_leakage,
    split_candidates,
    split_pdf_pages,
    pdf_pages,
    flatten_pages,
)


class FullPdfBuilderTests(unittest.TestCase):
    def test_terminal_form_feed_does_not_add_page(self) -> None:
        self.assertEqual(split_pdf_pages("page one\fpage two\f"), ["page one", "page two"])
        self.assertEqual(split_pdf_pages("page one\fpage two"), ["page one", "page two"])

    def test_complete_summary_boundary(self) -> None:
        lines = [
            Line(1, 1, "Contents"),
            Line(2, 1, "Executive Summary"),
            Line(2, 2, "A " + "substantive finding " * 40 + "."),
            Line(3, 1, "1 Introduction"),
            Line(3, 2, "The body begins here."),
        ]
        start, end, error = locate_summary(lines)
        self.assertIsNone(error)
        self.assertEqual(lines[start].text, "Executive Summary")
        self.assertEqual(lines[end].text, "1 Introduction")

    def test_reference_substring_gate(self) -> None:
        shared = "a deterministic phrase longer than fifty characters that must be removed from candidates"
        rows = [
            {"sid": "s1", "page": 2, "text": shared + " with suffix."},
            {"sid": "s2", "page": 3, "text": "A completely unrelated engineering observation remains available for selection."},
        ]
        kept, removed = remove_reference_leakage(rows, "Official summary: " + shared + ".")
        self.assertEqual(len(removed), 1)
        self.assertEqual(len(kept), 1)
        self.assertEqual(longest_common_substring_at_least("short", "short", 50), 0)

    def test_no_fixed_eighty_sentence_cap(self) -> None:
        lines = [
            Line(page=(idx // 20) + 1, line=idx + 1, text=f"Sentence {idx} contains enough deterministic engineering words for stable segmentation and audit.")
            for idx in range(125)
        ]
        candidates, _ = split_candidates(lines, set())
        self.assertEqual(len(candidates), 125)
        self.assertGreater(len(candidates), 80)

    def test_recurrent_header_is_removed(self) -> None:
        lines = []
        for page in range(1, 11):
            lines.extend(
                [
                    Line(page, 1, "NERC Confidential Running Header"),
                    Line(page, 2, f"Page {page} body sentence contains sufficient engineering words for deterministic extraction."),
                ]
            )
        recurrent = recurrent_line_keys(lines, 10)
        self.assertIn("nerc confidential running header", recurrent)

    def test_running_title_with_changing_page_number_is_recurrent(self) -> None:
        lines = [Line(page, 1, f"N OVEMBER 13 W YOMING D ISTURBANCE {page}") for page in range(1, 11)]
        recurrent = recurrent_line_keys(lines, 10)
        self.assertIn("n ovember w yoming d isturbance", recurrent)
        candidates, drops = split_candidates(lines, recurrent)
        self.assertEqual(candidates, [])
        self.assertEqual(drops["recurrent_header_footer"], 10)

    def test_pollution_gate(self) -> None:
        rows = [
            {"sid": "s1", "page": 1, "text": "<Public> malformed \ufffd row"},
            {"sid": "s2", "page": 2, "text": "Executive Summary fused into body text."},
            {"sid": "s3", "page": 3, "text": "Introduction Table I.1 fused layout row."},
        ]
        counts = pollution_counts(rows)
        self.assertEqual(counts["public_marker"], 1)
        self.assertEqual(counts["replacement_character"], 1)
        self.assertEqual(counts["executive_summary_running_head"], 1)
        self.assertEqual(counts["section_table_fusion"], 1)

    def test_reproduced_real_pdf_boundaries_and_page_counts(self) -> None:
        expected = {
            "nerc_001": (8, "Introduction"),
            "nerc_008": (8, "Chapter 1: Disturbance Analyses"),
            "nerc_011": (10, "Introduction"),
            "nerc_028": (7, "Introduction"),
            "nerc_040": (12, "Chapter 1: Availability Data Systems Assessment"),
        }
        manifest = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
        for prefix, (expected_page, expected_heading) in expected.items():
            source = next(row for row in manifest if row["doc_id"].startswith(prefix))
            pdf = SOURCE_ROOT / source["local_pdf"]
            pages = pdf_pages(pdf)
            info = subprocess.run(
                ["pdfinfo", str(pdf)], check=True, capture_output=True, text=True, errors="replace"
            ).stdout
            declared_pages = int(next(line.split(":", 1)[1] for line in info.splitlines() if line.startswith("Pages:")))
            self.assertEqual(len(pages), declared_pages, source["doc_id"])
            lines = flatten_pages(pages)
            start, end, error = locate_summary(lines)
            self.assertIsNone(error, source["doc_id"])
            self.assertEqual(lines[end].page, expected_page, source["doc_id"])
            self.assertEqual(" ".join(lines[end].text.split()), expected_heading, source["doc_id"])
            self.assertGreater(lines[end].page, lines[start].page, source["doc_id"])

    def test_duplicate_candidates_keep_first_page_anchor(self) -> None:
        rows = [
            {"sid": "s1", "page": 3, "text": "The same sufficiently long engineering sentence is repeated in the report."},
            {"sid": "s2", "page": 8, "text": "The same sufficiently long engineering sentence is repeated in the report."},
        ]
        kept, removed = deduplicate_candidates(rows)
        self.assertEqual(len(kept), 1)
        self.assertEqual(kept[0]["page"], 3)
        self.assertEqual(removed[0]["first_page"], 3)

    def test_known_report_series_are_grouped(self) -> None:
        self.assertEqual(report_series("a", "June 2022 Odessa Disturbance Report"), "series_odessa")
        self.assertEqual(report_series("b", "Odessa Disturbance Report"), "series_odessa")
        self.assertEqual(report_series("c", "2025 State of Reliability Report"), "series_state_of_reliability")


if __name__ == "__main__":
    unittest.main()
