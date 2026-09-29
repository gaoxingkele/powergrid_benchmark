"""Figure S5: budget-efficiency curves on the frozen external corpus (G1b).

Left panel: equal-word budgets.  Right panel: equal-unit budgets.  The point of
the figure is that the *ranking* of the arms is a property of the budget type,
and that the equal-unit protocol lets the role-conditioned arms pack roughly
1.5-3x more words into each selected unit.

Input : 03_Reproducibility/Data/external_prospective_v1/external_arms_curve_v4.json
Output: 01_Manuscript/Supplementary/figures/figS5_budget_efficiency_curve.pdf
        03_Reproducibility/Data/budget_curve_v1/figS5_source.csv
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
DATA = PROJECT / "03_Reproducibility" / "Data"
SOURCE = DATA / "external_prospective_v1" / "external_arms_curve_v4.json"
OUT_FIG = PROJECT / "01_Manuscript" / "Supplementary" / "figures" / "figS5_budget_efficiency_curve.pdf"
OUT_CSV = DATA / "budget_curve_v1" / "figS5_source.csv"

STYLE = {
    "AB0": ("#4C72B0", "o", "AB-0 lexical+position"),
    "AB2": ("#DD8452", "s", "AB-2 role-conditioned"),
    "no_path": ("#55A868", "^", "C2GES no-path"),
    "Full": ("#C44E52", "v", "C2GES full (path)"),
    "TextRank": ("#8172B3", "D", "TextRank"),
    "Lead": ("#937860", "P", "Lead"),
}


def main() -> None:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    summary = payload["summary"]
    word_budgets = payload["word_budgets"]
    unit_budgets = payload["unit_budgets"]

    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.0))
    for panel, (axis, budgets, kind, xlabel) in enumerate(
        (
            (axes[0], word_budgets, "word", "Equal-word budget (selected words)"),
            (axes[1], unit_budgets, "unit", "Equal-unit budget (selected units)"),
        )
    ):
        for arm, (colour, marker, label) in STYLE.items():
            xs = [b for b in budgets if f"{kind}:{b}" in summary and arm in summary[f"{kind}:{b}"]]
            ys = [summary[f"{kind}:{b}"][arm]["mean_rougeL"] for b in xs]
            wpu = [summary[f"{kind}:{b}"][arm]["words_per_unit"] for b in xs]
            axis.plot(xs, ys, marker=marker, color=colour, label=label if panel == 0 else None, linewidth=1.6, markersize=5)
            if arm in ("AB2", "TextRank"):
                for x, y, w in zip(xs, ys, wpu):
                    axis.annotate(f"{w:.0f} w/u", (x, y), textcoords="offset points", xytext=(0, -13),
                                  ha="center", fontsize=6.5, color=colour)
        axis.set_xlabel(xlabel, fontsize=9)
        axis.set_ylabel("Mean ROUGE-L F1", fontsize=9)
        axis.grid(alpha=0.25, linewidth=0.6)
        axis.tick_params(labelsize=8)
    axes[0].set_title("(a) controls at equal selected words", fontsize=9.5)
    axes[1].set_title("(b) controls at equal selected units", fontsize=9.5)
    axes[0].legend(fontsize=7.5, loc="lower right", frameon=False)
    fig.suptitle(
        "Arm ranking on the frozen 24-report external corpus depends on the budget type "
        "(labels: selected words per unit)",
        fontsize=9.5,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    OUT_FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_FIG, bbox_inches="tight")
    plt.close(fig)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["budget_type", "budget", "arm", "mean_rougeL", "mean_units", "mean_words", "words_per_unit"])
        for kind, budgets in (("word", word_budgets), ("unit", unit_budgets)):
            for budget in budgets:
                for arm in STYLE:
                    entry = summary.get(f"{kind}:{budget}", {}).get(arm)
                    if entry:
                        writer.writerow(
                            [kind, budget, arm, entry["mean_rougeL"], entry["mean_units"], entry["mean_words"],
                             entry["words_per_unit"]]
                        )
    print(f"wrote {OUT_FIG}")
    print(f"wrote {OUT_CSV}")


if __name__ == "__main__":
    main()
