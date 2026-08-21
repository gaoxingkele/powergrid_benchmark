#!/usr/bin/env python3
"""Generate Round-2 presentation-only figures from the frozen v2 CSVs.

This script does not modify the manuscript or canonical_v2_reanalysis.  Cell
confidence intervals in the v2 release quantify sensitivity to the observed
template-cluster composition; they are deliberately not drawn as conventional
sampling-error bars here.  Inferential intervals remain in the contrast plot
and canonical tables.
"""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
V2 = PROJECT / "canonical_v2_reanalysis"
FIGURES = HERE / "figures"
QA = HERE / "qa"

CELL_SOURCE = V2 / "tables" / "cell_summary_v2.csv"
CONTEXT_SOURCE = V2 / "tables" / "context_question_gold_offline_audit.csv"
PROMPT_SOURCE = V2 / "tables" / "prompt_context_summary.csv"

CONDITIONS = [
    "F00_Full_NoShape",
    "F01_Full_WithShape",
    "F10_Compact_NoShape",
    "F11_Compact_WithShape",
]
SHORT = ["F00", "F01", "F10", "F11"]
BACKBONES = ["qwen", "granite"]
COLORS = {"qwen": "#0072B2", "granite": "#D55E00"}
MARKERS = {"qwen": "o", "granite": "s"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def save_three(fig: plt.Figure, stem: str) -> list[Path]:
    FIGURES.mkdir(parents=True, exist_ok=True)
    outputs = []
    for ext in ("svg", "pdf", "png"):
        path = FIGURES / f"{stem}.{ext}"
        fig.savefig(
            path,
            dpi=450 if ext == "png" else None,
            bbox_inches="tight",
            facecolor="white",
        )
        outputs.append(path)
    return outputs


def cell_plot(cell_rows: list[dict[str, str]]) -> list[Path]:
    lookup = {
        (row["backbone"], row["condition"], row["metric"]): float(row["mean"])
        for row in cell_rows
    }
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.35), sharey=True)
    metric_titles = [
        ("execution", "(a) Execution equality"),
        ("structural_common", "(b) Common-target projected-column conformity"),
    ]
    x = np.arange(4)
    offsets = {"qwen": -0.065, "granite": 0.065}
    for ax, (metric, title) in zip(axes, metric_titles):
        for backbone in BACKBONES:
            values = np.array([lookup[(backbone, condition, metric)] for condition in CONDITIONS])
            xx = x + offsets[backbone]
            ax.plot(
                xx,
                values,
                color=COLORS[backbone],
                marker=MARKERS[backbone],
                markersize=6.5,
                linewidth=1.6,
                label=backbone.title(),
            )
            for xpos, value in zip(xx, values):
                text_dx = -9 if backbone == "qwen" else 9
                text_ha = "right" if backbone == "qwen" else "left"
                ax.annotate(
                    f"{100 * value:.1f}",
                    (xpos, value),
                    xytext=(text_dx, 7),
                    textcoords="offset points",
                    ha=text_ha,
                    va="bottom",
                    fontsize=8.5,
                    color=COLORS[backbone],
                    fontweight="semibold",
                )
        ax.set_xticks(x, SHORT)
        ax.set_xlim(-0.4, 3.4)
        ax.set_ylim(0.30, 1.04)
        ax.set_title(title, loc="left", fontsize=10.5, fontweight="semibold")
        ax.set_xlabel("Factorial condition")
        ax.grid(axis="y", color="#D9D9D9", linewidth=0.6, alpha=0.8)
    axes[0].set_ylabel("Proportion (direct labels: %)")
    axes[1].legend(frameon=False, loc="lower right")
    fig.suptitle(
        "POINT ESTIMATES ONLY — no cell-level error bars",
        x=0.5,
        y=1.015,
        fontsize=11.5,
        fontweight="bold",
        color="#7A1F1F",
    )
    fig.text(
        0.5,
        0.015,
        "v2 template-cluster composition-sensitivity intervals are intentionally omitted here; "
        "cluster-aware intervals are reported for registered contrasts.",
        ha="center",
        va="bottom",
        fontsize=8.8,
    )
    fig.tight_layout(rect=(0, 0.10, 1, 0.96), w_pad=2.0)
    outputs = save_three(fig, "ma_r2_f01_v2_cells_point_estimates")
    plt.close(fig)
    return outputs


