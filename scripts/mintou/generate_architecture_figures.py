"""Generate exact, editable architecture figures for the six Mintou papers.

GPT Image 2 style masters are retained beside the outputs for visual provenance.
This script is the source of record for labels, topology, and vector submission files.
"""

from __future__ import annotations

from pathlib import Path
from textwrap import wrap

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[2]
PROJECTS = ROOT / "paper_projects"

NAVY = "#12305A"
TEAL = "#087C7E"
ORANGE = "#D95F02"
GRAY = "#5E6670"
PALE_BLUE = "#EEF5FB"
PALE_TEAL = "#ECF8F6"
PALE_ORANGE = "#FFF4EA"

mpl.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.linewidth": 0.8,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
    }
)


def box(ax, x, y, w, h, label, *, edge=NAVY, fill="white", fontsize=8.5,
        linestyle="-", note=None):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        linewidth=1.25, edgecolor=edge, facecolor=fill, linestyle=linestyle,
    )
    ax.add_patch(patch)
    wrapped = []
    for logical_line in label.split("\n"):
        wrapped.extend(
            wrap(
                logical_line,
                width=max(10, int(w * 63)),
                break_long_words=False,
                break_on_hyphens=False,
            )
            or [""]
        )
    lines = "\n".join(wrapped)
    ax.text(x + w / 2, y + h / 2, lines, ha="center", va="center",
            color=edge, fontsize=fontsize, fontweight="semibold")
    if note:
        ax.text(x + w / 2, y + 0.10 * h, note, ha="center", va="bottom",
                color=GRAY, fontsize=max(6.8, fontsize - 1.8))
    return patch


def arrow(ax, start, end, *, color=GRAY, linestyle="-", rad=0.0, width=1.15):
    arr = FancyArrowPatch(
        start, end, arrowstyle="-|>", mutation_scale=10,
        linewidth=width, color=color, linestyle=linestyle,
        connectionstyle=f"arc3,rad={rad}", shrinkA=1.5, shrinkB=1.5,
    )
    ax.add_patch(arr)
    return arr


def canvas():
    fig, ax = plt.subplots(figsize=(14.0, 5.6))
    fig.patch.set_facecolor("white")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax


def strip(ax, text, *, x=0.20, y=0.06, w=0.60, h=0.10, edge=TEAL):
    box(ax, x, y, w, h, text, edge=edge, fill="white", fontsize=8.2)


