import csv
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import stat_audit


class StatAuditTests(unittest.TestCase):
    def setUp(self):
        self.hash_a = hashlib.sha256(b"input-a").hexdigest()
        self.rows = []
        # Treatment corrects two baseline errors and introduces none.
        for question, document, baseline, treatment in [
            ("q1", "d1", 0, 1),
            ("q2", "d1", 0, 1),
            ("q3", "d2", 1, 1),
            ("q4", "d2", 1, 1),
        ]:
            for condition, correct in [("baseline", baseline), ("treatment", treatment)]:
                self.rows.append({
                    "condition": condition,
                    "question_id": question,
                    "document_id": document,
                    "correct": correct,
                    "input_hash": self.hash_a,
                    "run_id": "run-001",
                })

    def test_clean_audit_and_statistics(self):
        audit = stat_audit.audit_records(
            self.rows, condition_field="condition", item_fields=["question_id"],
            cluster_field="document_id", metric_fields=["correct"],
            required_fields=["run_id"], hash_fields=["input_hash"],
            expected_conditions=["baseline", "treatment"],
        )
        self.assertTrue(audit["passed"])
        results = stat_audit.compare_conditions(
            self.rows, condition_field="condition", item_fields=["question_id"],
            cluster_field="document_id", metric_fields=["correct"],
            conditions=["baseline", "treatment"], bootstrap_samples=500,
            confidence=0.95, seed=7,
        )
        self.assertEqual(results[0]["complete_pair_count"], 4)
        self.assertAlmostEqual(results[0]["paired_cluster_bootstrap"]["estimate"], 0.5)
        self.assertEqual(results[0]["mcnemar_exact"]["treatment_only_correct"], 2)
        self.assertIn("p_value_holm", results[0]["mcnemar_exact"])

    def test_detects_cartesian_duplicate_cluster_and_hash_defects(self):
        dirty = list(self.rows)
        dirty.pop()  # missing treatment × q4
        dirty.append(dict(dirty[0]))  # duplicate baseline × q1
        dirty[1] = dict(dirty[1], document_id="wrong", input_hash="not-a-hash")
        audit = stat_audit.audit_records(
            dirty, condition_field="condition", item_fields=["question_id"],
            cluster_field="document_id", metric_fields=["correct"],
            required_fields=["run_id"], hash_fields=["input_hash"],
            expected_conditions=["baseline", "treatment"],
        )
        self.assertFalse(audit["passed"])
        codes = {issue["code"] for issue in audit["issues"]}
        self.assertTrue({
            "incomplete_cartesian_product", "duplicate_ids", "ambiguous_item_cluster",
            "invalid_hash_format", "inconsistent_item_hash",
        }.issubset(codes))

    def test_holm_known_values(self):
        adjusted = stat_audit.holm_adjust([0.01, 0.04, 0.03])
        self.assertEqual([round(value, 6) for value in adjusted], [0.03, 0.06, 0.06])

    def test_jsonl_loader(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "rows.jsonl"
            path.write_text("\n".join(json.dumps(row) for row in self.rows), encoding="utf-8")
            rows, detected = stat_audit.load_records(path)
            self.assertEqual(detected, "jsonl")
            self.assertEqual(len(rows), len(self.rows))

    def test_cli_writes_json_and_markdown(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "rows.csv"
            with source.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(self.rows[0]))
                writer.writeheader()
                writer.writerows(self.rows)
            json_out = root / "audit.json"
            markdown_out = root / "audit.md"
            completed = subprocess.run([
                sys.executable, str(Path(__file__).with_name("stat_audit.py")), str(source),
                "--item-fields", "question_id", "--cluster-field", "document_id",
                "--metrics", "correct", "--conditions", "baseline,treatment",
                "--required-fields", "run_id", "--hash-fields", "input_hash",
                "--bootstrap-samples", "200", "--json-out", str(json_out),
                "--markdown-out", str(markdown_out),
            ], capture_output=True, text=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertTrue(json.loads(json_out.read_text(encoding="utf-8"))["audit"]["passed"])
            self.assertIn("Overall audit: **PASS**", markdown_out.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
