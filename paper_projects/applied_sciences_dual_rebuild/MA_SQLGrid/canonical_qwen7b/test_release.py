import csv
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
STATS = HERE.parent / "statistics"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


class CanonicalQwenReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(HERE / "generate_release.py")], check=True, cwd=HERE)
        cls.manifest = json.loads((HERE / "release_manifest.json").read_text(encoding="utf-8"))
        cls.audit = json.loads((STATS / "MA_LOCAL_FORMAL_INDEPENDENT_AUDIT.json").read_text(encoding="utf-8"))

    def test_closed_source_policy_and_hashes(self):
        self.assertIn("Only the independent audit", self.manifest["input_policy"])
        self.assertIn("clean_rerun1", self.manifest["eligible_run_from_audit"])
        self.assertEqual(self.manifest["quarantined_run_excluded"], self.audit["quarantined_run"])
        expected = {
            "independent_audit": STATS / "MA_LOCAL_FORMAL_INDEPENDENT_AUDIT.json",
            "canonical_rows": STATS / "canonical_recomputed_rows.jsonl",
            "cell_summary": STATS / "table_cell_summary.csv",
            "factorial_effects": STATS / "table_factorial_effects.csv",
            "registered_contrasts": STATS / "table_registered_contrasts.csv",
        }
        for name, path in expected.items():
            self.assertEqual(self.manifest["source_hashes"][name]["sha256"], sha256(path))

    def test_canonical_counts_and_cell_numbers(self):
        self.assertEqual(self.manifest["canonical_counts"], {"rows": 720, "questions": 180, "conditions": 4, "template_clusters": 70, "family_clusters": 39})
        with (HERE / "tables/table01_cell_accuracy.csv").open(newline="", encoding="utf-8") as fh:
            rows = {r["condition"]: r for r in csv.DictReader(fh)}
        expected = {
            "F00_Full_NoShape": (76, 0.4222222222222222, 90, 0.5),
            "F01_Full_WithShape": (129, 0.7166666666666667, 174, 0.9666666666666667),
            "F10_Compact_NoShape": (78, 0.43333333333333335, 79, 0.4388888888888889),
            "F11_Compact_WithShape": (108, 0.6, 173, 0.9611111111111111),
        }
        for condition, values in expected.items():
            r = rows[condition]
            self.assertEqual(int(r["execution_correct"]), values[0])
            self.assertAlmostEqual(float(r["execution_accuracy"]), values[1], places=14)
            self.assertEqual(int(r["shape_correct"]), values[2])
            self.assertAlmostEqual(float(r["shape_accuracy"]), values[3], places=14)

    def test_factorial_and_registered_decisions(self):
        with (HERE / "tables/table02_factorial_effects.csv").open(newline="", encoding="utf-8") as fh:
            effects = {(r["metric"], r["effect"]): r for r in csv.DictReader(fh)}
        self.assertAlmostEqual(float(effects[("correct_int", "shape_hint_main")]["estimate"]), 0.23055555555555557)
        self.assertEqual(effects[("correct_int", "interaction")]["ci_excludes_zero"], "True")
        self.assertEqual(effects[("shape_int", "interaction")]["ci_excludes_zero"], "False")
        with (HERE / "tables/table03_registered_contrasts.csv").open(newline="", encoding="utf-8") as fh:
            contrasts = {(r["contrast"], r["metric"]): r for r in csv.DictReader(fh)}
        self.assertEqual(contrasts[("shape_at_full", "correct_int")]["holm_reject_0_05"], "True")
        self.assertEqual(contrasts[("compact_at_no_shape", "correct_int")]["holm_reject_0_05"], "False")
        self.assertEqual(contrasts[("compact_at_no_shape", "shape_int")]["holm_reject_0_05"], "True")

    def test_taxonomy_and_family_totals(self):
        with (HERE / "tables/table04_error_taxonomy.csv").open(newline="", encoding="utf-8") as fh:
            taxonomy = list(csv.DictReader(fh))
        self.assertEqual(sum(int(r["n"]) for r in taxonomy), 720)
        for r in taxonomy:
            total = sum(int(r[k]) for k in ["execution_and_shape_correct", "execution_only", "shape_only", "both_incorrect"])
            self.assertEqual(total, 180)
        with (HERE / "tables/table05_family_error_summary.csv").open(newline="", encoding="utf-8") as fh:
            family = list(csv.DictReader(fh))
        self.assertEqual(len(family), 39)
        self.assertEqual(sum(int(r["questions"]) for r in family), 180)
        self.assertEqual(sum(int(r["cell_rows"]) for r in family), 720)
        stable = [r for r in family if int(r["questions"]) >= 3]
        self.assertEqual(len(stable), 12)

    def test_figure_contract_and_png_dpi(self):
        for idx in range(1, 7):
            matches = list((HERE / "figures").glob(f"fig{idx:02d}_*"))
            self.assertEqual({p.suffix for p in matches}, {".svg", ".pdf", ".png"})
            png = next(p for p in matches if p.suffix == ".png")
            with Image.open(png) as image:
                self.assertGreaterEqual(image.width, 2000)
                self.assertAlmostEqual(image.info["dpi"][0], 450, delta=1)
            svg = next(p for p in matches if p.suffix == ".svg")
            self.assertIn("<text", svg.read_text(encoding="utf-8"))

    def test_scope_labels_and_output_hashes(self):
        captions = (HERE / "CAPTIONS.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(captions.count("single model/database; Granite pending"), 7)
        self.assertIn("Granite second-model robustness pending", self.manifest["claim_boundary"])
        for rel, meta in self.manifest["outputs"].items():
            path = HERE / rel
            self.assertTrue(path.is_file())
            self.assertEqual(meta["sha256"], sha256(path))
        qa_pdf = HERE / "qa/page_scale_preview.pdf"
        self.assertTrue(qa_pdf.is_file())
        self.assertGreater(qa_pdf.stat().st_size, 100_000)


if __name__ == "__main__":
    unittest.main(verbosity=2)
