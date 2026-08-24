"""Generate the C2GES output-length diagnostic from packaged CSV evidence."""

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


PROJECT = Path(__file__).resolve().parents[3]
SOURCE = PROJECT / "03_Reproducibility" / "Data" / "postrun_diagnostics" / "output_length_summary.csv"
OUT = PROJECT / "03_Reproducibility" / "Figures"
FIXED_TIME = datetime(2026, 8, 24, tzinfo=timezone.utc)

CONDITIONS = [
    ("c2ges_full", "Full C2GES"),
    ("graph_no_cf_strict", "Unrenorm. removal"),
    ("semantic_mmr", "Semantic-MMR"),
    ("textrank", "TextRank"),
]

mpl.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "pdf.fonttype": 42,
    "svg.fonttype": "none",
})


def main() -> None:
    with SOURCE.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    indexed = {(row["condition"], int(row["budget"])): row for row in rows}
    required = [(condition, budget) for condition, _ in CONDITIONS for budget in (5, 10)]
    missing = [key for key in required if key not in indexed]
    if missing:
        raise RuntimeError(f"missing output-length records: {missing}")
    if any(int(indexed[key]["reports"]) != 15 for key in required):
        raise RuntimeError("every plotted output-length record must summarize 15 reports")

    labels = [label for _, label in CONDITIONS]
    k5 = [float(indexed[(condition, 5)]["mean_output_words"]) for condition, _ in CONDITIONS]
    k10 = [float(indexed[(condition, 10)]["mean_output_words"]) for condition, _ in CONDITIONS]
    x = np.arange(len(labels))
    width = 0.36
    fig, ax = plt.subplots(figsize=(8.2, 3.6))
    bars5 = ax.bar(x - width / 2, k5, width, label="K = 5", color="#3975A8")
    bars10 = ax.bar(x + width / 2, k10, width, label="K = 10", color="#E38336")
    ax.bar_label(bars5, fmt="%.1f", padding=2, fontsize=8)
    ax.bar_label(bars10, fmt="%.1f", padding=2, fontsize=8)
    ax.set_ylabel("Mean selected words per report")
    ax.set_xticks(x, labels)
    ax.set_ylim(0, 670)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False, ncol=2, loc="upper left")
    fig.tight_layout()

    OUT.mkdir(parents=True, exist_ok=True)
    metadata = {
        "Creator": "C2GES reproducible figure generator",
        "CreationDate": FIXED_TIME,
        "ModDate": FIXED_TIME,
    }
    fig.savefig(OUT / "fig05_output_length.pdf", metadata=metadata, bbox_inches="tight")
    svg_path = OUT / "fig05_output_length.svg"
    fig.savefig(svg_path, metadata={"Date": "2026-08-24"}, bbox_inches="tight")
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8",
    )
    fig.savefig(OUT / "fig05_output_length.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(OUT / "fig05_output_length.pdf")


if __name__ == "__main__":
    main()
