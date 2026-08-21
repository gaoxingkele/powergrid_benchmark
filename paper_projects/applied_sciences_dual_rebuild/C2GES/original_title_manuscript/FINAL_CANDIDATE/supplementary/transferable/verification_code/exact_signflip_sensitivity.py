#!/usr/bin/env python3
"""Exact report-level sign-flip sensitivity for the frozen C2GES v0.3.1 ledger.

This is an unregistered post-run sensitivity analysis. It reads the immutable
prediction ledger and never invokes a summarizer or changes a prediction.
The randomization distribution assumes joint sign symmetry of the 15 paired
report-level differences under each sharp null. That assumption is stated,
not inferred from the data.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
from collections import defaultdict
from pathlib import Path


CONTRASTS = (
    (5, "c2ges_full", "graph_no_cf_strict", "c2ges_full_minus_graph_no_cf_strict"),
    (5, "c2ges_full", "semantic_mmr", "c2ges_full_minus_semantic_mmr"),
    (5, "c2ges_full", "textrank", "c2ges_full_minus_textrank"),
    (10, "c2ges_full", "graph_no_cf_strict", "c2ges_full_minus_graph_no_cf_strict"),
    (10, "c2ges_full", "semantic_mmr", "c2ges_full_minus_semantic_mmr"),
    (10, "c2ges_full", "textrank", "c2ges_full_minus_textrank"),
)
METRIC = "rougeL_f1"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def load_ledger(path: Path) -> dict[tuple[str, int, str], float]:
    rows: dict[tuple[str, int, str], float] = {}
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            key = (row["doc_id"], int(row["budget"]), row["condition"])
            if key in rows:
                raise ValueError(f"duplicate ledger key at line {line_no}: {key}")
            rows[key] = float(row["metrics"][METRIC])
    return rows


def exact_signflip_p(deltas: list[float]) -> tuple[float, int, int]:
    """Return exact two-sided p, extreme count, and enumeration size.

    The statistic is the absolute arithmetic mean. All 2^n report-level sign
    assignments are enumerated, including the observed and global-negation
    assignments. The comparison is inclusive, so no Monte Carlo correction is
    involved.
    """
    if not deltas:
        raise ValueError("deltas must be non-empty")
    observed = abs(sum(deltas) / len(deltas))
    tol = 1e-15
    extreme = 0
    total = 1 << len(deltas)
    for bits in range(total):
        signed_sum = 0.0
        for i, delta in enumerate(deltas):
            signed_sum += delta if (bits >> i) & 1 else -delta
        if abs(signed_sum / len(deltas)) + tol >= observed:
            extreme += 1
    return extreme / total, extreme, total


def holm_adjust(p_values: list[float]) -> list[float]:
    """Holm adjusted p-values, returned in original order."""
    m = len(p_values)
    order = sorted(range(m), key=lambda i: (p_values[i], i))
    adjusted = [0.0] * m
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * p_values[i]))
        adjusted[i] = running
    return adjusted


def compute(ledger: dict[tuple[str, int, str], float]) -> list[dict]:
    by_budget_condition: dict[tuple[int, str], set[str]] = defaultdict(set)
    for doc_id, budget, condition in ledger:
        by_budget_condition[(budget, condition)].add(doc_id)

    results: list[dict] = []
    for budget, left, right, name in CONTRASTS:
        left_docs = by_budget_condition[(budget, left)]
        right_docs = by_budget_condition[(budget, right)]
        if left_docs != right_docs:
            raise ValueError(f"unpaired documents for K={budget}, {left} vs {right}")
        docs = sorted(left_docs)
        if len(docs) != 15:
            raise ValueError(f"expected 15 reports, got {len(docs)} for {name}, K={budget}")
        deltas = [ledger[(d, budget, left)] - ledger[(d, budget, right)] for d in docs]
        p, extreme, total = exact_signflip_p(deltas)
        eps = 1e-15
        signs = {
            "positive": sum(d > eps for d in deltas),
            "negative": sum(d < -eps for d in deltas),
            "tie": sum(abs(d) <= eps for d in deltas),
        }
        results.append(
            {
                "budget": budget,
                "contrast": name,
                "left_condition": left,
                "right_condition": right,
                "metric": METRIC,
                "n_reports": len(docs),
                "observed_mean_delta": sum(deltas) / len(deltas),
                "sign_counts": signs,
                "exact_two_sided_signflip_p": p,
                "extreme_assignments": extreme,
                "enumerated_assignments": total,
                "report_deltas": [
                    {"doc_id": doc_id, "delta": delta}
                    for doc_id, delta in zip(docs, deltas)
                ],
            }
        )
    adjusted = holm_adjust([r["exact_two_sided_signflip_p"] for r in results])
    for row, value in zip(results, adjusted):
        row["holm_adjusted_p_six_tests"] = value
    return results


def write_outputs(ledger_path: Path, out_dir: Path, results: list[dict]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    input_hash = sha256(ledger_path)
    envelope = {
        "analysis_id": "C2GES-v0.3.1-unregistered-postrun-exact-signflip-v1",
        "status": "unregistered_post_run_sensitivity_not_confirmatory",
        "input": {
            "path_label": "formal_runs_v0_3_1/c2ges_v031_formal_20260808/predictions.jsonl",
            "sha256": input_hash,
            "row_count_expected": 210,
        },
        "data_use": {
            "prediction_generation_calls": 0,
            "formal_test_rerun": False,
            "test_hyperparameter_selection": False,
        },
        "method": {
            "unit": "report",
            "statistic": "absolute mean paired ROUGE-L difference",
            "enumeration": "all 2^15 report-level sign assignments per contrast",
            "two_sided_rule": "Pr(|T_signflip| >= |T_observed|), inclusive",
            "assumption": "joint sign symmetry/exchangeability of paired report-level differences under each sharp null",
            "assumption_status": "stated sensitivity assumption; not established by n=15 data",
            "multiplicity": "Holm step-down adjustment over the same six contrasts",
        },
        "results": results,
    }
    json_path = out_dir / "exact_signflip_results.json"
    json_path.write_text(json.dumps(envelope, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    csv_path = out_dir / "exact_signflip_results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        fields = [
            "budget", "contrast", "metric", "n_reports", "observed_mean_delta",
            "positive", "negative", "tie", "exact_two_sided_signflip_p",
            "holm_adjusted_p_six_tests", "extreme_assignments", "enumerated_assignments",
        ]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in results:
            w.writerow({
                "budget": row["budget"], "contrast": row["contrast"],
                "metric": row["metric"], "n_reports": row["n_reports"],
                "observed_mean_delta": format(row["observed_mean_delta"], ".17g"),
                **row["sign_counts"],
                "exact_two_sided_signflip_p": format(row["exact_two_sided_signflip_p"], ".17g"),
                "holm_adjusted_p_six_tests": format(row["holm_adjusted_p_six_tests"], ".17g"),
                "extreme_assignments": row["extreme_assignments"],
                "enumerated_assignments": row["enumerated_assignments"],
            })

    report = [
        "# Exact Report-Level Sign-Flip Sensitivity",
        "",
        "**Status:** unregistered post-run sensitivity; not confirmatory and not a replacement for the registered percentile intervals.",
        "",
        f"**Frozen input SHA-256:** `{input_hash}` (`predictions.jsonl`, expected 210 rows).",
        "",
        "No prediction was regenerated and no test hyperparameter was selected. For each of the same six contrasts, all $2^{15}=32,768$ report-level sign assignments were enumerated. The two-sided statistic is the absolute mean paired ROUGE-L difference. This randomization interpretation requires joint sign symmetry/exchangeability of the paired report-level differences under the sharp null; that assumption is a sensitivity assumption and is not established by the 15 reports. Holm adjustment spans all six values.",
        "",
        "| K | Contrast | Mean delta | Signs +/-/= | Exact two-sided p | Holm (6) |",
        "|---:|---|---:|---:|---:|---:|",
    ]
    for row in results:
        s = row["sign_counts"]
        report.append(
            f"| {row['budget']} | `{row['contrast']}` | {row['observed_mean_delta']:.6f} | "
            f"{s['positive']}/{s['negative']}/{s['tie']} | {row['exact_two_sided_signflip_p']:.6f} | "
            f"{row['holm_adjusted_p_six_tests']:.6f} |"
        )
    report += [
        "",
        "The registered bootstrap sign-tail quantities remain frozen machine outputs. Because their resampling distribution is centered at the observed empirical distribution rather than generated under a null, they are descriptive tail summaries, not null-calibrated p-values. Holm adjustment of those descriptive quantities does not convert them into hypothesis-test p-values.",
        "",
    ]
    (out_dir / "EXACT_SIGNFLIP_REPORT.md").write_text("\n".join(report), encoding="utf-8")

    manifest = {
        "analysis_id": envelope["analysis_id"],
        "input_sha256": input_hash,
        "output_sha256": {
            p.name: sha256(p) for p in (json_path, csv_path, out_dir / "EXACT_SIGNFLIP_REPORT.md")
        },
    }
    (out_dir / "OUTPUT_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("predictions", type=Path)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("--expected-sha256")
    args = parser.parse_args()
    if args.expected_sha256 and sha256(args.predictions) != args.expected_sha256.upper():
        raise SystemExit("input SHA-256 mismatch; refusing analysis")
    ledger = load_ledger(args.predictions)
    if len(ledger) != 210:
        raise SystemExit(f"expected 210 unique prediction rows, got {len(ledger)}")
    results = compute(ledger)
    write_outputs(args.predictions, args.out_dir, results)


if __name__ == "__main__":
    main()
