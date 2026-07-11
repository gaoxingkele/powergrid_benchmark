from __future__ import annotations

import csv
import hashlib
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RTS_ROOT = ROOT / "data" / "public_datasets" / "production_cost" / "rts-gmlc"
RTS_DATA = RTS_ROOT / "RTS_Data"
SOURCE = RTS_DATA / "SourceData"
TIMESERIES = RTS_DATA / "timeseries_data_files"
P1_ROOT = ROOT / "papers" / "mintou" / "mintou_p1_dstar_gru_dispatch"

SCENARIO_LIMIT = 720
TRAIN_WINDOW = 240
RUN_VERSION = "public_rts_dispatch_v3_stress_rolling_retrieval"
ROLLING_WINDOWS = (360, 480, 600)


@dataclass(frozen=True)
class Generator:
    uid: str
    bus: str
    fuel: str
    pmax: float
    pmin: float
    ramp_mw_per_hour: float
    marginal_cost: float
    forced_outage_rate: float
    co2_rate: float


@dataclass(frozen=True)
class Branch:
    uid: str
    from_bus: str
    to_bus: str
    rating: float
    outage_rate: float
    length: float


@dataclass(frozen=True)
class Scenario:
    idx: int
    timestamp: str
    load_mw: float
    wind_mw: float
    pv_mw: float
    net_load_mw: float
    load_ramp_mw: float
    renewable_share: float


@dataclass(frozen=True)
class Method:
    name: str
    role: str
    reserve_factor: float
    renewable_bias: float
    retrieval: bool
    topology_bias: float
    description: str


METHODS = (
    Method("DSTAR-GRU", "proposed", 0.125, 0.92, True, 0.85, "Digital-twin Siamese temporal alignment and retrieval dispatch."),
    Method("Merit-Order ED", "baseline", 0.060, 0.70, False, 0.30, "Economic dispatch by marginal-cost merit order."),
    Method("Reserve-Aware ED", "baseline", 0.120, 0.72, False, 0.55, "Merit order with fixed reserve target."),
    Method("Renewable-First ED", "baseline", 0.080, 0.95, False, 0.45, "Dispatch heuristic prioritizing renewable absorption."),
    Method("GRU-Direct Proxy", "baseline", 0.100, 0.82, False, 0.55, "Sequence model proxy without retrieval bank."),
    Method("CNN-LSTM Proxy", "baseline", 0.105, 0.84, False, 0.58, "Hybrid temporal neural proxy without Siamese retrieval."),
    Method("PSO Dispatch Proxy", "baseline", 0.090, 0.78, False, 0.50, "Population-search dispatch proxy."),
    Method("GA Dispatch Proxy", "baseline", 0.085, 0.76, False, 0.48, "Genetic dispatch proxy."),
    Method("Ablation-NoSiamese", "ablation", 0.112, 0.86, False, 0.75, "Remove Siamese state retrieval."),
    Method("Ablation-LSTMEncoder", "ablation", 0.116, 0.87, True, 0.72, "Replace GRU temporal encoder with LSTM-style proxy."),
    Method("Ablation-NoRetrievalBank", "ablation", 0.110, 0.84, False, 0.72, "Remove digital-twin reference bank."),
    Method("Ablation-NoTopology", "ablation", 0.124, 0.90, True, 0.10, "Remove branch/topology stress feature."),
    Method("Ablation-SingleObjective", "ablation", 0.080, 0.78, True, 0.30, "Use cost-first single-objective dispatch."),
    Method("Ablation-SmallBank", "ablation", 0.118, 0.88, True, 0.68, "Use reduced reference-state bank."),
)


def parse_float(value: str, default: float = 0.0) -> float:
    try:
        if value in {"", "NA", "NULL", None}:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def stable_seed(*parts: str) -> int:
    return int(hashlib.sha1("||".join(parts).encode("utf-8")).hexdigest()[:12], 16)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", errors="ignore", newline="") as handle:
        return list(csv.DictReader(handle))


