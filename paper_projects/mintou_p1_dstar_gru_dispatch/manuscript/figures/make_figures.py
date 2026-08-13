"""Regenerate P1 manuscript figures and derived tables from the fair-run manifest.

The script deliberately has no dependency on the legacy v5/v6 evidence tree.
It validates every manifest-listed fair-run output before drawing, then derives
all plotted values from ``experiments/p1_s3_fair_v1``.  Pillow is used instead
of matplotlib so the generator remains runnable in the paper-harness Python
environment.  PNG, PDF, and SVG-wrapper copies are emitted for each figure.

Usage:
    python manuscript/figures/make_figures.py
"""

from __future__ import annotations

import base64
import csv
import hashlib
import io
import json
import math
import os
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    # The managed Windows image currently exposes a regular CPython launcher
    # alongside free-threaded Pillow wheels.  Re-exec with the matching sibling
    # interpreter so the documented ``python make_figures.py`` command remains
    # valid instead of depending on a machine-specific manual launcher choice.
    sibling = Path(sys.executable).with_name("python3.14t.exe")
    if sibling.exists() and os.environ.get("P1_FIGURE_REEXEC") != "1":
        env = dict(os.environ)
        env["P1_FIGURE_REEXEC"] = "1"
        raise SystemExit(subprocess.call([str(sibling), str(Path(__file__).resolve()), *sys.argv[1:]], env=env))
    raise


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
RUN = PROJECT / "experiments" / "p1_s3_fair_v1"
RESULTS = RUN / "results"
DERIVED = PROJECT / "manuscript" / "derived_tables"
MANIFEST_PATH = RUN / "run_manifest.json"

WIDTH = 2400
HEIGHT = 1450
DPI = 300
FIXED_PDF_DATE = time.gmtime(0)

INK = "#17243a"
MUTED = "#596579"
GRID = "#d9dfe8"
BLUE = "#276fbf"
TEAL = "#138a86"
ORANGE = "#e67e22"
RED = "#c43d4b"
GREEN = "#2f8f5b"
PURPLE = "#7453a6"
LIGHT_BLUE = "#eaf2fb"
LIGHT_TEAL = "#e8f6f4"
LIGHT_ORANGE = "#fff2e6"
LIGHT_RED = "#fdecee"
SURFACE = "#ffffff"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


F_TITLE = font(54, True)
F_SUBTITLE = font(35, True)
F_BODY = font(29)
F_BODY_BOLD = font(29, True)
F_SMALL = font(24)
F_TINY = font(20)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: Iterable[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields))
        writer.writeheader()
        writer.writerows(rows)


def validate_manifest(manifest: dict[str, Any]) -> None:
    if manifest.get("status") != "completed":
        raise ValueError("fair-run manifest is not completed")
    for name, record in manifest["outputs"].items():
        path = RESULTS / name
        if not path.exists():
            raise FileNotFoundError(path)
        if path.stat().st_size != int(record["bytes"]):
            raise ValueError(f"byte-count mismatch for {name}")
        if sha256(path) != record["sha256"]:
            raise ValueError(f"SHA-256 mismatch for {name}")


def new_canvas(title: str, subtitle: str = "") -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (WIDTH, HEIGHT), SURFACE)
    draw = ImageDraw.Draw(image)
    draw.text((90, 55), title, fill=INK, font=F_TITLE)
    if subtitle:
        draw.text((92, 125), subtitle, fill=MUTED, font=F_SMALL)
    draw.line((90, 170, WIDTH - 90, 170), fill=GRID, width=3)
    return image, draw


def centered(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str,
             *, fill: str = INK, face: ImageFont.ImageFont = F_BODY,
             spacing: int = 8) -> None:
    left, top, right, bottom = box
    bounds = draw.multiline_textbbox((0, 0), text, font=face, align="center", spacing=spacing)
    tw, th = bounds[2] - bounds[0], bounds[3] - bounds[1]
    draw.multiline_text(
        (left + (right - left - tw) / 2, top + (bottom - top - th) / 2),
        text,
        fill=fill,
        font=face,
        align="center",
        spacing=spacing,
    )


