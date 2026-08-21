#!/usr/bin/env python3
"""Build canonical W6 C2GES tables and journal-ready vector/raster figures."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


SEEDS = (2026, 2027, 2028, 2029, 2030)
K_VALUES = (1, 3, 5, 10)
PROTOCOL_DIRS = {"oracle-label": "oracle", "predicted-label": "predicted", "label-blind": "label_blind"}
LABELS = {"oracle-label": "Oracle-label", "predicted-label": "Predicted-label", "label-blind": "Label-blind", "bm25": "BM25"}
STYLES = {
    "oracle-label": {"color": "#0072B2", "marker": "o", "linestyle": "-"},
    "predicted-label": {"color": "#D55E00", "marker": "s", "linestyle": "--"},
    "label-blind": {"color": "#009E73", "marker": "^", "linestyle": ":"},
    "bm25": {"color": "#222222", "marker": "D", "linestyle": "-."},
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_run_dir(w3_root: Path, w4_root: Path, seed: int, protocol: str) -> Path:
    return w3_root / PROTOCOL_DIRS[protocol] if seed == 2026 else w4_root / f"seed_{seed}" / PROTOCOL_DIRS[protocol]


def save_figure(fig, figures_dir: Path, stem: str) -> list[Path]:
    paths = []
    for suffix, kwargs in (("svg", {}), ("pdf", {}), ("png", {"dpi": 450})):
        path = figures_dir / f"{stem}.{suffix}"
        fig.savefig(path, bbox_inches="tight", facecolor="white", **kwargs)
        paths.append(path)
    plt.close(fig)
    return paths


def write_csv(path: Path, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"refusing empty canonical table {path.name}")
    fields = fieldnames or list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def pareto_indices(x: list[float], y: list[float]) -> list[int]:
    """Return non-dominated points for lower x and higher y."""
    out = []
    for i, (xi, yi) in enumerate(zip(x, y)):
        dominated = any((xj <= xi and yj >= yi) and (xj < xi or yj > yi) for j, (xj, yj) in enumerate(zip(x, y)) if j != i)
        if not dominated:
            out.append(i)
    return out


def markdown_table(rows: list[dict], columns: list[tuple[str, str]]) -> list[str]:
    lines = ["| " + " | ".join(label for _, label in columns) + " |", "|" + "|".join("---" for _ in columns) + "|"]
    for row in rows:
        values = []
        for key, _ in columns:
            value = row[key]
            values.append(f"{value:.4f}" if isinstance(value, float) else str(value))
        lines.append("| " + " | ".join(values) + " |")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--w3-root", type=Path, required=True)
    parser.add_argument("--w4-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true", help="Rewrite the known canonical files in an existing canonical directory.")
    args = parser.parse_args()
    if args.out.exists() and any(args.out.iterdir()) and not args.overwrite:
        parser.error(f"refusing to overwrite non-empty canonical output: {args.out}")
    tables_dir = args.out / "tables"
    figures_dir = args.out / "figures"
    data_dir = args.out / "data"
    for directory in (tables_dir, figures_dir, data_dir):
        directory.mkdir(parents=True, exist_ok=True)

    aggregate_path = args.w4_root / "five_seed_aggregate.json"
    effects_path = args.w4_root / "five_seed_effects.csv"
    audit_path = args.w4_root / "failure_and_evidence_audit.json"
    freeze_path = args.w4_root / "W4_FREEZE_MANIFEST.json"
    aggregate = json.loads(aggregate_path.read_text(encoding="utf-8"))
    evidence_audit = json.loads(audit_path.read_text(encoding="utf-8"))
    if not evidence_audit.get("passed") or evidence_audit.get("failure_count") != 0:
        raise RuntimeError("canonical generation requires a passing zero-failure W4 audit")
    if aggregate.get("seeds") != list(SEEDS) or aggregate.get("k_values") != list(K_VALUES):
        raise RuntimeError("unexpected canonical seed/K set")
    decisions = aggregate["claim_decisions"]
    if decisions["role_conditioning_primary_claim"]["decision"] != "NO-GO":
        raise RuntimeError("canonical caption contract expects the frozen role-effect NO-GO decision")

    input_artifacts = {
        "five_seed_aggregate.json": {"path": str(aggregate_path.resolve()), "sha256": sha256(aggregate_path)},
        "five_seed_effects.csv": {"path": str(effects_path.resolve()), "sha256": sha256(effects_path)},
        "failure_and_evidence_audit.json": {"path": str(audit_path.resolve()), "sha256": sha256(audit_path)},
        "W4_FREEZE_MANIFEST.json": {"path": str(freeze_path.resolve()), "sha256": sha256(freeze_path)},
    }

    # Canonical prediction subset: only full C2GES and fixed BM25 rows used in
    # W6 analyses. The original candidate ranking is retained, never recomputed.
    prediction_index = []
    case_records = defaultdict(lambda: defaultdict(dict))
    canonical_prediction_path = data_dir / "canonical_full_and_bm25_predictions.csv.gz"
    canonical_fields = [
        "seed", "protocol", "mode", "k", "qid", "underlying_document_id", "gold_role", "selector_role",
        "precision", "recall", "f1", "predicted_sentence_ids", "gold_sentence_ids",
    ]
    canonical_rows = 0
    with gzip.open(canonical_prediction_path, "wt", encoding="utf-8", newline="") as compressed:
        writer = csv.DictWriter(compressed, fieldnames=canonical_fields)
        writer.writeheader()
        for seed in SEEDS:
            for protocol in PROTOCOL_DIRS:
                directory = source_run_dir(args.w3_root, args.w4_root, seed, protocol)
                predictions_path = directory / "predictions.jsonl"
                source_rows = 0
                selected_rows = 0
                with predictions_path.open(encoding="utf-8") as handle:
                    for line in handle:
                        source_rows += 1
                        row = json.loads(line)
                        if row["mode"] not in {"full", "bm25"}:
                            continue
                        selected_rows += 1
                        canonical_rows += 1
                        writer.writerow(
                            {
                                "seed": seed,
                                "protocol": protocol,
                                "mode": row["mode"],
                                "k": row["k"],
                                "qid": row["qid"],
                                "underlying_document_id": row["underlying_document_id"],
                                "gold_role": row["gold_role"],
                                "selector_role": row["selector_role"],
                                "precision": row["precision"],
                                "recall": row["recall"],
                                "f1": row["f1"],
                                "predicted_sentence_ids": "|".join(row["predicted_sentence_ids"]),
                                "gold_sentence_ids": "|".join(row["gold_sentence_ids"]),
                            }
                        )
                        if protocol == "predicted-label" and row["k"] == 3:
                            case_records[row["qid"]][seed][row["mode"]] = {
                                "f1": row["f1"],
                                "doc": row["underlying_document_id"],
                                "pred": row["predicted_sentence_ids"],
                                "gold": row["gold_sentence_ids"],
                            }
                if source_rows != 54000 or selected_rows != 12000:
                    raise RuntimeError(f"unexpected prediction rows for {seed}/{protocol}: {source_rows}/{selected_rows}")
                run_files = {}
                for name in ("predictions.jsonl", "summary.json", "run_config.json", "provenance.json", "resource_usage.json"):
                    path = directory / name
                    run_files[name] = {"path": str(path.resolve()), "sha256": sha256(path)}
                prediction_index.append(
                    {
                        "seed": seed,
                        "protocol": protocol,
                        "source": "W3 frozen" if seed == 2026 else "W4",
                        "prediction_rows": source_rows,
                        "canonical_rows": selected_rows,
                        "predictions_sha256": run_files["predictions.jsonl"]["sha256"],
                        "run_files": run_files,
                    }
                )
    if canonical_rows != 180000:
        raise RuntimeError(f"canonical prediction subset has {canonical_rows} rows, expected 180000")
    write_csv(
        data_dir / "canonical_predictions_index.csv",
        [{key: value for key, value in row.items() if key != "run_files"} for row in prediction_index],
    )

    # Canonical tables.
    main_rows = []
    seed_rows = []
    for protocol in PROTOCOL_DIRS:
        for k in K_VALUES:
            metric = aggregate["metric_summary"][protocol][str(k)]
            effect = aggregate["effects"][f"{protocol}_minus_bm25"][str(k)]
            main_rows.append(
                {
                    "protocol": protocol,
                    "k": k,
                    "mean_f1": metric["mean"],
                    "sample_std_f1": metric["sample_std"],
                    "t_ci95_low": metric["t_ci95"][0],
                    "t_ci95_high": metric["t_ci95"][1],
                    "delta_vs_bm25": effect["seed_level"]["mean"],
                    "hier_ci95_low": effect["hierarchical_bootstrap"]["ci95"][0],
                    "hier_ci95_high": effect["hierarchical_bootstrap"]["ci95"][1],
                    "positive_effect_gate": effect["positive_effect_gate"],
                    "oracle_is_conditional_not_end_to_end": protocol == "oracle-label",
                }
            )
            for seed, value, bm25 in zip(SEEDS, metric["values"], effect["seed_level"]["right_values"]):
                seed_rows.append({"seed": seed, "protocol": protocol, "k": k, "f1": value, "bm25_f1": bm25, "delta_vs_bm25": value - bm25})
    bm25_values = {k: aggregate["effects"]["oracle-label_minus_bm25"][str(k)]["seed_level"]["right_values"][0] for k in K_VALUES}
    for k in K_VALUES:
        main_rows.append(
            {
                "protocol": "bm25", "k": k, "mean_f1": bm25_values[k], "sample_std_f1": 0.0,
                "t_ci95_low": bm25_values[k], "t_ci95_high": bm25_values[k], "delta_vs_bm25": 0.0,
                "hier_ci95_low": 0.0, "hier_ci95_high": 0.0, "positive_effect_gate": True,
                "oracle_is_conditional_not_end_to_end": False,
            }
        )
    write_csv(tables_dir / "table_main_results.csv", main_rows)
    write_csv(tables_dir / "table_seed_distribution.csv", seed_rows)

    role_rows = []
    for comparison in ("oracle-label_minus_predicted-label", "oracle-label_minus_label-blind", "predicted-label_minus_label-blind"):
        for k in K_VALUES:
            item = aggregate["effects"][comparison][str(k)]
            role_rows.append(
                {
                    "comparison": comparison,
                    "k": k,
                    "mean_delta": item["seed_level"]["mean"],
                    "seed_std": item["seed_level"]["sample_std"],
                    "seed_t_ci_low": item["seed_level"]["t_ci95"][0],
                    "seed_t_ci_high": item["seed_level"]["t_ci95"][1],
                    "hier_ci_low": item["hierarchical_bootstrap"]["ci95"][0],
                    "hier_ci_high": item["hierarchical_bootstrap"]["ci95"][1],
                    "paired_t_p": item["seed_level"]["paired_t_p_two_sided"],
                    "exact_sign_flip_p": item["seed_level"]["exact_sign_flip_p_two_sided"],
                    "positive_effect_gate": item["positive_effect_gate"],
                }
            )
    write_csv(tables_dir / "table_role_effects.csv", role_rows)

    runtime_rows = []
    failure_rows = []
    for protocol in PROTOCOL_DIRS:
        wall = aggregate["resources"][protocol]["wall_seconds"]
        memory = aggregate["resources"][protocol]["peak_rss_gib"]
        runtime_rows.append(
            {
                "protocol": protocol, "mean_wall_seconds": wall["mean"], "sd_wall_seconds": wall["sample_std"],
                "wall_t_ci_low": wall["t_ci95"][0], "wall_t_ci_high": wall["t_ci95"][1],
                "mean_peak_rss_gib": memory["mean"], "sd_peak_rss_gib": memory["sample_std"],
                "rss_t_ci_low": memory["t_ci95"][0], "rss_t_ci_high": memory["t_ci95"][1],
            }
        )
        for index, seed in enumerate(SEEDS):
            directory = source_run_dir(args.w3_root, args.w4_root, seed, protocol)
            resource = json.loads((directory / "resource_usage.json").read_text(encoding="utf-8"))
            failure_rows.append(
                {
                    "seed": seed, "protocol": protocol, "status": resource["status"],
                    "failure": json.dumps(resource["failure"], ensure_ascii=False),
                    "wall_seconds": resource["wall_seconds"],
                    "peak_rss_gib": resource["resource_sampling"]["peak_tree_rss_gib"],
                    "stdout_sha256": resource["logs"]["stdout_sha256"], "stderr_sha256": resource["logs"]["stderr_sha256"],
                }
            )
    write_csv(tables_dir / "table_runtime_memory.csv", runtime_rows)
    write_csv(tables_dir / "table_failure_audit.csv", failure_rows)

    k_rows = []
    for protocol in (*PROTOCOL_DIRS.keys(), "bm25"):
        row = {"protocol": protocol}
        for k in K_VALUES:
            source = next(item for item in main_rows if item["protocol"] == protocol and item["k"] == k)
            row[f"k{k}_mean_f1"] = source["mean_f1"]
            row[f"k{k}_sd"] = source["sample_std_f1"]
        k_rows.append(row)
    write_csv(tables_dir / "table_k_sensitivity.csv", k_rows)

    case_rows = []
    for qid, seed_map in sorted(case_records.items()):
        if set(seed_map) != set(SEEDS) or any(set(seed_map[seed]) != {"full", "bm25"} for seed in SEEDS):
            raise RuntimeError(f"incomplete canonical K=3 case {qid}")
        deltas = [seed_map[seed]["full"]["f1"] - seed_map[seed]["bm25"]["f1"] for seed in SEEDS]
        wins, losses, ties = sum(v > 0 for v in deltas), sum(v < 0 for v in deltas), sum(v == 0 for v in deltas)
        if wins == len(SEEDS):
            category = "consistent_c2ges_win"
        elif losses == len(SEEDS):
            category = "consistent_bm25_win"
        elif ties == len(SEEDS):
            category = "all_tie"
        else:
            category = "mixed_across_seeds"
        first = seed_map[SEEDS[0]]["full"]
        case_rows.append(
            {
                "qid": qid, "underlying_document_id": first["doc"], "category": category,
                "mean_delta_f1": float(np.mean(deltas)), "wins": wins, "ties": ties, "losses": losses,
                "gold_sentence_ids": "|".join(first["gold"]),
            }
        )
    write_csv(tables_dir / "table_k3_case_stability.csv", case_rows)
    examples = []
    for category in ("consistent_c2ges_win", "consistent_bm25_win", "mixed_across_seeds", "all_tie"):
        candidates = [row for row in case_rows if row["category"] == category]
        candidates.sort(key=lambda row: (-abs(row["mean_delta_f1"]), row["qid"]))
        examples.extend(candidates[:10])
    write_csv(tables_dir / "table_k3_case_examples.csv", examples)

    # Journal figure defaults: editable SVG text, embedded TrueType PDF fonts,
    # colorblind-safe colors plus redundant marker/dash coding for grayscale.
    plt.rcParams.update(
        {
            "font.family": "DejaVu Serif", "font.size": 8.5, "axes.labelsize": 9,
            "axes.titlesize": 9.5, "legend.fontsize": 7.5, "xtick.labelsize": 8,
            "ytick.labelsize": 8, "svg.fonttype": "none", "pdf.fonttype": 42,
            "axes.spines.top": False, "axes.spines.right": False,
        }
    )
    generated_figures = []

    fig, ax = plt.subplots(figsize=(6.8, 4.1))
    for protocol in (*PROTOCOL_DIRS.keys(), "bm25"):
        points = [next(row for row in main_rows if row["protocol"] == protocol and row["k"] == k) for k in K_VALUES]
        style = STYLES[protocol]
        marker_face = "none" if protocol == "oracle-label" else style["color"]
        ax.errorbar(
            K_VALUES, [row["mean_f1"] for row in points], yerr=[row["sample_std_f1"] for row in points],
            label=LABELS[protocol], color=style["color"], marker=style["marker"], linestyle=style["linestyle"],
            markerfacecolor=marker_face, markeredgecolor=style["color"], linewidth=1.5, capsize=3,
        )
    ax.set(xlabel="Evidence budget K", ylabel="Evidence F1", xticks=K_VALUES)
    ax.grid(axis="y", color="#cccccc", linewidth=0.5, alpha=0.7)
    ax.legend(ncol=2, frameon=False)
    generated_figures += save_figure(fig, figures_dir, "fig01_k_sensitivity_f1")

    fig, ax = plt.subplots(figsize=(7.1, 5.2))
    comparisons = ("oracle-label_minus_predicted-label", "oracle-label_minus_label-blind", "predicted-label_minus_label-blind")
    comp_style = {comparisons[0]: STYLES["oracle-label"], comparisons[1]: {**STYLES["label-blind"], "marker": "o"}, comparisons[2]: STYLES["predicted-label"]}
    y_positions, y_labels = [], []
    position = 0
    for comparison in comparisons:
        for k in K_VALUES:
            item = next(row for row in role_rows if row["comparison"] == comparison and row["k"] == k)
            style = comp_style[comparison]
            ax.errorbar(
                item["mean_delta"], position,
                xerr=[[item["mean_delta"] - item["hier_ci_low"]], [item["hier_ci_high"] - item["mean_delta"]]],
                fmt=style["marker"], color=style["color"], markerfacecolor="none" if comparison.startswith("oracle") else style["color"],
                capsize=2.5, markersize=5,
            )
            y_positions.append(position)
            y_labels.append(f"{comparison.replace('-label', '').replace('_minus_', ' - ')}; K={k}")
            position += 1
        position += 0.6
    ax.axvline(0, color="#333333", linewidth=0.9, linestyle="--")
    ax.set_yticks(y_positions, y_labels)
    ax.set_xlabel("Mean evidence-F1 difference (95% hierarchical CI)")
    ax.invert_yaxis()
    ax.grid(axis="x", color="#cccccc", linewidth=0.5, alpha=0.7)
    generated_figures += save_figure(fig, figures_dir, "fig02_role_effect_forest")

    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    x, y, protocols = [], [], []
    for protocol in PROTOCOL_DIRS:
        runtime = next(row for row in runtime_rows if row["protocol"] == protocol)
        metric = next(row for row in main_rows if row["protocol"] == protocol and row["k"] == 3)
        x.append(runtime["mean_wall_seconds"]); y.append(metric["mean_f1"]); protocols.append(protocol)
        style = STYLES[protocol]
        ax.errorbar(
            runtime["mean_wall_seconds"], metric["mean_f1"],
            xerr=runtime["sd_wall_seconds"], yerr=metric["sample_std_f1"],
            fmt=style["marker"], color=style["color"], capsize=3, markersize=7,
            markerfacecolor="none" if protocol == "oracle-label" else style["color"], label=LABELS[protocol],
        )
    ax.set(xlabel="Full training + evaluation wall time (s)", ylabel="K=3 evidence F1")
    ax.grid(color="#cccccc", linewidth=0.5, alpha=0.7)
    ax.legend(frameon=False)
    generated_figures += save_figure(fig, figures_dir, "fig03_compute_accuracy_tradeoff")

    fig, ax = plt.subplots(figsize=(6.8, 4.1))
    for protocol in PROTOCOL_DIRS:
        rows = [row for row in seed_rows if row["protocol"] == protocol and row["k"] == 3]
        style = STYLES[protocol]
        ax.plot(
            [row["seed"] for row in rows], [row["delta_vs_bm25"] for row in rows],
            label=LABELS[protocol], color=style["color"], marker=style["marker"], linestyle=style["linestyle"],
            markerfacecolor="none" if protocol == "oracle-label" else style["color"], linewidth=1.3,
        )
    ax.axhline(0, color="#222222", linewidth=0.8, linestyle="--")
    ax.set(xlabel="Training seed", ylabel="K=3 F1 difference from BM25", xticks=SEEDS)
    ax.grid(axis="y", color="#cccccc", linewidth=0.5, alpha=0.7)
    ax.legend(frameon=False, ncol=3)
    generated_figures += save_figure(fig, figures_dir, "fig04_seed_stability_k3")

    fig, ax = plt.subplots(figsize=(6.6, 3.8))
    categories = ("consistent_c2ges_win", "consistent_bm25_win", "mixed_across_seeds", "all_tie")
    counts = Counter(row["category"] for row in case_rows)
    labels = ("C2GES win (5/5)", "BM25 win (5/5)", "Mixed", "Tie (5/5)")
    colors = ("#0072B2", "#555555", "#E69F00", "#BBBBBB")
    bars = ax.barh(labels, [counts[value] for value in categories], color=colors, edgecolor="#222222", linewidth=0.6)
    ax.bar_label(bars, padding=3, fontsize=8)
    ax.set_xlabel("Number of K=3 test instances")
    ax.invert_yaxis()
    ax.grid(axis="x", color="#cccccc", linewidth=0.5, alpha=0.7)
    generated_figures += save_figure(fig, figures_dir, "fig05_k3_case_stability")

    captions = {
        "fig01_k_sensitivity_f1": "Five-seed evidence F1 across evidence budgets; error bars are +/-1 sample SD over training seeds. Oracle-label (hollow marker) is conditional and not end-to-end. The frozen role-conditioning claim is NO-GO, and K=1 remains below BM25.",
        "fig02_role_effect_forest": "Protocol differences with 95% hierarchical seed/Wikipedia-document bootstrap intervals. Every role comparison at the primary K=3 crosses zero, establishing the role-effect NO-GO boundary. Oracle-label comparisons are conditional rather than end-to-end.",
        "fig03_compute_accuracy_tradeoff": "Measured full-script CPU wall time versus K=3 evidence F1; horizontal and vertical error bars are +/-1 seed SD. This is training-plus-evaluation cost, not per-query latency. Oracle-label is a conditional upper-bound protocol, and the role-effect claim remains NO-GO.",
        "fig04_seed_stability_k3": "Per-seed K=3 difference from the fixed BM25 result. Lines show all five frozen seeds without seed selection. Oracle-label is conditional; the predicted-versus-label-blind role effect is NO-GO under the frozen criterion.",
        "fig05_k3_case_stability": "Deterministic K=3 instance outcomes for predicted-label C2GES versus BM25 across all five seeds. Categories use only gold/predicted sentence IDs and evidence F1; they are not semantic error labels. The aggregate role-effect claim is NO-GO.",
    }
    (args.out / "FIGURE_CAPTIONS.md").write_text(
        "# Canonical Figure Captions\n\n" + "\n\n".join(f"## {key}\n\n{value}" for key, value in captions.items()) + "\n",
        encoding="utf-8",
    )

    table_doc = [
        "# Canonical C2GES Tables",
        "",
        "All values are generated from the frozen five-seed artifacts. Oracle-label is conditional and must not be reported as end-to-end. The primary role-effect and blanket-superiority claims are NO-GO.",
        "",
        "## Main results",
        "",
    ]
    compact_main = [
        {"protocol": row["protocol"], "K": row["k"], "mean_F1": row["mean_f1"], "SD": row["sample_std_f1"], "delta_BM25": row["delta_vs_bm25"], "gate": row["positive_effect_gate"]}
        for row in main_rows
    ]
    table_doc += markdown_table(compact_main, [("protocol", "Protocol"), ("K", "K"), ("mean_F1", "Mean F1"), ("SD", "SD"), ("delta_BM25", "Delta vs BM25"), ("gate", "Positive gate")])
    table_doc += ["", "## Runtime and memory", ""]
    table_doc += markdown_table(runtime_rows, [("protocol", "Protocol"), ("mean_wall_seconds", "Mean wall s"), ("sd_wall_seconds", "Wall SD"), ("mean_peak_rss_gib", "Mean RSS GiB"), ("sd_peak_rss_gib", "RSS SD")])
    (args.out / "CANONICAL_TABLES.md").write_text("\n".join(table_doc) + "\n", encoding="utf-8")

    output_files = [path for path in args.out.rglob("*") if path.is_file() and path.name != "canonical_manifest.json"]
    validation = {
        "passed": True,
        "canonical_prediction_rows": canonical_rows,
        "prediction_source_runs": len(prediction_index),
        "expected_figure_files": 15,
        "actual_figure_files": len(generated_figures),
        "png_dpi": 450,
        "editable_vector_formats": ["svg", "pdf"],
        "tables": {
            "main_results": len(main_rows), "role_effects": len(role_rows), "seed_distribution": len(seed_rows),
            "runtime_memory": len(runtime_rows), "failure_audit": len(failure_rows), "case_stability": len(case_rows),
        },
        "caption_contract": {
            "all_mention_no_go": all("NO-GO" in value for value in captions.values()),
            "oracle_figures_mention_conditional": all("conditional" in captions[key].lower() for key in captions if key != "fig05_k3_case_stability"),
        },
        "w4_evidence_audit_passed": True,
    }
    validation["passed"] = (
        validation["actual_figure_files"] == validation["expected_figure_files"]
        and validation["caption_contract"]["all_mention_no_go"]
        and validation["caption_contract"]["oracle_figures_mention_conditional"]
        and len(failure_rows) == 15
        and all(row["status"] == "success" for row in failure_rows)
    )
    (args.out / "validation.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2), encoding="utf-8")
    if not validation["passed"]:
        raise RuntimeError(f"canonical validation failed: {validation}")

    # Hash all sources and outputs after validation. Manifest deliberately does
    # not self-hash; its hash is reported by the caller after generation.
    input_artifacts["prediction_runs"] = prediction_index
    manifest = {
        "status": "canonical",
        "source_contract": "Frozen W4 aggregate/effects/audit/resources and the indexed W3/W4 prediction JSONL files only.",
        "seeds": list(SEEDS),
        "k_values": list(K_VALUES),
        "claim_decisions": decisions,
        "inputs": input_artifacts,
        "outputs": {
            str(path.relative_to(args.out)).replace("\\", "/"): {"sha256": sha256(path), "bytes": path.stat().st_size}
            for path in sorted(output_files, key=lambda item: item.as_posix())
        },
        "validation": validation,
        "rendering": {
            "png_dpi": 450,
            "svg_text_editable": True,
            "pdf_fonttype": 42,
            "accessibility": "Okabe-Ito-derived palette with redundant marker and line-style encoding for grayscale.",
        },
    }
    manifest_path = args.out / "canonical_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": "canonical", "out": str(args.out), "manifest_sha256": sha256(manifest_path), "validation": validation}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
