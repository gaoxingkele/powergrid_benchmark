from __future__ import annotations

import shutil
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "generated"
C2_FIG = ROOT / "C2GES" / "figures"
MA_FIG = ROOT / "MA_SQLGrid" / "figures"

COLORS = {
    "blue": "#DCEEF8",
    "green": "#E1F1E6",
    "mint": "#D9EEE5",
    "amber": "#FFF0C9",
    "purple": "#EAE1F3",
    "gray": "#F2F3F5",
    "line": "#263238",
    "accent": "#0077BB",
    "violet": "#7A5195",
    "orange": "#EE7733",
    "red": "#CC3311",
}

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.linewidth": 0.8,
})


def setup(height: float = 7.1):
    fig, ax = plt.subplots(figsize=(13.8, height))
    ax.set_xlim(0, 13.8)
    ax.set_ylim(0, height)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    return fig, ax


def rounded_box(ax, x, y, w, h, title, lines=(), fill="#F2F3F5", edge=None,
                title_size=14, text_size=12, lw=1.4, dashed=False):
    edge = edge or COLORS["line"]
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.018,rounding_size=0.16",
        facecolor=fill, edgecolor=edge, linewidth=lw,
        linestyle=(0, (5, 3)) if dashed else "solid",
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h * 0.72, title, ha="center", va="center",
            fontsize=title_size, fontweight="bold", color="#111111", linespacing=1.05)
    if lines:
        ax.text(x + w / 2, y + h * 0.36, "\n".join(lines), ha="center", va="center",
                fontsize=text_size, linespacing=1.35, color="#1E1E1E")
    return patch


def arrow(ax, x1, y1, x2, y2, color=None, lw=1.6, dashed=False,
          connectionstyle="arc3", mutation=16, zorder=3):
    a = FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=mutation,
        linewidth=lw, color=color or COLORS["line"],
        linestyle=(0, (4, 3)) if dashed else "solid",
        connectionstyle=connectionstyle, zorder=zorder,
    )
    ax.add_patch(a)
    return a


def panel_label(ax, x, y, label, title):
    ax.text(x, y, label, fontsize=17, fontweight="bold", va="center")
    ax.text(x + 0.55, y, title, fontsize=16, fontweight="bold", va="center")


def save(fig, stem: str, destinations: list[Path]):
    OUT.mkdir(parents=True, exist_ok=True)
    pdf = OUT / f"{stem}.pdf"
    svg = OUT / f"{stem}.svg"
    png = OUT / f"{stem}_preview.png"
    fig.savefig(pdf, bbox_inches=None, pad_inches=0, facecolor="white")
    fig.savefig(svg, bbox_inches=None, pad_inches=0, facecolor="white")
    fig.savefig(png, dpi=160, bbox_inches=None, pad_inches=0, facecolor="white")
    plt.close(fig)
    for dest in destinations:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(pdf if dest.suffix.lower() == ".pdf" else svg, dest)


