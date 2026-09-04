"""Unit tests for the P3 Stage-3 method/action implementation contract."""

from __future__ import annotations

import unittest
import json
from pathlib import Path

from scripts.p3_s03_method_contract import (
    ACValidationResult,
    ActionKind,
    AdaptationConfig,
    ContractError,
    DecisionVariable,
    EvaluationAccount,
    IndividualControls,
    SplitAdaptationController,
    bind_network_action,
    decode_genome,
    inherit_selected_controls,
    repair_to_budget,
    validate_complete_registry,
)


def variable(variable_id: str, kind: ActionKind, target_type: str, cost: float) -> DecisionVariable:
    return DecisionVariable(
        variable_id=variable_id,
        kind=kind,
        source_subnet="legacy-subnet",
        target_network="registered-public-network",
        target_element_type=target_type,
        target_element_id=f"target-{variable_id}",
        cost_units=cost,
        capacity_increment=1.0,
        capacity_unit="registered-unit",
        provenance="test fixture; not experiment evidence",
    )


class AdaptationTests(unittest.TestCase):
    def test_all_four_arms_are_distinct(self) -> None:
        arms = {
            AdaptationConfig(parameter_adaptive=p, strategy_adaptive=s).arm
            for p in (False, True)
            for s in (False, True)
        }
        self.assertEqual(len(arms), 4)

    def test_legacy_switch_maps_to_both_gates(self) -> None:
        enabled = AdaptationConfig.from_legacy(True)
        disabled = AdaptationConfig.from_legacy(False)
        self.assertEqual(enabled.arm, "adaptive_parameter__adaptive_strategy")
        self.assertEqual(disabled.arm, "fixed_parameter__fixed_strategy")
        self.assertTrue(enabled.to_legacy_switch())
        self.assertFalse(disabled.to_legacy_switch())
        with self.assertRaises(ContractError):
            AdaptationConfig(True, False).to_legacy_switch()

    def test_independent_random_streams(self) -> None:
        # Toggling strategy adaptation cannot consume or alter parameter draws.
        a = SplitAdaptationController(AdaptationConfig(True, True, resample_probability=1.0), 17)
        b = SplitAdaptationController(AdaptationConfig(True, False, resample_probability=1.0), 17)
        parent = IndividualControls()
        for _ in range(10):
            a.choose_strategy()
        self.assertEqual(a.propose_controls(parent), b.propose_controls(parent))
        # Parameter proposals likewise cannot consume or alter strategy draws.
        c = SplitAdaptationController(AdaptationConfig(True, True, resample_probability=1.0), 23)
        d = SplitAdaptationController(AdaptationConfig(False, True, resample_probability=1.0), 23)
        for _ in range(10):
            c.propose_controls(parent)
        self.assertEqual(c.choose_strategy(), d.choose_strategy())

    def test_deterministic_replay(self) -> None:
        cfg = AdaptationConfig(True, True, resample_probability=0.5)
        def trace() -> list[tuple[IndividualControls, str]]:
            controller = SplitAdaptationController(cfg, 99)
            parent = IndividualControls()
            return [(controller.propose_controls(parent), controller.choose_strategy()) for _ in range(20)]
        self.assertEqual(trace(), trace())

    def test_controls_follow_survivors(self) -> None:
        parents = [IndividualControls(0.2, 0.3), IndividualControls(0.4, 0.5)]
        trials = [IndividualControls(0.6, 0.7), IndividualControls(0.8, 0.9)]
        self.assertEqual(inherit_selected_controls(parents, trials, [2, 1]), [trials[0], parents[1]])


class ActionAndEvaluationTests(unittest.TestCase):
    def test_action_types_have_explicit_effects(self) -> None:
        cases = [
            variable("r", ActionKind.REINFORCEMENT, "line", 10),
            variable("s", ActionKind.STORAGE, "bus", 8),
            variable("d", ActionKind.DER, "bus", 6),
            variable("a", ActionKind.AUTOMATION, "switch", 4),
        ]
        for item in cases:
            action = bind_network_action(item)
            self.assertTrue(action.electrical_effect)
            self.assertTrue(action.proxy_effect)

    def test_registry_is_total(self) -> None:
        item = variable("r", ActionKind.REINFORCEMENT, "line", 10)
        self.assertEqual(len(validate_complete_registry(["r"], {"r": item})), 1)
        with self.assertRaises(ContractError):
            validate_complete_registry(["r", "missing"], {"r": item})

    def test_decode_and_repair_are_deterministic(self) -> None:
        variables = [
            variable("b", ActionKind.DER, "bus", 6),
            variable("a", ActionKind.STORAGE, "bus", 6),
        ]
        phenotype = decode_genome([0.5, 0.9])
        self.assertEqual(phenotype, [1, 1])
        self.assertEqual(repair_to_budget(phenotype, variables, [1.0, 1.0], 6), [1, 0])

    def test_ac_limits_and_failure_accounting(self) -> None:
        account = EvaluationAccount()
        account.charge_candidates(2)
        account.charge_objective_rows(4)
        account.charge_power_flow(False)
        self.assertEqual((account.generated_candidates, account.objective_rows, account.power_flow_failures), (2, 4, 1))
        self.assertTrue(ACValidationResult(True, 0.95, 1.05, 100.0).feasible())
        self.assertFalse(ACValidationResult(False, None, None, None).feasible())
        self.assertFalse(ACValidationResult(True, 0.949, 1.05, 100.0).feasible())


class ContractArtifactTests(unittest.TestCase):
    def test_machine_contract_matches_code_and_remains_no_go(self) -> None:
        root = Path(__file__).resolve().parents[1]
        path = root / "experiments/p3_s4_energies_samode_ac_planning_v1/method_implementation_contract.json"
        contract = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(contract["action_registry"]["status"], "NO_GO")
        self.assertFalse(contract["formal_run_allowed"])
        self.assertEqual(
            contract["adaptation"]["arms"],
            [
                "fixed_parameter__fixed_strategy",
                "adaptive_parameter__fixed_strategy",
                "fixed_parameter__adaptive_strategy",
                "adaptive_parameter__adaptive_strategy",
            ],
        )


if __name__ == "__main__":
    unittest.main()
