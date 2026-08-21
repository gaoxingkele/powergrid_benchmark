"""Build a non-verbatim selected-ID-to-page locator from frozen local inputs.

The output contains identifiers, positions, page locators, report metadata and
source URLs only.  It deliberately excludes candidate text, selected text,
reference summaries and source PDFs.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


EXPECTED_PREDICTION_SHA256 = (
    "AAE2BFE0E6C426B6A69D727F24239A07DFD7DBEE8A4CE228E86625CCDCA2338F"
)
EXPECTED_TEST_CANDIDATE_SHA256 = (
    "A9342BD75BB5E20B61C9B06FE21B1FBA260347BFDB77B0AEBBA89A423DFCD127"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def build(predictions: list[dict], reports: list[dict]) -> tuple[list[dict], dict]:
    report_index: dict[str, dict] = {}
    candidate_index: dict[tuple[str, str], dict] = {}
    duplicate_candidates: list[str] = []
    sid_order_mismatches: list[str] = []
    invalid_pages: list[str] = []

    for report in reports:
        doc_id = report["doc_id"]
        if doc_id in report_index:
            raise AssertionError(f"duplicate report ID: {doc_id}")
        report_index[doc_id] = report
        for source_order, candidate in enumerate(report["candidate_sentences"], start=1):
            sid = candidate["sid"]
            key = (doc_id, sid)
            if key in candidate_index:
                duplicate_candidates.append(f"{doc_id}:{sid}")
            candidate_index[key] = {"page": candidate["page"], "source_order": source_order}
            if sid != f"s{source_order:05d}":
                sid_order_mismatches.append(f"{doc_id}:{sid}:{source_order}")
            if not isinstance(candidate["page"], int) or not 1 <= candidate["page"] <= report["source_page_count"]:
                invalid_pages.append(f"{doc_id}:{sid}:{candidate['page']}")

    output: list[dict] = []
    unresolved: list[str] = []
    duplicate_output_keys: list[str] = []
    seen_output_keys: set[tuple] = set()
    for row in predictions:
        doc_id = row["doc_id"]
        report = report_index.get(doc_id)
        if report is None:
            unresolved.append(f"missing-report:{doc_id}")
            continue
        if len(row["selected_sentence_ids"]) != row["budget"]:
            unresolved.append(f"budget-cardinality:{doc_id}:{row['condition']}:{row['budget']}")
            continue
        for selection_rank, sid in enumerate(row["selected_sentence_ids"], start=1):
            locator = candidate_index.get((doc_id, sid))
            if locator is None:
                unresolved.append(f"missing-candidate:{doc_id}:{sid}")
                continue
            primary_key = (row["condition"], int(row["budget"]), doc_id, selection_rank)
            if primary_key in seen_output_keys:
                duplicate_output_keys.append(":".join(map(str, primary_key)))
            seen_output_keys.add(primary_key)
            output.append(
                {
                    "condition": row["condition"],
                    "budget": int(row["budget"]),
                    "report_id": doc_id,
                    "report_title": report["title"],
                    "sentence_id": sid,
                    "selection_rank": selection_rank,
                    "page": locator["page"],
                    "source_order": locator["source_order"],
                    "source_page_count": report["source_page_count"],
                    "source_url": report["source_url"],
                }
            )

    checks = {
        "prediction_rows_210": len(predictions) == 210,
        "test_reports_15": len(reports) == 15,
        "selected_references_1575": len(output) == 1575,
        "candidate_keys_unique": not duplicate_candidates,
        "output_primary_keys_unique": not duplicate_output_keys,
        "all_references_resolved": not unresolved,
        "all_pages_valid": not invalid_pages,
        "sid_matches_one_based_source_order": not sid_order_mismatches,
        "contains_no_verbatim_fields": all(
            not ({"text", "selected_text", "prediction", "reference_summary"} & set(row)) for row in output
        ),
    }
    audit = {
        "schema": "c2ges-selected-page-locator-audit-v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "counts": {
            "prediction_rows": len(predictions),
            "test_reports": len(reports),
            "candidate_keys": len(candidate_index),
            "selected_references": len(output),
            "unresolved": len(unresolved),
            "duplicate_candidate_keys": len(duplicate_candidates),
            "duplicate_output_primary_keys": len(duplicate_output_keys),
            "invalid_pages": len(invalid_pages),
            "sid_order_mismatches": len(sid_order_mismatches),
        },
        "scope": "non-verbatim identifier-to-page locator; no source or selected text",
    }
    return output, audit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", required=True, type=Path)
    parser.add_argument("--test-candidates", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    prediction_hash = digest(args.predictions)
    candidate_hash = digest(args.test_candidates)
    if prediction_hash != EXPECTED_PREDICTION_SHA256:
        raise SystemExit(f"refused: prediction hash mismatch: {prediction_hash}")
    if candidate_hash != EXPECTED_TEST_CANDIDATE_SHA256:
        raise SystemExit(f"refused: candidate hash mismatch: {candidate_hash}")

    output, audit = build(load_jsonl(args.predictions), load_jsonl(args.test_candidates))
    audit["prediction_sha256"] = prediction_hash
    audit["test_candidate_sha256"] = candidate_hash
    args.output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.output_dir / "selected_page_locator.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(output[0]))
        writer.writeheader()
        writer.writerows(output)
    audit["locator_sha256"] = digest(csv_path)
    audit["locator_bytes"] = csv_path.stat().st_size
    (args.output_dir / "SELECTED_PAGE_LOCATOR_AUDIT.json").write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"status": audit["status"], **audit["counts"]}, indent=2))
    raise SystemExit(0 if audit["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
