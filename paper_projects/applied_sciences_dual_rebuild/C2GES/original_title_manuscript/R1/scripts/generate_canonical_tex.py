#!/usr/bin/env python3
"""Generate every empirical manuscript number from frozen C2GES artifacts."""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve()
ROOT = next(p for p in HERE.parents if (p / "paper_projects").is_dir())
OUT = HERE.parent.parent / "generated"
W6 = ROOT / "paper_projects/2026_c2ges_engineeringletters/workspace/w6_c2_canonical_v2"
W4 = ROOT / "paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed"
DATA = ROOT / "paper_projects/2026_c2ges_engineeringletters/workspace/fever_benchmark_document_grouped/manifest.json"
UPSTREAM = ROOT / "paper_projects/2026_c2ges_engineeringletters/workspace/w3_c2_pilot/full_8000_1500_1500/upstream_labels/metrics.json"
CONVERSION_AUDIT = HERE.parent.parent / "evidence/conversion_audit.json"
METHOD_CONTRACT = HERE.parent.parent / "evidence/method_implementation_contract.json"
GZIP_TRANSITION = HERE.parent.parent / "evidence/canonical_gzip_transition.json"
REBUILD_C2 = HERE.parent.parent.parent
ADDON = REBUILD_C2 / "addon_round3"
EXPLORATORY = REBUILD_C2 / "exploratory_v3"
BGE = REBUILD_C2 / "bge_expansion_20260806"
UPSTREAM_MATRIX = REBUILD_C2 / "upstream_uncertainty_20260806"
UPSTREAM_ANALYSIS = UPSTREAM_MATRIX / "formal_analysis_v1"


