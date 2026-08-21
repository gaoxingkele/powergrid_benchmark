"""Offline tests for the external local-model execution harness."""

from __future__ import annotations

import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import external_local_model_harness as harness  # noqa: E402


class ExternalLocalHarnessTests(unittest.TestCase):
    def test_registered_design_and_strict_prompt_boundary(self) -> None:
        prompts, manifest, references = harness.validate_registered_protocol()
        self.assertEqual((manifest["question_count"], len(prompts)), (91, 364))
        self.assertEqual({row["condition"] for row in prompts}, harness.EXPECTED_CELLS)
        self.assertEqual(len({harness.registered_key(row) for row in prompts}), 364)
        for row in prompts:
            self.assertEqual(harness.sha256_text(row["prompt"]), row["prompt_hash"])
            self.assertNotIn(references[row["instance_id"]]["registered_reference_sql"], row["prompt"])

    def test_loopback_only(self) -> None:
        for url in ("http://127.0.0.1:8000/v1", "http://localhost:11434/v1", "http://[::1]:8000/v1"):
            self.assertTrue(harness.is_loopback_url(url), url)
        for url in ("https://api.openai.com/v1", "http://192.168.1.2:8000/v1", "http://user:secret@localhost:8000/v1"):
            self.assertFalse(harness.is_loopback_url(url), url)

    def test_single_select_guard_and_sqlite_execution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = Path(directory) / "test.sqlite"
            conn = sqlite3.connect(db)
            conn.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, value TEXT)")
            conn.execute("INSERT INTO items(value) VALUES ('ok')")
            conn.commit(); conn.close()
            result = harness.execute_select(db, "WITH x AS (SELECT * FROM items) SELECT * FROM x;")
            self.assertTrue(result["safe"] and result["executable"])
            self.assertEqual(result["row_count"], 1)
            for sql in ("DROP TABLE items", "SELECT 1; SELECT 2", "PRAGMA table_info(items)",
                        "WITH x AS (SELECT 1) DELETE FROM items"):
                rejected = harness.execute_select(db, sql)
                self.assertFalse(rejected["safe"], sql)

    def test_dry_run_generates_exact_safe_plan_without_predictions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory) / "dry"
            self.assertEqual(harness.run(["--out", str(out)]), 0)
            manifest = json.loads((out / "run_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["status"], "dry_run_prompts_frozen_not_executed")
            self.assertEqual(manifest["cell_count"], 364)
            self.assertFalse(manifest["canonical_result_eligible"])
            self.assertFalse((out / "predictions.jsonl").exists())
            self.assertFalse((out / "run.lock.json").exists())
            prompt = json.loads((out / "prompts.jsonl").read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(prompt["exact_key_sha256"], harness.canonical_hash(prompt["exact_key"]))

    def test_lock_refuses_overlap_and_human_sealed_refuses(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory); lock = harness.RunLock(out, "a" * 64)
            with lock:
                with self.assertRaises(RuntimeError):
                    harness.RunLock(out, "a" * 64).__enter__()
            with self.assertRaises(SystemExit):
                harness.parse_args(["--scoring-authority", "HUMAN_SEALED"])

    def test_resume_refuses_duplicates_and_journal_divergence(self) -> None:
        key = ["DATASET", "QUESTION", "PERTURBATION", "CELL"]
        row = {"exact_key": key, "run_fingerprint": "frozen"}
        with self.assertRaisesRegex(RuntimeError, "duplicate prediction"):
            harness.validate_resume_checkpoints([row, dict(row)], [row], "frozen")
        with self.assertRaisesRegex(RuntimeError, "checkpoint key mismatch"):
            harness.validate_resume_checkpoints([row], [], "frozen")
        with self.assertRaisesRegex(RuntimeError, "fingerprint mismatch"):
            harness.validate_resume_checkpoints([{**row, "run_fingerprint": "changed"}], [row], "frozen")


if __name__ == "__main__":
    unittest.main()
