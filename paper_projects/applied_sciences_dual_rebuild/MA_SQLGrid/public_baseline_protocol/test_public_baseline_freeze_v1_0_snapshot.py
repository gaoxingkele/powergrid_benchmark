"""Unit tests for the public-baseline freeze; no model generation occurs."""
from __future__ import annotations

import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

import freeze_public_baseline as f


class FreezeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = Path(self.temp.name) / "test.sqlite"
        con = sqlite3.connect(self.db)
        con.executescript("CREATE TABLE a(id INTEGER PRIMARY KEY, x TEXT); INSERT INTO a VALUES(1,'x'),(2,'x');")
        con.commit(); con.close()

    def tearDown(self):
        self.temp.cleanup()

    def test_official_ex_boundary(self):
        self.assertEqual(f.official_ex([(1,), (1,)], [(1,)]), 1)  # official set semantics
        self.assertEqual(f.official_ex([(1, 2)], [(2, 1)]), 0)
        self.assertEqual(f.official_ex([(2,), (1,)], [(1,), (2,)]), 1)

    def test_safe_execution(self):
        status, rows = f.safe_execute("SELECT x FROM a ORDER BY id", self.db)
        self.assertEqual(status, "SAFE_EXECUTED")
        self.assertEqual(rows, [("x",), ("x",)])
        self.assertNotEqual(f.safe_execute("DELETE FROM a", self.db)[0], "SAFE_EXECUTED")
        self.assertNotEqual(f.safe_execute("WITH q AS (SELECT 1) DELETE FROM a", self.db)[0], "SAFE_EXECUTED")
        check = sqlite3.connect(self.db)
        try:
            self.assertEqual(check.execute("SELECT count(*) FROM a").fetchone()[0], 2)
        finally:
            check.close()

    def test_error_vocabulary(self):
        self.assertEqual(f.safe_execute("SELECT nope FROM a", self.db)[0], "UNKNOWN_COLUMN")
        self.assertEqual(f.safe_execute("SELECT * FROM absent", self.db)[0], "UNKNOWN_TABLE")
        self.assertTrue(set(f.FEEDBACK) >= {"SAFE_EXECUTED", "UNKNOWN_COLUMN", "UNKNOWN_TABLE", "PARSE_ERROR"})

    def test_adapters_and_second_call(self):
        row = {"db_id": "d", "question": "q", "evidence": "e"}
        for method in f.METHODS:
            prompt = f.user_prompt(method, row, "TABLE a")
            self.assertNotIn("final answer from gold", prompt)
        repair = f.user_prompt("B3_EXEC_REPAIR", row, "TABLE a", second=True)
        self.assertIn("CANDIDATE_1", repair)
        self.assertIn("VALIDATOR_FEEDBACK", repair)
        self.assertIn("Always return", repair)

    def test_extractors(self):
        self.assertEqual(f.extract_sql("```sql\nSELECT 1\n```", "B0_DIRECT"), "SELECT 1")
        payload = json.dumps({"schema_links": [], "clause_plan": [], "final_sql": "SELECT 1"})
        self.assertEqual(f.extract_sql(payload, "B1_DECOMP"), "SELECT 1")
        self.assertEqual(f.extract_sql("not json", "B1_DECOMP"), "")


if __name__ == "__main__":
    unittest.main()
