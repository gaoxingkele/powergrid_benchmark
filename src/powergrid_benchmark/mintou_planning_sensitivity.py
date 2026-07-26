"""Parameter sensitivity study for mintou p3 (CARS-MODE) and p4 (SHIELD-MOEA).

Energies reviewers near-mandatorily ask how sensitive the headline comparison is
to algorithm parameter choices. This module sweeps the key parameters of each
proposed method on the paper's flagship experiment, re-using the *identical*
problem definition, scenario seeds, fixed normalization bounds, and feasible
non-dominated-front hypervolume evaluation from mintou_real_planning.py:

- p3 (CARS-MODE, experiment `base_distribution_planning`):
    * population size {20, 40, 60}
    * jDE F/CR resampling probability {0.05, 0.1, 0.2}
      (implementation note: CarsConfig originally hardcoded this probability at
      0.1 inside run_cars_mode; it is now exposed as CarsConfig.resample_prob
      with default 0.1, which reproduces the original behaviour bit-for-bit, so
      the main-experiment results are unaffected.)
- p4 (SHIELD-MOEA, experiment `deterministic_vs_scenario`):
    * population size {20, 40, 60}
    * scenario-screening worst-K, screen_k {2, 4, 8}
    * screening period, screen_every {3, 5, 10}

On the population-size axis the strongest baseline (pymoo NSGA-II, which shares
the same population-size constant) is re-run at each matched population size;
on proposed-method-only axes the NSGA-II reference at the default population
size (40) is used. 10 seeds per parameter point (sha1-stable seed pattern,
mirroring mintou_real_planning.run_paper); Mann-Whitney U per point.

POP_SIZE is a module-level constant consumed inside the run functions, so it is
monkeypatched per run and restored in a finally block.

Outputs per paper:
  evidence/tables/real_sensitivity_sweep.csv
  manuscript/figures/fig_sensitivity.png (300 dpi)
  manuscript/sensitivity_section.md
"""

from __future__ import annotations

import csv
import hashlib
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import powergrid_benchmark.mintou_real_planning as mrp  # noqa: E402
from powergrid_benchmark.mintou_real_planning import (  # noqa: E402
    CarsConfig,
    PlanningProblem,
    ShieldConfig,
    build_candidates,
    experiment_pool,
    feasible_front,
    load_subnet_stats,
    make_scenarios,
    normalization_bounds,
    run_cars_mode,
    run_shield_moea,
)

STATUS = "public_simbench_planning_sensitivity_v1"
N_SEEDS_FULL = 10
DEFAULT_POP = 40

POP_GRID = (20, 40, 60)
RESAMPLE_GRID = (0.05, 0.1, 0.2)
SCREEN_K_GRID = (2, 4, 8)
SCREEN_EVERY_GRID = (3, 5, 10)


@dataclass(frozen=True)
class SweepPoint:
    axis: str  # population_size | jde_resample_prob | screen_k | screen_every
    value: float
    pop_size: int
    cars: CarsConfig | None = None
    shield: ShieldConfig | None = None
    run_baseline: bool = False  # also run NSGA-II at this pop size


@dataclass(frozen=True)
class PaperSweep:
    paper: str
    root: Path
    experiment: str
    proposed: str
    points: tuple[SweepPoint, ...] = field(default_factory=tuple)


def p3_sweep() -> PaperSweep:
    points = [
        SweepPoint("population_size", p, p, cars=CarsConfig(), run_baseline=True)
        for p in POP_GRID
    ] + [
        SweepPoint("jde_resample_prob", r, DEFAULT_POP, cars=CarsConfig(resample_prob=r))
        for r in RESAMPLE_GRID
    ]
    return PaperSweep("p3", mrp.P3_ROOT, "base_distribution_planning", "CARS-MODE", tuple(points))


def p4_sweep() -> PaperSweep:
    points = (
        [
            SweepPoint("population_size", p, p, shield=ShieldConfig(), run_baseline=True)
            for p in POP_GRID
        ]
        + [
            SweepPoint("screen_k", k, DEFAULT_POP, shield=ShieldConfig(screen_k=k))
            for k in SCREEN_K_GRID
        ]
        + [
            SweepPoint("screen_every", e, DEFAULT_POP, shield=ShieldConfig(screen_every=e))
            for e in SCREEN_EVERY_GRID
        ]
    )
    return PaperSweep("p4", mrp.P4_ROOT, "deterministic_vs_scenario", "SHIELD-MOEA", tuple(points))