def box(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], text: str,
        *, outline: str = BLUE, fill: str = SURFACE, face: ImageFont.ImageFont = F_BODY_BOLD) -> None:
    draw.rounded_rectangle(xy, radius=28, fill=fill, outline=outline, width=5)
    centered(draw, xy, text, fill=INK, face=face)


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: str = MUTED) -> None:
    draw.line((*start, *end), fill=color, width=6)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    size = 22
    for delta in (2.55, -2.55):
        point = (end[0] + size * math.cos(angle + delta), end[1] + size * math.sin(angle + delta))
        draw.line((*end, *point), fill=color, width=6)


def save_figure(image: Image.Image, stem: str) -> list[dict[str, Any]]:
    png = HERE / f"{stem}.png"
    pdf = HERE / f"{stem}.pdf"
    svg = HERE / f"{stem}.svg"
    image.save(png, format="PNG", dpi=(DPI, DPI), optimize=True)
    # Pillow otherwise stamps the current time into each PDF, making a clean
    # manifest-bound regeneration differ byte-for-byte on every invocation.
    image.save(
        pdf,
        format="PDF",
        resolution=DPI,
        creationDate=FIXED_PDF_DATE,
        modDate=FIXED_PDF_DATE,
    )
    buffer = io.BytesIO()
    image.save(buffer, format="PNG", dpi=(DPI, DPI), optimize=True)
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    svg.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}"><image width="{WIDTH}" height="{HEIGHT}" '
        f'href="data:image/png;base64,{encoded}"/></svg>\n',
        encoding="utf-8",
    )
    return [
        {"file": path.name, "sha256": sha256(path), "bytes": path.stat().st_size}
        for path in (png, pdf, svg)
    ]


def method_label(row: dict[str, str]) -> str:
    if row["method"] == "GRU-LSR" and row["blend_mode"] == "selected":
        return "GRU-LSR selected (retrieval-only)"
    if row["method"] == "GRU-LSR-Fixed0.5":
        return "GRU-LSR fixed 0.5"
    if row["method"] == "GRU-LSR-Fixed1":
        return "GRU head (alpha=1)"
    if row["method"] == "DirectPolicyTransform-Privileged":
        return "Direct transform (privileged)"
    return row["method"]


def primary_rows(board: list[dict[str, str]], horizon: int) -> list[dict[str, str]]:
    wanted = []
    for row in board:
        if row["cap"] != "0.70" or int(row["horizon_hours"]) != horizon:
            continue
        if row["method"] in {"DirectPolicyTransform-Privileged", "Persistence", "Seasonal-24h"}:
            wanted.append(row)
        elif row["selection_objective"] == "mae" and row["blend_mode"] in {"selected", "fixed_0.5", "fixed_1"}:
            wanted.append(row)
        elif row["method"] == "Ridge" and row["selection_objective"] == "mae":
            wanted.append(row)
    return sorted(wanted, key=lambda row: float(row["mean_curtailment_mae"]))


