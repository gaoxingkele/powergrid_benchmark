"""Generate Figures 5--6 from packaged, release-local sources."""

import csv
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent
SOURCE = OUT / "lineage_sources" / "fig05_selector_diagnostics.csv"
plt.rcParams.update({"font.size": 9, "font.family": "DejaVu Sans"})


def save_all(fig, stem: str) -> None:
    for suffix in ("pdf", "svg", "png"):
        kwargs = {"bbox_inches": "tight"}
        if suffix == "png":
            kwargs["dpi"] = 400
        fig.savefig(OUT / f"{stem}.{suffix}", **kwargs)
    plt.close(fig)


def selector_diagnostics() -> None:
    with SOURCE.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 3:
        raise ValueError(f"Expected three selectors in {SOURCE}, found {len(rows)}")
    names = [row["selector"] for row in rows]
    correct = np.array([int(row["reference_matches"]) for row in rows])
    invariant = np.array([int(row["metamorphic_invariant"]) for row in rows])
    x = np.arange(3)
    width = 0.36
    fig, ax = plt.subplots(figsize=(8.2, 3.7))
    b1 = ax.bar(x - width / 2, correct, width, label="Reference matches",
                color="#3975a8")
    b2 = ax.bar(x + width / 2, invariant, width, label="Metamorphically invariant",
                color="#75a867")
    ax.bar_label(b1, padding=2)
    ax.bar_label(b2, padding=2)
    ax.set_ylabel("Questions out of 180")
    ax.set_xticks(x, names)
    ax.set_ylim(0, 200)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False, ncol=2, loc="upper left")
    fig.tight_layout()
    save_all(fig, "fig05_offline_selector_diagnostics")


def evidence_map() -> None:
    rows = [
        ("Executor and trace tests", "implemented safety boundary", "#d8ead2"),
        ("GridDB/component protocols", "finite-corpus component evidence", "#d8ead2"),
        ("BIRD Mini-Dev", "non-grid portability evidence", "#dbe7f5"),
        ("Historical-pool re-execution", "descriptive selector behavior", "#f7dfb2"),
        ("Prospective five-role benefit", "not evaluated", "#efc1c1"),
        ("Operational grid validity", "not evaluated", "#efc1c1"),
    ]
    fig, ax = plt.subplots(figsize=(8.2, 4.7))
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")
    for i, (source, claim, color) in enumerate(rows):
        y = 6.1 - i
        ax.add_patch(plt.Rectangle((0.5, y - 0.35), 9, 0.7,
                                   facecolor=color, edgecolor="#555", lw=0.8))
        ax.text(0.8, y, source, va="center", fontweight="bold")
        ax.text(9.2, y, claim, va="center", ha="right")
    ax.text(5, 6.7, "Evidence classes and claim ceiling", ha="center",
            fontsize=11, fontweight="bold")
    fig.tight_layout()
    save_all(fig, "fig06_evidence_map")


if __name__ == "__main__":
    selector_diagnostics()
    evidence_map()
