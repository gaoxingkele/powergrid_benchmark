"""Regenerate the P3 S4 result tables and figures from one canonical manifest.

This is a deterministic narrative aggregation of the accepted P3 S3 evidence.
It does not rerun an optimizer or an AC power flow.  The base configuration's
two seed blocks are pooled within that configuration; six configurations then
receive equal weight in cross-configuration descriptive summaries.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "evidence/runs/p3_s4_results_narrative_20260813/manifest.json"

BLUE = "#0077BB"
BLUE_DARK = "#005A8C"
ORANGE = "#EE7733"
TEAL = "#009988"
RED = "#CC3311"
GRAY = "#8A8A86"
LIGHT = "#E6E6E2"
INK = "#242424"
WHITE = "#FFFFFF"

METRICS = [
    "legacy_hv_sampled_clip_ref110",
    "analytic_hv_ref110",
    "analytic_hv_ref105",
    "igd_plus_common_reference",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not data.get("canonical") or data.get("schema_version") != "1.0":
        raise ValueError("expected canonical manifest schema 1.0")
    for name, spec in data["sources"].items():
        source = ROOT / spec["path"]
        if not source.is_file():
            raise FileNotFoundError(f"missing source {name}: {source}")
        actual = sha256(source)
        if actual != spec["sha256"]:
            raise ValueError(f"source hash mismatch for {name}: {actual}")
    return data


def read_csv(manifest: dict, key: str) -> pd.DataFrame:
    spec = manifest["sources"][key]
    frame = pd.read_csv(ROOT / spec["path"])
    expected = spec.get("expected_rows")
    if expected is not None and len(frame) != expected:
        raise ValueError(f"{key}: expected {expected} rows, found {len(frame)}")
    return frame


def write_csv(frame: pd.DataFrame, relative: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False, lineterminator="\n", float_format="%.10g")


def prepare_tables(manifest: dict) -> dict[str, pd.DataFrame]:
    runs = read_csv(manifest, "run_metrics")
    _ = read_csv(manifest, "inference")
    compositions = read_csv(manifest, "compromise_compositions")
    ac_common = read_csv(manifest, "ac_common_panel")

    configs = manifest["configuration_contract"]
    exp_to_config: dict[str, str] = {}
    for cfg in configs:
        for experiment in cfg["seed_blocks"]:
            if experiment in exp_to_config:
                raise ValueError(f"seed block assigned twice: {experiment}")
            exp_to_config[experiment] = cfg["configuration_id"]
    observed = set(runs["experiment_id"].unique())
    if observed != set(exp_to_config):
        raise ValueError(f"configuration mapping mismatch: observed={sorted(observed)}")
    if len(configs) != 6 or len(exp_to_config) != 7:
        raise ValueError("contract must contain six configurations and seven seed blocks")

    runs = runs.copy()
    runs["configuration_id"] = runs["experiment_id"].map(exp_to_config)
    compositions = compositions.copy()
    compositions["configuration_id"] = compositions["experiment_id"].map(exp_to_config)

    cfg_rows = []
    for cfg in configs:
        cfg_rows.append({
            "configuration_id": cfg["configuration_id"],
            "label": cfg["label"],
            "budget_factor": cfg["budget_factor"],
            "load_factor": cfg["load_factor"],
            "search_dimension": cfg["search_dimension"],
            "pool_restriction": cfg["pool_restriction"],
            "seed_blocks": ";".join(cfg["seed_blocks"]),
            "seed_block_count": len(cfg["seed_blocks"]),
            "is_internal_replication_pair": len(cfg["seed_blocks"]) > 1,
        })
    cfg_contract = pd.DataFrame(cfg_rows)

    # First average within each experiment-labelled seed block. This prevents
    # Weighted Sum's rectangular 30-row provenance from becoming replication.
    exp_means = (
        runs.groupby(["configuration_id", "experiment_id", "method", "method_role"], as_index=False)
        .agg(
            seed_rows=("run_id", "size"),
            mean_legacy_hv_sampled_clip_ref110=("legacy_hv_sampled_clip_ref110", "mean"),
            mean_analytic_hv_ref110=("analytic_hv_ref110", "mean"),
            mean_analytic_hv_ref105=("analytic_hv_ref105", "mean"),
            mean_igd_plus_common_reference=("igd_plus_common_reference", "mean"),
            mean_front_size=("front_size", "mean"),
            mean_runtime_s_provenance_only=("runtime_s", "mean"),
        )
    )
    cfg_means = (
        exp_means.groupby(["configuration_id", "method", "method_role"], as_index=False)
        .agg(
            seed_block_count=("experiment_id", "size"),
            source_seed_rows=("seed_rows", "sum"),
            mean_legacy_hv_sampled_clip_ref110=("mean_legacy_hv_sampled_clip_ref110", "mean"),
            mean_analytic_hv_ref110=("mean_analytic_hv_ref110", "mean"),
            mean_analytic_hv_ref105=("mean_analytic_hv_ref105", "mean"),
            mean_igd_plus_common_reference=("mean_igd_plus_common_reference", "mean"),
            mean_front_size=("mean_front_size", "mean"),
            mean_runtime_s_provenance_only=("mean_runtime_s_provenance_only", "mean"),
        )
    )
    order = {cfg["configuration_id"]: i for i, cfg in enumerate(configs)}
    cfg_means["configuration_order"] = cfg_means["configuration_id"].map(order)
    cfg_means = cfg_means.sort_values(["configuration_order", "method"]).drop(columns="configuration_order")

    leaderboard = (
        cfg_means.groupby(["method", "method_role"], as_index=False)
        .agg(
            configuration_count=("configuration_id", "size"),
            mean_legacy_hv_sampled_clip_ref110=("mean_legacy_hv_sampled_clip_ref110", "mean"),
            mean_analytic_hv_ref110=("mean_analytic_hv_ref110", "mean"),
            mean_analytic_hv_ref105=("mean_analytic_hv_ref105", "mean"),
            mean_igd_plus_common_reference=("mean_igd_plus_common_reference", "mean"),
            mean_front_size=("mean_front_size", "mean"),
            mean_runtime_s_provenance_only=("mean_runtime_s_provenance_only", "mean"),
        )
    )
    for metric in METRICS[:-1]:
        col = "mean_" + metric
        leaderboard["rank_" + metric] = leaderboard[col].rank(method="min", ascending=False).astype(int)
    leaderboard["rank_igd_plus_common_reference"] = leaderboard[
        "mean_igd_plus_common_reference"
    ].rank(method="min", ascending=True).astype(int)
    leaderboard["weighting"] = "equal weight across six configurations; base pools two seed blocks"
    leaderboard = leaderboard.sort_values("rank_analytic_hv_ref105")

    effect_rows = []
    for cfg in configs:
        cid = cfg["configuration_id"]
        sub = cfg_means[cfg_means["configuration_id"] == cid].set_index("method")
        proposed = sub.loc["CARS-MODE"]
        row = {
            "configuration_id": cid,
            "configuration_label": cfg["label"],
            "source_seed_blocks": ";".join(cfg["seed_blocks"]),
            "proposed_seed_rows": int(proposed["source_seed_rows"]),
            "cars_legacy_hv": proposed["mean_legacy_hv_sampled_clip_ref110"],
            "cars_analytic_hv_ref105": proposed["mean_analytic_hv_ref105"],
            "cars_igd_plus": proposed["mean_igd_plus_common_reference"],
        }
        for opponent, prefix in [
            ("NSGA-II+Repair", "vs_nsga2_repair"),
            ("Ablation-FixedDE", "vs_fixedde"),
            ("GDE3", "vs_gde3"),
            ("NSDE", "vs_nsde"),
        ]:
            other = sub.loc[opponent]
            row[f"{prefix}_legacy_effect_pct"] = 100 * (
                proposed["mean_legacy_hv_sampled_clip_ref110"]
                - other["mean_legacy_hv_sampled_clip_ref110"]
            ) / abs(other["mean_legacy_hv_sampled_clip_ref110"])
            row[f"{prefix}_analytic_ref105_effect_pct"] = 100 * (
                proposed["mean_analytic_hv_ref105"] - other["mean_analytic_hv_ref105"]
            ) / abs(other["mean_analytic_hv_ref105"])
            row[f"{prefix}_igd_plus_effect_pct"] = 100 * (
                other["mean_igd_plus_common_reference"]
                - proposed["mean_igd_plus_common_reference"]
            ) / abs(other["mean_igd_plus_common_reference"])
        effect_rows.append(row)
    effects = pd.DataFrame(effect_rows)

    # Configuration-equal portfolio composition: seed-block means first,
    # configuration means second, then equal weight across six configurations.
    comp_exp = (
        compositions.groupby(["configuration_id", "experiment_id", "method", "method_role"], as_index=False)
        .agg({"reinforcement": "mean", "storage": "mean", "der": "mean", "automation": "mean"})
    )
    comp_cfg = (
        comp_exp.groupby(["configuration_id", "method", "method_role"], as_index=False)
        .agg({"reinforcement": "mean", "storage": "mean", "der": "mean", "automation": "mean"})
    )
    comp_summary = (
        comp_cfg.groupby(["method", "method_role"], as_index=False)
        .agg({"reinforcement": "mean", "storage": "mean", "der": "mean", "automation": "mean"})
    )
    comp_summary["weighting"] = "equal weight across six configurations; all rerun seed compromises; not AC-evaluated"

    ac_summary = pd.DataFrame(manifest["archived_ac_summary"])
    role_map = ac_summary.set_index("method")["method_role"].to_dict()
    ac_decision = ac_common.copy()
    ac_decision.insert(1, "method_role", ac_decision["method"].map(role_map))
    ac_decision = ac_decision.merge(
        ac_summary[["method", "ac_feasible_rate", "stress_ac_feasible_rate"]], on="method", how="left"
    )
    ac_decision["evidence_scope"] = manifest["ac_scope"]["label"]

    sensitivity = pd.DataFrame(manifest["sensitivity_summary"])
    ac_margin = ac_summary[[
        "method", "method_role", "ac_feasible_rate", "median_max_line_loading_pct",
        "p95_max_line_loading_pct",
    ]].copy()
    ac_margin["n"] = 72
    ac_margin["scope"] = "illustrative; 72 dependent cases from three run-index-0 compositions"

    pooled_efficiency = leaderboard[[
        "method", "method_role", "mean_legacy_hv_sampled_clip_ref110",
        "mean_runtime_s_provenance_only", "mean_front_size", "configuration_count", "weighting",
    ]].copy()

    outputs = manifest["artifact_outputs"]["tables"]
    table_map = {
        "p3_configuration_contract.csv": cfg_contract,
        "p3_configuration_metric_means.csv": cfg_means,
        "p3_configuration_effects.csv": effects,
        "p3_configuration_weighted_leaderboard.csv": leaderboard,
        "p3_hv_reference_robustness.csv": leaderboard,
        "p3_pooled_efficiency.csv": pooled_efficiency,
        "p3_portfolio_composition_config_weighted.csv": comp_summary,
        "p3_ac_common_panel_vs_no_plan.csv": ac_common,
        "p3_ac_decision_value.csv": ac_decision,
        "p3_ac_margin_diagnostics.csv": ac_margin,
        "p3_sensitivity.csv": sensitivity,
    }
    for relative in outputs:
        name = Path(relative).name
        if name not in table_map:
            raise ValueError(f"no generator for declared table {name}")
        write_csv(table_map[name], relative)
    return {
        "configuration_means": cfg_means,
        "effects": effects,
        "leaderboard": leaderboard,
        "composition": comp_summary,
        "ac_summary": ac_summary,
        "ac_decision": ac_decision,
        "sensitivity": sensitivity,
    }


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def canvas(width: int = 2100, height: int = 1260) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (width, height), WHITE)
    return image, ImageDraw.Draw(image)


def text(draw: ImageDraw.ImageDraw, xy: tuple[float, float], value: str, size: int = 30,
         fill: str = INK, anchor: str = "la", bold: bool = False) -> None:
    draw.text(xy, value, font=font(size, bold), fill=fill, anchor=anchor)


def save(image: Image.Image, relative: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, dpi=(300, 300), optimize=True)


def axes(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], ymin: float, ymax: float,
         ylabel: str, ticks: int = 5) -> None:
    x0, y0, x1, y1 = box
    draw.line((x0, y0, x0, y1), fill=INK, width=3)
    draw.line((x0, y1, x1, y1), fill=INK, width=3)
    for i in range(ticks + 1):
        value = ymin + (ymax - ymin) * i / ticks
        y = y1 - (y1 - y0) * i / ticks
        draw.line((x0, y, x1, y), fill=LIGHT, width=2)
        text(draw, (x0 - 18, y), f"{value:.1f}", 25, anchor="ra")
    text(draw, (x0 - 105, (y0 + y1) / 2), ylabel, 27, anchor="mm")


def draw_marker(draw: ImageDraw.ImageDraw, x: float, y: float, color: str, shape: str) -> None:
    r = 11
    if shape == "square":
        draw.rectangle((x - r, y - r, x + r, y + r), fill=color, outline=INK, width=2)
    elif shape == "triangle":
        draw.polygon([(x, y - r - 2), (x - r - 2, y + r), (x + r + 2, y + r)], fill=color, outline=INK)
    else:
        draw.ellipse((x - r, y - r, x + r, y + r), fill=color, outline=INK, width=2)


def figure_configuration_effects(manifest: dict, tables: dict[str, pd.DataFrame]) -> None:
    frame = tables["effects"]
    configs = manifest["configuration_contract"]
    series = [
        ("legacy_effect_pct", "Sampled/clipped HV", BLUE, "circle"),
        ("analytic_ref105_effect_pct", "Analytic HV, r=1.05", ORANGE, "square"),
        ("igd_plus_effect_pct", "Common-ref IGD+", TEAL, "triangle"),
    ]
    image, draw = canvas(2400, 1280)
    text(draw, (1200, 42), "Configuration-specific CARS-MODE effects", 42, anchor="ma", bold=True)
    panels = [
        ((170, 155, 1130, 1000), "vs NSGA-II+Repair", "vs_nsga2_repair"),
        ((1370, 155, 2330, 1000), "vs FixedDE joint control", "vs_fixedde"),
    ]
    vals = []
    for _, _, prefix in panels:
        for suffix, _, _, _ in series:
            vals.extend(frame[f"{prefix}_{suffix}"].astype(float).tolist())
    bound = max(5.0, math.ceil(max(abs(min(vals)), abs(max(vals))) / 5.0) * 5.0)
    ymin, ymax = -bound, bound
    for box, title_value, prefix in panels:
        x0, y0, x1, y1 = box
        axes(draw, box, ymin, ymax, "Effect on metric (%)")
        zero = y1 - (0 - ymin) / (ymax - ymin) * (y1 - y0)
        draw.line((x0, zero, x1, zero), fill=INK, width=4)
        text(draw, ((x0 + x1) / 2, y0 - 45), title_value, 33, anchor="ma", bold=True)
        xs = [x0 + (x1 - x0) * (i + 0.5) / len(configs) for i in range(len(configs))]
        for suffix, label, color, shape in series:
            ys = []
            for idx, x in enumerate(xs):
                value = float(frame.iloc[idx][f"{prefix}_{suffix}"])
                y = y1 - (value - ymin) / (ymax - ymin) * (y1 - y0)
                ys.append((x, y))
            draw.line(ys, fill=color, width=6)
            for x, y in ys:
                draw_marker(draw, x, y, color, shape)
        for x, cfg in zip(xs, configs):
            label = cfg["short_label"].replace(" ", "\n", 1)
            text(draw, (x, y1 + 28), label, 23, anchor="ma")
    legend_x = 620
    for suffix, label, color, shape in series:
        draw_marker(draw, legend_x, 1110, color, shape)
        text(draw, (legend_x + 25, 1110), label, 27, anchor="lm")
        legend_x += 440
    text(draw, (1200, 1205),
         "Positive values favor CARS-MODE. The base estimate pools two independent 30-run seed blocks; it is one configuration.",
         27, anchor="ma")
    save(image, "manuscript/figures/fig_configuration_effects.png")


def horizontal_bars(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], labels: list[str],
                    values: list[float], colors: list[str], xmin: float, xmax: float,
                    xlabel: str, value_format: str = ".3f") -> None:
    x0, y0, x1, y1 = box
    zero = x0 + (0 - xmin) / (xmax - xmin) * (x1 - x0)
    draw.line((zero, y0, zero, y1), fill=INK, width=3)
    row_h = (y1 - y0) / len(labels)
    for i, (label, value, color) in enumerate(zip(labels, values, colors)):
        yc = y0 + row_h * (i + 0.5)
        xv = x0 + (value - xmin) / (xmax - xmin) * (x1 - x0)
        draw.rectangle((min(zero, xv), yc - row_h * 0.28, max(zero, xv), yc + row_h * 0.28), fill=color, outline=INK, width=1)
        text(draw, (x0 - 20, yc), label, 24, anchor="rm")
        anchor = "lm" if value >= 0 else "rm"
        offset = 10 if value >= 0 else -10
        text(draw, (xv + offset, yc), format(value, value_format), 23, anchor=anchor)
    draw.line((x0, y1, x1, y1), fill=INK, width=3)
    text(draw, ((x0 + x1) / 2, y1 + 55), xlabel, 27, anchor="ma")


def figure_ablation(tables: dict[str, pd.DataFrame]) -> None:
    methods = ["CARS-MODE", "Ablation-FixedDE", "Ablation-NoDER", "Ablation-NoRepair", "Ablation-NoDiversity"]
    labels = ["CARS-MODE", "FixedDE", "NoDER (problem variant)", "NoRepair", "NoDiversity"]
    frame = tables["leaderboard"].set_index("method").loc[methods]
    values = frame["mean_legacy_hv_sampled_clip_ref110"].astype(float).tolist()
    colors = [BLUE, ORANGE, GRAY, GRAY, GRAY]
    image, draw = canvas(2100, 1180)
    text(draw, (1050, 45), "Configuration-equal sampled/clipped hypervolume", 40, anchor="ma", bold=True)
    horizontal_bars(draw, (510, 145, 1920, 930), labels, values, colors, 0, 0.05, "Mean hypervolume across six configurations", ".5f")
    full = values[0]
    fixed = values[1]
    text(draw, (1050, 1050), f"FixedDE is nominally {100*(fixed-full)/full:.2f}% above CARS-MODE; the joint adaptation effect remains unresolved.", 29, anchor="ma")
    save(image, "manuscript/figures/fig_ablation.png")


def figure_ac_validation(tables: dict[str, pd.DataFrame]) -> None:
    frame = tables["ac_summary"].sort_values("ac_feasible_rate", ascending=False)
    labels = frame["method"].replace({"NoPlan": "No-Plan"}).tolist()
    all_values = frame["ac_feasible_rate"].astype(float).tolist()
    stress = frame["stress_ac_feasible_rate"].astype(float).tolist()
    image, draw = canvas(2300, 1550)
    text(draw, (1150, 42), "Archived composition-level AC diagnostic", 42, anchor="ma", bold=True)
    x0, y0, x1, y1 = 520, 140, 2160, 1310
    row_h = (y1 - y0) / len(labels)
    for i, (label, all_v, stress_v) in enumerate(zip(labels, all_values, stress)):
        yc = y0 + row_h * (i + 0.5)
        text(draw, (x0 - 20, yc), label, 24, anchor="rm")
        col = BLUE if label == "CARS-MODE" else (ORANGE if label == "Ablation-FixedDE" else GRAY)
        draw.rectangle((x0, yc - 24, x0 + all_v * (x1-x0), yc - 2), fill=col)
        draw.rectangle((x0, yc + 4, x0 + stress_v * (x1-x0), yc + 26), fill=LIGHT, outline=col, width=2)
    for tick in [0, .2, .4, .6, .8, 1.0]:
        x = x0 + tick * (x1 - x0)
        draw.line((x, y0, x, y1), fill=LIGHT, width=2)
        text(draw, (x, y1 + 25), f"{tick:.1f}", 24, anchor="ma")
    xref = x0 + .5 * (x1 - x0)
    draw.line((xref, y0, xref, y1), fill=INK, width=4)
    text(draw, ((x0+x1)/2, y1+85), "AC-feasible fraction of 72 dependent fixed cases", 28, anchor="ma")
    text(draw, (1150, 1465), "Solid: all cases; outlined: stress-only. Fractions are descriptive and are not optimizer-seed feasibility probabilities.", 27, anchor="ma")
    save(image, "manuscript/figures/fig_ac_validation.png")


def figure_sensitivity(tables: dict[str, pd.DataFrame]) -> None:
    frame = tables["sensitivity"]
    image, draw = canvas(2200, 1160)
    text(draw, (1100, 40), "Exploratory parameter sensitivity", 42, anchor="ma", bold=True)
    for panel, axis_name, title_value in [(0, "population_size", "Population size"), (1, "tau", "Resampling probability")]:
        sub = frame[frame["axis"] == axis_name].reset_index(drop=True)
        x0 = 160 + panel * 1080
        box = (x0, 160, x0 + 900, 900)
        axes(draw, box, 0, 0.05, "Hypervolume")
        text(draw, (x0 + 450, 115), title_value, 32, anchor="ma", bold=True)
        group_w = 210
        for i, row in sub.iterrows():
            xc = x0 + 150 + i * 280
            scale = (box[3] - box[1]) / 0.05
            y_cars = box[3] - float(row["cars_mean"]) * scale
            y_nsga = box[3] - float(row["nsga_reference"]) * scale
            draw.rectangle((xc - 72, y_cars, xc - 4, box[3]), fill=BLUE, outline=INK)
            draw.rectangle((xc + 4, y_nsga, xc + 72, box[3]), fill=GRAY, outline=INK)
            err = float(row["cars_std"]) * scale
            draw.line((xc - 38, y_cars-err, xc - 38, y_cars+err), fill=INK, width=3)
            draw.line((xc - 50, y_cars-err, xc - 26, y_cars-err), fill=INK, width=3)
            draw.line((xc - 50, y_cars+err, xc - 26, y_cars+err), fill=INK, width=3)
            text(draw, (xc, box[3] + 25), str(row["label"]), 24, anchor="ma")
    draw.rectangle((720, 1020, 750, 1050), fill=BLUE, outline=INK)
    text(draw, (765, 1035), "CARS-MODE mean +/- SD", 27, anchor="lm")
    draw.rectangle((1270, 1020, 1300, 1050), fill=GRAY, outline=INK)
    text(draw, (1315, 1035), "Matched NSGA-II mean", 27, anchor="lm")
    save(image, "manuscript/figures/fig_sensitivity.png")


def figure_portfolio(tables: dict[str, pd.DataFrame]) -> None:
    methods = ["CARS-MODE", "Ablation-FixedDE", "NSGA-II", "Standard DE"]
    frame = tables["composition"].set_index("method").loc[methods]
    actions = [("reinforcement", BLUE), ("storage", ORANGE), ("der", TEAL), ("automation", GRAY)]
    image, draw = canvas(2200, 1180)
    text(draw, (1100, 42), "Configuration-equal compromise composition", 42, anchor="ma", bold=True)
    box = (180, 150, 2080, 920)
    ymax = math.ceil(frame[[a for a, _ in actions]].to_numpy().max() + 1)
    axes(draw, box, 0, ymax, "Mean selected actions")
    x0, y0, x1, y1 = box
    group_centers = [x0 + (x1-x0)*(i+.5)/len(methods) for i in range(len(methods))]
    bar_w = 55
    for mi, method in enumerate(methods):
        for ai, (action, color) in enumerate(actions):
            value = float(frame.loc[method, action])
            xc = group_centers[mi] + (ai-1.5)*bar_w
            y = y1 - value/ymax*(y1-y0)
            draw.rectangle((xc-bar_w*.42, y, xc+bar_w*.42, y1), fill=color, outline=INK)
        text(draw, (group_centers[mi], y1+30), method.replace("Ablation-", ""), 25, anchor="ma")
    lx = 520
    for action, color in actions:
        draw.rectangle((lx, 1040, lx+28, 1068), fill=color, outline=INK)
        text(draw, (lx+40, 1054), action.capitalize(), 26, anchor="lm")
        lx += 330
    text(draw, (1100, 1135), "All rerun seed compromises; not the three run-index-0 compositions evaluated in the archived AC panel.", 25, anchor="ma")
    save(image, "manuscript/figures/fig_portfolio_composition.png")


def figure_decision_value(tables: dict[str, pd.DataFrame]) -> None:
    frame = tables["ac_decision"].sort_values("net_feasible_case_change", ascending=False)
    labels = frame["method"].str.replace("Ablation-", "", regex=False).tolist()
    colors = [BLUE if m == "CARS-MODE" else (ORANGE if m == "Ablation-FixedDE" else GRAY) for m in frame["method"]]
    image, draw = canvas(2500, 1530)
    text(draw, (1250, 38), "Decision-screening signals relative to the same No-Plan cases", 42, anchor="ma", bold=True)
    text(draw, (625, 115), "Net AC-feasible case change", 32, anchor="ma", bold=True)
    horizontal_bars(draw, (420, 170, 1180, 1280), labels, frame["net_feasible_case_change"].astype(float).tolist(), colors, -2, 15,
                    "Cases (11 methods x 72 dependent rows)", ".0f")
    text(draw, (1875, 115), "Median maximum-loading change", 32, anchor="ma", bold=True)
    horizontal_bars(draw, (1670, 170, 2430, 1280), labels, frame["median_paired_max_loading_delta_pct_point"].astype(float).tolist(), colors, -36, 5,
                    "Percentage points vs No-Plan", ".1f")
    text(draw, (1250, 1435), "Negative loading change is favorable. These paired summaries diagnose three mapped compositions; they do not certify physical feasibility.", 27, anchor="ma")
    save(image, "manuscript/figures/fig_decision_value.png")


def figure_ac_margin(tables: dict[str, pd.DataFrame]) -> None:
    frame = tables["ac_summary"].sort_values("median_max_line_loading_pct")
    labels = frame["method"].str.replace("Ablation-", "", regex=False).str.replace("NoPlan", "No-Plan", regex=False).tolist()
    image, draw = canvas(2250, 1500)
    text(draw, (1125, 40), "Archived maximum line-loading distribution summaries", 42, anchor="ma", bold=True)
    x0, y0, x1, y1 = 480, 140, 2100, 1280
    row_h = (y1-y0)/len(frame)
    for i, (_, row) in enumerate(frame.iterrows()):
        yc=y0+row_h*(i+.5)
        text(draw,(x0-20,yc),labels[i],23,anchor="rm")
        med=float(row["median_max_line_loading_pct"]); p95=float(row["p95_max_line_loading_pct"])
        col=BLUE if row["method"]=="CARS-MODE" else (ORANGE if row["method"]=="Ablation-FixedDE" else GRAY)
        draw.line((x0+med/170*(x1-x0),yc,x0+p95/170*(x1-x0),yc),fill=col,width=8)
        draw.ellipse((x0+med/170*(x1-x0)-9,yc-9,x0+med/170*(x1-x0)+9,yc+9),fill=col,outline=INK)
        draw.rectangle((x0+p95/170*(x1-x0)-8,yc-8,x0+p95/170*(x1-x0)+8,yc+8),fill=WHITE,outline=col,width=4)
    for tick in [0,50,100,150]:
        x=x0+tick/170*(x1-x0); draw.line((x,y0,x,y1),fill=LIGHT,width=2); text(draw,(x,y1+25),str(tick),24,anchor="ma")
    x100=x0+100/170*(x1-x0);draw.line((x100,y0,x100,y1),fill=RED,width=4)
    text(draw,((x0+x1)/2,y1+85),"Maximum line loading (%)",28,anchor="ma")
    text(draw,(1125,1420),"Filled circle: median; open square: 95th percentile; red line: 100% thermal criterion.",26,anchor="ma")
    save(image,"manuscript/figures/fig_ac_margin_distribution.png")


def figure_direct_de(manifest: dict, tables: dict[str, pd.DataFrame]) -> None:
    methods=[("CARS-MODE",BLUE,"circle"),("GDE3",ORANGE,"square"),("NSDE",TEAL,"triangle")]
    cfgs=manifest["configuration_contract"]
    frame=tables["configuration_means"].set_index(["configuration_id","method"])
    image,draw=canvas(2200,1180)
    text(draw,(1100,42),"Direct multi-objective DE controls by configuration",42,anchor="ma",bold=True)
    box=(180,150,2070,900);axes(draw,box,0.03,0.052,"Sampled/clipped HV")
    x0,y0,x1,y1=box;xs=[x0+(x1-x0)*(i+.5)/len(cfgs) for i in range(len(cfgs))]
    for method,color,shape in methods:
        pts=[]
        for x,cfg in zip(xs,cfgs):
            value=float(frame.loc[(cfg["configuration_id"],method),"mean_legacy_hv_sampled_clip_ref110"])
            y=y1-(value-.03)/(.052-.03)*(y1-y0);pts.append((x,y))
        draw.line(pts,fill=color,width=7)
        for x,y in pts:draw_marker(draw,x,y,color,shape)
    for x,cfg in zip(xs,cfgs):text(draw,(x,y1+30),cfg["short_label"].replace(" ","\n",1),24,anchor="ma")
    lx=650
    for method,color,shape in methods:
        draw_marker(draw,lx,1050,color,shape);text(draw,(lx+25,1050),method,27,anchor="lm");lx+=420
    text(draw,(1100,1135),"The base point pools the primary and replicate seed blocks; the plot contains six configurations.",25,anchor="ma")
    save(image,"manuscript/figures/fig_direct_de_controls.png")


def generate_figures(manifest: dict, manifest_path: Path) -> None:
    renderer = ROOT / "scripts/generate_p3_s4_figures.ps1"
    subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(renderer),
            "-Manifest",
            str(manifest_path),
        ],
        cwd=ROOT,
        check=True,
    )
    for relative in manifest["artifact_outputs"]["figures"]:
        path = ROOT / relative
        if not path.is_file() or path.stat().st_size < 1024:
            raise RuntimeError(f"figure generation failed: {path}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--tables-only", action="store_true")
    args = parser.parse_args()
    manifest = load_manifest(args.manifest.resolve())
    tables = prepare_tables(manifest)
    if not args.tables_only:
        generate_figures(manifest, args.manifest.resolve())
    print(f"OK: regenerated P3 S4 artifacts from {args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
