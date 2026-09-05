from __future__ import annotations

import math
import unittest

from experiment import CONDITIONS, contrast_summary, normalized_weights, word_count


class ProspectiveExperimentTests(unittest.TestCase):
    def test_condition_registry_complete(self) -> None:
        self.assertEqual(set(CONDITIONS), {"AB-0", "AB-1", "AB-2", "AB-3", "AB-4", "AB-5", "AB-6", "RP-00", "RP-10", "RP-01", "RP-11", "G-U", "G-T"})

    def test_positive_weights_renormalize(self) -> None:
        base = {"relevance": 0.4, "role": 0.2, "graph": 0.15, "path": 0.15, "position": 0.1}
        weights = normalized_weights(base, ("relevance", "role", "position"))
        self.assertTrue(math.isclose(sum(weights.values()), 1.0))
        self.assertEqual(weights["graph"], 0.0)
        self.assertEqual(weights["path"], 0.0)

    def test_word_count(self) -> None:
        self.assertEqual(word_count("A 110-word test isn't truncated."), 5)

    def test_exact_signflip_is_bounded(self) -> None:
        result = contrast_summary({"s1": 0.1, "s2": -0.02, "s3": 0.04}, samples=100, seed=7)
        self.assertGreaterEqual(result["exact_series_signflip_p"], 0.0)
        self.assertLessEqual(result["exact_series_signflip_p"], 1.0)


if __name__ == "__main__":
    unittest.main()
