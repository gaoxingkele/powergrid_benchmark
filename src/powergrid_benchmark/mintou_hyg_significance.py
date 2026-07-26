"""p2 v7 evidence: 10-seed significance tests + the Ausgrid hierarchical dataset.

Closes the component-evidence gap left by the v6 neural upgrade: with 3 seeds
the hyperbolic-graph ablations were within seed noise. This module

1. extends the decision-relevant model set (the 6 neural HyG variants + the MLP
   baseline, which is the strongest external baseline everywhere) to 10 seeds
   on OPSD and SimBench (the original 3 seed runs are merged in unchanged), and
2. adds the Ausgrid solar-home dataset as a genuinely HIERARCHICAL third
   benchmark: hourly GC (general consumption) series for the 12 highest-energy
   customers with complete 3-year records, 4 postcode-region aggregates over
   all complete customers, and the system total (17 series, 2010-07..2013-06,
   day-ahead 24h horizon only), and
3. runs Mann-Whitney U tests (proposed vs every ablation, proposed vs MLP)
   with Holm correction per dataset/horizon on each dataset's primary metric
   (MAPE for OPSD; normalized MAE for SimBench and Ausgrid, whose customer
   series have near-zero denominators).

Protocol is unchanged from v5/v6 (same splits, full test sets, Adam/MSE,
temporal early stopping). Ausgrid multi-series windows are gathered lazily per
batch because the full tensor would not fit in memory.

Stages (run separately, parallelizable): --stage opsd | simbench | ausgrid,
then --stage report to build the significance tables and analysis.
"""

from __future__ import annotations

import csv
import json
import math
import statistics
import time
import zipfile
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

if __name__ == "__main__":
    import sys

    sys.path.insert(0, str(ROOT / "src"))

from powergrid_benchmark.mintou_hyg_neural import (  # noqa: E402
    EPOCHS as HYG_EPOCHS,
    VARIANTS,
    make_hyg_model,
    multi_series_tensors,
)
from powergrid_benchmark.mintou_neural_forecasting import (  # noqa: E402
    BATCH_SIZE,
    SEEDS as BASE_SEEDS,
    TRAIN_STRIDE,
    WINDOW,
    build_tensors,
    denormalize,
    make_model,
)
from powergrid_benchmark.mintou_neural_forecasting import (  # noqa: E402
    train_and_predict as baseline_train_and_predict,
)
from powergrid_benchmark.mintou_real_load_forecasting import (  # noqa: E402
    P2_ROOT,
    Sample,
    evaluate_predictions,
    parse_opsd,
    parse_simbench,
    samples_for,
    write_csv,
)

AUSGRID_ZIP = ROOT / "data" / "public_datasets" / "renewable_weather" / "ausgrid_solar_home" / "Ausgrid_solar_home_data.zip"
AUSGRID_CACHE = AUSGRID_ZIP.parent / "processed_hourly_gc_hierarchy.json"
AUSGRID_YEAR_FILES = ("Solar home 2010-2011.csv", "Solar home 2011-2012.csv", "Solar home 2012-2013.csv")
AUSGRID_N_CUSTOMERS = 12
AUSGRID_N_REGIONS = 4
AUSGRID_HORIZONS = (24,)
AUSGRID_TRAIN_STRIDE = 6
AUSGRID_HYG_EPOCHS = 10

EXTRA_SEEDS = (59, 71, 83, 97, 109, 127, 139)
ALL_SEEDS = tuple(BASE_SEEDS) + EXTRA_SEEDS
V7_RUN_VERSION = "public_data_benchmark_v7_seed_significance_ausgrid"

# Ausgrid mixes customer (~1.5 kWh) and system (~200 kWh) scales, so range-
# normalized MAE is dominated by the large series and customer-level MAPE has
# near-zero denominators; sMAPE is scale-free and robust to both.
PRIMARY_METRIC = {"opsd": "mape", "simbench": "normalized_mae", "ausgrid": "smape"}


