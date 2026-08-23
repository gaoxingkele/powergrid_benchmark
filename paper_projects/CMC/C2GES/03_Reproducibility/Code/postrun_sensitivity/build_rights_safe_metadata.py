#!/usr/bin/env python3
"""Build a non-verbatim 40-report metadata index from already local manifests.

No PDF or candidate/reference text is read. Titles and URLs are copied only
from the frozen source manifest; years are merely title-derived labels and are
never promoted to independently verified publication dates.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def report_series(doc_id: str, title: str) -> str:
    lower = title.lower()
    for marker, group in (
        ("state of reliability", "series_state_of_reliability"),
        ("odessa", "series_odessa"),
        ("ems", "series_ems"),
        ("hurricane", "series_hurricane"),
        ("winter storm elliott", "series_winter_storm_elliott"),
    ):
        if marker in lower:
            return group
    if "solar photovoltaic" in lower or "solar pv" in lower:
        return "series_solar_pv"
    return doc_id


def planned_split(series_id: str) -> str:
    bucket = int(hashlib.sha256(series_id.encode("utf-8")).hexdigest()[:8], 16) % 10
    return "dev" if bucket < 3 else "test"


def genre_label(source_page: str) -> str:
    return {
        "nerc_event_analysis_reports.html": "event_analysis_collection",
        "nerc_winter_storm_elliott.html": "winter_storm_elliott_collection",
        "nerc_state_of_reliability.html": "state_of_reliability_collection",
        "nerc_lessons_learned.html": "lessons_learned_collection",
        "manual_url_pattern": "state_of_reliability_manual_locator",
    }.get(source_page, "unclassified_source_collection")


def build(source_manifest: Path, audit_jsonl: Path, rights_jsonl: Path) -> list[dict]:
    sources = json.loads(source_manifest.read_text(encoding="utf-8"))
    audits = [json.loads(x) for x in audit_jsonl.read_text(encoding="utf-8").splitlines() if x.strip()]
    rights = [json.loads(x) for x in rights_jsonl.read_text(encoding="utf-8").splitlines() if x.strip()]
    if not (len(sources) == len(audits) == len(rights) == 40):
        raise ValueError(f"expected 40 rows in all inputs: {len(sources)}, {len(audits)}, {len(rights)}")
    audit_by_id = {x["doc_id"]: x for x in audits}
    rights_by_id = {x["doc_id"]: x for x in rights}
    if len(audit_by_id) != 40 or len(rights_by_id) != 40:
        raise ValueError("duplicate doc_id in audit or rights ledger")

    rows = []
    for src in sources:
        doc_id, title = src["doc_id"], src["title"]
        audit, right = audit_by_id[doc_id], rights_by_id[doc_id]
        series = report_series(doc_id, title)
        years = sorted(set(re.findall(r"(?<!\d)(?:19|20)\d{2}(?!\d)", title)))
        included = audit["status"] == "included"
        rows.append({
            "doc_id": doc_id,
            "title_metadata": title,
            "source_collection": src.get("source_page", "not_recorded"),
            "genre_collection_label": genre_label(src.get("source_page", "")),
            "source_host": "www.nerc.com",
            "source_url": src.get("url", ""),
            "year_label_from_title": ";".join(years) if years else "not_stated_in_title",
            "year_verification_status": "title_metadata_only_not_independently_verified",
            "page_count": audit.get("page_count", "not_recorded"),
            "reference_words": audit.get("reference_words", "not_applicable_excluded"),
            "candidate_count": audit.get("candidate_count", "not_applicable_excluded"),
            "report_series_id": series,
            "planned_group_split": planned_split(series),
            "analysis_split": audit.get("split", "excluded"),
            "inclusion_status": "included" if included else "excluded",
            "exclusion_reason": "not_applicable" if included else audit["status"],
            "pdf_sha256": audit.get("pdf_sha256", right.get("pdf_sha256", "")),
            "access_date": right.get("access_date", "not_recorded"),
            "rights_holder": right.get("rights_holder", "not_verified"),
            "license_or_terms_locator": right.get("license_or_terms_locator", "not_recorded"),
            "pdf_redistribution_status": right.get("pdf_redistribution_status", "not_authorized"),
            "verbatim_text_redistribution_status": right.get("verbatim_text_redistribution_status", "not_authorized"),
            "reviewer_access_status": right.get("reviewer_access_status", "subject_to_third_party_terms"),
        })
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("source_manifest", type=Path)
    ap.add_argument("audit_jsonl", type=Path)
    ap.add_argument("rights_jsonl", type=Path)
    ap.add_argument("out_dir", type=Path)
    args = ap.parse_args()
    rows = build(args.source_manifest, args.audit_jsonl, args.rights_jsonl)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.out_dir / "rights_safe_report_metadata.json"
    csv_path = args.out_dir / "rights_safe_report_metadata.csv"
    json_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    included = sum(r["inclusion_status"] == "included" for r in rows)
    reasons: dict[str, int] = {}
    for r in rows:
        if r["inclusion_status"] == "excluded":
            reasons[r["exclusion_reason"]] = reasons.get(r["exclusion_reason"], 0) + 1
    summary = {
        "artifact_status": "rights_safe_non_verbatim_metadata_only",
        "source_inputs": {
            "source_manifest_sha256": sha256(args.source_manifest),
            "extraction_audit_sha256": sha256(args.audit_jsonl),
            "rights_ledger_sha256": sha256(args.rights_jsonl),
        },
        "counts": {"total": len(rows), "included": included, "excluded": len(rows) - included,
                   "exclusion_reasons": reasons},
        "limitations": [
            "Title and URL are source-manifest metadata; no report text is redistributed.",
            "Year labels are parsed from titles and are not independently verified publication dates.",
            "Genre labels describe source collections, not independently adjudicated document genres.",
            "Rights-holder and terms fields remain unresolved where the frozen rights ledger says not_verified/not_recorded.",
        ],
        "output_sha256": {json_path.name: sha256(json_path), csv_path.name: sha256(csv_path)},
    }
    (args.out_dir / "RIGHTS_SAFE_METADATA_MANIFEST.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