def rows(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def f4(value):
    return f"{float(value):.4f}"


def f3(value):
    return f"{float(value):.3f}"


def f2(value):
    return f"{float(value):.2f}"


def signed4(value):
    return f"{float(value):+.4f}"


def ci4(lo, hi):
    return f"[{float(lo):.4f}, {float(hi):.4f}]"


def tex_bool(value):
    return "Met" if str(value).lower() == "true" else "Not met"


def macro(name, value):
    return rf"\newcommand{{\{name}}}{{{value}}}"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    source_paths = {
        "main_results": W6 / "tables/table_main_results.csv",
        "role_effects": W6 / "tables/table_role_effects.csv",
        "runtime_memory": W6 / "tables/table_runtime_memory.csv",
        "failure_audit": W6 / "tables/table_failure_audit.csv",
        "case_stability": W6 / "tables/table_k3_case_stability.csv",
        "canonical_manifest": W6 / "canonical_manifest.json",
        "validation": W6 / "validation.json",
        "dataset_manifest": DATA,
        "upstream_metrics": UPSTREAM,
        "freeze_manifest": W4 / "W4_FREEZE_MANIFEST.json",
        "evidence_audit": W4 / "failure_and_evidence_audit.json",
        "conversion_audit": CONVERSION_AUDIT,
        "method_contract": METHOD_CONTRACT,
        "canonical_gzip_transition": GZIP_TRANSITION,
        "addon_protocol_freeze": ADDON / "ADDON_PROTOCOL_FREEZE.json",
        "addon_results": ADDON / "results.json",
        "addon_manifest": ADDON / "artifact_manifest.json",
        "addon_primary_contrasts": ADDON / "primary_contrasts.csv",
        "addon_primary_table": ADDON / "table_primary.tex",
        "exploratory_protocol_freeze": EXPLORATORY / "PROTOCOL_FREEZE.json",
        "exploratory_manifest": EXPLORATORY / "artifact_manifest.json",
        "exploratory_validation": EXPLORATORY / "validation.json",
        "exploratory_primary_contrasts": EXPLORATORY / "primary_editorial_contrasts.csv",
        "exploratory_primary_figure": EXPLORATORY / "fig_primary_forest.pdf",
        "bge_protocol_freeze": BGE / "PROTOCOL_FREEZE.json",
        "bge_results": BGE / "RESULTS_SUMMARY.json",
        "bge_artifact_manifest": BGE / "artifact_manifest.json",
        "bge_validation": BGE / "INDEPENDENT_VALIDATION.json",
        "bge_cell_summary": BGE / "cell_summary.csv",
        "bge_primary_contrasts": BGE / "primary_contrasts.csv",
        "bge_primary_table": BGE / "primary_contrasts.tex",
        "bge_predictions": BGE / "formal_run/predictions.jsonl",
        "bge_provenance": BGE / "formal_run/provenance.json",
        "bge_resources": BGE / "formal_run/resource_usage.json",
        "upstream_matrix_protocol_freeze": UPSTREAM_MATRIX / "PROTOCOL_FREEZE.json",
        "upstream_matrix_protocol_clarification": UPSTREAM_MATRIX / "PROTOCOL_CLARIFICATION_PRE_ANALYSIS.md",
        "upstream_matrix_analysis_freeze": UPSTREAM_MATRIX / "ANALYSIS_FREEZE.json",
        "upstream_matrix_run_success": UPSTREAM_MATRIX / "formal_run_5x5/SUCCESS.json",
        "upstream_matrix_results": UPSTREAM_ANALYSIS / "results.json",
        "upstream_matrix_validation": UPSTREAM_ANALYSIS / "validation.json",
        "upstream_matrix_cells": UPSTREAM_ANALYSIS / "cell_summary.csv",
        "upstream_matrix_independent_audit": UPSTREAM_ANALYSIS / "INDEPENDENT_AUDIT.json",
        "upstream_matrix_independent_report": UPSTREAM_ANALYSIS / "INDEPENDENT_AUDIT.md",
    }
    main_rows = rows(source_paths["main_results"])
    role_rows = rows(source_paths["role_effects"])
    runtime_rows = rows(source_paths["runtime_memory"])
    failure_rows = rows(source_paths["failure_audit"])
    case_rows = rows(source_paths["case_stability"])
    manifest = load(source_paths["canonical_manifest"])
    validation = load(source_paths["validation"])
    data = load(DATA)
    upstream = load(UPSTREAM)
    freeze = load(source_paths["freeze_manifest"])
    audit = load(source_paths["evidence_audit"])
    conversion = load(CONVERSION_AUDIT)
    method = load(METHOD_CONTRACT)
    upstream_matrix = load(source_paths["upstream_matrix_results"])
    upstream_matrix_validation = load(source_paths["upstream_matrix_validation"])
    upstream_variance = upstream_matrix["primary"]["variance_decomposition"]
    upstream_composition = upstream_matrix["primary"]["document_clustered_composition_sensitivity"]

    by_pk = {(r["protocol"], int(r["k"])): r for r in main_rows}
    by_role = {(r["comparison"], int(r["k"])): r for r in role_rows}
    pred3 = by_pk[("predicted-label", 3)]
    blind3 = by_pk[("label-blind", 3)]
    bm251 = by_pk[("bm25", 1)]
    bm253 = by_pk[("bm25", 3)]
    role3 = by_role[("predicted-label_minus_label-blind", 3)]
    counts = data["counts"]
    docs = data["leakage_audit"]["unique_documents"]
    cfg = freeze["fingerprint"]["base_run_config"]
    case_counts = Counter(r["category"] for r in case_rows)

    macros = [
        "% GENERATED FILE. DO NOT EDIT. Source hashes are in claim_source_map.json.",
        macro("TrainInstances", counts["train"]),
        macro("DevInstances", counts["dev"]),
        macro("TestInstances", counts["test"]),
        macro("TrainDocuments", docs["train"]),
        macro("DevDocuments", docs["dev"]),
        macro("TestDocuments", docs["test"]),
        macro("DocumentOverlap", data["leakage_audit"]["overlap_document_count"]),
        macro("SeedCount", len(manifest["seeds"])),
        macro("ProtocolCount", 3),
        macro("SuccessfulRuns", sum(r["status"] == "success" for r in failure_rows)),
        macro("AuditChecks", audit["check_count"]),
        macro("AuditFailures", audit["failure_count"]),
        macro("BootstrapSamples", cfg["bootstrap_samples"]),
        macro("TrainingEpochs", cfg["epochs"]),
        macro("LearningRate", cfg["lr"]),
        macro("TrainingCutoff", cfg["train_k"]),
        macro("EvalCutoffs", ", ".join(map(str, cfg["eval_k"]))),
        macro("EncoderModel", str(cfg["encoder"]).replace("_", r"\_")),
        macro("PredKThreeFOne", f4(pred3["mean_f1"])),
        macro("PredKThreeSD", f4(pred3["sample_std_f1"])),
        macro("BlindKThreeFOne", f4(blind3["mean_f1"])),
        macro("BMKOneFOne", f4(bm251["mean_f1"])),
        macro("BMKThreeFOne", f4(bm253["mean_f1"])),
        macro("PredVsBMKThreeDelta", signed4(pred3["delta_vs_bm25"])),
        macro("PredVsBMKThreeCI", ci4(pred3["hier_ci95_low"], pred3["hier_ci95_high"])),
        macro("RoleKThreeDelta", signed4(role3["mean_delta"])),
        macro("RoleKThreeTCI", ci4(role3["seed_t_ci_low"], role3["seed_t_ci_high"])),
        macro("RoleKThreeHierCI", ci4(role3["hier_ci_low"], role3["hier_ci_high"])),
        macro("UpstreamTestAccuracy", f3(upstream["test"]["accuracy"])),
        macro("UpstreamTestMacroFOne", f3(upstream["test"]["macro_f1"])),
        macro("CaseCount", len(case_rows)),
        macro("CaseAllTie", case_counts.get("all_tie", 0)),
        macro("CanonicalPredictionRows", validation["canonical_prediction_rows"]),
        macro("SourceRows", conversion["eligibility"]["source_rows"]),
        macro("EligibleRows", conversion["eligibility"]["eligible_unique_rows"]),
        macro("ShortCandidateExclusions", conversion["eligibility"]["excluded_fewer_than_two_sentences"]),
        macro("UpstreamMatrixCells", upstream_matrix_validation["primary_cells"]),
        macro("UpstreamMatrixGrandFOne", f4(upstream_variance["grand_mean"])),
        macro("UpstreamMatrixUpstreamRange", f'{min(upstream_variance["upstream_means"]):.4f}--{max(upstream_variance["upstream_means"]):.4f}'),
        macro("UpstreamMatrixDownstreamRange", f'{min(upstream_variance["downstream_means"]):.4f}--{max(upstream_variance["downstream_means"]):.4f}'),
        macro("UpstreamMatrixCompositionCI", ci4(*upstream_composition["composition_interval_95"])),
    ]
    (OUT / "canonical_numbers.tex").write_text("\n".join(macros) + "\n", encoding="utf-8")

    labels = {"oracle-label": r"Oracle-label$^{\dagger}$", "predicted-label": "Predicted-label", "label-blind": "Label-blind", "bm25": "BM25"}
    lines = [r"\begin{tabular}{llrrrr}", r"\toprule", r"System & $K$ & Mean F1 & SD & $\Delta$ vs. BM25 & Criterion \\", r"\midrule"]
    for r in main_rows:
        gate = "Reference" if r["protocol"] == "bm25" else tex_bool(r["positive_effect_gate"])
        lines.append(f'{labels[r["protocol"]]} & {r["k"]} & {f4(r["mean_f1"])} & {f4(r["sample_std_f1"])} & {signed4(r["delta_vs_bm25"])} & {gate} \\\\')
    lines += [r"\bottomrule", r"\end{tabular}"]
    (OUT / "table_main_results.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")

    comp = {
        "oracle-label_minus_predicted-label": r"Oracle$^{\dagger}$ $-$ predicted",
        "oracle-label_minus_label-blind": r"Oracle$^{\dagger}$ $-$ blind",
        "predicted-label_minus_label-blind": "Predicted $-$ blind",
    }
    lines = [r"\begin{tabular}{llrrr}", r"\toprule", r"Contrast & $K$ & Mean $\Delta$ & Hierarchical 95\% CI & Criterion \\", r"\midrule"]
    for r in role_rows:
        lines.append(f'{comp[r["comparison"]]} & {r["k"]} & {signed4(r["mean_delta"])} & {ci4(r["hier_ci_low"], r["hier_ci_high"])} & {tex_bool(r["positive_effect_gate"])} \\\\')
    lines += [r"\bottomrule", r"\end{tabular}"]
    (OUT / "table_role_effects.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")

    lines = [r"\begin{tabular}{lrrrr}", r"\toprule", r"Protocol & Wall time (s) & SD (s) & Peak RSS (GiB) & SD (GiB) \\", r"\midrule"]
    for r in runtime_rows:
        lines.append(f'{labels[r["protocol"]]} & {f2(r["mean_wall_seconds"])} & {f2(r["sd_wall_seconds"])} & {f3(r["mean_peak_rss_gib"])} & {f3(r["sd_peak_rss_gib"])} \\\\')
    lines += [r"\bottomrule", r"\end{tabular}"]
    (OUT / "table_runtime.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")

    lines = [r"\begin{tabular}{lrrr}", r"\toprule", r"Partition & Instances & Documents & Cross-split overlap \\", r"\midrule"]
    for split, title in (("train", "Train"), ("dev", "Development"), ("test", "Test")):
        lines.append(f'{title} & {counts[split]} & {docs[split]} & {data["leakage_audit"]["overlap_document_count"]} \\\\')
    lines += [r"\bottomrule", r"\end{tabular}"]
    (OUT / "table_data_audit.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")

    lines = [r"\begin{tabular}{llrrr}", r"\toprule", r"Partition & Prediction scheme & Accuracy & Balanced accuracy & Macro-F1 \\", r"\midrule"]
    schemes = {"train": "Document-grouped OOF", "dev": "Train-only model", "test": "Train-only model"}
    for split, title in (("train", "Train"), ("dev", "Development"), ("test", "Test")):
        u = upstream[split]
        lines.append(f'{title} & {schemes[split]} & {f3(u["accuracy"])} & {f3(u["balanced_accuracy"])} & {f3(u["macro_f1"])} \\\\')
    lines += [r"\bottomrule", r"\end{tabular}"]
    (OUT / "table_upstream.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")

    lines = [r"\begin{tabular}{>{\raggedright\arraybackslash}p{0.16\textwidth}>{\raggedright\arraybackslash}p{0.35\textwidth}>{\raggedright\arraybackslash}p{0.37\textwidth}}", r"\toprule", r"Element & Frozen choice & Implementation detail \\", r"\midrule"]
    for element, choice, detail in method["rows"]:
        lines.append(f"{element} & {choice} & {detail} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    (OUT / "table_implementation.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")

    ex = conversion["eligibility"]
    limits = conversion["document_limit_exclusions"]
    lines = [r"\begin{tabular}{lrrr}", r"\toprule", r"Stage & Train & Development & Test \\", r"\midrule",
             f'Source rows pooled & {conversion["local_cache"]["split_rows"]["train"]} & {conversion["local_cache"]["split_rows"]["dev"]} & {conversion["local_cache"]["split_rows"]["test"]} \\\\',
             f'Excluded: $<2$ candidate sentences & {ex["excluded_fewer_than_two_sentences"]} & 0 & 0 \\\\',
             f'Eligible unique rows (pooled) & \\multicolumn{{3}}{{c}}{{{ex["eligible_unique_rows"]}}} \\\\',
             f'Excluded by whole-document capacity rule & {limits["train"]["rows"]} & {limits["dev"]["rows"]} & {limits["test"]["rows"]} \\\\',
             f'Final rows & {conversion["included"]["rows"]["train"]} & {conversion["included"]["rows"]["dev"]} & {conversion["included"]["rows"]["test"]} \\\\',
             r"\bottomrule", r"\end{tabular}"]
    (OUT / "table_conversion_audit.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Keep the manuscript directory independently compilable while retaining the
    # frozen result table as the hash-bound source of the copied fragment.
    (OUT / "table_bge_contrasts.tex").write_text(
        source_paths["bge_primary_table"].read_text(encoding="utf-8").replace(
            r"95\% composition interval", r"95\% composition-sensitivity interval"
        ),
        encoding="utf-8",
    )
    (OUT / "table_structural_neural_contrasts.tex").write_text(
        source_paths["addon_primary_table"].read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    exploratory_target = HERE.parent.parent / "figures/results/fig06_exploratory_forest.pdf"
    exploratory_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_paths["exploratory_primary_figure"], exploratory_target)

    variance_components = upstream_variance["descriptive_variance_components"]
    lines = [r"\begin{tabular}{lr}", r"\toprule", r"Quantity & Estimate \\", r"\midrule",
             f'Crossed upstream--downstream cells & {upstream_matrix_validation["primary_cells"]} ' + r'\\',
             f'Grand mean exact-ID F1 at $K=3$ & {f4(upstream_variance["grand_mean"])} ' + r'\\',
             f'Upstream-seed mean range & {min(upstream_variance["upstream_means"]):.4f}--{max(upstream_variance["upstream_means"]):.4f} ' + r'\\',
             f'Downstream-seed mean range & {min(upstream_variance["downstream_means"]):.4f}--{max(upstream_variance["downstream_means"]):.4f} ' + r'\\',
             f'Upstream variance component & {variance_components["upstream"]:.8f} ' + r'\\',
             f'Downstream variance component & {variance_components["downstream"]:.8f} ' + r'\\',
             f'Interaction/residual variance & {variance_components["interaction_residual"]:.8f} ' + r'\\',
             f'Document-composition sensitivity interval & {ci4(*upstream_composition["composition_interval_95"])} ' + r'\\',
             r"\bottomrule", r"\end{tabular}"]
    (OUT / "table_upstream_seed_matrix.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")

    source_map = {
        "status": "generated-from-frozen-artifacts",
        "canonical_manifest_status": manifest["status"],
        "claim_decisions": manifest["claim_decisions"],
        "sources": {name: {"path": str(path.relative_to(ROOT)), "sha256": sha(path)} for name, path in source_paths.items()},
        "generated": {p.name: sha(p) for p in sorted(OUT.glob("*.tex"))},
    }
    (OUT / "claim_source_map.json").write_text(json.dumps(source_map, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
