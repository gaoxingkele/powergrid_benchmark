"""P3 Stage-3 action and adaptation implementation contract.

This module is deliberately independent of the immutable legacy experiment
archive.  It provides the code-level contract for the next experiment:

* parameter adaptation and strategy adaptation are separate gates;
* ``legacy_coupled`` maps the historical switch to both gates;
* parameter controls are heritable and follow selected individuals;
* parameter and strategy draws use independent, reproducible random streams;
* binary decoding, deterministic budget repair, action binding, evaluation
  accounting, and AC post-validation have explicit validation rules.

It does not manufacture the missing mapping from legacy ``subnet::kind``
variables to concrete SimBench buses and branches.  A formal action-aligned run
must supply and validate those bindings before optimization.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import math
import random
from typing import Iterable, Mapping, Sequence


class ContractError(ValueError):
    """Raised when a preregistered implementation invariant is violated."""


class ActionKind(str, Enum):
    REINFORCEMENT = "reinforcement"
    STORAGE = "storage"
    DER = "der"
    AUTOMATION = "automation"


@dataclass(frozen=True)
class AdaptationConfig:
    """Independent mechanism gates with an explicit legacy compatibility mode."""

    parameter_adaptive: bool = True
    strategy_adaptive: bool = True
    legacy_coupled: bool = False
    f_fixed: float = 0.5
    cr_fixed: float = 0.9
    resample_probability: float = 0.1

    @classmethod
    def from_legacy(cls, strategy_adaptive: bool) -> "AdaptationConfig":
        """Reproduce the historical one-switch configuration exactly in intent."""

        return cls(
            parameter_adaptive=strategy_adaptive,
            strategy_adaptive=strategy_adaptive,
            legacy_coupled=True,
        )

    def validate(self) -> None:
        if self.legacy_coupled and self.parameter_adaptive != self.strategy_adaptive:
            raise ContractError("legacy_coupled requires equal adaptation gates")
        if not 0.0 <= self.resample_probability <= 1.0:
            raise ContractError("resample_probability must be in [0, 1]")
        if not 0.0 < self.f_fixed <= 2.0 or not 0.0 <= self.cr_fixed <= 1.0:
            raise ContractError("invalid fixed F/CR")

    def to_legacy_switch(self) -> bool:
        """Return the historical switch value for a compatibility configuration."""

        self.validate()
        if not self.legacy_coupled:
            raise ContractError("an independent-arm configuration has no single legacy switch")
        return self.parameter_adaptive

    @property
    def arm(self) -> str:
        return {
            (False, False): "fixed_parameter__fixed_strategy",
            (True, False): "adaptive_parameter__fixed_strategy",
            (False, True): "fixed_parameter__adaptive_strategy",
            (True, True): "adaptive_parameter__adaptive_strategy",
        }[(self.parameter_adaptive, self.strategy_adaptive)]


@dataclass(frozen=True)
class IndividualControls:
    """Heritable jDE controls attached to a genome, never to an array slot."""

    f: float = 0.5
    cr: float = 0.9


def _labelled_seed(master_seed: int, label: str) -> int:
    material = f"p3-s03|{master_seed}|{label}".encode("utf-8")
    return int.from_bytes(hashlib.sha256(material).digest()[:8], "big")


class SplitAdaptationController:
    """Stateful controller with independent parameter and strategy RNG streams."""

    def __init__(self, config: AdaptationConfig, seed: int):
        config.validate()
        self.config = config
        self.parameter_rng = random.Random(_labelled_seed(seed, "parameter"))
        self.strategy_rng = random.Random(_labelled_seed(seed, "strategy"))
        self.strategy_success = [1.0, 1.0]  # rand/1, best/1

    def propose_controls(self, parent: IndividualControls) -> IndividualControls:
        if not self.config.parameter_adaptive:
            return IndividualControls(self.config.f_fixed, self.config.cr_fixed)
        if self.parameter_rng.random() >= self.config.resample_probability:
            return parent
        return IndividualControls(
            f=self.parameter_rng.uniform(0.1, 0.9),
            cr=self.parameter_rng.uniform(0.0, 1.0),
        )

    def choose_strategy(self) -> str:
        if not self.config.strategy_adaptive:
            return "rand/1"
        probability_best = self.strategy_success[1] / sum(self.strategy_success)
        return "best/1" if self.strategy_rng.random() < probability_best else "rand/1"

    def credit(self, strategy: str, successful: bool) -> None:
        if self.config.strategy_adaptive and successful:
            self.strategy_success[0 if strategy == "rand/1" else 1] += 1.0

    def finish_generation(self) -> None:
        if self.config.strategy_adaptive:
            self.strategy_success = [max(0.2, value * 0.95) for value in self.strategy_success]


def inherit_selected_controls(
    parent_controls: Sequence[IndividualControls],
    trial_controls: Sequence[IndividualControls],
    survivor_indices: Sequence[int],
) -> list[IndividualControls]:
    """Apply environmental-selection indices to controls as well as genomes."""

    union = list(parent_controls) + list(trial_controls)
    if any(index < 0 or index >= len(union) for index in survivor_indices):
        raise ContractError("survivor index outside parent/trial union")
    return [union[index] for index in survivor_indices]


@dataclass(frozen=True)
class DecisionVariable:
    variable_id: str
    kind: ActionKind
    source_subnet: str
    target_network: str
    target_element_type: str
    target_element_id: str
    cost_units: float
    capacity_increment: float
    capacity_unit: str
    provenance: str

    def validate(self) -> None:
        required = {
            "variable_id": self.variable_id,
            "source_subnet": self.source_subnet,
            "target_network": self.target_network,
            "target_element_type": self.target_element_type,
            "target_element_id": self.target_element_id,
            "capacity_unit": self.capacity_unit,
            "provenance": self.provenance,
        }
        missing = [name for name, value in required.items() if not str(value).strip()]
        if missing:
            raise ContractError(f"decision variable has empty fields: {', '.join(missing)}")
        if not math.isfinite(self.cost_units) or self.cost_units < 0:
            raise ContractError("cost_units must be finite and nonnegative")
        if not math.isfinite(self.capacity_increment) or self.capacity_increment < 0:
            raise ContractError("capacity_increment must be finite and nonnegative")
        expected_target = {
            ActionKind.REINFORCEMENT: "line",
            ActionKind.STORAGE: "bus",
            ActionKind.DER: "bus",
            ActionKind.AUTOMATION: "switch",
        }[self.kind]
        if self.target_element_type != expected_target:
            raise ContractError(f"{self.kind.value} requires target type {expected_target}")


@dataclass(frozen=True)
class NetworkAction:
    variable_id: str
    network: str
    target: str
    cost_units: float
    electrical_effect: str
    proxy_effect: str


def bind_network_action(variable: DecisionVariable) -> NetworkAction:
    """Convert one fully registered decision variable to an auditable action."""

    variable.validate()
    target = f"{variable.target_element_type}:{variable.target_element_id}"
    effects = {
        ActionKind.REINFORCEMENT: (
            f"increase line parallel circuits by {variable.capacity_increment:g}",
            "loss, voltage-risk, hosting, reliability, and resilience proxy terms",
        ),
        ActionKind.STORAGE: (
            f"add controllable storage at bus with {variable.capacity_increment:g} {variable.capacity_unit}",
            "loss, voltage-risk, hosting, reliability, resilience, and DER-support proxy terms",
        ),
        ActionKind.DER: (
            f"add static generation at bus with {variable.capacity_increment:g} {variable.capacity_unit}",
            "loss, hosting, reliability, resilience, and DER-support proxy terms",
        ),
        ActionKind.AUTOMATION: (
            "no steady-state AC injection or impedance change; record switch action for reliability study",
            "reliability and resilience proxy terms only",
        ),
    }
    electrical, proxy = effects[variable.kind]
    return NetworkAction(
        variable_id=variable.variable_id,
        network=variable.target_network,
        target=target,
        cost_units=variable.cost_units,
        electrical_effect=electrical,
        proxy_effect=proxy,
    )


def validate_complete_registry(
    variable_ids: Iterable[str], registry: Mapping[str, DecisionVariable]
) -> list[NetworkAction]:
    """Reject missing, extra, duplicate-by-key, or mismatched action bindings."""

    expected = list(variable_ids)
    if len(expected) != len(set(expected)):
        raise ContractError("optimizer variable IDs must be unique")
    missing = sorted(set(expected) - set(registry))
    extra = sorted(set(registry) - set(expected))
    if missing or extra:
        raise ContractError(f"registry mismatch; missing={missing}, extra={extra}")
    actions = []
    for variable_id in expected:
        variable = registry[variable_id]
        if variable.variable_id != variable_id:
            raise ContractError(f"registry key/variable mismatch: {variable_id}")
        actions.append(bind_network_action(variable))
    return actions


def decode_genome(genome: Sequence[float], threshold: float = 0.5) -> list[int]:
    """Frozen phenotype rule: equality is selected (g >= 0.5)."""

    if threshold != 0.5:
        raise ContractError("the preregistered decoding threshold is exactly 0.5")
    if any(not math.isfinite(value) for value in genome):
        raise ContractError("genome contains a non-finite value")
    return [int(value >= threshold) for value in genome]


def repair_to_budget(
    phenotype: Sequence[int],
    variables: Sequence[DecisionVariable],
    benefit_scores: Sequence[float],
    budget: float,
) -> list[int]:
    """Deterministic repair: drop lowest benefit/cost, tie by variable ID."""

    if not (len(phenotype) == len(variables) == len(benefit_scores)):
        raise ContractError("repair arrays must have equal lengths")
    if budget < 0 or not math.isfinite(budget):
        raise ContractError("budget must be finite and nonnegative")
    repaired = [int(bool(value)) for value in phenotype]
    for variable in variables:
        variable.validate()
    while sum(x * v.cost_units for x, v in zip(repaired, variables)) > budget + 1e-12:
        selected = [index for index, value in enumerate(repaired) if value]
        if not selected:
            raise ContractError("repair could not produce an affordable phenotype")
        def order_key(index: int) -> tuple[float, str]:
            cost = variables[index].cost_units
            ratio = benefit_scores[index] / cost if cost > 0 else math.inf
            return ratio, variables[index].variable_id
        repaired[min(selected, key=order_key)] = 0
    return repaired


@dataclass(frozen=True)
class OperatingScenario:
    scenario_id: str
    load_multiplier: float
    der_multiplier: float
    n_minus_one: bool


FROZEN_AC_SCENARIOS = (
    OperatingScenario("base", 1.0, 1.0, False),
    OperatingScenario("peak_load", 1.3, 1.0, False),
    OperatingScenario("load_growth", 1.5, 1.0, False),
    OperatingScenario("extreme_growth", 1.8, 1.0, False),
    OperatingScenario("high_der", 0.5, 2.5, False),
    OperatingScenario("growth_n_minus_one", 1.5, 1.0, True),
)


@dataclass
class EvaluationAccount:
    generated_candidates: int = 0
    objective_rows: int = 0
    power_flow_attempts: int = 0
    power_flow_failures: int = 0

    def charge_candidates(self, count: int) -> None:
        if count < 0:
            raise ContractError("negative candidate charge")
        self.generated_candidates += count

    def charge_objective_rows(self, count: int) -> None:
        if count < 0:
            raise ContractError("negative objective-row charge")
        self.objective_rows += count

    def charge_power_flow(self, converged: bool) -> None:
        self.power_flow_attempts += 1
        self.power_flow_failures += int(not converged)


@dataclass(frozen=True)
class ACValidationResult:
    converged: bool
    min_voltage_pu: float | None
    max_voltage_pu: float | None
    max_line_loading_percent: float | None

    def feasible(self) -> bool:
        if not self.converged:
            return False
        values = (self.min_voltage_pu, self.max_voltage_pu, self.max_line_loading_percent)
        if any(value is None or not math.isfinite(value) for value in values):
            return False
        return (
            self.min_voltage_pu >= 0.95
            and self.max_voltage_pu <= 1.05
            and self.max_line_loading_percent <= 100.0
        )
