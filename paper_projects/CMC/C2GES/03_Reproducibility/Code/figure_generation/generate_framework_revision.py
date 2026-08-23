"""Generate the revised C2GES algorithm figure as vector PDF/SVG."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
OUT.mkdir(parents=True, exist_ok=True)
FIXED_TIME = datetime(2026, 8, 12, tzinfo=timezone.utc)

COLORS = {
    "blue": "#DCEEF8",
    "green": "#E1F1E6",
    "mint": "#D9EEE5",
    "amber": "#FFF0C9",
    "purple": "#EAE1F3",
    "gray": "#F2F3F5",
    "line": "#263238",
    "violet": "#7A5195",
}

mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "axes.linewidth": 0.8,
    }
)


def rounded_box(ax, x, y, w, h, title, lines=(), fill="#F2F3F5", dashed=False):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.018,rounding_size=0.14",
        facecolor=fill,
        edgecolor=COLORS["line"],
        linewidth=1.25,
        linestyle=(0, (5, 3)) if dashed else "solid",
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2,
        y + h * 0.70,
        title,
        ha="center",
        va="center",
        fontsize=10.4,
        fontweight="bold",
        linespacing=1.05,
    )
    if lines:
        ax.text(
            x + w / 2,
            y + h * 0.33,
            "\n".join(lines),
            ha="center",
            va="center",
            fontsize=8.3,
            linespacing=1.25,
        )


def arrow(ax, x1, y1, x2, y2, color=None, dashed=False, rad=0):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle="-|>",
            mutation_scale=13,
            linewidth=1.35,
            color=color or COLORS["line"],
            linestyle=(0, (4, 3)) if dashed else "solid",
            connectionstyle=f"arc3,rad={rad}",
            zorder=3,
        )
    )


def save(fig):
    metadata = {
        "Creator": "C2GES reproducible figure generator",
        "CreationDate": FIXED_TIME,
        "ModDate": FIXED_TIME,
    }
    fig.savefig(OUT / "fig01_algorithm_dual_panel.pdf", metadata=metadata)
    fig.savefig(OUT / "fig01_algorithm_dual_panel.svg", metadata={"Date": "2026-08-12"})
    fig.savefig(OUT / "fig01_algorithm_dual_panel_preview.png", dpi=200)
    plt.close(fig)


def main():
    fig, ax = plt.subplots(figsize=(13.8, 7.2))
    ax.set_xlim(0, 13.8)
    ax.set_ylim(0, 7.2)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    ax.text(0.22, 6.88, "(a)", fontsize=15, fontweight="bold", va="center")
    ax.text(0.78, 6.88, "End-to-end deterministic framework", fontsize=14, fontweight="bold", va="center")

    h = 1.18
    top = [
        (0.55, 3.25, "Complete Reports", ("Candidate/reference gates", "Source IDs retained"), COLORS["blue"]),
        (5.25, 3.25, "Lexical Roles", ("Cause / Trigger; Propagation / Impact", "Mitigation / Abstain"), COLORS["green"]),
        (9.95, 3.25, "Typed-Path Graph", ("Stage-monotone edges", "Qualified 2--4-edge paths"), COLORS["mint"]),
    ]
    bottom = [
        (0.55, 3.25, "Five Score Channels", ("0.40 Q; 0.20 R; 0.15 G", "0.15 C; 0.10 P"), COLORS["amber"]),
        (5.25, 3.25, "Role-Group Reservation", ("1 Cause/Trigger; 2 Propagation/Impact", "3 Mitigation when available"), COLORS["green"]),
        (9.95, 3.25, "Redundancy-Aware Greedy Fill", ("-0.50 max Jaccard; stable ties", "Restore source order and page links"), COLORS["purple"]),
    ]
    for x, w, title, lines, fill in top:
        rounded_box(ax, x, 5.25, w, h, title, lines, fill)
    for x, w, title, lines, fill in bottom:
        rounded_box(ax, x, 3.55, w, h, title, lines, fill)
    arrow(ax, 3.80, 5.84, 5.25, 5.84)
    arrow(ax, 8.50, 5.84, 9.95, 5.84)
    arrow(ax, 11.58, 5.25, 2.18, 4.73, rad=0.28)
    arrow(ax, 3.80, 4.14, 5.25, 4.14)
    arrow(ax, 8.50, 4.14, 9.95, 4.14)

    rounded_box(ax, 0.82, 2.95, 2.72, 0.48, "Strict ablation", ("Set C = 0; no renormalization",), "#F7F0FA", dashed=True)
    arrow(ax, 2.18, 3.55, 2.18, 3.43, COLORS["violet"], dashed=True)
    arrow(ax, 3.54, 3.19, 5.25, 3.72, COLORS["violet"], dashed=True, rad=-0.12)

    ax.plot([0.22, 13.58], [2.82, 2.82], color="#B0BEC5", lw=0.9)
    ax.text(0.22, 2.50, "(b)", fontsize=15, fontweight="bold", va="center")
    ax.text(0.78, 2.50, "Path-deletion mechanism for candidate node i", fontsize=14, fontweight="bold", va="center")

    by, bh = 0.50, 1.40
    lower = [
        (0.50, 2.55, "Typed graph G", ("Qualified paths through i", "Stages 0 to 4"), COLORS["mint"]),
        (3.62, 2.05, "Delete node i", ("Remove i and incident edges", "Re-enumerate paths"), "#FBE5E1"),
        (6.26, 2.30, "Perturbed graph", ("Only surviving paths", "contribute to U(G without i)"), COLORS["blue"]),
        (9.15, 2.42, "Deletion loss", ("C_i = U(G) - U(G without i)", "Min--max scale in report"), COLORS["amber"]),
        (12.13, 1.22, "C channel", ("joins Q, R, G, P",), COLORS["purple"]),
    ]
    for x, w, title, lines, fill in lower:
        rounded_box(ax, x, by, w, bh, title, lines, fill)
    for (x, w, *_), (nx, *_rest) in zip(lower, lower[1:]):
        arrow(ax, x + w, by + bh / 2, nx, by + bh / 2)

    save(fig)
    print(OUT / "fig01_algorithm_dual_panel.pdf")


if __name__ == "__main__":
    main()