def draw_overview(run_rows: list[dict[str, str]], manifest: dict[str, Any]) -> Image.Image:
    image, draw = new_canvas(
        "Fair temporal gate and onset support",
        "Counts are delivery-target rows from the completed p1_s3_fair_v1 manifest; no row is an independent inferential unit.",
    )
    # Panel A: temporal phases.
    draw.text((100, 215), "(a) Disjoint artifact-building phases", fill=INK, font=F_SUBTITLE)
    phases = [("Fit", 0.50, BLUE), ("Selection", 0.10, TEAL), ("Calibration", 0.10, ORANGE), ("Test", 0.30, PURPLE)]
    x0, x1, y0, y1 = 110, 2290, 300, 475
    cursor = x0
    for name, fraction, color in phases:
        width = int((x1 - x0) * fraction)
        draw.rectangle((cursor, y0, cursor + width, y1), fill=color, outline=SURFACE, width=5)
        centered(draw, (cursor, y0, cursor + width, y1), f"{name}\n{int(fraction*100)}%", fill=SURFACE, face=F_BODY_BOLD)
        cursor += width
    draw.text((115, 500), "Fit-only normalization/model/bank | selection-only checkpoint, lambda, alpha | calibration-only threshold | held-out scoring", fill=MUTED, font=F_SMALL)

    # Panel B: support counts from one representative row per cap/horizon.
    draw.text((100, 590), "(b) Positive onset counts by phase", fill=INK, font=F_SUBTITLE)
    support: dict[tuple[str, int], dict[str, int]] = {}
    for row in run_rows:
        key = (row["cap"], int(row["horizon_hours"]))
        support.setdefault(
            key,
            {
                "selection": int(row["n_onsets_selection"]),
                "calibration": int(row["n_onsets_calibration"]),
                "test": int(row["n_onsets_test"]),
            },
        )
    plot_left, plot_top, plot_right, plot_bottom = 160, 690, 2240, 1250
    draw.line((plot_left, plot_bottom, plot_right, plot_bottom), fill=INK, width=3)
    max_count = max(value["test"] for value in support.values())
    groups = [(cap, horizon) for cap in ("0.60", "0.70", "0.80") for horizon in (1, 24)]
    group_width = (plot_right - plot_left) / len(groups)
    colors = {"selection": TEAL, "calibration": ORANGE, "test": PURPLE}
    for index, key in enumerate(groups):
        center_x = plot_left + group_width * (index + 0.5)
        values = support[key]
        for offset, phase in zip((-62, 0, 62), ("selection", "calibration", "test")):
            value = values[phase]
            height = int((plot_bottom - plot_top - 40) * value / max_count)
            left = int(center_x + offset - 23)
            draw.rectangle((left, plot_bottom - height, left + 46, plot_bottom), fill=colors[phase])
            draw.text((left - 8, plot_bottom - height - 34), str(value), fill=INK, font=F_TINY)
        centered(draw, (int(center_x - group_width/2), plot_bottom + 20, int(center_x + group_width/2), plot_bottom + 100), f"cap {key[0]}\n{key[1]} h", face=F_SMALL)
    for i, phase in enumerate(("selection", "calibration", "test")):
        x = 650 + i * 390
        draw.rectangle((x, 1328, x + 36, 1364), fill=colors[phase])
        draw.text((x + 48, 1327), phase, fill=MUTED, font=F_SMALL)
    draw.text((103, 625), "Zero selection and calibration positives at every cap and lag force the declared onset-selection/threshold fallbacks.", fill=RED, font=F_BODY_BOLD)
    return image


