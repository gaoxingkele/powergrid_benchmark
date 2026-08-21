#!/usr/bin/env python3
"""Generate MDPI-page-legible Round-1 MA-SQLGrid framework figures."""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "figures"
QA = ROOT / "qa"
OUT.mkdir(exist_ok=True)
QA.mkdir(exist_ok=True)

NAVY = "#143D59"
BLUE = "#3A7CA5"
TEAL = "#2A9D8F"
GOLD = "#E9C46A"
ORANGE = "#F4A261"
RED = "#C94C4C"
PALE = "#F4F7FA"
INK = "#1F2933"


def setup(figsize=(7.2, 3.4)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text, color=BLUE, fs=10, lw=1.3):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.018",
                       facecolor=color, edgecolor=NAVY, linewidth=lw)
    ax.add_patch(p)
    ax.text(x+w/2, y+h/2, text, ha="center", va="center", fontsize=fs,
            color="white" if color not in {GOLD, PALE} else INK, fontweight="semibold")
    return p


def arrow(ax, x1, y1, x2, y2, color=NAVY, style="-|>", lw=1.5):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle=style,
                                mutation_scale=12,linewidth=lw,color=color))


def save(fig, stem):
    for ext in ("svg", "pdf"):
        fig.savefig(OUT / f"{stem}.{ext}", bbox_inches="tight", facecolor="white")
    fig.savefig(OUT / f"{stem}.png", dpi=450, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig1():
    fig, ax = setup((7.2, 3.15))
    ax.text(.5,.955,"Executed one-pass MA-SQLGrid pipeline",ha="center",va="top",fontsize=14,fontweight="bold",color=INK)
    labels=[("Question +\nfrozen DB",.03,TEAL),("Prompt package\ncontext × hint",.27,BLUE),
            ("Frozen local\nbackbone",.51,NAVY),("Parse • validate\nexecute",.75,RED)]
    for t,x,c in labels: box(ax,x,.54,.19,.20,t,c,fs=9.0)
    for i in range(3): arrow(ax,labels[i][1]+.19,.64,labels[i+1][1]-.012,.64)
    box(ax,.27,.18,.46,.18,"Terminal evidence ledger\nIDs • hashes • raw response • SQL • status • tokens • latency",GOLD,fs=10)
    arrow(ax,.845,.53,.67,.37)
    ax.text(.5,.07,"One generation per question/cell/backbone • no candidate ranking • no repair loop",ha="center",fontsize=10.2,color=RED,fontweight="bold")
    save(fig,"ma_r1_f01_executed_pipeline")


def fig2():
    fig, ax = setup((7.2, 3.75))
    ax.text(.5,.965,"Frozen 2 × 2 prompt-package experiment",ha="center",va="top",fontsize=14,fontweight="bold",color=INK)
    ax.text(.10,.77,"Context\npackage",ha="center",va="center",fontsize=11,fontweight="bold",color=INK)
    ax.text(.39,.86,"Composite hint OFF",ha="center",fontsize=11,fontweight="bold",color=INK)
    ax.text(.73,.86,"Composite hint ON",ha="center",fontsize=11,fontweight="bold",color=INK)
    box(ax,.24,.60,.30,.16,"F00\nFull DDL\n+ global values",BLUE,fs=8.7)
    box(ax,.58,.60,.30,.16,"F01\nF00 + composite\nSQL hint",ORANGE,fs=8.7)
    box(ax,.24,.35,.30,.16,"F10\nSelected schema\n+ domain grounding",TEAL,fs=8.7)
    box(ax,.58,.35,.30,.16,"F11\nF10 + composite\nSQL hint",RED,fs=8.7)
    ax.text(.11,.67,"FULL",ha="center",fontsize=10,fontweight="bold",color=BLUE)
    ax.text(.11,.42,"COMPACT",ha="center",fontsize=10,fontweight="bold",color=TEAL)
    arrow(ax,.39,.59,.39,.52); arrow(ax,.73,.59,.73,.52)
    arrow(ax,.545,.68,.575,.68); arrow(ax,.545,.43,.575,.43)
    box(ax,.20,.08,.68,.14,"Qwen-7B: one 180 × 4 run\nGranite-8B: one 180 × 4 run",GOLD,fs=9.4)
    ax.text(.5,.015,"1,440 canonical predictions total; “context” is a bundled package intervention",ha="center",fontsize=9.8,color=INK)
    save(fig,"ma_r1_f02_factorial_design")


def fig3():
    fig, ax = setup((7.2, 3.45))
    ax.text(.5,.96,"Evidence promotion and sealed external gate",ha="center",va="top",fontsize=14,fontweight="bold",color=INK)
    xs=[.03,.27,.51,.75]
    labels=[("91 visible\nauto-candidates",BLUE),("Dual review +\nadjudication",TEAL),("New isolated\nsealed set",NAVY),("One no-drop\nfrozen run",RED)]
    for x,(t,c) in zip(xs,labels): box(ax,x,.54,.19,.20,t,c,fs=8.7)
    for i in range(3): arrow(ax,xs[i]+.19,.64,xs[i+1]-.012,.64)
    box(ax,.07,.19,.37,.16,"Human-reviewed UNSEALED\nvisible candidates only",GOLD,fs=8.8)
    box(ax,.56,.19,.37,.16,"Eligible confirmatory evidence\nafter audit + license clearance",PALE,fs=8.8)
    arrow(ax,.365,.53,.255,.36); arrow(ax,.845,.53,.745,.36)
    ax.text(.5,.065,"No failed item dropped • separate dataset reporting • access log • permanent artifact",ha="center",fontsize=10,color=INK,fontweight="semibold")
    save(fig,"ma_r1_f03_external_evidence_gate")


def preview():
    paths=[OUT/"ma_r1_f01_executed_pipeline.png",OUT/"ma_r1_f02_factorial_design.png",OUT/"ma_r1_f03_external_evidence_gate.png"]
    fig, axes=plt.subplots(3,1,figsize=(8.27,11.69))
    fig.suptitle("MA-SQLGrid framework figures at approximate MDPI text width",fontsize=13,fontweight="bold")
    for ax,p in zip(axes,paths):
        ax.imshow(plt.imread(p)); ax.axis("off"); ax.set_title(p.stem,fontsize=9)
    fig.tight_layout(rect=(0.06,.03,.94,.96),h_pad=1.0)
    fig.savefig(QA/"page_scale_preview.pdf",dpi=300,facecolor="white")
    fig.savefig(QA/"page_scale_preview.png",dpi=200,facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    fig1(); fig2(); fig3(); preview()
    print("generated 3 figure families in SVG/PDF/450-dpi PNG plus page-scale preview")