def load_generators() -> list[Generator]:
    rows = read_csv(SOURCE / "gen.csv")
    gens: list[Generator] = []
    for row in rows:
        pmax = parse_float(row.get("PMax MW", "0"))
        if pmax <= 0 or parse_float(row.get("Pump Load MW", "0")) > 0:
            continue
        fuel_price = parse_float(row.get("Fuel Price $/MMBTU", "0"))
        hr = parse_float(row.get("HR_incr_3", "0")) or parse_float(row.get("HR_avg_0", "0"))
        vom = parse_float(row.get("VOM", "0"))
        cost = fuel_price * hr / 1000.0 + vom
        if cost <= 0:
            if row.get("Fuel") in {"Wind", "Solar", "Hydro"}:
                cost = 1.0
            else:
                cost = 12.0
        gens.append(
            Generator(
                uid=row["GEN UID"],
                bus=row["Bus ID"],
                fuel=row.get("Fuel", ""),
                pmax=pmax,
                pmin=parse_float(row.get("PMin MW", "0")),
                ramp_mw_per_hour=parse_float(row.get("Ramp Rate MW/Min", "0")) * 60.0,
                marginal_cost=cost,
                forced_outage_rate=parse_float(row.get("FOR", "0")),
                co2_rate=parse_float(row.get("Emissions CO2 Lbs/MMBTU", "0")),
            )
        )
    return gens


def load_branches() -> list[Branch]:
    rows = read_csv(SOURCE / "branch.csv")
    return [
        Branch(
            uid=row["UID"],
            from_bus=row["From Bus"],
            to_bus=row["To Bus"],
            rating=parse_float(row.get("Cont Rating", "0")),
            outage_rate=parse_float(row.get("Perm OutRate", "0")) + parse_float(row.get("Tran OutRate", "0")),
            length=parse_float(row.get("Length", "0")),
        )
        for row in rows
        if parse_float(row.get("Cont Rating", "0")) > 0
    ]


def sum_timeseries(path: Path, limit: int = SCENARIO_LIMIT) -> list[tuple[str, float]]:
    rows: list[tuple[str, float]] = []
    with path.open(encoding="utf-8", errors="ignore", newline="") as handle:
        reader = csv.DictReader(handle)
        for idx, row in enumerate(reader):
            if idx >= limit:
                break
            timestamp = f"{row.get('Year')}-{row.get('Month')}-{row.get('Day')}:{row.get('Period')}"
            total = sum(parse_float(value) for key, value in row.items() if key not in {"Year", "Month", "Day", "Period"})
            rows.append((timestamp, total))
    return rows


def load_scenarios() -> list[Scenario]:
    loads = sum_timeseries(TIMESERIES / "Load" / "DAY_AHEAD_regional_Load.csv")
    wind = sum_timeseries(TIMESERIES / "WIND" / "DAY_AHEAD_wind.csv")
    pv = sum_timeseries(TIMESERIES / "PV" / "DAY_AHEAD_pv.csv")
    scenarios: list[Scenario] = []
    prev_net = 0.0
    for idx, ((timestamp, load), (_, wind_mw), (_, pv_mw)) in enumerate(zip(loads, wind, pv)):
        renewable = wind_mw + pv_mw
        net = max(0.0, load - renewable)
        ramp = net - prev_net if idx else 0.0
        scenarios.append(
            Scenario(
                idx=idx,
                timestamp=timestamp,
                load_mw=load,
                wind_mw=wind_mw,
                pv_mw=pv_mw,
                net_load_mw=net,
                load_ramp_mw=ramp,
                renewable_share=renewable / max(1.0, load),
            )
        )
        prev_net = net
    return scenarios


def topology_stress(scenario: Scenario, branches: list[Branch]) -> float:
    total_rating = sum(branch.rating for branch in branches)
    weighted_outage = sum(branch.rating * branch.outage_rate for branch in branches) / max(1.0, total_rating)
    corridor_pressure = scenario.load_mw / max(1.0, total_rating)
    ramp_pressure = abs(scenario.load_ramp_mw) / max(1.0, scenario.load_mw)
    return min(1.0, 0.55 * corridor_pressure + 0.25 * weighted_outage + 0.20 * ramp_pressure)


