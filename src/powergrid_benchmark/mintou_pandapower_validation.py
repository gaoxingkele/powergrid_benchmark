"""AC load-flow validation for mintou p3 (CARS-MODE) and p4 (SHIELD-MOEA) plans.

Answers the P0 gap flagged in both journal reviews: the planning experiments
score portfolios with engineering proxies, so manuscript claims about voltage
or feasibility need an actual AC power-flow check. This module:

1. Rebuilds every method's planning portfolio deterministically from
   `mintou_real_planning` (same seeds, same code path as the published runs).
2. Maps the portfolio *composition* onto real SimBench MV networks using a
   fixed, method-independent rule set (documented below), because the planning
   candidates live on aggregated subnet statistics rather than concrete buses:
     - reinforcement x k  -> add one parallel conductor on the k most-loaded lines
     - storage x k        -> sgen at the k weakest-voltage load buses,
                             p = +3% of net load (discharge) in load-stress
                             scenarios, -3% (charging) in the high-DER scenario
     - der x k            -> PV sgen at the k highest-load buses, p = 4% of net
                             load, scaled with the scenario DER factor
     - automation x k     -> no steady-state electrical effect (recorded only)
3. Runs AC power flow across stress scenarios (base, peak 1.3x, growth 1.5x,
   high-DER 1.5x, peak + N-1 line outage) and reports voltage-band, thermal,
   loss, and convergence metrics against a No-Plan reference.

This is an AC feasibility *screen* of plan compositions, not a siting study;
the mapping assumptions are stated in the generated analysis file.
"""

from __future__ import annotations

import csv
import json
import time
import warnings
from pathlib import Path

import numpy as np

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]

NETWORK_CODES = (
    "1-MV-rural--0-sw",
    "1-MV-semiurb--0-sw",
    "1-MV-urban--0-sw",
    "1-MV-comm--0-sw",
)

SCENARIOS = (
    ("base", {"load": 1.0, "der": 1.0, "n1": False}),
    ("peak_load", {"load": 1.3, "der": 1.0, "n1": False}),
    ("load_growth", {"load": 1.5, "der": 1.0, "n1": False}),
    ("extreme_growth", {"load": 1.8, "der": 1.0, "n1": False}),
    ("high_der", {"load": 0.5, "der": 2.5, "n1": False}),
    ("growth_n1_outage", {"load": 1.5, "der": 1.0, "n1": True}),
)

STORAGE_P_FRACTION = 0.03  # per storage action, fraction of total net load
DER_P_FRACTION = 0.04  # per DER action, fraction of total net load
VMIN, VMAX = 0.95, 1.05
LOADING_LIMIT = 100.0

P3_VALIDATION_EXPERIMENTS = ("base_distribution_planning", "der_siting_sizing", "storage_allocation")
P4_VALIDATION_EXPERIMENTS = ("deterministic_vs_scenario", "outage_contingency", "der_uncertainty")

STATUS = "public_simbench_ac_validation_v2_real_moea_plans"


_COMPOSITION_CACHE: dict[str, list[dict[str, str]]] = {}


def load_compositions(paper: str) -> list[dict[str, str]]:
    """Compromise-plan compositions exported by the real-MOEA planning pipeline
    (`mintou_real_planning.py`, seed 0 compromise solution per method/experiment)."""
    from powergrid_benchmark import mintou_real_planning as planning

    if paper not in _COMPOSITION_CACHE:
        root = planning.P3_ROOT if paper == "p3" else planning.P4_ROOT
        path = root / "evidence" / "tables" / "real_simbench_planning_compromise_compositions.csv"
        with path.open(encoding="utf-8-sig", newline="") as handle:
            _COMPOSITION_CACHE[paper] = list(csv.DictReader(handle))
    return _COMPOSITION_CACHE[paper]


def portfolio_composition(paper: str, method_name: str, experiment: str) -> dict[str, int]:
    for row in load_compositions(paper):
        if row["method"] == method_name and row["experiment_id"] == experiment:
            return {
                "reinforcement": int(row["reinforcement"]),
                "storage": int(row["storage"]),
                "der": int(row["der"]),
                "automation": int(row["automation"]),
            }
    raise KeyError(f"no composition for {paper}/{experiment}/{method_name}")


_NET_CACHE: dict[str, object] = {}


def load_network(code: str):
    import copy

    import simbench as sb

    if code not in _NET_CACHE:
        _NET_CACHE[code] = sb.get_simbench_net(code)
    return copy.deepcopy(_NET_CACHE[code])


