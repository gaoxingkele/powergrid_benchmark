"""External-consistency backtest for mintou p5/p6 against NERC-documented failure modes.

First rung of the external-ground-truth ladder decided on 2026-07-14
(NERC rule backtest -> MISO MTEP historical backtest -> expert labels).

Design guards against construct circularity: the candidate pool used by the
published experiments was NERC-adjusted at the KIND level (renewable/storage
kinds received global boosts), so a naive "prioritize kinds with documented
events" rule would partially validate the construction rather than the methods.
Therefore:

- The rule score uses the RAW candidate builders (`build_rts_candidates` /
  `build_simbench_candidates`, i.e. BEFORE the NERC adjustment step), so the
  zone-stress component is fully NERC-independent physics from RTS/SimBench.
- NERC report topics only set kind-level weights, and the residual kind-level
  overlap with the constructed pool is disclosed in the generated analysis as
  an explicit boundary (the MISO MTEP backtest remains the true external
  anchor).

Rule: priority(candidate) = topic_weight(kind) * stress_percentile(candidate),
where topic weights come from keyword counts over the cached NERC manifest
(winter/transmission events -> grid reinforcement & automation kinds; IBR
events -> renewable support; battery mentions -> storage flexibility), and the
stress percentile ranks the candidate's raw reliability attribute within the
pool.

Alignment metrics per method (selection frequency over 10 seeded compromise
portfolios, deterministic seeds identical to the published v2 runs):
- priority_capture: freq-weighted mean rule score of selected candidates
  divided by the pool mean (>1 = method concentrates on documented-risk areas)
- kendall_tau between selection frequency and rule score (with p-value)
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

if __name__ == "__main__":
    import sys

    sys.path.insert(0, str(ROOT / "src"))

import numpy as np
from scipy.stats import kendalltau

from powergrid_benchmark.mintou_real_project_review import (  # noqa: E402
    P5_ROOT,
    P6_ROOT,
    PortfolioProblem,
    budget_for,
    build_candidates,
    build_rts_candidates,
    build_simbench_candidates,
    experiment_pool,
    feasible_front,
    load_nerc_evidence,
    normalization_bounds,
    p5_methods,
    p6_methods,
    run_method,
)

STATUS = "public_nerc_rule_backtest_v1"
N_SEEDS = 10
EXPERIMENTS = {
    "p5": ("benchmark_portfolio_optimization", "reliability_driven_review"),
    "p6": ("budget_constrained_selection", "reliability_prioritized_review"),
}
RELIABILITY_KINDS = ("transmission_reinforcement", "reliability_automation", "protection_automation", "distribution_reinforcement")


def rule_scores(pool_cids: list[str]) -> dict[str, float]:
    """NERC-topic kind weights x NERC-independent stress percentile."""
    nerc = load_nerc_evidence()
    winter_grid = nerc["winter_mentions"] + nerc["event_reports"]
    ibr = nerc["ibr_mentions"]
    battery = nerc["battery_mentions"]
    total = max(1.0, winter_grid + ibr + battery)
    kind_weight = {kind: winter_grid / total for kind in RELIABILITY_KINDS}
    kind_weight["renewable_support"] = ibr / total
    kind_weight["storage_flexibility"] = battery / total

    raw = build_rts_candidates() + build_simbench_candidates()
    raw_by_cid = {c.cid: c for c in raw}
    reliabilities = np.array([raw_by_cid[cid].reliability for cid in pool_cids if cid in raw_by_cid])
    scores: dict[str, float] = {}
    for cid in pool_cids:
        c = raw_by_cid[cid]
        pct = float((reliabilities <= c.reliability).mean())
        scores[cid] = kind_weight.get(c.kind, 0.0) * pct
    return scores


def compromise_selection_frequency(paper: str, experiment: str) -> tuple[dict[str, dict[str, float]], list[str]]:
    """Per method: candidate selection frequency across N_SEEDS compromise solutions."""
    all_candidates = build_candidates()
    pool = experiment_pool(experiment, all_candidates)
    budget = budget_for(experiment, paper)
    problem = PortfolioProblem(pool, paper, budget)
    lo, hi = normalization_bounds(problem)
    methods = p5_methods() if paper == "p5" else p6_methods()
    freq: dict[str, dict[str, float]] = {}
    for spec in methods:
        counts: dict[str, float] = {c.cid: 0.0 for c in pool}
        for seed_index in range(N_SEEDS):
            digest = hashlib.sha1(f"{paper}|{experiment}|{spec.name}".encode("utf-8")).hexdigest()
            seed = 100000 + seed_index * 7919 + int(digest[:6], 16) % 4096
            X, eval_problem, _, _ = run_method(spec, pool, paper, experiment, seed)
            front_X, front_F = feasible_front(eval_problem, X)
            if front_X.shape[0] == 0:
                continue
            norm = (front_F - lo) / np.maximum(hi - lo, 1e-9)
            best = front_X[int(np.argmin(norm.sum(axis=1)))]
            # map through the (possibly pool-transformed) eval problem's candidates
            for i in np.where(best > 0)[0]:
                cid = eval_problem.candidates[int(i)].cid
                if cid in counts:
                    counts[cid] += 1.0
        freq[spec.name] = {cid: value / N_SEEDS for cid, value in counts.items()}
    return freq, [c.cid for c in pool]


def run_paper(paper: str) -> None:
    root = P5_ROOT if paper == "p5" else P6_ROOT
    methods = p5_methods() if paper == "p5" else p6_methods()
    roles = {m.name: m.role for m in methods}
    rows: list[dict[str, str]] = []
    for experiment in EXPERIMENTS[paper]:
        freq, pool_cids = compromise_selection_frequency(paper, experiment)
        scores = rule_scores(pool_cids)
        score_vec = np.array([scores[cid] for cid in pool_cids])
        pool_mean = float(score_vec.mean())
        for method, selection in freq.items():
            sel_vec = np.array([selection[cid] for cid in pool_cids])
            if sel_vec.sum() <= 0:
                capture, tau, p_value = float("nan"), float("nan"), float("nan")
            else:
                capture = float((sel_vec * score_vec).sum() / sel_vec.sum() / max(1e-12, pool_mean))
                tau, p_value = kendalltau(sel_vec, score_vec)
            rows.append(
                {
                    "paper": paper,
                    "experiment_id": experiment,
                    "method": method,
                    "method_role": roles[method],
                    "n_seeds": str(N_SEEDS),
                    "priority_capture_ratio": f"{capture:.6f}",
                    "kendall_tau": f"{tau:.6f}",
                    "kendall_p": f"{p_value:.6g}",
                    "mean_portfolio_size": f"{np.array([v for v in selection.values()]).sum():.2f}",
                    "source_status": STATUS,
                }
            )
        print(f"[{paper}] {experiment}: backtest done")

    rows.sort(key=lambda r: (r["experiment_id"], -float(r["priority_capture_ratio"]) if r["priority_capture_ratio"] != "nan" else 0))
    table_dir = root / "evidence" / "tables"
    table_dir.mkdir(parents=True, exist_ok=True)
    with (table_dir / "real_nerc_rule_backtest.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    proposed_name = "TRACE-MOEA" if paper == "p5" else "BiLo-NSGA"
    lines = [
        f"# NERC Rule-Based External Consistency Backtest - {'P5 TRACE-MOEA' if paper == 'p5' else 'P6 BiLo-NSGA'}",
        "",
        f"Status: `{STATUS}`. First rung of the external-validity ladder",
        "(NERC rule backtest -> MISO MTEP historical backtest -> expert labels).",
        "",
        "Rule: priority(candidate) = NERC-topic kind weight x NERC-independent",
        "stress percentile (raw candidate attributes BEFORE the pool's NERC",
        "adjustment). Alignment measured against each method's selection",
        f"frequency over {N_SEEDS} seeded compromise portfolios (published-run seeds).",
        "",
        "## Results",
        "",
        "| experiment | method | role | priority capture | Kendall tau | p |",
        "|---|---|---|---|---|---|",
    ]
    for r in rows:
        marker = " **" if r["method"] == proposed_name else " "
        lines.append(
            f"|{marker}{r['experiment_id']} | {r['method']} | {r['method_role']} | {r['priority_capture_ratio']} | {r['kendall_tau']} | {r['kendall_p']} |"
        )
    lines.extend(
        [
            "",
            "## Boundary (read before citing)",
            "",
            "- This is an external-CONSISTENCY check, not ground truth: it asks whether",
            "  portfolios concentrate on candidates whose kind and physical stress match",
            "  failure modes documented in the cached NERC reports.",
            "- Residual construct overlap: the experiment pool's candidate attributes were",
            "  NERC-adjusted at the kind level during construction, so kind weights are",
            "  not fully independent of the pool. The stress-percentile component IS",
            "  independent (raw RTS/SimBench physics). The MISO MTEP historical backtest",
            "  remains the required true external anchor before manuscript validity",
            "  claims.",
            "- priority_capture > 1 means the method over-samples documented-risk",
            "  candidates relative to a uniform pool draw.",
        ]
    )
    (root / "evidence" / "runs" / "real_nerc_rule_backtest_analysis.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (root / "src" / "configs" / "real_nerc_rule_backtest_config.json").write_text(
        json.dumps(
            {
                "experiments": list(EXPERIMENTS[paper]),
                "n_seeds": N_SEEDS,
                "rule": "NERC topic kind-weights x NERC-independent stress percentile (raw builders)",
                "metrics": ["priority_capture_ratio", "kendall_tau"],
                "ladder": ["nerc_rule_backtest (this)", "miso_mtep_historical_backtest (next)", "expert_labels (optional)"],
                "status": STATUS,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"[{paper}] backtest complete")


if __name__ == "__main__":
    for paper in ("p5", "p6"):
        run_paper(paper)
