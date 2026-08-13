"""Build inferential tables for the frozen P2 exact-hierarchy experiment.

This script performs no model training. It reads the 440 frozen v8 records,
holds OLS reconciliation fixed, and compares CSA-LoadNet (historical evidence
label HyG-LoadFormer (neural)) with external baselines and ablations in
separate Holm families.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from scipy.stats import mannwhitneyu


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "papers" / "mintou" / "mintou_p2_hygraph_load_forecasting" / "evidence"
SOURCE = EVIDENCE / "runs" / "real_ausgrid_exact_hierarchy_v8_results.csv"
OUTPUT = EVIDENCE / "tables" / "real_ausgrid_exact_hierarchy_v8_significance.csv"
PROPOSED = "HyG-LoadFormer (neural)"


def holm(raw: list[float]) -> list[float]:
    order = sorted(range(len(raw)), key=raw.__getitem__)
    adjusted = [1.0] * len(raw)
    running = 0.0
    m = len(raw)
    for rank, idx in enumerate(order):
        running = max(running, min(1.0, (m - rank) * raw[idx]))
        adjusted[idx] = running
    return adjusted


def main() -> None:
    data = pd.read_csv(SOURCE)
    data = data[data["reconciliation"].eq("OLS-Reconciled")].copy()
    proposed = data[data["method"].eq(PROPOSED)]["hierarchy_weighted_smape"]
    if len(proposed) != 10:
        raise RuntimeError(f"Expected 10 proposed OLS seeds, found {len(proposed)}")

    families = {
        "external_baselines": data[data["method_role"].eq("baseline")]["method"].drop_duplicates().tolist(),
        "component_ablations": data[data["method_role"].eq("ablation")]["method"].drop_duplicates().tolist(),
    }
    rows: list[dict[str, object]] = []
    for family, opponents in families.items():
        family_rows: list[dict[str, object]] = []
        raw: list[float] = []
        for opponent in opponents:
            values = data[data["method"].eq(opponent)]["hierarchy_weighted_smape"]
            if len(values) != 10:
                raise RuntimeError(f"Expected 10 OLS seeds for {opponent}, found {len(values)}")
            test = mannwhitneyu(proposed, values, alternative="two-sided")
            p_value = float(test.pvalue)
            raw.append(p_value)
            family_rows.append(
                {
                    "family": family,
                    "reconciliation": "OLS-Reconciled",
                    "comparison": f"CSA-LoadNet vs {opponent}",
                    "n_per_group": 10,
                    "mean_proposed": proposed.mean(),
                    "mean_opponent": values.mean(),
                    "mean_diff": proposed.mean() - values.mean(),
                    "u_statistic": float(test.statistic),
                    "p_value": p_value,
                }
            )
        adjusted = holm(raw)
        for row, p_holm in zip(family_rows, adjusted):
            row["p_holm"] = p_holm
            row["significant_005_holm"] = p_holm < 0.05
            diff = float(row["mean_diff"])
            row["verdict"] = "win" if diff < 0 and p_holm < 0.05 else (
                "loss" if diff > 0 and p_holm < 0.05 else "not_separable"
            )
        rows.extend(family_rows)

    out = pd.DataFrame(rows)
    out.to_csv(OUTPUT, index=False, encoding="utf-8-sig", float_format="%.10g")
    print(f"wrote {len(out)} comparisons -> {OUTPUT}")


if __name__ == "__main__":
    main()
