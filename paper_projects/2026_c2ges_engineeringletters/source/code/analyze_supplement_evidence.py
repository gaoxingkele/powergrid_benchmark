#!/usr/bin/env python3
"""Extract and cross-check the in-package evidence in the BM25/K-sensitivity supplement.

Reads  source/supplement/bm25_k_sensitivity/summary.json  and writes
  source/supplement/bm25_k_sensitivity/derived_tables.json
  source/supplement/bm25_k_sensitivity/derived_tables.md

Sections produced:
  (a) K=3 aggregate metrics table for all seven conditions;
  (b) ALL paired document-cluster bootstrap comparisons (9 comparisons x 4 metrics);
  (c) role-stratified K=3 table (5 causal roles x 7 conditions);
  (d) per-document dispersion statistics of evidence F1 (40 docs per condition per K);
  (e) supplement-vs-manuscript cross-check for every number the manuscript
      (source/paper.tex) cites that also lives in this supplement.

No file outside the supplement directory is modified. The script is deterministic
and has no third-party dependencies.
"""

import json
import math
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUPP = HERE.parent / "supplement" / "bm25_k_sensitivity"
SUMMARY = SUPP / "summary.json"

ROLES = ["trigger_event", "root_cause", "propagation_or_response", "impact", "mitigation"]
K3_CONDITIONS = [
    "bm25_query",
    "tfidf_query",
    "sbert_query",
    "c2ges_full",
    "c2ges_no_graph",
    "c2ges_no_role",
    "c2ges_query_only",
]
METRICS = ["evidence_f1", "evidence_precision", "evidence_recall", "rouge_l_selected_evidence_text"]


def r4(x):
    return round(float(x), 4)


# ----------------------------------------------------------------------------- (a)
def aggregate_k3_table(data):
    agg = data["aggregate_metrics_by_k_condition"]["3"]
    table = {}
    for cond in K3_CONDITIONS:
        m = agg[cond]
        table[cond] = {
            "evidence_f1": m["evidence_f1"],
            "evidence_f1_std": m["evidence_f1_std"],
            "evidence_precision": m["evidence_precision"],
            "evidence_precision_std": m["evidence_precision_std"],
            "evidence_recall": m["evidence_recall"],
            "evidence_recall_std": m["evidence_recall_std"],
            "rouge_l": m["rouge_l_selected_evidence_text"],
            "rouge_l_std": m["rouge_l_selected_evidence_text_std"],
            "questions": m["questions"],
        }
    return table


# ----------------------------------------------------------------------------- (b)
def paired_comparison_table(data):
    pc = data["paired_comparisons"]
    out = {
        "method": pc["method"],
        "samples": pc["samples"],
        "seed": pc["seed"],
        "comparisons": {},
    }
    for name in sorted(pc["comparisons"]):
        comp = pc["comparisons"][name]
        out["comparisons"][name] = {
            metric: {
                "mean_diff": comp[metric]["mean_diff"],
                "ci95_lower": comp[metric]["ci95"]["lower"],
                "ci95_upper": comp[metric]["ci95"]["upper"],
                "bootstrap_two_sided_p": comp[metric]["bootstrap_two_sided_p"],
                "n_units": comp[metric]["n_units"],
            }
            for metric in METRICS
        }
    return out


# ----------------------------------------------------------------------------- (c)
def role_stratified_k3_table(data):
    rs = data["role_stratified_metrics_by_k_condition"]["3"]
    table = {}
    for cond in K3_CONDITIONS:
        table[cond] = {
            role: {
                "evidence_f1": rs[cond][role]["evidence_f1"],
                "evidence_precision": rs[cond][role]["evidence_precision"],
                "evidence_recall": rs[cond][role]["evidence_recall"],
                "questions": rs[cond][role]["questions"],
            }
            for role in ROLES
        }
    return table


# ----------------------------------------------------------------------------- (d)
def document_dispersion(data):
    dl = data["document_level_metrics_by_k_condition"]
    out = {}
    for k in sorted(dl, key=int):
        out[k] = {}
        for cond in sorted(dl[k]):
            f1s = [dl[k][cond][doc]["evidence_f1"] for doc in sorted(dl[k][cond])]
            out[k][cond] = {
                "n_documents": len(f1s),
                "mean": statistics.mean(f1s),
                "std": statistics.pstdev(f1s),
                "sample_std": statistics.stdev(f1s),
                "min": min(f1s),
                "median": statistics.median(f1s),
                "max": max(f1s),
                "n_docs_f1_zero": sum(1 for v in f1s if v == 0.0),
                "n_docs_f1_ge_0.5": sum(1 for v in f1s if v >= 0.5),
            }
    return out