def c2ges():
    fig, ax = setup(7.2)
    panel_label(ax, 0.22, 6.88, "(a)", "End-to-end deterministic framework")

    y, h = 4.35, 1.78
    boxes = [
        (0.25, 2.18, "Complete Reports", ("Candidate/leakage gates", "Source IDs retained"), COLORS["blue"]),
        (2.78, 2.05, "Lexical Roles", ("Root Cause / Trigger", "Propagation / Impact", "Mitigation / Abstain"), COLORS["green"]),
        (5.17, 2.10, "Typed Textual\nProxy Graph", ("Stage-monotone edges", "Qualified paths"), COLORS["mint"]),
        (7.63, 2.85, "Normalized Channels", ("0.40 Q  Centroid relevance", "0.20 R  Role evidence", "0.15 G  Graph salience", "0.15 C  Path-deletion loss", "0.10 P  Position prior"), COLORS["amber"]),
        (10.88, 2.67, "Redundancy-Aware\nSelection", ("−0.50 max Jaccard", "Stable source-order ties", "Source-linked extract"), COLORS["purple"]),
    ]
    for x, w, title, lines, fill in boxes:
        rounded_box(ax, x, y, w, h, title, lines, fill=fill,
                    title_size=12.3, text_size=10.0)
    for (x, w, *_), (nx, *_rest) in zip(boxes, boxes[1:]):
        arrow(ax, x + w, y + h / 2, nx, y + h / 2)

    rounded_box(ax, 8.05, 3.15, 2.20, 0.78, "Registered no-CF", ("Set C = 0; no renormalization",),
                fill="#F7F0FA", title_size=11.2, text_size=9.0, dashed=True, lw=1.2)
    arrow(ax, 8.98, 4.35, 9.03, 3.93, color=COLORS["violet"], dashed=True, mutation=13)
    arrow(ax, 10.25, 3.54, 11.78, 4.35, color=COLORS["violet"], dashed=True,
          connectionstyle="arc3,rad=-0.12", mutation=13)

    ax.plot([0.25, 13.55], [2.83, 2.83], color="#B0BEC5", lw=0.9)
    panel_label(ax, 0.22, 2.50, "(b)", "Path-deletion mechanism for candidate node i")

    by, bh = 0.50, 1.40
    rounded_box(ax, 0.55, by, 2.55, bh, "Typed graph G", ("Qualified paths through i", r"$p_1$: root→i→impact", r"$p_2$: trigger→i→mitigation"),
                fill=COLORS["mint"], title_size=12.2, text_size=9.4)
    rounded_box(ax, 3.73, by, 2.05, bh, "Delete node i", ("Remove i + incident edges", "Re-enumerate paths"),
                fill="#FBE5E1", title_size=12.2, text_size=9.4)
    rounded_box(ax, 6.42, by, 2.35, bh, "Perturbed graph\n" + r"$G\setminus i$", ("Only surviving paths", r"contribute to $U(G\setminus i)$"),
                fill=COLORS["blue"], title_size=11.6, text_size=9.2)
    rounded_box(ax, 9.42, by, 2.55, bh, "Deletion loss", (r"$C_i = U(G) - U(G\setminus i)$", r"Normalize $C_i$ within report"),
                fill=COLORS["amber"], title_size=12.2, text_size=10.2)
    rounded_box(ax, 12.25, by, 1.20, bh, "C channel", ("joins Q,R,G,P",),
                fill=COLORS["purple"], title_size=10.8, text_size=8.8)
    arrow(ax, 3.10, by + bh / 2, 3.73, by + bh / 2)
    arrow(ax, 5.78, by + bh / 2, 6.42, by + bh / 2)
    arrow(ax, 8.77, by + bh / 2, 9.42, by + bh / 2)
    arrow(ax, 11.97, by + bh / 2, 12.25, by + bh / 2)

    save(fig, "fig01_algorithm_dual_panel", [
        C2_FIG / "fig01_algorithm_dual_panel.pdf",
        C2_FIG / "fig01_algorithm_dual_panel.svg",
    ])


