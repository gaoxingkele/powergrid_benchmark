"""Generate the C2GES path-deletion diagnostic from machine-readable audits."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


PROJECT = Path(__file__).resolve().parents[3]
OUT = PROJECT / "03_Reproducibility" / "Figures"
POSTRUN_AUDIT = PROJECT / "03_Reproducibility" / "Data" / "audits" / "POSTRUN_AUDIT_v0_3_1.json"
CALIBRATION_DECISION = (
    PROJECT
    / "03_Reproducibility"
    / "Code"
    / "dev_calibration"
    / "artifacts"
    / "CALIBRATION_DECISION.json"
)
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


def load_inputs() -> tuple[dict, dict]:
    audit = json.loads(POSTRUN_AUDIT.read_text(encoding="utf-8"))
    calibration = json.loads(CALIBRATION_DECISION.read_text(encoding="utf-8"))
    if audit.get("verdict") != "PASS":
        raise ValueError("post-run audit is not PASS")
    if audit.get("recalculation", {}).get("contrast_max_absolute_difference") != 0.0:
        raise ValueError("registered contrasts did not reproduce exactly")
    if calibration.get("test_input_accessed") is not False:
        raise ValueError("development calibration did not preserve the test boundary")
    return audit, calibration


def main():
    audit, calibration = load_inputs()
    method = audit["method_checks"]
    contrast_rows = {
        int(row["budget"]): row
        for row in audit["recalculation"]["contrasts"]
        if row["baseline"] == "graph_no_cf_strict"
    }
    if set(contrast_rows) != {5, 10}:
        raise ValueError("expected strict-removal contrasts at K=5 and K=10")

    changed_scores = int(method["nonzero_sentence_score_differences"])
    score_total = int(method["sentence_score_comparisons"])
    changed_selections = int(method["cf_vs_no_cf_selection_distinct_cases"])
    selection_total = int(method["cf_vs_no_cf_selection_total_cases"])
    if not (0 <= changed_scores <= score_total and 0 <= changed_selections <= selection_total):
        raise ValueError("invalid diagnostic counts")

    winner_frequency = calibration["winner_frequency"]
    selected_folds = sum(int(value) for value in winner_frequency.values())
    zero_weight_id = calibration["robust_overall"]["candidate_id"]
    zero_weight_folds = int(winner_frequency.get(zero_weight_id, 0))
    if float(calibration["robust_overall"]["cf_weight"]) != 0.0:
        raise ValueError("calibration winner is not the zero path-weight condition")

    fig, axes = plt.subplots(1, 4, figsize=(10.6, 2.9))
    blue, amber, green, gray = "#0077BB", "#EE7733", "#009988", "#C7CDD1"

    counts = np.array([changed_scores, score_total - changed_scores])
    axes[0].bar([0, 1], counts, color=[blue, gray], edgecolor="black", linewidth=0.4)
    axes[0].set_xticks([0, 1], ["Changed", "Unchanged"])
    axes[0].set_ylabel("Sentence-score comparisons")
    axes[0].set_title("(a) Score activity")
    offset = max(counts) * 0.04
    axes[0].text(0, counts[0] + offset, str(counts[0]), ha="center", fontsize=8)
    axes[0].text(1, counts[1] + offset, str(counts[1]), ha="center", fontsize=8)
    axes[0].set_ylim(0, max(counts) * 1.15)

    selections = np.array([changed_selections, selection_total - changed_selections])
    axes[1].bar([0, 1], selections, color=[green, gray], edgecolor="black", linewidth=0.4)
    axes[1].set_xticks([0, 1], ["Changed", "Same"])
    axes[1].set_ylabel("Report--budget cells")
    axes[1].set_title("(b) Selection activity")
    selection_offset = max(selections) * 0.025
    axes[1].text(0, selections[0] + selection_offset, str(selections[0]), ha="center", fontsize=8)
    axes[1].text(1, selections[1] + selection_offset, str(selections[1]), ha="center", fontsize=8)
    axes[1].set_ylim(0, max(selections) * 1.14)

    means = np.array([float(contrast_rows[k]["mean_delta_rougeL"]) for k in (5, 10)])
    lower = np.array([float(contrast_rows[k]["ci95"][0]) for k in (5, 10)])
    upper = np.array([float(contrast_rows[k]["ci95"][1]) for k in (5, 10)])
    yerr = np.vstack((means - lower, upper - means))
    axes[2].axhline(0, color="black", linewidth=0.8)
    axes[2].errorbar([0, 1], means, yerr=yerr, fmt="o", color=amber, ecolor=amber, capsize=4)
    axes[2].set_xticks([0, 1], ["K=5", "K=10"])
    axes[2].set_ylabel("Full - unrenorm. removal ROUGE-L")
    axes[2].set_title("(c) Endpoint effect")
    axes[2].set_ylim(-0.014, 0.006)

    weight_counts = [zero_weight_folds, selected_folds - zero_weight_folds]
    axes[3].bar([0, 1], weight_counts, color=[gray, blue], edgecolor="black", linewidth=0.4)
    axes[3].set_xticks([0, 1], ["Zero", "Nonzero"])
    axes[3].set_ylabel("Leave-one-report-out folds")
    axes[3].set_title("(d) Selected weight")
    weight_offset = max(weight_counts) * 0.025
    axes[3].text(0, weight_counts[0] + weight_offset, str(weight_counts[0]), ha="center", fontsize=8)
    axes[3].text(1, weight_counts[1] + weight_offset, str(weight_counts[1]), ha="center", fontsize=8)
    axes[3].set_ylim(0, max(weight_counts) * 1.125)

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
    print(f"inputs: {POSTRUN_AUDIT}; {CALIBRATION_DECISION}")


if __name__ == "__main__":
    main()
