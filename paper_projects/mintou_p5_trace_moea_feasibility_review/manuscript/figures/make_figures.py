"""Regenerate TRACE-MOEA result tables and Figures 2--8.

Inputs are pinned by ``manuscript/RESULTS_ARTIFACT_MANIFEST.json``.  The script
verifies every source digest before reading data, writes reader-facing derived
CSV tables, and renders the manuscript's result figures as SVG and 300-DPI PNG.
It uses only pandas, NumPy, and Pillow because this host's Matplotlib extension
is built for a different Python ABI.

Inference scopes remain separate: the 0.89% pooled mean gap is descriptive;
stochastic p-values are Holm-adjusted across 12 opponents within scenario; the
preference ablation receives a second Holm adjustment across seven scenarios;
and deterministic, matched-output, sensitivity, and public-record comparisons
remain descriptive.
"""

from __future__ import annotations

import hashlib
from html import escape
import json
import math
from pathlib import Path
import struct
import zlib

import numpy as np
import pandas as pd


SCRIPT = Path(__file__).resolve()
PROJECT = SCRIPT.parents[2]
ROOT = SCRIPT.parents[4]
MANUSCRIPT = PROJECT / "manuscript"
OUT = SCRIPT.parent
TABLES = MANUSCRIPT / "derived_tables"
MANIFEST_PATH = MANUSCRIPT / "RESULTS_ARTIFACT_MANIFEST.json"

INK = "#111111"
INK2 = "#4D4D4D"
MUTED = "#777777"
GRID = "#DEDEDE"
SURFACE = "#FFFFFF"
BLUE = "#0077BB"
CYAN = "#33BBEE"
TEAL = "#009988"
ORANGE = "#EE7733"
MAGENTA = "#EE3377"
GREY = "#BBBBBB"
PURPLE = "#6F4E9C"

METHOD_COLORS = {
    "TRACE-MOEA": BLUE,
    "NSGA-II": TEAL,
    "R-NSGA-II": ORANGE,
    "MOEA/D": PURPLE,
    "AHP-TOPSIS": "#D99A00",
    "Weighted Sum": MAGENTA,
    "Greedy BCR": "#777777",
    "Random Feasible": "#56B4E9",
    "Ablation-NoScheduleRisk": "#8DB7E8",
    "Ablation-NoPreferenceRanking": CYAN,
    "Ablation-NoFeasibilityRepair": "#7AC7B7",
    "Ablation-NSGA2Only": GREY,
    "Ablation-NoRenewableFeatures": "#B9A1D6",
    "Ablation-SingleObjective": "#E7A2BB",
    "Ablation-NoReliabilityFeatures": "#E8BE6B",
    "Ablation-SmallProjectPool": "#AAAAAA",
}

