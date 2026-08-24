"""Generate the C2GES path-deletion component diagnostic from retained results."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


PROJECT = Path(__file__).resolve().parents[3]
OUT = PROJECT / "03_Reproducibility" / "Figures"
OUT.mkdir(parents=True, exist_ok=True)
FIXED_TIME = datetime(2026, 8, 12, tzinfo=timezone.utc)

mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
        "font.size": 9,
        "axes.labelsize": 9,
        "axes.titlesize": 10,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "pdf.fonttype": 42,
        "svg.fonttype": "none",
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)


def main():
    fig, axes = plt.subplots(1, 4, figsize=(10.6, 2.9))
    blue, amber, green, gray = "#0077BB", "#EE7733", "#009988", "#C7CDD1"

    counts = np.array([9774, 19008 - 9774])
    axes[0].bar([0, 1], counts, color=[blue, gray], edgecolor="black", linewidth=0.4)
    axes[0].set_xticks([0, 1], ["Changed", "Unchanged"])
    axes[0].set_ylabel("Sentence-score comparisons")
    axes[0].set_title("(a) Score activity")
    axes[0].text(0, counts[0] + 380, "9774", ha="center", fontsize=8)
    axes[0].text(1, counts[1] + 380, "9234", ha="center", fontsize=8)
    axes[0].set_ylim(0, 11200)

    selections = np.array([28, 2])
    axes[1].bar([0, 1], selections, color=[green, gray], edgecolor="black", linewidth=0.4)
    axes[1].set_xticks([0, 1], ["Changed", "Same"])
    axes[1].set_ylabel("Report--budget cells")
    axes[1].set_title("(b) Selection activity")
    axes[1].text(0, 28.5, "28", ha="center", fontsize=8)
    axes[1].text(1, 2.5, "2", ha="center", fontsize=8)
    axes[1].set_ylim(0, 32)

    means = np.array([-0.003332, -0.003360])
    lower = np.array([-0.010889, -0.008306])
    upper = np.array([0.002826, 0.001040])
    yerr = np.vstack((means - lower, upper - means))
    axes[2].axhline(0, color="black", linewidth=0.8)
    axes[2].errorbar([0, 1], means, yerr=yerr, fmt="o", color=amber, ecolor=amber, capsize=4)
    axes[2].set_xticks([0, 1], ["K=5", "K=10"])
    axes[2].set_ylabel("Full - unrenorm. removal ROUGE-L")
    axes[2].set_title("(c) Endpoint effect")
    axes[2].set_ylim(-0.014, 0.006)

    axes[3].bar([0, 1], [12, 0], color=[gray, blue], edgecolor="black", linewidth=0.4)
    axes[3].set_xticks([0, 1], ["Zero", "Nonzero"])
    axes[3].set_ylabel("Leave-one-report-out folds")
    axes[3].set_title("(d) Selected weight")
    axes[3].text(0, 12.25, "12", ha="center", fontsize=8)
    axes[3].text(1, 0.25, "0", ha="center", fontsize=8)
    axes[3].set_ylim(0, 13.5)

    for ax in axes:
        ax.grid(axis="y", alpha=0.18)
    fig.tight_layout(w_pad=1.2)
    metadata = {
        "Creator": "C2GES reproducible figure generator",
        "CreationDate": FIXED_TIME,
        "ModDate": FIXED_TIME,
    }
    fig.savefig(OUT / "fig06_component_diagnostic.pdf", metadata=metadata)
    svg_path = OUT / "fig06_component_diagnostic.svg"
    fig.savefig(svg_path, metadata={"Date": "2026-08-12"})
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8",
    )
    fig.savefig(OUT / "fig06_component_diagnostic.png", dpi=300)
    plt.close(fig)
    print(OUT / "fig06_component_diagnostic.pdf")


if __name__ == "__main__":
    main()