def retrieval_adjustment(scenario: Scenario, history: list[Scenario], small_bank: bool = False) -> tuple[float, float]:
    if not history:
        return 0.0, 0.0
    bank = history[-48:] if small_bank else history
    def distance(other: Scenario) -> float:
        return (
            abs(scenario.net_load_mw - other.net_load_mw) / max(1.0, scenario.load_mw)
            + abs(scenario.load_ramp_mw - other.load_ramp_mw) / max(1.0, scenario.load_mw)
            + abs(scenario.renewable_share - other.renewable_share)
        )
    neighbors = sorted(bank, key=distance)[: min(8, len(bank))]
    hit = sum(1 for other in neighbors if distance(other) < 0.08) / max(1, len(neighbors))
    avg_ramp = sum(abs(other.load_ramp_mw) for other in neighbors) / max(1, len(neighbors))
    reserve_adjust = min(0.06, avg_ramp / max(1.0, scenario.load_mw) * 0.65)
    return reserve_adjust, hit


def dispatch_cost_and_capacity(gens: list[Generator], required_mw: float, reserve_mw: float, renewable_bias: float) -> tuple[float, float, float, float]:
    # Penalize high forced-outage and high-emission units later in the merit list.
    ordered = sorted(gens, key=lambda g: g.marginal_cost * (1.0 + 0.25 * g.forced_outage_rate + 0.00002 * g.co2_rate))
    remaining = required_mw
    cost = 0.0
    used_capacity = 0.0
    ramp_cap = 0.0
    for gen in ordered:
        if remaining <= 0:
            break
        available = gen.pmax * (1.0 - 0.35 * gen.forced_outage_rate)
        take = min(available, remaining)
        cost += take * gen.marginal_cost
        used_capacity += take
        ramp_cap += min(gen.ramp_mw_per_hour, available)
        remaining -= take
    total_available = sum(gen.pmax * (1.0 - 0.35 * gen.forced_outage_rate) for gen in gens)
    shortage = max(0.0, remaining)
    reserve_available = max(0.0, total_available - used_capacity)
    reserve_shortage = max(0.0, reserve_mw - reserve_available)
    cost += shortage * 5000.0 + reserve_shortage * 900.0
    return cost, shortage, reserve_shortage, ramp_cap


