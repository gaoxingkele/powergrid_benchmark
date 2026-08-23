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
    """Render the scientific evidence flow rather than an audit/permission table."""
    streams = [
        ("GridDB generation\n1,440 predictions", "Context and\nhint effects", "#DDEBF7"),
        ("Component study\n700 calls", "Value evidence and\ncandidate selection", "#E2F0D9"),
        ("Constructed states\n25,920 rows", "Execution and\nstate stability", "#FFF2CC"),
        ("BIRD Mini-Dev\n11 databases", "Cross-database\nportability", "#E4DFEC"),
    ]
    fig, ax = plt.subplots(figsize=(9.0, 4.9))
    ax.set_xlim(0, 12); ax.set_ylim(0, 8); ax.axis("off")
    ax.text(6, 7.55, "Complementary evidence flow in MA-SQLGrid", ha="center",
            fontsize=12, fontweight="bold")

    for i, (source, finding, color) in enumerate(streams):
        y = 6.45 - i * 1.35
        ax.add_patch(plt.Rectangle((0.45, y - 0.42), 3.1, 0.84,
                                   facecolor=color, edgecolor="#4D4D4D", lw=0.9))
        ax.text(2.0, y, source, ha="center", va="center", fontweight="bold")
        ax.annotate("", xy=(4.15, y), xytext=(3.55, y),
                    arrowprops=dict(arrowstyle="->", lw=1.2, color="#4D4D4D"))
        ax.add_patch(plt.Rectangle((4.15, y - 0.42), 3.1, 0.84,
                                   facecolor="#F2F2F2", edgecolor="#4D4D4D", lw=0.9))
        ax.text(5.7, y, finding, ha="center", va="center")

    ax.add_patch(plt.Rectangle((8.35, 3.05), 3.15, 2.85,
                               facecolor="#D9EAD3", edgecolor="#3F6B3A", lw=1.2))
    ax.text(9.925, 5.52, "Shared workflow evidence", ha="center", va="center",
            fontweight="bold")
    ax.text(9.925, 4.72, "Read-only execution\nShared blackboard trace\nDeterministic adjudication",
            ha="center", va="center", linespacing=1.35)
    ax.text(9.925, 3.43, "Unified evaluator\n76  ->  99  ->  100",
            ha="center", va="center", fontweight="bold", color="#1F4E79")
    for i in range(len(streams)):
        y = 6.45 - i * 1.35
        ax.annotate("", xy=(8.35, 4.48), xytext=(7.25, y),
                    arrowprops=dict(arrowstyle="->", lw=0.9, color="#777777"))

    ax.add_patch(plt.Rectangle((8.35, 0.9), 3.15, 1.15,
                               facecolor="#FCE4D6", edgecolor="#A65E2E", lw=1.0))
    ax.text(9.925, 1.68, "Observed stability limit", ha="center", va="center",
            fontweight="bold")
    ax.text(9.925, 1.26, "130/180 top-score ties\norder-sensitive selection",
            ha="center", va="center")
    ax.annotate("", xy=(9.925, 2.05), xytext=(9.925, 3.05),
                arrowprops=dict(arrowstyle="->", lw=1.2, color="#A65E2E"))
    fig.tight_layout()
    save_all(fig, "fig06_evidence_map")


if __name__ == "__main__":
    selector_diagnostics()
    evidence_map()
