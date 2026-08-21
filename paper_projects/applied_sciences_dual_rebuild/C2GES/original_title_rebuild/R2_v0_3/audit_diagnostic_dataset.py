"""Independent-style structural audit of a v0.3 diagnostic dataset artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

from build_full_pdf_dataset import (
    FORBIDDEN_FRAGMENT,
    POLLUTION_PATTERNS,
    SOURCE_MANIFEST,
    SOURCE_ROOT,
    normalize_match,
    remaining_leak_count,
    sha256,
)
from v03_methods import build_graph_v03


def token_jaccard(left: str, right: str) -> float:
    a, b = set(normalize_match(left).split()), set(normalize_match(right).split())
    return len(a & b) / len(a | b) if a or b else 0.0


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def audit(dataset_dir: Path, output: Path) -> dict:
    if output.exists():
        raise FileExistsError(f"Refusing existing audit output: {output}")
    output.mkdir(parents=True)
    dataset_path = dataset_dir / "nerc_full_pdf_benchmark_v0_3.jsonl"
    build_manifest_path = dataset_dir / "build_manifest.json"
    rights_path = dataset_dir / "rights_ledger.jsonl"
    missing_path = dataset_dir / "missing_inputs.jsonl"
    rows = jsonl(dataset_path)
    manifest = json.loads(build_manifest_path.read_text(encoding="utf-8"))
    rights = jsonl(rights_path)
    missing = jsonl(missing_path)
    source_rows = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    extraction_audits = {row["doc_id"]: row for row in jsonl(dataset_dir / "per_report_extraction_audit.jsonl")}

    failures: list[dict] = []
    advisories: list[dict] = []
    per_report: list[dict] = []
    for row in rows:
        candidates = row["candidate_sentences"]
        keys = [normalize_match(item["text"]) for item in candidates]
        duplicates = sum(count - 1 for count in Counter(keys).values() if count > 1)
        leaks = remaining_leak_count(candidates, row["reference_summary"])
        pollution = {
            name: sum(bool(pattern.search(item["text"])) for item in candidates)
            for name, pattern in POLLUTION_PATTERNS.items()
        }
        page_anchor_errors = sum(
            not isinstance(item.get("page"), int)
            or item["page"] < 1
            or item["page"] > row["source_page_count"]
            for item in candidates
        )
        sid_errors = int([item["sid"] for item in candidates] != [f"s{i:05d}" for i in range(1, len(candidates) + 1)])
        pdf = SOURCE_ROOT / next(source["local_pdf"] for source in source_rows if source["doc_id"] == row["doc_id"])
        pdf_hash_match = sha256(pdf) == row["source_pdf_sha256"]
        info = subprocess.run(
            ["pdfinfo", str(pdf)], check=True, capture_output=True, text=True, errors="replace"
        ).stdout
        actual_page_count = int(next(line.split(":", 1)[1] for line in info.splitlines() if line.startswith("Pages:")))
        page_count_match = actual_page_count == row["source_page_count"]
        candidate_min_page = min((item["page"] for item in candidates), default=0)
        reference_page_max = int(row.get("reference_page_max", 0))
        page_interval_overlap = int(candidate_min_page <= reference_page_max)
        extraction = extraction_audits.get(row["doc_id"], {})
        record = {
            "doc_id": row["doc_id"],
            "split": row["split"],
            "candidate_count": len(candidates),
            "candidate_truncation": row["candidate_truncation"],
            "duplicate_normalized_candidates": duplicates,
            "reference_substring_ge_50": leaks,
            "pollution_counts": pollution,
            "page_anchor_errors": page_anchor_errors,
            "sid_sequence_error": sid_errors,
            "pdf_hash_match": pdf_hash_match,
            "actual_pdf_page_count": actual_page_count,
            "stored_pdf_page_count": row["source_page_count"],
            "pdf_page_count_match": page_count_match,
            "reference_page_max": reference_page_max,
            "candidate_min_page": candidate_min_page,
            "page_interval_overlap": page_interval_overlap,
            "extraction_audit_page_interval_overlap": extraction.get("page_interval_overlap"),
        }
        per_report.append(record)
        if (
            duplicates or leaks or any(pollution.values()) or page_anchor_errors or sid_errors
            or not pdf_hash_match or not page_count_match or page_interval_overlap
            or extraction.get("page_interval_overlap") != 0
        ):
            failures.append(record)

    dev_rows = [row for row in rows if row["split"] == "dev"]
    test_rows = [row for row in rows if row["split"] == "test"]
    group_splits: dict[str, set[str]] = {}
    for row in rows:
        group_splits.setdefault(row["report_series_id"], set()).add(row["split"])
    crossing_groups = {group: sorted(splits) for group, splits in group_splits.items() if len(splits) > 1}
    similarities = sorted(
        (
            {
                "dev_doc_id": dev["doc_id"],
                "test_doc_id": test["doc_id"],
                "reference_token_jaccard": token_jaccard(dev["reference_summary"], test["reference_summary"]),
            }
            for dev in dev_rows
            for test in test_rows
        ),
        key=lambda item: item["reference_token_jaccard"],
        reverse=True,
    )
    if similarities and similarities[0]["reference_token_jaccard"] >= 0.65:
        advisories.append(
            {
                "type": "cross_split_reference_similarity",
                "detail": similarities[0],
                "status": "requires report-series human audit; not silently treated as a pass",
            }
        )

    rights_failures = [
        row["doc_id"]
        for row in rights
        if row["pdf_redistribution_status"] != "not_authorized_pending_human_rights_review"
        or row["verbatim_text_redistribution_status"] != "not_authorized_pending_human_rights_review"
    ]
    reproduced_boundaries = {
        "nerc_001": (8, "Introduction"),
        "nerc_008": (8, "Chapter 1: Disturbance Analyses"),
        "nerc_011": (10, "Introduction"),
        "nerc_028": (7, "Introduction"),
        "nerc_040": (12, "Chapter 1: Availability Data Systems Assessment"),
    }
    boundary_regressions = []
    for prefix, expected in reproduced_boundaries.items():
        row = next((item for item in rows if item["doc_id"].startswith(prefix)), None)
        if row is None or (row["body_start"]["page"], " ".join(row["body_start"]["text"].split())) != expected:
            boundary_regressions.append({"prefix": prefix, "expected": expected, "actual": row and row["body_start"]})
    nerc034_exclusion = next(
        (record for doc_id, record in extraction_audits.items() if doc_id.startswith("nerc_034")), None
    )

    ambiguous_role_nodes = 0
    ambiguous_role_with_dominant = 0
    ambiguous_role_edge_endpoints = 0
    for row in dev_rows:
        graph = build_graph_v03(row["candidate_sentences"], max_distance=12)
        ambiguous = set()
        for node in graph.nodes:
            values = dict(node.role_scores)
            best = max(values.values(), default=0.0)
            maxima = [role for role, value in values.items() if best > 0 and abs(value - best) <= 1e-12]
            if len(maxima) > 1:
                ambiguous.add(node.sid)
                ambiguous_role_nodes += 1
                ambiguous_role_with_dominant += int(node.dominant_role is not None)
        ambiguous_role_edge_endpoints += sum(edge.source in ambiguous or edge.target in ambiguous for edge in graph.edges)

    global_checks = {
        "dataset_hash_matches_manifest": sha256(dataset_path) == manifest["dataset_sha256"],
        "source_manifest_hash_matches": sha256(SOURCE_MANIFEST) == manifest["source_manifest_sha256"],
        "source_manifest_rows_40": len(source_rows) == 40,
        "missing_inputs_zero": len(missing) == 0,
        "included_27": len(rows) == 27,
        "dev_12_test_15": (len(dev_rows), len(test_rows)) == (12, 15),
        "report_series_cross_split_zero": not crossing_groups,
        "no_fixed_candidate_cap": all(row["candidate_truncation"] == "none" for row in rows),
        "at_least_one_report_over_80": any(len(row["candidate_sentences"]) > 80 for row in rows),
        "forbidden_excerpt_asset_absent": FORBIDDEN_FRAGMENT not in dataset_path.read_text(encoding="utf-8") and not manifest["forbidden_excerpt_asset_used"],
        "rights_rows_40": len(rights) == 40,
        "rights_fail_closed": not rights_failures,
        "per_report_failures_zero": len(failures) == 0,
        "reproduced_boundary_cases_pass": not boundary_regressions,
        "ambiguous_roles_abstain": ambiguous_role_with_dominant == 0,
        "ambiguous_roles_create_no_edges": ambiguous_role_edge_endpoints == 0,
        "nerc_034_conservatively_excluded": (
            nerc034_exclusion is not None
            and nerc034_exclusion.get("status") == "missing_executive_summary_end"
            and not any(row["doc_id"].startswith("nerc_034") for row in rows)
        ),
    }
    failed_globals = [name for name, passed in global_checks.items() if not passed]
    result = {
        "audit_schema": "C2GES-NERC-v0.3-diagnostic-structural-audit-v2",
        "evaluation_status": "post_audit_corrective_not_confirmatory",
        "independence_status": "builder-team structural self-audit; fresh independent audit still required",
        "dataset_dir": str(dataset_dir),
        "dataset_sha256": sha256(dataset_path),
        "global_checks": global_checks,
        "failed_global_checks": failed_globals,
        "per_report_failures": failures,
        "boundary_regressions": boundary_regressions,
        "role_ambiguity_audit": {
            "development_ambiguous_nodes": ambiguous_role_nodes,
            "ambiguous_nodes_with_dominant_role": ambiguous_role_with_dominant,
            "edges_incident_to_ambiguous_nodes": ambiguous_role_edge_endpoints,
        },
        "advisories": advisories,
        "top_cross_split_reference_similarities": similarities[:10],
        "rights_human_approval_status": "pending",
        "status": "PASS_WITH_ADVISORIES" if not failed_globals and not failures else "FAIL",
    }
    (output / "diagnostic_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (output / "per_report_audit.jsonl").open("w", encoding="utf-8", newline="\n") as stream:
        for record in per_report:
            stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(audit(args.dataset_dir.resolve(), args.output.resolve()), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