def save(fig, slug):
    out = PROJECTS / slug / "manuscript" / "figures"
    out.mkdir(parents=True, exist_ok=True)
    stem = out / "fig_architecture"
    fig.savefig(stem.with_suffix(".svg"), bbox_inches="tight", pad_inches=0.03)
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight", pad_inches=0.03)
    fig.savefig(stem.with_suffix(".png"), dpi=300, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def p1():
    fig, ax = canvas()
    box(ax, .02, .64, .14, .17, "RTS-GMLC inputs", fill=PALE_BLUE)
    box(ax, .02, .39, .14, .17, "Method-independent\ncurtailment target", edge=ORANGE, fill=PALE_ORANGE)
    box(ax, .02, .14, .14, .17, "Temporal windows and onset slice", edge=TEAL, fill=PALE_TEAL)
    box(ax, .21, .39, .11, .17, "GRU encoder", edge=TEAL)
    box(ax, .36, .39, .12, .17, "Metric embedding", edge=TEAL)
    box(ax, .53, .58, .12, .16, "Retrieval bank", edge=TEAL)
    box(ax, .53, .27, .12, .16, "Prediction head", edge=NAVY)
    box(ax, .70, .39, .08, .17, "Blend", edge=ORANGE, fill=PALE_ORANGE)
    box(ax, .83, .39, .14, .17, "1 h / 24 h evaluation", edge=NAVY)
    for y in (.725, .475, .225):
        arrow(ax, (.16, y), (.21, .475))
    arrow(ax, (.32, .475), (.36, .475)); arrow(ax, (.48, .475), (.53, .66))
    arrow(ax, (.48, .475), (.53, .35)); arrow(ax, (.65, .66), (.70, .50))
    arrow(ax, (.65, .35), (.70, .45)); arrow(ax, (.78, .475), (.83, .475))
    strip(ax, "MAE  •  onset F1  •  seeded Mann–Whitney U  •  Holm correction")
    save(fig, "mintou_p1_dstar_gru_dispatch")


def p2():
    fig, ax = canvas()
    box(ax, .02, .61, .13, .16, "Multi-region load", fill=PALE_BLUE)
    box(ax, .02, .29, .13, .16, "Calendar features", edge=TEAL, fill=PALE_TEAL)
    box(ax, .20, .43, .12, .17, "Shared temporal encoder", edge=TEAL)
    box(ax, .36, .43, .11, .17, "Series embeddings", edge=TEAL)
    box(ax, .51, .38, .14, .27, "Cross-series attention", edge=NAVY,
        note="Poincaré | Euclidean | equal")
    box(ax, .69, .43, .11, .17, "Context fusion", edge=TEAL)
    box(ax, .84, .43, .08, .17, "Forecast head", edge=NAVY)
    box(ax, .94, .43, .05, .17, "1 h / 24 h", edge=ORANGE, fill=PALE_ORANGE, fontsize=7.3)
    arrow(ax, (.15, .69), (.20, .53)); arrow(ax, (.15, .37), (.20, .49))
    for a, b in [((.32,.515),(.36,.515)),((.47,.515),(.51,.515)),((.65,.515),(.69,.515)),
                 ((.80,.515),(.84,.515)),((.92,.515),(.94,.515))]: arrow(ax,a,b)
    strip(ax, "OPSD  •  SimBench  •  Ausgrid  •  dataset-specific seeded tests", x=.23, w=.54)
    save(fig, "mintou_p2_hygraph_load_forecasting")


def p3():
    fig, ax = canvas()
    labels = [
        ("SimBench candidates", NAVY), ("Binary population", TEAL),
        ("jDE parameter update", NAVY), ("Two-strategy DE", NAVY),
        ("Decode + budget repair", TEAL), ("Constraint dominance", NAVY),
        ("Pareto archive", TEAL), ("Standard hypervolume", ORANGE),
    ]
    xs = [.015,.14,.265,.39,.515,.64,.765,.89]
    for x, (label, edge) in zip(xs, labels):
        box(ax, x, .43, .10, .20, label, edge=edge,
            fill=PALE_ORANGE if edge == ORANGE else "white", fontsize=7.8)
    for x in xs[:-1]: arrow(ax, (x+.10,.53), (x+.125,.53))
    ax.text(.377, .72, "Constraint-aware search", color=NAVY, fontsize=9,
            fontweight="semibold", ha="center")
    ax.plot([.255,.505],[.69,.69],color="#9BB7DD",lw=1.2)
    box(ax, .76, .17, .12, .14, "AC power-flow validation", edge=TEAL, fill=PALE_TEAL)
    arrow(ax, (.815,.43),(.82,.31), color=TEAL)
    arrow(ax, (.69,.43),(.19,.40), color=NAVY, rad=-.18)
    save(fig, "mintou_p3_samode_distribution_planning")


def p4():
    fig, ax = canvas()
    box(ax,.01,.62,.13,.16,"Grid candidates",fill=PALE_BLUE)
    box(ax,.01,.29,.13,.16,"Uncertainty\nscenarios",edge=TEAL,fill=PALE_TEAL)
    labels=[("Population-dependent worst-K screening",NAVY),("Hybrid GA / DE",TEAL),
            ("Budget repair",GRAY),("Constraint-aware selection",NAVY),("Pareto archive",ORANGE)]
    xs=[.20,.36,.52,.68,.84]
    for x,(label,edge) in zip(xs,labels): box(ax,x,.43,.12,.20,label,edge=edge,fontsize=7.8)
    arrow(ax,(.14,.70),(.20,.55)); arrow(ax,(.14,.37),(.20,.50))
    for x in xs[:-1]: arrow(ax,(x+.12,.53),(x+.16,.53))
    box(ax,.80,.15,.09,.14,"Unseen-stress test",edge=ORANGE,fill=PALE_ORANGE,fontsize=7.5)
    box(ax,.90,.15,.09,.14,"AC validation",edge=TEAL,fill=PALE_TEAL,fontsize=7.5)
    arrow(ax,(.90,.43),(.845,.29),color=ORANGE); arrow(ax,(.93,.43),(.945,.29),color=TEAL)
    arrow(ax,(.74,.43),(.42,.39),color=NAVY,rad=-.18)
    save(fig,"mintou_p4_shield_resilience_planning")


def p5():
    fig, ax = canvas()
    labels=[("Public project candidates",NAVY),("Five objectives + budget",TEAL),
            ("Binary population",NAVY),("Preference-guided ranking",TEAL),
            ("Deterministic\nrepair",NAVY),("NSGA-II kernel",NAVY),
            ("Feasible Pareto front",TEAL)]
    xs=[.01,.15,.29,.43,.57,.71,.85]
    for x,(label,edge) in zip(xs,labels): box(ax,x,.55,.12,.19,label,edge=edge,fontsize=7.7)
    for x in xs[:-1]: arrow(ax,(x+.12,.645),(x+.14,.645))
    box(ax,.46,.25,.25,.14,"Quarantined decision trace",edge=ORANGE,fill=PALE_ORANGE,
        note="append-only; never enters fitness")
    arrow(ax,(.49,.55),(.53,.39),color=ORANGE,linestyle="--")
    arrow(ax,(.63,.55),(.64,.39),color=ORANGE,linestyle="--")
    strip(ax,"NERC rule consistency  •  MTEP16 outcome alignment",x=.27,w=.46)
    save(fig,"mintou_p5_trace_moea_feasibility_review")


def p6():
    fig, ax = canvas()
    box(ax,.01,.48,.12,.19,"Project candidates",fill=PALE_BLUE)
    box(ax,.15,.48,.12,.19,"Budget +\ndependencies",edge=TEAL,fill=PALE_TEAL)
    box(ax,.29,.48,.12,.19,"NSGA-II offspring",edge=NAVY)
    group=FancyBboxPatch((.43,.38),.25,.40,boxstyle="round,pad=0.012,rounding_size=0.018",
                         lw=1.2,edgecolor="#9BB7DD",facecolor="white")
    ax.add_patch(group); ax.text(.555,.74,"Forward-dominant project search",ha="center",color=NAVY,
                                fontsize=9,fontweight="semibold")
    box(ax,.45,.48,.10,.18,"Forward insertion",edge=TEAL)
    box(ax,.57,.48,.09,.18,"Atomic\nsubstitution",edge=TEAL,fontsize=7.7)
    ax.text(.615,.43,"recorded replacement; no resolved HV gain",ha="center",color=ORANGE,fontsize=6.5)
    box(ax,.70,.48,.11,.19,"Dependency-aware\nrepair",edge=TEAL,fontsize=7.5)
    box(ax,.83,.48,.08,.19,"Acceptance + selection",edge=NAVY,fontsize=7.3)
    box(ax,.93,.48,.06,.19,"Feasible front",edge=TEAL,fontsize=7.1)
    for a,b in [((.13,.575),(.15,.575)),((.27,.575),(.29,.575)),((.41,.575),(.45,.575)),
                ((.55,.575),(.57,.575)),((.66,.575),(.70,.575)),((.81,.575),(.83,.575)),
                ((.91,.575),(.93,.575))]: arrow(ax,a,b)
    arrow(ax,(.87,.48),(.35,.44),color=NAVY,rad=-.18)
    strip(ax,"Budget sensitivity  •  NERC backtest  •  MTEP16 backtest",x=.25,w=.50)
    save(fig,"mintou_p6_bilonsga_project_review")


if __name__ == "__main__":
    p1(); p2(); p3(); p4(); p5(); p6()
    print("Generated SVG, vector PDF, and 300 dpi PNG architecture figures for P1–P6.")