# ---------------------------------------------------------------------------
# Evaluation core (identical problem/normalization/HV as the main experiments)
# ---------------------------------------------------------------------------


def _seed_for(paper: str, experiment: str, method: str, label: str, seed_index: int) -> int:
    digest = hashlib.sha1(f"sens|{paper}|{experiment}|{method}|{label}".encode("utf-8")).hexdigest()
    return 300000 + seed_index * 7919 + int(digest[:6], 16) % 4096


def evaluate_point(
    paper: str,
    experiment: str,
    method: str,
    runner: str,  # cars | shield | nsga2
    point: SweepPoint,
    n_seeds: int,
    search_problem: PlanningProblem,
    eval_problem: PlanningProblem,
    lo: np.ndarray,
    hi: np.ndarray,
) -> np.ndarray:
    hypervolume, _, _ = mrp._hv_helpers()
    label = f"{point.axis}={point.value:g}|pop={point.pop_size}"
    hvs = np.empty(n_seeds)
    for seed_index in range(n_seeds):
        seed = _seed_for(paper, experiment, method, label, seed_index)
        old_pop = mrp.POP_SIZE
        try:
            mrp.POP_SIZE = point.pop_size
            if runner == "cars":
                X = run_cars_mode(search_problem, point.cars or CarsConfig(), seed)
            elif runner == "shield":
                X = run_shield_moea(search_problem, point.shield or ShieldConfig(), seed)
            else:
                X = mrp.run_pymoo(search_problem, "NSGA-II", seed)
        finally:
            mrp.POP_SIZE = old_pop
        _, front_F = feasible_front(eval_problem, X)
        hvs[seed_index] = hypervolume(front_F, lo, hi)
    return hvs


def run_sweep(sweep: PaperSweep, n_seeds: int) -> list[dict[str, str]]:
    from scipy.stats import mannwhitneyu

    setup = (mrp.P3_EXPERIMENTS if sweep.paper == "p3" else mrp.P4_EXPERIMENTS)[sweep.experiment]
    stats = load_subnet_stats()
    pool = experiment_pool(build_candidates(stats), setup)
    eval_scenarios = make_scenarios(setup, sweep.paper, evaluation=True)
    search_scenarios = make_scenarios(setup, sweep.paper, evaluation=False)
    eval_problem = PlanningProblem(pool, stats, sweep.paper, setup, eval_scenarios)
    search_problem = PlanningProblem(pool, stats, sweep.paper, setup, search_scenarios)
    lo, hi = normalization_bounds(eval_problem)
    runner = "cars" if sweep.paper == "p3" else "shield"

    # NSGA-II references keyed by pop size (matched pop on the population axis,
    # default pop elsewhere). Computed lazily, once per pop size.
    baseline_cache: dict[int, np.ndarray] = {}

    def baseline_at(pop_size: int) -> np.ndarray:
        if pop_size not in baseline_cache:
            ref_point = SweepPoint("population_size", pop_size, pop_size)
            baseline_cache[pop_size] = evaluate_point(
                sweep.paper, sweep.experiment, "NSGA-II", "nsga2", ref_point,
                n_seeds, search_problem, eval_problem, lo, hi,
            )
        return baseline_cache[pop_size]

    rows: list[dict[str, str]] = []
    for point in sweep.points:
        start = time.perf_counter()
        hvs = evaluate_point(
            sweep.paper, sweep.experiment, sweep.proposed, runner, point,
            n_seeds, search_problem, eval_problem, lo, hi,
        )
        ref_pop = point.pop_size if point.run_baseline else DEFAULT_POP
        ref = baseline_at(ref_pop)
        if np.allclose(hvs, ref):
            p_value = 1.0
        else:
            try:
                _, p_value = mannwhitneyu(hvs, ref, alternative="two-sided")
            except ValueError:
                p_value = 1.0
        elapsed = time.perf_counter() - start
        for method, values in ((sweep.proposed, hvs), ("NSGA-II", ref)):
            rows.append(
                {
                    "paper": sweep.paper,
                    "experiment_id": sweep.experiment,
                    "param_axis": point.axis,
                    "param_value": f"{point.value:g}",
                    "population_size": str(point.pop_size if method == sweep.proposed else ref_pop),
                    "method": method,
                    "method_role": "proposed" if method == sweep.proposed else "baseline_reference",
                    "n_seeds": str(n_seeds),
                    "mean_hypervolume": f"{values.mean():.8f}",
                    "std_hypervolume": f"{values.std(ddof=1):.8f}",
                    "min_hypervolume": f"{values.min():.8f}",
                    "max_hypervolume": f"{values.max():.8f}",
                    "hv_seed_values": ";".join(f"{v:.8f}" for v in values),
                    "mw_p_value_vs_reference": f"{p_value:.6g}",
                    "rank_vs_reference": (
                        "proposed_above" if values.mean() > ref.mean() else "proposed_below"
                    ) if method == sweep.proposed else "reference",
                    "source_status": STATUS,
                }
            )
        print(
            f"[{sweep.paper}] {point.axis}={point.value:g} pop={point.pop_size}: "
            f"{sweep.proposed} HV {hvs.mean():.5f}±{hvs.std(ddof=1):.5f} vs NSGA-II "
            f"{ref.mean():.5f} (p={p_value:.3g}, {elapsed:.1f}s)"
        )
    return rows


