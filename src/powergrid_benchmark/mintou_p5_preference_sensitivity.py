"""Pre-registered P5 preference-family and budget sensitivity extension."""

from __future__ import annotations

import csv
import hashlib
import json
import time
from pathlib import Path
import sys

import numpy as np
from scipy.stats import mannwhitneyu

ROOT = Path(__file__).resolve().parents[2]
if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "src"))

from powergrid_benchmark import mintou_real_project_review as core

STATUS = "public_p5_preference_budget_v1_rnsga2"
MULTIPLIERS = (0.75, 1.00, 1.25)
METHODS = ("TRACE-MOEA", "R-NSGA-II", "NSGA-II")
EXPERIMENT = "preference_aware_support"


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    candidates = core.build_candidates()
    weights = core.experiment_weights(EXPERIMENT, "p5")
    trace_spec = next(method for method in core.p5_methods() if method.name == "TRACE-MOEA")
    rows: list[dict[str, str]] = []
    for multiplier in MULTIPLIERS:
        problem = core.PortfolioProblem(candidates, "p5", 1160.0 * multiplier)
        lo, hi = core.normalization_bounds(problem)
        for method_name in METHODS:
            for seed_index in range(core.N_SEEDS):
                digest = hashlib.sha1(f"p5-pref-budget|{multiplier}|{method_name}".encode()).hexdigest()
                seed = 310000 + seed_index * 7919 + int(digest[:6], 16) % 4096
                start = time.perf_counter()
                if method_name == "TRACE-MOEA":
                    result = core.run_custom_ea(problem, trace_spec.engine or core.EngineConfig(), seed, seed_weights=weights)
                    X = result.population
                    trace_count = len(result.trace_events)
                else:
                    X = core.run_pymoo_baseline(problem, method_name, seed, weights=weights)
                    trace_count = 0
                _, front = core.feasible_front(problem, X)
                rows.append(
                    {
                        "experiment": EXPERIMENT,
                        "budget_multiplier": f"{multiplier:.2f}",
                        "method": method_name,
                        "seed": str(seed_index),
                        "hypervolume": f"{core.hypervolume(front, lo, hi):.8f}",
                        "preference_achievement_distance": f"{core.achievement_distance(front, problem, weights):.8f}",
                        "feasible_front_size": str(front.shape[0]),
                        "trace_event_count": str(trace_count),
                        "runtime_s": f"{time.perf_counter() - start:.6f}",
                        "source_status": STATUS,
                    }
                )
            print(f"[p5-pref] budget {multiplier:.2f} {method_name}: done")

    board: list[dict[str, str]] = []
    stats: list[dict[str, str]] = []
    for multiplier in MULTIPLIERS:
        mult = f"{multiplier:.2f}"
        group = [row for row in rows if row["budget_multiplier"] == mult]
        proposed = [float(row["hypervolume"]) for row in group if row["method"] == "TRACE-MOEA"]
        pvals: list[float] = []
        pending: list[dict[str, str]] = []
        for method_name in METHODS:
            values = [row for row in group if row["method"] == method_name]
            board.append(
                {
                    "budget_multiplier": mult,
                    "method": method_name,
                    "mean_hypervolume": f"{np.mean([float(row['hypervolume']) for row in values]):.8f}",
                    "std_hypervolume": f"{np.std([float(row['hypervolume']) for row in values], ddof=1):.8f}",
                    "mean_preference_achievement_distance": f"{np.mean([float(row['preference_achievement_distance']) for row in values]):.8f}",
                    "mean_runtime_s": f"{np.mean([float(row['runtime_s']) for row in values]):.6f}",
                    "runs": str(len(values)),
                }
            )
            if method_name == "TRACE-MOEA":
                continue
            opponent = [float(row["hypervolume"]) for row in values]
            u_stat, p_value = mannwhitneyu(proposed, opponent, alternative="two-sided")
            pvals.append(float(p_value))
            pending.append(
                {
                    "budget_multiplier": mult,
                    "comparison": f"TRACE-MOEA vs {method_name}",
                    "mean_diff": f"{np.mean(proposed) - np.mean(opponent):.8f}",
                    "u_statistic": f"{u_stat:.2f}",
                    "p_value": f"{p_value:.8g}",
                }
            )
        corrected = core.holm_correction(pvals)
        for row, adjusted in zip(pending, corrected):
            row["p_holm"] = f"{adjusted:.8g}"
            row["significant_005_holm"] = str(adjusted < 0.05)
            stats.append(row)

    root = core.P5_ROOT
    _write_csv(root / "evidence" / "runs" / "real_preference_budget_v1_results.csv", rows)
    _write_csv(root / "evidence" / "tables" / "real_preference_budget_v1_leaderboard.csv", board)
    _write_csv(root / "evidence" / "tables" / "real_preference_budget_v1_significance.csv", stats)
    (root / "src" / "configs" / "real_preference_budget_v1_config.json").write_text(
        json.dumps(
            {
                "experiment": EXPERIMENT,
                "budget_multipliers": MULTIPLIERS,
                "methods": METHODS,
                "seeds": core.N_SEEDS,
                "population_size": core.POP_SIZE,
                "generations": core.N_GENERATIONS,
                "primary_metric": "standard feasible-front hypervolume",
                "secondary_metric": "normalized achievement distance to the fixed scenario reference point",
                "status": STATUS,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"[p5-pref] complete: {len(rows)} runs")


if __name__ == "__main__":
    main()