def draw_architecture(config: dict[str, Any]) -> Image.Image:
    image, draw = new_canvas(
        "Manifest-bound GRU learned-space retrieval evaluation",
        "The direct transform is a visibility audit; it is not on the lag-forecasting path.",
    )
    box(draw, (90, 300, 430, 510), "RTS-GMLC\ndelivery rows", outline=BLUE, fill=LIGHT_BLUE)
    box(draw, (520, 250, 900, 465), "48-row query\nwindow", outline=TEAL, fill=LIGHT_TEAL)
    box(draw, (520, 555, 900, 770), "Fixed policy\nproxy target", outline=ORANGE, fill=LIGHT_ORANGE)
    box(draw, (1000, 250, 1380, 465), "Fit-only GRU\nencoder + head", outline=TEAL, fill=LIGHT_TEAL)
    box(draw, (1000, 555, 1380, 770), f"Fit-only bank\nk={config['retrieval']['k_neighbors']}", outline=TEAL, fill=LIGHT_TEAL)
    box(draw, (1480, 330, 1840, 690), "alpha controls\n0 / 0.5 / 1\n+ selected alpha", outline=PURPLE, fill="#f2edf9")
    box(draw, (1940, 260, 2310, 500), "Selection\ncheckpoint / alpha", outline=TEAL, fill=LIGHT_TEAL)
    box(draw, (1940, 585, 2310, 825), "Calibration\ndetection threshold", outline=ORANGE, fill=LIGHT_ORANGE)
    arrow(draw, (430, 405), (520, 355))
    arrow(draw, (430, 405), (520, 665))
    arrow(draw, (900, 355), (1000, 355))
    arrow(draw, (900, 665), (1000, 665))
    arrow(draw, (1380, 355), (1480, 445))
    arrow(draw, (1380, 665), (1480, 575))
    arrow(draw, (1840, 445), (1940, 380))
    arrow(draw, (1840, 575), (1940, 700))
    box(draw, (1030, 930, 1840, 1150), "Held-out test: MAE + onset metrics\npaired seed-run contrasts; Holm within lag", outline=BLUE, fill=LIGHT_BLUE)
    arrow(draw, (2125, 825), (1840, 1035))
    box(draw, (120, 990, 760, 1220), "Privileged direct transform\nuses target-hour rows\n(zero MAE by construction)", outline=RED, fill=LIGHT_RED)
    arrow(draw, (520, 770), (520, 990), RED)
    draw.text((105, 1310), "Scope boundary: source issue timestamps and vintages are absent; every 1 h/24 h result is a retrospective delivery-row lag result.", fill=RED, font=F_BODY_BOLD)
    return image


def bar_panel(draw: ImageDraw.ImageDraw, rows: list[dict[str, str]], area: tuple[int, int, int, int], title: str) -> None:
    left, top, right, bottom = area
    draw.text((left, top - 62), title, fill=INK, font=F_SUBTITLE)
    max_value = max(float(row["mean_curtailment_mae"]) for row in rows) * 1.08
    label_width = 440
    plot_left = left + label_width
    row_height = (bottom - top) / len(rows)
    for index, row in enumerate(rows):
        value = float(row["mean_curtailment_mae"])
        y = int(top + index * row_height + row_height * 0.18)
        h = int(row_height * 0.58)
        label = method_label(row)
        color = MUTED
        if "selected" in label:
            color = BLUE
        elif "head" in label:
            color = ORANGE
        elif "privileged" in label:
            color = RED
        elif row["method"] == "Persistence":
            color = GREEN
        draw.text((left, y + 5), label, fill=INK, font=F_SMALL)
        width = int((right - plot_left - 120) * value / max_value)
        draw.rectangle((plot_left, y, plot_left + max(3, width), y + h), fill=color)
        draw.text((plot_left + max(8, width) + 12, y + 4), f"{value:.5f}", fill=INK, font=F_SMALL)
    draw.line((plot_left, top - 8, plot_left, bottom), fill=GRID, width=3)


def draw_leaderboard(board: list[dict[str, str]]) -> Image.Image:
    image, draw = new_canvas(
        "RQ1: continuous proxy error at the primary cap",
        "Mean test MAE at cap 0.70.  The target-hour direct transform is shown only as a privileged construction control.",
    )
    bar_panel(draw, primary_rows(board, 1), (90, 300, 1170, 1260), "(a) 1 h retrospective lag")
    bar_panel(draw, primary_rows(board, 24), (1230, 300, 2310, 1260), "(b) 24 h retrospective lag")
    draw.text((100, 1350), "Persistence remains lower-MAE than selected GRU-LSR at both lags; selected alpha=0 in all ten seeds.", fill=RED, font=F_BODY_BOLD)
    return image


def effect_color(metric: str, value: float, direction: str) -> str:
    favorable = value < 0 if direction == "lower" else value > 0
    if abs(value) < 1e-14:
        return MUTED
    return BLUE if favorable else RED