def context_audit_plot(
    question_rows: list[dict[str, str]], prompt_rows: list[dict[str, str]]
) -> tuple[list[Path], dict[str, int]]:
    total = len(question_rows)
    all_tables = sum(int(row["gold_all_tables_retained"]) for row in question_rows)
    all_columns = sum(int(row["gold_all_columns_retained"]) for row in question_rows)
    multi = [row for row in question_rows if int(row["gold_required_table_count"]) > 1]
    joins = sum(int(row["gold_join_path_retained"]) for row in multi)
    counts = {
        "all_gold_tables_retained": all_tables,
        "all_gold_tables_denominator": total,
        "all_gold_columns_retained": all_columns,
        "all_gold_columns_denominator": total,
        "multi_table_join_paths_retained": joins,
        "multi_table_denominator": len(multi),
    }

    token_lookup = {
        (row["backbone"], row["condition"]): float(row["mean"])
        for row in prompt_rows
        if row["measure"] == "model_token_input" and row["backbone"] in BACKBONES
    }
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.45), gridspec_kw={"width_ratios": [1.0, 1.2]})

    labels = ["All required\ntables", "All required\ncolumns", "Multi-table\njoin path"]
    numerators = [all_tables, all_columns, joins]
    denominators = [total, total, len(multi)]
    rates = np.array(numerators) / np.array(denominators)
    y = np.arange(3)
    audit_colors = ["#009E73", "#56B4E9", "#CC79A7"]
    axes[0].barh(y, rates, color=audit_colors, edgecolor="#333333", linewidth=0.6)
    axes[0].set_yticks(y, labels)
    axes[0].invert_yaxis()
    axes[0].set_xlim(0, 1.08)
    axes[0].set_xlabel("Offline gold-retention rate")
    axes[0].set_title("(a) Compact-context coverage audit", loc="left", fontsize=10.5, fontweight="semibold")
    axes[0].grid(axis="x", color="#D9D9D9", linewidth=0.6, alpha=0.8)
    for ypos, rate, num, den in zip(y, rates, numerators, denominators):
        axes[0].text(
            min(rate + 0.018, 1.015),
            ypos,
            f"{num}/{den}\n({100 * rate:.1f}%)",
            va="center",
            ha="left",
            fontsize=9.3,
            fontweight="bold",
        )
    x = np.arange(4)
    width = 0.34
    for index, backbone in enumerate(BACKBONES):
        values = [token_lookup[(backbone, condition)] for condition in CONDITIONS]
        xpos = x + (index - 0.5) * width
        bars = axes[1].bar(
            xpos,
            values,
            width,
            label=backbone.title(),
            color=COLORS[backbone],
            edgecolor="#222222",
            linewidth=0.5,
            hatch="" if backbone == "qwen" else "//",
        )
        axes[1].bar_label(bars, labels=[f"{value:.0f}" for value in values], padding=3, fontsize=8.2)
    axes[1].set_xticks(x, SHORT)
    axes[1].set_ylabel("Mean model-token input")
    axes[1].set_xlabel("Factorial condition")
    axes[1].set_ylim(0, 3100)
    axes[1].set_title("(b) Prompt-length manipulation", loc="left", fontsize=10.5, fontweight="semibold")
    axes[1].legend(frameon=False, ncol=2, loc="upper right")
    axes[1].grid(axis="y", color="#D9D9D9", linewidth=0.6, alpha=0.8)

    fig.text(
        0.5,
        0.015,
        "Coverage is a post hoc offline diagnostic; token counts use each backbone's tokenizer.",
        ha="center",
        va="bottom",
        fontsize=8.8,
    )
    fig.tight_layout(rect=(0, 0.11, 1, 1), w_pad=2.5)
    outputs = save_three(fig, "ma_r2_f02_context_audit_direct_counts")
    plt.close(fig)
    return outputs, counts


def page_scale_preview(fig_paths: list[Path]) -> list[Path]:
    QA.mkdir(parents=True, exist_ok=True)
    images = [Image.open(path) for path in fig_paths]
    page, axes = plt.subplots(2, 1, figsize=(8.27, 11.69))
    for ax, image in zip(axes, images):
        ax.imshow(image)
        ax.axis("off")
    page.suptitle(
        "Round-2 figure page-scale legibility preview (A4, 7.1-inch content width)",
        fontsize=11,
        y=0.985,
    )
    page.subplots_adjust(left=0.07, right=0.93, top=0.96, bottom=0.04, hspace=0.13)
    outputs = []
    for ext in ("pdf", "png"):
        path = QA / f"page_scale_preview.{ext}"
        page.savefig(path, dpi=220 if ext == "png" else None, facecolor="white")
        outputs.append(path)
    plt.close(page)
    for image in images:
        image.close()
    return outputs


def main() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9.5,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )
    cell_rows = read_csv(CELL_SOURCE)
    question_rows = read_csv(CONTEXT_SOURCE)
    prompt_rows = read_csv(PROMPT_SOURCE)
    cell_outputs = cell_plot(cell_rows)
    context_outputs, counts = context_audit_plot(question_rows, prompt_rows)
    preview_outputs = page_scale_preview(
        [FIGURES / "ma_r2_f01_v2_cells_point_estimates.png", FIGURES / "ma_r2_f02_context_audit_direct_counts.png"]
    )

    png_properties = {}
    for path in [p for p in cell_outputs + context_outputs if p.suffix == ".png"]:
        with Image.open(path) as image:
            png_properties[path.name] = {"pixels": list(image.size), "dpi": list(image.info.get("dpi", (None, None)))}

    source_paths = [CELL_SOURCE, CONTEXT_SOURCE, PROMPT_SOURCE]
    output_paths = cell_outputs + context_outputs + preview_outputs
    manifest = {
        "schema_version": "ma-sqlgrid-round2-figure-assets-v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "presentation-only redraw from frozen v2 tables; no new model or component results",
        "cell_interval_policy": (
            "Point estimates only. The v2 cell intervals are template-cluster composition-sensitivity intervals, "
            "not independent-observation sampling-error bars; registered contrast intervals remain canonical."
        ),
        "source_files": {
            str(path.relative_to(PROJECT)).replace("\\", "/"): {
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
            }
            for path in source_paths
        },
        "derived_context_counts": counts,
        "png_properties": png_properties,
        "output_files": {
            str(path.relative_to(HERE)).replace("\\", "/"): {
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
            }
            for path in output_paths
        },
    }
    (HERE / "release_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