SCENARIOS = [
    "benchmark_portfolio_optimization",
    "distribution_project_review",
    "reliability_driven_review",
    "renewable_accommodation_review",
    "budget_ranking_stability",
    "preference_aware_support",
    "traceability_evaluation",
]
SCENARIO_LABELS = {
    "benchmark_portfolio_optimization": "Benchmark|portfolio",
    "distribution_project_review": "Distribution|review",
    "reliability_driven_review": "Reliability-|driven",
    "renewable_accommodation_review": "Renewable|support",
    "budget_ranking_stability": "Budget|stability",
    "preference_aware_support": "Preference-|aware",
    "traceability_evaluation": "Traceability|scenario",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_sources() -> tuple[dict, dict[str, Path], dict[str, pd.DataFrame]]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    paths: dict[str, Path] = {}
    frames: dict[str, pd.DataFrame] = {}
    for key, entry in manifest["sources"].items():
        path = ROOT / Path(entry["path"])
        if not path.is_file():
            raise FileNotFoundError(f"manifest source missing: {key}: {path}")
        actual = sha256(path)
        if actual != entry["sha256"]:
            raise RuntimeError(
                f"manifest hash mismatch for {key}: expected {entry['sha256']}, got {actual}"
            )
        paths[key] = path
        if path.suffix.lower() == ".csv":
            frames[key] = pd.read_csv(path)

    main_config = json.loads(paths["main_config"].read_text(encoding="utf-8"))
    stage_config = json.loads(paths["stage_config_snapshot"].read_text(encoding="utf-8"))
    if main_config["status"] != manifest["main_run_status"]:
        raise RuntimeError("main-run status does not match the accepted manifest")
    if main_config["experiments"] != SCENARIOS:
        raise RuntimeError("main-run scenarios differ from the accepted design")
    if main_config["seeds_per_method_per_experiment"] != 30:
        raise RuntimeError("main-run seed count differs from the accepted design")
    if stage_config["status"] != "prespecified_before_execution":
        raise RuntimeError("stage-local configuration is not the frozen prespecification")
    if stage_config["scenarios"] != SCENARIOS:
        raise RuntimeError("stage-local scenarios differ from the accepted design")
    return manifest, paths, frames


def holm_adjust(values: pd.Series) -> pd.Series:
    raw = values.astype(float).to_numpy()
    order = np.argsort(raw, kind="stable")
    adjusted = np.empty_like(raw)
    running = 0.0
    total = len(raw)
    for rank, index in enumerate(order):
        running = max(running, min(1.0, (total - rank) * raw[index]))
        adjusted[index] = running
    return pd.Series(adjusted, index=values.index)


def write_csv(frame: pd.DataFrame, name: str) -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    frame.to_csv(TABLES / name, index=False, float_format="%.10g", lineterminator="\n")


def generate_tables(frames: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    runs = frames["main_runs"].copy()
    inference = frames["main_inference"].copy()
    expected = 16 * 7 * 30
    if len(runs) != expected:
        raise RuntimeError(f"main run count is {len(runs)}, expected {expected}")

    leaderboard = (
        runs.groupby(["method", "method_role"], as_index=False)
        .agg(
            runs=("hypervolume", "size"),
            mean_hypervolume=("hypervolume", "mean"),
            std_hypervolume=("hypervolume", lambda x: x.std(ddof=1)),
            mean_runtime_s=("runtime_s", "mean"),
            mean_repair_drop_records=("local_move_count", "mean"),
            mean_total_event_records=("trace_event_count", "mean"),
            mean_position_cooccurrence=("decision_coverage", "mean"),
        )
        .sort_values("mean_hypervolume", ascending=False)
    )
    write_csv(leaderboard, "p5_main_leaderboard.csv")

    nsga = inference[inference["opponent"] == "NSGA-II"].copy()
    nsga["multiplicity_family"] = "12 stochastic opponents within scenario"
    write_csv(nsga, "p5_nsga2_scenario_comparison.csv")

    component = inference[
        inference["opponent"].isin(
            ["Ablation-NoPreferenceRanking", "Ablation-NoScheduleRisk"]
        )
    ].copy()
    component["p_holm_across_seven_scenarios"] = component.groupby("opponent")[
        "p_raw"
    ].transform(holm_adjust)
    component["significant_005_across_scenarios"] = (
        component["p_holm_across_seven_scenarios"] < 0.05
    )
    component["within_scenario_family"] = "12 stochastic opponents"
    component["across_scenario_family"] = "7 raw scenario contrasts per component"
    write_csv(component, "p5_component_multiplicity.csv")

    budget_summary = frames["preference_budget_summary"].copy()
    budget_inference = frames["preference_budget_inference"].copy()
    budget_rows: list[dict] = []
    for row in budget_summary.to_dict(orient="records"):
        out = dict(row)
        if row["method"] == "TRACE-MOEA":
            out.update(
                comparison="reference method",
                mean_difference=np.nan,
                p_holm=np.nan,
                significant_005_holm=np.nan,
                hv_inference_scope="reference cell",
            )
        else:
            label = f"TRACE-MOEA vs {row['method']}"
            match = budget_inference[
                (budget_inference["budget_multiplier"] == row["budget_multiplier"])
                & (budget_inference["comparison"] == label)
            ]
            if len(match) != 1:
                raise RuntimeError(f"missing matched-budget inference row: {label}")
            sig = match.iloc[0]
            out.update(
                comparison=label,
                mean_difference=sig["mean_diff"],
                p_holm=sig["p_holm"],
                significant_005_holm=sig["significant_005_holm"],
                hv_inference_scope="2 comparators within budget",
            )
        out["preference_distance_scope"] = "descriptive"
        budget_rows.append(out)
    budget = pd.DataFrame(budget_rows)
    write_csv(budget, "p5_matched_budget_controls.csv")

    matched = frames["matched_output_summary"].copy()
    matched["comparison_scope"] = "descriptive matched one-output attributes"
    write_csv(matched, "p5_matched_output_summary.csv")

    bounds = frames["normalization_bounds"].copy()
    write_csv(
        bounds[bounds["scenario"] == SCENARIOS[0]].copy(),
        "p5_normalization_bounds_benchmark.csv",
    )

    norm = frames["normalization_summary"].copy()
    norm_pooled = (
        norm.groupby(["method", "method_type"], as_index=False)
        .agg(
            reported_clipped_ref1p1=("mean_hv_reported_empirical_ref1p1_clipped", "mean"),
            reported_unclipped_ref1p1=("mean_hv_reported_empirical_ref1p1_unclipped", "mean"),
            expanded_unclipped_ref1p1=("mean_hv_expanded_empirical_ref1p1_unclipped", "mean"),
            analytic_ref1p1=("mean_hv_analytic_ref1p1_unclipped", "mean"),
            analytic_ref1p2=("mean_hv_analytic_ref1p2_unclipped", "mean"),
        )
        .sort_values("reported_clipped_ref1p1", ascending=False)
    )
    norm_pooled["comparison_scope"] = "descriptive bound/reference sensitivity"
    write_csv(norm_pooled, "p5_normalization_summary.csv")

    clipping = frames["clipping_summary"]
    total_points = int(clipping["front_points"].sum())
    clipping_totals = pd.DataFrame(
        [
            {
                "front_points": total_points,
                "reported_clipped_points": int(clipping["reported_clipped_points"].sum()),
                "reported_point_clip_rate": clipping["reported_clipped_points"].sum()
                / total_points,
                "expanded_clipped_points": int(clipping["expanded_clipped_points"].sum()),
                "expanded_point_clip_rate": clipping["expanded_clipped_points"].sum()
                / total_points,
                "analytic_clipped_points_beyond_1e_12": int(
                    clipping["analytic_clipped_points"].sum()
                ),
                "analytic_point_clip_rate_beyond_1e_12": clipping[
                    "analytic_clipped_points"
                ].sum()
                / total_points,
            }
        ]
    )
    write_csv(clipping_totals, "p5_clipping_totals.csv")

    sensitivity = frames["sensitivity_effects"].copy()
    sensitivity["comparison_scope"] = "descriptive; no p-values"
    write_csv(sensitivity, "p5_sensitivity_effects.csv")

    event_methods = [
        "TRACE-MOEA",
        "Ablation-NoPreferenceRanking",
        "Ablation-NoFeasibilityRepair",
    ]
    events = leaderboard[leaderboard["method"].isin(event_methods)].copy()
    events["record_scope"] = "implemented in-memory event records summarized per run"
    events["lineage_or_replay"] = "not supported by released rows"
    write_csv(events, "p5_event_record_summary.csv")

    search_event = leaderboard[
        leaderboard["method"].isin(event_methods + ["NSGA-II"])
    ].copy()
    search_event["event_fields"] = np.where(
        search_event["method"] == "NSGA-II", "not instrumented", "reported"
    )
    write_csv(search_event, "p5_search_event_efficiency.csv")

    nerc = frames["nerc_descriptive"].copy()
    nerc["comparison_scope"] = "descriptive external consistency"
    write_csv(nerc, "p5_nerc_descriptive_summary.csv")

    mtep = frames["mtep_descriptive"].copy()
    mtep["comparison_scope"] = "descriptive; project-level dependence not preserved"
    write_csv(mtep, "p5_mtep_outcome_summary.csv")

    return {
        "runs": runs,
        "leaderboard": leaderboard,
        "component": component,
        "budget": budget,
        "search_event": search_event,
        "nerc": nerc,
        "mtep": mtep,
    }


class SVG:
    """Small publication-chart renderer with a deterministic SVG surface."""

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.items = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            f'<rect width="{width}" height="{height}" fill="{SURFACE}"/>',
            '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#111} .tick{font-size:15px;fill:#4D4D4D} .axis{font-size:17px} .title{font-size:18px;font-weight:600}</style>',
        ]

    def line(self, x1: float, y1: float, x2: float, y2: float, **attrs: object) -> None:
        params = {"stroke": INK, "stroke-width": 1, **attrs}
        self.items.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" {_attrs(params)}/>' )

    def rect(self, x: float, y: float, w: float, h: float, **attrs: object) -> None:
        params = {"fill": "none", **attrs}
        self.items.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" {_attrs(params)}/>' )

    def circle(self, x: float, y: float, r: float, **attrs: object) -> None:
        params = {"fill": INK, **attrs}
        self.items.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" {_attrs(params)}/>' )

    def polygon(self, points: list[tuple[float, float]], **attrs: object) -> None:
        value = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
        params = {"fill": INK, **attrs}
        self.items.append(f'<polygon points="{value}" {_attrs(params)}/>' )

    def text(
        self,
        x: float,
        y: float,
        value: object,
        *,
        anchor: str = "start",
        css: str = "tick",
        rotate: float | None = None,
        weight: str | None = None,
    ) -> None:
        transform = f' transform="rotate({rotate} {x:.2f} {y:.2f})"' if rotate else ""
        font_weight = f' font-weight="{weight}"' if weight else ""
        self.items.append(
            f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}" class="{css}"{transform}{font_weight}>{escape(str(value))}</text>'
        )

    def save(self, stem: str) -> None:
        self.items.append("</svg>")
        svg_path = OUT / f"{stem}.svg"
        svg_path.write_text("\n".join(self.items) + "\n", encoding="utf-8")
        rasterize(svg_path, OUT / f"{stem}.png", self.width, self.height)


