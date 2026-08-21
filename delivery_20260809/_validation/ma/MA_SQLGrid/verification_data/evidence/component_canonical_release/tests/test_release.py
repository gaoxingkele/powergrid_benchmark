import csv
import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ComponentReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = json.loads((ROOT / "CANONICAL_RESULTS.json").read_text(encoding="utf-8"))
        cls.audit = json.loads((ROOT / "INDEPENDENT_AUDIT.json").read_text(encoding="utf-8"))

    def test_audit_pass_and_counts(self):
        self.assertEqual(self.audit["status"], "pass")
        self.assertEqual(self.audit["eligible_questions"], 170)
        for model in ("qwen", "granite"):
            self.assertEqual(self.audit["models"][model]["formal_rows"], 350)
            self.assertEqual(self.audit["models"][model]["zero_retry_rows"], 350)
            self.assertEqual(self.audit["models"][model]["independent_sqlite_rescored_rows"], 350)
            self.assertEqual(self.audit["models"][model]["independent_scoring_mismatches"], 0)

    def test_claim_boundaries(self):
        e1 = {x["model"]: x for x in self.results["effects"]["E1"]}
        e2 = {x["model"]: x for x in self.results["effects"]["E2"]}
        self.assertEqual(e1["qwen"]["claim_label"], "positive_component_efficacy")
        self.assertEqual(e1["granite"]["claim_label"], "no_detectable_improvement")
        self.assertTrue(all(x["claim_label"] == "no_detectable_improvement" for x in e2.values()))
        self.assertEqual(self.results["replication"], {"E1": False, "E2": False})
        self.assertTrue(all(not x["formal_latency_eligible"] for x in self.results["efficiency"]))

    def test_exact_key_estimates(self):
        e1 = {x["model"]: x for x in self.results["effects"]["E1"]}
        e2 = {x["model"]: x for x in self.results["effects"]["E2"]}
        self.assertAlmostEqual(e1["qwen"]["estimate"], 18/170)
        self.assertAlmostEqual(e1["granite"]["estimate"], 0)
        self.assertAlmostEqual(e2["qwen"]["estimate"], 7/180)
        self.assertAlmostEqual(e2["granite"]["estimate"], 10/180)

    def test_tables_have_expected_rows(self):
        with (ROOT / "table_primary_effects.csv").open(encoding="utf-8") as f:
            self.assertEqual(len(list(csv.DictReader(f))), 6)
        with (ROOT / "table_selection_descriptives.csv").open(encoding="utf-8") as f:
            self.assertEqual(len(list(csv.DictReader(f))), 2)

    def test_figure_triplets(self):
        for stem in ("figure_01_primary_effects", "figure_02_selection_descriptives", "figure_03_efficiency_diagnostics"):
            for ext in ("svg", "pdf", "png"):
                path = ROOT / f"{stem}.{ext}"
                self.assertTrue(path.is_file())
                self.assertGreater(path.stat().st_size, 1000)

    def test_manifest(self):
        manifest = json.loads((ROOT / "release_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["status"], "complete_and_verified")
        for name, record in manifest["files"].items():
            path = ROOT / Path(name)
            self.assertEqual(path.stat().st_size, record["bytes"])
            self.assertEqual(sha(path), record["sha256"])


if __name__ == "__main__":
    unittest.main()
