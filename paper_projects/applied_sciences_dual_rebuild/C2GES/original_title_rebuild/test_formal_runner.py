import json
import tempfile
import unittest
from pathlib import Path

from rouge_score import rouge_scorer

from run_formal_experiment import (
    EXPECTED_CONDITIONS,
    aggregate,
    evaluate_document,
    paired_bootstrap,
    validate_config,
)


HERE = Path(__file__).resolve().parent


def fixture_row() -> dict:
    sentences = [
        {"sid": "s0", "text": "A frozen protection setting caused the relay to misoperate."},
        {"sid": "s1", "text": "The relay fault initiated the transmission outage."},
        {"sid": "s2", "text": "The line trip propagated a voltage decline."},
        {"sid": "s3", "text": "Five hundred MW of load was lost and customers were affected."},
        {"sid": "s4", "text": "Operators recommend corrective settings to prevent recurrence."},
        {"sid": "s5", "text": "The report describes regional weather."},
    ]
    silver = {
        "root_cause": [{"sid": "s0"}], "trigger_event": [{"sid": "s1"}],
        "propagation_or_response": [{"sid": "s2"}], "impact": [{"sid": "s3"}],
        "mitigation": [{"sid": "s4"}],
    }
    return {
        "doc_id": "fixture", "split": "test", "candidate_sentences": sentences,
        "reference_summary": "A protection setting caused an outage, load loss, and corrective action.",
        "reference_provenance": "fixture_reference",
        "silver_role_evidence": silver,
        "silver_label_provenance": "machine_fixture_not_human_gold",
    }


class FormalRunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = json.loads((HERE / "formal_config_v0.1.json").read_text(encoding="utf-8"))

    def test_six_conditions_share_one_document_and_budget(self) -> None:
        scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
        rows = evaluate_document(fixture_row(), self.config, scorer)
        self.assertEqual(tuple(row["condition"] for row in rows), EXPECTED_CONDITIONS)
        self.assertTrue(all(row["doc_id"] == "fixture" for row in rows))
        self.assertTrue(all(len(row["selected_sentence_ids"]) == 5 for row in rows))
        self.assertTrue(all(row["silver_label_provenance"] == "machine_fixture_not_human_gold" for row in rows))

    def test_aggregate_and_bootstrap_are_deterministic(self) -> None:
        scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
        rows = evaluate_document(fixture_row(), self.config, scorer)
        summary = aggregate(rows)
        self.assertEqual(set(summary), set(EXPECTED_CONDITIONS))
        first = paired_bootstrap(rows, "lead", "rougeL_f1", samples=100, seed=7)
        second = paired_bootstrap(rows, "lead", "rougeL_f1", samples=100, seed=7)
        self.assertEqual(first, second)
        self.assertEqual(first["n_reports"], 1)

    def test_invalid_condition_order_fails_closed(self) -> None:
        altered = dict(self.config)
        altered["conditions"] = list(reversed(altered["conditions"]))
        with self.assertRaisesRegex(ValueError, "exactly"):
            validate_config(altered)


if __name__ == "__main__":
    unittest.main()
