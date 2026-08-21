from __future__ import annotations

import json
import math
import sys
import tempfile
import unittest
from pathlib import Path


TESTS = Path(__file__).resolve().parent
ROOT = TESTS.parent
sys.path.insert(0, str(ROOT))

import aggregate_results as stats  # noqa: E402


class RegisteredStatisticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads((TESTS / "fixtures" / "synthetic_pairs.json").read_text(encoding="utf-8"))["rows"]

    def pairs(self, field: str) -> list[stats.PairedValue]:
        return [stats.PairedValue(row["question_id"], row["cluster"], row[field]) for row in self.fixture]

    def test_question_weighted_estimate_with_unequal_clusters(self) -> None:
        rows = [stats.PairedValue("a", "large", 1), stats.PairedValue("b", "large", 1), stats.PairedValue("c", "small", 0)]
        result = stats.cluster_bootstrap(rows, samples=500, seed=11)
        self.assertAlmostEqual(result["estimate"], 2 / 3)

    def test_bootstrap_is_deterministic_and_positive(self) -> None:
        rows = self.pairs("qwen_e1")
        first = stats.cluster_bootstrap(rows, samples=1_000, seed=22)
        second = stats.cluster_bootstrap(rows, samples=1_000, seed=22)
        self.assertEqual(first, second)
        self.assertEqual(first["estimate"], 1.0)
        self.assertGreater(first["ci_low"], 0)

    def test_cluster_sign_flip_is_deterministic(self) -> None:
        rows = self.pairs("qwen_e1")
        first = stats.cluster_sign_flip(rows, samples=10_000, seed=33)
        second = stats.cluster_sign_flip(rows, samples=10_000, seed=33)
        self.assertEqual(first, second)
        self.assertLess(first["p_value"], 0.01)

    def test_holm_known_family(self) -> None:
        adjusted = stats.holm_adjust([0.01, 0.04])
        self.assertEqual(adjusted, [0.02, 0.04])

    def test_claim_rules(self) -> None:
        positive = {"estimate": 0.2, "ci_low": 0.01, "ci_high": 0.4, "holm_adjusted_p": 0.02}
        harm = {"estimate": -0.2, "ci_low": -0.4, "ci_high": -0.01, "holm_adjusted_p": 0.02}
        null = {"estimate": 0.2, "ci_low": -0.01, "ci_high": 0.4, "holm_adjusted_p": 0.02}
        self.assertEqual(stats.claim_label(positive), "positive_component_efficacy")
        self.assertEqual(stats.claim_label(harm), "significant_harm")
        self.assertEqual(stats.claim_label(null), "no_detectable_improvement")

    def test_cross_backbone_modifier_orientation(self) -> None:
        rows = [stats.PairedValue(row["question_id"], row["cluster"], row["granite_e2"] - row["qwen_e2"]) for row in self.fixture]
        result = stats.cluster_bootstrap(rows, samples=1_000, seed=44)
        expected = sum(row["granite_e2"] - row["qwen_e2"] for row in self.fixture) / len(self.fixture)
        self.assertAlmostEqual(result["estimate"], expected)

    def test_latency_log_ratio_back_transform(self) -> None:
        rows = self.pairs("log_latency")
        result = stats.cluster_bootstrap(rows, samples=1_000, seed=55)
        self.assertAlmostEqual(math.exp(result["estimate"]), math.exp(sum(row["log_latency"] for row in self.fixture) / len(self.fixture)))

    def test_full_synthetic_pipeline_without_formal_outputs(self) -> None:
        freeze = json.loads((ROOT / "PROTOCOL_FREEZE.json").read_text(encoding="utf-8"))
        def write_jsonl(path: Path, rows: list[dict]) -> None:
            path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")

        with tempfile.TemporaryDirectory(prefix="ma_sqlgrid_synthetic_stats_") as temporary:
            runs = Path(temporary)
            for model in stats.MODELS:
                run_dir = runs / model
                run_dir.mkdir()
                order = stats.read_jsonl(ROOT / f"call_order_{model}.jsonl")
                predictions, selections, scored = [], [], []
                for item in order:
                    qid, condition = item["question_id"], item["condition"]
                    number = int(qid[1:])
                    first = (number % 3) != 0
                    if condition == stats.V1 and number % 5 == 0:
                        first = True
                    selected = first or (condition == stats.V1 and number % 7 == 0)
                    predictions.append({
                        "question_id": qid, "condition": condition, "status": "success", "retry_count": 0,
                        "latency_ms": 110 if condition == stats.V1 else 100,
                        "token_input": 120 if condition == stats.V1 else 100, "token_output": 30,
                        "token_total": 150 if condition == stats.V1 else 130,
                        "model_sha256": freeze["models"][model]["model_sha256"],
                        "served_model_id": freeze["models"][model]["served_model_id"],
                    })
                    selected_index = 1 if selected != first else 0
                    trace = [{"candidate_index": index, "safe": True, "exec_ok": True} for index in range(3)]
                    selections.append({"question_id": qid, "condition": condition, "candidate_count": 3,
                                       "selected_candidate_index": selected_index, "rank_trace": trace})
                    scored.append({"question_id": qid, "condition": condition, "candidate_count": 3,
                                   "first_correct": first, "validator_selected_correct": selected,
                                   "oracle_at_3_correct_diagnostic_only": selected})
                pred_path, selection_path, score_path = run_dir / "predictions.jsonl", run_dir / "candidate_selections.jsonl", run_dir / "scored_rows.jsonl"
                write_jsonl(pred_path, predictions); write_jsonl(selection_path, selections); write_jsonl(score_path, scored)
                selection_sha = stats.sha256_file(selection_path)
                (run_dir / "SELECTION_SEAL.json").write_text(json.dumps({"selection_ledger_sha256": selection_sha, "gold_loaded": False}) + "\n", encoding="utf-8")
                (run_dir / "SCORING_MANIFEST.json").write_text(json.dumps({"selection_ledger_sha256": selection_sha,
                    "scored_rows_sha256": stats.sha256_file(score_path)}) + "\n", encoding="utf-8")
                (run_dir / "RUN_MANIFEST.json").write_text(json.dumps({
                    "status": "completed_predictions_unscored", "freeze_sha256": stats.sha256_file(ROOT / "PROTOCOL_FREEZE.json"),
                    "model_sha256": freeze["models"][model]["model_sha256"], "prediction_ledger_sha256": stats.sha256_file(pred_path),
                    "gpu_before": {}, "gpu_after": {},
                }) + "\n", encoding="utf-8")
            original_bootstrap, original_randomization = stats.BOOTSTRAP_SAMPLES, stats.RANDOMIZATION_SAMPLES
            stats.BOOTSTRAP_SAMPLES, stats.RANDOMIZATION_SAMPLES = 500, 2_000
            try:
                result = stats.analyze(runs)
            finally:
                stats.BOOTSTRAP_SAMPLES, stats.RANDOMIZATION_SAMPLES = original_bootstrap, original_randomization
            self.assertEqual(len(result["primary_effects"]["E1"]), 2)
            self.assertEqual(len(result["primary_effects"]["E2"]), 2)
            self.assertEqual(len(result["primary_effects"]["cross_backbone"]), 2)
            self.assertEqual(len(result["descriptives"]), 2)
            self.assertEqual(len(result["efficiency"]), 2)
            self.assertTrue(all(not row["validity"]["formal_latency_eligible"] for row in result["efficiency"]))


if __name__ == "__main__":
    unittest.main()