def choose_n1_line(net) -> int | None:
    """Highest-loaded line whose outage leaves every bus supplied."""
    import pandapower as pp
    import pandapower.topology as top

    try:
        pp.runpp(net, numba=False)
    except Exception:
        return None
    order = net.res_line.loading_percent.sort_values(ascending=False).index
    for line_idx in order:
        net.line.at[line_idx, "in_service"] = False
        unsupplied = top.unsupplied_buses(net)
        net.line.at[line_idx, "in_service"] = True
        if not unsupplied:
            return int(line_idx)
    return None


def apply_plan(net, composition: dict[str, int], der_factor: float, storage_mode: str) -> None:
    """Apply the composition mapping (method-independent constants)."""
    import pandapower as pp

    pp.runpp(net, numba=False)
    total_load = float(net.load.p_mw.sum())

    k_reinforce = composition.get("reinforcement", 0)
    if k_reinforce:
        top_lines = net.res_line.loading_percent.sort_values(ascending=False).index[:k_reinforce]
        for idx in top_lines:
            net.line.at[idx, "parallel"] = int(net.line.at[idx, "parallel"]) + 1

    k_storage = composition.get("storage", 0)
    if k_storage:
        load_buses = net.load.bus.unique()
        vm = net.res_bus.vm_pu.loc[load_buses].sort_values()
        weakest = vm.index[:k_storage]
        sign = -1.0 if storage_mode == "charge" else 1.0
        for bus in weakest:
            pp.create_sgen(net, bus=int(bus), p_mw=sign * STORAGE_P_FRACTION * total_load, q_mvar=0.0, name="plan_storage")

    k_der = composition.get("der", 0)
    if k_der:
        bus_load = net.load.groupby("bus").p_mw.sum().sort_values(ascending=False)
        targets = bus_load.index[:k_der]
        for bus in targets:
            pp.create_sgen(net, bus=int(bus), p_mw=DER_P_FRACTION * total_load * der_factor, q_mvar=0.0, name="plan_der")


def evaluate_case(code: str, composition: dict[str, int] | None, scenario: dict) -> dict[str, object]:
    import pandapower as pp

    net = load_network(code)
    net.load.p_mw *= scenario["load"]
    net.load.q_mvar *= scenario["load"]
    net.sgen.p_mw *= scenario["der"]

    if composition is not None:
        storage_mode = "charge" if scenario["der"] > 1.0 else "discharge"
        apply_plan(net, composition, scenario["der"], storage_mode)

    n1_line = None
    if scenario["n1"]:
        n1_line = choose_n1_line(net)
        if n1_line is not None:
            net.line.at[n1_line, "in_service"] = False

    try:
        pp.runpp(net, numba=False)
        converged = bool(net.converged)
    except Exception:
        converged = False

    if not converged:
        return {
            "converged": False,
            "min_vm_pu": float("nan"),
            "max_vm_pu": float("nan"),
            "n_undervoltage": -1,
            "n_overvoltage": -1,
            "max_line_loading_pct": float("nan"),
            "n_overloaded_lines": -1,
            "losses_mw": float("nan"),
            "ac_feasible": False,
            "n1_line": n1_line if n1_line is not None else "",
        }
    vm = net.res_bus.vm_pu.dropna()
    loading = net.res_line.loading_percent.dropna()
    n_under = int((vm < VMIN).sum())
    n_over = int((vm > VMAX).sum())
    n_overload = int((loading > LOADING_LIMIT).sum())
    return {
        "converged": True,
        "min_vm_pu": float(vm.min()),
        "max_vm_pu": float(vm.max()),
        "n_undervoltage": n_under,
        "n_overvoltage": n_over,
        "max_line_loading_pct": float(loading.max()),
        "n_overloaded_lines": n_overload,
        "losses_mw": float(net.res_line.pl_mw.sum() + net.res_trafo.pl_mw.sum()),
        "ac_feasible": bool(n_under == 0 and n_over == 0 and n_overload == 0),
        "n1_line": n1_line if n1_line is not None else "",
    }


