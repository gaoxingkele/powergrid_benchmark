"""Offline contract tests for the registered Applied Sciences factorial run."""

from __future__ import annotations

import contextlib
import importlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SOURCE = Path(__file__).resolve().parents[1]
EXPERIMENT = SOURCE / "code" / "experiment_final"
sys.path.insert(0, str(EXPERIMENT))
factorial = importlib.import_module("applsci_factorial")


class AppliedSciencesFactorialTests(unittest.TestCase):
    def run_quietly(self, arguments: list[str]) -> int:
        with contextlib.redirect_stdout(io.StringIO()):
            return factorial.run(arguments)

    def test_full_dry_run_is_balanced_stable_and_gold_free(self) -> None:
        with tempfile.TemporaryDirectory() as first_dir, tempfile.TemporaryDirectory() as second_dir:
            self.assertEqual(self.run_quietly(["--out", first_dir]), 0)
            self.assertEqual(self.run_quietly(["--out", second_dir]), 0)
            first = json.loads((Path(first_dir) / "manifest.json").read_text(encoding="utf-8"))
            second = json.loads((Path(second_dir) / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(first["question_count"], 180)
            self.assertEqual(first["prompt_count"], 720)
            self.assertEqual(first["prompt_counts_by_cell"], {name: 180 for name in factorial.CELL_NAMES})
            self.assertEqual(first["prompt_set_sha256"], second["prompt_set_sha256"])
            prompts = factorial.read_jsonl(Path(first_dir) / "prompts.jsonl")
            records = {row["question_id"]: row for row in factorial.formal.load_split_records("formal")}
            for prompt in prompts:
                gold = records[prompt["question_id"]]["gold_sql"]
                self.assertNotIn(gold, prompt["prompt"])
                self.assertEqual(prompt["prompt_hash"], factorial.stable_hash(prompt["prompt"]))
                self.assertEqual(prompt["context_hash"], factorial.stable_hash(prompt["context"]))

    def test_existing_outputs_require_explicit_resume_or_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as out_dir:
            self.run_quietly(["--out", out_dir, "--max-questions", "1"])
            with self.assertRaisesRegex(RuntimeError, "refusing to overwrite"):
                self.run_quietly(["--out", out_dir, "--max-questions", "1"])
            self.assertEqual(self.run_quietly(["--out", out_dir, "--max-questions", "1", "--resume"]), 0)

    def test_provider_failure_is_recorded_without_fabricated_sql(self) -> None:
        failure = {
            "ok": False,
            "response": None,
            "response_hash": None,
            "model_returned": None,
            "latency_ms": 3,
            "token_input": 0,
            "token_output": 0,
            "token_total": 0,
            "retry_count": 2,
            "error_type": "URLError",
            "error_message": "offline test",
        }
        with tempfile.TemporaryDirectory() as out_dir:
            with mock.patch.dict(os.environ, {"TEST_FACTORIAL_API_KEY": "not-a-real-key"}), mock.patch.object(
                factorial, "call_openai_compatible", return_value=failure
            ):
                self.run_quietly(
                    [
                        "--out", out_dir,
                        "--execute",
                        "--max-questions", "1",
                        "--base-url", "https://user:secret@example.invalid/v1?key=secret",
                        "--model", "offline-model",
                        "--api-key-env", "TEST_FACTORIAL_API_KEY",
                    ]
                )
            predictions = factorial.read_jsonl(Path(out_dir) / "predictions.jsonl")
            self.assertEqual(len(predictions), 4)
            self.assertTrue(all(row["status"] == "provider_error" for row in predictions))
            self.assertTrue(all(row["predicted_sql"] is None for row in predictions))
            self.assertTrue(all(row["response_hash"] is None for row in predictions))
            self.assertNotIn("secret", predictions[0]["base_url"])
            self.assertNotIn("user", predictions[0]["base_url"])
            self.assertNotIn("SELECT 1", json.dumps(predictions))
            manifest = json.loads((Path(out_dir) / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["status"], "completed_with_failures")
            self.assertEqual(manifest["status_counts"]["provider_error"], 4)
            self.assertEqual(manifest["score_status_counts"]["not_scored"], 4)

    def test_gold_fields_are_rejected_on_prompt_path(self) -> None:
        record = factorial.formal.load_split_records("formal")[0]
        self.assertNotIn("gold_sql", factorial.without_gold(record))
        with self.assertRaisesRegex(ValueError, "gold fields"):
            factorial.build_contexts(mock.Mock(), record)

    def test_local_provider_rejects_non_loopback_endpoint(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            factorial.parse_args(
                [
                    "--execute",
                    "--provider", "local-openai-compatible",
                    "--base-url", "http://192.0.2.10:8080/v1",
                    "--model", "local-test-model",
                    "--local-model-manifest", "manifest.json",
                ]
            )

    def test_local_dev_smoke_is_noncanonical_and_never_gold_scored(self) -> None:
        model_bytes = b"tiny-test-model-artifact"
        model_sha = factorial.stable_hash(model_bytes)
        provider_result = {
            "ok": True,
            "response": "```sql\nSELECT 1 AS smoke_value;\n```",
            "response_hash": factorial.stable_hash("```sql\nSELECT 1 AS smoke_value;\n```"),
            "model_returned": "local-test-model",
            "latency_ms": 7,
            "token_input": 11,
            "token_output": 9,
            "token_total": 20,
            "retry_count": 0,
            "error_type": None,
            "error_message": None,
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            model_file = root / "model.gguf"
            model_file.write_bytes(model_bytes)
            local_manifest = root / "local_model.json"
            local_manifest.write_text(
                json.dumps(
                    {
                        "schema_version": "ma-sqlgrid-local-model-v1",
                        "served_model_id": "local-test-model",
                        "model_repo": "local/test",
                        "model_revision": "test-revision",
                        "model_file": str(model_file),
                        "model_sha256": model_sha,
                        "model_bytes": len(model_bytes),
                        "license": "test-only",
                        "backend": "test-server",
                        "backend_revision": "test-backend-revision",
                    }
                ),
                encoding="utf-8",
            )
            out = root / "out"
            with mock.patch.object(factorial, "call_openai_compatible", return_value=provider_result):
                self.assertEqual(
                    self.run_quietly(
                        [
                            "--out", str(out),
                            "--execute",
                            "--provider", "local-openai-compatible",
                            "--base-url", "http://127.0.0.1:8080/v1",
                            "--model", "local-test-model",
                            "--local-model-manifest", str(local_manifest),
                            "--split", "dev-smoke",
                            "--max-questions", "1",
                            "--retries", "0",
                        ]
                    ),
                    0,
                )
            manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
            predictions = factorial.read_jsonl(out / "predictions.jsonl")
            diagnostics = factorial.read_jsonl(out / "scores.jsonl")
            self.assertEqual(manifest["status"], "noncanonical_smoke_completed")
            self.assertFalse(manifest["canonical_result_eligible"])
            self.assertFalse(manifest["gold_scoring_enabled"])
            self.assertEqual(manifest["configuration"]["local_model"]["model_sha256"], model_sha)
            self.assertEqual(len(predictions), 4)
            self.assertTrue(all(row["status"] == "success" for row in predictions))
            self.assertTrue(all(row["response_hash"] for row in predictions))
            self.assertTrue(all(row["status"] == "diagnostic_only" for row in diagnostics))
            self.assertTrue(all(row["correct"] is None for row in diagnostics))


if __name__ == "__main__":
    unittest.main()