# ----------------------------------------------------------------------------- (e)
def cross_check(data):
    """Compare every manuscript number that also lives in the supplement.

    Manuscript values are transcribed from source/paper.tex (Tables 3-6, the
    abstract, Section 5.1/6 text). A claim MATCHES when the supplement value,
    rounded to the manuscript's printed precision, equals the manuscript value.
    """
    agg = data["aggregate_metrics_by_k_condition"]
    rs3 = data["role_stratified_metrics_by_k_condition"]["3"]
    pc = data["paired_comparisons"]["comparisons"]
    ds = data["dataset"]
    checks = []

    def add(label, manuscript, supplement, ndigits=4):
        sup_rounded = round(float(supplement), ndigits)
        checks.append(
            {
                "claim": label,
                "manuscript_value": manuscript,
                "supplement_value": float(supplement),
                "supplement_rounded": sup_rounded,
                "match": math.isclose(sup_rounded, manuscript, abs_tol=10 ** (-ndigits) / 2 + 1e-12),
            }
        )

    # --- Table 3 (tab:3): the four query-retrieval / full rows -----------------
    t3 = {
        "tfidf_query": ("TF-IDF query retrieval", 0.2122, 0.2293, 0.2050, 0.2253, 0.2471, 0.2976, 0.3224, 0.1931),
        "bm25_query": ("BM25 query retrieval", 0.2273, 0.2410, 0.2217, 0.2410, 0.2575, 0.2971, 0.3247, 0.1929),
        "sbert_query": ("SBERT query retrieval", 0.1972, 0.2301, 0.1883, 0.2200, 0.2329, 0.3037, 0.3067, 0.1884),
        "c2ges_full": ("Full C2GES reranker", 0.2983, 0.2409, 0.2950, 0.2454, 0.3325, 0.2993, 0.3732, 0.1933),
    }
    for cond, (name, f1, f1s, p, ps, r, rcs, rl, rls) in t3.items():
        m = agg["3"][cond]
        add(f"Table 3 {name}: evidence F1", f1, m["evidence_f1"])
        add(f"Table 3 {name}: F1 std", f1s, m["evidence_f1_std"])
        add(f"Table 3 {name}: precision", p, m["evidence_precision"])
        add(f"Table 3 {name}: precision std", ps, m["evidence_precision_std"])
        add(f"Table 3 {name}: recall", r, m["evidence_recall"])
        add(f"Table 3 {name}: recall std", rcs, m["evidence_recall_std"])
        add(f"Table 3 {name}: ROUGE-L", rl, m["rouge_l_selected_evidence_text"])
        add(f"Table 3 {name}: ROUGE-L std", rls, m["rouge_l_selected_evidence_text_std"])

    # --- Abstract improvement percentages -------------------------------------
    full = agg["3"]["c2ges_full"]["evidence_f1"]
    add(
        "Abstract: ~41% improvement over TF-IDF query (percent)",
        41.0,
        100.0 * (full / agg["3"]["tfidf_query"]["evidence_f1"] - 1.0),
        ndigits=0,
    )
    add(
        "Abstract: ~51% improvement over SBERT query (percent)",
        51.0,
        100.0 * (full / agg["3"]["sbert_query"]["evidence_f1"] - 1.0),
        ndigits=0,
    )

    # --- Table 4 (tab:4): baseline paired rows (evidence F1) ------------------
    t4 = {
        "k3_c2ges_full_vs_tfidf_query": ("vs TF-IDF query", 0.0861, 0.0581, 0.1145),
        "k3_c2ges_full_vs_bm25_query": ("vs BM25 query", 0.0710, 0.0423, 0.1000),
        "k3_c2ges_full_vs_sbert_query": ("vs SBERT query", 0.1010, 0.0629, 0.1388),
    }
    for key, (name, diff, lo, hi) in t4.items():
        c = pc[key]["evidence_f1"]
        add(f"Table 4 {name}: mean F1 diff", diff, c["mean_diff"])
        add(f"Table 4 {name}: CI lower", lo, c["ci95"]["lower"])
        add(f"Table 4 {name}: CI upper", hi, c["ci95"]["upper"])
        checks.append(
            {
                "claim": f"Table 4 {name}: p < 0.001",
                "manuscript_value": "<0.001",
                "supplement_value": c["bootstrap_two_sided_p"],
                "supplement_rounded": c["bootstrap_two_sided_p"],
                "match": c["bootstrap_two_sided_p"] < 0.001,
            }
        )

    # --- Table 4 ablation mean diffs (CI/p NOT in supplement; means are) ------
    for cond, name, diff in [
        ("c2ges_query_only", "vs C2GES query-only: mean F1 diff (derived from aggregates)", 0.0831),
        ("c2ges_no_role", "vs C2GES no-role: mean F1 diff (derived from aggregates)", 0.0688),
        ("c2ges_no_graph", "vs C2GES no-graph: mean F1 diff (derived from aggregates)", 0.0060),
    ]:
        add(f"Table 4 {name}", diff, full - agg["3"][cond]["evidence_f1"])

    # --- Section 6.2 ablation aggregate F1 values ------------------------------
    add("Sec 6.2 text: query-only F1", 0.2152, agg["3"]["c2ges_query_only"]["evidence_f1"])
    add("Sec 6.2 text: no-role F1", 0.2295, agg["3"]["c2ges_no_role"]["evidence_f1"])
    add("Sec 6.2 text: no-graph F1", 0.2923, agg["3"]["c2ges_no_graph"]["evidence_f1"])

    # --- Table 5 (tab:k_sensitivity) -------------------------------------------
    ks = {
        "tfidf_query": ("TF-IDF query", 0.1783, 0.2122, 0.2162),
        "bm25_query": ("BM25 query", 0.1857, 0.2273, 0.2208),
        "sbert_query": ("SBERT query", 0.1560, 0.1972, 0.2042),
        "c2ges_full": ("Full C2GES", 0.2133, 0.2983, 0.2850),
    }
    for cond, (name, k1, k3, k5) in ks.items():
        add(f"Table 5 {name}: K=1 F1", k1, agg["1"][cond]["evidence_f1"])
        add(f"Table 5 {name}: K=3 F1", k3, agg["3"][cond]["evidence_f1"])
        add(f"Table 5 {name}: K=5 F1", k5, agg["5"][cond]["evidence_f1"])

    # --- Section 6.2 K-sensitivity text claims ---------------------------------
    c5 = pc["k5_c2ges_full_vs_bm25_query"]["evidence_f1"]
    add("Sec 6.2 text: K=5 gain over BM25", 0.0643, c5["mean_diff"])
    add("Sec 6.2 text: K=5 CI lower", 0.0331, c5["ci95"]["lower"])
    add("Sec 6.2 text: K=5 CI upper", 0.0961, c5["ci95"]["upper"])
    for key, name in [
        ("k1_c2ges_full_vs_tfidf_query", "vs TF-IDF"),
        ("k1_c2ges_full_vs_bm25_query", "vs BM25"),
    ]:
        c1 = pc[key]["evidence_f1"]
        crosses = c1["ci95"]["lower"] <= 0.0 <= c1["ci95"]["upper"]
        checks.append(
            {
                "claim": f"Sec 6.2 text: K=1 CI {name} crosses zero",
                "manuscript_value": "crosses zero",
                "supplement_value": [c1["ci95"]["lower"], c1["ci95"]["upper"]],
                "supplement_rounded": [r4(c1["ci95"]["lower"]), r4(c1["ci95"]["upper"])],
                "match": crosses,
            }
        )

    # --- Table tab:per_role_full_metrics ----------------------------------------
    per_role = {
        "trigger_event": ("Trigger event", 0.3114, 0.2833, 0.4000, 0.1006, 0.0723),
        "root_cause": ("Root cause", 0.2594, 0.2500, 0.2896, 0.0470, 0.0475),
        "propagation_or_response": ("Propagation/response", 0.2611, 0.2750, 0.2625, 0.0436, 0.0281),
        "impact": ("Impact", 0.3429, 0.3500, 0.3625, 0.1438, 0.0988),
        "mitigation": ("Mitigation", 0.3167, 0.3167, 0.3479, 0.0955, 0.0971),
    }
    for role, (name, f1, p, r, d_tfidf, d_norole) in per_role.items():
        m = rs3["c2ges_full"][role]
        add(f"Per-role table {name}: full F1", f1, m["evidence_f1"])
        add(f"Per-role table {name}: full precision", p, m["evidence_precision"])
        add(f"Per-role table {name}: full recall", r, m["evidence_recall"])
        add(
            f"Per-role table {name}: F1 delta vs TF-IDF query",
            d_tfidf,
            m["evidence_f1"] - rs3["tfidf_query"][role]["evidence_f1"],
        )
        add(
            f"Per-role table {name}: F1 delta vs NoRole",
            d_norole,
            m["evidence_f1"] - rs3["c2ges_no_role"][role]["evidence_f1"],
        )

    # --- Table tab:role_graph_delta ---------------------------------------------
    graph_delta = {
        "trigger_event": ("Trigger event", 0.3114, 0.0000),
        "root_cause": ("Root cause", 0.2594, 0.0000),
        "propagation_or_response": ("Propagation/response", 0.2527, 0.0083),
        "impact": ("Impact", 0.3429, 0.0000),
        "mitigation": ("Mitigation", 0.2952, 0.0214),
    }
    for role, (name, nograph_f1, delta) in graph_delta.items():
        m_ng = rs3["c2ges_no_graph"][role]
        add(f"Graph-delta table {name}: NoGraph F1", nograph_f1, m_ng["evidence_f1"])
        add(
            f"Graph-delta table {name}: delta",
            delta,
            rs3["c2ges_full"][role]["evidence_f1"] - m_ng["evidence_f1"],
        )

    # --- Dataset facts ------------------------------------------------------------
    add("Dataset: document count", 40, ds["document_count"], ndigits=0)
    add("Dataset: question count", 200, ds["question_count"], ndigits=0)
    add("Dataset: evidence ID count", 608, ds["evidence_id_count"], ndigits=0)
    add("Dataset: schema validation errors", 0, ds["annotation_summary"]["schema_evidence_validation_errors"], ndigits=0)
    add("Dataset: newly annotated documents", 15, ds["annotation_summary"]["new_documents_annotated"], ndigits=0)

    n_match = sum(1 for c in checks if c["match"])
    return {
        "n_checks": len(checks),
        "n_match": n_match,
        "n_mismatch": len(checks) - n_match,
        "checks": checks,
    }