# ---------------------------------------------------------------------------
# Figure (dataviz reference palette, light mode, 300 dpi)
# ---------------------------------------------------------------------------

PALETTE = {
    "proposed": "#2a78d6",  # categorical slot 1 (blue)
    "baseline": "#1baf7a",  # categorical slot 2 (aqua)
    "surface": "#fcfcfb",
    "ink": "#0b0b0b",
    "ink2": "#52514e",
    "muted": "#898781",
    "grid": "#e1e0d9",
    "axisline": "#c3c2b7",
}

AXIS_LABELS = {
    "population_size": "Population size $N_p$",
    "jde_resample_prob": "jDE resampling probability $\\tau$",
    "screen_k": "Screened scenarios $K$",
    "screen_every": "Screening period $T_s$ (generations)",
}


def _points_frame(rows: list[dict[str, str]], axis: str, method: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    sel = [r for r in rows if r["param_axis"] == axis and r["method"] == method]
    sel = sorted(sel, key=lambda r: float(r["param_value"]))
    x = np.array([float(r["param_value"]) for r in sel])
    mean = np.array([float(r["mean_hypervolume"]) for r in sel])
    std = np.array([float(r["std_hypervolume"]) for r in sel])
    return x, mean, std


def make_figure(sweep: PaperSweep, rows: list[dict[str, str]], out_path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    axes_order = [p for p in dict.fromkeys(point.axis for point in sweep.points)]
    n_panels = len(axes_order)
    fig, axs = plt.subplots(1, n_panels, figsize=(4.0 * n_panels, 3.4), dpi=300, sharey=True)
    if n_panels == 1:
        axs = [axs]
    fig.patch.set_facecolor(PALETTE["surface"])

    for panel_idx, (ax, axis) in enumerate(zip(axs, axes_order)):
        ax.set_facecolor(PALETTE["surface"])
        x_p, m_p, s_p = _points_frame(rows, axis, sweep.proposed)
        x_b, m_b, s_b = _points_frame(rows, axis, "NSGA-II")
        matched = axis == "population_size"
        # proposed: line + error bars (mean +/- std over seeds)
        ax.errorbar(
            x_p, m_p, yerr=s_p, color=PALETTE["proposed"], linewidth=2.0,
            marker="o", markersize=5.5, capsize=3.0, elinewidth=1.2,
            label=sweep.proposed, zorder=3,
        )
        if matched:
            ax.errorbar(
                x_b, m_b, yerr=s_b, color=PALETTE["baseline"], linewidth=2.0,
                linestyle="--", marker="s", markersize=5.0, capsize=3.0,
                elinewidth=1.2, label="NSGA-II (matched $N_p$)", zorder=2,
            )
        else:
            ax.axhline(
                m_b.mean(), color=PALETTE["baseline"], linewidth=2.0, linestyle="--",
                label=f"NSGA-II ($N_p$={DEFAULT_POP})", zorder=2,
            )
        ax.set_xlabel(AXIS_LABELS[axis], fontsize=9, color=PALETTE["ink2"])
        if panel_idx == 0:
            ax.set_ylabel("Hypervolume (fixed normalization)", fontsize=9, color=PALETTE["ink2"])
        ax.set_xticks(x_p)
        ax.tick_params(colors=PALETTE["muted"], labelsize=8)
        ax.grid(True, axis="y", color=PALETTE["grid"], linewidth=0.7)
        ax.set_axisbelow(True)
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)
        for spine in ("left", "bottom"):
            ax.spines[spine].set_color(PALETTE["axisline"])
        ax.set_title(f"({chr(97 + panel_idx)})", loc="left", fontsize=10, color=PALETTE["ink"])

    handles, labels = axs[0].get_legend_handles_labels()
    if len(axs) > 1:
        extra_h, extra_l = axs[-1].get_legend_handles_labels()
        for h, l in zip(extra_h, extra_l):
            if l not in labels:
                handles.append(h)
                labels.append(l)
    fig.legend(
        handles, labels, loc="lower center", ncol=len(labels), frameon=False,
        fontsize=8, bbox_to_anchor=(0.5, -0.02), labelcolor=PALETTE["ink2"],
    )
    fig.suptitle(
        f"{sweep.proposed} parameter sensitivity - {sweep.experiment.replace('_', ' ')} (mean $\\pm$ std over seeds)",
        fontsize=10, color=PALETTE["ink"],
    )
    fig.tight_layout(rect=(0, 0.06, 1, 0.94))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=300, facecolor=PALETTE["surface"], bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Manuscript section (numbers interpolated from the sweep rows)
# ---------------------------------------------------------------------------

AXIS_PROSE = {
    "population_size": "population size $N_p$",
    "jde_resample_prob": "jDE resampling probability $\\tau$",
    "screen_k": "number of screened worst-case scenarios $K$",
    "screen_every": "scenario-screening period $T_s$",
}

DEFAULT_VALUE = {
    "population_size": DEFAULT_POP,
    "jde_resample_prob": 0.1,
    "screen_k": 4,
    "screen_every": 5,
}


def _fmt(v: float) -> str:
    return f"{v:.4f}"


def section_markdown(sweep: PaperSweep, rows: list[dict[str, str]], n_seeds: int) -> str:
    axes_order = [p for p in dict.fromkeys(point.axis for point in sweep.points)]
    proposed_rows = [r for r in rows if r["method"] == sweep.proposed]
    flips = [r for r in proposed_rows if r["rank_vs_reference"] == "proposed_below"]

    # spread of the proposed method's mean HV across all parameter points,
    # relative to the default-configuration point
    default_rows = {
        axis: next(
            r for r in proposed_rows
            if r["param_axis"] == axis and float(r["param_value"]) == DEFAULT_VALUE[axis]
        )
        for axis in axes_order
    }
    default_hv = float(default_rows[axes_order[0]]["mean_hypervolume"])
    means = np.array([float(r["mean_hypervolume"]) for r in proposed_rows])
    spread_pct = (means.max() - means.min()) / default_hv * 100

    if sweep.paper == "p3":
        method_prose = (
            "CARS-MODE exposes two influential parameters: the population size $N_p$ "
            "(shared by all population-based competitors) and the jDE resampling "
            "probability $\\tau$, i.e., the per-individual probability of redrawing the "
            "self-adaptive scale factor $F$ and crossover rate $CR$ in each generation. "
            "The remaining mechanisms (two-strategy pool, budget repair, crowding "
            "diversity) are binary switches already covered by the ablation study. "
            "Since the original implementation hardcoded $\\tau=0.1$, we exposed it as a "
            "configuration parameter whose default reproduces the main-experiment "
            "behaviour exactly, and swept it over $\\{0.05, 0.1, 0.2\\}$; $N_p$ was swept "
            "over $\\{20, 40, 60\\}$ (default 40)."
        )
        fig_desc = "panels (a) and (b)"
    else:
        method_prose = (
            "SHIELD-MOEA exposes three influential parameters: the population size "
            "$N_p$ (shared by all population-based competitors), the number of "
            "worst-case scenarios retained during screening $K$, and the screening "
            "period $T_s$ (a re-screen every $T_s$ generations). We swept "
            "$N_p \\in \\{20, 40, 60\\}$ (default 40), $K \\in \\{2, 4, 8\\}$ (default 4), and "
            "$T_s \\in \\{3, 5, 10\\}$ (default 5). The final evaluation always uses the "
            "full disjoint-seed scenario set, so screening parameters can only affect "
            "the search, never the scoring."
        )
        fig_desc = "panels (a)-(c)"

    lines = [
        "## Parameter Sensitivity Analysis",
        "",
        "<!-- Auto-generated by src/powergrid_benchmark/mintou_planning_sensitivity.py"
        f" (status: {STATUS}). Numbers match evidence/tables/real_sensitivity_sweep.csv. -->",
        "",
        f"To verify that the comparison in the {sweep.experiment.replace('_', ' ')} "
        "experiment does not hinge on a fortunate parameter choice, we performed a "
        "one-at-a-time parameter sweep around the default configuration. "
        + method_prose,
        "",
        f"Each parameter point was re-run with {n_seeds} independent seeds under the "
        "protocol of the main experiments: identical SimBench-derived problem "
        "instance, identical search/evaluation scenario seeds, and the hypervolume "
        "of the feasible non-dominated front computed under the same fixed, "
        "method-independent normalization bounds, so hypervolumes are directly "
        "comparable across parameter points. On the population-size axis the "
        "strongest baseline (NSGA-II) was re-run at each matched population size; "
        "for the method-specific parameters, which do not affect the baselines, the "
        f"NSGA-II reference at the default $N_p={DEFAULT_POP}$ is shown. "
        "Two-sided Mann-Whitney U tests compare the proposed method against the "
        "corresponding NSGA-II reference at every point.",
        "",
        f"Figure \\ref{{fig:sensitivity}} ({fig_desc}) and Table "
        "\\ref{tab:sensitivity} summarize the sweep.",
        "",
        "| Parameter | Value | "
        f"{sweep.proposed} HV (mean $\\pm$ std) | NSGA-II reference HV | $p$ (MWU) |",
        "|---|---|---|---|---|",
    ]
    for axis in axes_order:
        p_rows = sorted(
            (r for r in proposed_rows if r["param_axis"] == axis),
            key=lambda r: float(r["param_value"]),
        )
        for r in p_rows:
            ref = next(
                b for b in rows
                if b["param_axis"] == axis and b["method"] == "NSGA-II"
                and b["param_value"] == r["param_value"]
            )
            default_mark = " (default)" if float(r["param_value"]) == DEFAULT_VALUE[axis] else ""
            lines.append(
                f"| {AXIS_PROSE[axis]} | {r['param_value']}{default_mark} | "
                f"{_fmt(float(r['mean_hypervolume']))} $\\pm$ {_fmt(float(r['std_hypervolume']))} | "
                f"{_fmt(float(ref['mean_hypervolume']))} | {r['mw_p_value_vs_reference']} |"
            )
    lines.append("")

    # per-axis observations
    for axis in axes_order:
        p_rows = sorted(
            (r for r in proposed_rows if r["param_axis"] == axis),
            key=lambda r: float(r["param_value"]),
        )
        vals = [float(r["param_value"]) for r in p_rows]
        m = [float(r["mean_hypervolume"]) for r in p_rows]
        rel = (max(m) - min(m)) / default_hv * 100
        best_v = vals[int(np.argmax(m))]
        lines.append(
            f"Across the {AXIS_PROSE[axis]} axis, the mean hypervolume of "
            f"{sweep.proposed} varies between {_fmt(min(m))} and {_fmt(max(m))} "
            f"(a spread of {rel:.1f}% of the default-configuration value), with the "
            f"best mean at {AXIS_PROSE[axis].split('$')[0].strip()} = {best_v:g}."
        )
        lines.append("")

    if flips:
        flip_desc = "; ".join(
            f"{AXIS_PROSE[r['param_axis']]} = {r['param_value']} "
            f"({sweep.proposed} {_fmt(float(r['mean_hypervolume']))} vs NSGA-II "
            f"{_fmt(float(next(b for b in rows if b['param_axis'] == r['param_axis'] and b['method'] == 'NSGA-II' and b['param_value'] == r['param_value'])['mean_hypervolume']))}, "
            f"$p$ = {r['mw_p_value_vs_reference']})"
            for r in flips
        )
        conclusion = (
            f"**Rank reversals were observed and must be reported:** at {flip_desc}, "
            f"the mean hypervolume of {sweep.proposed} falls below the NSGA-II "
            "reference. The main-experiment conclusion therefore holds for the "
            "default configuration but is *not* uniformly robust across the swept "
            "range, and the affected parameter(s) should be kept at or near their "
            "default values in practice."
        )
    else:
        min_gap = min(
            float(r["mean_hypervolume"])
            - float(next(
                b for b in rows
                if b["param_axis"] == r["param_axis"] and b["method"] == "NSGA-II"
                and b["param_value"] == r["param_value"]
            )["mean_hypervolume"])
            for r in proposed_rows
        )
        not_significant = [
            r for r in proposed_rows if float(r["mw_p_value_vs_reference"]) >= 0.05
        ]
        if not_significant:
            ns_desc = "; ".join(
                f"{AXIS_PROSE[r['param_axis']]} = {r['param_value']} "
                f"($p$ = {r['mw_p_value_vs_reference']})"
                for r in not_significant
            )
            ns_sentence = (
                f" The advantage retains its sign but loses statistical "
                f"significance at the 0.05 level at {ns_desc}, which we report "
                "for completeness."
            )
        else:
            ns_sentence = (
                " The advantage is statistically significant (two-sided "
                "Mann-Whitney U, $p < 0.05$) at every point."
            )
        conclusion = (
            f"At every parameter point the mean hypervolume of {sweep.proposed} "
            "remains above the corresponding NSGA-II reference (smallest margin "
            f"{_fmt(min_gap)} in absolute hypervolume), i.e., no rank reversal "
            f"occurs anywhere in the swept range.{ns_sentence} "
            "The total spread of the proposed "
            f"method's mean hypervolume across all {len(proposed_rows)} parameter "
            f"points is {spread_pct:.1f}% of the default-configuration value. "
            "We conclude that the main comparative result is robust to the tested "
            "parameter choices, and that the defaults "
            + (
                "($N_p = 40$, $\\tau = 0.1$)"
                if sweep.paper == "p3"
                else "($N_p = 40$, $K = 4$, $T_s = 5$)"
            )
            + " sit in a flat region of the response rather than at a tuned peak."
        )
    lines.extend([conclusion, ""])
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


def write_csv_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def run_paper_sensitivity(sweep: PaperSweep, n_seeds: int, smoke: bool) -> list[dict[str, str]]:
    rows = run_sweep(sweep, n_seeds)
    suffix = "_smoke" if smoke else ""
    csv_path = sweep.root / "evidence" / "tables" / f"real_sensitivity_sweep{suffix}.csv"
    write_csv_rows(csv_path, rows)
    fig_path = sweep.root / "manuscript" / "figures" / f"fig_sensitivity{suffix}.png"
    make_figure(sweep, rows, fig_path)
    if not smoke:
        section_path = sweep.root / "manuscript" / "sensitivity_section.md"
        section_path.parent.mkdir(parents=True, exist_ok=True)
        section_path.write_text(section_markdown(sweep, rows, n_seeds), encoding="utf-8")
    print(f"[{sweep.paper}] sensitivity outputs written under {sweep.root}")
    return rows


if __name__ == "__main__":
    smoke = "--smoke" in sys.argv
    n_seeds = 2 if smoke else N_SEEDS_FULL
    selected = tuple(arg for arg in sys.argv[1:] if arg in {"p3", "p4"}) or ("p3", "p4")
    sweeps = {"p3": p3_sweep(), "p4": p4_sweep()}
    for paper in selected:
        run_paper_sensitivity(sweeps[paper], n_seeds, smoke)