def _attrs(attrs: dict[str, object]) -> str:
    return " ".join(f'{name.replace("_", "-")}="{escape(str(value))}"' for name, value in attrs.items())


FONT_5X7 = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01111", "10000", "10000", "10000", "10000", "10000", "01111"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01111", "10000", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("11111", "00100", "00100", "00100", "00100", "00100", "11111"),
    "J": ("00111", "00010", "00010", "00010", "10010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "10000", "11110", "00001", "00001", "11110"),
    "6": ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    ".": ("00000", "00000", "00000", "00000", "00000", "00110", "00110"),
    ",": ("00000", "00000", "00000", "00000", "00110", "00110", "00100"),
    ":": ("00000", "00110", "00110", "00000", "00110", "00110", "00000"),
    ";": ("00000", "00110", "00110", "00000", "00110", "00110", "00100"),
    "-": ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "%": ("11001", "11010", "00100", "01000", "10110", "00110", "00000"),
    "=": ("00000", "11111", "00000", "11111", "00000", "00000", "00000"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    " ": ("00000",) * 7,
    "?": ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
}


class Raster:
    def __init__(self, width: int, height: int, scale_factor: int = 2) -> None:
        self.factor = scale_factor
        self.width = width * scale_factor
        self.height = height * scale_factor
        self.pixels = bytearray(b"\xff\xff\xff") * (self.width * self.height)

    @staticmethod
    def color(value: str | None) -> tuple[int, int, int]:
        if not value or value == "none":
            return (255, 255, 255)
        value = value.lstrip("#")
        return tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))  # type: ignore[return-value]

    def pixel(self, x: int, y: int, color: tuple[int, int, int]) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            offset = (y * self.width + x) * 3
            self.pixels[offset : offset + 3] = bytes(color)

    def line(self, x1: float, y1: float, x2: float, y2: float, color: str, width: float = 1) -> None:
        x1, y1, x2, y2 = [round(value * self.factor) for value in (x1, y1, x2, y2)]
        rgb = self.color(color)
        dx, dy = abs(x2 - x1), -abs(y2 - y1)
        sx, sy = (1 if x1 < x2 else -1), (1 if y1 < y2 else -1)
        error = dx + dy
        radius = max(0, round(width * self.factor / 2) - 1)
        while True:
            for ox in range(-radius, radius + 1):
                for oy in range(-radius, radius + 1):
                    self.pixel(x1 + ox, y1 + oy, rgb)
            if x1 == x2 and y1 == y2:
                break
            twice = 2 * error
            if twice >= dy:
                error += dy
                x1 += sx
            if twice <= dx:
                error += dx
                y1 += sy

    def rect(self, x: float, y: float, w: float, h: float, fill: str | None, stroke: str | None = None) -> None:
        x0, y0, x1, y1 = [round(value * self.factor) for value in (x, y, x + w, y + h)]
        if fill and fill != "none":
            rgb = self.color(fill)
            for py in range(max(0, y0), min(self.height, y1 + 1)):
                for px in range(max(0, x0), min(self.width, x1 + 1)):
                    self.pixel(px, py, rgb)
        if stroke:
            self.line(x, y, x + w, y, stroke)
            self.line(x + w, y, x + w, y + h, stroke)
            self.line(x + w, y + h, x, y + h, stroke)
            self.line(x, y + h, x, y, stroke)

    def circle(self, x: float, y: float, radius: float, fill: str) -> None:
        cx, cy, r = round(x * self.factor), round(y * self.factor), round(radius * self.factor)
        rgb = self.color(fill)
        for py in range(cy - r, cy + r + 1):
            width = round(math.sqrt(max(0, r * r - (py - cy) ** 2)))
            for px in range(cx - width, cx + width + 1):
                self.pixel(px, py, rgb)

    def polygon(self, points: list[tuple[float, float]], fill: str) -> None:
        pts = [(x * self.factor, y * self.factor) for x, y in points]
        rgb = self.color(fill)
        min_y, max_y = math.floor(min(y for _, y in pts)), math.ceil(max(y for _, y in pts))
        for py in range(min_y, max_y + 1):
            intersections = []
            for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
                if (y1 <= py < y2) or (y2 <= py < y1):
                    intersections.append(x1 + (py - y1) * (x2 - x1) / (y2 - y1))
            intersections.sort()
            for start, end in zip(intersections[::2], intersections[1::2]):
                for px in range(math.ceil(start), math.floor(end) + 1):
                    self.pixel(px, py, rgb)

    def text(self, x: float, y: float, value: str, anchor: str, css: str, rotate: float | None) -> None:
        # The SVG retains proper rotated axis labels.  The dependency-free PNG
        # rasterizer omits them rather than risk placing low-resolution bitmap
        # text inside the data region; panel titles and captions retain units.
        if rotate == -90:
            return
        dot = {"tick": 3, "axis": 4, "title": 4}.get(css, 3)
        value = value.upper()
        glyph_w, glyph_h = 6 * dot, 7 * dot
        width = max(0, len(value) * glyph_w - dot)
        if anchor == "middle":
            x = x * self.factor - width / 2
        elif anchor == "end":
            x = x * self.factor - width
        else:
            x *= self.factor
        y = y * self.factor - glyph_h
        rgb = self.color(INK)
        points: list[tuple[int, int]] = []
        cursor = 0
        for char in value:
            glyph = FONT_5X7.get(char, FONT_5X7["?"])
            for row, bits in enumerate(glyph):
                for col, bit in enumerate(bits):
                    if bit == "1":
                        for ox in range(dot):
                            for oy in range(dot):
                                points.append((round(x + cursor + col * dot + ox), round(y + row * dot + oy)))
            cursor += glyph_w
        for px, py in points:
            self.pixel(px, py, rgb)

    def save(self, path: Path) -> None:
        raw = b"".join(
            b"\x00" + bytes(self.pixels[row * self.width * 3 : (row + 1) * self.width * 3])
            for row in range(self.height)
        )
        def chunk(kind: bytes, data: bytes) -> bytes:
            return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        payload = b"\x89PNG\r\n\x1a\n"
        payload += chunk(b"IHDR", struct.pack(">IIBBBBB", self.width, self.height, 8, 2, 0, 0, 0))
        payload += chunk(b"pHYs", struct.pack(">IIB", 11811, 11811, 1))
        payload += chunk(b"IDAT", zlib.compress(raw, level=9))
        payload += chunk(b"IEND", b"")
        path.write_bytes(payload)