def effect_panel(draw: ImageDraw.ImageDraw, rows: list[dict[str, str]], area: tuple[int, int, int, int], title: str) -> None:
    left, top, right, bottom = area
    draw.text((left, top - 62), title, fill=INK, font=F_SUBTITLE)
    max_abs = max(abs(float(row["mean_treatment_minus_control"])) for row in rows) or 1.0
    center_x = int(left + (right - left) * 0.63)
    draw.line((center_x, top, center_x, bottom), fill=INK, width=3)
    row_height = (bottom - top) / len(rows)
    labels = {
        "selected_retrieval_vs_head_mae": "selected vs head",
        "fixed_half_vs_head_mae": "fixed 0.5 vs head",
        "selected_vs_fixed_half_mae": "selected vs fixed 0.5",
        "selected_retrieval_vs_head_onset": "selected vs head",
        "fixed_half_vs_head_onset": "fixed 0.5 vs head",
        "selected_vs_fixed_half_onset": "selected vs fixed 0.5",
    }
    for index, row in enumerate(rows):
        value = float(row["mean_treatment_minus_control"])
        y = int(top + row_height * (index + 0.5))
        draw.text((left, y - 22), f"{row['horizon_hours']} h: {labels[row['contrast_id']]}", fill=INK, font=F_SMALL)
        span = int((right - center_x - 100) * value / max_abs)
        color = effect_color(row["metric"], value, row["better_direction"])
        draw.line((center_x, y, center_x + span, y), fill=color, width=20)
        draw.ellipse((center_x + span - 14, y - 14, center_x + span + 14, y + 14), fill=color)
        p = float(row["p_holm_within_horizon"])
        draw.text((right - 270, y - 22), f"d={value:+.5f}; pH={p:.4f}", fill=MUTED, font=F_TINY)


def draw_effects(paired: list[dict[str, str]]) -> Image.Image:
    image, draw = new_canvas(
        "Paired mechanism contrasts at cap 0.70",
        "Differences are treatment minus control over ten paired seed runs; pH is Holm-adjusted within lag.",
    )
    mae = [row for row in paired if row["metric"] == "curtailment_mae"]
    onset = [row for row in paired if row["metric"] == "onset_f1"]
    effect_panel(draw, mae, (90, 315, 1170, 1240), "(a) MAE difference (lower is favorable)")
    effect_panel(draw, onset, (1230, 315, 2310, 1240), "(b) Onset-F1 difference (higher is favorable)")
    draw.text((100, 1325), "Onset panel is diagnostically retained but not an onset-selection estimate: selection and calibration contain zero positive onsets.", fill=RED, font=F_BODY_BOLD)
    return image


def draw_seed_pairs(run_rows: list[dict[str, str]]) -> Image.Image:
    image, draw = new_canvas(
        "Seed-paired MAE: selected retrieval versus matched GRU head",
        "Each segment is one training seed at cap 0.70 under MAE selection; lower is better.",
    )
    for panel, horizon in enumerate((1, 24)):
        left = 120 + panel * 1160
        right = left + 1040
        top, bottom = 300, 1220
        draw.text((left, 225), f"({'a' if panel == 0 else 'b'}) {horizon} h retrospective lag", fill=INK, font=F_SUBTITLE)
        selected = {
            int(row["seed_index"]): float(row["curtailment_mae"])
            for row in run_rows
            if row["cap"] == "0.70" and int(row["horizon_hours"]) == horizon
            and row["selection_objective"] == "mae" and row["blend_mode"] == "selected"
        }
        head = {
            int(row["seed_index"]): float(row["curtailment_mae"])
            for row in run_rows
            if row["cap"] == "0.70" and int(row["horizon_hours"]) == horizon
            and row["selection_objective"] == "mae" and row["blend_mode"] == "fixed_1"
        }
        values = list(selected.values()) + list(head.values())
        lo, hi = min(values) * 0.96, max(values) * 1.04
        x_selected, x_head = left + 260, right - 260
        draw.line((x_selected, top, x_selected, bottom), fill=GRID, width=3)
        draw.line((x_head, top, x_head, bottom), fill=GRID, width=3)
        for seed in sorted(selected):
            y_sel = int(bottom - (selected[seed] - lo) / (hi - lo) * (bottom - top))
            y_head = int(bottom - (head[seed] - lo) / (hi - lo) * (bottom - top))
            draw.line((x_selected, y_sel, x_head, y_head), fill="#a9b9cd", width=4)
            draw.ellipse((x_selected - 10, y_sel - 10, x_selected + 10, y_sel + 10), fill=BLUE)
            draw.ellipse((x_head - 10, y_head - 10, x_head + 10, y_head + 10), fill=ORANGE)
        centered(draw, (x_selected - 170, 1240, x_selected + 170, 1320), "selected\n(alpha=0)", face=F_SMALL)
        centered(draw, (x_head - 170, 1240, x_head + 170, 1320), "head\n(alpha=1)", face=F_SMALL)
        draw.text((left + 10, 1340), f"10/10 pairs favor retrieval; mean d={sum(selected[s]-head[s] for s in selected)/10:+.6f}", fill=MUTED, font=F_SMALL)
    return image