def ma_sqlgrid():
    fig, ax = setup(8.15)
    panel_label(ax, 0.22, 7.82, "(a)", "Five-role coordination and append-only evidence trace")

    rounded_box(ax, 2.35, 7.02, 9.05, 0.56, "Deterministic Controller", ("orders calls • enforces typed contracts • seals decision and trace",),
                fill=COLORS["gray"], title_size=11.6, text_size=8.8, dashed=True, lw=1.1)

    rounded_box(ax, 0.25, 5.55, 1.62, 0.95, "NL Request", ("question xᵢ",), fill=COLORS["blue"], title_size=13.2, text_size=11)
    rounded_box(ax, 0.25, 4.30, 1.62, 0.95, "DB Schema", ("introspected Sᵢ",), fill=COLORS["blue"], title_size=13.2, text_size=11)
    rounded_box(ax, 0.25, 3.05, 1.62, 0.95, "External SQL", ("candidate set Yᵢ",), fill=COLORS["amber"], title_size=13.2, text_size=11)

    rounded_box(ax, 2.30, 5.47, 2.15, 1.08, "1. Query Analyst", ("question-only intent",), fill=COLORS["green"], title_size=11.4, text_size=9.6)
    rounded_box(ax, 2.30, 4.22, 2.15, 1.08, "2. Schema\nCartographer", ("intent + schema map",), fill=COLORS["green"], title_size=10.8, text_size=9.5)
    rounded_box(ax, 2.30, 2.97, 2.15, 1.08, "3. SQL Synthesizer", ("packages external SQL",), fill=COLORS["green"], title_size=11.0, text_size=9.5)

    rounded_box(ax, 5.05, 3.45, 2.35, 2.50, "Append-Only\nBlackboard", ("typed messages", "candidate IDs", "execution + state evidence", "decision digest"),
                fill=COLORS["gray"], title_size=11.8, text_size=10.0)
    rounded_box(ax, 8.12, 5.15, 2.18, 1.20, "4. Validation\nEngine", ("safe read-only execution", "append execution trace"), fill=COLORS["purple"], title_size=11.0, text_size=9.2)
    rounded_box(ax, 8.12, 3.45, 2.18, 1.34, "5. Metamorphic-State\nCritic", ("append named-state evidence",), fill=COLORS["purple"], title_size=10.4, text_size=9.0)
    rounded_box(ax, 11.05, 4.05, 2.45, 1.75, "Deterministic\nDecision", ("hard gates → score", "stable tie or abstain", "seal board + decision"), fill=COLORS["amber"], title_size=11.6, text_size=9.5)

    arrow(ax, 1.87, 6.02, 2.30, 6.02)
    arrow(ax, 1.87, 4.77, 2.30, 4.77)
    arrow(ax, 1.87, 3.52, 2.30, 3.52)
    arrow(ax, 4.45, 6.01, 5.05, 5.38)
    arrow(ax, 5.05, 5.02, 4.45, 4.77, color=COLORS["accent"], connectionstyle="arc3,rad=0.14")
    arrow(ax, 4.45, 4.50, 5.05, 4.70, color=COLORS["accent"], connectionstyle="arc3,rad=0.14")
    arrow(ax, 4.45, 3.52, 5.05, 4.02)
    arrow(ax, 7.40, 5.35, 8.12, 5.75)
    arrow(ax, 10.30, 5.48, 7.40, 5.10, color=COLORS["violet"], connectionstyle="arc3,rad=-0.12")
    arrow(ax, 7.40, 4.25, 8.12, 4.12)
    arrow(ax, 10.30, 4.02, 7.40, 3.85, color=COLORS["violet"], connectionstyle="arc3,rad=0.12")
    arrow(ax, 7.40, 4.70, 11.05, 4.86, color=COLORS["accent"])

    ax.plot([0.25, 13.55], [2.60, 2.60], color="#B0BEC5", lw=0.9)
    panel_label(ax, 0.22, 2.28, "(b)", "Per-candidate lifecycle and evaluation boundary")

    y, h = 0.60, 1.16
    lifecycle = [
        (0.27, 1.55, "Candidate ID", ("external SQL",), COLORS["green"]),
        (2.12, 1.90, "Read-Only Executor", ("authorizer + limits", "retained failures"), COLORS["purple"]),
        (4.31, 1.72, "Hard Gates", ("safe + executable",), COLORS["amber"]),
        (6.33, 2.10, "Named-State Gate", ("complete when required", "registered threshold"), COLORS["purple"]),
        (8.73, 1.92, "Evidence Score", (r"$10I_{shape}+5I_{order}+5V$",), COLORS["amber"]),
        (10.95, 1.32, "Decision", ("select / abstain", "seal board"), COLORS["amber"]),
        (12.57, 1.02, "Offline Gold", ("after sealing",), COLORS["gray"]),
    ]
    for x, w, title, lines, fill in lifecycle:
        rounded_box(ax, x, y, w, h, title.replace("Read-Only Executor", "Read-Only\nExecutor").replace("Named-State Gate", "Named-State\nGate").replace("Evidence Score", "Evidence\nScore").replace("Offline Gold", "Offline\nGold"), lines, fill=fill, title_size=9.8, text_size=8.2,
                    dashed=(title == "Offline Gold"))
    for (x, w, *_), (nx, *_rest) in zip(lifecycle, lifecycle[1:]):
        arrow(ax, x + w, y + h / 2, nx, y + h / 2,
              dashed=(nx == 12.57), mutation=13, lw=1.35)
    ax.add_patch(Rectangle((0.12, 0.35), 12.26, 1.72, fill=False, linewidth=1.1,
                           edgecolor=COLORS["accent"], linestyle=(0, (5, 3))))
    ax.text(0.27, 0.38, "MA-SQLGrid software boundary", fontsize=10.8, color=COLORS["accent"], va="bottom")
    ax.text(12.62, 0.38, "evaluation only", fontsize=9.8, color="#555555", va="bottom")

    save(fig, "fig_ma_sqlgrid_dual_panel", [
        MA_FIG / "fig_ma_sqlgrid_dual_panel.pdf",
        MA_FIG / "fig_ma_sqlgrid_dual_panel.svg",
    ])


if __name__ == "__main__":
    c2ges()
    ma_sqlgrid()
    print(f"Generated vector figures under {OUT}")
