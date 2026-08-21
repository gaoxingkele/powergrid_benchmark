import importlib.util
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("semantic_reliability", ROOT / "semantic_reliability.py")
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class SemanticReliabilityTests(unittest.TestCase):
    def test_read_only_lexical_gate(self):
        self.assertTrue(mod.clean_sql("SELECT 1;")[0])
        self.assertTrue(mod.clean_sql("WITH x AS (SELECT 1) SELECT * FROM x;")[0])
        for sql in ["DELETE FROM assets", "PRAGMA table_info(assets)", "SELECT 1; SELECT 2"]:
            self.assertFalse(mod.clean_sql(sql)[0])

    def test_read_only_authorizer_blocks_side_effect(self):
        with tempfile.TemporaryDirectory() as td:
            db = Path(td) / "x.sqlite"
            c = sqlite3.connect(db); c.execute("CREATE TABLE x(a INTEGER)"); c.execute("INSERT INTO x VALUES (1)"); c.commit(); c.close()
            c = mod.readonly_conn(db)
            try:
                self.assertTrue(mod.execute(c, "SELECT * FROM x")["ok"])
                with self.assertRaises(sqlite3.DatabaseError):
                    c.execute("DELETE FROM x")
            finally:
                c.close()

    def test_frozen_states_and_release_if_present(self):
        if not mod.FREEZE.exists():
            self.skipTest("freeze not built yet")
        lock = mod.validate_freeze()
        self.assertEqual(len(lock["states_manifest"]), 7)
        self.assertFalse(lock["prediction_files_accessed_during_freeze"])
        for rec in lock["states_manifest"]:
            c = sqlite3.connect((mod.HERE / rec["path"]).resolve().as_uri() + "?mode=ro&immutable=1", uri=True)
            try:
                self.assertEqual(c.execute("PRAGMA integrity_check").fetchone()[0], "ok")
                self.assertEqual(c.execute("PRAGMA foreign_key_check").fetchall(), [])
            finally:
                c.close()
        if mod.RESULTS.exists():
            result = json.loads(mod.RESULTS.read_text(encoding="utf-8"))
            self.assertEqual(result["denominators"]["prediction_state_executions"], 10080)
            self.assertEqual(result["gold"]["failures"], 0)
            self.assertEqual(sum(1 for _ in (mod.LOGS / "execution.jsonl").open(encoding="utf-8")), 10080)

    def test_generator_is_deterministic_and_integral(self):
        with tempfile.TemporaryDirectory() as td:
            a, b = Path(td) / "a.sqlite", Path(td) / "b.sqlite"
            ma = mod.build_state(a, ["combined"])
            mb = mod.build_state(b, ["combined"])
            self.assertEqual(mod.sha(a), mod.sha(b))
            self.assertEqual(ma, mb)
            self.assertEqual(ma["integrity_check"], ["ok"])
            self.assertEqual(ma["foreign_key_violations"], 0)
            base = sqlite3.connect(mod.DB)
            try:
                for table in mod.TABLE_ORDER:
                    n = base.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
                    self.assertEqual(ma["row_counts"][table], 2 * n)
            finally:
                base.close()


if __name__ == "__main__":
    unittest.main()
