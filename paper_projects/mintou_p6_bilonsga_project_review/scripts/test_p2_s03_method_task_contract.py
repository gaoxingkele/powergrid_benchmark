"""Tests for the prospective P2 method/task implementation contract."""

import json
from pathlib import Path
import unittest

from scripts.p2_s03_method_task_contract import (
    ContractError, CostModel, EvaluationLedger, build_rts_transmission_tasks,
    build_simbench_feeder_tasks, normalized_violation, repair_to_budget,
    run_arm_local_search, run_local_pass, validate_independent_families,
)


DIGEST_A = "a" * 64
DIGEST_B = "b" * 64


def families():
    rts = build_rts_transmission_tasks(
        [{"branch_id": "z", "capacity_increment_mva": 2}, {"branch_id": "a", "capacity_increment_mva": 2}],
        "rts.csv", DIGEST_A, CostModel("rts-f1", "test fixture only", 1, 2, "capacity_increment_mva"),
    )
    sim = build_simbench_feeder_tasks(
        [{"line_id": "l1", "line_length_km": 3, "capacity_increment_mva": 1}],
        "simbench.csv", DIGEST_B, CostModel("sb-f1", "test fixture only", 2, 1, "line_length_km"),
    )
    return rts, sim


class TaskTests(unittest.TestCase):
    def test_families_are_independent_and_costs_trace(self):
        rts, sim = families()
        validate_independent_families(rts, sim)
        self.assertEqual([a.action_id for a in rts], ["rts-branch::a", "rts-branch::z"])
        self.assertEqual(rts[0].cost_units, 5)
        self.assertEqual(sim[0].cost_units, 5)
        with self.assertRaises(ContractError):
            validate_independent_families(rts, [sim[0].__class__(**{**sim[0].__dict__, "source_sha256": DIGEST_A})])

    def test_violation_and_repair_tie_rule(self):
        actions, _ = families()
        self.assertEqual(normalized_violation((1, 1), actions, 5), 1.0)
        repaired, removed = repair_to_budget((1, 1), actions, [1, 1], 5)
        self.assertEqual(removed, ("rts-branch::a",))
        self.assertEqual(repaired, (0, 1))


class MoveAndAccountingTests(unittest.TestCase):
    def test_duplicate_cache_and_unique_counter(self):
        actions, _ = families()
        ledger = EvaluationLedger(unique_limit=3, request_limit=4)
        scorer = lambda x: (float(-sum(x)), float(sum(x)))
        first = ledger.evaluate((1, 0), scorer, actions, 10)
        second = ledger.evaluate((1, 0), scorer, actions, 10)
        self.assertEqual(first, second)
        self.assertEqual((ledger.requests, ledger.unique_evaluations, ledger.cache_hits), (2, 1, 1))

    def test_strict_tie_rejects_and_terminates(self):
        actions, _ = families()
        ledger = EvaluationLedger(unique_limit=10, request_limit=10)
        final, accepted, reason = run_local_pass(
            (1, 0), "backward", 4, actions, [1, 1], 10,
            lambda x: (0.0,), (0.0,), (1.0,), 0.0, ledger,
        )
        self.assertEqual(final, (1, 0))
        self.assertEqual(accepted, 0)
        self.assertEqual(reason, "first_non_improvement")

    def test_forward_then_atomic_semantics(self):
        actions, _ = families()
        scorer = lambda x: (-float(sum(x)),)
        ledger = EvaluationLedger(unique_limit=10, request_limit=10)
        final, accepted, reason = run_local_pass(
            (1, 0), "forward", 2, actions, [1, 2], 10,
            scorer, (-2.0,), (0.0,), 10.0, ledger,
        )
        self.assertEqual((final, accepted, reason), ((1, 1), 1, "neighborhood_exhausted"))

    def test_atomic_substitution_scores_only_combined_state(self):
        actions, _ = families()
        seen = []
        def scorer(x):
            seen.append(x)
            return (0.0 if x == (1, 0) else -1.0,)
        ledger = EvaluationLedger(unique_limit=10, request_limit=10)
        final, accepted, _ = run_local_pass(
            (1, 0), "atomic_substitution", 1, actions, [1, 2], 5,
            scorer, (-1.0,), (0.0,), 10.0, ledger,
        )
        self.assertEqual(final, (0, 1))
        self.assertEqual(accepted, 1)
        self.assertEqual(seen, [(1, 0), (0, 1)])

    def test_principal_bidirectional_arm_reports_directions_separately(self):
        actions, _ = families()
        ledger = EvaluationLedger(unique_limit=10, request_limit=10)
        result = run_arm_local_search(
            (1, 0), "bidirectional", 1, 1, actions, [1, 2], 10,
            lambda x: (-float(sum(x)), float(sum(x))),
            (-2.0, 0.0), (0.0, 2.0), 0.0, ledger,
        )
        self.assertEqual(result.accepted_forward, 0)
        self.assertEqual(result.accepted_backward, 0)
        self.assertEqual(len(result.termination_reasons), 2)


class ArtifactTests(unittest.TestCase):
    def test_machine_contract_is_no_results_and_formal_run_blocked(self):
        root = Path(__file__).resolve().parents[1]
        contract = json.loads((root / "experiments/p6_s4_applsci_grid_investment_v1/method_task_contract.json").read_text(encoding="utf-8"))
        self.assertEqual(contract["task_families"][0]["source"], "RTS-GMLC")
        self.assertEqual(contract["task_families"][1]["source"], "SimBench")
        self.assertFalse(contract["formal_run_allowed"])
        self.assertEqual(contract["results"], [])


if __name__ == "__main__":
    unittest.main()
