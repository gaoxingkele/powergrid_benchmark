import json
import unittest
from pathlib import Path

import numpy as np
from rouge_score import rouge_scorer

from run_formal_experiment_v0_2 import CONDITIONS, aggregate, evaluate_document, validate_config
from test_formal_runner import fixture_row


HERE = Path(__file__).resolve().parent


class FakeEncoder:
    def encode(self, texts, **kwargs):
        return np.asarray([[len(text), text.lower().count("relay") + 1.0] for text in texts], dtype=float)


class FormalRunnerV02Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = json.loads((HERE / "formal_config_v0.2.json").read_text(encoding="utf-8"))

    def test_strict_no_cf_is_proportional_full_without_cf(self) -> None:
        validate_config(self.config)
        full = self.config["c2ges_full_weights"]
        strict = self.config["graph_no_cf_strict_weights"]
        retained = 1.0 - full["counterfactual"]
        for key in ("relevance", "role", "graph", "position"):
            self.assertAlmostEqual(strict[key], full[key] / retained, places=12)
        self.assertEqual(strict["counterfactual"], 0.0)
        self.assertEqual(strict["redundancy_penalty"], full["redundancy_penalty"])

    def test_budgets_and_conditions_are_complete(self) -> None:
        scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
        rows = evaluate_document(fixture_row(), self.config, scorer, FakeEncoder())
        self.assertEqual(len(rows), 14)
        self.assertEqual({row["budget"] for row in rows}, {5, 10})
        for budget in (5, 10):
            subset = [row for row in rows if row["budget"] == budget]
            self.assertEqual(tuple(row["condition"] for row in subset), CONDITIONS)
            self.assertTrue(all(len(row["selected_sentence_ids"]) == min(budget, 6) for row in subset))
        summary = aggregate(rows)
        self.assertEqual(set(summary), {"5", "10"})
        self.assertEqual(set(summary["5"]), set(CONDITIONS))

    def test_nonproportional_ablation_fails_closed(self) -> None:
        altered = json.loads(json.dumps(self.config))
        altered["graph_no_cf_strict_weights"]["position"] += 0.01
        with self.assertRaisesRegex(ValueError, "not proportional"):
            validate_config(altered)


if __name__ == "__main__":
    unittest.main()
