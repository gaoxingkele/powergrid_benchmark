#!/usr/bin/env python3
"""Integrity and vector-format checks for the two framework figures."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class VectorFigureTests(unittest.TestCase):
    def test_artifacts_and_manifest_hashes(self) -> None:
        for paper in ("C2GES", "MA_SQLGrid"):
            with self.subTest(paper=paper):
                directory = ROOT / paper
                manifest = json.loads((directory / "artifact_manifest.json").read_text(encoding="utf-8"))
                self.assertEqual(manifest["config"]["sha256"], digest(directory / "framework_config.json"))
                self.assertEqual(len(manifest["outputs"]), 3)
                for item in manifest["outputs"]:
                    artifact = directory / item["path"]
                    self.assertTrue(artifact.is_file() and artifact.stat().st_size > 1000)
                    self.assertEqual(item["sha256"], digest(artifact))

    def test_live_svg_and_vector_pdf(self) -> None:
        stems = {
            "C2GES": "c2ges_algorithm_framework_vector",
            "MA_SQLGrid": "ma_sqlgrid_algorithm_framework_vector",
        }
        for paper, stem in stems.items():
            with self.subTest(paper=paper):
                directory = ROOT / paper
                svg = (directory / f"{stem}.svg").read_text(encoding="utf-8")
                self.assertIn("<text", svg)
                self.assertNotIn("<image", svg)
                self.assertTrue((directory / f"{stem}.pdf").read_bytes().startswith(b"%PDF"))
                with Image.open(directory / f"{stem}.png") as image:
                    self.assertGreaterEqual(min(image.info.get("dpi", (0, 0))), 300)
                    self.assertGreaterEqual(min(image.size), 1800)

    def test_required_claim_boundaries(self) -> None:
        c2 = (ROOT / "C2GES" / "c2ges_algorithm_framework_vector.svg").read_text(encoding="utf-8")
        ma = (ROOT / "MA_SQLGrid" / "ma_sqlgrid_algorithm_framework_vector.svg").read_text(encoding="utf-8")
        for phrase in ("0.40 Q", "0.15 C", "No-CF", "structural text proxy"):
            self.assertIn(phrase, c2)
        for phrase in ("External SQL", "Hard eligibility gates", "SELECT or ABSTAIN", "Gold / reference"):
            self.assertIn(phrase, ma)
        for forbidden in ("GNN", "physical causal identification"):
            self.assertNotIn(forbidden, c2)
        for forbidden in ("autonomous agents", "gold SQL ranking"):
            self.assertNotIn(forbidden, ma.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