def rasterize(svg_path: Path, png_path: Path, width: int, height: int) -> None:
    """Rasterize this script's closed SVG vocabulary using only stdlib code."""
    import xml.etree.ElementTree as et

    canvas = Raster(width, height)
    for element in et.parse(svg_path).getroot():
        tag = element.tag.split("}")[-1]
        a = element.attrib
        if tag in {"style"}:
            continue
        if tag == "rect":
            canvas.rect(
                float(a.get("x", 0)),
                float(a.get("y", 0)),
                float(a.get("width", width)),
                float(a.get("height", height)),
                a.get("fill"),
                a.get("stroke"),
            )
        elif tag == "line":
            canvas.line(
                float(a["x1"]), float(a["y1"]), float(a["x2"]), float(a["y2"]),
                a.get("stroke", INK), float(a.get("stroke-width", 1)),
            )
        elif tag == "circle":
            canvas.circle(float(a["cx"]), float(a["cy"]), float(a["r"]), a.get("fill", INK))
        elif tag == "polygon":
            points = [tuple(float(part) for part in pair.split(",")) for pair in a["points"].split()]
            canvas.polygon(points, a.get("fill", INK))  # type: ignore[arg-type]
        elif tag == "text":
            rotation = -90.0 if "rotate(-90" in a.get("transform", "") else None
            canvas.text(
                float(a["x"]), float(a["y"]), element.text or "", a.get("text-anchor", "start"),
                a.get("class", "tick"), rotation,
            )
    canvas.save(png_path)


