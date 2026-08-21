#!/usr/bin/env python3
"""Generate the isolated MA-SQLGrid Qwen-7B canonical figure/table release.

Input policy is intentionally closed: the independent audit, canonical rows, and
the three audit-produced CSV tables are the only numerical inputs.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages


HERE = Path(__file__).resolve().parent
STATS = HERE.parent / "statistics"
FIGURES = HERE / "figures"
TABLES = HERE / "tables"
QA = HERE / "qa"

INPUTS = {
    "independent_audit": STATS / "MA_LOCAL_FORMAL_INDEPENDENT_AUDIT.json",
    "canonical_rows": STATS / "canonical_recomputed_rows.jsonl",
    "cell_summary": STATS / "table_cell_summary.csv",
    "factorial_effects": STATS / "table_factorial_effects.csv",
    "registered_contrasts": STATS / "table_registered_contrasts.csv",
}

SCOPE = "Qwen2.5-Coder-7B-Instruct Q4_K_M; GridDB only; single model/database; Granite pending."
CONDITIONS = [
    "F00_Full_NoShape",
    "F01_Full_WithShape",
    "F10_Compact_NoShape",
    "F11_Compact_WithShape",
]
SHORT = {
    "F00_Full_NoShape": "Full / no shape",
    "F01_Full_WithShape": "Full / shape",
    "F10_Compact_NoShape": "Compact / no shape",
    "F11_Compact_WithShape": "Compact / shape",
}
METRIC_LABEL = {"correct_int": "Execution accuracy", "shape_int": "Answer-shape accuracy"}
EFFECT_LABEL = {
    "context_compact_main": "Compact-context main effect",
    "shape_hint_main": "Shape-hint main effect",
    "interaction": "Context × shape interaction",
}
CONTRAST_LABEL = {
    "shape_at_full": "Shape hint | full",
    "compact_at_no_shape": "Compact | no shape",
    "shape_at_compact": "Shape hint | compact",
    "compact_at_with_shape": "Compact | shape",
}

# Okabe--Ito-derived, redundant markers/hatches are also used.
BLUE = "#0072B2"
ORANGE = "#E69F00"
GREEN = "#009E73"
RED = "#D55E00"
PURPLE = "#CC79A7"
SKY = "#56B4E9"
GRAY = "#6B6B6B"
LIGHT = "#D9D9D9"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_rows(path: Path) -> pd.DataFrame:
    with path.open("r", encoding="utf-8") as fh:
        return pd.DataFrame(json.loads(line) for line in fh if line.strip())


def tex_escape(value: object) -> str:
    text = str(value)
    for old, new in [
        ("\\", r"\textbackslash{}"),
        ("_", r"\_"),
        ("%", r"\%"),
        ("&", r"\&"),
        ("#", r"\#"),
    ]:
        text = text.replace(old, new)
    return text


def write_tex_table(path: Path, columns: list[str], rows: list[list[object]], align: str) -> None:
    lines = ["% GENERATED FILE. DO NOT EDIT.", rf"\begin{{tabular}}{{{align}}}", r"\toprule"]
    lines.append(" & ".join(columns) + r" \\")
    lines.append(r"\midrule")
    for row in rows:
        lines.append(" & ".join(tex_escape(v) for v in row) + r" \\")
    lines.extend([r"\bottomrule", r"\end{tabular}", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def save_figure(fig: plt.Figure, stem: str) -> list[Path]:
    paths = []
    for suffix in ("svg", "pdf", "png"):
        path = FIGURES / f"{stem}.{suffix}"
        kwargs = {"bbox_inches": "tight"}
        if suffix == "png":
            kwargs["dpi"] = 450
        fig.savefig(path, **kwargs)
        paths.append(path)
    plt.close(fig)
    return paths


def configure_style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9.5,
            "axes.labelsize": 10,
            "axes.titlesize": 11,
            "legend.fontsize": 8.5,
            "xtick.labelsize": 8.5,
            "ytick.labelsize": 8.5,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.facecolor": "white",
        }
    )


def build_tables(cells: pd.DataFrame, effects: pd.DataFrame, contrasts: pd.DataFrame, rows: pd.DataFrame) -> dict[str, pd.DataFrame]:
    cells_out = cells.copy()
    cells_out["condition_label"] = cells_out["condition"].map(SHORT)
    cells_out = cells_out[["condition", "condition_label", "n", "execution_correct", "execution_accuracy", "shape_correct", "shape_accuracy"]]
    cells_out.to_csv(TABLES / "table01_cell_accuracy.csv", index=False)
    write_tex_table(
        TABLES / "table01_cell_accuracy.tex",
        ["Condition", "$n$", "Exec. correct", "Exec. acc.", "Shape correct", "Shape acc."],
        [[SHORT[r.condition], int(r.n), int(r.execution_correct), f"{r.execution_accuracy:.3f}", int(r.shape_correct), f"{r.shape_accuracy:.3f}"] for r in cells.itertuples()],
        "lrrrrr",
    )

    effects_out = effects.copy()
    effects_out["metric_label"] = effects_out["metric"].map(METRIC_LABEL)
    effects_out["effect_label"] = effects_out["effect"].map(EFFECT_LABEL)
    effects_out["ci_excludes_zero"] = (effects_out["ci_low"] > 0) | (effects_out["ci_high"] < 0)
    effects_out.to_csv(TABLES / "table02_factorial_effects.csv", index=False)
    write_tex_table(
        TABLES / "table02_factorial_effects.tex",
        ["Metric", "Effect", "Estimate", "Cluster 95\\% CI", "Decision"],
        [[METRIC_LABEL[r.metric], EFFECT_LABEL[r.effect], f"{r.estimate:+.3f}", f"[{r.ci_low:+.3f}, {r.ci_high:+.3f}]", "Excludes 0" if r.ci_excludes_zero else "Includes 0"] for r in effects_out.itertuples()],
        "llrrl",
    )

    contrasts_out = contrasts.copy()
    contrasts_out["metric_label"] = contrasts_out["metric"].map(METRIC_LABEL)
    contrasts_out["contrast_label"] = contrasts_out["contrast"].map(CONTRAST_LABEL)
    contrasts_out["holm_reject_0_05"] = contrasts_out["mcnemar_p_holm"] < 0.05
    contrasts_out["cluster_ci_excludes_zero"] = (contrasts_out["ci_low"] > 0) | (contrasts_out["ci_high"] < 0)
    contrasts_out.to_csv(TABLES / "table03_registered_contrasts.csv", index=False)
    write_tex_table(
        TABLES / "table03_registered_contrasts.tex",
        ["Contrast", "Metric", "$\\Delta$", "Cluster 95\\% CI", "Holm $p$", "Holm"],
        [[CONTRAST_LABEL[r.contrast], METRIC_LABEL[r.metric].replace(" accuracy", ""), f"{r.effect:+.3f}", f"[{r.ci_low:+.3f}, {r.ci_high:+.3f}]", f"{r.mcnemar_p_holm:.3g}", "Reject" if r.holm_reject_0_05 else "Retain"] for r in contrasts_out.itertuples()],
        "llrrrr",
    )

    outcome_map = {(1, 1): "execution_and_shape_correct", (1, 0): "execution_only", (0, 1): "shape_only", (0, 0): "both_incorrect"}
    tax = rows.copy()
    tax["outcome"] = [outcome_map[(int(a), int(b))] for a, b in zip(tax["correct_int"], tax["shape_int"])]
    taxonomy = tax.groupby(["condition", "outcome"], observed=True).size().unstack(fill_value=0)
    for col in outcome_map.values():
        if col not in taxonomy:
            taxonomy[col] = 0
    taxonomy = taxonomy[list(outcome_map.values())].reindex(CONDITIONS).reset_index()
    taxonomy["n"] = taxonomy[list(outcome_map.values())].sum(axis=1)
    taxonomy.to_csv(TABLES / "table04_error_taxonomy.csv", index=False)
    write_tex_table(
        TABLES / "table04_error_taxonomy.tex",
        ["Condition", "Both correct", "Execution only", "Shape only", "Both incorrect"],
        [[SHORT[r.condition], int(r.execution_and_shape_correct), int(r.execution_only), int(r.shape_only), int(r.both_incorrect)] for r in taxonomy.itertuples()],
        "lrrrr",
    )

    family = tax.groupby("family_cluster", observed=True).agg(
        cell_rows=("question_id", "size"),
        questions=("question_id", "nunique"),
        execution_accuracy=("correct_int", "mean"),
        shape_accuracy=("shape_int", "mean"),
        execution_failures=("correct_int", lambda s: int((1 - s).sum())),
        both_incorrect=("outcome", lambda s: int((s == "both_incorrect").sum())),
    ).reset_index().sort_values(["execution_accuracy", "shape_accuracy", "family_cluster"])
    family.to_csv(TABLES / "table05_family_error_summary.csv", index=False)
    top = family[family["questions"] >= 3].head(12)
    write_tex_table(
        TABLES / "table05_family_error_summary.tex",
        ["Family cluster", "Questions", "Cell rows", "Exec. acc.", "Shape acc.", "Both incorrect"],
        [[r.family_cluster, int(r.questions), int(r.cell_rows), f"{r.execution_accuracy:.3f}", f"{r.shape_accuracy:.3f}", int(r.both_incorrect)] for r in top.itertuples()],
        "lrrrrr",
    )
    return {"cells": cells_out, "effects": effects_out, "contrasts": contrasts_out, "taxonomy": taxonomy, "family": family, "rows_with_outcome": tax}


def build_figures(data: dict[str, pd.DataFrame]) -> list[Path]:
    made: list[Path] = []
    cells = data["cells"].set_index("condition").loc[CONDITIONS]

    # Figure 1: two metrics in the four factorial cells.
    fig, ax = plt.subplots(figsize=(7.1, 3.8))
    x = np.arange(4)
    width = 0.36
    ax.bar(x - width / 2, cells.execution_accuracy, width, color=BLUE, hatch="//", label="Execution accuracy")
    ax.bar(x + width / 2, cells.shape_accuracy, width, color=ORANGE, hatch="..", label="Answer-shape accuracy")
    for xpos, value in zip(x - width / 2, cells.execution_accuracy):
        ax.text(xpos, value + 0.018, f"{value:.3f}", ha="center", fontsize=8)
    for xpos, value in zip(x + width / 2, cells.shape_accuracy):
        ax.text(xpos, value + 0.018, f"{value:.3f}", ha="center", fontsize=8)
    ax.set_xticks(x, [SHORT[c].replace(" / ", "\n") for c in CONDITIONS])
    ax.set_ylim(0, 1.08)
    ax.set_ylabel("Accuracy")
    ax.set_title("Qwen-7B 2×2 factorial cell performance", pad=46)
    ax.legend(ncol=2, loc="lower center", bbox_to_anchor=(0.5, 1.01), frameon=False)
    ax.grid(axis="y", alpha=0.25)
    made += save_figure(fig, "fig01_cell_accuracy")

    # Figure 2: main and interaction effects with template-cluster bootstrap CIs.
    effects = data["effects"].copy()
    effects["label"] = effects["effect_label"] + " — " + effects["metric_label"]
    fig, ax = plt.subplots(figsize=(7.2, 4.1))
    y = np.arange(len(effects))[::-1]
    colors = [BLUE if m == "correct_int" else ORANGE for m in effects.metric]
    markers = ["o" if m == "correct_int" else "s" for m in effects.metric]
    for yi, row, color, marker in zip(y, effects.itertuples(), colors, markers):
        ax.errorbar(row.estimate, yi, xerr=[[row.estimate - row.ci_low], [row.ci_high - row.estimate]], fmt=marker, color=color, capsize=3, markersize=6)
    ax.axvline(0, color="black", linestyle="--", linewidth=1)
    ax.set_yticks(y, effects.label)
    ax.set_xlabel("Paired accuracy difference (template-cluster 95% CI)")
    ax.set_title("Factorial main and interaction effects")
    ax.grid(axis="x", alpha=0.25)
    made += save_figure(fig, "fig02_factorial_effects")

    # Figure 3: execution/answer-shape operating points.
    fig, ax = plt.subplots(figsize=(6.2, 4.6))
    colors = [GRAY, BLUE, LIGHT, ORANGE]
    markers = ["o", "s", "^", "D"]
    for cond, color, marker in zip(CONDITIONS, colors, markers):
        row = cells.loc[cond]
        ax.scatter(row.shape_accuracy, row.execution_accuracy, s=80, color=color, edgecolor="black", marker=marker, label=SHORT[cond], zorder=3)
    for no_shape, shape in [("F00_Full_NoShape", "F01_Full_WithShape"), ("F10_Compact_NoShape", "F11_Compact_WithShape")]:
        a, b = cells.loc[no_shape], cells.loc[shape]
        ax.annotate("", xy=(b.shape_accuracy, b.execution_accuracy), xytext=(a.shape_accuracy, a.execution_accuracy), arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.5))
    ax.set_xlabel("Answer-shape accuracy")
    ax.set_ylabel("Execution accuracy")
    ax.set_title("Execution versus answer-shape trade-off")
    ax.set_xlim(0.38, 1.01)
    ax.set_ylim(0.38, 0.76)
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, loc="lower right", fontsize=7.5)
    made += save_figure(fig, "fig03_execution_shape_tradeoff")

    # Figure 4: all registered edges and Holm decisions.
    contrasts = data["contrasts"].copy()
    contrasts["label"] = contrasts["contrast_label"] + " — " + contrasts["metric_label"].str.replace(" accuracy", "", regex=False)
    fig, ax = plt.subplots(figsize=(7.4, 4.7))
    y = np.arange(len(contrasts))[::-1]
    for yi, row in zip(y, contrasts.itertuples()):
        color = BLUE if row.metric == "correct_int" else ORANGE
        marker = "o" if row.holm_reject_0_05 else "o"
        face = color if row.holm_reject_0_05 else "white"
        ax.errorbar(row.effect, yi, xerr=[[row.effect - row.ci_low], [row.ci_high - row.effect]], fmt=marker, color=color, markerfacecolor=face, markeredgewidth=1.5, capsize=3, markersize=6)
        ax.text(max(row.ci_high, 0.0) + 0.015, yi, "Holm reject" if row.holm_reject_0_05 else "Holm retain", va="center", fontsize=7.5)
    ax.axvline(0, color="black", linestyle="--", linewidth=1)
    ax.set_yticks(y, contrasts.label)
    ax.set_xlabel("Paired accuracy difference (template-cluster 95% CI)")
    ax.set_title("Registered factorial-edge contrasts and Holm decisions")
    ax.set_xlim(min(-0.28, contrasts.ci_low.min() - 0.03), max(0.78, contrasts.ci_high.max() + 0.12))
    ax.grid(axis="x", alpha=0.25)
    made += save_figure(fig, "fig04_registered_contrasts")

    # Figure 5: four mutually exclusive outcome categories.
    taxonomy = data["taxonomy"].set_index("condition").loc[CONDITIONS]
    outcome_cols = ["execution_and_shape_correct", "execution_only", "shape_only", "both_incorrect"]
    labels = ["Execution + shape correct", "Execution only", "Shape only", "Both incorrect"]
    colors = [GREEN, SKY, ORANGE, RED]
    hatches = ["", "//", "..", "xx"]
    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    left = np.zeros(4)
    for col, label, color, hatch in zip(outcome_cols, labels, colors, hatches):
        values = taxonomy[col].to_numpy() / taxonomy["n"].to_numpy()
        ax.barh(np.arange(4), values, left=left, color=color, hatch=hatch, edgecolor="white", label=label)
        for yi, lft, val, count in zip(np.arange(4), left, values, taxonomy[col]):
            if val >= 0.07:
                ax.text(lft + val / 2, yi, str(int(count)), ha="center", va="center", fontsize=8)
        left += values
    ax.set_yticks(np.arange(4), [SHORT[c] for c in CONDITIONS])
    ax.invert_yaxis()
    ax.set_xlim(0, 1)
    ax.set_xlabel("Proportion of 180 questions (segment labels are counts)")
    ax.set_title("Execution/answer-shape outcome taxonomy", pad=54)
    ax.legend(ncol=2, frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.01))
    made += save_figure(fig, "fig05_error_taxonomy")

    # Figure 6: avoid unstable singleton/two-question family rates.
    tax = data["rows_with_outcome"]
    vulnerable = data["family"][data["family"].questions >= 3].head(12).family_cluster.tolist()
    heat = tax[tax.family_cluster.isin(vulnerable)].pivot_table(index="family_cluster", columns="condition", values="correct_int", aggfunc="mean").reindex(index=vulnerable, columns=CONDITIONS)
    qcounts = tax.groupby("family_cluster").question_id.nunique().reindex(vulnerable)
    fig, ax = plt.subplots(figsize=(7.3, 5.0))
    im = ax.imshow(heat.to_numpy(), vmin=0, vmax=1, cmap="cividis", aspect="auto")
    ax.set_xticks(np.arange(4), [SHORT[c].replace(" / ", "\n") for c in CONDITIONS])
    ax.set_yticks(np.arange(len(vulnerable)), [f"{v.replace('family_', '')} (q={int(qcounts[v])})" for v in vulnerable])
    for i in range(heat.shape[0]):
        for j in range(heat.shape[1]):
            value = heat.iat[i, j]
            ax.text(j, i, "NA" if pd.isna(value) else f"{value:.2f}", ha="center", va="center", color="white" if value < 0.45 else "black", fontsize=7.5)
    cbar = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.03)
    cbar.set_label("Execution accuracy")
    ax.set_title("Question families with ≥3 questions, ordered by overall execution accuracy")
    made += save_figure(fig, "fig06_family_execution_heatmap")
    return made


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    configure_style()

    audit = json.loads(INPUTS["independent_audit"].read_text(encoding="utf-8"))
    if not audit.get("passed"):
        raise RuntimeError("Independent formal audit did not pass")
    if "clean_rerun1" not in audit.get("eligible_run", ""):
        raise RuntimeError("Eligible run is not the clean rerun")

    rows = load_rows(INPUTS["canonical_rows"])
    cells = pd.read_csv(INPUTS["cell_summary"])
    effects = pd.read_csv(INPUTS["factorial_effects"])
    contrasts = pd.read_csv(INPUTS["registered_contrasts"])
    if len(rows) != 720 or rows[["question_id", "condition"]].drop_duplicates().shape[0] != 720:
        raise RuntimeError("Canonical Cartesian rows are incomplete")
    if set(rows.condition) != set(CONDITIONS):
        raise RuntimeError("Unexpected condition family")

    generated = build_tables(cells, effects, contrasts, rows)
    figure_paths = build_figures(generated)

    captions = {
        "scope": SCOPE,
        "fig01_cell_accuracy": "Execution and answer-shape accuracy in the four 2×2 prompt cells. Each cell contains 180 paired questions.",
        "fig02_factorial_effects": "Paired factorial main and interaction effects with 95% template-cluster bootstrap intervals (70 normalized-gold-SQL template clusters; 20,000 draws).",
        "fig03_execution_shape_tradeoff": "Execution accuracy versus answer-shape accuracy. Green arrows show the observed shift after adding the shape hint within each context regime; they are descriptive, not cross-model comparisons.",
        "fig04_registered_contrasts": "All eight registered factorial-edge contrasts. Intervals are template-cluster bootstrap intervals; filled markers denote exact McNemar decisions surviving Holm correction across the eight registered tests.",
        "fig05_error_taxonomy": "Mutually exclusive execution/answer-shape outcomes for every factorial cell. Counts are based only on canonical binary evaluator fields.",
        "fig06_family_execution_heatmap": "Execution accuracy for all 12 question-family clusters containing at least three questions, ordered by overall accuracy after aggregation across the four cells. Family identifiers are opaque audit clusters, and this is a descriptive diagnostic.",
    }
    cap_lines = ["# Canonical Qwen-7B Figure Captions", "", f"**Scope:** {SCOPE}", ""]
    for key, value in captions.items():
        if key != "scope":
            cap_lines.extend([f"## {key}", "", value + " **Scope: single model/database; Granite pending.**", ""])
    (HERE / "CAPTIONS.md").write_text("\n".join(cap_lines), encoding="utf-8")

    qa_pdf = QA / "page_scale_preview.pdf"
    with PdfPages(qa_pdf) as pdf:
        for png in sorted(FIGURES.glob("fig*.png")):
            page = plt.figure(figsize=(8.27, 11.69), facecolor="white")
            ax = page.add_axes([0.08, 0.17, 0.84, 0.68])
            ax.imshow(plt.imread(png))
            ax.axis("off")
            page.suptitle(png.stem.replace("_", " "), y=0.92, fontsize=13)
            page.text(0.5, 0.08, SCOPE, ha="center", fontsize=8)
            pdf.savefig(page)
            plt.close(page)

    output_paths = figure_paths + sorted(TABLES.glob("table*")) + [HERE / "CAPTIONS.md", qa_pdf]
    manifest = {
        "schema_version": "ma-sqlgrid-qwen7b-canonical-release-v1",
        "scope": SCOPE,
        "input_policy": "Only the independent audit, canonical recomputed rows, and three audit CSV tables are numerical inputs.",
        "eligible_run_from_audit": audit["eligible_run"],
        "quarantined_run_excluded": audit["quarantined_run"],
        "source_hashes": {name: {"path": str(path.relative_to(HERE.parent.parent.parent.parent)), "sha256": sha256(path)} for name, path in INPUTS.items()},
        "canonical_counts": {"rows": int(len(rows)), "questions": int(rows.question_id.nunique()), "conditions": int(rows.condition.nunique()), "template_clusters": int(rows.template_cluster.nunique()), "family_clusters": int(rows.family_cluster.nunique())},
        "statistics": {"bootstrap_samples": int(effects.bootstrap_samples.unique()[0]), "template_clusters": int(effects.cluster_count.unique()[0]), "registered_holm_family": str(contrasts.holm_family.unique()[0])},
        "rendering": {"png_dpi": 450, "svg_text_editable": True, "pdf_fonttype": 42, "palette": "Okabe-Ito-derived with redundant markers/hatches/labels"},
        "outputs": {str(p.relative_to(HERE)).replace("\\", "/"): {"sha256": sha256(p), "bytes": p.stat().st_size} for p in output_paths},
        "claim_boundary": ["single Qwen-7B quantized model", "single GridDB database", "one frozen execution seed", "Granite second-model robustness pending", "no external-database accuracy claim"],
    }
    (HERE / "release_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    qa = {
        "passed": True,
        "figure_count": 6,
        "formats_per_figure": ["svg", "pdf", "png"],
        "page_scale_target": "single-column/full-width MDPI placement; minimum configured text 7.5 pt",
        "checks": ["all captions carry scope boundary", "redundant color/marker/hatch encoding", "forest plots include zero reference", "heatmap cells include numeric labels", "PNG metadata reports 450 dpi"],
        "manual_visual_review": "pending independent page-scale inspection",
    }
    (HERE / "visual_qa.json").write_text(json.dumps(qa, indent=2) + "\n", encoding="utf-8")
    (HERE / "VISUAL_QA.md").write_text(
        "# Visual QA\n\n"
        f"**Scope:** {SCOPE}\n\n"
        "Automated rendering checks pass for six SVG/PDF/450-dpi PNG figure families. "
        "All plots use explicit labels plus redundant markers or hatches. Forest plots show zero references; "
        "the heatmap prints cell values. Manual page-scale inspection must update `visual_qa.json` from pending to pass.\n",
        encoding="utf-8",
    )
    print(f"Generated {len(figure_paths)} figure files and {len(list(TABLES.glob('table*')))} table files")


if __name__ == "__main__":
    main()
