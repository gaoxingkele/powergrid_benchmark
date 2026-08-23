from __future__ import annotations

import unittest

from run_test_v0_3_1 import holm_adjust, validate_config


class FormalRunnerV031Tests(unittest.TestCase):
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
            "conditions": ["lead", "centroid", "textrank", "semantic_mmr", "role", "graph_no_cf_strict", "c2ges_full"],
            "selection_budgets": [5, 10],
            "c2ges_full_weights": {"relevance": 0.4, "role": 0.2, "graph": 0.15, "counterfactual": 0.15, "position": 0.1},
            "primary_contrasts": ["graph_no_cf_strict", "semantic_mmr", "textrank"],
            "semantic_model": {"local_files_only": True},
            "semantic_mmr": {"lambda": 0.5, "relevance_weight": 0.5, "redundancy_penalty": 0.5},
            "path_min_edges": 2,
            "path_max_edges": 4,
            "path_max_paths": 250000,
            "path_max_expansions": 2000000,
        }
        validate_config(config)
        config["primary_contrasts"] = ["lead"]
        with self.assertRaises(ValueError): validate_config(config)


if __name__ == "__main__":
    unittest.main()
