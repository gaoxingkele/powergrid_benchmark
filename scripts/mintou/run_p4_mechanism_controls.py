"""Run three targeted SHIELD-MOEA mechanism controls without replacing main evidence.

Outputs are deliberately isolated under ``real_shield_mechanism_controls_20260810``.
The experiment reuses the frozen P4 candidate construction, eight scenarios,
evaluation budget, population size, generations, seeds, normalization, and held-out
evaluation protocol. Only the named mechanism switch changes.
"""

from __future__ import annotations

import csv
import hashlib
import json
import time
from pathlib import Path

import numpy as np

from powergrid_benchmark import mintou_real_planning as mrp


RUN_ID = "real_shield_mechanism_controls_20260810"
METHODS = [
    mrp.MethodSpec(
        "Control-GAOnly", "mechanism_control", "shield",
        "SHIELD with GA variation only; screening and repair unchanged.",
        shield=mrp.ShieldConfig(variation_mode="ga"),
    ),
    mrp.MethodSpec(
        "Control-DEOnly", "mechanism_control", "shield",
        "SHIELD with binary-DE variation only; screening and repair unchanged.",
        shield=mrp.ShieldConfig(variation_mode="de"),
    ),
    mrp.MethodSpec(
        "Control-FixedWorstK", "mechanism_control", "shield",
        "Worst-K scenarios frozen after generation 1; hybrid variation unchanged.",
        shield=mrp.ShieldConfig(screen_dynamic=False),
    ),
]


def _existing_proposed_rows() -> list[dict[str, str]]:
    path = mrp.P4_ROOT / "evidence" / "runs" / "real_simbench_planning_results.csv"
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return [row for row in csv.DictReader(handle) if row["method"] == "SHIELD-MOEA"]


def main() -> None:
    hypervolume, _, holm = mrp._hv_helpers()
    all_candidates = mrp.build_candidates(mrp.load_subnet_stats())
    rows: list[dict[str, str]] = []

    for experiment, setup in mrp.P4_EXPERIMENTS.items():
        pool = mrp.experiment_pool(all_candidates, setup)
        eval_problem = mrp.PlanningProblem(
            pool, mrp.load_subnet_stats(), "p4", setup,
            mrp.make_scenarios(setup, "p4", evaluation=True),
        )
        search_problem = mrp.PlanningProblem(
            pool, mrp.load_subnet_stats(), "p4", setup,
            mrp.make_scenarios(setup, "p4", evaluation=False),
        )
        lo, hi = mrp.normalization_bounds(eval_problem)
        lo_w, hi_w = mrp.normalization_bounds(eval_problem, aggregate="worst")
        for spec in METHODS:
            for seed_index in range(mrp.N_SEEDS):
                digest = hashlib.sha1(f"p4|{experiment}|{spec.name}".encode()).hexdigest()
                seed = 200000 + seed_index * 7919 + int(digest[:6], 16) % 4096
                start = time.perf_counter()
                X = mrp.run_method(spec, search_problem, seed)
                front_x, front_f = mrp.feasible_front(eval_problem, X)
                hv = hypervolume(front_f, lo, hi)
                if front_x.shape[0]:
                    hv_w = hypervolume(eval_problem.objectives(front_x, aggregate="worst"), lo_w, hi_w)
                else:
                    hv_w = 0.0
                rows.append(
                    {
                        "paper": "p4", "experiment_id": experiment,
                        "method": spec.name, "method_role": spec.role,
                        "seed": str(seed_index), "hypervolume": f"{hv:.8f}",
                        "hypervolume_worst_case": f"{hv_w:.8f}",
                        "feasible_front_size": str(front_x.shape[0]),
                        "compromise_cost_index": "nan", "compromise_loss_index": "nan",
                        "compromise_voltage_risk": "nan", "compromise_hosting_capacity": "nan",
                        "compromise_reliability": "nan", "compromise_survivability": "nan",
                        "portfolio_size": "0", "hosting_shortfall": "nan",
                        "der_readiness_shortfall": "nan",
                        "runtime_s": f"{time.perf_counter() - start:.6f}",
                        "run_status": RUN_ID,
                    }
                )
        print(f"{experiment}: {len(METHODS) * mrp.N_SEEDS} control runs complete")

    combined = _existing_proposed_rows() + rows
    stats = mrp.statistics_table(combined, "p4", "SHIELD-MOEA", holm)
    run_path = mrp.P4_ROOT / "evidence" / "runs" / f"{RUN_ID}.csv"
    table_dir = mrp.P4_ROOT / "evidence" / "tables"
    mrp.write_csv_rows(run_path, rows)
    mrp.write_csv_rows(table_dir / f"{RUN_ID}_leaderboard.csv", mrp.aggregate(combined, "p4"))
    mrp.write_csv_rows(table_dir / f"{RUN_ID}_significance.csv", stats)
    config = {
        "run_id": RUN_ID,
        "main_evidence_replaced": False,
        "methods": {m.name: m.description for m in METHODS},
        "experiments": list(mrp.P4_EXPERIMENTS),
        "seeds": mrp.N_SEEDS,
        "population_size": mrp.POP_SIZE,
        "generations": mrp.N_GENERATIONS,
        "statistics": "two-sided Mann-Whitney U; Holm within each experiment over three controls",
    }
    (mrp.P4_ROOT / "src" / "configs" / f"{RUN_ID}.json").write_text(
        json.dumps(config, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
