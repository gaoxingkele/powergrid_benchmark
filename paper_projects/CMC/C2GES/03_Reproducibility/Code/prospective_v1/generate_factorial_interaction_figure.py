#!/usr/bin/env python3
"""Render the exploratory reservation-by-path interaction diagnostics."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt


CONDITION = {
    (False, False): "RP-00",
    (True, False): "RP-10",
    (False, True): "RP-01",
    (True, True): "RP-11",
}
METRICS = (
    ("rougeL_f1", "ROUGE-L F1", (0.145, 0.195)),
    ("role_coverage", "Role coverage", (0.55, 1.04)),
    ("typed_edge_coverage", "Typed-edge coverage", (0.86, 1.02)),
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("aggregate_csv", type=Path)
    parser.add_argument("output_pdf", type=Path)
    parser.add_argument("--output-png", type=Path)
    args = parser.parse_args()

    with args.aggregate_csv.open(newline="", encoding="utf-8-sig") as stream:
        rows = list(csv.DictReader(stream))
    lookup = {(int(row["word_budget"]), row["condition"]): row for row in rows}

    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "legend.fontsize": 8,
    })
    fig, axes = plt.subplots(2, 3, figsize=(10.5, 5.8), sharex=True)
    colors = {False: "#2F6B9A", True: "#C45A3C"}
    markers = {False: "o", True: "s"}
    for row_index, budget in enumerate((110, 260)):
        for col_index, (metric, label, ylim) in enumerate(METRICS):
            ax = axes[row_index, col_index]
            for reservation in (False, True):
                values = [
                    float(lookup[(budget, CONDITION[(reservation, path)])][metric])
                    for path in (False, True)
                ]
                ax.plot(
                    (0, 1), values,
                    color=colors[reservation], marker=markers[reservation],
                    linewidth=1.8, markersize=5.5,
                    label=f"Reservation {'on' if reservation else 'off'}",
                )
                for x, value in enumerate(values):
                    horizontal = "left" if x == 0 else "right"
                    x_offset = 3 if x == 0 else -3
                    offset = (x_offset, -13) if not reservation else (x_offset, 7)
                    ax.annotate(
                        f"{value:.3f}", (x, value), xytext=offset,
                        textcoords="offset points", ha=horizontal, fontsize=7,
                    )
            ax.set_ylim(*ylim)
            ax.set_xticks((0, 1), ("Path off", "Path on"))
            ax.grid(axis="y", color="#D9D9D9", linewidth=0.6)
            ax.spines[["top", "right"]].set_visible(False)
            if row_index == 0:
                ax.set_title(label)
            if col_index == 0:
                ax.set_ylabel(f"{budget}-word budget")
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False, bbox_to_anchor=(0.5, 1.01))
    fig.suptitle("Reservation × Path Exploratory Interaction Diagnostics", y=1.07, fontsize=12, fontweight="bold")
    fig.text(0.5, 0.01, "Lines connect descriptive series-equal means; no factorial effect survived Holm correction.", ha="center", fontsize=8)
    fig.tight_layout(rect=(0, 0.035, 1, 0.96), w_pad=2.2, h_pad=1.8)
    args.output_pdf.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output_pdf, bbox_inches="tight")
    if args.output_png:
        args.output_png.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(args.output_png, dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
