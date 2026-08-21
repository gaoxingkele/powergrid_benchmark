"""Generate Figures 5--6 from packaged, release-local sources.

The numeric panel reads its values from ``lineage_sources``.  The evidence
ladder is a conceptual boundary diagram and introduces no measurements.  All
paths resolve from this file, so the script is independent of the caller's
working directory.
"""

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT = Path(__file__).resolve().parent
SOURCE = OUT / "lineage_sources" / "fig05_output_length.csv"
plt.rcParams.update({"font.size": 9, "font.family": "DejaVu Sans"})


def save_all(fig, stem: str) -> None:
    for suffix in ("pdf", "svg", "png"):
        kwargs = {"bbox_inches": "tight"}
        if suffix == "png":
            kwargs["dpi"] = 400
        fig.savefig(OUT / f"{stem}.{suffix}", **kwargs)
    plt.close(fig)


def output_lengths() -> None:
    with SOURCE.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 4:
        raise ValueError(f"Expected four headline conditions in {SOURCE}, found {len(rows)}")
    methods = [row["method"] for row in rows]
    k5 = [float(row["mean_words_k5"]) for row in rows]
    k10 = [float(row["mean_words_k10"]) for row in rows]
    x = np.arange(len(methods))
    width = 0.36
    fig, ax = plt.subplots(figsize=(8.2, 3.6))
    b1 = ax.bar(x - width / 2, k5, width, label="K = 5", color="#3975a8")
    b2 = ax.bar(x + width / 2, k10, width, label="K = 10", color="#e38336")
    ax.bar_label(b1, fmt="%.1f", padding=2, fontsize=8)
    ax.bar_label(b2, fmt="%.1f", padding=2, fontsize=8)
    ax.set_ylabel("Mean selected words per report")
    ax.set_xticks(x, methods)
    ax.set_ylim(0, 670)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False, ncol=2, loc="upper left")
    fig.tight_layout()
    save_all(fig, "fig05_output_length")


def evidence_ladder() -> None:
    rows = [
        ("Mechanism execution", "verified", "#d8ead2"),
        ("Selected-proxy lexical overlap", "descriptive support", "#d8ead2"),
        ("Incremental counterfactual gain", "not demonstrated", "#f7dfb2"),
        ("Length-controlled superiority", "not evaluated", "#efc1c1"),
        ("Maintenance-work-order utility", "not evaluated", "#efc1c1"),
    ]
    fig, ax = plt.subplots(figsize=(8.2, 4.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    for i, (claim, status, color) in enumerate(rows):
        y = 5.3 - i
        ax.add_patch(plt.Rectangle((0.6, y - 0.36), 8.8, 0.72,
                                   facecolor=color, edgecolor="#555555", lw=0.8))
        ax.text(0.9, y, claim, va="center", ha="left", fontweight="bold")
        ax.text(9.05, y, status, va="center", ha="right")
        if i < len(rows) - 1:
            ax.annotate("", xy=(5, y - 0.62), xytext=(5, y - 0.38),
                        arrowprops={"arrowstyle": "-|>", "color": "#666666"})
    ax.text(5, 5.85, "Evidence ladder: claims narrow as validation requirements increase",
            ha="center", va="center", fontsize=11, fontweight="bold")
    fig.tight_layout()
    save_all(fig, "fig06_evidence_ladder")


if __name__ == "__main__":
    output_lengths()
    evidence_ladder()
