"""Central pre-freeze regression gates for the unchanged v3 study rules."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sqlite3
import unittest

import offline_coordination_study_v2 as study


HERE = Path(__file__).resolve().parents[1]
V2 = HERE / "prospective_from_freeze_offline_study_v2"
RUN = V2 / "run_v2a"
WITNESSES = HERE / "metamorphic_witnesses_v2"
T0 = study.ROOT / "paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/semantic_reliability_experiment/states_v2b/T0_snapshot.sqlite"


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def table_snapshot(path: Path, table: str, columns: list[str]) -> list[tuple]:
    connection = sqlite3.connect(path)
    try:
        names = ",".join(f'"{name}"' for name in columns)
        return connection.execute(f'SELECT {names} FROM "{table}" ORDER BY rowid').fetchall()
    finally:
        connection.close()


class ReleaseV3CentralRegressionTests(unittest.TestCase):
    def test_selection_view_has_only_question_fields(self) -> None:
        rows = jsonl(V2 / "selection_inputs.jsonl")
        self.assertEqual(180, len(rows))
        self.assertTrue(all(set(row) == {"question_id", "question"} for row in rows))
        self.assertFalse(any(study.FORBIDDEN_SELECTION_FIELDS & set(row) for row in rows))

    def test_gold_read_is_after_all_seal_writes_in_runner(self) -> None:
        source = (HERE / "offline_coordination_study_v2.py").read_text(encoding="utf-8")
        seal = source.index('write_json(run_dir / "pre_gold_seal_manifest.json"')
        gold = source.index('gold_records = {row["question_id"]: row for row in load_jsonl(gold_path)}')
        self.assertLess(seal, gold)
        pre = json.loads((RUN / "pre_gold_seal_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(180, pre["blackboard_count"])
        self.assertTrue(pre["all_sealed"])

    def test_attempt_topology_is_180_by_8_by_4_before_decisions(self) -> None:
        attempts = jsonl(RUN / "candidate_execution_attempts.jsonl")
        self.assertEqual(180 * 8 * 4, len(attempts))
        manifest = json.loads((V2 / "freeze_manifest.json").read_text(encoding="utf-8"))
        state_hashes = [
            manifest["files"]["reference_database"]["sha256"],
            *(manifest["files"][f"state:{state}"]["sha256"] for state in [
                "M1_irrelevant_relation_rows", "M2_harmless_indexes_rebuild", "M3_nullable_schema_extension"
            ]),
        ]
        for offset in range(0, len(attempts), 4):
            self.assertEqual(state_hashes, [row["database_sha256"] for row in attempts[offset:offset + 4]])
        boards = jsonl(RUN / "blackboards_sealed_before_gold.jsonl")
        for board in boards:
            kinds = [message["kind"] for message in board["messages"]]
            self.assertEqual(16, sum(kind in {"validation_evidence", "counterfactual_evidence"} for kind in kinds))
            self.assertGreater(kinds.index("decision:fixed_order_equal_budget"), max(i for i, kind in enumerate(kinds) if kind == "counterfactual_evidence"))

    def test_witness_hashes_are_unique_and_integrity_ok(self) -> None:
        manifest = json.loads((WITNESSES / "WITNESS_MANIFEST.json").read_text(encoding="utf-8"))
        hashes = {manifest["base"]["sha256"], *(row["sha256"] for row in manifest["states"])}
        self.assertEqual(4, len(hashes))
        self.assertTrue(all(row["integrity_check"] == "ok" for row in manifest["states"]))

    def test_witness_logical_invariants_on_original_named_columns(self) -> None:
        base = sqlite3.connect(T0)
        try:
            tables = [row[0] for row in base.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
            columns = {table: [row[1] for row in base.execute(f'PRAGMA table_info("{table}")')] for table in tables}
        finally:
            base.close()
        for state in ["M1_irrelevant_relation_rows", "M2_harmless_indexes_rebuild", "M3_nullable_schema_extension"]:
            path = WITNESSES / f"{state}.sqlite"
            for table in tables:
                self.assertEqual(table_snapshot(T0, table, columns[table]), table_snapshot(path, table, columns[table]))

    def test_m3_explicit_projection_passes_and_select_star_is_predeclared_failure(self) -> None:
        m3 = WITNESSES / "M3_nullable_schema_extension.sqlite"
        explicit = "SELECT work_order_id, scheduled_date FROM work_orders ORDER BY work_order_id"
        wildcard = "SELECT * FROM work_orders ORDER BY work_order_id"
        for sql, should_match in [(explicit, True), (wildcard, False)]:
            def query(path: Path) -> tuple[list[str], list[tuple]]:
                connection = sqlite3.connect(path)
                try:
                    cursor = connection.execute(sql)
                    return [item[0] for item in cursor.description], cursor.fetchall()
                finally:
                    connection.close()
            self.assertEqual(should_match, query(T0) == query(m3))
        manifest = json.loads((WITNESSES / "WITNESS_MANIFEST.json").read_text(encoding="utf-8"))
        m3_record = next(row for row in manifest["states"] if row["state_id"] == "M3_nullable_schema_extension")
        self.assertIn("wildcard projections may fail", m3_record["invariant"])

    def test_validation_decisions_receive_no_counterfactual_scores(self) -> None:
        for board in jsonl(RUN / "blackboards_sealed_before_gold.jsonl"):
            decision = next(message["payload"] for message in board["messages"] if message["kind"] == "decision:validation_rank_equal_budget_no_cf")
            self.assertTrue(all(score["counterfactual_total"] == 0 and score["counterfactual_passes"] == 0 for score in decision["scores"]))

    def test_summary_is_recomputed_from_all_evaluation_rows(self) -> None:
        rows = jsonl(RUN / "evaluation_ledger.jsonl")
        summary = json.loads((RUN / "summary.json").read_text(encoding="utf-8"))
        for method, expected in summary["methods"].items():
            subset = [row for row in rows if row["method"] == method]
            self.assertEqual(180, len(subset))
            self.assertEqual(sum(row["correct"] for row in subset), expected["correct"])
            self.assertEqual(sum(row["covered"] for row in subset), expected["covered"])
            self.assertEqual(sum(row["robust_invariance"] for row in subset), expected["robust_invariance_selected"])

    def test_full_validation_differences_are_derived_not_assumed_as_improvement(self) -> None:
        selections = {(row["question_id"], row["method"]): row for row in jsonl(RUN / "selection_ledger_pre_gold.jsonl")}
        evaluations = {(row["question_id"], row["method"]): row for row in jsonl(RUN / "evaluation_ledger.jsonl")}
        qids = sorted({qid for qid, _ in selections})
        differences = [qid for qid in qids if selections[(qid, study.METHODS[1])]["selected_candidate_id"] != selections[(qid, study.METHODS[2])]["selected_candidate_id"]]
        derived_effects = Counter(
            evaluations[(qid, study.METHODS[2])]["correct"] - evaluations[(qid, study.METHODS[1])]["correct"]
            for qid in differences
        )
        self.assertEqual(len(differences), sum(derived_effects.values()))
        for qid in differences:
            validation_sql = selections[(qid, study.METHODS[1])]["selected_sql"]
            full_sql = selections[(qid, study.METHODS[2])]["selected_sql"]
            self.assertNotEqual(validation_sql, full_sql)
            self.assertTrue("*" in validation_sql or "*" in full_sql)


if __name__ == "__main__":
    unittest.main()
