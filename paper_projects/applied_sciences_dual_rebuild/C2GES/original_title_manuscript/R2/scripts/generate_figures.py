from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

HERE = Path(__file__).resolve().parent
R2 = HERE.parent
ROOT = R2.parents[4]
RUN = ROOT / "paper_projects/applied_sciences_dual_rebuild/C2GES/original_title_rebuild/R2_v0_3/formal_runs_v0_3_1/c2ges_v031_formal_20260808"
AGG = RUN / "aggregate_metrics.json"
PRED = RUN / "predictions.jsonl"
EXPECTED = {
    "aggregate_metrics.json": "DF9D9E4EF21BE0BDEC401C27D732D6A2692980FA8C018B119E41D85EE22149AA",
    "predictions.jsonl": "AAE2BFE0E6C426B6A69D727F24239A07DFD7DBEE8A4CE228E86625CCDCA2338F",
}
for path in (AGG, PRED):
    got = hashlib.sha256(path.read_bytes()).hexdigest().upper()
    assert got == EXPECTED[path.name], (path, got)

OUT = R2 / "figures"
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9,
    "axes.labelsize": 9, "xtick.labelsize": 8, "ytick.labelsize": 8,
    "legend.fontsize": 8, "savefig.dpi": 300, "savefig.bbox": "tight",
    "axes.spines.top": False, "axes.spines.right": False,
})
COL = ["#0077BB", "#EE7733", "#009988", "#CC3311", "#33BBEE", "#BBBBBB", "#000000"]


def save(fig, stem: str):
    fig.savefig(OUT / f"{stem}.pdf")
    fig.savefig(OUT / f"{stem}.png", dpi=300)
    plt.close(fig)


def architecture():
    fig, ax = plt.subplots(figsize=(7.0, 3.25))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")
    boxes = [
        (0.2, 3.45, 1.65, .85, "Full-PDF body\n(after summary gate)"),
        (2.15, 3.45, 1.55, .85, "Sentence roles\n(lexical proxies)"),
        (4.0, 3.45, 1.55, .85, "Typed directed\nproxy graph"),
        (5.85, 3.45, 1.75, .85, "2--4-edge typed\npath utility"),
        (7.9, 3.45, 1.85, .85, "Node deletion\nstructural score"),
        (1.1, 1.35, 1.45, .85, "Centroid\nrelevance Q"),
        (2.9, 1.35, 1.35, .85, "Role R"),
        (4.6, 1.35, 1.35, .85, "Degree G"),
        (6.3, 1.35, 1.35, .85, "Deletion C"),
        (8.0, 1.35, 1.75, .85, "Greedy MMR-like\nselection; K=5,10"),
    ]
    for i,(x,y,w,h,label) in enumerate(boxes):
        fc = "#E8F1F8" if i < 5 else "#F4F4F4"
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=.03",fc=fc,ec="#2F4858",lw=1.1))
        ax.text(x+w/2,y+h/2,label,ha="center",va="center",fontsize=8)
    for a,b in [((1.85,3.88),(2.15,3.88)),((3.7,3.88),(4.0,3.88)),((5.55,3.88),(5.85,3.88)),((7.6,3.88),(7.9,3.88)),
                ((1.05,3.45),(1.75,2.2)),((2.9,3.45),(3.55,2.2)),((4.75,3.45),(5.25,2.2)),((8.8,3.45),(6.95,2.2)),
                ((2.55,1.78),(2.9,1.78)),((4.25,1.78),(4.6,1.78)),((5.95,1.78),(6.3,1.78)),((7.65,1.78),(8.0,1.78))]:
        ax.add_patch(FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=10,lw=1,color="#555555"))
    ax.text(5,0.55,"All edges and 'counterfactuals' are text-derived structural proxies; no physical causal effect is identified.",ha="center",fontsize=8,style="italic")
    save(fig,"fig01_algorithm")


