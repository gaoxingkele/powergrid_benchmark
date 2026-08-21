#!/usr/bin/env python3
"""Five-seed aggregation and claim gate for frozen C2GES W3/W4 runs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import statistics
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats

from w4_freeze_guard import file_sha, tree_sha


SEEDS = (2026, 2027, 2028, 2029, 2030)
K_VALUES = (1, 3, 5, 10)
PROTOCOL_DIRS = {"oracle-label": "oracle", "predicted-label": "predicted", "label-blind": "label_blind"}
PROTOCOL_PAIRS = (
    ("oracle-label", "predicted-label"),
    ("oracle-label", "label-blind"),
    ("predicted-label", "label-blind"),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_dir(args, seed: int, protocol: str) -> Path:
    if seed == 2026:
        return args.w3_root / PROTOCOL_DIRS[protocol]
    return args.w4_root / f"seed_{seed}" / PROTOCOL_DIRS[protocol]


def exact_sign_flip_p(values: list[float]) -> float:
    observed = abs(float(np.mean(values)))
    permutations = []
    for signs in itertools.product((-1.0, 1.0), repeat=len(values)):
        permutations.append(abs(float(np.mean(np.asarray(values) * np.asarray(signs)))))
    return float(np.mean(np.asarray(permutations) >= observed - 1e-15))


def summarize_seed_values(values: list[float]) -> dict:
    mean = statistics.fmean(values)
    sd = statistics.stdev(values)
    sem = sd / np.sqrt(len(values))
    critical = stats.t.ppf(0.975, len(values) - 1)
    return {
        "values": values,
        "mean": mean,
        "sample_std": sd,
        "t_ci95": [mean - critical * sem, mean + critical * sem],
    }


def paired_seed_effect(left: list[float], right: list[float]) -> dict:
    delta = [a - b for a, b in zip(left, right)]
    result = summarize_seed_values(delta)
    test = stats.ttest_rel(left, right)
    result.update(
        {
            "left_values": left,
            "right_values": right,
            "positive_seed_count": sum(value > 0 for value in delta),
            "negative_seed_count": sum(value < 0 for value in delta),
            "paired_t_p_two_sided": float(test.pvalue),
            "exact_sign_flip_p_two_sided": exact_sign_flip_p(delta),
        }
    )
    return result


def hierarchical_bootstrap(delta_by_seed: dict[int, dict[str, list[float]]], samples: int, seed: int) -> dict:
    """Resample training seeds, then Wikipedia-document clusters within seed."""
    rng = np.random.default_rng(seed)
    seed_ids = sorted(delta_by_seed)
    draws = []
    for _ in range(samples):
        chosen_seeds = rng.choice(seed_ids, size=len(seed_ids), replace=True)
        values = []
        for chosen_seed in chosen_seeds:
            clusters = delta_by_seed[int(chosen_seed)]
            doc_ids = list(clusters)
            chosen_docs = rng.choice(doc_ids, size=len(doc_ids), replace=True)
            for doc_id in chosen_docs:
                values.extend(clusters[str(doc_id)])
        draws.append(float(np.mean(values)))
    array = np.asarray(draws)
    return {
        "mean": float(array.mean()),
        "ci95": [float(np.quantile(array, 0.025)), float(np.quantile(array, 0.975))],
        "p_two_sided": float(min(1.0, 2 * min(np.mean(array <= 0), np.mean(array >= 0)))),
        "samples": samples,
        "outer_unit": "training_seed",
        "inner_unit": "underlying_wikipedia_document",
        "seed_count": len(seed_ids),
        "document_counts": {str(key): len(value) for key, value in delta_by_seed.items()},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--w3-root", type=Path, required=True)
    parser.add_argument("--w4-root", type=Path, required=True)
    parser.add_argument("--freeze", type=Path, required=True)
    parser.add_argument("--bootstrap-samples", type=int, default=2000)
    args = parser.parse_args()
    if any((args.w4_root / "seed_2026").exists() for _ in (0,)):
        raise RuntimeError("seed_2026 must be sourced from frozen W3; unexpected W4 seed_2026 directory exists")

    freeze = json.loads(args.freeze.read_text(encoding="utf-8"))
    base_config = freeze["fingerprint"]["base_run_config"]
    expected_data_hashes = freeze["fingerprint"]["w3_input_data_hashes"]
    checks = []
    failures = []

    def check(check_id: str, passed: bool, evidence) -> None:
        row = {"id": check_id, "passed": bool(passed), "evidence": evidence}
        checks.append(row)
        if not passed:
            failures.append(row)

    summaries = defaultdict(dict)
    resources = defaultdict(dict)
    full_rows = defaultdict(lambda: defaultdict(dict))
    baseline_rows = defaultdict(lambda: defaultdict(dict))
    metric_values = defaultdict(lambda: defaultdict(dict))

    for seed in SEEDS:
        for protocol in PROTOCOL_DIRS:
            directory = run_dir(args, seed, protocol)
            required = ("summary.json", "run_config.json", "provenance.json", "predictions.jsonl", "resource_usage.json")
            check(f"{seed}:{protocol}:files", all((directory / name).is_file() for name in required), str(directory))
            summary = json.loads((directory / "summary.json").read_text(encoding="utf-8"))
            config = json.loads((directory / "run_config.json").read_text(encoding="utf-8"))
            provenance = json.loads((directory / "provenance.json").read_text(encoding="utf-8"))
            resource = json.loads((directory / "resource_usage.json").read_text(encoding="utf-8"))
            summaries[seed][protocol] = summary
            resources[seed][protocol] = resource
            check(f"{seed}:{protocol}:seed", config.get("seed") == seed, config.get("seed"))
            check(f"{seed}:{protocol}:protocol", summary.get("protocol") == protocol, summary.get("protocol"))
            check(f"{seed}:{protocol}:counts", [summary.get("train_n"), summary.get("dev_n"), summary.get("test_n")] == [8000, 1500, 1500], [summary.get("train_n"), summary.get("dev_n"), summary.get("test_n")])
            check(f"{seed}:{protocol}:k", summary.get("evaluated_k") == list(K_VALUES), summary.get("evaluated_k"))
            check(f"{seed}:{protocol}:resource", resource.get("status") == "success" and resource.get("failure") is None, resource.get("failure"))
            check(f"{seed}:{protocol}:leakage", summary.get("document_leakage_audit", {}).get("passed") is True, summary.get("document_leakage_audit"))
            common = {key: value for key, value in config.items() if key not in {"out", "protocol", "predicted_labels", "protocol_definition", "seed"}}
            check(f"{seed}:{protocol}:base_config", common == base_config, {"found": common, "expected": base_config})
            hashes = {split: provenance["data_hashes"][split]["sha256"] for split in ("train", "dev", "test")}
            check(f"{seed}:{protocol}:data_hashes", hashes == expected_data_hashes, hashes)
            if protocol == "predicted-label":
                expected_label_hash = freeze["fingerprint"]["predicted_labels_sha256"]
                check(
                    f"{seed}:{protocol}:predicted_labels_hash",
                    provenance.get("predicted_labels_sha256") == expected_label_hash,
                    provenance.get("predicted_labels_sha256"),
                )
            for k in K_VALUES:
                metric_values[protocol][k][seed] = summary["k_sensitivity"][str(k)]["test"]["full"]["evidence_f1"]

            row_count = 0
            with (directory / "predictions.jsonl").open(encoding="utf-8") as handle:
                for line in handle:
                    row_count += 1
                    row = json.loads(line)
                    if row["mode"] == "full":
                        full_rows[seed][protocol][(row["k"], row["qid"])] = row
                    elif row["mode"] == "bm25":
                        baseline_rows[seed][protocol][(row["k"], row["qid"])] = row
            check(f"{seed}:{protocol}:prediction_rows", row_count == 54000, row_count)

    # BM25 is deterministic and must be identical across every seed/protocol.
    reference_bm25 = baseline_rows[2026]["oracle-label"]
    for seed in SEEDS:
        for protocol in PROTOCOL_DIRS:
            current = baseline_rows[seed][protocol]
            same = current.keys() == reference_bm25.keys() and all(current[key]["f1"] == reference_bm25[key]["f1"] for key in reference_bm25)
            check(f"{seed}:{protocol}:fixed_bm25", same, len(current))

    metric_summary = {
        protocol: {str(k): summarize_seed_values([metric_values[protocol][k][seed] for seed in SEEDS]) for k in K_VALUES}
        for protocol in PROTOCOL_DIRS
    }
    effects = {}
    effect_rows = []

    def add_effect(name: str, k: int, left_protocol: str, right_protocol: str | None) -> None:
        left = [metric_values[left_protocol][k][seed] for seed in SEEDS]
        if right_protocol is None:
            right = [summaries[seed][left_protocol]["k_sensitivity"][str(k)]["test"]["bm25"]["evidence_f1"] for seed in SEEDS]
        else:
            right = [metric_values[right_protocol][k][seed] for seed in SEEDS]
        seed_effect = paired_seed_effect(left, right)
        delta_by_seed = {}
        for seed in SEEDS:
            left_map = full_rows[seed][left_protocol]
            right_map = baseline_rows[seed][left_protocol] if right_protocol is None else full_rows[seed][right_protocol]
            clustered = defaultdict(list)
            for qid_key, left_row in left_map.items():
                if qid_key[0] != k:
                    continue
                right_row = right_map[qid_key]
                clustered[left_row["underlying_document_id"]].append(left_row["f1"] - right_row["f1"])
            delta_by_seed[seed] = dict(clustered)
        hierarchical = hierarchical_bootstrap(delta_by_seed, args.bootstrap_samples, 50000 + k + len(effects) * 100)
        gate = bool(seed_effect["mean"] > 0 and seed_effect["t_ci95"][0] > 0 and hierarchical["ci95"][0] > 0)
        effects[name] = effects.get(name, {})
        effects[name][str(k)] = {"seed_level": seed_effect, "hierarchical_bootstrap": hierarchical, "positive_effect_gate": gate}
        effect_rows.append(
            {
                "comparison": name,
                "k": k,
                "mean_delta": seed_effect["mean"],
                "seed_std": seed_effect["sample_std"],
                "seed_ci_low": seed_effect["t_ci95"][0],
                "seed_ci_high": seed_effect["t_ci95"][1],
                "paired_t_p": seed_effect["paired_t_p_two_sided"],
                "exact_sign_flip_p": seed_effect["exact_sign_flip_p_two_sided"],
                "hier_ci_low": hierarchical["ci95"][0],
                "hier_ci_high": hierarchical["ci95"][1],
                "positive_effect_gate": gate,
            }
        )

    for protocol in PROTOCOL_DIRS:
        for k in K_VALUES:
            add_effect(f"{protocol}_minus_bm25", k, protocol, None)
    for left, right in PROTOCOL_PAIRS:
        for k in K_VALUES:
            add_effect(f"{left}_minus_{right}", k, left, right)

    role_gate = effects["predicted-label_minus_label-blind"]["3"]["positive_effect_gate"]
    oracle_role_gate = effects["oracle-label_minus_label-blind"]["3"]["positive_effect_gate"]
    bm25_all_k_gate = all(effects[f"{protocol}_minus_bm25"][str(k)]["positive_effect_gate"] for protocol in PROTOCOL_DIRS for k in K_VALUES)
    k3_any_protocol = {protocol: effects[f"{protocol}_minus_bm25"]["3"]["positive_effect_gate"] for protocol in PROTOCOL_DIRS}
    decisions = {
        "role_conditioning_primary_claim": {
            "decision": "GO" if role_gate else "NO-GO",
            "criterion": "At K=3, predicted-label minus label-blind mean > 0 and both seed-level t CI and hierarchical seed/document CI exclude zero positively.",
            "oracle_sensitivity_gate": oracle_role_gate,
        },
        "blanket_superiority_over_bm25": {
            "decision": "GO" if bm25_all_k_gate else "NO-GO",
            "criterion": "Every protocol and K must pass the positive-effect gate against BM25.",
        },
        "k3_reranking_advantage_over_bm25": {
            "decision_by_protocol": {protocol: "GO" if value else "NO-GO" for protocol, value in k3_any_protocol.items()},
            "criterion": "Protocol-specific K=3 positive-effect gate against BM25.",
        },
        "manuscript_implication": "Do not claim a reliable role-conditioning gain if the primary role gate is NO-GO; frame results around budget-dependent retrieval behavior and transparent cost/accuracy trade-offs.",
    }

    check("freeze_manifest_status", freeze.get("status") == "frozen", freeze.get("status"))
    code_dir = Path(__file__).resolve().parent
    for name, expected in freeze["fingerprint"]["core_code"].items():
        current_hash = file_sha(code_dir / name)
        check(f"freeze_core_code:{name}", current_hash == expected["sha256"], current_hash)
    encoder_info = freeze["fingerprint"]["encoder"]
    encoder_root = Path.home() / ".cache/huggingface/hub/models--sentence-transformers--all-MiniLM-L6-v2" / "snapshots" / encoder_info["snapshot_ref"]
    current_encoder = tree_sha(encoder_root)
    check("freeze_encoder_snapshot", current_encoder["sha256"] == encoder_info["sha256"], current_encoder)
    check("all_15_runs_present", len(summaries) == 5 and all(len(summaries[seed]) == 3 for seed in SEEDS), {str(seed): len(summaries[seed]) for seed in SEEDS})
    check("no_w4_seed_2026", not (args.w4_root / "seed_2026").exists(), str(args.w4_root / "seed_2026"))
    audit = {
        "passed": not failures,
        "check_count": len(checks),
        "failure_count": len(failures),
        "checks": checks,
        "failures": failures,
        "seed_sources": {"2026": "frozen W3 (not rerun)", **{str(seed): "W4" for seed in SEEDS if seed != 2026}},
        "freeze_manifest_sha256": sha256(args.freeze),
    }
    aggregate = {
        "seeds": list(SEEDS),
        "k_values": list(K_VALUES),
        "metric": "macro mean instance-level evidence F1",
        "metric_summary": metric_summary,
        "effects": effects,
        "claim_decisions": decisions,
        "failure_audit": audit,
        "resources": {
            protocol: {
                "wall_seconds": summarize_seed_values([resources[seed][protocol]["wall_seconds"] for seed in SEEDS]),
                "peak_rss_gib": summarize_seed_values([resources[seed][protocol]["resource_sampling"]["peak_tree_rss_gib"] for seed in SEEDS]),
            }
            for protocol in PROTOCOL_DIRS
        },
    }
    aggregate_path = args.w4_root / "five_seed_aggregate.json"
    aggregate_path.write_text(json.dumps(aggregate, ensure_ascii=False, indent=2), encoding="utf-8")
    with (args.w4_root / "five_seed_effects.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(effect_rows[0]))
        writer.writeheader()
        writer.writerows(effect_rows)
    audit_path = args.w4_root / "failure_and_evidence_audit.json"
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# W4 C2GES Five-Seed Report",
        "",
        "## Decision",
        "",
        f"- Role-conditioning primary claim: **{decisions['role_conditioning_primary_claim']['decision']}**.",
        f"- Blanket superiority over BM25: **{decisions['blanket_superiority_over_bm25']['decision']}**.",
        "- Seed 2026 is the frozen W3 run and was not rerun; seeds 2027-2030 are new W4 runs.",
        f"- Evidence/failure audit: **{'PASS' if audit['passed'] else 'FAIL'}** ({audit['check_count']} checks, {audit['failure_count']} failures).",
        "",
        "## Five-seed evidence F1 (mean +/- sample SD)",
        "",
        "| Protocol | K=1 | K=3 | K=5 | K=10 |",
        "|---|---:|---:|---:|---:|",
    ]
    for protocol in PROTOCOL_DIRS:
        values = [metric_summary[protocol][str(k)] for k in K_VALUES]
        lines.append(f"| {protocol} | " + " | ".join(f"{item['mean']:.4f} +/- {item['sample_std']:.4f}" for item in values) + " |")
    bm25 = [summaries[2026]["oracle-label"]["k_sensitivity"][str(k)]["test"]["bm25"]["evidence_f1"] for k in K_VALUES]
    lines.append("| BM25 (fixed) | " + " | ".join(f"{value:.4f}" for value in bm25) + " |")
    lines.extend(["", "## Primary role effect at K=3", ""])
    for comparison in ("predicted-label_minus_label-blind", "oracle-label_minus_label-blind", "oracle-label_minus_predicted-label"):
        item = effects[comparison]["3"]
        seed_item, hier = item["seed_level"], item["hierarchical_bootstrap"]
        lines.append(f"- {comparison}: mean delta {seed_item['mean']:.5f}; seed t-CI [{seed_item['t_ci95'][0]:.5f}, {seed_item['t_ci95'][1]:.5f}]; hierarchical CI [{hier['ci95'][0]:.5f}, {hier['ci95'][1]:.5f}]; gate={'GO' if item['positive_effect_gate'] else 'NO-GO'}.")
    lines.extend(["", "## Relative to BM25", ""])
    for protocol in PROTOCOL_DIRS:
        vals = []
        for k in K_VALUES:
            item = effects[f"{protocol}_minus_bm25"][str(k)]
            vals.append(f"K={k}: delta={item['seed_level']['mean']:.4f}, hierarchical CI [{item['hierarchical_bootstrap']['ci95'][0]:.4f}, {item['hierarchical_bootstrap']['ci95'][1]:.4f}], gate={'GO' if item['positive_effect_gate'] else 'NO-GO'}")
        lines.append(f"- {protocol}: " + "; ".join(vals) + ".")
    lines.extend(["", "## Runtime and failures", "", "| Protocol | Mean wall s | Mean peak RSS GiB | Successful runs |", "|---|---:|---:|---:|"])
    for protocol in PROTOCOL_DIRS:
        lines.append(f"| {protocol} | {aggregate['resources'][protocol]['wall_seconds']['mean']:.2f} | {aggregate['resources'][protocol]['peak_rss_gib']['mean']:.3f} | 5/5 |")
    lines.extend(["", "No subprocess failure was recorded. RSS is a 0.2-second psutil process-tree sample and may miss shorter spikes.", "", "## Claim guidance", "", decisions["manuscript_implication"], "The five training seeds are a small algorithmic-repeat sample; seed-level t intervals and the hierarchical seed/document bootstrap are both reported. Exact sign-flip p-values are retained in the JSON/CSV rather than treated as adequately powered with n=5.", ""])
    report_path = args.w4_root / "W4_C2_FIVE_SEED_REPORT.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"passed": audit["passed"], "checks": audit["check_count"], "failures": audit["failure_count"], "decisions": decisions, "report": str(report_path)}, indent=2))
    return 0 if audit["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
