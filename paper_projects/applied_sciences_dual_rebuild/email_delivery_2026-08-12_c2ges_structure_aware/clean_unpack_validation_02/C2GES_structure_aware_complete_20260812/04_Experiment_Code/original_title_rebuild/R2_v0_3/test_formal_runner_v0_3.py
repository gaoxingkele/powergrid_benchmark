from __future__ import annotations

import unittest

from run_test_v0_3 import holm_adjust, validate_config


class FormalRunnerV03Tests(unittest.TestCase):
    def test_holm_is_monotone_and_bounded(self) -> None:
        rows = [
            {"p_two_sided_bootstrap": 0.01, "budget": 5, "contrast": "a"},
            {"p_two_sided_bootstrap": 0.02, "budget": 5, "contrast": "b"},
            {"p_two_sided_bootstrap": 0.5, "budget": 10, "contrast": "c"},
        ]
        holm_adjust(rows)
        ordered = sorted(rows, key=lambda row: row["p_two_sided_bootstrap"])
        self.assertEqual([row["p_holm"] for row in ordered], [0.03, 0.04, 0.5])
        self.assertTrue(all(0 <= row["p_holm"] <= 1 for row in rows))

    def test_config_requires_strict_registered_primary_family(self) -> None:
        config = {
            "conditions": ["lead", "centroid", "textrank", "semantic_centroid", "role", "graph_no_cf_strict", "c2ges_full"],
            "selection_budgets": [5, 10],
            "c2ges_full_weights": {"relevance": 0.4, "role": 0.2, "graph": 0.15, "counterfactual": 0.15, "position": 0.1},
            "primary_contrasts": ["graph_no_cf_strict", "semantic_centroid", "textrank"],
            "semantic_model": {"local_files_only": True},
        }
        validate_config(config)
        config["primary_contrasts"] = ["lead"]
        with self.assertRaises(ValueError): validate_config(config)


if __name__ == "__main__":
    unittest.main()
