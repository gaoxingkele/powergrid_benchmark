"""Supplementary Tables S14-S16: reviewer-requested descriptive addenda (round 2).

These answer four open items from the paperreview.ai round that are computable
from artifacts already inside the release scope.  They are **descriptive**: no
new hypothesis test, no new Holm family, no re-tuning, and no third-party text.

  S14 (R1-Q5)  reservations x path 2x2 main effects and interaction, exact values
               with cluster-bootstrap intervals and per-series deltas
  S15 (R1-Q9)  external prospective corpus stratified by publisher family
               (never pooled across families)
  S16 (R1-Q3)  measured per-report cost against candidate-set size
      (R1-Q4)  per-report role and typed-edge coverage, redundancy, unit counts

Usage:
    python -B run_descriptive_addenda_v2.py
"""

from __future__ import annotations

import csv
import hashlib
import json
import statistics
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
DATA = PROJECT / "03_Reproducibility" / "Data"
OUT = DATA / "descriptive_addenda_v2"

INTERACTIONS = DATA / "exploratory_external_v0/e3_factorial_exploratory_v3/factorial_interactions.json"
ITEM_METRICS = DATA / "exploratory_external_v0/e3_factorial_exploratory_v3/factorial_item_metrics.csv"
PRIVATE_REPORTS = DATA / "exploratory_external_v0/derived_private/exploratory_reports_v3.jsonl"
EXTERNAL_ARMS = DATA / "external_prospective_v1/external_arms_v3.json"
EXTERNAL_CORPUS = DATA / "external_prospective_v1/external_prospective_v2_expanded.json"