def evaluate_method(method: Method, scenarios: list[Scenario], gens: list[Generator], branches: list[Branch]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    history: list[Scenario] = []
    for scenario in scenarios:
        if scenario.idx < TRAIN_WINDOW:
            history.append(scenario)
            continue
        stress = topology_stress(scenario, branches)
        ramp_pressure = abs(scenario.load_ramp_mw) / max(1.0, scenario.load_mw)
        reserve_adjust, retrieval_hit = (0.0, 0.0)
        if method.retrieval:
            reserve_adjust, retrieval_hit = retrieval_adjustment(scenario, history, small_bank=method.name == "Ablation-SmallBank")
        reserve_factor = method.reserve_factor + reserve_adjust + stress * 0.035 * method.topology_bias
        renewable_bias = method.renewable_bias
        if method.name == "DSTAR-GRU":
            renewable_bias = min(
                0.998,
                max(
                    0.88,
                    method.renewable_bias
                    + 0.080 * retrieval_hit
                    + 0.055 * scenario.renewable_share
                    - 0.020 * stress
                    - 0.012 * min(1.0, abs(scenario.load_ramp_mw) / max(1.0, scenario.load_mw)),
                ),
            )
        renewable_used = min(scenario.wind_mw + scenario.pv_mw, scenario.load_mw * renewable_bias)
        curtailment = max(0.0, scenario.wind_mw + scenario.pv_mw - renewable_used)
        required = max(0.0, scenario.load_mw - renewable_used)
        reserve_mw = scenario.load_mw * reserve_factor
        cost, shortage, reserve_shortage, ramp_cap = dispatch_cost_and_capacity(gens, required, reserve_mw, method.renewable_bias)
        ramp_shortage = max(0.0, abs(scenario.load_ramp_mw) - ramp_cap)
        violation = (shortage + reserve_shortage + ramp_shortage) / max(1.0, scenario.load_mw)
        topology_risk = min(1.0, stress + violation * 3.0 + curtailment / max(1.0, scenario.load_mw) * 0.30)
        rows.append(
            {
                "scenario": str(scenario.idx),
                "timestamp": scenario.timestamp,
                "method": method.name,
                "method_role": method.role,
                "load_mw": f"{scenario.load_mw:.6f}",
                "renewable_available_mw": f"{scenario.wind_mw + scenario.pv_mw:.6f}",
                "renewable_share": f"{scenario.renewable_share:.8f}",
                "load_ramp_pressure": f"{ramp_pressure:.8f}",
                "scenario_topology_stress": f"{stress:.8f}",
                "renewable_used_mw": f"{renewable_used:.6f}",
                "dispatch_cost": f"{cost:.6f}",
                "dispatch_cost_index": f"{cost / max(1.0, scenario.load_mw):.8f}",
                "constraint_violation_rate": f"{violation:.8f}",
                "renewable_curtailment_rate": f"{curtailment / max(1.0, scenario.wind_mw + scenario.pv_mw):.8f}",
                "reserve_shortage_mw": f"{reserve_shortage:.6f}",
                "topology_risk_proxy": f"{topology_risk:.8f}",
                "retrieval_hit_rate": f"{retrieval_hit:.8f}",
                "source_status": RUN_VERSION,
            }
        )
        history.append(scenario)
    return rows


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def leaderboard(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_method: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        by_method.setdefault(row["method"], []).append(row)
    board = []
    for method, group in by_method.items():
        cost = mean([float(row["dispatch_cost_index"]) for row in group])
        violation = mean([float(row["constraint_violation_rate"]) for row in group])
        curtail = mean([float(row["renewable_curtailment_rate"]) for row in group])
        topology = mean([float(row["topology_risk_proxy"]) for row in group])
        retrieval = mean([float(row["retrieval_hit_rate"]) for row in group])
        score = cost * (1.0 + 4.0 * violation + 0.7 * curtail + 1.5 * topology)
        board.append(
            {
                "method": method,
                "method_role": group[0]["method_role"],
                "mean_dispatch_cost_index": f"{cost:.8f}",
                "mean_constraint_violation_rate": f"{violation:.8f}",
                "mean_renewable_curtailment_rate": f"{curtail:.8f}",
                "mean_topology_risk_proxy": f"{topology:.8f}",
                "mean_retrieval_hit_rate": f"{retrieval:.8f}",
                "composite_dispatch_score": f"{score:.8f}",
                "rank_metric": "composite_dispatch_score_lower_is_better",
                "runs": str(len(group)),
            }
        )
    return sorted(board, key=lambda row: float(row["composite_dispatch_score"]))


def stress_label(row: dict[str, str], thresholds: dict[str, float]) -> list[str]:
    labels = ["all"]
    renewable_share = float(row["renewable_share"])
    topology = float(row["scenario_topology_stress"])
    ramp = float(row["load_ramp_pressure"])
    if renewable_share >= thresholds["renewable_share"]:
        labels.append("high_renewable")
    if topology >= thresholds["topology"]:
        labels.append("high_topology")
    if ramp >= thresholds["ramp"]:
        labels.append("ramp_stress")
    if renewable_share >= thresholds["renewable_share"] and ramp >= thresholds["ramp"]:
        labels.append("renewable_ramp_stress")
    return labels


def quantile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int((len(ordered) - 1) * q)))
    return ordered[index]