# ----------------------------------------------------------------------------- md
def to_markdown(derived):
    lines = []
    a = lines.append
    a("# Derived tables from `summary.json` (BM25 / K-sensitivity supplement)")
    a("")
    a("Generated by `source/code/analyze_supplement_evidence.py`. All values are")
    a("extracted or arithmetically derived from `summary.json`; nothing is new data.")
    a("")

    a("## (a) K=3 aggregate metrics, all seven conditions")
    a("")
    a("| Condition | Evidence F1 | Precision | Recall | ROUGE-L | Questions |")
    a("| --- | ---: | ---: | ---: | ---: | ---: |")
    for cond, m in derived["a_aggregate_k3"].items():
        a(
            f"| {cond} | {m['evidence_f1']:.4f} ± {m['evidence_f1_std']:.4f} "
            f"| {m['evidence_precision']:.4f} ± {m['evidence_precision_std']:.4f} "
            f"| {m['evidence_recall']:.4f} ± {m['evidence_recall_std']:.4f} "
            f"| {m['rouge_l']:.4f} ± {m['rouge_l_std']:.4f} | {m['questions']} |"
        )
    a("")

    a("## (b) All paired document-cluster bootstrap comparisons")
    a("")
    pcs = derived["b_paired_comparisons"]
    a(f"Method: {pcs['method']}; samples: {pcs['samples']}; seed: {pcs['seed']}.")
    a("")
    a("| Comparison | Metric | Mean diff | 95% CI | p (bootstrap, two-sided) |")
    a("| --- | --- | ---: | --- | ---: |")
    for name, comp in pcs["comparisons"].items():
        for metric in METRICS:
            c = comp[metric]
            a(
                f"| {name} | {metric} | {c['mean_diff']:.4f} "
                f"| [{c['ci95_lower']:.4f}, {c['ci95_upper']:.4f}] | {c['bootstrap_two_sided_p']:.4f} |"
            )
    a("")

    a("## (c) Role-stratified evidence F1 at K=3 (5 roles x 7 conditions)")
    a("")
    header = "| Condition | " + " | ".join(ROLES) + " |"
    a(header)
    a("| --- |" + " ---: |" * len(ROLES))
    for cond, roles in derived["c_role_stratified_k3"].items():
        a("| " + cond + " | " + " | ".join(f"{roles[r]['evidence_f1']:.4f}" for r in ROLES) + " |")
    a("")
    a("Per-role precision/recall for every condition are in `derived_tables.json`.")
    a("")

    a("## (d) Per-document evidence-F1 dispersion (40 documents per condition)")
    a("")
    for k, conds in derived["d_document_dispersion"].items():
        a(f"### K={k}")
        a("")
        a("| Condition | Mean | Std (pop.) | Min | Median | Max | Docs F1=0 | Docs F1>=0.5 |")
        a("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
        for cond, s in conds.items():
            a(
                f"| {cond} | {s['mean']:.4f} | {s['std']:.4f} | {s['min']:.4f} "
                f"| {s['median']:.4f} | {s['max']:.4f} | {s['n_docs_f1_zero']} | {s['n_docs_f1_ge_0.5']} |"
            )
        a("")

    a("## (e) Supplement-vs-manuscript cross-check")
    a("")
    cc = derived["e_cross_check"]
    a(f"{cc['n_match']}/{cc['n_checks']} checks match; {cc['n_mismatch']} mismatch.")
    a("")
    a("| Claim | Manuscript | Supplement (rounded) | Match |")
    a("| --- | --- | --- | --- |")
    for c in cc["checks"]:
        a(f"| {c['claim']} | {c['manuscript_value']} | {c['supplement_rounded']} | {'YES' if c['match'] else '**NO**'} |")
    a("")

    a("## Dataset and provenance facts used by the manuscript")
    a("")
    for k, v in derived["dataset_facts"].items():
        a(f"- **{k}**: {v}")
    a("")
    return "\n".join(lines)


def main():
    data = json.loads(SUMMARY.read_text(encoding="utf-8"))
    ds = data["dataset"]
    derived = {
        "source": str(SUMMARY),
        "run_timestamp": data["metadata"]["run_timestamp"],
        "code_version_or_git_sha": data["metadata"]["code_version_or_git_sha"],
        "a_aggregate_k3": aggregate_k3_table(data),
        "b_paired_comparisons": paired_comparison_table(data),
        "c_role_stratified_k3": role_stratified_k3_table(data),
        "d_document_dispersion": document_dispersion(data),
        "e_cross_check": cross_check(data),
        "dataset_facts": {
            "name": ds["name"],
            "base_dataset": ds["base_dataset"],
            "document_count": ds["document_count"],
            "question_count": ds["question_count"],
            "evidence_id_count": ds["evidence_id_count"],
            "label_provenance": ds["label_provenance"],
            "new_documents_annotated": ds["annotation_summary"]["new_documents_annotated"],
            "schema_evidence_validation_errors": ds["annotation_summary"]["schema_evidence_validation_errors"],
            "suspicious_low_evidence_diversity": ds["annotation_summary"]["suspicious_low_evidence_diversity"],
            "verifier_pass": ds["independent_verifier_summary"]["pass"],
            "verifier_pass_with_minor_repaired": ds["independent_verifier_summary"]["pass_with_minor_repaired"],
            "verifier_fail_repaired_by_answer_narrowing": ds["independent_verifier_summary"]["fail_repaired_by_answer_narrowing"],
            "verifier_failed_batches_due_to_429": ds["independent_verifier_summary"]["failed_verifier_batches_due_to_429"],
            "verifier_notes": ds["independent_verifier_summary"]["notes"],
            "source_asset_root": ds["source_asset_root"],
            "role_counts": ds["schema_evidence_validation"]["role_counts"],
        },
    }

    (SUPP / "derived_tables.json").write_text(json.dumps(derived, indent=2), encoding="utf-8")
    md = to_markdown(derived)
    (SUPP / "derived_tables.md").write_text(md, encoding="utf-8")

    cc = derived["e_cross_check"]
    print(f"Wrote {SUPP / 'derived_tables.json'}")
    print(f"Wrote {SUPP / 'derived_tables.md'}")
    print(f"Cross-check: {cc['n_match']}/{cc['n_checks']} match, {cc['n_mismatch']} mismatch")
    for c in cc["checks"]:
        if not c["match"]:
            print(f"  MISMATCH: {c['claim']}: manuscript={c['manuscript_value']} supplement={c['supplement_rounded']} (raw {c['supplement_value']})")


if __name__ == "__main__":
    main()
