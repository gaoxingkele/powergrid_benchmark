"""Generate additional MA-SQLGrid figures from reported results and design."""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent
plt.rcParams.update({"font.size": 9, "font.family": "DejaVu Sans"})


def selector_diagnostics() -> None:
    names = ["Fixed order", "Validation only", "Complete witnesses"]
    correct = np.array([80, 100, 101])
    invariant = np.array([177, 179, 180])
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
    fig.savefig(OUT / "fig05_offline_selector_diagnostics.pdf", bbox_inches="tight")
    plt.close(fig)


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
    fig.savefig(OUT / "fig06_evidence_map.pdf", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    selector_diagnostics()
    evidence_map()
