"""Rebuild MA-SQLGrid Figures 2--6 from packaged summary artifacts.

This release-local renderer replaces two workspace-bound analysis scripts that
were copied into the 2026-08-09 manuscript directory.  It does not rerun model
calls or recompute inferential results.  It only renders publication figures
from the frozen CSV/JSON summaries included beside this file.
"""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "lineage_sources"
RESULTS = HERE / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.size": 9, "font.family": "DejaVu Sans"})


def read_csv(name: str) -> list[dict[str, str]]:
    path = SOURCE / name
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def save_all(fig, directory: Path, stem: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    for suffix in ("pdf", "svg", "png"):
        kwargs = {"bbox_inches": "tight"}
        if suffix == "png":
            kwargs["dpi"] = 400
        fig.savefig(directory / f"{stem}.{suffix}", **kwargs)
    plt.close(fig)


def figure2_cells() -> None:
    rows = read_csv("fig02_cell_summary_v2.csv")
    backbones = ("qwen", "granite")
    cells = ("F00_Full_NoShape", "F01_Full_WithShape", "F10_Compact_NoShape", "F11_Compact_WithShape")
    metrics = ("execution", "structural_common")
    if len(rows) != len(backbones) * len(cells) * len(metrics):
        raise ValueError("Figure 2 source is not the complete 2 x 4 x 2 cell summary")
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
    x = np.arange(4)
    width = 0.34
    for ax, metric, title in zip(axes, metrics, ("Execution equality", "Common-target projected-column conformity")):
        for index, backbone in enumerate(backbones):
            values = [float(next(row for row in rows if row["backbone"] == backbone and row["condition"] == cell and row["metric"] == metric)["mean"]) for cell in cells]
            ax.bar(x + (index - 0.5) * width, values, width, label=backbone.title())
        ax.set_xticks(x, ("F00", "F01", "F10", "F11"))
        ax.set_ylim(0, 1)
        ax.set_title(title)
        ax.set_ylabel("Proportion")
        ax.grid(axis="y", alpha=0.25)
    axes[1].legend(frameon=False)
    fig.tight_layout()
    save_all(fig, RESULTS, "fig01_v2_cells")


def figure3_components() -> None:
    rows = [row for row in read_csv("fig03_table_primary_effects.csv") if row["family"] in {"E1", "E2"}]
    if len(rows) != 4:
        raise ValueError("Figure 3 source must contain two E1 and two E2 rows")
    labels = [f"{row['family']} {row['model'].title()}" for row in rows]
    y = np.arange(len(rows))[::-1]
    colors = ["#2271B2" if row["model"] == "qwen" else "#D55E00" for row in rows]
    fig, ax = plt.subplots(figsize=(7.1, 3.5))
    for yi, row, color in zip(y, rows, colors):
        estimate = float(row["estimate"])
        low = float(row["ci_low"])
        high = float(row["ci_high"])
        ax.errorbar(estimate, yi, xerr=[[estimate - low], [high - estimate]], fmt="o", color=color, capsize=3)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_yticks(y, labels)
    ax.set_xlabel("Paired frozen-state execution-equality difference")
    ax.set_title("Cluster-aware primary component effects")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    save_all(fig, RESULTS, "figure_01_primary_effects")


def figure4_semantic() -> None:
    script = SOURCE / "fig04_build_manuscript_semantic_figure.py"
    command = [
        sys.executable,
        str(script),
        "--contrasts", str(SOURCE / "fig04_clustered_contrasts.csv"),
        "--exact-tests", str(SOURCE / "fig04_exact_cluster_sign_tests.csv"),
        "--suite", str(SOURCE / "fig04_suite_outcomes.csv"),
        "--out-dir", str(RESULTS),
        "--table-dir", str(SOURCE / "generated_tables"),
        "--lineage", str(SOURCE / "fig04_render_lineage.json"),
    ]
    subprocess.run(command, check=True)


def figures5_and_6() -> None:
    subprocess.run([sys.executable, str(HERE / "generate_p60_additions.py")], check=True)


def main() -> None:
    figure2_cells()
    figure3_components()
    figure4_semantic()
    figures5_and_6()
    print("Rebuilt MA-SQLGrid Figures 2--6 from release-local sources.")


if __name__ == "__main__":
    main()
