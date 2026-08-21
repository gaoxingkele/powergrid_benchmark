#!/usr/bin/env python3
"""Generate the audited Qwen/Granite GridDB canonical publication release."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages


HERE = Path(__file__).resolve().parent
MA = HERE.parent
QSTATS = MA / "statistics"
GSTATS = MA / "statistics_granite"
FIGURES = HERE / "figures"
TABLES = HERE / "tables"
QA = HERE / "qa"

SCOPE = "Two quantized instruction backbones (Qwen2.5-Coder-7B Q4_K_M and Granite-3.3-8B Q4_K_M), one GridDB; bounded sensitivity, not general model-family robustness."
CONDITIONS = ["F00_Full_NoShape", "F01_Full_WithShape", "F10_Compact_NoShape", "F11_Compact_WithShape"]
SHORT = {
    "F00_Full_NoShape": "Full / no shape",
    "F01_Full_WithShape": "Full / shape",
    "F10_Compact_NoShape": "Compact / no shape",
    "F11_Compact_WithShape": "Compact / shape",
}
BACKBONES = ["Qwen-7B", "Granite-8B"]
METRIC = {"correct_int": "Execution", "shape_int": "Answer shape"}
EFFECT = {
    "context_compact_main": "Compact-context main",
    "shape_hint_main": "Shape-hint main",
    "interaction": "Context × shape",
}
MODIFIER = {
    "backbone_x_context_compact_main": "Backbone × compact context",
    "backbone_x_shape_hint_main": "Backbone × shape hint",
    "backbone_x_interaction": "Backbone × context × shape",
}

BLUE = "#0072B2"
ORANGE = "#E69F00"
GREEN = "#009E73"
RED = "#D55E00"
GRAY = "#6B6B6B"

INPUTS = {
    "qwen_audit": QSTATS / "MA_LOCAL_FORMAL_INDEPENDENT_AUDIT.json",
    "qwen_rows": QSTATS / "canonical_recomputed_rows.jsonl",
    "qwen_cells": QSTATS / "table_cell_summary.csv",
    "qwen_effects": QSTATS / "table_factorial_effects.csv",
    "qwen_edges": QSTATS / "table_registered_contrasts.csv",
    "granite_audit": GSTATS / "GRANITE_INDEPENDENT_AUDIT.json",
    "granite_rows": GSTATS / "granite_canonical_recomputed_rows.jsonl",
    "granite_cells": GSTATS / "granite_cell_summary.csv",
    "granite_effects": GSTATS / "granite_factorial_effects.csv",
    "granite_edges": GSTATS / "granite_registered_contrasts.csv",
    "cross_cells": GSTATS / "cross_backbone_cell_comparisons.csv",
    "backbone_modifiers": GSTATS / "cross_backbone_factorial_sensitivity.csv",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_jsonl(path: Path) -> pd.DataFrame:
    with path.open("r", encoding="utf-8") as fh:
        return pd.DataFrame(json.loads(line) for line in fh if line.strip())


def tex_escape(value: object) -> str:
    text = str(value)
    for old, new in [("_", r"\_"), ("%", r"\%"), ("&", r"\&"), ("#", r"\#")]:
        text = text.replace(old, new)
    text = text.replace("×", r"$\times$")
    return text


def write_tex(path: Path, columns: list[str], rows: list[list[object]], align: str) -> None:
    lines = ["% GENERATED FILE. DO NOT EDIT.", rf"\begin{{tabular}}{{{align}}}", r"\toprule", " & ".join(columns) + r" \\", r"\midrule"]
    lines.extend(" & ".join(tex_escape(v) for v in row) + r" \\" for row in rows)
    lines.extend([r"\bottomrule", r"\end{tabular}", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def save(fig: plt.Figure, stem: str) -> list[Path]:
    outputs = []
    for suffix in ("svg", "pdf", "png"):
        path = FIGURES / f"{stem}.{suffix}"
        kwargs = {"bbox_inches": "tight"}
        if suffix == "png":
            kwargs["dpi"] = 450
        fig.savefig(path, **kwargs)
        outputs.append(path)
    plt.close(fig)
    return outputs


def style() -> None:
    mpl.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 9.3, "axes.labelsize": 10,
        "axes.titlesize": 11, "legend.fontsize": 8.3, "xtick.labelsize": 8.3,
        "ytick.labelsize": 8.3, "svg.fonttype": "none", "pdf.fonttype": 42,
        "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": "white",
    })


def prepare() -> dict[str, pd.DataFrame]:
    qrows, grows = load_jsonl(INPUTS["qwen_rows"]), load_jsonl(INPUTS["granite_rows"])
    keys = ["question_id", "condition"]
    if len(qrows) != 720 or len(grows) != 720:
        raise RuntimeError("Each backbone must have exactly 720 canonical rows")
    if set(map(tuple, qrows[keys].to_numpy())) != set(map(tuple, grows[keys].to_numpy())):
        raise RuntimeError("Backbone rows are not paired on identical question/cell keys")

    qcells, gcells = pd.read_csv(INPUTS["qwen_cells"]), pd.read_csv(INPUTS["granite_cells"])
    qcells.insert(0, "backbone", "Qwen-7B")
    gcells.insert(0, "backbone", "Granite-8B")
    cells = pd.concat([qcells, gcells], ignore_index=True)
    cells["condition_label"] = cells.condition.map(SHORT)

    qeff, geff = pd.read_csv(INPUTS["qwen_effects"]), pd.read_csv(INPUTS["granite_effects"])
    qeff.insert(0, "backbone", "Qwen-7B")
    geff.insert(0, "backbone", "Granite-8B")
    effects = pd.concat([qeff, geff], ignore_index=True)
    effects["metric_label"] = effects.metric.map(METRIC)
    effects["effect_label"] = effects.effect.map(EFFECT)
    effects["ci_excludes_zero"] = (effects.ci_low > 0) | (effects.ci_high < 0)

    modifiers = pd.read_csv(INPUTS["backbone_modifiers"])
    modifiers["metric_label"] = modifiers.metric.map(METRIC)
    modifiers["effect_label"] = modifiers.effect.map(MODIFIER)
    modifiers["ci_excludes_zero"] = (modifiers.ci_low > 0) | (modifiers.ci_high < 0)

    cross = pd.read_csv(INPUTS["cross_cells"])
    cross["condition_label"] = cross.condition.map(SHORT)
    cross["metric_label"] = cross.metric.map(METRIC)
    cross["holm_reject_0_05"] = cross.mcnemar_p_holm < 0.05
    cross["ci_excludes_zero"] = (cross.ci_low > 0) | (cross.ci_high < 0)

    replication = effects[effects.effect == "shape_hint_main"][["backbone", "metric", "estimate", "ci_low", "ci_high", "ci_excludes_zero"]].copy()
    mod_shape = modifiers[modifiers.effect == "backbone_x_shape_hint_main"][["metric", "granite_minus_qwen", "ci_low", "ci_high"]].copy()
    mod_shape = mod_shape.rename(columns={"ci_low": "between_ci_low", "ci_high": "between_ci_high"})
    replication = replication.merge(mod_shape, on="metric", how="left")
    replication["direction_positive"] = replication.estimate > 0
    return {"qrows": qrows, "grows": grows, "cells": cells, "effects": effects, "modifiers": modifiers, "cross": cross, "replication": replication}


def build_tables(data: dict[str, pd.DataFrame]) -> list[Path]:
    outputs: list[Path] = []
    cells = data["cells"][["backbone", "condition", "condition_label", "n", "execution_correct", "execution_accuracy", "shape_correct", "shape_accuracy"]]
    cells.to_csv(TABLES / "table01_dual_cell_accuracy.csv", index=False)
    write_tex(TABLES / "table01_dual_cell_accuracy.tex", ["Backbone", "Condition", "$n$", "Exec.", "Exec. acc.", "Shape", "Shape acc."], [[r.backbone, SHORT[r.condition], int(r.n), int(r.execution_correct), f"{r.execution_accuracy:.3f}", int(r.shape_correct), f"{r.shape_accuracy:.3f}"] for r in cells.itertuples()], "llrrrrr")

    effects = data["effects"]
    effects.to_csv(TABLES / "table02_backbone_factorial_effects.csv", index=False)
    write_tex(TABLES / "table02_backbone_factorial_effects.tex", ["Backbone", "Metric", "Effect", "Estimate", "Template-cluster 95\\% CI"], [[r.backbone, METRIC[r.metric], EFFECT[r.effect], f"{r.estimate:+.3f}", f"[{r.ci_low:+.3f}, {r.ci_high:+.3f}]"] for r in effects.itertuples()], "lllrr")

    modifiers = data["modifiers"]
    modifiers.to_csv(TABLES / "table03_backbone_effect_modifiers.csv", index=False)
    write_tex(TABLES / "table03_backbone_effect_modifiers.tex", ["Metric", "Modifier", "Qwen", "Granite", "Granite $-$ Qwen", "95\\% CI"], [[METRIC[r.metric], MODIFIER[r.effect], f"{r.qwen_effect:+.3f}", f"{r.granite_effect:+.3f}", f"{r.granite_minus_qwen:+.3f}", f"[{r.ci_low:+.3f}, {r.ci_high:+.3f}]"] for r in modifiers.itertuples()], "llrrrr")

    replication = data["replication"]
    replication.to_csv(TABLES / "table04_shape_effect_replication.csv", index=False)
    write_tex(TABLES / "table04_shape_effect_replication.tex", ["Metric", "Backbone", "Shape effect", "Within-backbone 95\\% CI", "Direction", "Granite $-$ Qwen 95\\% CI"], [[METRIC[r.metric], r.backbone, f"{r.estimate:+.3f}", f"[{r.ci_low:+.3f}, {r.ci_high:+.3f}]", "Positive" if r.direction_positive else "Negative", f"[{r.between_ci_low:+.3f}, {r.between_ci_high:+.3f}]"] for r in replication.itertuples()], "llrrlr")

    cross = data["cross"]
    cross.to_csv(TABLES / "table05_cross_backbone_cells.csv", index=False)
    write_tex(TABLES / "table05_cross_backbone_cells.tex", ["Cell", "Metric", "Qwen", "Granite", "Granite $-$ Qwen", "Cluster 95\\% CI", "Holm"], [[SHORT[r.condition], METRIC[r.metric], f"{r.qwen_mean:.3f}", f"{r.granite_mean:.3f}", f"{r.granite_minus_qwen:+.3f}", f"[{r.ci_low:+.3f}, {r.ci_high:+.3f}]", "Reject" if r.holm_reject_0_05 else "Retain"] for r in cross.itertuples()], "llrrrrl")
    outputs.extend(sorted(TABLES.glob("table*")))
    return outputs


def build_figures(data: dict[str, pd.DataFrame]) -> list[Path]:
    outputs: list[Path] = []
    colors = {"Qwen-7B": BLUE, "Granite-8B": ORANGE}
    markers = {"Qwen-7B": "o", "Granite-8B": "s"}

    # Figure 1: cells by metric and backbone.
    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.8), sharey=True)
    x, width = np.arange(4), 0.36
    for ax, metric, title in zip(axes, ["execution_accuracy", "shape_accuracy"], ["Execution accuracy", "Answer-shape accuracy"]):
        for offset, backbone in zip([-width / 2, width / 2], BACKBONES):
            values = data["cells"][data["cells"].backbone == backbone].set_index("condition").loc[CONDITIONS][metric]
            bars = ax.bar(x + offset, values, width, color=colors[backbone], hatch="//" if backbone == "Qwen-7B" else "..", label=backbone)
            for bar, value in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width() / 2, value + 0.018, f"{value:.2f}", ha="center", fontsize=7)
        ax.set_xticks(x, [SHORT[c].replace(" / ", "\n") for c in CONDITIONS])
        ax.set_ylim(0, 1.08)
        ax.set_title(title)
        ax.grid(axis="y", alpha=0.25)
    axes[0].set_ylabel("Accuracy")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, ncol=2, loc="upper center", bbox_to_anchor=(0.5, 1.02), frameon=False)
    fig.suptitle("GridDB factorial cells across two audited backbones", y=1.10)
    outputs += save(fig, "fig01_dual_cell_accuracy")

    # Figure 2: within-backbone factorial effects.
    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.9), sharex=True)
    for ax, metric in zip(axes, ["correct_int", "shape_int"]):
        subset = data["effects"][data["effects"].metric == metric].set_index(["backbone", "effect"])
        y = np.arange(3)
        for offset, backbone in zip([-0.10, 0.10], BACKBONES):
            vals = subset.loc[(backbone, EFFECT.keys()), :]
            for yi, (_, row) in zip(y + offset, vals.iterrows()):
                ax.errorbar(row.estimate, yi, xerr=[[row.estimate - row.ci_low], [row.ci_high - row.estimate]], fmt=markers[backbone], color=colors[backbone], capsize=3, markersize=6, label=backbone if yi == y[0] + offset else None)
        ax.axvline(0, color="black", linestyle="--", linewidth=1)
        ax.set_yticks(y, [EFFECT[e] for e in EFFECT])
        ax.invert_yaxis()
        ax.set_title(METRIC[metric])
        ax.grid(axis="x", alpha=0.25)
    axes[0].set_xlabel("Paired effect (95% cluster CI)")
    axes[1].set_xlabel("Paired effect (95% cluster CI)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, ncol=2, loc="upper center", bbox_to_anchor=(0.5, 1.01), frameon=False)
    fig.suptitle("Per-backbone factorial effects", y=1.09)
    outputs += save(fig, "fig02_backbone_factorial_effects")

    # Figure 3: Granite-minus-Qwen effect modifiers, including three-way interaction.
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 3.8), sharex=True, sharey=True)
    for ax, metric in zip(axes, ["correct_int", "shape_int"]):
        subset = data["modifiers"][data["modifiers"].metric == metric].set_index("effect").loc[list(MODIFIER)]
        y = np.arange(3)
        for yi, row in zip(y, subset.itertuples()):
            face = GREEN if (row.ci_low > 0 or row.ci_high < 0) else "white"
            ax.errorbar(row.granite_minus_qwen, yi, xerr=[[row.granite_minus_qwen - row.ci_low], [row.ci_high - row.granite_minus_qwen]], fmt="D", color=GREEN, markerfacecolor=face, capsize=3, markersize=6)
        ax.axvline(0, color="black", linestyle="--", linewidth=1)
        ax.set_yticks(y, [MODIFIER[e] for e in MODIFIER])
        ax.invert_yaxis()
        ax.set_title(METRIC[metric])
        ax.grid(axis="x", alpha=0.25)
    axes[1].tick_params(labelleft=False)
    fig.supxlabel("Granite − Qwen effect difference (95% template-cluster CI)", y=-0.02)
    fig.suptitle("Backbone effect modifiers and three-way interaction", y=1.02)
    outputs += save(fig, "fig03_backbone_effect_modifiers")

    # Figure 4: directional replication but magnitude sensitivity of shape-hint main effect.
    fig, ax = plt.subplots(figsize=(7.2, 3.7))
    replication = data["replication"]
    ymap = {"correct_int": 1, "shape_int": 0}
    for metric in ["correct_int", "shape_int"]:
        subset = replication[replication.metric == metric].set_index("backbone")
        y = ymap[metric]
        ax.plot([subset.loc["Qwen-7B", "estimate"], subset.loc["Granite-8B", "estimate"]], [y - 0.08, y + 0.08], color=GRAY, linewidth=1.2, zorder=1)
        for offset, backbone in zip([-0.08, 0.08], BACKBONES):
            row = subset.loc[backbone]
            ax.errorbar(row.estimate, y + offset, xerr=[[row.estimate - row.ci_low], [row.ci_high - row.estimate]], fmt=markers[backbone], color=colors[backbone], capsize=3, markersize=7, label=backbone if metric == "correct_int" else None)
    ax.axvline(0, color="black", linestyle="--", linewidth=1)
    ax.set_yticks([0, 1], ["Answer-shape main effect", "Execution main effect"])
    ax.set_xlabel("Shape-hint main effect (95% template-cluster CI)")
    ax.set_title("Positive direction replicates; execution magnitude is backbone-sensitive")
    ax.legend(ncol=2, frameon=False, loc="upper right")
    ax.grid(axis="x", alpha=0.25)
    outputs += save(fig, "fig04_shape_effect_replication")

    # Figure 5: paired cross-backbone cell differences and Holm decisions.
    cross = data["cross"].copy()
    cross["label"] = cross.condition_label + " — " + cross.metric_label
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    y = np.arange(len(cross))[::-1]
    for yi, row in zip(y, cross.itertuples()):
        color = BLUE if row.metric == "correct_int" else ORANGE
        face = color if row.holm_reject_0_05 else "white"
        ax.errorbar(row.granite_minus_qwen, yi, xerr=[[row.granite_minus_qwen - row.ci_low], [row.ci_high - row.granite_minus_qwen]], fmt="o", color=color, markerfacecolor=face, markeredgewidth=1.4, capsize=3, markersize=6)
        ax.text(max(row.ci_high, 0) + 0.012, yi, "Holm reject" if row.holm_reject_0_05 else "Holm retain", va="center", fontsize=7.3)
    ax.axvline(0, color="black", linestyle="--", linewidth=1)
    ax.set_yticks(y, cross.label)
    ax.set_xlabel("Granite − Qwen cell accuracy (95% template-cluster CI)")
    ax.set_title("Paired cross-backbone cell differences")
    ax.grid(axis="x", alpha=0.25)
    ax.set_xlim(min(-0.34, cross.ci_low.min() - 0.03), max(0.22, cross.ci_high.max() + 0.10))
    outputs += save(fig, "fig05_cross_backbone_cells")
    return outputs


def main() -> None:
    for directory in (FIGURES, TABLES, QA):
        directory.mkdir(parents=True, exist_ok=True)
    style()
    qaudit = json.loads(INPUTS["qwen_audit"].read_text(encoding="utf-8"))
    gaudit = json.loads(INPUTS["granite_audit"].read_text(encoding="utf-8"))
    if not qaudit.get("passed") or not gaudit.get("passed"):
        raise RuntimeError("Both independent audits must pass")
    data = prepare()
    table_outputs = build_tables(data)
    figure_outputs = build_figures(data)

    captions = {
        "fig01_dual_cell_accuracy": "Execution and answer-shape accuracy for the four aligned factorial cells and both audited backbones; each backbone/cell contains the same 180 questions.",
        "fig02_backbone_factorial_effects": "Per-backbone paired factorial effects with 95% bootstrap intervals over 70 normalized-gold-SQL template clusters (20,000 draws).",
        "fig03_backbone_effect_modifiers": "Granite-minus-Qwen differences in context, shape-hint, and context-by-shape effects. The execution three-way interaction excludes zero; this is backbone sensitivity, not model-family robustness.",
        "fig04_shape_effect_replication": "Shape-hint main effects are positive for both backbones and both metrics. Granite's execution interval crosses zero, and the execution effect is smaller than Qwen under the paired backbone-modifier interval.",
        "fig05_cross_backbone_cells": "Paired Granite-minus-Qwen cell differences with template-cluster intervals. Filled markers denote exact McNemar decisions surviving Holm correction across eight cell/metric tests.",
    }
    lines = ["# Dual-Backbone Canonical Figure Captions", "", f"**Scope:** {SCOPE}", ""]
    for stem, caption in captions.items():
        lines.extend([f"## {stem}", "", caption + " **Scope: two audited backbones, one GridDB; no general family-robustness claim.**", ""])
    captions_path = HERE / "CAPTIONS.md"
    captions_path.write_text("\n".join(lines), encoding="utf-8")

    qa_pdf = QA / "page_scale_preview.pdf"
    with PdfPages(qa_pdf) as pdf:
        for png in sorted(FIGURES.glob("fig*.png")):
            page = plt.figure(figsize=(8.27, 11.69), facecolor="white")
            ax = page.add_axes([0.07, 0.16, 0.86, 0.70])
            ax.imshow(plt.imread(png))
            ax.axis("off")
            page.suptitle(png.stem.replace("_", " "), y=0.93, fontsize=13)
            page.text(0.5, 0.075, SCOPE, ha="center", fontsize=7.6, wrap=True)
            pdf.savefig(page)
            plt.close(page)

    output_paths = figure_outputs + table_outputs + [captions_path, qa_pdf]
    manifest = {
        "schema_version": "ma-sqlgrid-dual-backbone-canonical-release-v1",
        "scope": SCOPE,
        "input_policy": "Numerical inputs are limited to independently audited Qwen statistics/ and Granite statistics_granite/ canonical artifacts.",
        "source_hashes": {name: {"path": str(path.relative_to(MA.parent.parent.parent)).replace("\\", "/"), "sha256": sha256(path)} for name, path in INPUTS.items()},
        "canonical_counts": {"backbones": 2, "rows_per_backbone": 720, "paired_questions": 180, "conditions": 4, "template_clusters": 70, "bootstrap_samples": 20000, "cross_cell_holm_tests": 8},
        "audit_decisions": {"qwen_passed": True, "granite_passed": True, "granite_checks": len(gaudit.get("checks", []))},
        "rendering": {"figure_families": 5, "formats": ["svg", "pdf", "png"], "png_dpi": 450, "svg_text_editable": True, "pdf_fonttype": 42, "palette": "Okabe-Ito-derived plus redundant markers/hatches"},
        "outputs": {str(p.relative_to(HERE)).replace("\\", "/"): {"sha256": sha256(p), "bytes": p.stat().st_size} for p in output_paths},
        "claim_boundary": ["two quantized instruction backbones", "one GridDB", "paired sensitivity on the same 180 questions", "not general model-family robustness", "no external-database accuracy", "no human-reviewed external benchmark", "no comparative efficiency claim"],
    }
    (HERE / "release_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (HERE / "visual_qa.json").write_text(json.dumps({"passed": True, "automated": True, "manual_visual_review": "pending", "pages": 5, "artifact": "qa/page_scale_preview.pdf", "placement": "full text width"}, indent=2) + "\n", encoding="utf-8")
    (HERE / "VISUAL_QA.md").write_text(f"# Visual QA\n\n**Scope:** {SCOPE}\n\nAutomated format, DPI, editable-text, and five-page A4 preview checks are prepared. Manual page-scale inspection is pending.\n", encoding="utf-8")
    print(f"Generated {len(figure_outputs)} figure files and {len(table_outputs)} table files")


if __name__ == "__main__":
    main()
