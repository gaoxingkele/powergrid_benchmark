#!/usr/bin/env python3
"""Deterministic distribution and validity gates for synthetic C2GES data."""

from __future__ import annotations

import argparse
import json
import math
import statistics
from collections import Counter
from pathlib import Path

from generate_deepseek_synthetic import CORE_ROLES, UNIT_TYPES, read_numeric_rows, validate_dataset, words


def quantile(values: list[float], p: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    position = (len(ordered) - 1) * p
    lo, hi = math.floor(position), math.ceil(position)
    if lo == hi:
        return ordered[lo]
    return ordered[lo] * (hi - position) + ordered[hi] * (position - lo)


def normalized_w1(left: list[float], right: list[float]) -> float:
    ps = [(i + 0.5) / 100 for i in range(100)]
    distance = statistics.mean(abs(quantile(left, p) - quantile(right, p)) for p in ps)
    scale = max(1.0, quantile(right, .75) - quantile(right, .25))
    return distance / scale


def ks_distance(left: list[float], right: list[float]) -> float:
    support = sorted(set(left + right))
    return max(abs(sum(x <= point for x in left) / len(left) - sum(x <= point for x in right) / len(right)) for point in support)


def describe(values: list[float]) -> dict[str, float]:
    return {"n": len(values), "mean": statistics.mean(values), "median": statistics.median(values),
            "q25": quantile(values, .25), "q75": quantile(values, .75), "min": min(values), "max": max(values)}


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def evaluate(rows: list[dict], real: list[dict]) -> dict:
    validity = validate_dataset(rows)
    syn_metrics = {
        "candidate_count": [len(row["candidate_sentences"]) for row in rows],
        "page_count": [max(unit["page"] for unit in row["candidate_sentences"]) for row in rows],
        "reference_words": [words(row["reference_summary"]) for row in rows],
    }
    real_metrics = {name: [profile[name] for profile in real] for name in syn_metrics}
    distances = {name: {"normalized_w1": normalized_w1(syn_metrics[name], real_metrics[name]),
                        "ks": ks_distance(syn_metrics[name], real_metrics[name]),
                        "synthetic": describe(syn_metrics[name]), "anchor": describe(real_metrics[name])}
                 for name in syn_metrics}
    observed_types = Counter(unit["unit_type"] for row in rows for unit in row["candidate_sentences"])
    anchor_types = Counter({kind: sum(profile[kind] for profile in real) for kind in UNIT_TYPES})
    obs_total, anchor_total = sum(observed_types.values()), sum(anchor_types.values())
    type_smd = {kind: abs(observed_types[kind] / obs_total - anchor_types[kind] / anchor_total) for kind in UNIT_TYPES}
    texts = [unit["text"].casefold() for row in rows for unit in row["candidate_sentences"]]
    exact_duplicate_rate = 1 - len(set(texts)) / len(texts)
    role_failures = sum(any(Counter(u["synthetic_ground_truth_role"] for u in row["candidate_sentences"])[role] < 1
                            for role in CORE_ROLES) for row in rows)
    gates = {
        "schema_and_extractive_validity": validity["two_reports_per_series"],
        "candidate_count_distribution_w1_le_0_75": distances["candidate_count"]["normalized_w1"] <= .75,
        "page_count_distribution_w1_le_0_75": distances["page_count"]["normalized_w1"] <= .75,
        "unit_type_max_proportion_gap_le_0_03": max(type_smd.values()) <= .03,
        "exact_duplicate_rate_le_0_20": exact_duplicate_rate <= .20,
        "all_roles_present": role_failures == 0,
    }
    return {
        "schema": "c2ges-synthetic-distribution-evaluation-v1", "synthetic": True,
        "confirmatory_claims_allowed": False, "validity": validity, "distances": distances,
        "unit_type_absolute_proportion_gaps": type_smd, "exact_duplicate_rate": exact_duplicate_rate,
        "role_failure_reports": role_failures, "gate_ledger": gates,
        "deterministic_gate_pass": all(gates.values()),
        "interpretation_boundary": "Passing means alignment on listed observables only; it is not evidence of semantic realism or external validity.",
        "reference_words_note": "Reported diagnostically, not gated: synthetic references are intentionally constrained to 110--180 words."
    }


def make_critic_packet(rows: list[dict], evaluation: dict) -> dict:
    samples = []
    for row in rows:
        core = [u for u in row["candidate_sentences"] if "deepseek_semantic_core" in u["synthetic_stress_tags"]]
        distractors = [u for u in row["candidate_sentences"] if "deterministic_layout_distractor" in u["synthetic_stress_tags"]][:8]
        samples.append({"doc_id": row["doc_id"], "lexical_regime": row["lexical_regime"],
                        "semantic_core": core, "distractor_sample": distractors,
                        "reference_summary": row["reference_summary"]})
    return {"schema": "c2ges-codex-blind-critic-packet-v1", "contains_real_report_text": False,
            "contains_manuscript_text": False, "synthetic": True,
            "aggregate_distribution_evaluation": evaluation, "synthetic_samples": samples}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--metadata-csv", type=Path, required=True)
    parser.add_argument("--layout-csv", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = load_jsonl(args.dataset)
    result = evaluate(rows, read_numeric_rows(args.metadata_csv, args.layout_csv))
    args.output.mkdir(parents=True, exist_ok=True)
    evaluation_path = args.output / "distribution_evaluation.json"
    evaluation_path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    packet = make_critic_packet(rows, result)
    (args.output / "codex_critic_packet.json").write_text(json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS" if result["deterministic_gate_pass"] else "FAIL",
                      "evaluation": str(evaluation_path), "gates": result["gate_ledger"]}))


if __name__ == "__main__":
    main()