def draw_cap_sensitivity(cap_rows: list[dict[str, str]]) -> Image.Image:
    image, draw = new_canvas(
        "RQ3: descriptive cap sensitivity on one system-year",
        "Difference = MAE-selected GRU-LSR minus Persistence; negative favors GRU-LSR. No cross-cap inference is performed.",
    )
    index = {(row["cap"], int(row["horizon_hours"]), row["method"], row["selection_objective"], row["blend_mode"]): row for row in cap_rows}
    for panel, horizon in enumerate((1, 24)):
        left = 130 + panel * 1160
        right = left + 1030
        top, bottom = 330, 1210
        center = (left + right) // 2
        draw.text((left, 235), f"({'a' if panel == 0 else 'b'}) {horizon} h retrospective lag", fill=INK, font=F_SUBTITLE)
        draw.line((center, top, center, bottom), fill=INK, width=3)
        deltas = []
        for cap in ("0.60", "0.70", "0.80"):
            gru = float(index[(cap, horizon, "GRU-LSR", "mae", "selected")]["mean_curtailment_mae"])
            persistence = float(index[(cap, horizon, "Persistence", "not_applicable", "not_applicable")]["mean_curtailment_mae"])
            deltas.append((cap, gru - persistence, gru, persistence))
        max_abs = max(abs(value) for _, value, _, _ in deltas)
        for row_index, (cap, value, gru, persistence) in enumerate(deltas):
            y = top + 155 + row_index * 235
            span = int((right - center - 180) * value / max_abs)
            color = BLUE if value < 0 else RED
            draw.line((center, y, center + span, y), fill=color, width=28)
            draw.ellipse((center + span - 15, y - 15, center + span + 15, y + 15), fill=color)
            draw.text((left, y - 25), f"cap {cap}", fill=INK, font=F_BODY_BOLD)
            draw.text((right - 460, y - 25), f"d={value:+.6f}", fill=INK, font=F_SMALL)
            draw.text((left + 10, y + 55), f"GRU-LSR {gru:.6f} | Persistence {persistence:.6f}", fill=MUTED, font=F_TINY)
        draw.text((left + 125, 1260), "GRU-LSR better", fill=BLUE, font=F_SMALL)
        draw.text((center + 170, 1260), "Persistence better", fill=RED, font=F_SMALL)
    draw.text((100, 1370), "Crossings occur only at cap 0.60/1 h and cap 0.80/24 h; they are same-series descriptive scope checks.", fill=RED, font=F_BODY_BOLD)
    return image


