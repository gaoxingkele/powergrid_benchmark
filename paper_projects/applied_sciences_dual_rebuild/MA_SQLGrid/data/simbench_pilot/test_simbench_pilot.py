import csv
import hashlib
import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[4]
SOURCE = WORKSPACE / "data/public_datasets/grid_cases/simbench"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def execute_hash(connection: sqlite3.Connection, sql: str) -> str:
    cursor = connection.execute(sql)
    payload = {"columns": [item[0] for item in cursor.description], "rows": [list(row) for row in cursor.fetchall()]}
    encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


class SimBenchPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(ROOT / "build_simbench_pilot.py"), "--source-root", str(SOURCE),
                        "--output-dir", str(ROOT)], check=True, capture_output=True, text=True)

    def test_required_artifacts_and_license_boundary(self):
        required = {"schema.sql", "source_manifest.json", "UPSTREAM_LICENSE.txt", "simbench_mv_urban.sqlite",
                    "questions_auto_candidate.csv", "gold_execution_results.jsonl", "field_dictionary.csv",
                    "data_card.json", "artifact_hashes.json"}
        self.assertTrue(all((ROOT / name).is_file() for name in required))
        manifest = json.loads((ROOT / "source_manifest.json").read_text(encoding="utf-8"))
        self.assertIn("ODbL", manifest["licenses"]["database"])
        self.assertIn("DbCL", manifest["licenses"]["individual_database_contents"])
        self.assertEqual(manifest["licenses"]["software"], "BSD 3-Clause")
        self.assertEqual(len(manifest["git_commit"]), 40)
        self.assertGreaterEqual(len(manifest["source_files"]), 19)

    def test_database_integrity_and_representative_assets(self):
        card = json.loads((ROOT / "data_card.json").read_text(encoding="utf-8"))
        expected = {"buses": 144, "lines": 147, "transformers": 2, "loads": 139,
                    "generators": 134, "switches": 305}
        for table, minimum in expected.items():
            self.assertEqual(card["table_counts"][table], minimum)
        with sqlite3.connect(ROOT / "simbench_mv_urban.sqlite") as connection:
            self.assertEqual(connection.execute("PRAGMA integrity_check").fetchone()[0], "ok")
            self.assertEqual(connection.execute("PRAGMA foreign_key_check").fetchall(), [])
            self.assertEqual({row[0] for row in connection.execute("SELECT nominal_kv FROM voltage_levels")}, {10.0, 110.0})

    def test_candidate_status_coverage_and_family_isolation(self):
        with (ROOT / "questions_auto_candidate.csv").open(encoding="utf-8", newline="") as handle:
            questions = list(csv.DictReader(handle))
        self.assertEqual(len(questions), 36)
        self.assertEqual({q["provenance_label"] for q in questions}, {"AUTO_CANDIDATE"})
        self.assertEqual({q["human_gold"] for q in questions}, {"False"})
        self.assertEqual({q["sealed"] for q in questions}, {"False"})
        self.assertEqual({q["query_class"] for q in questions},
                         {"single_table", "join", "aggregate", "filter", "top_k", "topology"})
        family_splits = defaultdict(set)
        for question in questions:
            family_splits[question["template_family_id"]].add(question["split"])
        self.assertTrue(all(len(splits) == 1 for splits in family_splits.values()))
        self.assertGreaterEqual(len(family_splits), 6)

    def test_gold_execution_hashes_recompute(self):
        with (ROOT / "questions_auto_candidate.csv").open(encoding="utf-8", newline="") as handle:
            questions = {row["question_id"]: row for row in csv.DictReader(handle)}
        results = [json.loads(line) for line in (ROOT / "gold_execution_results.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual(set(questions), {row["question_id"] for row in results})
        with sqlite3.connect(f"file:{(ROOT / 'simbench_mv_urban.sqlite').resolve()}?mode=ro", uri=True) as connection:
            for result in results:
                sql = questions[result["question_id"]]["gold_sql"]
                self.assertTrue(sql.upper().startswith(("SELECT", "WITH")))
                self.assertNotIn(";", sql)
                self.assertEqual(execute_hash(connection, sql), result["result_sha256"])

    def test_artifact_hash_manifest(self):
        manifest = json.loads((ROOT / "artifact_hashes.json").read_text(encoding="utf-8"))
        for artifact in manifest["artifacts"]:
            path = ROOT / artifact["path"]
            self.assertEqual(path.stat().st_size, artifact["bytes"])
            self.assertEqual(sha256(path), artifact["sha256"])

    def test_rebuild_is_deterministic(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            subprocess.run([sys.executable, str(ROOT / "build_simbench_pilot.py"), "--source-root", str(SOURCE),
                            "--output-dir", str(output)], check=True, capture_output=True, text=True)
            for name in ["schema.sql", "questions_auto_candidate.csv", "gold_execution_results.jsonl",
                         "field_dictionary.csv", "data_card.json", "simbench_mv_urban.sqlite"]:
                self.assertEqual(sha256(ROOT / name), sha256(output / name), name)


if __name__ == "__main__":
    unittest.main()
