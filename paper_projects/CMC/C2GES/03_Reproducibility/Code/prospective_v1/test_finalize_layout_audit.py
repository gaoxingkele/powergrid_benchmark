from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from finalize_layout_audit import finalize


class FinalizeLayoutAuditTests(unittest.TestCase):
    def write(self, path: Path, field: str, labels: list[str]) -> None:
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=["doc_id", "candidate_id", "normalized_sha256", field])
            writer.writeheader()
            for number, label in enumerate(labels):
                writer.writerow({"doc_id": "doc", "candidate_id": f"u{number}", "normalized_sha256": f"{number + 1:064x}", field: label})

    def test_pass_summary_uses_adjudicated_labels(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            a, b, final, output = (root / name for name in ("a.csv", "b.csv", "final.csv", "summary.json"))
            labels = ["valid_standalone"] * 9 + ["valid_with_adjacent_context"]
            self.write(a, "reviewer_a_validity", labels); self.write(b, "reviewer_b_validity", labels); self.write(final, "adjudication", labels)
            result = finalize(a, b, final, output, "reviewer-A", "reviewer-B")
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["candidate_validity_rate"], 1.0)
            self.assertTrue(output.is_file())

    def test_failure_gate_and_distinct_reviewer_guard(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            a, b, final = (root / name for name in ("a.csv", "b.csv", "final.csv"))
            labels = ["valid_standalone"] * 8 + ["fragment_or_truncated"] * 2
            self.write(a, "reviewer_a_validity", labels); self.write(b, "reviewer_b_validity", labels); self.write(final, "adjudication", labels)
            self.assertEqual(finalize(a, b, final, root / "fail.json", "A", "B")["status"], "FAIL")
            with self.assertRaisesRegex(ValueError, "distinct"):
                finalize(a, b, final, root / "other.json", "A", "A")


if __name__ == "__main__":
    unittest.main()
