#!/usr/bin/env python3
"""Audit paired experiment artifacts and compute cluster-aware statistics.

The module deliberately has no project-specific column names.  MA-SQLGrid can
cluster by ``question_id`` (or a coarser database/domain identifier), while
C2GES can cluster by ``document_id``.  Only complete, unique pairs enter the
statistical analysis; the audit records everything that was excluded.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import random
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any, Iterable, Sequence


EMPTY = (None, "")
HEX_HASH = re.compile(r"^[0-9a-fA-F]{32,128}$")


@dataclass
class Issue:
    code: str
    severity: str
    count: int
    message: str
    examples: list[Any]


def _value(row: dict[str, Any], field: str) -> Any:
    value = row.get(field)
    if isinstance(value, str):
        value = value.strip()
    return value


def _key(row: dict[str, Any], fields: Sequence[str]) -> tuple[str, ...]:
    return tuple(str(_value(row, field)) for field in fields)


def load_records(path: Path) -> tuple[list[dict[str, Any]], str]:
    """Load UTF-8 CSV or JSONL records and return records plus detected format."""
    suffix = path.suffix.lower()
    if suffix in {".jsonl", ".ndjson"}:
        records: list[dict[str, Any]] = []
        with path.open("r", encoding="utf-8-sig") as handle:
            for line_no, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                value = json.loads(line)
                if not isinstance(value, dict):
                    raise ValueError(f"JSONL line {line_no} is not an object")
                records.append(value)
        return records, "jsonl"
    if suffix == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle)), "csv"
    raise ValueError(f"Unsupported input format {suffix!r}; use .csv, .jsonl, or .ndjson")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _limited(values: Iterable[Any], limit: int) -> list[Any]:
    result = []
    for value in values:
        if len(result) == limit:
            break
        result.append(value)
    return result


def audit_records(
    records: list[dict[str, Any]],
    *,
    condition_field: str,
    item_fields: Sequence[str],
    cluster_field: str,
    metric_fields: Sequence[str],
    required_fields: Sequence[str],
    hash_fields: Sequence[str],
    expected_conditions: Sequence[str] | None = None,
    max_examples: int = 20,
) -> dict[str, Any]:
    """Audit schema, Cartesian completeness, IDs, clusters, and hashes."""
    mandatory = list(dict.fromkeys(
        [condition_field, *item_fields, cluster_field, *metric_fields, *required_fields, *hash_fields]
    ))
    all_columns = set().union(*(row.keys() for row in records)) if records else set()
    missing_columns = [field for field in mandatory if field not in all_columns]
    issues: list[Issue] = []
    if missing_columns:
        issues.append(Issue(
            "missing_columns", "error", len(missing_columns),
            "Required columns are absent from the artifact.", missing_columns[:max_examples],
        ))

    blank_cells = []
    for index, row in enumerate(records, 1):
        for field in mandatory:
            if _value(row, field) in EMPTY:
                blank_cells.append({"row": index, "field": field})
    if blank_cells:
        issues.append(Issue(
            "missing_values", "error", len(blank_cells),
            "Required fields contain blank or null values.", blank_cells[:max_examples],
        ))

    observed_conditions = sorted({str(_value(row, condition_field)) for row in records
                                  if _value(row, condition_field) not in EMPTY})
    conditions = list(expected_conditions) if expected_conditions else observed_conditions
    unexpected = sorted(set(observed_conditions) - set(conditions))
    absent_conditions = sorted(set(conditions) - set(observed_conditions))
    if unexpected:
        issues.append(Issue(
            "unexpected_conditions", "error", len(unexpected),
            "Observed conditions are not in the expected condition list.", unexpected[:max_examples],
        ))
    if absent_conditions:
        issues.append(Issue(
            "absent_conditions", "error", len(absent_conditions),
            "Expected conditions are absent from the artifact.", absent_conditions[:max_examples],
        ))

    usable = [row for row in records if all(_value(row, f) not in EMPTY
                                             for f in [condition_field, *item_fields])]
    identity_counts = Counter((str(_value(row, condition_field)), *_key(row, item_fields)) for row in usable)
    duplicates = [{"condition_and_item": list(key), "count": count}
                  for key, count in identity_counts.items() if count > 1]
    if duplicates:
        issues.append(Issue(
            "duplicate_ids", "error", len(duplicates),
            "Condition-by-item identities must be unique.", duplicates[:max_examples],
        ))

    item_keys = sorted({_key(row, item_fields) for row in usable})
    observed_cells = set(identity_counts)
    missing_cells = [
        {"condition": condition, "item": list(item)}
        for condition in conditions for item in item_keys
        if (condition, *item) not in observed_cells
    ]
    if missing_cells:
        issues.append(Issue(
            "incomplete_cartesian_product", "error", len(missing_cells),
            "The expected condition × item Cartesian product is incomplete.",
            missing_cells[:max_examples],
        ))

    item_clusters: dict[tuple[str, ...], set[str]] = defaultdict(set)
    clusters_by_condition: dict[str, set[str]] = defaultdict(set)
    for row in records:
        if any(_value(row, f) in EMPTY for f in [condition_field, *item_fields, cluster_field]):
            continue
        item = _key(row, item_fields)
        cluster = str(_value(row, cluster_field))
        condition = str(_value(row, condition_field))
        item_clusters[item].add(cluster)
        clusters_by_condition[condition].add(cluster)
    multi_cluster = [{"item": list(item), "clusters": sorted(clusters)}
                     for item, clusters in item_clusters.items() if len(clusters) != 1]
    if multi_cluster:
        issues.append(Issue(
            "ambiguous_item_cluster", "error", len(multi_cluster),
            "Each item must map to exactly one cluster across all conditions.",
            multi_cluster[:max_examples],
        ))
    all_clusters = set().union(*clusters_by_condition.values()) if clusters_by_condition else set()
    cluster_gaps = []
    for condition in conditions:
        for cluster in sorted(all_clusters - clusters_by_condition.get(condition, set())):
            cluster_gaps.append({"condition": condition, "missing_cluster": cluster})
    if cluster_gaps:
        issues.append(Issue(
            "incomplete_cluster_coverage", "error", len(cluster_gaps),
            "Every condition must cover the same cluster set.", cluster_gaps[:max_examples],
        ))

    invalid_hashes = []
    inconsistent_hashes = []
    for field in hash_fields:
        hashes_by_item: dict[tuple[str, ...], set[str]] = defaultdict(set)
        for index, row in enumerate(records, 1):
            raw = _value(row, field)
            if raw in EMPTY:
                continue
            value = str(raw)
            if not HEX_HASH.fullmatch(value):
                invalid_hashes.append({"row": index, "field": field, "value": value})
            if all(_value(row, f) not in EMPTY for f in item_fields):
                hashes_by_item[_key(row, item_fields)].add(value.lower())
        for item, hashes in hashes_by_item.items():
            if len(hashes) > 1:
                inconsistent_hashes.append({
                    "field": field, "item": list(item), "hashes": sorted(hashes)
                })
    if invalid_hashes:
        issues.append(Issue(
            "invalid_hash_format", "error", len(invalid_hashes),
            "Hash fields must contain 32–128 hexadecimal characters.", invalid_hashes[:max_examples],
        ))
    if inconsistent_hashes:
        issues.append(Issue(
            "inconsistent_item_hash", "error", len(inconsistent_hashes),
            "Input/provenance hashes must be invariant across conditions for an item.",
            inconsistent_hashes[:max_examples],
        ))

    return {
        "passed": not any(issue.severity == "error" for issue in issues),
        "row_count": len(records),
        "item_count": len(item_keys),
        "cluster_count": len(all_clusters),
        "conditions": conditions,
        "observed_conditions": observed_conditions,
        "expected_cartesian_cells": len(conditions) * len(item_keys),
        "observed_unique_cells": len(observed_cells),
        "issues": [asdict(issue) for issue in issues],
    }


def _float(value: Any, field: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Metric {field!r} contains non-numeric value {value!r}") from exc
    if not math.isfinite(number):
        raise ValueError(f"Metric {field!r} contains non-finite value {value!r}")
    return number


def percentile(values: Sequence[float], probability: float) -> float:
    """Linear-interpolated percentile compatible with common statistical tools."""
    if not values:
        raise ValueError("Cannot calculate a percentile of an empty sequence")
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def paired_rows(
    records: list[dict[str, Any]], condition_field: str, item_fields: Sequence[str]
) -> dict[str, dict[tuple[str, ...], dict[str, Any]]]:
    """Index only unique condition-item records; duplicates are excluded."""
    buckets: dict[tuple[str, tuple[str, ...]], list[dict[str, Any]]] = defaultdict(list)
    for row in records:
        if any(_value(row, f) in EMPTY for f in [condition_field, *item_fields]):
            continue
        buckets[(str(_value(row, condition_field)), _key(row, item_fields))].append(row)
    indexed: dict[str, dict[tuple[str, ...], dict[str, Any]]] = defaultdict(dict)
    for (condition, item), rows in buckets.items():
        if len(rows) == 1:
            indexed[condition][item] = rows[0]
    return indexed


def cluster_paired_bootstrap(
    pairs: Sequence[tuple[float, float, str]], *, samples: int, confidence: float, seed: int
) -> dict[str, Any]:
    """Bootstrap paired treatment-minus-baseline differences by cluster.

    Clusters are sampled with replacement and all their paired observations are
    retained.  This preserves within-document/question dependence.
    """
    if not pairs:
        raise ValueError("No complete pairs available")
    grouped: dict[str, list[float]] = defaultdict(list)
    for baseline, treatment, cluster in pairs:
        grouped[cluster].append(treatment - baseline)
    clusters = sorted(grouped)
    rng = random.Random(seed)
    draws = []
    for _ in range(samples):
        sampled = [rng.choice(clusters) for _ in clusters]
        differences = [delta for cluster in sampled for delta in grouped[cluster]]
        draws.append(mean(differences))
    alpha = 1.0 - confidence
    differences = [delta for values in grouped.values() for delta in values]
    return {
        "estimate": mean(differences),
        "ci_low": percentile(draws, alpha / 2),
        "ci_high": percentile(draws, 1 - alpha / 2),
        "confidence": confidence,
        "bootstrap_samples": samples,
        "cluster_count": len(clusters),
        "pair_count": len(pairs),
        "seed": seed,
    }


def mcnemar_exact(pairs: Sequence[tuple[float, float, str]]) -> dict[str, Any]:
    """Two-sided exact McNemar test for paired binary outcomes."""
    binary = [(int(a), int(b)) for a, b, _ in pairs]
    if any(a not in (0, 1) or b not in (0, 1) for a, b in binary):
        return {"applicable": False, "reason": "metric_is_not_binary"}
    baseline_only = sum(a == 1 and b == 0 for a, b in binary)
    treatment_only = sum(a == 0 and b == 1 for a, b in binary)
    discordant = baseline_only + treatment_only
    if discordant == 0:
        p_value = 1.0
        engine = "degenerate_no_discordant_pairs"
    else:
        try:
            from scipy.stats import binomtest

            p_value = float(binomtest(treatment_only, discordant, 0.5, alternative="two-sided").pvalue)
            engine = "scipy.stats.binomtest"
        except ImportError:
            tail = sum(math.comb(discordant, k) for k in range(0, min(baseline_only, treatment_only) + 1))
            p_value = min(1.0, 2.0 * tail / (2 ** discordant))
            engine = "stdlib_exact_fallback"
    return {
        "applicable": True,
        "baseline_only_correct": baseline_only,
        "treatment_only_correct": treatment_only,
        "discordant_pairs": discordant,
        "p_value": p_value,
        "engine": engine,
    }


def holm_adjust(p_values: Sequence[float]) -> list[float]:
    """Holm step-down family-wise error adjustment in original order."""
    count = len(p_values)
    if count == 0:
        return []
    order = sorted(range(count), key=lambda index: p_values[index])
    adjusted = [0.0] * count
    running = 0.0
    for rank, index in enumerate(order):
        candidate = min(1.0, (count - rank) * p_values[index])
        running = max(running, candidate)
        adjusted[index] = running
    return adjusted


def compare_conditions(
    records: list[dict[str, Any]], *, condition_field: str, item_fields: Sequence[str],
    cluster_field: str, metric_fields: Sequence[str], conditions: Sequence[str],
    bootstrap_samples: int, confidence: float, seed: int,
) -> list[dict[str, Any]]:
    indexed = paired_rows(records, condition_field, item_fields)
    results = []
    for pair_index, (baseline, treatment) in enumerate(itertools.combinations(conditions, 2)):
        complete_items = sorted(set(indexed.get(baseline, {})) & set(indexed.get(treatment, {})))
        for metric_index, metric in enumerate(metric_fields):
            pairs = []
            invalid = []
            for item in complete_items:
                left = indexed[baseline][item]
                right = indexed[treatment][item]
                try:
                    left_value = _float(_value(left, metric), metric)
                    right_value = _float(_value(right, metric), metric)
                except ValueError as exc:
                    invalid.append({"item": list(item), "error": str(exc)})
                    continue
                left_cluster = str(_value(left, cluster_field))
                right_cluster = str(_value(right, cluster_field))
                if left_cluster != right_cluster or left_cluster in ("", "None"):
                    invalid.append({"item": list(item), "error": "cluster mismatch or missing cluster"})
                    continue
                pairs.append((left_value, right_value, left_cluster))
            result: dict[str, Any] = {
                "baseline": baseline,
                "treatment": treatment,
                "metric": metric,
                "complete_pair_count": len(pairs),
                "excluded_pair_count": len(invalid),
                "excluded_examples": invalid[:20],
            }
            if pairs:
                result["baseline_mean"] = mean(pair[0] for pair in pairs)
                result["treatment_mean"] = mean(pair[1] for pair in pairs)
                result["paired_cluster_bootstrap"] = cluster_paired_bootstrap(
                    pairs, samples=bootstrap_samples, confidence=confidence,
                    seed=seed + pair_index * 1009 + metric_index,
                )
                result["mcnemar_exact"] = mcnemar_exact(pairs)
            else:
                result["error"] = "no_complete_numeric_pairs"
            results.append(result)

    applicable = [result for result in results
                  if result.get("mcnemar_exact", {}).get("applicable")]
    adjusted = holm_adjust([result["mcnemar_exact"]["p_value"] for result in applicable])
    for result, adjusted_p in zip(applicable, adjusted):
        result["mcnemar_exact"]["p_value_holm"] = adjusted_p
    return results


def build_report(
    input_path: Path, records: list[dict[str, Any]], input_format: str, *,
    condition_field: str, item_fields: Sequence[str], cluster_field: str,
    metric_fields: Sequence[str], required_fields: Sequence[str], hash_fields: Sequence[str],
    expected_conditions: Sequence[str] | None, bootstrap_samples: int,
    confidence: float, seed: int, max_examples: int,
) -> dict[str, Any]:
    audit = audit_records(
        records, condition_field=condition_field, item_fields=item_fields,
        cluster_field=cluster_field, metric_fields=metric_fields,
        required_fields=required_fields, hash_fields=hash_fields,
        expected_conditions=expected_conditions, max_examples=max_examples,
    )
    conditions = audit["conditions"]
    comparisons = compare_conditions(
        records, condition_field=condition_field, item_fields=item_fields,
        cluster_field=cluster_field, metric_fields=metric_fields, conditions=conditions,
        bootstrap_samples=bootstrap_samples, confidence=confidence, seed=seed,
    ) if len(conditions) >= 2 else []
    return {
        "schema_version": "1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input": {
            "path": str(input_path.resolve()),
            "format": input_format,
            "sha256": sha256_file(input_path),
        },
        "configuration": {
            "condition_field": condition_field,
            "item_fields": list(item_fields),
            "cluster_field": cluster_field,
            "metric_fields": list(metric_fields),
            "required_fields": list(required_fields),
            "hash_fields": list(hash_fields),
            "expected_conditions": list(expected_conditions) if expected_conditions else None,
            "bootstrap_samples": bootstrap_samples,
            "confidence": confidence,
            "seed": seed,
        },
        "audit": audit,
        "comparisons": comparisons,
    }


def report_markdown(report: dict[str, Any]) -> str:
    audit = report["audit"]
    lines = [
        "# Experiment Artifact Audit and Paired Statistics",
        "",
        f"- Overall audit: **{'PASS' if audit['passed'] else 'FAIL'}**",
        f"- Input: `{report['input']['path']}`",
        f"- SHA-256: `{report['input']['sha256']}`",
        f"- Rows / items / clusters: {audit['row_count']} / {audit['item_count']} / {audit['cluster_count']}",
        f"- Conditions: {', '.join(audit['conditions']) or '(none)'}",
        f"- Cartesian cells (observed/expected): {audit['observed_unique_cells']}/{audit['expected_cartesian_cells']}",
        "",
        "## Audit findings",
        "",
    ]
    if not audit["issues"]:
        lines.append("No schema, completeness, identity, cluster, or hash defects were detected.")
    else:
        lines.extend(["| Severity | Code | Count | Finding |", "|---|---|---:|---|"])
        for issue in audit["issues"]:
            lines.append(
                f"| {issue['severity']} | `{issue['code']}` | {issue['count']} | {issue['message']} |"
            )
        lines.extend(["", "Detailed examples are retained in the machine-readable JSON report."])
    lines.extend(["", "## Paired comparisons", ""])
    if not report["comparisons"]:
        lines.append("No pairwise comparison was available.")
    else:
        lines.extend([
            "| Baseline | Treatment | Metric | Pairs | Delta | Bootstrap CI | McNemar p | Holm p |",
            "|---|---|---|---:|---:|---|---:|---:|",
        ])
        for result in report["comparisons"]:
            bootstrap = result.get("paired_cluster_bootstrap", {})
            mcnemar = result.get("mcnemar_exact", {})
            delta = bootstrap.get("estimate")
            interval = (f"[{bootstrap['ci_low']:.6g}, {bootstrap['ci_high']:.6g}]"
                        if bootstrap else "n/a")
            p_value = mcnemar.get("p_value") if mcnemar.get("applicable") else None
            adjusted = mcnemar.get("p_value_holm") if mcnemar.get("applicable") else None
            lines.append(
                f"| {result['baseline']} | {result['treatment']} | {result['metric']} | "
                f"{result['complete_pair_count']} | {delta:.6g} | {interval} | "
                f"{p_value:.6g} | {adjusted:.6g} |"
                if delta is not None and p_value is not None and adjusted is not None else
                f"| {result['baseline']} | {result['treatment']} | {result['metric']} | "
                f"{result['complete_pair_count']} | {delta if delta is not None else 'n/a'} | "
                f"{interval} | n/a | n/a |"
            )
    lines.extend([
        "", "## Interpretation contract", "",
        "Positive delta means treatment minus baseline. Confidence intervals use paired cluster "
        "resampling; McNemar is emitted only for binary paired outcomes. Holm adjustment spans "
        "all applicable pairwise metric tests in this report.", "",
    ])
    return "\n".join(lines)


def comma_list(value: str | None) -> list[str]:
    return [part.strip() for part in (value or "").split(",") if part.strip()]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit paired experiment CSV/JSONL and compute cluster-aware statistics."
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("--condition-field", default="condition")
    parser.add_argument("--item-fields", required=True,
                        help="Comma-separated pairing identity, e.g. question_id or instance_id,seed")
    parser.add_argument("--cluster-field", required=True,
                        help="Resampling cluster, e.g. question_id or document_id")
    parser.add_argument("--metrics", required=True, help="Comma-separated numeric outcome fields")
    parser.add_argument("--conditions", help="Comma-separated expected conditions; inferred if omitted")
    parser.add_argument("--required-fields", default="", help="Additional non-empty fields")
    parser.add_argument("--hash-fields", default="", help="Invariant per-item provenance hash fields")
    parser.add_argument("--bootstrap-samples", type=int, default=10_000)
    parser.add_argument("--confidence", type=float, default=0.95)
    parser.add_argument("--seed", type=int, default=20260805)
    parser.add_argument("--max-issue-examples", type=int, default=20)
    parser.add_argument("--json-out", type=Path, required=True)
    parser.add_argument("--markdown-out", type=Path, required=True)
    parser.add_argument("--allow-audit-fail", action="store_true",
                        help="Return zero even when strict artifact audit fails")
    args = parser.parse_args(argv)
    if args.bootstrap_samples <= 0:
        parser.error("--bootstrap-samples must be positive")
    if not 0 < args.confidence < 1:
        parser.error("--confidence must be between 0 and 1")
    return args


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    records, input_format = load_records(args.input)
    report = build_report(
        args.input, records, input_format,
        condition_field=args.condition_field,
        item_fields=comma_list(args.item_fields),
        cluster_field=args.cluster_field,
        metric_fields=comma_list(args.metrics),
        required_fields=comma_list(args.required_fields),
        hash_fields=comma_list(args.hash_fields),
        expected_conditions=comma_list(args.conditions) or None,
        bootstrap_samples=args.bootstrap_samples,
        confidence=args.confidence,
        seed=args.seed,
        max_examples=args.max_issue_examples,
    )
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.markdown_out.write_text(report_markdown(report), encoding="utf-8")
    print(f"audit={'PASS' if report['audit']['passed'] else 'FAIL'}")
    print(f"json={args.json_out}")
    print(f"markdown={args.markdown_out}")
    return 0 if report["audit"]["passed"] or args.allow_audit_fail else 2


if __name__ == "__main__":
    sys.exit(main())
