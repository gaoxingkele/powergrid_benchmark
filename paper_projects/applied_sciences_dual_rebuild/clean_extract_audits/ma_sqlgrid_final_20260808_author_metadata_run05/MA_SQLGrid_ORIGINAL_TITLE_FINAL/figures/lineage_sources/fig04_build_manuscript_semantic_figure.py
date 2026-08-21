"""Build the manuscript forest plot from the frozen v5 contrast CSV."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contrasts", type=Path, required=True)
    parser.add_argument("--exact-tests", type=Path, required=True)
    parser.add_argument("--suite", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--table-dir", type=Path, required=True)
    parser.add_argument("--lineage", type=Path, required=True)
    args = parser.parse_args()

    with args.contrasts.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 9:
        raise ValueError(f"Expected the frozen nine-test family, found {len(rows)} rows")
    with args.exact_tests.open(encoding="utf-8-sig", newline="") as handle:
        exact_rows = list(csv.DictReader(handle))
    if len(exact_rows) != 9 or any(float(row["exact_two_sided_p_holm"]) != 1.0 for row in exact_rows):
        raise ValueError("Exact nine-test sensitivity is incomplete or changes the Holm conclusion")
    with args.suite.open(encoding="utf-8-sig", newline="") as handle:
        suite_rows = list(csv.DictReader(handle))
    if len(suite_rows) != 1440:
        raise ValueError(f"Expected 1,440 frozen suite rows, found {len(suite_rows)}")

    backbone_label = {
        "qwen": "Qwen",
        "granite": "Granite",
        "granite_minus_qwen": "Granite - Qwen",
    }
    effect_label = {"hint": "hint", "compact": "context", "interaction": "interaction"}
    colors = {"qwen": "#2F6B9A", "granite": "#D47A32", "granite_minus_qwen": "#567D46"}

    labels = [
        f"{backbone_label[row['backbone_or_modifier']]}: {effect_label[row['effect']]}"
        for row in rows
    ]
    estimates = [float(row["estimate"]) for row in rows]
    lows = [float(row["composition_sensitivity_low"]) for row in rows]
    highs = [float(row["composition_sensitivity_high"]) for row in rows]
    y = list(range(len(rows) - 1, -1, -1))

    plt.rcParams.update({"font.size": 9, "axes.titlesize": 11, "axes.labelsize": 9})
    fig, ax = plt.subplots(figsize=(7.4, 4.6), constrained_layout=True)
    ax.axvspan(-0.02, 0.02, color="#E8E8E8", zorder=0)
    ax.axvline(0, color="#444444", linewidth=1.0, zorder=1)
    for position, row, estimate, low, high in zip(y, rows, estimates, lows, highs):
        color = colors[row["backbone_or_modifier"]]
        ax.plot([low, high], [position, position], color=color, linewidth=2.0, zorder=2)
        ax.plot([low, low], [position - 0.10, position + 0.10], color=color, linewidth=1.0)
        ax.plot([high, high], [position - 0.10, position + 0.10], color=color, linewidth=1.0)
        ax.scatter([estimate], [position], s=38, color=color, edgecolor="white", linewidth=0.6, zorder=3)

    ax.set_yticks(y, labels)
    ax.set_xlim(-0.62, 0.92)
    ax.set_ylim(-0.7, 8.7)
    ax.set_xlabel("Effect on 15-state logical-AND execution agreement")
    ax.set_title("Retrospective multi-state reliability effects (66 order-insensitive questions)")
    ax.grid(axis="x", color="#D9D9D9", linewidth=0.6)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.text(0.99, 0.98, "Exact enumeration: all Holm p = 1.000", transform=ax.transAxes, ha="right", va="top", fontsize=8)
    ax.text(
        0.0,
        -0.16,
        "Bars are 95% composition-sensitivity intervals, not population confidence intervals.",
        transform=ax.transAxes,
        fontsize=8,
        color="#444444",
    )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    outputs = {}
    metadata = {"Title": "MA-SQLGrid multi-state reliability effects", "Subject": f"source_sha256={sha256(args.contrasts)}"}
    for suffix in ("pdf", "svg", "png"):
        out = args.out_dir / f"fig04_semantic_reliability.{suffix}"
        save_args = {"dpi": 300, "bbox_inches": "tight"}
        if suffix == "pdf":
            save_args["metadata"] = metadata
        fig.savefig(out, **save_args)
        outputs[suffix] = {"path": str(out.resolve()), "bytes": out.stat().st_size, "sha256": sha256(out)}
    plt.close(fig)

    args.table_dir.mkdir(parents=True, exist_ok=True)
    condition_label = {
        "F00_Full_NoShape": "F00",
        "F01_Full_WithShape": "F01",
        "F10_Compact_NoShape": "F10",
        "F11_Compact_WithShape": "F11",
    }
    cell_lines = [
        "% Generated from the frozen v5 suite_outcomes.csv; do not edit by hand.",
        "\\begin{tabular}{llrrrr}",
        "\\toprule",
        "Backbone & Cell & T0 agreement & T0 rate & 15-state AND & Suite rate \\\\",
        "\\midrule",
    ]
    for backbone in ("qwen", "granite"):
        for condition in condition_label:
            selected = [
                row
                for row in suite_rows
                if row["backbone"] == backbone
                and row["condition"] == condition
                and row["automatic_primary_eligible"].lower() == "true"
            ]
            if len(selected) != 66:
                raise ValueError(f"Expected 66 eligible rows for {backbone}/{condition}")
            snapshot_n = sum(row["snapshot_agreement"].lower() == "true" for row in selected)
            suite_n = sum(row["suite_15state_and"].lower() == "true" for row in selected)
            cell_lines.append(
                f"{backbone_label[backbone]} & {condition_label[condition]} & "
                f"{snapshot_n}/66 & {snapshot_n / 66:.4f} & {suite_n}/66 & {suite_n / 66:.4f} \\\\"
            )
        if backbone == "qwen":
            cell_lines.append("\\midrule")
    cell_lines.extend(["\\bottomrule", "\\end{tabular}", ""])
    cell_table = args.table_dir / "table_semantic_cell_robustness.tex"
    cell_table.write_text("\n".join(cell_lines), encoding="utf-8")

    effect_lines = [
        "% Generated from the frozen v5 clustered_contrasts.csv; do not edit by hand.",
        "\\begin{tabular}{llrrrr}",
        "\\toprule",
        "Backbone/modifier & Effect & Estimate & Sensitivity interval & Raw $p$ & Holm $p$ \\\\",
        "\\midrule",
    ]
    for index, row in enumerate(rows):
        name = backbone_label[row["backbone_or_modifier"]]
        effect = effect_label[row["effect"]]
        estimate = float(row["estimate"])
        low = float(row["composition_sensitivity_low"])
        high = float(row["composition_sensitivity_high"])
        raw = float(exact_rows[index]["exact_two_sided_p_raw"])
        holm = float(exact_rows[index]["exact_two_sided_p_holm"])
        effect_lines.append(
            f"{name} & {effect} & {estimate:+.4f} & [{low:+.4f}, {high:+.4f}] & {raw:.4f} & {holm:.4f} \\\\"
        )
        if index in (2, 5):
            effect_lines.append("\\midrule")
    effect_lines.extend(["\\bottomrule", "\\end{tabular}", ""])
    effect_table = args.table_dir / "table_semantic_effects.tex"
    effect_table.write_text("\n".join(effect_lines), encoding="utf-8")

    lineage = {
        "schema_version": "ma-sqlgrid-manuscript-semantic-figure-v1",
        "contrast_csv": {
            "path": str(args.contrasts.resolve()),
            "bytes": args.contrasts.stat().st_size,
            "sha256": sha256(args.contrasts),
        },
        "exact_test_csv": {
            "path": str(args.exact_tests.resolve()),
            "bytes": args.exact_tests.stat().st_size,
            "sha256": sha256(args.exact_tests),
        },
        "suite_csv": {
            "path": str(args.suite.resolve()),
            "bytes": args.suite.stat().st_size,
            "sha256": sha256(args.suite),
        },
        "generator": {
            "path": str(Path(__file__).resolve()),
            "bytes": Path(__file__).stat().st_size,
            "sha256": sha256(Path(__file__)),
        },
        "outputs": outputs,
        "tables": {
            "cell_robustness": {"path": str(cell_table.resolve()), "bytes": cell_table.stat().st_size, "sha256": sha256(cell_table)},
            "effects": {"path": str(effect_table.resolve()), "bytes": effect_table.stat().st_size, "sha256": sha256(effect_table)},
        },
    }
    args.lineage.write_text(json.dumps(lineage, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(lineage, sort_keys=True))


if __name__ == "__main__":
    main()