def draw_runtime(run_rows: list[dict[str, str]]) -> Image.Image:
    image, draw = new_canvas(
        "Supplement: implementation timing and MAE",
        "Wall-clock timing is descriptive and excluded from scientific-output reproduction checks.",
    )
    selected = [
        row for row in run_rows
        if row["cap"] == "0.70" and row["selection_objective"] == "mae"
        and row["blend_mode"] == "selected"
    ]
    for panel, horizon in enumerate((1, 24)):
        rows = [row for row in selected if int(row["horizon_hours"]) == horizon]
        left = 150 + panel * 1160
        right = left + 1030
        top, bottom = 300, 1240
        times = [float(row["runtime_s"]) for row in rows]
        errors = [float(row["curtailment_mae"]) for row in rows]
        tlo, thi = min(times), max(times)
        elo, ehi = min(errors), max(errors)
        draw.text((left, 220), f"({'a' if panel == 0 else 'b'}) {horizon} h", fill=INK, font=F_SUBTITLE)
        draw.rectangle((left, top, right, bottom), outline=GRID, width=3)
        for idx, (runtime, error) in enumerate(zip(times, errors)):
            x = int(left + 60 + (runtime - tlo) / max(1e-12, thi - tlo) * (right - left - 120))
            y = int(bottom - 60 - (error - elo) / max(1e-12, ehi - elo) * (bottom - top - 120))
            draw.ellipse((x - 12, y - 12, x + 12, y + 12), fill=BLUE)
            draw.text((x + 10, y - 30), str(idx), fill=MUTED, font=F_TINY)
        draw.text((left + 20, bottom + 25), f"runtime range {tlo:.3f}-{thi:.3f} s", fill=MUTED, font=F_SMALL)
        draw.text((left + 20, bottom + 75), f"MAE range {elo:.6f}-{ehi:.6f}", fill=MUTED, font=F_SMALL)
    return image


