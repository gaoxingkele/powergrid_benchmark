import importlib.util
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("metadata", HERE / "build_rights_safe_metadata.py")
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MOD)


class MetadataTests(unittest.TestCase):
    def test_series_rules_match_frozen_builder(self):
        self.assertEqual(MOD.report_series("x", "2025 State of Reliability"), "series_state_of_reliability")
        self.assertEqual(MOD.report_series("x", "Solar PV Disturbance"), "series_solar_pv")
        self.assertEqual(MOD.report_series("unique", "Other report"), "unique")

    def test_local_inputs_account_for_all_40(self):
        r2 = HERE.parent
        root = next((p for p in (HERE, *HERE.parents) if (p / ".git").exists()), None)
        if root is None:
            root = next((p for p in (HERE, *HERE.parents) if (p / "C2GES_RELEASE_MARKER.json").is_file()), None)
        self.assertIsNotNone(root, "workspace or portable C2GES root must be discoverable")
        audit = r2 / "diagnostic_build_08/per_report_extraction_audit.jsonl"
        rights = r2 / "diagnostic_build_08/rights_ledger.jsonl"
        if not audit.exists() or not rights.exists():
            self.skipTest("restricted extraction audit and rights ledger are not distributed")
        rows = MOD.build(
            root / "data/public_datasets/reliability_reports/c2ges_nerc_reports/metadata/c2ges_nerc_report_manifest.json",
            audit,
            rights,
        )
        self.assertEqual(len(rows), 40)
        self.assertEqual(sum(r["inclusion_status"] == "included" for r in rows), 27)
        self.assertEqual(sum(r["exclusion_reason"] == "missing_executive_summary_heading" for r in rows), 11)
        self.assertEqual(sum(r["exclusion_reason"] == "missing_executive_summary_end" for r in rows), 2)
        forbidden = {"reference_summary", "candidate_sentences", "prediction", "selected_sentences"}
        self.assertTrue(all(forbidden.isdisjoint(r) for r in rows))


if __name__ == "__main__":
    unittest.main()