FAMILY_LABEL = {
    "entsoe_grid": "ENTSO-E grid incidents",
    "entsoe_market": "ENTSO-E market-coupling incidents",
    "nerc": "NERC event reports",
    "other": "ENTSO-E frequency-deviation reports",
}
CONDITIONS = ("AB0", "AB2", "no_path", "Full", "TextRank", "Lead")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    """Write a derived table, refusing any field long enough to be corpus text.

    This table lives inside the release scope, so a field that accidentally holds a
    candidate list or a passage is a redistribution-boundary violation, not just a
    formatting bug.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    for row in rows:
        for field in fields:
            value = row.get(field)
            if isinstance(value, str) and len(value) > 400:
                raise AssertionError(f"{path.name}:{field} looks like corpus text ({len(value)} chars)")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def table_s14() -> tuple[list[dict], list[dict]]:
    payload = json.loads(INTERACTIONS.read_text(encoding="utf-8"))
    blocks = (
        ("path_main", "path channel (paths off vs on)"),
        ("reservation_main", "role-group reservation (on vs off)"),
        ("reservation_by_path_interaction", "reservation x path interaction"),
    )
    effects, deltas = [], []
    for key, label in blocks:
        for item in payload[key]:
            effects.append(
                {
                    "factor": label,
                    "word_budget": item["word_budget"],
                    "series": item["n_series"],
                    "mean_delta_rougeL": round(item["mean_delta"], 6),
                    "cluster_bootstrap_95_low": round(item["cluster_bootstrap_95"][0], 6),
                    "cluster_bootstrap_95_high": round(item["cluster_bootstrap_95"][1], 6),
                    "paired_smd": round(item["paired_standardized_mean_difference"], 3),
                    "exact_series_signflip_p": item["exact_series_signflip_p"],
                    "holm_adjusted_p": item["holm_adjusted_p"],
                    "holm_family_size": item["holm_family_size"],
                    "bootstrap_samples": item["bootstrap_samples"],
                    "bootstrap_seed": item["bootstrap_seed"],
                }
            )
            for series, value in sorted(item["series_deltas"].items()):
                deltas.append(
                    {
                        "factor": label,
                        "word_budget": item["word_budget"],
                        "series": series,
                        "delta_rougeL": round(value, 6),
                    }
                )
    return effects, deltas


def table_s15() -> tuple[list[dict], list[dict]]:
    arms = json.loads(EXTERNAL_ARMS.read_text(encoding="utf-8"))
    corpus = json.loads(EXTERNAL_CORPUS.read_text(encoding="utf-8"))
    meta = {d["doc_id"]: d for d in corpus["kept_documents"]}
    cells: dict[tuple[str, str], dict[str, dict]] = defaultdict(dict)
    for row in arms["rows"]:
        cells[(row["doc_id"], row["key"])][row["condition"]] = row

    families = sorted({d["family"] for d in corpus["kept_documents"]})
    means, contrasts = [], []
    for family in families:
        docs = [d["doc_id"] for d in corpus["kept_documents"] if d["family"] == family]
        for key in ("word:110", "word:260"):
            for condition in CONDITIONS:
                values = [
                    cells[(doc, key)][condition]["rougeL_f1"]
                    for doc in docs
                    if (doc, key) in cells and condition in cells[(doc, key)]
                ]
                if not values:
                    continue
                means.append(
                    {
                        "family": FAMILY_LABEL.get(family, family),
                        "budget": key,
                        "condition": condition,
                        "reports": len(values),
                        "mean_rougeL": round(statistics.fmean(values), 5),
                    }
                )
            for cand, ref in (("Full", "no_path"), ("AB2", "AB0"), ("TextRank", "no_path")):
                diffs = [
                    cells[(doc, key)][cand]["rougeL_f1"] - cells[(doc, key)][ref]["rougeL_f1"]
                    for doc in docs
                    if (doc, key) in cells and cand in cells[(doc, key)] and ref in cells[(doc, key)]
                ]
                if not diffs:
                    continue
                contrasts.append(
                    {
                        "family": FAMILY_LABEL.get(family, family),
                        "budget": key,
                        "contrast": f"{cand} - {ref}",
                        "reports": len(diffs),
                        "mean_delta_rougeL": round(statistics.fmean(diffs), 5),
                        "negative": sum(1 for d in diffs if d < -1e-12),
                        "positive": sum(1 for d in diffs if d > 1e-12),
                        "tied": sum(1 for d in diffs if abs(d) <= 1e-12),
                        "candidate_units_min": min(meta[d]["candidate_units"] for d in docs if d in meta),
                        "candidate_units_max": max(meta[d]["candidate_units"] for d in docs if d in meta),
                        "reference_words_min": min(meta[d]["reference_words"] for d in docs if d in meta),
                        "reference_words_max": max(meta[d]["reference_words"] for d in docs if d in meta),
                    }
                )
    return means, contrasts


def _candidate_counts() -> dict[str, int]:
    counts = {}
    if not PRIVATE_REPORTS.is_file():
        return counts
    with PRIVATE_REPORTS.open(encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            candidates = record.get("candidate_sentences", 0)
            # The field is the candidate list itself; only its length may be emitted,
            # never the units it contains.
            counts[record["doc_id"]] = len(candidates) if isinstance(candidates, list) else int(candidates)
    return counts


def table_s16() -> tuple[list[dict], list[dict], list[dict]]:
    counts = _candidate_counts()
    rows = list(csv.DictReader(ITEM_METRICS.open(encoding="utf-8-sig")))
    main = [r for r in rows if r["condition"] in ("AB-0", "AB-6", "RP-11", "G-T")]
    cost, coverage = [], []
    for row in sorted(main, key=lambda r: (r["condition"], r["word_budget"], r["doc_id"])):
        cost.append(
            {
                "document": row["doc_id"],
                "series": row["report_series_id"],
                "condition": row["condition"],
                "word_budget": row["word_budget"],
                "candidate_sentences": counts.get(row["doc_id"], ""),
                "selection_and_scoring_seconds": round(float(row["selection_and_scoring_seconds"]), 4),
                "preprocess_seconds_shared": round(float(row["preprocess_seconds_shared"]), 4),
                "estimated_total_seconds": round(float(row["estimated_total_seconds"]), 4),
                "python_peak_memory_mb": round(float(row["python_peak_memory_mb"]), 3),
                "selected_units": row["selected_units"],
                "actual_words": row["actual_words"],
                "status": row["status"],
            }
        )
    for row in sorted(rows, key=lambda r: (r["condition"], r["word_budget"], r["doc_id"])):
        coverage.append(
            {
                "document": row["doc_id"],
                "series": row["report_series_id"],
                "condition": row["condition"],
                "word_budget": row["word_budget"],
                "role_coverage": round(float(row["role_coverage"]), 4),
                "typed_edge_coverage": round(float(row["typed_edge_coverage"]), 4),
                "redundancy": round(float(row["redundancy"]), 4),
                "budget_utilization": round(float(row["budget_utilization"]), 4),
                "selected_units": row["selected_units"],
            }
        )
    per_report = []
    for doc_id in sorted({r["doc_id"] for r in rows}):
        for budget in ("110", "260"):
            subset = [r for r in rows if r["doc_id"] == doc_id and r["word_budget"] == budget]
            if not subset:
                continue
            per_report.append(
                {
                    "document": doc_id,
                    "series": subset[0]["report_series_id"],
                    "word_budget": budget,
                    "candidate_sentences": counts.get(doc_id, ""),
                    "conditions": len(subset),
                    "mean_role_coverage": round(statistics.fmean(float(r["role_coverage"]) for r in subset), 4),
                    "mean_typed_edge_coverage": round(
                        statistics.fmean(float(r["typed_edge_coverage"]) for r in subset), 4
                    ),
                    "min_role_coverage": round(min(float(r["role_coverage"]) for r in subset), 4),
                    "max_role_coverage": round(max(float(r["role_coverage"]) for r in subset), 4),
                    "mean_selection_seconds": round(
                        statistics.fmean(float(r["selection_and_scoring_seconds"]) for r in subset), 4
                    ),
                    "mean_peak_memory_mb": round(
                        statistics.fmean(float(r["python_peak_memory_mb"]) for r in subset), 3
                    ),
                }
            )
    return cost, coverage, per_report


def main() -> None:
    effects, deltas = table_s14()
    means, contrasts = table_s15()
    cost, coverage, per_report = table_s16()

    write_csv(
        OUT / "q5_reservation_path_effects.csv",
        effects,
        [
            "factor",
            "word_budget",
            "series",
            "mean_delta_rougeL",
            "cluster_bootstrap_95_low",
            "cluster_bootstrap_95_high",
            "paired_smd",
            "exact_series_signflip_p",
            "holm_adjusted_p",
            "holm_family_size",
            "bootstrap_samples",
            "bootstrap_seed",
        ],
    )
    write_csv(OUT / "q5_reservation_path_series_deltas.csv", deltas, ["factor", "word_budget", "series", "delta_rougeL"])
    write_csv(
        OUT / "q9_external_family_condition_means.csv",
        means,
        ["family", "budget", "condition", "reports", "mean_rougeL"],
    )
    write_csv(
        OUT / "q9_external_family_paired_contrasts.csv",
        contrasts,
        [
            "family",
            "budget",
            "contrast",
            "reports",
            "mean_delta_rougeL",
            "negative",
            "positive",
            "tied",
            "candidate_units_min",
            "candidate_units_max",
            "reference_words_min",
            "reference_words_max",
        ],
    )
    write_csv(
        OUT / "q3_report_cost_vs_candidates.csv",
        cost,
        [
            "document",
            "series",
            "condition",
            "word_budget",
            "candidate_sentences",
            "selection_and_scoring_seconds",
            "preprocess_seconds_shared",
            "estimated_total_seconds",
            "python_peak_memory_mb",
            "selected_units",
            "actual_words",
            "status",
        ],
    )
    write_csv(
        OUT / "q4_role_edge_coverage_per_condition.csv",
        coverage,
        [
            "document",
            "series",
            "condition",
            "word_budget",
            "role_coverage",
            "typed_edge_coverage",
            "redundancy",
            "budget_utilization",
            "selected_units",
        ],
    )
    write_csv(
        OUT / "q4_role_edge_coverage_per_report.csv",
        per_report,
        [
            "document",
            "series",
            "word_budget",
            "candidate_sentences",
            "conditions",
            "mean_role_coverage",
            "mean_typed_edge_coverage",
            "min_role_coverage",
            "max_role_coverage",
            "mean_selection_seconds",
            "mean_peak_memory_mb",
        ],
    )

    manifest = {
        "schema": "c2ges-descriptive-addenda-v2",
        "claim_class": "DESCRIPTIVE_ONLY_NO_NEW_INFERENCE",
        "reviewer_items": {
            "R1-Q5": "q5_reservation_path_effects.csv + q5_reservation_path_series_deltas.csv (Table S14)",
            "R1-Q9": "q9_external_family_condition_means.csv + q9_external_family_paired_contrasts.csv (Table S15)",
            "R1-Q3": "q3_report_cost_vs_candidates.csv (Table S16)",
            "R1-Q4": "q4_role_edge_coverage_per_condition.csv + q4_role_edge_coverage_per_report.csv (Table S16)",
        },
        "inputs": {
            path.name: sha256(path)
            for path in (INTERACTIONS, ITEM_METRICS, EXTERNAL_ARMS, EXTERNAL_CORPUS)
            if path.is_file()
        },
        "private_inputs_used_for_counts_only": {
            PRIVATE_REPORTS.name: sha256(PRIVATE_REPORTS) if PRIVATE_REPORTS.is_file() else None
        },
        "boundaries": [
            "no third-party report text is read into any output",
            "no new hypothesis test, no new Holm family",
            "family rows are never pooled into a single accuracy",
            "candidate-set counts come from the private derived corpus and are reported as counts only",
        ],
        "row_counts": {
            "q5_effects": len(effects),
            "q5_series_deltas": len(deltas),
            "q9_family_means": len(means),
            "q9_family_contrasts": len(contrasts),
            "q3_cost": len(cost),
            "q4_coverage": len(coverage),
            "q4_per_report": len(per_report),
        },
    }
    (OUT / "ADDENDA_V2_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest["row_counts"], indent=2))
    print("\nS15 family contrasts (descriptive):")
    for row in contrasts:
        print(
            f"  {row['family']:36s} {row['budget']:9s} {row['contrast']:18s} n={row['reports']} "
            f"mean={row['mean_delta_rougeL']:+.5f} neg/pos/tie={row['negative']}/{row['positive']}/{row['tied']}"
        )


if __name__ == "__main__":
    main()
