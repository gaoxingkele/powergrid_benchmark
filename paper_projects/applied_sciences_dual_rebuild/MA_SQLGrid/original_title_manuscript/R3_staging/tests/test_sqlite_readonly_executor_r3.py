import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

from sqlite_readonly_executor_r3 import SQLiteReadOnlyExecutor


class SQLiteReadOnlyExecutorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.database = self.root / "test.sqlite"
        connection = sqlite3.connect(self.database)
        connection.executescript(
            """
            CREATE TABLE assets(asset_id INTEGER PRIMARY KEY, status TEXT, secret TEXT);
            CREATE TABLE denied(note TEXT);
            INSERT INTO assets(status, secret) VALUES ('active', 'x'), ('retired', 'y'), ('active', 'z');
            INSERT INTO denied(note) VALUES ('private');
            """
        )
        connection.commit()
        connection.close()
        self.before = hashlib.sha256(self.database.read_bytes()).hexdigest()
        self.trace_path = self.root / "failures.jsonl"

    def tearDown(self):
        self.temp.cleanup()

    def executor(self, **kwargs):
        return SQLiteReadOnlyExecutor(
            self.database,
            allowed_tables={"assets": ["asset_id", "status"]},
            trace_path=self.trace_path,
            **kwargs,
        )

    def test_valid_select_and_database_unchanged(self):
        result = self.executor()("SELECT asset_id, status FROM assets ORDER BY asset_id")
        self.assertTrue(result["executable"])
        self.assertEqual(result["row_count"], 3)
        self.assertTrue(result["result_hash"])
        self.assertEqual(hashlib.sha256(self.database.read_bytes()).hexdigest(), self.before)
        self.assertTrue(result["trace"]["query_only"])
        self.assertTrue(result["trace"]["read_only_uri"])

    def test_mutation_ddl_attach_pragma_and_multiple_statements_fail_closed(self):
        attempts = [
            "INSERT INTO assets(status) VALUES ('x')",
            "UPDATE assets SET status='x'",
            "DELETE FROM assets",
            "CREATE TABLE x(a)",
            "DROP TABLE assets",
            "ATTACH DATABASE ':memory:' AS x",
            "PRAGMA schema_version",
            "SELECT 1; SELECT 2",
        ]
        executor = self.executor()
        for sql in attempts:
            with self.subTest(sql=sql):
                self.assertFalse(executor(sql)["executable"])
        self.assertEqual(hashlib.sha256(self.database.read_bytes()).hexdigest(), self.before)

    def test_dangerous_function_and_metadata_are_denied(self):
        executor = self.executor()
        self.assertFalse(executor("SELECT load_extension('x')")["executable"])
        self.assertFalse(executor("SELECT name FROM sqlite_master")["executable"])

    def test_table_and_column_authorization(self):
        executor = self.executor()
        self.assertFalse(executor("SELECT note FROM denied")["executable"])
        self.assertFalse(executor("SELECT secret FROM assets")["executable"])
        self.assertTrue(executor("SELECT status FROM assets")["executable"])

    def test_row_limit_is_retained_as_failure(self):
        result = self.executor(max_rows=2)("SELECT asset_id FROM assets")
        self.assertFalse(result["executable"])
        self.assertEqual(result["failure_kind"], "row_limit")

    def test_oversized_scalar_and_total_result_fail_closed(self):
        cell = self.executor(max_cell_bytes=32)("SELECT printf('%0100d', 1)")
        self.assertFalse(cell["executable"])
        self.assertEqual(cell["failure_kind"], "cell_byte_limit")
        total = self.executor(max_cell_bytes=128, max_result_bytes=12)(
            "SELECT status FROM assets ORDER BY asset_id"
        )
        self.assertFalse(total["executable"])
        self.assertEqual(total["failure_kind"], "result_byte_limit")

    def test_wide_projection_fails_closed(self):
        result = self.executor(max_output_columns=2)(
            "SELECT asset_id, status, asset_id AS duplicate_id FROM assets"
        )
        self.assertFalse(result["executable"])
        self.assertEqual(result["failure_kind"], "output_column_limit")

    def test_explicit_function_allowlist(self):
        executor = self.executor(allowed_functions=["count"])
        self.assertTrue(executor("SELECT count(*) FROM assets")["executable"])
        denied = executor("SELECT lower(status) FROM assets")
        self.assertFalse(denied["executable"])
        self.assertEqual(denied["failure_kind"], "authorization")

    def test_recursive_query_hits_registered_resource_limit(self):
        result = self.executor(max_opcodes=2_000, progress_step=100)(
            "WITH RECURSIVE cnt(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM cnt WHERE x<1000000) SELECT sum(x) FROM cnt"
        )
        self.assertFalse(result["executable"])
        self.assertIn(result["failure_kind"], {"opcode_limit", "timeout"})

    def test_trace_ledger_retains_every_attempt(self):
        executor = self.executor()
        executor("SELECT status FROM assets")
        executor("DELETE FROM assets")
        rows = [json.loads(line) for line in self.trace_path.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(len(rows), 2)
        self.assertTrue(rows[0]["executable"])
        self.assertFalse(rows[1]["executable"])


if __name__ == "__main__":
    unittest.main()
