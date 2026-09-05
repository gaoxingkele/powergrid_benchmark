import unittest

import numpy as np

from pacsum_minilm import TUNING_GRID, pacsum_scores, select_word_budget


class PacSumMiniLMTests(unittest.TestCase):
    def test_grid_has_nine_unique_configs(self):
        self.assertEqual(len(TUNING_GRID), 9)
        self.assertEqual(len({tuple(sorted(row.items())) for row in TUNING_GRID}), 9)

    def test_single_unit_has_zero_score(self):
        np.testing.assert_array_equal(
            pacsum_scores(np.array([[1.0, 0.0]]), lambda_preceding=-1, lambda_following=1, beta=0.3),
            np.array([0.0]),
        )

    def test_position_direction_changes_scores(self):
        embeddings = np.array([[1.0, 0.0], [0.9, 0.1], [0.0, 1.0]])
        forward = pacsum_scores(embeddings, lambda_preceding=-1, lambda_following=1, beta=0.0)
        reverse = pacsum_scores(embeddings, lambda_preceding=1, lambda_following=-1, beta=0.0)
        np.testing.assert_allclose(forward, np.array([0.9, -0.8, -0.1]))
        np.testing.assert_allclose(reverse, -forward)

    def test_complete_ranking_budget_skips_oversized_unit(self):
        units = [
            {"sid": "u1", "source_order": 1, "text": "one two three four five", "word_count": 5},
            {"sid": "u2", "source_order": 2, "text": "one two three", "word_count": 3},
            {"sid": "u3", "source_order": 3, "text": "one two", "word_count": 2},
        ]
        selected = select_word_budget(units, [3.0, 2.0, 1.0], 4)
        self.assertEqual([row["sid"] for row in selected], ["u2"])


if __name__ == "__main__":
    unittest.main()
