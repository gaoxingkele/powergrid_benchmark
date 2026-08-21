"""Integrity and layout-smoke tests for both protocol-only framework figure sets."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ("MA_SQLGrid", "C2GES")
FORMATS = ("svg", "pdf", "png")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def framework_dir(paper: str) -> Path:
    return ROOT / paper / "figures" / "frameworks"


class FrameworkArtifactTests(unittest.TestCase):
    def test_manifest_and_all_artifact_hashes(self) -> None:
        for paper in PAPERS:
            with self.subTest(paper=paper):
                directory = framework_dir(paper)
                config_path = directory / "framework_config.json"
                manifest = json.loads((directory / "artifact_manifest.json").read_text(encoding="utf-8"))
                config = json.loads(config_path.read_text(encoding="utf-8"))
                self.assertEqual(config["data_status"], "protocol_only_no_unfrozen_results")
                self.assertEqual(manifest["data_status"], config["data_status"])
                self.assertEqual(manifest["config"]["sha256"], digest(config_path))
                self.assertEqual(manifest["captions"]["sha256"], digest(directory / "captions.md"))
                self.assertEqual(len(config["figures"]), 3)
                self.assertEqual(len(manifest["outputs"]), 3 * len(FORMATS))
                for item in manifest["outputs"]:
                    artifact = directory / item["path"]
                    self.assertTrue(artifact.is_file() and artifact.stat().st_size > 1000)
                    self.assertEqual(item["sha256"], digest(artifact))

    def test_vector_editability_and_png_resolution(self) -> None:
        for paper in PAPERS:
            directory = framework_dir(paper)
            config = json.loads((directory / "framework_config.json").read_text(encoding="utf-8"))
            for figure in config["figures"]:
                with self.subTest(paper=paper, figure=figure["id"]):
                    stem = figure["id"]
                    svg = (directory / f"{stem}.svg").read_text(encoding="utf-8")
                    self.assertIn("<svg", svg)
                    self.assertIn("<text", svg)
                    self.assertNotIn("<image", svg)
                    self.assertTrue((directory / f"{stem}.pdf").read_bytes().startswith(b"%PDF"))
                    with Image.open(directory / f"{stem}.png") as image:
                        dpi = image.info.get("dpi", (0, 0))
                        self.assertGreaterEqual(min(dpi), 300)
                        self.assertGreaterEqual(min(image.size), 2500)
                        rgb = image.convert("RGB")
                        width, height = rgb.size
                        border = 8
                        pixels = list(rgb.crop((0, 0, width, border)).get_flattened_data())
                        pixels += list(rgb.crop((0, height - border, width, height)).get_flattened_data())
                        pixels += list(rgb.crop((0, border, border, height - border)).get_flattened_data())
                        pixels += list(rgb.crop((width - border, border, width, height - border)).get_flattened_data())
                        dark_fraction = sum(any(channel < 245 for channel in pixel) for pixel in pixels) / len(pixels)
                        self.assertLess(dark_fraction, 0.001, f"content reaches PNG boundary: {stem}")

    def test_protocol_only_style_and_geometric_bounds(self) -> None:
        for paper in PAPERS:
            config = json.loads((framework_dir(paper) / "framework_config.json").read_text(encoding="utf-8"))
            serialized = json.dumps(config).lower()
            for forbidden in ('"observed_value"', '"result_value"', '"estimate"', '"score"'):
                self.assertNotIn(forbidden, serialized)
            self.assertGreaterEqual(config["style"]["png_dpi"], 300)
            self.assertEqual(config["style"]["palette"], "Okabe-Ito")
            for figure in config["figures"]:
                ids = {node["id"] for node in figure["nodes"]}
                for node in figure["nodes"]:
                    pad = 0.018 if node.get("shape", "round") == "round" else 0.0
                    self.assertTrue(node["hatch"])
                    self.assertTrue(node["linestyle"])
                    self.assertGreaterEqual(node["x"] - node["w"] / 2 - pad, 0)
                    self.assertLessEqual(node["x"] + node["w"] / 2 + pad, 1)
                    self.assertGreaterEqual(node["y"] - node["h"] / 2 - pad, 0)
                    self.assertLessEqual(node["y"] + node["h"] / 2 + pad, 1)
                for edge in figure["edges"]:
                    self.assertIn(edge["source"], ids)
                    self.assertIn(edge["target"], ids)

    def test_c2_left_split_nodes_are_disjoint(self) -> None:
        config = json.loads((framework_dir("C2GES") / "framework_config.json").read_text(encoding="utf-8"))
        figure = next(item for item in config["figures"] if item["id"] == "c2_f02_oof_document_split")
        nodes = {item["id"]: item for item in figure["nodes"]}

        def right(node: dict) -> float:
            return node["x"] + node["w"] / 2 + (0.018 if node.get("shape", "round") == "round" else 0)

        def left(node: dict) -> float:
            return node["x"] - node["w"] / 2 - (0.018 if node.get("shape", "round") == "round" else 0)

        self.assertLess(right(nodes["docs"]), left(nodes["split"]))
        self.assertLess(right(nodes["split"]), left(nodes["dev"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