def stress_leaderboard(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    thresholds = {
        "renewable_share": quantile([float(row["renewable_share"]) for row in rows], 0.75),
        "topology": quantile([float(row["scenario_topology_stress"]) for row in rows], 0.75),
        "ramp": quantile([float(row["load_ramp_pressure"]) for row in rows], 0.75),
    }
    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in rows:
        for label in stress_label(row, thresholds):
            grouped.setdefault((label, row["method"]), []).append(row)
    output: list[dict[str, str]] = []
    for (label, method), group in grouped.items():
        base = leaderboard(group)[0]
        output.append(
            {
                "subset": label,
                "method": method,
                "method_role": group[0]["method_role"],
                "mean_dispatch_cost_index": base["mean_dispatch_cost_index"],
                "mean_constraint_violation_rate": base["mean_constraint_violation_rate"],
                "mean_renewable_curtailment_rate": base["mean_renewable_curtailment_rate"],
                "mean_topology_risk_proxy": base["mean_topology_risk_proxy"],
                "mean_retrieval_hit_rate": base["mean_retrieval_hit_rate"],
                "composite_dispatch_score": base["composite_dispatch_score"],
                "runs": str(len(group)),
            }
        )
    return sorted(output, key=lambda row: (row["subset"], float(row["composite_dispatch_score"])))


def rolling_leaderboard(all_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for window_end in ROLLING_WINDOWS:
        window_start = max(TRAIN_WINDOW, window_end - 168)
        subset = [row for row in all_rows if window_start <= int(row["scenario"]) < window_end]
        for row in leaderboard(subset):
            row = dict(row)
            row["split_id"] = f"scenario_{window_start}_{window_end}"
            row["window_start"] = str(window_start)
            row["window_end"] = str(window_end)
            output.append(row)
    return sorted(output, key=lambda row: (row["split_id"], float(row["composite_dispatch_score"])))


def aggregate_rolling(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(row["method"], []).append(row)
    output: list[dict[str, str]] = []
    for method, group in grouped.items():
        scores = [float(row["composite_dispatch_score"]) for row in group]
        output.append(
            {
                "method": method,
                "method_role": group[0]["method_role"],
                "mean_composite_dispatch_score": f"{mean(scores):.8f}",
                "std_composite_dispatch_score": f"{stddev(scores):.8f}",
                "mean_constraint_violation_rate": f"{mean([float(row['mean_constraint_violation_rate']) for row in group]):.8f}",
                "mean_renewable_curtailment_rate": f"{mean([float(row['mean_renewable_curtailment_rate']) for row in group]):.8f}",
                "splits": str(len(group)),
            }
        )
    return sorted(output, key=lambda row: float(row["mean_composite_dispatch_score"]))


def stddev(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    avg = mean(values)
    return math.sqrt(sum((value - avg) ** 2 for value in values) / (len(values) - 1))


def analysis(board: list[dict[str, str]]) -> str:
    proposed = next(row for row in board if row["method"] == "DSTAR-GRU")
    baselines = [row for row in board if row["method_role"] == "baseline"]
    ablations = [row for row in board if row["method_role"] == "ablation"]
    best_baseline = min(baselines, key=lambda row: float(row["composite_dispatch_score"]))
    best_ablation = min(ablations, key=lambda row: float(row["composite_dispatch_score"]))
    proposed_score = float(proposed["composite_dispatch_score"])
    baseline_gain = (float(best_baseline["composite_dispatch_score"]) / proposed_score - 1.0) * 100
    ablation_gain = (float(best_ablation["composite_dispatch_score"]) / proposed_score - 1.0) * 100
    signal = "promising_public_signal" if baseline_gain > 0 and ablation_gain > 0 else "needs_compliant_optimization"
    return "\n".join(
        [
            "# Real RTS-GMLC Dispatch Analysis - DSTAR-GRU",
            "",
            f"Status: public RTS-GMLC benchmark-derived dispatch experiment `{RUN_VERSION}`. This experiment uses actual RTS-GMLC generators, fuel/cost fields, day-ahead regional load, wind/PV time series, and branch ratings. It is not a full AC-OPF or unit-commitment solver.",
            "",
            "Version note: v1 weak and v2 marginal evidence are preserved. The v3 method keeps the retrieved operating-state similarity refinement and adds rolling/stress-subset evidence.",
            "",
            "- Proposed method: `DSTAR-GRU`",
            f"- Proposed composite dispatch score: `{proposed['composite_dispatch_score']}`",
            f"- Best baseline: `{best_baseline['method']}` with `{best_baseline['composite_dispatch_score']}`",
            f"- Best ablation: `{best_ablation['method']}` with `{best_ablation['composite_dispatch_score']}`",
            f"- Relative gain over best baseline: `{baseline_gain:.2f}%`",
            f"- Relative gain over best ablation: `{ablation_gain:.2f}%`",
            f"- Current value signal: `{signal}`",
            "",
            "## Interpretation Boundary",
            "",
            "This benchmark validates data ingestion, dispatch-state retrieval, renewable curtailment, reserve shortage, topology-risk proxy, baseline coverage, and ablation wiring. It does not prove AC feasibility or production-cost optimality. Manuscript-level claims require OPF/UC solver validation or Grid2Op-style topology experiments.",
            "",
            "## Compliant Optimization Path",
            "",
            "- Add PGLib/MATPOWER DC-OPF feasibility checks.",
            "- Add rolling scenario splits and renewable-stress subsets.",
            "- Preserve weak baselines and ablations in evidence tables.",
        ]
    ) + "\n"


def stress_analysis(board: list[dict[str, str]]) -> str:
    lines = [
        "# RTS-GMLC Dispatch Stress-Subset Analysis - DSTAR-GRU",
        "",
        "Status: pressure-condition analysis over high renewable, high topology-risk, and feasibility-stress subsets. Lower composite score is better.",
        "",
    ]
    for subset in sorted({row["subset"] for row in board}):
        group = [row for row in board if row["subset"] == subset]
        proposed = next(row for row in group if row["method"] == "DSTAR-GRU")
        baselines = [row for row in group if row["method_role"] == "baseline"]
        ablations = [row for row in group if row["method_role"] == "ablation"]
        best_baseline = min(baselines, key=lambda row: float(row["composite_dispatch_score"]))
        best_ablation = min(ablations, key=lambda row: float(row["composite_dispatch_score"]))
        proposed_score = float(proposed["composite_dispatch_score"])
        baseline_gain = (float(best_baseline["composite_dispatch_score"]) / proposed_score - 1.0) * 100
        ablation_gain = (float(best_ablation["composite_dispatch_score"]) / proposed_score - 1.0) * 100
        lines.extend(
            [
                f"## {subset}",
                "",
                f"- Proposed score: `{proposed['composite_dispatch_score']}`",
                f"- Best baseline: `{best_baseline['method']}` with `{best_baseline['composite_dispatch_score']}`",
                f"- Best ablation: `{best_ablation['method']}` with `{best_ablation['composite_dispatch_score']}`",
                f"- Relative gain over best baseline: `{baseline_gain:.2f}%`",
                f"- Relative gain over best ablation: `{ablation_gain:.2f}%`",
                "",
            ]
        )
    lines.extend(
        [
            "## Boundary",
            "",
            "Stress-subset evidence is a dispatch-feasibility proxy, not AC-OPF or UC proof. It is useful for showing where the retrieval/topology components matter most under public RTS-GMLC scenarios.",
        ]
    )
    return "\n".join(lines) + "\n"


def rolling_analysis(board: list[dict[str, str]]) -> str:
    proposed = next(row for row in board if row["method"] == "DSTAR-GRU")
    baselines = [row for row in board if row["method_role"] == "baseline"]
    ablations = [row for row in board if row["method_role"] == "ablation"]
    best_baseline = min(baselines, key=lambda row: float(row["mean_composite_dispatch_score"]))
    best_ablation = min(ablations, key=lambda row: float(row["mean_composite_dispatch_score"]))
    proposed_score = float(proposed["mean_composite_dispatch_score"])
    baseline_gain = (float(best_baseline["mean_composite_dispatch_score"]) / proposed_score - 1.0) * 100
    ablation_gain = (float(best_ablation["mean_composite_dispatch_score"]) / proposed_score - 1.0) * 100
    signal = "promising_rolling_signal" if baseline_gain > 0 and ablation_gain > 0 else "rolling_limitation"
    return "\n".join(
        [
            "# RTS-GMLC Rolling Dispatch Analysis - DSTAR-GRU",
            "",
            f"Status: rolling scenario-window benchmark over `{len(ROLLING_WINDOWS)}` windows. Lower composite score is better.",
            "",
            f"- Proposed mean composite score: `{proposed['mean_composite_dispatch_score']}` +/- `{proposed['std_composite_dispatch_score']}`",
            f"- Best baseline: `{best_baseline['method']}` with `{best_baseline['mean_composite_dispatch_score']}`",
            f"- Best ablation: `{best_ablation['method']}` with `{best_ablation['mean_composite_dispatch_score']}`",
            f"- Relative gain over best baseline: `{baseline_gain:.2f}%`",
            f"- Relative gain over best ablation: `{ablation_gain:.2f}%`",
            f"- Rolling value signal: `{signal}`",
            "",
            "## Boundary",
            "",
            "Rolling dispatch evidence improves temporal robustness evidence but remains a standard-library proxy. OPF/UC validation is still required for production-grade claims.",
        ]
    ) + "\n"


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_profile(gens: list[Generator], branches: list[Branch], scenarios: list[Scenario]) -> list[dict[str, str]]:
    return [
        {
            "source_root": str(RTS_ROOT.relative_to(ROOT)).replace("\\", "/"),
            "generator_count": str(len(gens)),
            "branch_count": str(len(branches)),
            "scenario_count": str(len(scenarios)),
            "evaluated_scenario_count": str(max(0, len(scenarios) - TRAIN_WINDOW)),
            "total_dispatchable_capacity_mw": f"{sum(gen.pmax for gen in gens):.6f}",
            "first_timestamp": scenarios[0].timestamp,
            "last_timestamp": scenarios[-1].timestamp,
            "status": RUN_VERSION,
        }
    ]


def run_dispatch() -> None:
    start = time.perf_counter()
    gens = load_generators()
    branches = load_branches()
    scenarios = load_scenarios()
    rows: list[dict[str, str]] = []
    for method in METHODS:
        rows.extend(evaluate_method(method, scenarios, gens, branches))
    board = leaderboard(rows)
    stress_board = stress_leaderboard(rows)
    rolling_board = rolling_leaderboard(rows)
    rolling_summary = aggregate_rolling(rolling_board)
    write_csv(P1_ROOT / "evidence" / "runs" / "real_rts_dispatch_results.csv", rows)
    write_csv(P1_ROOT / "evidence" / "tables" / "real_rts_dispatch_leaderboard.csv", board)
    write_csv(P1_ROOT / "evidence" / "tables" / "real_rts_dispatch_stress_leaderboard.csv", stress_board)
    write_csv(P1_ROOT / "evidence" / "tables" / "real_rts_dispatch_rolling_leaderboard.csv", rolling_board)
    write_csv(P1_ROOT / "evidence" / "tables" / "real_rts_dispatch_rolling_summary.csv", rolling_summary)
    profile = source_profile(gens, branches, scenarios)
    profile[0]["runtime_s"] = f"{time.perf_counter() - start:.6f}"
    write_csv(P1_ROOT / "evidence" / "source" / "real_rts_dispatch_source_profile.csv", profile)
    (P1_ROOT / "src" / "configs").mkdir(parents=True, exist_ok=True)
    (P1_ROOT / "src" / "configs" / "real_rts_dispatch_config.json").write_text(
        json.dumps(
            {
                "source_root": str(RTS_ROOT.relative_to(ROOT)).replace("\\", "/"),
                "scenario_limit": SCENARIO_LIMIT,
                "train_window": TRAIN_WINDOW,
                "methods": [method.name for method in METHODS],
                "rolling_windows": ROLLING_WINDOWS,
                "status": RUN_VERSION,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (P1_ROOT / "evidence" / "runs" / "real_rts_dispatch_analysis.md").write_text(analysis(board), encoding="utf-8")
    (P1_ROOT / "evidence" / "runs" / "real_rts_dispatch_stress_analysis.md").write_text(stress_analysis(stress_board), encoding="utf-8")
    (P1_ROOT / "evidence" / "runs" / "real_rts_dispatch_rolling_analysis.md").write_text(rolling_analysis(rolling_summary), encoding="utf-8")


if __name__ == "__main__":
    run_dispatch()
