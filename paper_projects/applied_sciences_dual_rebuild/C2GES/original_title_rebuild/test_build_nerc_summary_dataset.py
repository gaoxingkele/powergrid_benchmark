import tempfile
import unittest
from pathlib import Path

from build_nerc_summary_dataset import build, executive_summary


class NERCSummaryDatasetTests(unittest.TestCase):
    def test_build_has_hash_defined_dev_and_test_splits(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest = build(Path(directory))
        self.assertGreaterEqual(manifest["included"], 20)
        self.assertGreater(manifest["dev"], 0)
        self.assertGreater(manifest["test"], 0)
        self.assertTrue(manifest["dataset_sha256"])

    def test_executive_summary_stops_at_chapter_one(self) -> None:
        body = " ".join(["reliability evidence"] * 90)
        text = f"Executive Summary\n{body}\nChapter 1: Disturbance Analyses\nDO NOT INCLUDE"
        summary, status = executive_summary(text)
        self.assertEqual(status, "included")
        self.assertNotIn("DO NOT INCLUDE", summary)


if __name__ == "__main__":
    unittest.main()
