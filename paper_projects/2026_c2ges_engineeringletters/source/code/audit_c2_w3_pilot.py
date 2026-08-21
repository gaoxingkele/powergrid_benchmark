#!/usr/bin/env python3
"""Audit and summarize the seed-2026 full C2GES W3 pilot."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


PROTOCOL_DIRS = {
    "oracle-label": "oracle",
    "predicted-label": "predicted",
    "label-blind": "label_blind",
}
K_VALUES = (1, 3, 5, 10)
MODES = ("full", "query_only", "no_role", "no_graph", "tfidf", "bm25", "sbert", "lead_k", "lexcue")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cluster_bootstrap(left: dict, right: dict, samples: int, seed: int) -> dict:
    qids = sorted(set(left) & set(right))
    by_doc = defaultdict(list)
    for qid in qids:
        if left[qid]["underlying_document_id"] != right[qid]["underlying_document_id"]:
            raise ValueError(f"document mismatch for {qid}")
        by_doc[left[qid]["underlying_document_id"]].append(left[qid]["f1"] - right[qid]["f1"])
    docs = sorted(by_doc)
    rng = np.random.default_rng(seed)
    deltas = []
    for _ in range(samples):
        chosen = rng.choice(docs, size=len(docs), replace=True)
        values = [value for doc in chosen for value in by_doc[doc]]
        deltas.append(float(np.mean(values)))
    values = np.asarray(deltas)
    observed = float(np.mean([value for doc in docs for value in by_doc[doc]]))
    return {
        "observed_instance_mean_delta": observed,
        "bootstrap_mean_delta": float(values.mean()),
        "ci95": [float(np.quantile(values, 0.025)), float(np.quantile(values, 0.975))],
        "p_two_sided": float(min(1.0, 2 * min(np.mean(values <= 0), np.mean(values >= 0)))),
        "cluster_unit": "underlying_wikipedia_document",
        "cluster_count": len(docs),
        "samples": samples,
        "paired_instance_count": len(qids),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot-root", type=Path, required=True)
    parser.add_argument("--dataset-manifest", type=Path, required=True)
    parser.add_argument("--alias-summary", type=Path, required=True)
    parser.add_argument("--bootstrap-samples", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=2026)
    args = parser.parse_args()

    checks = []
    failures = []

    def check(check_id: str, passed: bool, evidence) -> None:
        row = {"id": check_id, "passed": bool(passed), "evidence": evidence}
        checks.append(row)
        if not passed:
            failures.append(row)

    manifest = json.loads(args.dataset_manifest.read_text(encoding="utf-8"))
    check("dataset_counts", manifest.get("counts") == {"train": 8000, "dev": 1500, "test": 1500}, manifest.get("counts"))
    check("document_split_disjoint", manifest.get("leakage_audit", {}).get("passed") is True, manifest.get("leakage_audit"))
    check("dataset_content_hash_present", bool(manifest.get("content_hashes", {}).get("corpus_sha256")), manifest.get("content_hashes"))

    alias = json.loads(args.alias_summary.read_text(encoding="utf-8"))
    check("title_alias_review_complete", alias.get("canonical_freeze_ready") is True, alias)
    check("title_alias_scope_caveat", "does not" in alias.get("method_scope", "").lower(), alias.get("method_scope"))

    upstream_dir = args.pilot_root / "upstream_labels"
    upstream_metrics = json.loads((upstream_dir / "metrics.json").read_text(encoding="utf-8"))
    upstream_provenance = json.loads((upstream_dir / "provenance.json").read_text(encoding="utf-8"))
    predicted_label_map = json.loads((upstream_dir / "predicted_labels.json").read_text(encoding="utf-8"))
    check("upstream_full_counts", [upstream_metrics[s]["n"] for s in ("train", "dev", "test")] == [8000, 1500, 1500], {s: upstream_metrics[s]["n"] for s in ("train", "dev", "test")})
    contract = upstream_provenance.get("no_gold_leakage_contract", {})
    check("upstream_oof_contract", "out-of-fold" in contract.get("train_predictions", ""), contract)
    check("upstream_data_disjoint", upstream_provenance.get("document_leakage_audit", {}).get("passed") is True, upstream_provenance.get("document_leakage_audit"))

    protocol_data = {}
    resources = {}
    summaries = {}
    expected_data_hashes = None
    expected_qids = None
    for protocol, directory in PROTOCOL_DIRS.items():
        run_dir = args.pilot_root / directory
        summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
        config = json.loads((run_dir / "run_config.json").read_text(encoding="utf-8"))
        provenance = json.loads((run_dir / "provenance.json").read_text(encoding="utf-8"))
        resource = json.loads((run_dir / "resource_usage.json").read_text(encoding="utf-8"))
        summaries[protocol] = summary
        resources[protocol] = resource
        check(f"{protocol}:identity", summary.get("protocol") == protocol, summary.get("protocol"))
        check(f"{protocol}:counts", [summary.get("train_n"), summary.get("dev_n"), summary.get("test_n")] == [8000, 1500, 1500], [summary.get("train_n"), summary.get("dev_n"), summary.get("test_n")])
        check(f"{protocol}:k_values", summary.get("evaluated_k") == list(K_VALUES), summary.get("evaluated_k"))
        check(f"{protocol}:bootstrap_config", config.get("bootstrap_samples") == args.bootstrap_samples, config.get("bootstrap_samples"))
        check(f"{protocol}:cluster_unit", summary.get("bootstrap_cluster_unit") == "underlying_wikipedia_document", summary.get("bootstrap_cluster_unit"))
        check(f"{protocol}:leakage", summary.get("document_leakage_audit", {}).get("passed") is True, summary.get("document_leakage_audit"))
        check(f"{protocol}:resource_success", resource.get("status") == "success" and resource.get("failure") is None, resource)
        if protocol == "oracle-label":
            check(f"{protocol}:not_end_to_end", summary.get("end_to_end") is False, summary.get("protocol_definition"))
        else:
            check(f"{protocol}:end_to_end", summary.get("end_to_end") is True, summary.get("protocol_definition"))
        data_hashes = {split: provenance["data_hashes"][split]["sha256"] for split in ("train", "dev", "test")}
        if expected_data_hashes is None:
            expected_data_hashes = data_hashes
        check(f"{protocol}:shared_input_hashes", data_hashes == expected_data_hashes, data_hashes)

        rows = []
        full_by_k = {k: {} for k in K_VALUES}
        with (run_dir / "predictions.jsonl").open(encoding="utf-8") as handle:
            for line in handle:
                row = json.loads(line)
                rows.append(row)
                if row["mode"] == "full":
                    full_by_k[row["k"]][row["qid"]] = row
                if protocol == "oracle-label" and row["selector_role"] != row["gold_role"]:
                    failures.append({"id": f"{protocol}:role_contract", "passed": False, "evidence": row["qid"]})
                if protocol == "label-blind" and row["selector_role"] != "unknown":
                    failures.append({"id": f"{protocol}:role_contract", "passed": False, "evidence": row["qid"]})
                if protocol == "predicted-label" and row["selector_role"] != predicted_label_map.get(row["qid"]):
                    failures.append({"id": f"{protocol}:role_contract", "passed": False, "evidence": row["qid"]})
        expected_rows = 1500 * len(MODES) * len(K_VALUES)
        check(f"{protocol}:prediction_row_count", len(rows) == expected_rows, {"found": len(rows), "expected": expected_rows})
        qids = set(full_by_k[1])
        check(f"{protocol}:full_qids_each_k", all(set(full_by_k[k]) == qids for k in K_VALUES), {str(k): len(full_by_k[k]) for k in K_VALUES})
        if expected_qids is None:
            expected_qids = qids
        check(f"{protocol}:shared_test_qids", qids == expected_qids, len(qids))
        protocol_data[protocol] = full_by_k

    # Role-contract violations are appended directly above; add positive checks
    # when no such violation exists.
    for protocol in PROTOCOL_DIRS:
        violated = any(item["id"] == f"{protocol}:role_contract" for item in failures)
        check(f"{protocol}:role_contract", not violated, "all prediction rows satisfy protocol role source")

    cross = {}
    pairs = (("oracle-label", "predicted-label"), ("oracle-label", "label-blind"), ("predicted-label", "label-blind"))
    for pair_index, (left, right) in enumerate(pairs):
        cross[f"{left}_minus_{right}"] = {
            str(k): cluster_bootstrap(
                protocol_data[left][k], protocol_data[right][k], args.bootstrap_samples, args.seed + pair_index * 100 + k
            )
            for k in K_VALUES
        }
    (args.pilot_root / "cross_protocol_cluster_bootstrap.json").write_text(json.dumps(cross, ensure_ascii=False, indent=2), encoding="utf-8")

    artifact_hashes = {}
    for path in sorted(args.pilot_root.rglob("*")):
        if path.is_file() and path.name not in {"shared_evidence_audit.json", "W3_C2_PILOT_REPORT.md"}:
            artifact_hashes[str(path.relative_to(args.pilot_root)).replace("\\", "/")] = sha256(path)
    audit = {
        "passed": not failures,
        "check_count": len(checks),
        "failure_count": len(failures),
        "checks": checks,
        "failures": failures,
        "corpus_sha256": manifest["content_hashes"]["corpus_sha256"],
        "artifact_sha256": artifact_hashes,
    }
    audit_path = args.pilot_root / "shared_evidence_audit.json"
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# W3 C2GES Pilot Report",
        "",
        "## Scope and decision",
        "",
        f"Shared evidence audit: **{'PASS' if audit['passed'] else 'FAIL'}** ({len(checks)} checks; {len(failures)} failures).",
        "This is a one-seed pilot on the complete document-grouped corpus, not the final five-seed result.",
        "Oracle-label remains conditional evidence selection and is not end-to-end.",
        "",
        "## Data and leakage controls",
        "",
        f"- Instances: 8000 train / 1500 dev / 1500 test; corpus SHA-256 `{manifest['content_hashes']['corpus_sha256']}`.",
        f"- Wikipedia documents: {manifest['leakage_audit']['unique_documents']}; exact document overlap: zero.",
        f"- Title audit examined {alias['cross_split_pairs_examined']} pairs at SequenceMatcher >= {alias['near_duplicate_rule']['sequence_matcher_threshold']} and trigram Jaccard >= {alias['near_duplicate_rule']['character_trigram_jaccard_prefilter']}.",
        f"- Exact normalized aliases: {alias['hard_exact_alias_count']}; reviewed candidates: {alias['review_candidate_count']}; unreviewed: {alias['unreviewed_candidate_count']}.",
        "- The sole high-similarity candidate was A_Game_of_Thrones versus Game_of_Thrones, manually evidenced as novel versus television series.",
        "- This title screen does not establish absence of redirect, content-level, or semantic near-duplicates.",
        "",
        "## Upstream label predictor",
        "",
        "| Split | Accuracy | Balanced accuracy | Macro-F1 |",
        "|---|---:|---:|---:|",
    ]
    for split in ("train", "dev", "test"):
        item = upstream_metrics[split]
        lines.append(f"| {split} | {item['accuracy']:.4f} | {item['balanced_accuracy']:.4f} | {item['macro_f1']:.4f} |")
    lines.extend(["", "Train values are document-grouped OOF predictions; dev/test use a model fitted only on train.", "", "## Selector evidence F1", "", "| Protocol | K=1 | K=3 | K=5 | K=10 |", "|---|---:|---:|---:|---:|"])
    for protocol in PROTOCOL_DIRS:
        vals = [summaries[protocol]["k_sensitivity"][str(k)]["test"]["full"]["evidence_f1"] for k in K_VALUES]
        lines.append(f"| {protocol} | " + " | ".join(f"{value:.4f}" for value in vals) + " |")
    lines.extend(["", "BM25 test F1 was " + ", ".join(f"K={k}: {summaries['oracle-label']['k_sensitivity'][str(k)]['test']['bm25']['evidence_f1']:.4f}" for k in K_VALUES) + ".", "At K=1, BM25 is significantly stronger than each C2GES protocol in the within-run document-cluster bootstrap; K=3 and K=5 differences are not significant. These pilot results do not support a blanket superiority claim.", "", "## Runtime and resources", "", "| Protocol | Wall seconds | Peak RSS GiB | Status |", "|---|---:|---:|---|"])
    for protocol in PROTOCOL_DIRS:
        item = resources[protocol]
        lines.append(f"| {protocol} | {item['wall_seconds']:.2f} | {item['resource_sampling']['peak_tree_rss_gib']:.3f} | {item['status']} |")
    lines.extend(["", "RSS is sampled with psutil over the process tree every 0.2 s; sub-interval peaks and GPU memory are not measured.", "", "## Cross-protocol paired cluster bootstrap", ""])
    for comparison, values in cross.items():
        lines.append(f"- {comparison}: " + "; ".join(f"K={k} delta={values[str(k)]['observed_instance_mean_delta']:.4f}, 95% CI [{values[str(k)]['ci95'][0]:.4f}, {values[str(k)]['ci95'][1]:.4f}]" for k in K_VALUES) + ".")
    lines.extend(["", "## Failures and next gate", "", f"- Recorded protocol failures: {sum(1 for value in resources.values() if value['status'] != 'success')}.", "- Complete the remaining four seeds before confirmatory claims or canonical manuscript tables.", "- Preserve oracle-label only as a conditional upper-bound protocol.", "- Retain the title-audit caveat and consider redirect/content fingerprint auditing as an additional robustness check.", ""])
    report_path = args.pilot_root.parent / "W3_C2_PILOT_REPORT.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"passed": audit["passed"], "checks": len(checks), "failures": len(failures), "report": str(report_path)}, indent=2))
    return 0 if audit["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
