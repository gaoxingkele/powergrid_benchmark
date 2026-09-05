import csv
import json
import tempfile
import unittest
from pathlib import Path

from human_validation import (
    FORM_FIELDS,
    cohen_kappa,
    final_analysis,
    freeze_pre,
    prepare_packets,
)


SCHEMA = {
    "schema": "test-v1",
    "tasks": {
        "role": {"fields": ["role_label"], "labels": {"role_label": ["root_cause", "trigger_event", "propagation_response", "impact", "mitigation", "none_other", "ambiguous_multiple", "cannot_judge"]}},
        "edge": {"fields": ["edge_supported", "edge_direction_correct", "lexical_only_false_relation", "context_sufficient"], "labels": {"edge_supported": ["yes", "no", "cannot_judge"], "edge_direction_correct": ["yes", "no", "cannot_judge"], "lexical_only_false_relation": ["yes", "no", "cannot_judge"], "context_sufficient": ["yes", "no", "cannot_judge"]}},
        "path": {"fields": ["path_validity", "path_adds_beyond_reservation"], "labels": {"path_validity": ["coherent", "partially_coherent", "unsupported", "directionally_inconsistent", "cannot_judge"], "path_adds_beyond_reservation": ["yes", "no", "cannot_judge"]}},
        "summary": {"fields": ["source_faithful", "critical_omission", "page_locator_correct"], "labels": {"source_faithful": ["yes", "no", "cannot_judge"], "critical_omission": ["yes", "no", "cannot_judge"], "page_locator_correct": ["yes", "no", "cannot_judge"]}},
        "unit": {"fields": ["unit_validity"], "labels": {"unit_validity": ["standalone", "needs_adjacent_context", "fused_or_malformed", "header_footer_table_contamination", "cannot_judge"]}},
    },
    "thresholds": {"role_macro_f1": 0.7, "role_kappa": 0.6, "edge_support_kappa": 0.6, "edge_direction_kappa": 0.6, "supported_edge_precision": 0.7, "coherent_or_partial_path_rate": 0.7, "page_locator_accuracy": 1.0, "source_faithfulness_rate": 0.9},
}


def write_csv(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)


class HumanValidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.schema = self.root / "schema.json"
        self.schema.write_text(json.dumps(SCHEMA), encoding="utf-8")
        self.manifest = self.root / "manifest.csv"
        self.manifest_fields = ["sample_id", "task", "report_series_id", "system_condition", "automated_role_label"]
        self.samples = [
            {"sample_id": "r1", "task": "role", "report_series_id": "s1", "system_condition": "Full", "automated_role_label": "root_cause"},
            {"sample_id": "e1", "task": "edge", "report_series_id": "s1", "system_condition": "Full", "automated_role_label": ""},
            {"sample_id": "p1", "task": "path", "report_series_id": "s2", "system_condition": "no-path", "automated_role_label": ""},
            {"sample_id": "s1", "task": "summary", "report_series_id": "s2", "system_condition": "Full", "automated_role_label": ""},
            {"sample_id": "u1", "task": "unit", "report_series_id": "s2", "system_condition": "Full", "automated_role_label": ""},
        ]
        write_csv(self.manifest, self.manifest_fields, self.samples)

    def tearDown(self):
        self.tmp.cleanup()

    def labelled(self, annotator, role="root_cause"):
        values = {
            "role": {"role_label": role},
            "edge": {"edge_supported": "yes", "edge_direction_correct": "yes", "lexical_only_false_relation": "no", "context_sufficient": "yes"},
            "path": {"path_validity": "coherent", "path_adds_beyond_reservation": "yes"},
            "summary": {"source_faithful": "yes", "critical_omission": "no", "page_locator_correct": "yes"},
            "unit": {"unit_validity": "standalone"},
        }
        rows = []
        for sample in self.samples:
            row = {field: "" for field in FORM_FIELDS}
            row.update(sample_id=sample["sample_id"], task=sample["task"], annotator_id=annotator)
            row.update(values[sample["task"]]); rows.append(row)
        return rows

    def test_prepare_does_not_leak_manifest_conditions(self):
        out = self.root / "packets"
        prepare_packets(self.manifest, self.schema, out, "A", "B")
        header = (out / "annotator_a_blinded.csv").read_text(encoding="utf-8").splitlines()[0]
        self.assertNotIn("system_condition", header)
        self.assertNotIn("automated_role_label", header)

    def test_missing_required_label_fails(self):
        a = self.root / "a.csv"; b = self.root / "b.csv"
        rows = self.labelled("A"); rows[0]["role_label"] = ""
        write_csv(a, FORM_FIELDS, rows); write_csv(b, FORM_FIELDS, self.labelled("B"))
        with self.assertRaisesRegex(ValueError, "invalid or missing"):
            freeze_pre(self.schema, self.manifest, a, b, self.root / "pre.json")

    def test_kappa_known_values(self):
        self.assertAlmostEqual(cohen_kappa(["y", "y", "n", "n"], ["y", "y", "n", "n"]), 1.0)
        self.assertAlmostEqual(cohen_kappa(["y", "y", "n", "n"], ["y", "n", "y", "n"]), 0.0)

    def test_final_rejects_changed_labels_and_incomplete_adjudication(self):
        a = self.root / "a.csv"; b = self.root / "b.csv"; pre = self.root / "pre.json"
        write_csv(a, FORM_FIELDS, self.labelled("A"))
        write_csv(b, FORM_FIELDS, self.labelled("B", role="impact"))
        freeze_pre(self.schema, self.manifest, a, b, pre)
        adjud = self.root / "adjud.csv"
        adjud_fields = ["sample_id", "task", "field", "annotator_a_value", "annotator_b_value", "adjudicated_value", "reason_code", "adjudicator_id", "notes_nonverbatim"]
        write_csv(adjud, adjud_fields, [])
        with self.assertRaisesRegex(ValueError, "exactly all disagreements"):
            final_analysis(self.schema, self.manifest, a, b, pre, adjud, self.root / "out")
        changed = self.labelled("A"); changed[-1]["notes_nonverbatim"] = "changed"
        write_csv(a, FORM_FIELDS, changed)
        with self.assertRaisesRegex(ValueError, "hashes changed"):
            final_analysis(self.schema, self.manifest, a, b, pre, adjud, self.root / "out")

    def test_final_writes_outputs_when_lock_and_adjudication_are_complete(self):
        a = self.root / "a.csv"; b = self.root / "b.csv"; pre = self.root / "pre.json"
        write_csv(a, FORM_FIELDS, self.labelled("A")); write_csv(b, FORM_FIELDS, self.labelled("B"))
        freeze_pre(self.schema, self.manifest, a, b, pre)
        adjud = self.root / "adjud.csv"
        adjud_fields = ["sample_id", "task", "field", "annotator_a_value", "annotator_b_value", "adjudicated_value", "reason_code", "adjudicator_id", "notes_nonverbatim"]
        write_csv(adjud, adjud_fields, [])
        out = self.root / "out"
        final_analysis(self.schema, self.manifest, a, b, pre, adjud, out)
        self.assertTrue((out / "human_structure_results.csv").is_file())
        gates = json.loads((out / "claim_gate_decisions.json").read_text(encoding="utf-8"))
        self.assertIn("all_structure_claim_gates_pass", gates)


if __name__ == "__main__":
    unittest.main()
