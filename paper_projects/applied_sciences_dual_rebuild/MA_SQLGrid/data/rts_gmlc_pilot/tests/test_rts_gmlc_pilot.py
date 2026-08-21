"""Acceptance tests for the deterministic RTS-GMLC SQLite pilot."""

from __future__ import annotations

import hashlib
import json
import sqlite3
import subprocess
import sys
import unittest
from collections import defaultdict
from pathlib import Path


PILOT = Path(__file__).resolve().parents[1]
WORKSPACE = PILOT.parents[4]
ARTIFACTS = PILOT / "artifacts"
BUILDER = PILOT / "code" / "build_rts_gmlc_pilot.py"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class RTSGMLCPilotTests(unittest.TestCase):
    def test_database_integrity_foreign_keys_and_expected_rows(self) -> None:
        summary = json.loads((ARTIFACTS / "build_summary.json").read_text(encoding="utf-8"))
        expected = {
            "branches": 120,
            "buses": 73,
            "dispatch_da": 52416,
            "generator_constraints": 158,
            "generator_costs": 158,
            "generators": 158,
            "load_timeseries_da": 26352,
            "renewable_availability_da": 254736,
            "reserve_products": 7,
            "reserve_requirements_da": 26352,
        }
        self.assertEqual(summary["table_row_counts"], expected)
        self.assertEqual(summary["timeseries_coverage"]["load_da"]["timestamp_count"], 8784)
        self.assertEqual(summary["timeseries_coverage"]["renewable_da"]["generator_count"], 29)
        self.assertEqual(summary["timeseries_coverage"]["reserve_da"]["product_count"], 3)
        self.assertEqual(summary["timeseries_coverage"]["dispatch_da"]["generator_count"], 156)
        self.assertEqual(summary["database_sha256"], sha256_file(ARTIFACTS / "database.sqlite"))
        conn = sqlite3.connect(ARTIFACTS / "database.sqlite")
        try:
            self.assertEqual(conn.execute("PRAGMA integrity_check").fetchone()[0], "ok")
            self.assertEqual(conn.execute("PRAGMA foreign_key_check").fetchall(), [])
            tables = {row[0] for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )}
            self.assertEqual(tables, set(expected))
            self.assertEqual(
                conn.execute("SELECT MIN(timestamp), MAX(timestamp), COUNT(DISTINCT timestamp) FROM load_timeseries_da").fetchone(),
                ("2020-01-01 00:00:00", "2020-12-31 23:00:00", 8784),
            )
            self.assertEqual(
                conn.execute("SELECT MIN(timestamp), MAX(timestamp), COUNT(DISTINCT timestamp) FROM dispatch_da").fetchone(),
                ("2020-07-05 00:00:00", "2020-07-18 23:00:00", 336),
            )
        finally:
            conn.close()

    def test_field_dictionary_covers_every_database_column(self) -> None:
        dictionary = json.loads((ARTIFACTS / "field_dictionary.json").read_text(encoding="utf-8"))["fields"]
        documented = {(row["table"], row["column"]) for row in dictionary}
        self.assertTrue(all(row["source"] and row["transformation_or_unit_note"] for row in dictionary))
        conn = sqlite3.connect(ARTIFACTS / "database.sqlite")
        try:
            actual = set()
            tables = [row[0] for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )]
            for table in tables:
                actual.update((table, row[1]) for row in conn.execute(f'PRAGMA table_info("{table}")'))
        finally:
            conn.close()
        self.assertEqual(documented, actual)

    def test_source_and_artifact_hash_chains(self) -> None:
        source_manifest = json.loads((ARTIFACTS / "source_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(source_manifest["git_commit"], "3ece0d3725c844056132393ee252b3083dd4eab4")
        self.assertTrue(source_manifest["license_audit"]["redistribution_notice_required"])
        self.assertIn("ends mid-sentence", source_manifest["license_audit"]["upstream_notice_integrity_warning"])
        source_root = WORKSPACE / source_manifest["local_source_path"]
        source_rows = read_jsonl(ARTIFACTS / "source_files.jsonl")
        self.assertEqual(len(source_rows), 14)
        for row in source_rows:
            path = source_root / row["path_within_rts_gmlc"]
            self.assertEqual(path.stat().st_size, row["bytes"])
            self.assertEqual(sha256_file(path), row["sha256"])

        artifact_manifest = json.loads((ARTIFACTS / "artifact_manifest.json").read_text(encoding="utf-8"))
        for row in artifact_manifest["artifacts"]:
            path = (ARTIFACTS / row["path"]).resolve()
            self.assertEqual(path.stat().st_size, row["bytes"])
            self.assertEqual(sha256_file(path), row["sha256"])

    def test_auto_candidates_are_unsealed_family_disjoint_and_cover_required_sql(self) -> None:
        questions = read_jsonl(ARTIFACTS / "questions_auto_candidate.jsonl")
        self.assertEqual(len(questions), 55)
        self.assertEqual(len({row["question_id"] for row in questions}), 55)
        self.assertEqual(len({row["question"] for row in questions}), 55)
        self.assertTrue(all(row["annotation_status"] == "AUTO_CANDIDATE" for row in questions))
        self.assertTrue(all(row["human_reviewed"] is False for row in questions))
        self.assertTrue(all(row["sealed"] is False for row in questions))
        self.assertTrue(all(row["benchmark_claim_eligible"] is False for row in questions))
        family_splits = defaultdict(set)
        tags = set()
        table_mentions = set()
        for row in questions:
            family_splits[row["template_family"]].add(row["split"])
            tags.update(row["sql_feature_tags"])
            table_mentions.update(row["tables"])
            self.assertRegex(row["gold_sql_sha256"], r"^[0-9a-f]{64}$")
            self.assertRegex(row["gold_result_sha256"], r"^[0-9a-f]{64}$")
        self.assertTrue(all(len(splits) == 1 for splits in family_splits.values()))
        self.assertTrue({"single-table", "join", "aggregate", "time", "filter", "top-k", "cost", "constraint"}.issubset(tags))
        self.assertTrue({"dispatch_da", "generator_costs", "generator_constraints", "load_timeseries_da", "renewable_availability_da"}.issubset(table_mentions))

    def test_every_gold_sql_reexecutes_to_recorded_hash(self) -> None:
        questions = read_jsonl(ARTIFACTS / "questions_auto_candidate.jsonl")
        evidence = {row["question_id"]: row for row in read_jsonl(ARTIFACTS / "gold_execution.jsonl")}
        self.assertEqual(len(evidence), len(questions))
        conn = sqlite3.connect(ARTIFACTS / "database.sqlite")
        try:
            for question in questions:
                cursor = conn.execute(question["gold_sql"])
                result = {
                    "columns": [column[0] for column in cursor.description or []],
                    "rows": [list(row) for row in cursor.fetchall()],
                }
                result_hash = hashlib.sha256(
                    json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
                ).hexdigest()
                self.assertEqual(result_hash, question["gold_result_sha256"])
                self.assertEqual(result_hash, evidence[question["question_id"]]["result_sha256"])
                self.assertGreater(evidence[question["question_id"]]["row_count"], 0)
        finally:
            conn.close()

    def test_rebuild_is_binary_and_question_hash_deterministic(self) -> None:
        before = json.loads((ARTIFACTS / "build_summary.json").read_text(encoding="utf-8"))
        completed = subprocess.run(
            [sys.executable, str(BUILDER)], cwd=WORKSPACE,
            capture_output=True, text=True, encoding="utf-8", errors="replace", check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        after = json.loads((ARTIFACTS / "build_summary.json").read_text(encoding="utf-8"))
        for key in ("database_sha256", "schema_sha256", "gold_execution_result_set_sha256", "table_row_counts", "question_family_counts"):
            self.assertEqual(before[key], after[key])


if __name__ == "__main__":
    unittest.main()
