"""Render the protocol-v0.2 aggregate ROUGE figure without changing results.

Input is the frozen run01 aggregate JSON. Output metadata records the input hash,
script hash, and plotted values so that the figure has a compact lineage record.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT.parent.parent
    / "original_title_rebuild"
    / "formal_runs"
    / "C2GES_NERC_FORMAL_v0_2_20260808_run01"
    / "aggregate_metrics.json"
)
OUTPUT = ROOT / "figures" / "fig_c2ges_v02_rouge_by_budget.png"
LINEAGE = ROOT / "figures" / "fig_c2ges_v02_rouge_by_budget.lineage.json"

METHODS = [
    ("lead", "Lead"),
    ("centroid", "Centroid"),
    ("textrank", "TextRank"),
    ("semantic_centroid", "Semantic\nCentroid"),
    ("role", "Role"),
    ("graph_no_cf_strict", "Strict\nno-CF"),
    ("c2ges_full", "Full\nC²GES"),
]
METRICS = [
    ("rouge1_f1", "ROUGE-1"),
    ("rouge2_f1", "ROUGE-2"),
    ("rougeL_f1", "ROUGE-L"),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> None:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.3), sharey=True)
    colors = ["#4472C4", "#ED7D31", "#70AD47"]
    x = np.arange(len(METHODS))
    width = 0.24
    plotted: dict[str, dict[str, dict[str, float]]] = {}

    for axis, budget in zip(axes, ("5", "10")):
        plotted[budget] = {}
        for offset, ((metric, label), color) in enumerate(zip(METRICS, colors)):
            values = [float(data[budget][key][metric]) for key, _ in METHODS]
            axis.bar(x + (offset - 1) * width, values, width, label=label, color=color)
            for (key, _), value in zip(METHODS, values):
                plotted[budget].setdefault(key, {})[metric] = value
        axis.set_title(f"Selection budget K={budget}", fontweight="bold")
        axis.set_xticks(x)
        axis.set_xticklabels([label for _, label in METHODS], fontsize=8.5)
        axis.set_ylim(0, 0.42)
        axis.grid(axis="y", alpha=0.25, linewidth=0.7)
        axis.set_axisbelow(True)
        axis.set_xlabel("Frozen condition")

    axes[0].set_ylabel("Mean ROUGE F1 on 16 test reports")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.925), ncol=3, frameon=False)
    fig.suptitle("C²GES protocol v0.2: aggregate overlap by budget", y=0.99, fontweight="bold")
    fig.text(
        0.5,
        -0.01,
        "Descriptive means only; paired bootstrap intervals are reported in the manuscript.",
        ha="center",
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0.03, 1, 0.84))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=240, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    metadata = {
        "protocol": "C2GES-NERC-FORMAL-v0.2",
        "input": str(SOURCE),
        "input_sha256": sha256(SOURCE),
        "script_sha256": sha256(Path(__file__)),
        "output": str(OUTPUT),
        "output_sha256": sha256(OUTPUT),
        "budgets": [5, 10],
        "n_test_reports": 16,
        "plotted_values": plotted,
        "note": "Descriptive visualization of frozen aggregate means; no recomputation or inferential test.",
    }
    LINEAGE.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
