"""Structural/counting tests; these do not validate semantic judgments."""
import unittest
from pathlib import Path

from measure_reviewed_paragraphs import measure, normalize, percentile, words


class TestReviewedParagraphs(unittest.TestCase):
    def test_line_wrap_and_ligature(self):
        self.assertEqual(normalize("fore-\ncasting ﬁeld"), "forecasting field")

    def test_compound_word_policy(self):
        self.assertEqual(words("week-ahead 72 h"), ["week-ahead", "72", "h"])

    def test_percentile(self):
        self.assertEqual(percentile([10, 20], .1), 11)

    def test_real_map_accounting(self):
        root = Path(__file__).resolve().parents[1]
        data = measure(root / "deconstruction/v1/papers/p_71fe4f1acd7e01c5.paragraph_map.json")
        self.assertEqual(data["summary"]["prose_paragraphs"], 63)
        self.assertEqual(data["summary"]["list_items"], 3)
        self.assertEqual(len(data["paragraphs"]), 66)
        self.assertEqual(data["summary"]["body_words"], 6892)
        self.assertEqual(sum(p["words"] for p in data["paragraphs"]), data["summary"]["body_words"])
        self.assertEqual(sum(s["words_exclusive"] for s in data["sections"].values()), data["summary"]["body_words"])
        self.assertFalse(data["human_calibrated"])
        self.assertTrue(all("text" not in p for p in data["paragraphs"]))

    def test_transformer_map_accounting(self):
        root = Path(__file__).resolve().parents[1]
        data = measure(root / "deconstruction/v1/papers/p_654ca5ab287c1e14.paragraph_map.json")
        self.assertEqual(data["summary"]["prose_paragraphs"], 48)
        self.assertEqual(data["summary"]["body_words"], 7240)
        self.assertEqual(sum(s["words_exclusive"] for s in data["sections"].values()), 7240)


if __name__ == "__main__":
    unittest.main()
