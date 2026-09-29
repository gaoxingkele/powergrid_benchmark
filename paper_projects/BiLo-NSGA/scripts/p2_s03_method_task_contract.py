"""Prospective P2 method/task implementation contract; no experiment results.

The module deliberately does not read the legacy archive.  It fixes the
semantics needed by the next experiment: two source-separated action-task
builders, budget violation and repair, deterministic local moves, strict
acceptance, duplicate caching, evaluation accounting, and bounded stopping.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import math
from typing import Callable, Iterable, Mapping, Sequence


class ContractError(ValueError):
    """Raised when a preregistered method/task invariant is violated."""


Phenotype = tuple[int, ...]
Score = tuple[float, ...]


@dataclass(frozen=True)
class CostModel:
    formula_id: str
    provenance: str
    fixed_units: float
    variable_units: float
    variable_name: str

    def cost(self, value: float) -> float:
        fields = (self.fixed_units, self.variable_units, value)
        if not all(math.isfinite(item) for item in fields) or value < 0:
            raise ContractError("cost model inputs must be finite and nonnegative")
        result = self.fixed_units + self.variable_units * value
        if result < 0:
            raise ContractError("cost model produced a negative cost")
        return result

    def validate(self) -> None:
        if not self.formula_id.strip() or not self.provenance.strip() or not self.variable_name.strip():
            raise ContractError("cost formula id, variable name, and provenance are required")
        self.cost(0.0)


@dataclass(frozen=True)
class InvestmentAction:
    task_family: str
    action_id: str
    source_artifact: str
    source_sha256: str
    source_element_id: str
    action_type: str
    capacity_increment: float
    capacity_unit: str
    cost_units: float
    cost_formula_id: str
    cost_formula_input: float
    cost_formula_input_name: str
    cost_fixed_units: float
    cost_variable_units: float
    cost_provenance: str

    def validate(self) -> None:
        text = (
            self.task_family, self.action_id, self.source_artifact,
            self.source_sha256, self.source_element_id, self.action_type,
            self.capacity_unit, self.cost_formula_id,
            self.cost_formula_input_name, self.cost_provenance,
        )
        if any(not value.strip() for value in text):
            raise ContractError("all action identity and provenance fields are required")
        if len(self.source_sha256) != 64 or any(c not in "0123456789abcdef" for c in self.source_sha256.lower()):
            raise ContractError("source_sha256 must be a 64-character hexadecimal digest")
        numbers = (
            self.capacity_increment, self.cost_units, self.cost_formula_input,
            self.cost_fixed_units, self.cost_variable_units,
        )
        if not all(math.isfinite(value) and value >= 0 for value in numbers):
            raise ContractError("action increments and costs must be finite and nonnegative")


def _required_float(row: Mapping[str, object], name: str) -> float:
    if name not in row:
        raise ContractError(f"missing source field: {name}")
    value = float(row[name])
    if not math.isfinite(value) or value < 0:
        raise ContractError(f"invalid source field: {name}")
    return value


def build_rts_transmission_tasks(
    rows: Iterable[Mapping[str, object]], source_artifact: str, source_sha256: str,
    cost_model: CostModel,
) -> list[InvestmentAction]:
    """Build an RTS-only branch-reinforcement family from identified branches."""
    cost_model.validate()
    if cost_model.variable_name != "capacity_increment_mva":
        raise ContractError("RTS cost model must use capacity_increment_mva")
    actions = []
    for row in rows:
        branch_id = str(row.get("branch_id", "")).strip()
        if not branch_id:
            raise ContractError("RTS row requires branch_id")
        increment = _required_float(row, "capacity_increment_mva")
        action = InvestmentAction(
            "rts_transmission_reinforcement", f"rts-branch::{branch_id}",
            source_artifact, source_sha256, branch_id, "increase_branch_rating",
            increment, "MVA", cost_model.cost(increment), cost_model.formula_id,
            increment, cost_model.variable_name, cost_model.fixed_units,
            cost_model.variable_units, cost_model.provenance,
        )
        action.validate()
        actions.append(action)
    return _validate_family(actions, "rts_transmission_reinforcement")


def build_simbench_feeder_tasks(
    rows: Iterable[Mapping[str, object]], source_artifact: str, source_sha256: str,
    cost_model: CostModel,
) -> list[InvestmentAction]:
    """Build a SimBench-only line-reinforcement family from identified lines."""
    cost_model.validate()
    if cost_model.variable_name != "line_length_km":
        raise ContractError("SimBench cost model must use line_length_km")
    actions = []
    for row in rows:
        line_id = str(row.get("line_id", "")).strip()
        if not line_id:
            raise ContractError("SimBench row requires line_id")
        length = _required_float(row, "line_length_km")
        increment = _required_float(row, "capacity_increment_mva")
        action = InvestmentAction(
            "simbench_feeder_reinforcement", f"simbench-line::{line_id}",
            source_artifact, source_sha256, line_id, "increase_line_rating",
            increment, "MVA", cost_model.cost(length), cost_model.formula_id,
            length, cost_model.variable_name, cost_model.fixed_units,
            cost_model.variable_units, cost_model.provenance,
        )
        action.validate()
        actions.append(action)
    return _validate_family(actions, "simbench_feeder_reinforcement")


def _validate_family(actions: Sequence[InvestmentAction], expected: str) -> list[InvestmentAction]:
    if not actions:
        raise ContractError("a task family cannot be empty")
    if any(action.task_family != expected for action in actions):
        raise ContractError("task-family contamination")
    ids = [action.action_id for action in actions]
    if len(ids) != len(set(ids)):
        raise ContractError("action IDs must be unique within a family")
    return sorted(actions, key=lambda item: item.action_id)


def validate_independent_families(
    rts: Sequence[InvestmentAction], simbench: Sequence[InvestmentAction]
) -> None:
    _validate_family(rts, "rts_transmission_reinforcement")
    _validate_family(simbench, "simbench_feeder_reinforcement")
    if {item.action_id for item in rts} & {item.action_id for item in simbench}:
        raise ContractError("task-family action namespaces overlap")
    if {item.source_sha256 for item in rts} & {item.source_sha256 for item in simbench}:
        raise ContractError("independent families must use distinct source snapshots")


def canonical(phenotype: Sequence[int]) -> Phenotype:
    if any(value not in (0, 1, False, True) for value in phenotype):
        raise ContractError("phenotype must be binary")
    return tuple(int(value) for value in phenotype)


def portfolio_cost(x: Sequence[int], actions: Sequence[InvestmentAction]) -> float:
    key = canonical(x)
    if len(key) != len(actions):
        raise ContractError("phenotype/action length mismatch")
    return sum(bit * action.cost_units for bit, action in zip(key, actions))


def normalized_violation(x: Sequence[int], actions: Sequence[InvestmentAction], budget: float) -> float:
    if not math.isfinite(budget) or budget <= 0:
        raise ContractError("budget must be finite and strictly positive")
    return max(0.0, (portfolio_cost(x, actions) - budget) / budget)


def _ratio(benefit: float, cost: float) -> float:
    if not math.isfinite(benefit):
        raise ContractError("ranking benefits must be finite")
    return math.inf if cost == 0 and benefit >= 0 else (-math.inf if cost == 0 else benefit / cost)


def repair_to_budget(
    x: Sequence[int], actions: Sequence[InvestmentAction], benefits: Sequence[float], budget: float
) -> tuple[Phenotype, tuple[str, ...]]:
    """Drop lowest benefit/cost; ties use ascending action_id."""
    current = list(canonical(x))
    if len(current) != len(actions) or len(actions) != len(benefits):
        raise ContractError("repair arrays must have equal lengths")
    removed: list[str] = []
    while normalized_violation(current, actions, budget) > 0:
        selected = [i for i, bit in enumerate(current) if bit]
        if not selected:
            raise ContractError("repair cannot reach the positive budget")
        weakest = min(selected, key=lambda i: (_ratio(benefits[i], actions[i].cost_units), actions[i].action_id))
        current[weakest] = 0
        removed.append(actions[weakest].action_id)
    return tuple(current), tuple(removed)


@dataclass
class EvaluationLedger:
    unique_limit: int
    request_limit: int
    requests: int = 0
    unique_evaluations: int = 0
    cache_hits: int = 0
    cache: dict[Phenotype, tuple[Score, float]] = field(default_factory=dict)

    def can_request(self) -> bool:
        return self.requests < self.request_limit and self.unique_evaluations < self.unique_limit

    def evaluate(
        self, x: Sequence[int], scorer: Callable[[Phenotype], Score],
        actions: Sequence[InvestmentAction], budget: float,
    ) -> tuple[Score, float] | None:
        if not self.can_request():
            return None
        self.requests += 1
        key = canonical(x)
        if key in self.cache:
            self.cache_hits += 1
            return self.cache[key]
        score = tuple(float(value) for value in scorer(key))
        if not score or any(not math.isfinite(value) for value in score):
            raise ContractError("objective score must be finite and nonempty")
        result = (score, normalized_violation(key, actions, budget))
        self.cache[key] = result
        self.unique_evaluations += 1
        return result


def scalar_acceptance(score: Score, violation: float, lo: Score, hi: Score, penalty: float) -> float:
    if not (len(score) == len(lo) == len(hi)) or penalty < 0 or not math.isfinite(penalty):
        raise ContractError("invalid frozen acceptance inputs")
    return sum((value - low) / max(high - low, 1e-12) for value, low, high in zip(score, lo, hi)) + penalty * violation


def _best(indices: Iterable[int], benefits: Sequence[float], actions: Sequence[InvestmentAction]) -> int | None:
    values = list(indices)
    return min(values, key=lambda i: (-_ratio(benefits[i], actions[i].cost_units), actions[i].action_id)) if values else None


def propose_forward(x: Sequence[int], actions: Sequence[InvestmentAction], benefits: Sequence[float], budget: float) -> Phenotype | None:
    key = canonical(x)
    slack = budget - portfolio_cost(key, actions)
    index = _best((i for i, bit in enumerate(key) if not bit and actions[i].cost_units <= slack + 1e-12), benefits, actions)
    if index is None:
        return None
    result = list(key); result[index] = 1
    return tuple(result)


def propose_backward(x: Sequence[int], actions: Sequence[InvestmentAction], benefits: Sequence[float]) -> Phenotype | None:
    key = canonical(x)
    selected = [i for i, bit in enumerate(key) if bit]
    if not selected:
        return None
    index = min(selected, key=lambda i: (_ratio(benefits[i], actions[i].cost_units), actions[i].action_id))
    result = list(key); result[index] = 0
    return tuple(result)


def propose_atomic_substitution(x: Sequence[int], actions: Sequence[InvestmentAction], benefits: Sequence[float], budget: float) -> Phenotype | None:
    key = canonical(x)
    selected = [i for i, bit in enumerate(key) if bit]
    if not selected:
        return None
    removed = min(selected, key=lambda i: (_ratio(benefits[i], actions[i].cost_units), actions[i].action_id))
    provisional = list(key); provisional[removed] = 0
    slack = budget - portfolio_cost(provisional, actions)
    replacement = _best((i for i, bit in enumerate(provisional) if not bit and i != removed and actions[i].cost_units <= slack + 1e-12), benefits, actions)
    if replacement is None:
        return None
    provisional[replacement] = 1
    return tuple(provisional)


def run_local_pass(
    x: Sequence[int], operator: str, depth: int, actions: Sequence[InvestmentAction],
    benefits: Sequence[float], budget: float, scorer: Callable[[Phenotype], Score],
    lo: Score, hi: Score, penalty: float, ledger: EvaluationLedger,
) -> tuple[Phenotype, int, str]:
    """First-improvement pass; a tie is rejection and ends the pass."""
    if depth < 0:
        raise ContractError("depth must be nonnegative")
    current = canonical(x)
    evaluated = ledger.evaluate(current, scorer, actions, budget)
    if evaluated is None:
        return current, 0, "evaluation_limit"
    current_score, current_violation = evaluated
    accepted = 0
    for _ in range(depth):
        if operator == "forward":
            proposal = propose_forward(current, actions, benefits, budget)
        elif operator == "backward":
            proposal = propose_backward(current, actions, benefits)
        elif operator == "atomic_substitution":
            proposal = propose_atomic_substitution(current, actions, benefits, budget)
        else:
            raise ContractError("unknown local operator")
        if proposal is None:
            return current, accepted, "neighborhood_exhausted"
        evaluated = ledger.evaluate(proposal, scorer, actions, budget)
        if evaluated is None:
            return current, accepted, "evaluation_limit"
        proposal_score, proposal_violation = evaluated
        before = scalar_acceptance(current_score, current_violation, lo, hi, penalty)
        after = scalar_acceptance(proposal_score, proposal_violation, lo, hi, penalty)
        if not after < before:
            return current, accepted, "first_non_improvement"
        current, current_score, current_violation = proposal, proposal_score, proposal_violation
        accepted += 1
    return current, accepted, "depth_limit"


@dataclass(frozen=True)
class ArmResult:
    phenotype: Phenotype
    accepted_forward: int
    accepted_backward: int
    termination_reasons: tuple[str, ...]


def run_arm_local_search(
    x: Sequence[int], arm: str, forward_depth: int, backward_depth: int,
    actions: Sequence[InvestmentAction], benefits: Sequence[float], budget: float,
    scorer: Callable[[Phenotype], Score], lo: Score, hi: Score, penalty: float,
    ledger: EvaluationLedger,
) -> ArmResult:
    """Apply the declared principal arm; substitution is intentionally absent."""
    if arm not in {"nds_only", "forward_only", "backward_only", "bidirectional"}:
        raise ContractError("unknown principal arm")
    current = canonical(x)
    accepted_forward = accepted_backward = 0
    reasons: list[str] = []
    if arm in {"forward_only", "bidirectional"}:
        current, accepted_forward, reason = run_local_pass(
            current, "forward", forward_depth, actions, benefits, budget,
            scorer, lo, hi, penalty, ledger,
        )
        reasons.append(f"forward:{reason}")
    if arm in {"backward_only", "bidirectional"} and ledger.can_request():
        current, accepted_backward, reason = run_local_pass(
            current, "backward", backward_depth, actions, benefits, budget,
            scorer, lo, hi, penalty, ledger,
        )
        reasons.append(f"backward:{reason}")
    if arm == "nds_only":
        reasons.append("local_search_disabled")
    return ArmResult(current, accepted_forward, accepted_backward, tuple(reasons))
