#!/usr/bin/env python3
"""Generate pilot ablation and reservation-path interaction figures."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run_dir", type=Path, default=Path("run_1"))
    args = parser.parse_args()
    run_dir = args.run_dir.resolve()
    rows = read_rows(run_dir / "factorial_aggregate_metrics.csv")

    chain = [f"AB-{index}" for index in range(7)]
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.0), constrained_layout=True)
    for budget, marker in ((110, "o"), (260, "s")):
        values = [next(float(row["rougeL_f1"]) for row in rows if int(row["word_budget"]) == budget and row["condition"] == condition) for condition in chain]
        axes[0].plot(chain, values, marker=marker, linewidth=1.8, label=f"{budget} words")
    axes[0].set_title("Development-Pilot Component Chain")
    axes[0].set_ylabel("Mean ROUGE-L F1")
    axes[0].grid(alpha=0.25)
    axes[0].legend(frameon=False)

    for budget, linestyle in ((110, "-"), (260, "--")):
        for reservation, conditions, color in (("off", ("RP-00", "RP-01"), "#377eb8"), ("on", ("RP-10", "RP-11"), "#e41a1c")):
            values = [next(float(row["rougeL_f1"]) for row in rows if int(row["word_budget"]) == budget and row["condition"] == condition) for condition in conditions]
            axes[1].plot([0, 1], values, marker="o", linestyle=linestyle, color=color, label=f"reservation {reservation}, {budget}w")
    axes[1].set_xticks([0, 1], ["path off", "path on"])
    axes[1].set_title("Reservation × Path Interaction")
    axes[1].set_ylabel("Mean ROUGE-L F1")
    axes[1].grid(alpha=0.25)
    axes[1].legend(frameon=False, fontsize=8)
    fig.savefig(run_dir / "Figure_1.png", dpi=300)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.0), constrained_layout=True)
    rp = ["RP-00", "RP-10", "RP-01", "RP-11"]
    x_positions = list(range(len(rp)))
    for budget, marker in ((110, "o"), (260, "s")):
        role = [next(float(row["role_coverage"]) for row in rows if int(row["word_budget"]) == budget and row["condition"] == condition) for condition in rp]
        edge = [next(float(row["typed_edge_coverage"]) for row in rows if int(row["word_budget"]) == budget and row["condition"] == condition) for condition in rp]
        axes[0].plot(x_positions, role, marker=marker, label=f"{budget} words")
        axes[1].plot(x_positions, edge, marker=marker, label=f"{budget} words")
    axes[0].set_title("Role-Group Coverage")
    axes[1].set_title("Selected-Node Typed-Edge Coverage")
    for axis in axes:
        axis.set_xticks(x_positions, rp, rotation=18, ha="right")
        axis.set_ylim(0, 1.03)
        axis.grid(alpha=0.25)
        axis.legend(frameon=False)
    fig.savefig(run_dir / "Figure_2.png", dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