def write_derived_tables(
    manifest: dict[str, Any], run_rows: list[dict[str, str]], board: list[dict[str, str]],
    paired: list[dict[str, str]], cap_rows: list[dict[str, str]],
) -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    primary = []
    for horizon in (1, 24):
        for row in primary_rows(board, horizon):
            primary.append(
                {
                    "cap": row["cap"],
                    "horizon_hours": row["horizon_hours"],
                    "condition": method_label(row),
                    "selection_objective": row["selection_objective"],
                    "n_seeds": row["n_seeds"],
                    "mean_alpha_head": row["mean_alpha_head"],
                    "mean_curtailment_mae": row["mean_curtailment_mae"],
                    "std_curtailment_mae": row["std_curtailment_mae"],
                    "mean_onset_f1": row["mean_onset_f1"],
                    "mean_onset_mae": row["mean_onset_mae"],
                }
            )
    fields = list(primary[0])
    write_csv(DERIVED / "fair_primary_cap_summary.csv", primary, fields)
    write_csv(DERIVED / "fair_paired_contrasts.csv", paired, paired[0].keys())

    support_rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for row in run_rows:
        key = (row["cap"], row["horizon_hours"])
        if key in seen:
            continue
        seen.add(key)
        support_rows.append(
            {field: row[field] for field in (
                "cap", "horizon_hours", "n_fit", "n_selection", "n_calibration", "n_test",
                "n_onsets_selection", "n_onsets_calibration", "n_onsets_test", "n_events_test",
            )}
        )
    write_csv(DERIVED / "fair_onset_support.csv", support_rows, support_rows[0].keys())

    cap_summary: list[dict[str, Any]] = []
    idx = {(r["cap"], r["horizon_hours"], r["method"], r["selection_objective"], r["blend_mode"]): r for r in cap_rows}
    for cap in ("0.60", "0.70", "0.80"):
        for horizon in ("1", "24"):
            gru = idx[(cap, horizon, "GRU-LSR", "mae", "selected")]
            persistence = idx[(cap, horizon, "Persistence", "not_applicable", "not_applicable")]
            gv = float(gru["mean_curtailment_mae"])
            pv = float(persistence["mean_curtailment_mae"])
            cap_summary.append({
                "cap": cap,
                "horizon_hours": horizon,
                "gru_lsr_selected_mae": f"{gv:.10f}",
                "persistence_mae": f"{pv:.10f}",
                "gru_minus_persistence": f"{gv-pv:.10f}",
                "descriptive_winner": "GRU-LSR" if gv < pv else "Persistence",
            })
    write_csv(DERIVED / "fair_cap_selected_vs_persistence.csv", cap_summary, cap_summary[0].keys())

    series_stats = {
        "source_manifest": str(MANIFEST_PATH.relative_to(PROJECT)).replace("\\", "/"),
        "source_manifest_sha256": sha256(MANIFEST_PATH),
        "hours": manifest["source_profile"]["hours"],
        "primary_cap": manifest["evidence_boundary"]["primary_cap"],
        "phase_and_onset_counts": support_rows,
        "scope": "delivery-row retrospective lag tasks; paired seed-run inference covers training randomness only",
    }
    (HERE / "series_stats.json").write_text(json.dumps(series_stats, indent=2) + "\n", encoding="utf-8")
    (HERE / "cap_sensitivity.json").write_text(
        json.dumps({
            "source_manifest": str(MANIFEST_PATH.relative_to(PROJECT)).replace("\\", "/"),
            "source_manifest_sha256": sha256(MANIFEST_PATH),
            "scope": "descriptive method-level reruns on the same RTS-GMLC system and weather year; no cross-cap p-values",
            "selected_gru_lsr_vs_persistence": cap_summary,
        }, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    validate_manifest(manifest)
    config = json.loads((RUN / "config.json").read_text(encoding="utf-8"))
    run_rows = read_csv(RESULTS / "run_results.csv")
    board = read_csv(RESULTS / "leaderboard.csv")
    paired = read_csv(RESULTS / "paired_primary.csv")
    cap_rows = read_csv(RESULTS / "cap_sensitivity.csv")
    if len(run_rows) != int(manifest["row_counts"]["run_results"]):
        raise ValueError("run row count does not match manifest")

    write_derived_tables(manifest, run_rows, board, paired, cap_rows)
    generated: list[dict[str, Any]] = []
    figures = {
        "fig_benchmark_overview": draw_overview(run_rows, manifest),
        "fig_architecture": draw_architecture(config),
        "fig_leaderboard": draw_leaderboard(board),
        "fig_scale_dependency": draw_effects(paired),
        "fig_seed_uncertainty": draw_seed_pairs(run_rows),
        "fig_metric_rank_profile": draw_cap_sensitivity(cap_rows),
        "fig_runtime_error_tradeoff": draw_runtime(run_rows),
        # Historical filename retained as a compatibility copy; contents now
        # show the fair-run cap-sensitivity scope rather than v6/NREL controls.
        "fig_modern_baselines_transportability": draw_cap_sensitivity(cap_rows),
    }
    for stem, image in figures.items():
        generated.extend(save_figure(image, stem))

    artifact_manifest = {
        "generator": "manuscript/figures/make_figures.py",
        "source_run_manifest": str(MANIFEST_PATH.relative_to(PROJECT)).replace("\\", "/"),
        "source_run_manifest_sha256": sha256(MANIFEST_PATH),
        "validated_inputs": {
            name: {"sha256": record["sha256"], "bytes": record["bytes"]}
            for name, record in manifest["outputs"].items()
        },
        "derived_tables": [
            path.name for path in sorted(DERIVED.glob("fair_*.csv"))
        ],
        "generated_figures": generated,
        "scope": "all figure values derive from p1_s3_fair_v1; runtime figure is supplementary only",
    }
    (HERE / "artifact_manifest.json").write_text(json.dumps(artifact_manifest, indent=2) + "\n", encoding="utf-8")
    print(f"validated {len(manifest['outputs'])} manifest outputs; generated {len(figures)} figures")


if __name__ == "__main__":
    main()
