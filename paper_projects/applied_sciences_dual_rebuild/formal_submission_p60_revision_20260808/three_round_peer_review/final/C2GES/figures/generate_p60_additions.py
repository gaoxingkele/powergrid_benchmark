"""Generate additional C2GES figures from reported immutable results.

The numeric panel uses only values already reported in Table 5.  The evidence
ladder is a conceptual boundary diagram and introduces no measurements.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT = Path(__file__).resolve().parent
plt.rcParams.update({"font.size": 9, "font.family": "DejaVu Sans"})


def output_lengths() -> None:
    methods = ["Full C2GES", "Graph no-CF", "Semantic-MMR", "TextRank"]
    k5 = [287.7, 329.0, 184.7, 177.0]
    k10 = [568.9, 596.9, 354.5, 369.0]
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
    fig.savefig(OUT / "fig05_output_length.pdf", bbox_inches="tight")
    plt.close(fig)


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
    fig.savefig(OUT / "fig06_evidence_ladder.pdf", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    output_lengths()
    evidence_ladder()
