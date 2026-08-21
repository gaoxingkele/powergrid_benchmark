import csv
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
MA = HERE.parent


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


class DualBackboneReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(HERE / "generate_release.py")], check=True, cwd=HERE)
        cls.manifest = json.loads((HERE / "release_manifest.json").read_text(encoding="utf-8"))

    def test_closed_audited_source_hashes(self):
        self.assertEqual(len(self.manifest["source_hashes"]), 12)
        for meta in self.manifest["source_hashes"].values():
            path = MA.parent.parent.parent / meta["path"]
            self.assertTrue(path.is_file(), path)
            self.assertEqual(meta["sha256"], sha256(path))
        self.assertTrue(self.manifest["audit_decisions"]["qwen_passed"])
        self.assertTrue(self.manifest["audit_decisions"]["granite_passed"])

    def test_counts_and_exact_cells(self):
        self.assertEqual(self.manifest["canonical_counts"]["rows_per_backbone"], 720)
        self.assertEqual(self.manifest["canonical_counts"]["paired_questions"], 180)
        with (HERE / "tables/table01_dual_cell_accuracy.csv").open(newline="", encoding="utf-8") as fh:
            rows = {(r["backbone"], r["condition"]): r for r in csv.DictReader(fh)}
        self.assertEqual(len(rows), 8)
        self.assertAlmostEqual(float(rows[("Qwen-7B", "F01_Full_WithShape")]["execution_accuracy"]), 0.7166666666666667)
        self.assertAlmostEqual(float(rows[("Granite-8B", "F01_Full_WithShape")]["execution_accuracy"]), 0.5555555555555556)
        self.assertAlmostEqual(float(rows[("Qwen-7B", "F11_Compact_WithShape")]["execution_accuracy"]), 0.6)
        self.assertAlmostEqual(float(rows[("Granite-8B", "F11_Compact_WithShape")]["execution_accuracy"]), 0.6)

    def test_replication_and_three_way_numbers(self):
        with (HERE / "tables/table04_shape_effect_replication.csv").open(newline="", encoding="utf-8") as fh:
            rep = {(r["backbone"], r["metric"]): r for r in csv.DictReader(fh)}
        self.assertEqual(len(rep), 4)
        self.assertEqual(rep[("Qwen-7B", "correct_int")]["direction_positive"], "True")
        self.assertEqual(rep[("Granite-8B", "correct_int")]["direction_positive"], "True")
        self.assertGreater(float(rep[("Qwen-7B", "correct_int")]["ci_low"]), 0)
        self.assertLess(float(rep[("Granite-8B", "correct_int")]["ci_low"]), 0)
        with (HERE / "tables/table03_backbone_effect_modifiers.csv").open(newline="", encoding="utf-8") as fh:
            mods = {(r["metric"], r["effect"]): r for r in csv.DictReader(fh)}
        three = mods[("correct_int", "backbone_x_interaction")]
        self.assertAlmostEqual(float(three["granite_minus_qwen"]), 0.18888888888888888)
        self.assertGreater(float(three["ci_low"]), 0)

    def test_cross_backbone_holm_and_f01_gap(self):
        with (HERE / "tables/table05_cross_backbone_cells.csv").open(newline="", encoding="utf-8") as fh:
            rows = {(r["condition"], r["metric"]): r for r in csv.DictReader(fh)}
        self.assertEqual(len(rows), 8)
        f01 = rows[("F01_Full_WithShape", "correct_int")]
        self.assertAlmostEqual(float(f01["granite_minus_qwen"]), -0.16111111111111112)
        self.assertLess(float(f01["ci_high"]), 0)
        self.assertEqual(f01["holm_reject_0_05"], "True")
        self.assertEqual(rows[("F11_Compact_WithShape", "correct_int")]["holm_reject_0_05"], "False")

    def test_figure_and_scope_contract(self):
        for idx in range(1, 6):
            matches = list((HERE / "figures").glob(f"fig{idx:02d}_*"))
            self.assertEqual({p.suffix for p in matches}, {".svg", ".pdf", ".png"})
            png = next(p for p in matches if p.suffix == ".png")
            with Image.open(png) as image:
                self.assertGreaterEqual(image.width, 2000)
                self.assertAlmostEqual(image.info["dpi"][0], 450, delta=1)
            self.assertIn("<text", next(p for p in matches if p.suffix == ".svg").read_text(encoding="utf-8"))
        captions = (HERE / "CAPTIONS.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(captions.count("two audited backbones, one GridDB"), 5)
        self.assertIn("not general model-family robustness", self.manifest["claim_boundary"])

    def test_manifest_outputs_and_page_preview(self):
        for rel, meta in self.manifest["outputs"].items():
            path = HERE / rel
            self.assertTrue(path.is_file())
            self.assertEqual(meta["sha256"], sha256(path))
        self.assertGreater((HERE / "qa/page_scale_preview.pdf").stat().st_size, 100_000)


if __name__ == "__main__":
    unittest.main(verbosity=2)
