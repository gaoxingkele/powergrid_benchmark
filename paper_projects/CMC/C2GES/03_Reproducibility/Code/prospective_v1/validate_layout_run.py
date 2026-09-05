#!/usr/bin/env python3
"""Non-mutating integrity and privacy validation for a layout pilot run."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*")
FORBIDDEN_PUBLIC_KEYS = {"text", "reference", "summary", "title", "url", "source_url"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-output", type=Path, required=True)
    parser.add_argument("--public-audit-output", type=Path, required=True)
    args = parser.parse_args()
    private_file = args.private_output.resolve() / "layout_dev_candidates_v1.jsonl"
    public = args.public_audit_output.resolve()
    manifest = json.loads((public / "LAYOUT_DEV_PILOT_MANIFEST.json").read_text(encoding="utf-8"))
    audits = csv_rows(public / "layout_candidate_audit.csv")
    samples = csv_rows(public / "layout_boundary_sample_blank.csv")
    private_rows = [json.loads(line) for line in private_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    errors: list[str] = []

    if manifest.get("external_test_accessed") is not False or manifest.get("confirmatory_claims_allowed") is not False:
        errors.append("development-only evidence boundary failed")
    if len(private_rows) != manifest.get("reports") or len(audits) != manifest.get("reports"):
        errors.append("report count mismatch")
    audit_by_doc = {row["doc_id"]: row for row in audits}
    all_ids: set[tuple[str, str]] = set()
    total = 0
    for report in private_rows:
        doc_id = report["doc_id"]
        units = report["candidate_sentences"]
        total += len(units)
        if doc_id not in audit_by_doc or len(units) != int(audit_by_doc[doc_id]["candidate_count"]):
            errors.append(f"candidate count mismatch: {doc_id}")
        if [unit["source_order"] for unit in units] != list(range(1, len(units) + 1)):
            errors.append(f"non-consecutive source order: {doc_id}")
        previous_page = 0
        for expected, unit in enumerate(units, 1):
            if unit["sid"] != f"u{expected:05d}":
                errors.append(f"candidate id order mismatch: {doc_id}")
            if unit["page_start"] < previous_page or unit["page_end"] < unit["page_start"]:
                errors.append(f"page order mismatch: {doc_id} {unit['sid']}")
            previous_page = unit["page_start"]
            if unit["word_count"] != len(WORD_RE.findall(unit["text"])):
                errors.append(f"word count mismatch: {doc_id} {unit['sid']}")
            if unit["tokenizer_length"] <= 0 or not unit["normalized_sha256"]:
                errors.append(f"token/hash missing: {doc_id} {unit['sid']}")
            if unit["unit_type"] == "table_unit" and not all(value.startswith("t") for value in unit["block_ids"]):
                errors.append(f"table/body fusion marker: {doc_id} {unit['sid']}")
            if unit["unit_type"] != "table_unit" and any(value.startswith("t") for value in unit["block_ids"]):
                errors.append(f"table marker on non-table unit: {doc_id} {unit['sid']}")
            all_ids.add((doc_id, unit["sid"]))

    for path in (public / "layout_candidate_audit.csv", public / "layout_boundary_sample_blank.csv"):
        with path.open(encoding="utf-8-sig", newline="") as stream:
            headers = {value.lower() for value in next(csv.reader(stream))}
        if headers & FORBIDDEN_PUBLIC_KEYS:
            errors.append(f"forbidden public fields: {path.name}")
    for row in samples:
        if (row["doc_id"], row["candidate_id"]) not in all_ids:
            errors.append(f"sample locator not found: {row['doc_id']} {row['candidate_id']}")
        if any(row[field] for field in ("reviewer_a_validity", "reviewer_b_validity", "adjudication")):
            errors.append("blank human-review fields were prepopulated")

    observed_strata = Counter(value for row in samples for value in row["sampling_strata"].split("|") if value)
    if dict(observed_strata) != manifest.get("sample_strata"):
        errors.append("sample stratum counts do not match manifest")
    if total != manifest.get("total_candidates"):
        errors.append("total candidate count mismatch")
    expected_hashes = {
        private_file: manifest["outputs"]["private_dataset_sha256"],
        public / "layout_candidate_audit.csv": manifest["outputs"]["public_audit_sha256"],
        public / "layout_boundary_sample_blank.csv": manifest["outputs"]["blank_sample_sha256"],
    }
    for path, expected in expected_hashes.items():
        if sha256(path) != expected:
            errors.append(f"hash mismatch: {path.name}")

    if errors:
        print("LAYOUT VALIDATION FAIL")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("LAYOUT VALIDATION PASS")
    print(f"reports={len(private_rows)} candidates={total} samples={len(samples)}")
    print("external_test_accessed=false confirmatory_claims_allowed=false public_text_fields=0")


if __name__ == "__main__":
    main()
