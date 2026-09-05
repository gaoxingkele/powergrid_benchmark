"""Run the non-paper P1 activation pilot fixed in ``pilot_config.json``."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import platform
import sys
import time
import warnings
from dataclasses import asdict, replace
from pathlib import Path

import numpy as np


PILOT_ROOT = Path(__file__).resolve().parent
EXPERIMENT_ROOT = PILOT_ROOT.parent
INPUT_ROOT = PILOT_ROOT / "inputs"
RAW_ROOT = PILOT_ROOT / "raw"


def sha256(path: Path, *, normalize_lf: bool = False) -> str:
    payload = path.read_bytes()
    if normalize_lf:
        payload = payload.replace(b"\r\n", b"\n")
    return hashlib.sha256(payload).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def load_core():
    path = PILOT_ROOT / "runtime" / "core_snapshot.py"
    spec = importlib.util.spec_from_file_location("p1_pilot_core", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load core snapshot: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.RTS_SOURCE = INPUT_ROOT / "rts"
    module.SIMBENCH_NET = INPUT_ROOT / "simbench"
    module.NERC_ROOT = INPUT_ROOT / "nerc"
    return module


class CountingProblem:
    """Delegate the frozen problem while counting evaluated candidate rows."""

    def __init__(self, base):
        self._base = base
        self.objective_calls = 0

    def objectives(self, x: np.ndarray) -> np.ndarray:
        rows = int(np.atleast_2d(x).shape[0])
        self.objective_calls += rows
        return self._base.objectives(x)

    def __getattr__(self, name: str):
        return getattr(self._base, name)


def analytic_bounds(problem) -> tuple[np.ndarray, np.ndarray]:
    lo = np.array(
        [
            0.0,
            -float(problem.reliability.sum()),
            -float(problem.renewable.sum()),
            min(float(problem.risk.min()), 1.0),
            -float(problem.quality.max()),
        ]
    )
    hi = np.array(
        [float(problem.budget), 0.0, 0.0, max(float(problem.risk.max()), 1.0), 0.0]
    )
    if not np.all(np.isfinite(lo)) or not np.all(np.isfinite(hi)) or np.any(hi <= lo):
        raise ValueError("invalid analytic bounds")
    return lo, hi


def primary_hv(front: np.ndarray, lo: np.ndarray, hi: np.ndarray) -> float:
    from pymoo.indicators.hv import HV

    if front.size == 0:
        return 0.0
    normalized = (front - lo) / (hi - lo)
    if np.any(normalized > 1.0 + 1e-10) or np.any(normalized < -1e-10):
        raise ValueError("front exceeds frozen analytic bounds; clipping is forbidden")
    return float(HV(ref_point=np.full(front.shape[1], 1.1))(normalized))


def run_nsga2(core, problem: CountingProblem, seed: int, call_limit: int) -> np.ndarray:
    from pymoo.algorithms.moo.nsga2 import NSGA2
    from pymoo.core.problem import Problem as PymooProblem
    from pymoo.core.sampling import Sampling
    from pymoo.operators.crossover.pntx import TwoPointCrossover
    from pymoo.operators.mutation.bitflip import BitflipMutation
    from pymoo.optimize import minimize

    class LowDensitySampling(Sampling):
        def _do(self, pymoo_problem, n_samples, **kwargs):
            rng = np.random.default_rng(seed)
            density = rng.uniform(0.03, 0.15, size=(n_samples, 1))
            return rng.random((n_samples, pymoo_problem.n_var)) < density

    class Wrapped(PymooProblem):
        def __init__(self) -> None:
            super().__init__(n_var=problem.n, n_obj=problem.n_obj, n_ieq_constr=1, xl=0, xu=1, vtype=bool)

        def _evaluate(self, x, out, *args, **kwargs):
            xf = x.astype(float)
            out["F"] = problem.objectives(xf)
            out["G"] = problem.violation(xf)[:, None]

    algorithm = NSGA2(
        pop_size=core.POP_SIZE,
        sampling=LowDensitySampling(),
        crossover=TwoPointCrossover(),
        mutation=BitflipMutation(),
    )
    result = minimize(Wrapped(), algorithm, ("n_eval", call_limit), seed=seed, verbose=False)
    x = result.pop.get("X") if result.pop is not None else result.X
    return np.atleast_2d(x).astype(float)


def candidate_rows(candidates) -> list[dict[str, object]]:
    return [asdict(candidate) for candidate in candidates]


def environment_record(core) -> dict[str, object]:
    import pymoo
    import scipy

    return {
        "python": platform.python_version(),
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "pymoo": pymoo.__version__,
        "core_status": core.STATUS,
        "paper_use": False,
    }


def selected_hash(core, x: np.ndarray, problem) -> str:
    front_x, _ = core.feasible_front(problem, x)
    payload = front_x.astype(np.uint8).tobytes()
    return hashlib.sha256(payload).hexdigest()


def execute_once(core, method: str, candidates, scenario: str, seed: int, call_limit: int):
    pool = core.experiment_pool(scenario, candidates)
    evaluation_problem = core.PortfolioProblem(pool, "p5", core.budget_for(scenario, "p5"))
    counted = CountingProblem(evaluation_problem)
    started = time.perf_counter()
    if method == "Full_TRACE":
        trace = next(spec for spec in core.p5_methods() if spec.name == "TRACE-MOEA")
        config = replace(trace.engine, pop_size=40, generations=40)
        result = core.run_custom_ea(
            counted,
            config,
            seed,
            seed_weights=core.experiment_weights(scenario, "p5"),
        )
        x = result.population
        event_count = len(result.trace_events)
        configuration_id = "pilot_diagnostic_trace_defaults"
    elif method == "NSGA-II":
        x = run_nsga2(core, counted, seed, call_limit)
        event_count = 0
        configuration_id = "pilot_diagnostic_nsga2_defaults"
    else:
        raise ValueError(method)
    wall = time.perf_counter() - started
    front_x, front_f = core.feasible_front(evaluation_problem, x)
    lo, hi = analytic_bounds(evaluation_problem)
    hv = primary_hv(front_f, lo, hi)
    if front_x.shape[0]:
        index = int(np.argmin(((front_f - lo) / (hi - lo)).sum(axis=1)))
        compromise = front_x[index]
        size = int(compromise.sum())
        synthetic_cost = float(compromise @ evaluation_problem.cost)
        risk = float(compromise @ evaluation_problem.risk / max(size, 1))
    else:
        size, synthetic_cost, risk = 0, 0.0, 1.0
    feasible_share = float(np.mean(evaluation_problem.violation(x) <= 1e-12))
    return {
        "method": method,
        "configuration_id": configuration_id,
        "seed": seed,
        "objective_calls_executed": counted.objective_calls,
        "wall_time_seconds": wall,
        "primary_hv": hv,
        "front_size": int(front_f.shape[0]),
        "feasible_front_proportion": feasible_share,
        "budget_utilization": synthetic_cost / evaluation_problem.budget,
        "synthetic_cost_index": synthetic_cost,
        "portfolio_cardinality": size,
        "risk_proxy": risk,
        "event_count": event_count,
        "selected_front_sha256": selected_hash(core, x, evaluation_problem),
    }


def main() -> int:
    config_path = PILOT_ROOT / "pilot_config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if config["paper_use"] is not False or config["may_select_configuration"] is not False:
        raise ValueError("pilot exclusion flags are not locked")
    formal = json.loads((EXPERIMENT_ROOT / "config.json").read_text(encoding="utf-8"))
    forbidden = set(formal["seeds"]) | set(formal["tuning"]["seeds"])
    if forbidden.intersection(config["seeds"]):
        raise ValueError("pilot seed leakage into tuning or confirmatory schedule")

    core = load_core()
    candidates = core.build_candidates()
    if len(candidates) != 120:
        raise ValueError(f"expected 120 candidates, found {len(candidates)}")
    candidate_path = PILOT_ROOT / "candidate_pool.csv"
    write_csv(candidate_path, candidate_rows(candidates))

    warning_rows: list[dict[str, str]] = []
    planned_env = json.loads((EXPERIMENT_ROOT / "environment.json").read_text(encoding="utf-8"))
    actual_env = environment_record(core)
    for package, planned in planned_env["packages"].items():
        actual = str(actual_env[package])
        if actual != str(planned):
            warning_rows.append({"category": "environment_mismatch", "detail": f"{package}: planned {planned}, actual {actual}", "disposition": "blocks formal execution; no substitution claim"})
    warning_rows.append({"category": "nerc_redistribution", "detail": "Only a local metadata index is used; official website access does not confer a redistribution licence.", "disposition": "no NERC PDFs copied; blocks release of the metadata snapshot pending human/legal confirmation"})

    rows: list[dict[str, object]] = []
    replay_rows: list[dict[str, object]] = []
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        for seed in config["seeds"]:
            for method in config["methods"]:
                result = execute_once(core, method, candidates, config["scenario"], seed, config["objective_call_limit"])
                rows.append(result)
                replay = execute_once(core, method, candidates, config["scenario"], seed, config["objective_call_limit"])
                replay_rows.append({
                    "method": method,
                    "seed": seed,
                    "objective_calls_match": replay["objective_calls_executed"] == result["objective_calls_executed"],
                    "selected_front_hash_match": replay["selected_front_sha256"] == result["selected_front_sha256"],
                    "primary_hv_exact_match": replay["primary_hv"] == result["primary_hv"],
                })
        for item in caught:
            warning_rows.append({"category": "runtime_warning", "detail": str(item.message), "disposition": "reviewed; retained verbatim"})

    required = formal["output_schema"]["required_run_fields"]
    hashes = {
        "config_sha256": sha256(EXPERIMENT_ROOT / "config.json", normalize_lf=True),
        "data_manifest_sha256": sha256(EXPERIMENT_ROOT / "data_manifest.json", normalize_lf=True),
        "environment_sha256": sha256(EXPERIMENT_ROOT / "environment.json", normalize_lf=True),
        "bounds_sha256": sha256(EXPERIMENT_ROOT / "bounds.csv", normalize_lf=True),
    }
    output_rows: list[dict[str, object]] = []
    for row in rows:
        output_rows.append({
            "experiment_id": formal["experiment_id"], "phase": "pilot", "method": row["method"],
            "configuration_id": row["configuration_id"], "scenario": config["scenario"], "seed": row["seed"],
            "budget_multiplier": config["budget_multiplier"], "objective_call_limit": config["objective_call_limit"],
            "objective_calls_executed": row["objective_calls_executed"], "wall_time_seconds": f"{row['wall_time_seconds']:.6f}",
            "status": "completed", "failure_class": "", "primary_hv": f"{row['primary_hv']:.12f}",
            "front_size": row["front_size"], "feasible_front_proportion": f"{row['feasible_front_proportion']:.12f}",
            "budget_utilization": f"{row['budget_utilization']:.12f}", "synthetic_cost_index": f"{row['synthetic_cost_index']:.12f}",
            "portfolio_cardinality": row["portfolio_cardinality"], "risk_proxy": f"{row['risk_proxy']:.12f}",
            "event_count": row["event_count"], "event_position_cooccurrence": "not_computed_in_pilot",
            **hashes,
        })
    if list(output_rows[0]) != required:
        raise ValueError("pilot output columns do not match the frozen output schema")

    budget_equal = all(int(row["objective_calls_executed"]) == config["objective_call_limit"] for row in rows)
    replay_clear = all(all(value is True for key, value in row.items() if key.endswith("match")) for row in replay_rows)
    bounds_match = hashes["bounds_sha256"] == formal["hv_bounds"]["stage4_bounds_sha256"]
    feasibility_clear = all(0.0 <= float(row["budget_utilization"]) <= 1.0 + 1e-12 for row in rows)
    status = "PASS" if budget_equal and replay_clear and bounds_match and feasibility_clear else "FAIL"

    write_csv(RAW_ROOT / "results.csv", output_rows)
    write_csv(PILOT_ROOT / "replay_audit.csv", replay_rows)
    write_csv(PILOT_ROOT / "warnings.csv", warning_rows)
    write_json(PILOT_ROOT / "environment_resolved.json", actual_env)
    input_files = sorted(path for path in INPUT_ROOT.rglob("*") if path.is_file())
    write_json(PILOT_ROOT / "input_manifest.json", {
        "candidate_pool": {"path": "candidate_pool.csv", "rows": len(candidates), "sha256": sha256(candidate_path)},
        "files": [{"path": path.relative_to(PILOT_ROOT).as_posix(), "sha256": sha256(path), "bytes": path.stat().st_size} for path in input_files],
        "core_snapshot": {"path": "runtime/core_snapshot.py", "sha256": sha256(PILOT_ROOT / "runtime" / "core_snapshot.py")},
        "licence_scope": {
            "RTS-GMLC": "notice copied with the three source tables; reuse terms permit use/copy/distribution with the complete notice and attribution",
            "SimBench": "LICENSE copied; database is ODbL 1.0 and contents are DBCL 1.0",
            "NERC": "metadata-only local pilot use; no source PDF/text redistributed; redistribution permission not established",
        },
    })
    total_wall = sum(float(row["wall_time_seconds"]) for row in rows)
    mean_wall = total_wall / len(rows)
    write_json(PILOT_ROOT / "resource_estimate.json", {
        "distinct_pilot_runs": len(rows), "paired_seeds": len(config["seeds"]), "measured_total_seconds_excluding_replay": total_wall,
        "mean_seconds_per_run": mean_wall, "projected_formal_stochastic_runs": formal["budgets"]["formal_unique_stochastic_runs"],
        "projected_serial_seconds": mean_wall * formal["budgets"]["formal_unique_stochastic_runs"],
        "scope": "host-specific feasibility estimate only; replay overhead excluded; not a cross-platform efficiency claim",
    })
    manifest = {
        "experiment_id": formal["experiment_id"], "phase": "pilot", "paper_use": False,
        "pilot_config_sha256": sha256(config_path, normalize_lf=True),
        "scenario": config["scenario"], "methods": config["methods"], "seeds": config["seeds"],
        "paired_seed_count": len(config["seeds"]), "runs_completed": len(rows), "replay_executions": len(replay_rows),
        "objective_call_limit": config["objective_call_limit"], "budget_audit": "PASS" if budget_equal else "FAIL",
        "metric_orientation": config["metric_orientation"], "hashes": hashes,
        "artifacts": [
            "PILOT_PLAN.md", "PILOT_REPORT.md", "PILOT_GATE.json",
            "pilot_config.json", "candidate_pool.csv", "raw/results.csv",
            "replay_audit.csv", "warnings.csv", "environment_resolved.json",
            "input_manifest.json", "resource_estimate.json", "runtime/core_snapshot.py",
        ],
    }
    write_json(PILOT_ROOT / "run_manifest.json", manifest)
    write_json(PILOT_ROOT / "PILOT_GATE.json", {
        "status": status, "paper_use": False, "exit_codes_clear": status == "PASS",
        "warnings_reviewed": True, "budget_audit": manifest["budget_audit"],
        "leakage_audit": "PASS: pilot seeds are disjoint from tuning and confirmatory seeds; pilot namespace is separate",
        "decision": "STOP_BEFORE_FORMAL: pilot mechanics passed, but recreate the frozen environment and obtain a human/legal NERC metadata redistribution decision before formal execution",
    })
    print(f"pilot {status}: {len(rows)} distinct runs, {len(config['seeds'])} paired seeds")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