def dataset_flow():
    fig, ax = plt.subplots(figsize=(7.0, 2.7)); ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(0,4)
    labels=[("40 complete PDFs\n3,200 pages",.25),("13 excluded\nfail-closed gates",2.6),("27 retained\n12,924 candidates",5.0),("12 development\n144 configurations",7.35),("15 test reports\none authorized run",7.35)]
    ys=[2.35,2.35,2.35,3.1,1.15]
    for (lab,x),y in zip(labels,ys):
        ax.add_patch(FancyBboxPatch((x,y),2.0,.72,boxstyle="round,pad=.03",fc="#E8F1F8",ec="#2F4858"))
        ax.text(x+1,y+.36,lab,ha="center",va="center",fontsize=8)
    for a,b in [((2.25,2.71),(2.6,2.71)),((4.6,2.71),(5.0,2.71)),((7.0,2.71),(7.35,3.46)),((7.0,2.71),(7.35,1.51))]:
        ax.add_patch(FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=10,color="#555"))
    ax.text(5,0.3,"Independent gates: page boundary, exact match, >=50-character substring, pollution patterns, split integrity, and SHA-256 binding.",ha="center",fontsize=8)
    save(fig,"fig02_dataset_flow")


def aggregate():
    d=json.loads(AGG.read_text(encoding="utf-8")); order=["lead","centroid","textrank","semantic_mmr","role","graph_no_cf_strict","c2ges_full"]
    names=["Lead","Centroid","TextRank","Semantic-MMR","Role","Graph no-CF","Full C2GES"]
    fig,axs=plt.subplots(1,2,figsize=(7.0,3.0),sharey=True)
    x=np.arange(len(order)); width=.72
    for ax,k in zip(axs,["5","10"]):
        vals=[d[k][m]["rougeL_f1"] for m in order]
        ax.bar(x,vals,width,color=COL,edgecolor="black",linewidth=.35)
        ax.set_xticks(x,names,rotation=45,ha="right"); ax.set_title(f"K = {k}"); ax.set_ylim(0,.15); ax.set_ylabel("Mean ROUGE-L F1")
        ax.grid(axis="y",alpha=.2)
    fig.tight_layout(); save(fig,"fig03_aggregate_rougel")


def paired():
    rows=[json.loads(x) for x in PRED.read_text(encoding="utf-8").splitlines()]
    idx={(r["doc_id"],r["budget"],r["condition"]):r["metrics"]["rougeL_f1"] for r in rows}
    docs=sorted({r["doc_id"] for r in rows}); bases=["graph_no_cf_strict","semantic_mmr","textrank"]
    names=["Graph no-CF","Semantic-MMR","TextRank"]
    fig,axs=plt.subplots(2,3,figsize=(7.0,4.6),sharey=True)
    for rr,k in enumerate([5,10]):
        for cc,(base,name) in enumerate(zip(bases,names)):
            ax=axs[rr,cc]; vals=np.array([idx[(d,k,"c2ges_full")]-idx[(d,k,base)] for d in docs])
            ax.axhline(0,color="black",lw=.8); ax.scatter(np.arange(1,16),vals,color=COL[cc],s=15,alpha=.85)
            ax.plot([.5,15.5],[vals.mean(),vals.mean()],color=COL[cc],lw=1.8)
            ax.set_title(f"K={k}: Full - {name}",fontsize=8); ax.set_xlim(.5,15.5); ax.set_xticks([1,5,10,15]); ax.set_xlabel("Test report index")
            if cc==0: ax.set_ylabel("Paired ROUGE-L difference")
    fig.tight_layout(); save(fig,"fig04_paired_differences")


architecture(); dataset_flow(); aggregate(); paired()
lineage={
  "source_sha256": EXPECTED,
  "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest().upper(),
  "artifacts": ["fig01_algorithm.pdf","fig02_dataset_flow.pdf","fig03_aggregate_rougel.pdf","fig04_paired_differences.pdf"],
  "limitations": ["Aggregate bars show means without uncertainty; paired uncertainty is reported in the manuscript.","Causal/counterfactual labels describe structural text proxies, not identified physical effects."]
}
(OUT/"FIGURE_LINEAGE.json").write_text(json.dumps(lineage,indent=2),encoding="utf-8")