def scale(value: float, low: float, high: float, start: float, end: float) -> float:
    if high == low:
        return (start + end) / 2
    return start + (float(value) - low) / (high - low) * (end - start)


def axes(svg: SVG, left: float, top: float, right: float, bottom: float, y_ticks: list[float], y_min: float, y_max: float) -> None:
    for tick in y_ticks:
        y = scale(tick, y_min, y_max, bottom, top)
        svg.line(left, y, right, y, stroke=GRID, **{"stroke-width": 1})
        svg.text(left - 8, y + 5, f"{tick:g}", anchor="end")
    svg.line(left, top, left, bottom, stroke=INK2)
    svg.line(left, bottom, right, bottom, stroke=INK2)


def quantiles(values: np.ndarray) -> tuple[float, float, float, float, float]:
    return tuple(float(value) for value in np.quantile(values, [0, 0.25, 0.5, 0.75, 1]))  # type: ignore[return-value]


def fig_hv_boxplot(runs: pd.DataFrame) -> None:
    methods = [
        "TRACE-MOEA",
        "NSGA-II",
        "AHP-TOPSIS",
        "MOEA/D",
        "Weighted Sum",
        "Greedy BCR",
        "Random Feasible",
    ]
    deterministic = {"AHP-TOPSIS", "Weighted Sum", "Greedy BCR"}
    svg = SVG(1500, 700)
    left, top, right, bottom = 95, 55, 1460, 500
    axes(svg, left, top, right, bottom, [0, 0.05, 0.10, 0.15, 0.20], 0, 0.21)
    group = (right - left) / len(SCENARIOS)
    step = group * 0.84 / len(methods)
    for scenario_index, scenario in enumerate(SCENARIOS):
        center = left + group * (scenario_index + 0.5)
        for method_index, method in enumerate(methods):
            vals = runs.loc[
                (runs["experiment_id"] == scenario) & (runs["method"] == method),
                "hypervolume",
            ].to_numpy()
            x = center + (method_index - (len(methods) - 1) / 2) * step
            color = METHOD_COLORS[method]
            if method in deterministic:
                y = scale(float(vals[0]), 0, 0.21, bottom, top)
                svg.polygon([(x, y - 7), (x + 7, y), (x, y + 7), (x - 7, y)], fill=color)
            else:
                vmin, q1, med, q3, vmax = quantiles(vals)
                y_min, y1, y_med, y3, y_max = [scale(v, 0, 0.21, bottom, top) for v in (vmin, q1, med, q3, vmax)]
                svg.line(x, y_min, x, y_max, stroke=color)
                svg.rect(x - step * 0.32, y3, step * 0.64, y1 - y3, fill=color, opacity=0.80)
                svg.line(x - step * 0.32, y_med, x + step * 0.32, y_med, stroke=INK)
        for line_index, line in enumerate(SCENARIO_LABELS[scenario].split("|")):
            svg.text(center, bottom + 30 + line_index * 18, line, anchor="middle")
    svg.text((left + right) / 2, 580, "Review scenario", anchor="middle", css="axis")
    svg.text(22, (top + bottom) / 2, "Feasible-front hypervolume", anchor="middle", css="axis", rotate=-90)
    legend_y = 625
    legend_x = 90
    for index, method in enumerate(methods):
        x = legend_x + (index % 4) * 330
        y = legend_y + (index // 4) * 24
        svg.rect(x, y - 10, 16, 10, fill=METHOD_COLORS[method])
        suffix = " (deterministic)" if method in deterministic else ""
        svg.text(x + 23, y, method + suffix)
    svg.save("fig_hv_boxplot")


def fig_ablation(runs: pd.DataFrame, component: pd.DataFrame) -> None:
    labels = {
        "TRACE-MOEA": "TRACE-MOEA (full)",
        "Ablation-NoScheduleRisk": "No schedule-risk objective",
        "Ablation-NoPreferenceRanking": "No preference adaptation",
        "Ablation-NoFeasibilityRepair": "No budget repair",
        "Ablation-NSGA2Only": "Bare constrained kernel",
        "Ablation-NoRenewableFeatures": "No renewable objective",
        "Ablation-SingleObjective": "Scalarized single objective",
        "Ablation-NoReliabilityFeatures": "No reliability objective",
        "Ablation-SmallProjectPool": "One-third candidate pool",
    }
    summary = (
        runs[runs["method"].isin(labels)]
        .groupby("method")["hypervolume"]
        .agg(mean="mean", std=lambda x: x.std(ddof=1))
        .sort_values("mean")
    )
    svg = SVG(1200, 710)
    left, top, right, bottom = 330, 40, 1150, 535
    row = (bottom - top) / len(summary)
    for tick in np.arange(0, 0.221, 0.05):
        x = scale(tick, 0, 0.22, left, right)
        svg.line(x, top, x, bottom, stroke=GRID)
        svg.text(x, bottom + 24, f"{tick:.2f}", anchor="middle")
    nsga = runs.loc[runs["method"] == "NSGA-II", "hypervolume"].mean()
    nsga_x = scale(nsga, 0, 0.22, left, right)
    svg.line(nsga_x, top, nsga_x, bottom, stroke=TEAL, **{"stroke-dasharray": "6 5", "stroke-width": 2})
    for index, (method, values) in enumerate(summary.iterrows()):
        y = bottom - row * (index + 0.5)
        x = scale(values["mean"], 0, 0.22, left, right)
        err_l = scale(values["mean"] - values["std"], 0, 0.22, left, right)
        err_r = scale(values["mean"] + values["std"], 0, 0.22, left, right)
        svg.rect(left, y - row * 0.29, x - left, row * 0.58, fill=METHOD_COLORS[method])
        svg.line(err_l, y, err_r, y, stroke=INK2)
        svg.line(err_l, y - 4, err_l, y + 4, stroke=INK2)
        svg.line(err_r, y - 4, err_r, y + 4, stroke=INK2)
        svg.text(left - 12, y + 5, labels[method], anchor="end", weight="bold" if method == "TRACE-MOEA" else None)
    pref_min = component.loc[
        component["opponent"] == "Ablation-NoPreferenceRanking",
        "p_holm_across_seven_scenarios",
    ].min()
    svg.text(left, 585, "NSGA-II 0.17270; pooled TRACE gap +0.89% (descriptive)", css="axis")
    svg.text(left, 615, f"No-preference pooled gap +0.17%; 7-scenario Holm minimum p = {pref_min:.4f}", css="axis")
    svg.text((left + right) / 2, 680, "Pooled mean feasible-front hypervolume (whisker: run-level SD)", anchor="middle", css="axis")
    svg.save("fig_ablation")


def boxplot_panel(svg: SVG, data: list[np.ndarray], labels: list[str], colors: list[str], bounds: tuple[int, int, int, int], y_min: float, y_max: float, ticks: list[float], title: str, ylabel: str) -> None:
    left, top, right, bottom = bounds
    axes(svg, left, top, right, bottom, ticks, y_min, y_max)
    width = (right - left) / len(data)
    for index, (values, label, color) in enumerate(zip(data, labels, colors)):
        x = left + width * (index + 0.5)
        vmin, q1, med, q3, vmax = quantiles(values)
        ys = [scale(v, y_min, y_max, bottom, top) for v in (vmin, q1, med, q3, vmax)]
        svg.line(x, ys[0], x, ys[4], stroke=INK2)
        svg.rect(x - width * 0.22, ys[3], width * 0.44, ys[1] - ys[3], fill=color, opacity=0.78)
        svg.line(x - width * 0.22, ys[2], x + width * 0.22, ys[2], stroke=INK)
        for line_index, line in enumerate(label.split("|")):
            svg.text(x, bottom + 24 + line_index * 17, line, anchor="middle")
    svg.text(left, top - 14, title, css="title")
    svg.text(left - 55, (top + bottom) / 2, ylabel, anchor="middle", css="axis", rotate=-90)


def fig_event_records(runs: pd.DataFrame) -> None:
    methods = ["TRACE-MOEA", "Ablation-NoPreferenceRanking", "Ablation-NoFeasibilityRepair"]
    labels = ["Full|method", "No preference|adaptation", "No budget|repair"]
    colors = [BLUE, CYAN, TEAL]
    svg = SVG(1300, 540)
    boxplot_panel(
        svg,
        [runs.loc[runs["method"] == method, "decision_coverage"].to_numpy() for method in methods],
        labels,
        colors,
        (100, 65, 610, 420),
        0,
        1.05,
        [0, 0.25, 0.5, 0.75, 1.0],
        "(a) Final-front position co-occurrence",
        "Co-occurrence (fraction)",
    )
    boxplot_panel(
        svg,
        [runs.loc[runs["method"] == method, "trace_event_count"].to_numpy() for method in methods],
        labels,
        colors,
        (760, 65, 1260, 420),
        0,
        1800,
        [0, 500, 1000, 1500],
        "(b) Implemented event records",
        "Records per run (count)",
    )
    svg.save("fig_event_record_diagnostics")


def line_panel(svg: SVG, frame: pd.DataFrame, column: str, error: str | None, bounds: tuple[int, int, int, int], y_min: float, y_max: float, y_ticks: list[float], title: str, ylabel: str) -> None:
    left, top, right, bottom = bounds
    axes(svg, left, top, right, bottom, y_ticks, y_min, y_max)
    methods = ["TRACE-MOEA", "NSGA-II", "R-NSGA-II"]
    markers = ["circle", "square", "triangle"]
    for method, marker in zip(methods, markers):
        sub = frame[frame["method"] == method].sort_values("budget_multiplier")
        points = []
        for _, row in sub.iterrows():
            x = scale(row["budget_multiplier"], 0.75, 1.25, left, right)
            y = scale(row[column], y_min, y_max, bottom, top)
            points.append((x, y))
            if error:
                low = scale(row[column] - row[error], y_min, y_max, bottom, top)
                high = scale(row[column] + row[error], y_min, y_max, bottom, top)
                svg.line(x, low, x, high, stroke=METHOD_COLORS[method])
                svg.line(x - 4, low, x + 4, low, stroke=METHOD_COLORS[method])
                svg.line(x - 4, high, x + 4, high, stroke=METHOD_COLORS[method])
        for first, second in zip(points, points[1:]):
            svg.line(*first, *second, stroke=METHOD_COLORS[method], **{"stroke-width": 2})
        for x, y in points:
            if marker == "circle":
                svg.circle(x, y, 6, fill=METHOD_COLORS[method])
            elif marker == "square":
                svg.rect(x - 6, y - 6, 12, 12, fill=METHOD_COLORS[method])
            else:
                svg.polygon([(x, y - 7), (x + 7, y + 6), (x - 7, y + 6)], fill=METHOD_COLORS[method])
    for value in [0.75, 1.00, 1.25]:
        x = scale(value, 0.75, 1.25, left, right)
        svg.text(x, bottom + 25, f"{value:.2f}", anchor="middle")
    svg.text(left, top - 14, title, css="title")
    svg.text((left + right) / 2, bottom + 55, "Budget multiplier (times nominal)", anchor="middle", css="axis")
    svg.text(left - 60, (top + bottom) / 2, ylabel, anchor="middle", css="axis", rotate=-90)


def fig_preference_budget(budget: pd.DataFrame) -> None:
    svg = SVG(1300, 520)
    line_panel(svg, budget, "mean_hypervolume", "std_hypervolume", (100, 65, 610, 390), 0, 0.20, [0, 0.05, 0.10, 0.15, 0.20], "(a) Feasible-front hypervolume", "Mean hypervolume (SD)")
    line_panel(svg, budget, "mean_preference_achievement_distance", None, (760, 65, 1260, 390), 0, 0.60, [0, 0.15, 0.30, 0.45, 0.60], "(b) Preference-achievement distance", "Mean distance (descriptive)")
    for index, method in enumerate(["TRACE-MOEA", "NSGA-II", "R-NSGA-II"]):
        x = 390 + index * 180
        svg.rect(x, 475, 16, 10, fill=METHOD_COLORS[method])
        svg.text(x + 22, 485, method)
    svg.save("fig_preference_budget_controls")


def dot_panel(svg: SVG, frame: pd.DataFrame, column: str, methods: list[str], bounds: tuple[int, int, int, int], x_min: float, x_max: float, ticks: list[float], title: str, xlabel: str) -> None:
    left, top, right, bottom = bounds
    row = (bottom - top) / len(methods)
    for tick in ticks:
        x = scale(tick, x_min, x_max, left, right)
        svg.line(x, top, x, bottom, stroke=GRID)
        svg.text(x, bottom + 24, f"{tick:g}", anchor="middle")
    parity = scale(1.0, x_min, x_max, left, right)
    svg.line(parity, top, parity, bottom, stroke=INK2, **{"stroke-dasharray": "5 4"})
    for scenario, color, shape in zip([SCENARIOS[0], SCENARIOS[2]], [BLUE, ORANGE], ["circle", "square"]):
        for index, method in enumerate(methods):
            row_data = frame[(frame["experiment_id"] == scenario) & (frame["method"] == method)]
            if row_data.empty:
                continue
            value = float(row_data[column].iloc[0])
            if not math.isfinite(value):
                continue
            x = scale(value, x_min, x_max, left, right)
            y = top + row * (index + 0.5)
            if shape == "circle":
                svg.circle(x, y, 6, fill=color)
            else:
                svg.rect(x - 6, y - 6, 12, 12, fill=color)
    for index, method in enumerate(methods):
        y = top + row * (index + 0.5) + 5
        svg.text(left - 12, y, method, anchor="end", weight="bold" if method == "TRACE-MOEA" else None)
    svg.text(left, top - 14, title, css="title")
    svg.text((left + right) / 2, bottom + 55, xlabel, anchor="middle", css="axis")


def fig_external_validity(nerc: pd.DataFrame, mtep: pd.DataFrame) -> None:
    methods = ["TRACE-MOEA", "NSGA-II", "R-NSGA-II", "MOEA/D", "AHP-TOPSIS", "Weighted Sum", "Greedy BCR", "Random Feasible"]
    svg = SVG(1500, 610)
    dot_panel(svg, nerc, "priority_capture_ratio", methods, (170, 70, 700, 485), 0, 2.55, [0, 0.5, 1, 1.5, 2, 2.5], "(a) NERC-rule consistency", "Priority-capture ratio (descriptive)")
    dot_panel(svg, mtep, "outcome_capture_broad", methods, (930, 70, 1450, 485), 0.90, 1.16, [0.90, 1.00, 1.10], "(b) MTEP16 broad-outcome consistency", "Outcome-capture ratio (descriptive)")
    svg.circle(565, 565, 6, fill=BLUE)
    svg.text(580, 570, "Benchmark portfolio")
    svg.rect(820, 559, 12, 12, fill=ORANGE)
    svg.text(840, 570, "Reliability-driven")
    svg.save("fig_external_validity")


def fig_search_event(search_event: pd.DataFrame) -> None:
    methods = ["TRACE-MOEA", "Ablation-NoPreferenceRanking", "Ablation-NoFeasibilityRepair", "NSGA-II"]
    labels = ["Full method", "No preference", "No repair", "NSGA-II"]
    metrics = [
        ("mean_hypervolume", "Hypervolume", 0.18),
        ("mean_runtime_s", "Runtime (s)", 0.16),
        ("mean_repair_drop_records", "Repair records", 850),
        ("mean_total_event_records", "Total records", 1200),
        ("mean_position_cooccurrence", "Position overlap", 1.0),
    ]
    frame = search_event.set_index("method").reindex(methods)
    svg = SVG(1500, 460)
    top, bottom = 70, 340
    row = (bottom - top) / len(methods)
    panel_w = 235
    for panel, (column, title, maximum) in enumerate(metrics):
        left = 260 + panel * panel_w
        right = left + 185
        for tick in np.linspace(0, maximum, 3):
            x = scale(tick, 0, maximum, left, right)
            svg.line(x, top, x, bottom, stroke=GRID)
            svg.text(x, bottom + 22, f"{tick:.2g}", anchor="middle")
        for index, method in enumerate(methods):
            y = top + row * (index + 0.5)
            if method == "NSGA-II" and panel >= 2:
                svg.text(left + 5, y + 5, "not instrumented")
                continue
            value = float(frame.loc[method, column])
            x = scale(value, 0, maximum, left, right)
            svg.circle(x, y, 7, fill=METHOD_COLORS[method])
        svg.text((left + right) / 2, 45, title, anchor="middle", css="title")
    for index, (method, label) in enumerate(zip(methods, labels)):
        y = top + row * (index + 0.5) + 5
        svg.text(240, y, label, anchor="end", weight="bold" if method == "TRACE-MOEA" else None)
    svg.text(750, 425, "Native units shown in separate panels; no composite score", anchor="middle", css="axis")
    svg.save("fig_search_event_efficiency")


def fig_mtep_outcomes(mtep: pd.DataFrame) -> None:
    methods = ["TRACE-MOEA", "NSGA-II", "R-NSGA-II", "MOEA/D", "AHP-TOPSIS", "Weighted Sum", "Greedy BCR", "Random Feasible"]
    svg = SVG(1500, 610)
    dot_panel(svg, mtep, "outcome_capture_broad", methods, (170, 70, 700, 485), 0.90, 1.16, [0.90, 1.00, 1.10], "(a) Broad outcome definition", "Outcome-capture ratio (descriptive)")
    dot_panel(svg, mtep, "outcome_capture_strict", methods, (930, 70, 1450, 485), 0.90, 1.16, [0.90, 1.00, 1.10], "(b) Strict outcome definition", "Outcome-capture ratio (descriptive)")
    svg.circle(565, 565, 6, fill=BLUE)
    svg.text(580, 570, "Benchmark portfolio")
    svg.rect(820, 559, 12, 12, fill=ORANGE)
    svg.text(840, 570, "Reliability-driven")
    svg.save("fig_mtep_outcome_backtest")


def main() -> None:
    _, _, frames = load_sources()
    derived = generate_tables(frames)
    fig_hv_boxplot(derived["runs"])
    fig_ablation(derived["runs"], derived["component"])
    fig_event_records(derived["runs"])
    fig_preference_budget(derived["budget"])
    fig_external_validity(derived["nerc"], derived["mtep"])
    fig_search_event(derived["search_event"])
    fig_mtep_outcomes(derived["mtep"])
    generated_tables = sorted(
        [
            "p5_main_leaderboard.csv",
            "p5_nsga2_scenario_comparison.csv",
            "p5_component_multiplicity.csv",
            "p5_matched_budget_controls.csv",
            "p5_matched_output_summary.csv",
            "p5_normalization_bounds_benchmark.csv",
            "p5_normalization_summary.csv",
            "p5_clipping_totals.csv",
            "p5_sensitivity_effects.csv",
            "p5_event_record_summary.csv",
            "p5_search_event_efficiency.csv",
            "p5_nerc_descriptive_summary.csv",
            "p5_mtep_outcome_summary.csv",
        ]
    )
    generated_figures = sorted(
        [
            "fig_hv_boxplot.png",
            "fig_ablation.png",
            "fig_event_record_diagnostics.png",
            "fig_preference_budget_controls.png",
            "fig_external_validity.png",
            "fig_search_event_efficiency.png",
            "fig_mtep_outcome_backtest.png",
        ]
    )
    print(f"verified {len(frames)} manifest-pinned CSV inputs")
    print(f"wrote {len(generated_tables)} derived tables: {', '.join(generated_tables)}")
    print(f"available PNG figures: {', '.join(generated_figures)}")


if __name__ == "__main__":
    main()