# ---------------------------------------------------------------------------
# Ausgrid hierarchical dataset
# ---------------------------------------------------------------------------


def parse_ausgrid() -> tuple[list[str], dict[str, list[float]]]:
    """Hourly GC series: 12 top-energy complete customers, 4 postcode-region
    aggregates over all complete customers, 1 system total. Cached to JSON."""
    if AUSGRID_CACHE.exists():
        payload = json.loads(AUSGRID_CACHE.read_text(encoding="utf-8"))
        return payload["timestamps"], payload["series"]

    per_customer: dict[int, dict[str, list[float]]] = {}
    postcode: dict[int, str] = {}
    for name in AUSGRID_YEAR_FILES:
        with zipfile.ZipFile(AUSGRID_ZIP).open(name) as handle:
            text = (line.decode("utf-8", errors="ignore") for line in handle)
            reader = csv.reader(text)
            next(reader)  # disclaimer line
            header = next(reader)
            date_col = header.index("date")
            first_val = date_col + 1
            for row in reader:
                if len(row) <= first_val or row[3] != "GC":
                    continue
                try:
                    customer = int(row[0])
                except ValueError:
                    continue
                postcode[customer] = row[2]
                day_vals: list[float] = []
                ok = True
                for k in range(24):
                    try:
                        day_vals.append(float(row[first_val + 2 * k] or 0) + float(row[first_val + 2 * k + 1] or 0))
                    except (ValueError, IndexError):
                        ok = False
                        break
                if ok:
                    per_customer.setdefault(customer, {})[row[date_col]] = day_vals

    max_days = max(len(days) for days in per_customer.values())
    complete = {c: days for c, days in per_customer.items() if len(days) == max_days}
    if len(complete) < AUSGRID_N_CUSTOMERS + AUSGRID_N_REGIONS:
        raise RuntimeError(f"only {len(complete)} complete Ausgrid customers")

    def day_key(raw: str) -> datetime:
        for fmt in ("%d-%b-%y", "%d/%m/%Y", "%d/%m/%y"):
            try:
                return datetime.strptime(raw, fmt)
            except ValueError:
                continue
        raise ValueError(f"unrecognized Ausgrid date: {raw!r}")

    dates = sorted(next(iter(complete.values())).keys(), key=day_key)
    # verify contiguity
    for a, b in zip(dates, dates[1:]):
        if day_key(b) - day_key(a) != timedelta(days=1):
            raise RuntimeError(f"date gap between {a} and {b}")

    totals = {c: sum(sum(v) for v in days.values()) for c, days in complete.items()}
    top_customers = sorted(complete, key=lambda c: -totals[c])[:AUSGRID_N_CUSTOMERS]
    region_codes = sorted({postcode[c] for c in complete})
    bucket_size = math.ceil(len(region_codes) / AUSGRID_N_REGIONS)
    region_of = {code: f"region{r // bucket_size + 1}" for r, code in enumerate(region_codes)}

    timestamps: list[str] = []
    series: dict[str, list[float]] = {f"customer{c}": [] for c in top_customers}
    for r in range(AUSGRID_N_REGIONS):
        series[f"region{r + 1}"] = []
    series["system_total"] = []
    for date in dates:
        for hour in range(24):
            timestamps.append(f"{day_key(date).date()}T{hour:02d}:00")
            total = 0.0
            region_sum = [0.0] * AUSGRID_N_REGIONS
            for c, days in complete.items():
                value = days[date][hour]
                total += value
                region_sum[int(region_of[postcode[c]][6:]) - 1] += value
                if c in top_customers:
                    series[f"customer{c}"].append(value)
            for r in range(AUSGRID_N_REGIONS):
                series[f"region{r + 1}"].append(region_sum[r])
            series["system_total"].append(total)

    AUSGRID_CACHE.write_text(
        json.dumps({"timestamps": timestamps, "series": series, "n_complete_customers": len(complete)}),
        encoding="utf-8",
    )
    return timestamps, series