def run_paper(paper: str) -> None:
    from powergrid_benchmark import mintou_real_planning as planning

    root = planning.P3_ROOT if paper == "p3" else planning.P4_ROOT
    experiments = P3_VALIDATION_EXPERIMENTS if paper == "p3" else P4_VALIDATION_EXPERIMENTS

    rows: list[dict[str, str]] = []
    start = time.perf_counter()
    for experiment in experiments:
        exp_rows = [r for r in load_compositions(paper) if r["experiment_id"] == experiment]
        roles = {r["method"]: r["method_role"] for r in exp_rows}
        compositions: dict[str, dict[str, int]] = {"NoPlan": {}}
        for row in exp_rows:
            compositions[row["method"]] = portfolio_composition(paper, row["method"], experiment)
        for method_name, composition in compositions.items():
            role = "reference" if method_name == "NoPlan" else roles[method_name]
            for code in NETWORK_CODES:
                for scenario_name, scenario in SCENARIOS:
                    result = evaluate_case(code, composition if method_name != "NoPlan" else None, scenario)
                    rows.append(
                        {
                            "paper": paper,
                            "experiment_id": experiment,
                            "method": method_name,
                            "method_role": role,
                            "network": code,
                            "scenario": scenario_name,
                            "plan_reinforcement": str(composition.get("reinforcement", 0)),
                            "plan_storage": str(composition.get("storage", 0)),
                            "plan_der": str(composition.get("der", 0)),
                            "plan_automation": str(composition.get("automation", 0)),
                            "converged": str(result["converged"]),
                            "min_vm_pu": f"{result['min_vm_pu']:.6f}",
                            "max_vm_pu": f"{result['max_vm_pu']:.6f}",
                            "n_undervoltage": str(result["n_undervoltage"]),
                            "n_overvoltage": str(result["n_overvoltage"]),
                            "max_line_loading_pct": f"{result['max_line_loading_pct']:.4f}",
                            "n_overloaded_lines": str(result["n_overloaded_lines"]),
                            "losses_mw": f"{result['losses_mw']:.6f}",
                            "ac_feasible": str(result["ac_feasible"]),
                            "n1_line": str(result["n1_line"]),
                            "source_status": STATUS,
                        }
                    )
        print(f"[{paper}] {experiment} validated ({len(compositions)} plans x {len(NETWORK_CODES)} nets x {len(SCENARIOS)} scenarios)")

    # preserve the v1 screen (which validated the deprecated proxy-method plans)
    for src_rel, new_name in [
        ("evidence/runs/real_ac_validation_results.csv", "real_ac_validation_results_v1_proxy_plans.csv"),
        ("evidence/tables/real_ac_validation_summary.csv", "real_ac_validation_summary_v1_proxy_plans.csv"),
        ("evidence/runs/real_ac_validation_analysis.md", "real_ac_validation_analysis_v1_proxy_plans.md"),
    ]:
        src = root / src_rel
        target = src.parent / new_name
        if src.exists() and not target.exists():
            src.rename(target)
    write_csv(root / "evidence" / "runs" / "real_ac_validation_results.csv", rows)
    write_csv(root / "evidence" / "tables" / "real_ac_validation_summary.csv", summarize(rows, paper))
    (root / "evidence" / "runs" / "real_ac_validation_analysis.md").write_text(analysis(rows, paper), encoding="utf-8")
    (root / "src" / "configs" / "real_ac_validation_config.json").write_text(
        json.dumps(
            {
                "networks": list(NETWORK_CODES),
                "scenarios": {name: cfg for name, cfg in SCENARIOS},
                "experiments": list(experiments),
                "storage_p_fraction": STORAGE_P_FRACTION,
                "der_p_fraction": DER_P_FRACTION,
                "voltage_band": [VMIN, VMAX],
                "loading_limit_pct": LOADING_LIMIT,
                "mapping_rules": "reinforcement->parallel conductor on most-loaded lines; storage->sgen at weakest buses (discharge in load stress, charge in high-DER); der->PV sgen at highest-load buses; automation->no steady-state effect",
                "status": STATUS,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"[{paper}] complete in {time.perf_counter() - start:.1f}s")


def summarize(rows: list[dict[str, str]], paper: str) -> list[dict[str, str]]:
    by_method: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        by_method.setdefault(row["method"], []).append(row)
    board = []
    for method, group in by_method.items():
        feasible = [r["ac_feasible"] == "True" for r in group]
        converged = [r["converged"] == "True" for r in group]
        min_vm = [float(r["min_vm_pu"]) for r in group if r["converged"] == "True"]
        max_loading = [float(r["max_line_loading_pct"]) for r in group if r["converged"] == "True"]
        losses = [float(r["losses_mw"]) for r in group if r["converged"] == "True"]
        stress = [r for r in group if r["scenario"] != "base"]
        stress_feasible = [r["ac_feasible"] == "True" for r in stress]
        board.append(
            {
                "paper": paper,
                "method": method,
                "method_role": group[0]["method_role"],
                "cases": str(len(group)),
                "convergence_rate": f"{np.mean(converged):.6f}",
                "ac_feasible_rate": f"{np.mean(feasible):.6f}",
                "stress_ac_feasible_rate": f"{np.mean(stress_feasible):.6f}",
                "mean_min_vm_pu": f"{np.mean(min_vm):.6f}" if min_vm else "NA",
                "mean_max_line_loading_pct": f"{np.mean(max_loading):.4f}" if max_loading else "NA",
                "mean_losses_mw": f"{np.mean(losses):.6f}" if losses else "NA",
            }
        )
    return sorted(board, key=lambda r: (r["method_role"] != "reference", -float(r["ac_feasible_rate"])))


def analysis(rows: list[dict[str, str]], paper: str) -> str:
    summary = summarize(rows, paper)
    proposed_name = "CARS-MODE" if paper == "p3" else "SHIELD-MOEA"
    title = "P3 CARS-MODE" if paper == "p3" else "P4 SHIELD-MOEA"
    noplan = next(r for r in summary if r["method"] == "NoPlan")
    proposed = next(r for r in summary if r["method"] == proposed_name)
    baselines = [r for r in summary if r["method_role"] == "baseline"]
    best_baseline = max(baselines, key=lambda r: float(r["ac_feasible_rate"]))
    lines = [
        f"# SimBench AC Load-Flow Validation - {title}",
        "",
        f"Status: `{STATUS}`. pandapower AC power flow on real SimBench MV networks",
        f"({', '.join(NETWORK_CODES)}) across {len(SCENARIOS)} stress scenarios,",
        "validating the compromise-plan compositions exported by the real-MOEA",
        "planning pipeline (`real_simbench_planning_compromise_compositions.csv`,",
        "seed-0 compromise solution per method/experiment).",
        "",
        "## Headline",
        "",
        f"- No-Plan reference AC-feasible rate: `{noplan['ac_feasible_rate']}` (stress-only: `{noplan['stress_ac_feasible_rate']}`)",
        f"- `{proposed_name}` AC-feasible rate: `{proposed['ac_feasible_rate']}` (stress-only: `{proposed['stress_ac_feasible_rate']}`)",
        f"- Best baseline: `{best_baseline['method']}` with `{best_baseline['ac_feasible_rate']}` (stress-only: `{best_baseline['stress_ac_feasible_rate']}`)",
        f"- `{proposed_name}` mean min voltage: `{proposed['mean_min_vm_pu']}` pu vs No-Plan `{noplan['mean_min_vm_pu']}` pu",
        f"- `{proposed_name}` mean max line loading: `{proposed['mean_max_line_loading_pct']}%` vs No-Plan `{noplan['mean_max_line_loading_pct']}%`",
        "",
        "## Summary Table",
        "",
        "| method | role | AC-feasible rate | stress feasible | mean min vm (pu) | mean max loading (%) | mean losses (MW) |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in summary:
        lines.append(
            f"| {row['method']} | {row['method_role']} | {row['ac_feasible_rate']} | {row['stress_ac_feasible_rate']} | {row['mean_min_vm_pu']} | {row['mean_max_line_loading_pct']} | {row['mean_losses_mw']} |"
        )
    lines.extend(
        [
            "",
            "## Mapping Assumptions (read before citing)",
            "",
            "Planning candidates live on aggregated SimBench subnet statistics, so plan",
            "*compositions* (action-kind counts) are mapped onto concrete MV networks with",
            "fixed, method-independent rules: reinforcement adds a parallel conductor on the",
            "most-loaded lines; storage connects at the weakest-voltage load buses",
            f"(+/-{STORAGE_P_FRACTION:.0%} of net load, discharging under load stress and charging",
            f"under DER stress); DER adds PV at the highest-load buses ({DER_P_FRACTION:.0%} of net",
            "load, scaled with the scenario DER factor); automation has no steady-state",
            "electrical effect. This validates whether each method's plan mix restores or",
            "preserves AC feasibility under stress; it is not a nodal siting/sizing study.",
            "",
            "## Interpretation",
            "",
            "- `ac_feasible` requires convergence, all bus voltages within [0.95, 1.05] pu,",
            "  and no line above 100% loading.",
            "- The peak_n1_outage scenario drops the highest-loaded line whose outage leaves",
            "  all buses supplied (radial spurs are skipped).",
            "- Scenario axis doubles as a sensitivity analysis over load growth and DER",
            "  penetration; per-scenario rows are in the results CSV.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    import sys

    sys.path.insert(0, str(ROOT / "src"))
    selected = tuple(arg for arg in sys.argv[1:] if arg in {"p3", "p4"}) or ("p3", "p4")
    for paper in selected:
        run_paper(paper)
