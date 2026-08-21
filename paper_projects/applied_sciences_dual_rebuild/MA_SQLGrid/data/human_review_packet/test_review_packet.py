import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import agreement


ROOT = Path(__file__).resolve().parent
DATA_ROOT = ROOT.parent


class ReviewPacketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(ROOT / "build_review_packet.py"), "--data-root", str(DATA_ROOT),
                        "--output-dir", str(ROOT)], check=True, capture_output=True, text=True)

    def read_form(self, name):
        with (ROOT / name).open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))

    def test_exact_input_counts_and_status_boundary(self):
        items = [json.loads(line) for line in (ROOT / "machine_precheck.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual(len(items), 91)
        self.assertEqual(sum(item["dataset"] == "RTS-GMLC" for item in items), 55)
        self.assertEqual(sum(item["dataset"] == "SimBench" for item in items), 36)
        self.assertTrue(all(item["annotation_status"] == "AUTO_CANDIDATE" for item in items))
        self.assertTrue(all(not item["human_reviewed"] and not item["sealed"] for item in items))
        self.assertTrue(all(item["machine_precheck_only"] for item in items))

    def test_forms_are_complete_blind_skeletons_with_different_order(self):
        a, b = self.read_form("reviewer_A_form.csv"), self.read_form("reviewer_B_form.csv")
        self.assertEqual(len(a), 91); self.assertEqual(len(b), 91)
        self.assertEqual({row["blind_item_id"] for row in a}, {row["blind_item_id"] for row in b})
        self.assertNotEqual([row["blind_item_id"] for row in a], [row["blind_item_id"] for row in b])
        for row in a + b:
            self.assertEqual(row["decision"], "")
            self.assertNotIn("machine_risk", row)
            self.assertNotIn("machine_flags", row)

    def test_family_and_category_coverage(self):
        items = [json.loads(line) for line in (ROOT / "machine_precheck.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertGreaterEqual(len({(item["dataset"], item["template_family"]) for item in items}), 17)
        self.assertTrue({"single_table", "filter", "join", "aggregate", "top_k", "topology"}.issubset(
            {item["query_class"] for item in items}))
        self.assertTrue({"easy", "medium", "hard"}.issubset({item["difficulty"] for item in items}))

    def test_map_and_adjudication_cover_all_blind_ids(self):
        mapping = self.read_form("review_item_map.csv")
        adjudication = self.read_form("conflict_adjudication_template.csv")
        self.assertEqual(len(mapping), 91); self.assertEqual(len(adjudication), 91)
        self.assertEqual({row["blind_item_id"] for row in mapping}, {row["blind_item_id"] for row in adjudication})

    def test_agreement_math_known_cases(self):
        left = ["YES", "YES", "NO", "NO"]
        right = ["YES", "NO", "NO", "NO"]
        self.assertAlmostEqual(agreement.cohen_kappa(left, right), 0.5)
        rows_a, rows_b = {}, {}
        for index in range(4):
            key = f"x{index}"
            base = {field: "YES" for field in agreement.FIELDS}
            rows_a[key] = {"blind_item_id": key, "dataset": "x", **base}
            rows_b[key] = {"blind_item_id": key, "dataset": "x", **base}
        rows_b["x1"]["decision"] = "NO"
        report, conflicts = agreement.calculate(rows_a, rows_b)
        self.assertEqual(report["fields"]["decision"]["raw_agreement"], 0.75)
        self.assertEqual(len(conflicts), 1)

    def test_agreement_cli_emits_machine_and_human_reports(self):
        a = self.read_form("reviewer_A_form.csv")[:3]
        b_by_id = {row["blind_item_id"]: row for row in self.read_form("reviewer_B_form.csv")}
        b = [b_by_id[row["blind_item_id"]] for row in a]
        for rows in (a, b):
            for row in rows:
                row.update({field: "YES" for field in agreement.FIELDS})
                row["decision"] = "ACCEPT"
        b[1]["sql_correct"] = "NO"
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name, rows in (("a.csv", a), ("b.csv", b)):
                with (root / name).open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                    writer.writeheader(); writer.writerows(rows)
            completed = subprocess.run([
                sys.executable, str(ROOT / "agreement.py"), "--reviewer-a", str(root / "a.csv"),
                "--reviewer-b", str(root / "b.csv"), "--json-out", str(root / "agreement.json"),
                "--markdown-out", str(root / "agreement.md"), "--conflicts-out", str(root / "conflicts.csv")
            ], capture_output=True, text=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            report = json.loads((root / "agreement.json").read_text(encoding="utf-8"))
            self.assertEqual(report["item_count"], 3)
            self.assertEqual(report["conflict_count"], 1)
            self.assertIn("Cohen kappa", (root / "agreement.md").read_text(encoding="utf-8"))

    def test_build_is_deterministic(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp)
            subprocess.run([sys.executable, str(ROOT / "build_review_packet.py"), "--data-root", str(DATA_ROOT),
                            "--output-dir", str(out)], check=True, capture_output=True, text=True)
            for name in ["machine_precheck.jsonl", "machine_precheck_summary.json", "review_item_map.csv",
                         "reviewer_A_form.csv", "reviewer_B_form.csv", "conflict_adjudication_template.csv",
                         "packet_hashes.json"]:
                self.assertEqual((ROOT / name).read_bytes(), (out / name).read_bytes(), name)


if __name__ == "__main__":
    unittest.main()