# ---------------------------------------------------------------------------
# Lazy-window HyG training (needed for the 17-series Ausgrid tensors)
# ---------------------------------------------------------------------------


def hyg_train_and_predict_lazy(
    variant: dict,
    seed: int,
    tensors,
    train: list[Sample],
    test: list[Sample],
    horizon: int,
    epochs: int,
    train_stride: int,
) -> tuple[list[float], float]:
    import torch

    torch.manual_seed(seed)
    index = {name: i for i, name in enumerate(tensors.names)}
    offsets = torch.arange(-WINDOW + 1, 1)

    def indices(samples: list[Sample]):
        sidx = torch.tensor([index[s.country] for s in samples], dtype=torch.long)
        t_idx = torch.tensor([s.t for s in samples], dtype=torch.long)
        target_t = t_idx + horizon
        y = tensors.norm[sidx, target_t]
        hour = (target_t % 24).float()
        dow = ((target_t // 24) % 7).float()
        calendar = torch.stack(
            [
                torch.sin(2 * math.pi * hour / 24),
                torch.cos(2 * math.pi * hour / 24),
                torch.sin(2 * math.pi * dow / 7),
                torch.cos(2 * math.pi * dow / 7),
            ],
            dim=1,
        )
        return sidx, t_idx, calendar, y

    def gather_windows(t_batch: "torch.Tensor") -> "torch.Tensor":
        gather_idx = t_batch[:, None] + offsets[None, :]
        return tensors.norm[:, gather_idx].permute(1, 0, 2)  # [B, S, W]

    train_strided = train[::train_stride]
    ts = sorted(s.t for s in train_strided)
    cutoff = ts[int(len(ts) * 0.85)]
    fit_samples = [s for s in train_strided if s.t < cutoff]
    val_samples = [s for s in train_strided if s.t >= cutoff]

    s_fit, t_fit, c_fit, y_fit = indices(fit_samples)
    s_val, t_val, c_val, y_val = indices(val_samples)
    s_test, t_test, c_test, _ = indices(test)

    model = make_hyg_model(len(tensors.names), variant)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = torch.nn.MSELoss()

    start = time.perf_counter()
    best_val = float("inf")
    best_state = {k: v.clone() for k, v in model.state_dict().items()}
    n_fit = t_fit.shape[0]
    for _ in range(epochs):
        model.train()
        perm = torch.randperm(n_fit)
        for i in range(0, n_fit, BATCH_SIZE):
            idx = perm[i : i + BATCH_SIZE]
            optimizer.zero_grad()
            pred = model(gather_windows(t_fit[idx]), c_fit[idx], s_fit[idx])
            loss = loss_fn(pred, y_fit[idx])
            loss.backward()
            optimizer.step()
        model.eval()
        with torch.no_grad():
            val_loss = 0.0
            for i in range(0, t_val.shape[0], 2048):
                pred = model(gather_windows(t_val[i : i + 2048]), c_val[i : i + 2048], s_val[i : i + 2048])
                val_loss += loss_fn(pred, y_val[i : i + 2048]).item() * pred.shape[0]
            val_loss /= max(1, t_val.shape[0])
        if val_loss < best_val:
            best_val = val_loss
            best_state = {k: v.clone() for k, v in model.state_dict().items()}
    model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        preds = []
        for i in range(0, t_test.shape[0], 2048):
            batch = model(gather_windows(t_test[i : i + 2048]), c_test[i : i + 2048], s_test[i : i + 2048])
            preds.append(denormalize(batch, s_test[i : i + 2048], tensors))
        preds_full = torch.cat(preds)
    return preds_full.tolist(), time.perf_counter() - start


# ---------------------------------------------------------------------------
# Stage runners
# ---------------------------------------------------------------------------


def result_row(dataset_label: str, horizon: int, name: str, role: str, seed: int, metrics: dict, runtime: float, n_train: int, n_test: int) -> dict[str, str]:
    return {
        "dataset": dataset_label,
        "horizon_hours": str(horizon),
        "method": name,
        "method_role": role,
        "seed": str(seed),
        "mae": f"{metrics['mae']:.8f}",
        "rmse": f"{metrics['rmse']:.8f}",
        "mape": f"{metrics['mape']:.8f}",
        "smape": f"{metrics['smape']:.8f}",
        "normalized_mae": f"{metrics['normalized_mae']:.8f}",
        "peak_load_error": f"{metrics['peak_load_error']:.8f}",
        "runtime_s": f"{runtime:.4f}",
        "train_samples": str(n_train),
        "test_samples": str(n_test),
        "source_status": V7_RUN_VERSION,
    }


def merge_existing_seed_rows(dataset_key: str) -> list[dict[str, str]]:
    """Original 3-seed rows for the 10-seed model set (unchanged protocol)."""
    runs_dir = P2_ROOT / "evidence" / "runs"
    keep_models = {name for name, _, _ in VARIANTS} | {"MLP"}
    rows: list[dict[str, str]] = []
    for filename in (f"real_{dataset_key}_hyg_neural_results.csv", f"real_{dataset_key}_neural_results.csv"):
        path = runs_dir / filename
        if not path.exists():
            continue
        with path.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                if row["method"] in keep_models:
                    rows.append(row)
    return rows


def run_extension_stage(dataset_key: str) -> None:
    import torch

    torch.set_num_threads(4)
    if dataset_key == "opsd":
        timestamps, series = parse_opsd()
        dataset_label = "OPSD time_series_60min_singleindex"
        horizons = (1, 24)
    else:
        timestamps, series = parse_simbench()
        dataset_label = "SimBench 1-complete_data-mixed-all-0-sw LoadProfile hourly pload"
        horizons = (1, 24)
    n = len(timestamps)
    train_end = int(n * 0.70)
    tensors = build_tensors(series, train_end)

    rows: list[dict[str, str]] = []
    for horizon in horizons:
        train, test = samples_for(series, horizon=horizon, train_end=train_end)
        for name, role, variant in VARIANTS:
            for seed in EXTRA_SEEDS:
                preds, runtime = hyg_train_and_predict_lazy(
                    variant, seed, tensors, train, test, horizon, HYG_EPOCHS, TRAIN_STRIDE
                )
                metrics = evaluate_predictions(test, preds)
                rows.append(result_row(dataset_label, horizon, name, role, seed, metrics, runtime, len(train[::TRAIN_STRIDE]), len(test)))
            print(f"[{dataset_key}] h{horizon} {name}: +{len(EXTRA_SEEDS)} seeds done")
        for seed in EXTRA_SEEDS:
            preds, runtime = baseline_train_and_predict("MLP", 20, seed, tensors, train, test, horizon)
            metrics = evaluate_predictions(test, preds)
            rows.append(result_row(dataset_label, horizon, "MLP", "baseline", seed, metrics, runtime, len(train[::TRAIN_STRIDE]), len(test)))
        print(f"[{dataset_key}] h{horizon} MLP: +{len(EXTRA_SEEDS)} seeds done")

    write_csv(P2_ROOT / "evidence" / "runs" / f"real_{dataset_key}_v7_extra_seed_results.csv", rows)
    print(f"[{dataset_key}] extension stage complete")


def run_ausgrid_stage() -> None:
    import torch

    torch.set_num_threads(4)
    timestamps, series = parse_ausgrid()
    dataset_label = "Ausgrid solar home GC hourly (12 customers + 4 regions + total)"
    n = len(timestamps)
    train_end = int(n * 0.70)
    tensors = build_tensors(series, train_end)

    rows: list[dict[str, str]] = []
    for horizon in AUSGRID_HORIZONS:
        train, test = samples_for(series, horizon=horizon, train_end=train_end)
        n_train = len(train[::AUSGRID_TRAIN_STRIDE])
        for name, role, variant in VARIANTS:
            for seed in ALL_SEEDS:
                preds, runtime = hyg_train_and_predict_lazy(
                    variant, seed, tensors, train, test, horizon, AUSGRID_HYG_EPOCHS, AUSGRID_TRAIN_STRIDE
                )
                metrics = evaluate_predictions(test, preds)
                rows.append(result_row(dataset_label, horizon, name, role, seed, metrics, runtime, n_train, len(test)))
            print(f"[ausgrid] h{horizon} {name}: {len(ALL_SEEDS)} seeds done")
        baseline_plan = [("MLP", 20, ALL_SEEDS), ("DLinear", 20, ALL_SEEDS), ("TCN", 10, BASE_SEEDS), ("PatchTST-lite", 8, BASE_SEEDS), ("LSTM", 6, BASE_SEEDS)]
        for model_name, epochs, seeds in baseline_plan:
            for seed in seeds:
                preds, runtime = baseline_train_and_predict(model_name, epochs, seed, tensors, train, test, horizon)
                metrics = evaluate_predictions(test, preds)
                rows.append(result_row(dataset_label, horizon, model_name, "baseline", seed, metrics, runtime, n_train, len(test)))
            print(f"[ausgrid] h{horizon} {model_name}: {len(seeds)} seeds done")

    write_csv(P2_ROOT / "evidence" / "runs" / "real_ausgrid_v7_results.csv", rows)
    print("[ausgrid] stage complete")


# ---------------------------------------------------------------------------
# Report stage: significance tables + leaderboards + analysis
# ---------------------------------------------------------------------------


def collect_rows(dataset_key: str) -> list[dict[str, str]]:
    runs_dir = P2_ROOT / "evidence" / "runs"
    if dataset_key == "ausgrid":
        path = runs_dir / "real_ausgrid_v7_results.csv"
        with path.open(encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    rows = merge_existing_seed_rows(dataset_key)
    extra = runs_dir / f"real_{dataset_key}_v7_extra_seed_results.csv"
    with extra.open(encoding="utf-8-sig", newline="") as handle:
        rows.extend(csv.DictReader(handle))
    return rows


def holm(pvalues: list[float]) -> list[float]:
    import numpy as np

    order = np.argsort(pvalues)
    m = len(pvalues)
    adjusted = [0.0] * m
    running = 0.0
    for rank, idx in enumerate(order):
        running = max(running, min(1.0, (m - rank) * pvalues[idx]))
        adjusted[idx] = running
    return adjusted


def significance_tables() -> tuple[list[dict[str, str]], dict[str, dict]]:
    import numpy as np
    from scipy.stats import mannwhitneyu

    proposed_name = "HyG-LoadFormer (neural)"
    stats_rows: list[dict[str, str]] = []
    summary: dict[str, dict] = {}
    for dataset_key in ("opsd", "simbench", "ausgrid"):
        metric = PRIMARY_METRIC[dataset_key]
        rows = collect_rows(dataset_key)
        horizons = sorted({r["horizon_hours"] for r in rows}, key=int)
        for horizon in horizons:
            group = [r for r in rows if r["horizon_hours"] == horizon]
            proposed = [float(r[metric]) for r in group if r["method"] == proposed_name]
            opponents = sorted({r["method"] for r in group if r["method"] != proposed_name})
            entries = []
            pvals = []
            for opponent in opponents:
                values = [float(r[metric]) for r in group if r["method"] == opponent]
                if len(values) < 3 or len(proposed) < 3:
                    continue
                try:
                    u_stat, p_value = mannwhitneyu(proposed, values, alternative="two-sided")
                except ValueError:
                    u_stat, p_value = float("nan"), 1.0
                pvals.append(float(p_value))
                role = next(r["method_role"] for r in group if r["method"] == opponent)
                entries.append(
                    {
                        "dataset": dataset_key,
                        "horizon_hours": horizon,
                        "metric": metric,
                        "comparison": f"{proposed_name} vs {opponent}",
                        "opponent_role": role,
                        "n_proposed": str(len(proposed)),
                        "n_opponent": str(len(values)),
                        "mean_proposed": f"{np.mean(proposed):.8f}",
                        "mean_opponent": f"{np.mean(values):.8f}",
                        "proposed_better": str(np.mean(proposed) < np.mean(values)),
                        "u_statistic": f"{u_stat:.2f}" if not math.isnan(u_stat) else "NA",
                        "p_value": f"{p_value:.6g}",
                    }
                )
            for entry, p_h in zip(entries, holm(pvals)):
                entry["p_holm"] = f"{p_h:.6g}"
                entry["significant_005_holm"] = str(p_h < 0.05)
            stats_rows.extend(entries)
            summary[f"{dataset_key}_h{horizon}"] = {
                "proposed_mean": float(np.mean(proposed)) if proposed else float("nan"),
                "proposed_std": float(np.std(proposed, ddof=1)) if len(proposed) > 1 else 0.0,
                "n_seeds": len(proposed),
                "entries": entries,
            }
    return stats_rows, summary


def leaderboard_rows(dataset_key: str) -> list[dict[str, str]]:
    import numpy as np

    metric = PRIMARY_METRIC[dataset_key]
    rows = collect_rows(dataset_key)
    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault((row["horizon_hours"], row["method"]), []).append(row)
    board = []
    for (horizon, method), group in grouped.items():
        values = [float(r[metric]) for r in group]
        mapes = [float(r["mape"]) for r in group]
        board.append(
            {
                "horizon_hours": horizon,
                "method": method,
                "method_role": group[0]["method_role"],
                "n_seeds": str(len(group)),
                f"mean_{metric}": f"{np.mean(values):.8f}",
                f"std_{metric}": f"{np.std(values, ddof=1):.8f}" if len(values) > 1 else "0",
                "mean_mape": f"{np.mean(mapes):.8f}",
                "rank_metric": f"mean_{metric}_lower_is_better",
            }
        )
    return sorted(board, key=lambda r: (int(r["horizon_hours"]), float(r[f"mean_{metric}"])))


def analysis_markdown(stats_rows: list[dict[str, str]], summary: dict[str, dict]) -> str:
    proposed_name = "HyG-LoadFormer (neural)"
    lines = [
        "# P2 Seed-Significance and Ausgrid Hierarchical Analysis (v7)",
        "",
        f"Status: `{V7_RUN_VERSION}`. 10 seeds for the decision-relevant set (6 neural",
        "HyG variants + MLP) on OPSD and SimBench (3 original + 7 new seeds, identical",
        "protocol), plus the new Ausgrid solar-home hierarchical benchmark (hourly GC:",
        f"{AUSGRID_N_CUSTOMERS} top-energy complete customers + {AUSGRID_N_REGIONS} postcode-region",
        "aggregates + system total; 2010-07..2013-06; 24h day-ahead; 10 seeds for the",
        "HyG set and MLP/DLinear, 3 seeds for TCN/PatchTST/LSTM). Mann-Whitney U",
        "two-sided with Holm correction per dataset/horizon on the dataset's primary",
        "metric (OPSD: MAPE; SimBench/Ausgrid: normalized MAE).",
        "",
        "## Verdict tables (proposed vs opponents)",
        "",
    ]
    for key, info in summary.items():
        lines.append(f"### {key} (n_seeds={info['n_seeds']}, proposed mean `{info['proposed_mean']:.6f}` std `{info['proposed_std']:.6f}`)")
        lines.append("")
        lines.append("| opponent | role | mean opponent | proposed better? | p (Holm) | significant |")
        lines.append("|---|---|---|---|---|---|")
        for e in info["entries"]:
            lines.append(
                f"| {e['comparison'].split(' vs ')[1]} | {e['opponent_role']} | {e['mean_opponent']} | {e['proposed_better']} | {e['p_holm']} | {e['significant_005_holm']} |"
            )
        lines.append("")
    # component verdict
    lines.extend(["## Component verdict", ""])
    for key, info in summary.items():
        wins, losses, ties = [], [], []
        for e in info["entries"]:
            opponent = e["comparison"].split(" vs ")[1]
            if e["significant_005_holm"] == "True" and e["proposed_better"] == "True":
                wins.append(opponent)
            elif e["significant_005_holm"] == "True":
                losses.append(opponent)
            else:
                ties.append(opponent)
        lines.append(f"- **{key}**: significant wins: {', '.join(wins) if wins else 'none'}; significant losses: {', '.join(losses) if losses else 'none'}; not separable: {', '.join(ties) if ties else 'none'}")
    lines.extend(
        [
            "",
            "## Interpretation Boundary",
            "",
            "Every model in a comparison shares the training regime, splits, and test",
            "sets. OPSD/SimBench rows merge the original v5/v6 3-seed runs with 7 new",
            "seeds under an identical code path. Ausgrid uses lazy window gathering,",
            f"stride {AUSGRID_TRAIN_STRIDE}, {AUSGRID_HYG_EPOCHS} epochs (documented budget). If the",
            "hyperbolic components are still not separable from Euclidean/equal-weight",
            "ablations here, the manuscript's contribution claim must be downgraded",
            "accordingly (cross-series attention rather than hyperbolic geometry).",
        ]
    )
    return "\n".join(lines) + "\n"


def run_report_stage() -> None:
    stats_rows, summary = significance_tables()
    table_dir = P2_ROOT / "evidence" / "tables"
    write_csv(table_dir / "real_p2_v7_significance.csv", stats_rows)
    for dataset_key in ("opsd", "simbench", "ausgrid"):
        write_csv(table_dir / f"real_{dataset_key}_v7_leaderboard.csv", leaderboard_rows(dataset_key))
    (P2_ROOT / "evidence" / "runs" / "real_p2_v7_significance_analysis.md").write_text(
        analysis_markdown(stats_rows, summary), encoding="utf-8"
    )
    (P2_ROOT / "src" / "configs" / "real_p2_v7_config.json").write_text(
        json.dumps(
            {
                "seeds": ALL_SEEDS,
                "ten_seed_models": [name for name, _, _ in VARIANTS] + ["MLP"],
                "ausgrid": {
                    "zip": str(AUSGRID_ZIP.relative_to(ROOT)).replace("\\", "/"),
                    "series": f"{AUSGRID_N_CUSTOMERS} top-energy complete customers + {AUSGRID_N_REGIONS} postcode regions + system total",
                    "horizons": AUSGRID_HORIZONS,
                    "train_stride": AUSGRID_TRAIN_STRIDE,
                    "hyg_epochs": AUSGRID_HYG_EPOCHS,
                },
                "statistics": "Mann-Whitney U two-sided + Holm per dataset/horizon on the primary metric",
                "primary_metrics": PRIMARY_METRIC,
                "status": V7_RUN_VERSION,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print("report stage complete")


if __name__ == "__main__":
    import sys

    stage = next((a for a in sys.argv[1:] if a in {"opsd", "simbench", "ausgrid", "report"}), None)
    if stage == "opsd":
        run_extension_stage("opsd")
    elif stage == "simbench":
        run_extension_stage("simbench")
    elif stage == "ausgrid":
        run_ausgrid_stage()
    elif stage == "report":
        run_report_stage()
    else:
        raise SystemExit("usage: mintou_hyg_significance.py [opsd|simbench|ausgrid|report]")
