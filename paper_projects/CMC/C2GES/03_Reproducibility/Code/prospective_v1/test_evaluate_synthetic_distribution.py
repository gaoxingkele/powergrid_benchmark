from __future__ import annotations

import random
import unittest

from evaluate_synthetic_distribution import evaluate, ks_distance, normalized_w1
from generate_deepseek_synthetic import CORE_ROLES, expand_report, validate_core


class SyntheticEvaluationTests(unittest.TestCase):
    def test_distances_are_zero_for_identical_samples(self) -> None:
        self.assertEqual(normalized_w1([1, 2, 3], [1, 2, 3]), 0)
        self.assertEqual(ks_distance([1, 2, 3], [1, 2, 3]), 0)

    def test_evaluation_has_claim_boundary(self) -> None:
        units = [{"text": f"Synthetic station records {role} evidence number {i} under controlled fictional operating conditions today.",
                  "role": role, "causal_predecessors": []} for role in CORE_ROLES for i in range(4)]
        core = validate_core({"reports": [{"core_units": units}, {"core_units": units}]})[0]
        profile = {"page_count": 10, "candidate_count": 60, "reference_words": 140,
                   "units_over_256_tokens": 0, "body": 40, "heading": 5, "list_item": 7,
                   "table_unit": 5, "caption": 2, "footnote": 1}
        rows = [expand_report(core, profile, f"d{i}", "s1", "explicit", "fictional", random.Random(i)) for i in range(2)]
        result = evaluate(rows, [profile, profile])
        self.assertFalse(result["confirmatory_claims_allowed"])
        self.assertIn("gate_ledger", result)


if __name__ == "__main__":
    unittest.main()
