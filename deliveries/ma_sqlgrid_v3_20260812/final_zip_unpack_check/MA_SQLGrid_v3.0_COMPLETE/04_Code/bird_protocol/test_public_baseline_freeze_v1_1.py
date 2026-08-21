"""Regression tests for the sole v1.1 execution-guard correction."""
from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

import freeze_public_baseline_v1_1 as f


class FreezeV11RegressionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = Path(self.temp.name) / "test.sqlite"
        con = sqlite3.connect(self.db)
        con.executescript("CREATE TABLE a(id INTEGER PRIMARY KEY, x TEXT); INSERT INTO a VALUES(1,'x'),(2,'y');")
        con.commit()
        con.close()

    def tearDown(self):
        self.temp.cleanup()

    def test_multistatement_warning_is_deterministically_classified(self):
        status, rows = f.safe_execute("SELECT id FROM a; SELECT x FROM a", self.db)
        self.assertEqual(status, "OTHER_EXECUTION_ERROR")
        self.assertIsNone(rows)

    def test_single_statement_behavior_is_unchanged(self):
        status, rows = f.safe_execute("SELECT id FROM a ORDER BY id", self.db)
        self.assertEqual(status, "SAFE_EXECUTED")
        self.assertEqual(rows, [(1,), (2,)])

    def test_warning_class_is_distinct_under_pinned_runtime(self):
        self.assertFalse(issubclass(sqlite3.Warning, sqlite3.Error))
        self.assertEqual(sqlite3.sqlite_version, "3.40.1")


if __name__ == "__main__":
    unittest.main()
