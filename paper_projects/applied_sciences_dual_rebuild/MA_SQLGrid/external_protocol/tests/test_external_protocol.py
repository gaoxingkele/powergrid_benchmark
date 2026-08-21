"""Offline acceptance tests for the W4 MA external-database protocol."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[3]
OUTPUT = ROOT / "artifacts"
BUILDER = ROOT / "code" / "build_external_protocol.py"
sys.path.insert(0, str(BUILDER.parent))
import build_external_protocol as protocol  # noqa: E402


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class ExternalProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads((OUTPUT / "manifest.json").read_text(encoding="utf-8"))
        cls.prompts = read_jsonl(OUTPUT / "factorial_prompts.jsonl")
        cls.reference = read_jsonl(OUTPUT / "reference_sql_evaluation.jsonl")

    def test_exact_91_by_4_design_and_evidence_boundary(self) -> None:
        self.assertEqual(self.manifest["question_count"], 91)
        self.assertEqual(self.manifest["dataset_question_counts"], {
            "RTS_GMLC_AUTO_PILOT": 55,
            "SIMBENCH_AUTO_PILOT": 36,
        })
        self.assertEqual(len(self.prompts), 364)
        self.assertEqual(self.manifest["cell_counts_by_condition"], {name: 91 for name, _, _ in protocol.CELLS})
        self.assertTrue(all(row["annotation_status"] == "AUTO_CANDIDATE" for row in self.prompts))
        self.assertTrue(all(row["human_reviewed"] is False for row in self.prompts))
        self.assertTrue(all(row["sealed"] is False for row in self.prompts))
        self.assertEqual(self.manifest["paid_model_calls"], 0)
        self.assertEqual(self.manifest["network_calls"], 0)

    def test_registered_reference_never_enters_prompt(self) -> None:
        references = {row["instance_id"]: row["registered_reference_sql"] for row in self.reference}
        self.assertEqual(len(references), 91)
        for row in self.prompts:
            self.assertNotIn(references[row["instance_id"]].strip(), row["prompt"])
            self.assertNotIn("registered_reference_sql", row["prompt"])
            for prohibited_field in ("gold_sql", "gold_result", "answer_shape", "human_gold"):
                self.assertNotIn(prohibited_field, row["prompt"].lower())
        self.assertEqual(self.manifest["gold_leakage_count"], 0)

    def test_four_cells_share_database_question_and_perturbation(self) -> None:
        grouped = defaultdict(list)
        for row in self.prompts:
            grouped[row["instance_id"]].append(row)
        self.assertEqual(len(grouped), 91)
        expected_conditions = {name for name, _, _ in protocol.CELLS}
        expected_factors = {(scope, shape) for _, scope, shape in protocol.CELLS}
        for rows in grouped.values():
            self.assertEqual(len(rows), 4)
            self.assertEqual({row["condition"] for row in rows}, expected_conditions)
            self.assertEqual({(row["context_scope"], row["answer_shape_hints"]) for row in rows}, expected_factors)
            for field in ("database_hash", "schema_hash", "question_hash", "perturbation_id", "perturbation_hash"):
                self.assertEqual(len({row[field] for row in rows}), 1, field)
            self.assertEqual(len({row["perturbation_block"] for row in rows}), 1)
            for row in rows:
                self.assertEqual(
                    protocol.canonical_hash({"id": row["perturbation_id"], "block": row["perturbation_block"]}),
                    row["perturbation_hash"],
                )
            self.assertTrue(all(len(row["compact_selected_tables"]) <= 3 for row in rows))
            for row in rows:
                marker = "Question-derived answer-shape heuristic:" in row["context"]
                self.assertEqual(marker, row["answer_shape_hints"])
        self.assertEqual(self.manifest["symmetric_perturbation_failure_count"], 0)
        self.assertEqual(self.manifest["factor_mapping_failure_count"], 0)

    def test_reference_sql_interface_is_safe_executable_and_hashed(self) -> None:
        self.assertEqual(len(self.reference), 91)
        self.assertTrue(all(row["safe"] for row in self.reference))
        self.assertTrue(all(row["executable"] for row in self.reference))
        self.assertTrue(all(row["evidence_status"] == "AUTO_CANDIDATE_REGISTERED_REFERENCE_NOT_HUMAN_GOLD" for row in self.reference))
        self.assertTrue(all(row["human_reviewed"] is False and row["sealed"] is False for row in self.reference))
        self.assertTrue(all(len(row["result_sha256"]) == 64 for row in self.reference))
        self.assertEqual(sum(row["row_count"] == 0 for row in self.reference), 4)

        database = protocol.DATASETS["SIMBENCH_AUTO_PILOT"]["database"]
        accepted = protocol.evaluate_sql(database, "SELECT COUNT(*) AS n FROM buses;")
        self.assertTrue(accepted["safe"] and accepted["executable"])
        for unsafe in (
            "DROP TABLE buses;",
            "SELECT 1; DELETE FROM buses;",
            "PRAGMA table_info(buses);",
            "ATTACH DATABASE 'x' AS y;",
        ):
            rejected = protocol.evaluate_sql(database, unsafe)
            self.assertFalse(rejected["safe"], unsafe)
            self.assertFalse(rejected["executable"], unsafe)

    def test_shared_audit_and_provenance_hashes(self) -> None:
        audit = json.loads((OUTPUT / "shared_stat_audit.json").read_text(encoding="utf-8"))
        self.assertTrue(audit["audit"]["passed"])
        self.assertEqual(audit["audit"]["observed_unique_cells"], 364)
        self.assertEqual(audit["audit"]["expected_cartesian_cells"], 364)
        self.assertEqual(audit["audit"]["issues"], [])
        for config in self.manifest["datasets"].values():
            self.assertEqual(sha256_file(WORKSPACE / config["database_path"]), config["database_sha256"])
            self.assertRegex(config["schema_sha256"], r"^[0-9a-f]{64}$")
            self.assertRegex(config["questions_sha256"], r"^[0-9a-f]{64}$")
            self.assertRegex(config["source_manifest_sha256"], r"^[0-9a-f]{64}$")

        artifact_manifest = json.loads((OUTPUT / "artifact_manifest.json").read_text(encoding="utf-8"))
        for artifact in artifact_manifest["artifacts"]:
            path = ROOT / artifact["path"]
            self.assertEqual(path.stat().st_size, artifact["bytes"])
            self.assertEqual(sha256_file(path), artifact["sha256"])

    def test_rebuild_is_prompt_and_reference_hash_deterministic(self) -> None:
        before = self.manifest
        completed = subprocess.run(
            [sys.executable, str(BUILDER)], cwd=WORKSPACE,
            capture_output=True, text=True, encoding="utf-8", errors="replace", check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        after = json.loads((OUTPUT / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(before["prompt_set_sha256"], after["prompt_set_sha256"])
        self.assertEqual(before["reference_result_set_sha256"], after["reference_result_set_sha256"])
        self.assertEqual(before["datasets"], after["datasets"])

    def test_builder_contains_no_model_or_network_client(self) -> None:
        source = BUILDER.read_text(encoding="utf-8").lower()
        for forbidden in ("urllib", "requests", "openai", "anthropic", "api_key", "urlopen"):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
