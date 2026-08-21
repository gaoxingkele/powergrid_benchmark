"""Validation tests for the frozen W6 C2GES canonical release."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import unittest
from pathlib import Path

from PIL import Image
from pypdf import PdfReader

import build_c2_canonical_artifacts as canonical


PROJECT = Path(__file__).resolve().parents[2]
OUTPUT = PROJECT / "workspace/w6_c2_canonical_v2"


class CanonicalHelperTests(unittest.TestCase):
    def test_pareto_prefers_lower_cost_and_higher_accuracy(self):
        self.assertEqual(canonical.pareto_indices([1, 2, 3], [0.5, 0.6, 0.4]), [0, 1])

    def test_visual_styles_have_redundant_non_color_encoding(self):
        styles = [canonical.STYLES[key] for key in ("oracle-label", "predicted-label", "label-blind", "bm25")]
        self.assertEqual(len({item["marker"] for item in styles}), 4)
        self.assertEqual(len({item["linestyle"] for item in styles}), 4)


class CanonicalReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (OUTPUT / "canonical_manifest.json").is_file():
            raise AssertionError(f"missing canonical release: {OUTPUT}")
        cls.manifest = json.loads((OUTPUT / "canonical_manifest.json").read_text(encoding="utf-8"))

    def test_manifest_and_source_run_count(self):
        self.assertEqual(self.manifest["status"], "canonical")
        self.assertTrue(self.manifest["validation"]["passed"])
        self.assertEqual(len(self.manifest["inputs"]["prediction_runs"]), 15)
        self.assertEqual(self.manifest["validation"]["canonical_prediction_rows"], 180000)

    def test_every_manifest_output_hash_matches(self):
        for relative, expected in self.manifest["outputs"].items():
            path = OUTPUT / relative
            self.assertTrue(path.is_file(), relative)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected["sha256"], relative)

    def test_all_figure_formats_and_rendering_contract(self):
        for index in range(1, 6):
            stem = next((OUTPUT / "figures").glob(f"fig{index:02d}_*.png")).stem
            png, svg, pdf = (OUTPUT / "figures" / f"{stem}.{suffix}" for suffix in ("png", "svg", "pdf"))
            with Image.open(png) as image:
                dpi = image.info.get("dpi")
                self.assertIsNotNone(dpi)
                self.assertAlmostEqual(dpi[0], 450, delta=1)
                self.assertAlmostEqual(dpi[1], 450, delta=1)
            self.assertIn("<text", svg.read_text(encoding="utf-8"))
            self.assertEqual(len(PdfReader(str(pdf)).pages), 1)

    def test_caption_claim_boundaries(self):
        captions = (OUTPUT / "FIGURE_CAPTIONS.md").read_text(encoding="utf-8")
        self.assertEqual(captions.count("NO-GO"), 5)
        self.assertGreaterEqual(captions.lower().count("conditional"), 4)

    def test_canonical_prediction_row_count(self):
        path = OUTPUT / "data/canonical_full_and_bm25_predictions.csv.gz"
        with gzip.open(path, "rt", encoding="utf-8", newline="") as handle:
            self.assertEqual(sum(1 for _ in csv.DictReader(handle)), 180000)

    def test_failure_table_has_fifteen_successes(self):
        with (OUTPUT / "tables/table_failure_audit.csv").open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 15)
        self.assertEqual({row["status"] for row in rows}, {"success"})


if __name__ == "__main__":
    unittest.main()
