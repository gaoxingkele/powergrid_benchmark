"""Build C2GES-NERC v0.3 candidates directly from complete manifest PDFs.

The script is deterministic, offline, fail-closed, and does not import the R1
agent_audit_40doc excerpt asset.  It writes a conservative rights ledger; public
access is never interpreted as redistribution permission.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from dataclasses import dataclass, asdict
from difflib import SequenceMatcher
from pathlib import Path
from typing import Iterable


def find_repository_root(start: Path) -> Path:
    """Find the workspace root without depending on the package nesting depth."""
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    raise RuntimeError("repository root not found from script location")


ROOT = find_repository_root(Path(__file__).resolve().parent)
SOURCE_ROOT = ROOT / "data/public_datasets/reliability_reports/c2ges_nerc_reports"
SOURCE_MANIFEST = SOURCE_ROOT / "metadata/c2ges_nerc_report_manifest.json"
FORBIDDEN_FRAGMENT = "agent_audit_40doc"

START_RE = re.compile(r"^\s*(?:\d+(?:\.\d+)*\s+)?executive\s+summary\s*$", re.I)
# Only independent, chapter-level body headings may terminate the reference.
# Internal Executive Summary subsections (for example, Key Findings and
# Recommendations) are deliberately absent.  Narrative sentences such as
# "Chapter 1 provides ..." cannot match because a Chapter 1 heading must have
# explicit heading punctuation and may not contain sentence punctuation.
END_RE = re.compile(
    r"^\s*(?:"
    r"chapter\s+1\s*(?::|[\-\u2013\u2014])\s*[^.!?]{1,120}|"
    r"1(?:\.0+)?\s+(?:introduction|background|event\s+(?:overview|description)|"
    r"approach(?:\s+and\s+data)?|disturbance\s+analys(?:is|es)|purpose|scope)"
    r"(?:\s*(?::|[\-\u2013\u2014])\s*[^.!?]{1,100})?|"
    r"introduction|background|event\s+(?:overview|description)|"
    r"approach(?:\s+and\s+data)?|disturbance\s+analys(?:is|es)"
    r")\s*$",
    re.I,
)
PAGE_NUMBER_RE = re.compile(r"^(?:page\s+)?\d+(?:\s+of\s+\d+)?$", re.I)
TOC_LINE_RE = re.compile(r"\.{3,}\s*\d+\s*$")
SECTION_TOC_RE = re.compile(r"^\s*(?:table\s+of\s+contents|contents)\s*$", re.I)
PUBLIC_RE = re.compile(r"^\s*<?\s*public\s*>?\s*$", re.I)
WORD_RE = re.compile(r"[A-Za-z0-9]+")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"“‘(])")
POLLUTION_PATTERNS = {
    "public_marker": re.compile(r"<\s*public\s*>", re.I),
    "replacement_character": re.compile("\ufffd"),
    "common_mojibake": re.compile(r"(?:鈥|鈺|Ã.|Â.|â€|ðŸ)"),
    "page_marker": re.compile(r"\bpage\s+\d+\s+of\s+\d+\b", re.I),
    "dot_leader": re.compile(r"\.{4,}\s*\d+"),
    "spaced_uppercase_running_title": re.compile(r"^(?:[A-Z]\s+){1,}[A-Z]{2,}.*\s+\d+\s*$"),
    "executive_summary_running_head": re.compile(r"\bexecutive\s+summary\b", re.I),
    "section_table_fusion": re.compile(
        r"^(?:introduction|background|chapter\s+\d+[^.!?]{0,100})\s+table\s+[A-Z0-9]", re.I
    ),
}


@dataclass(frozen=True)
class Line:
    page: int
    line: int
    text: str


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def normalize_match(text: str) -> str:
    return normalize_space(re.sub(r"[^A-Za-z0-9]+", " ", text)).lower()


def recurrent_key(text: str) -> str:
    """Normalize running heads while ignoring their changing page-number tokens."""
    return normalize_space(re.sub(r"\b\d+\b", " ", normalize_match(text)))


def split_pdf_pages(text: str) -> list[str]:
    """Split pdftotext output without inventing a terminal blank page."""
    pages = text.replace("\r\n", "\n").split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    return pages


def pdf_pages(path: Path) -> list[str]:
    proc = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(path), "-"],
        check=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return split_pdf_pages(proc.stdout)


def flatten_pages(pages: list[str]) -> list[Line]:
    return [
        Line(page_no, line_no, raw.rstrip())
        for page_no, page in enumerate(pages, start=1)
        for line_no, raw in enumerate(page.splitlines(), start=1)
    ]


def recurrent_line_keys(lines: list[Line], page_count: int) -> set[str]:
    page_presence: dict[str, set[int]] = {}
    for item in lines:
        key = recurrent_key(item.text)
        if 4 <= len(key) <= 160:
            page_presence.setdefault(key, set()).add(item.page)
    threshold = max(3, int(page_count * 0.20 + 0.999))
    return {key for key, pages in page_presence.items() if len(pages) >= threshold}


def line_drop_reason(item: Line, recurrent: set[str]) -> str | None:
    text = normalize_space(item.text)
    if not text:
        return "blank"
    if PUBLIC_RE.fullmatch(text):
        return "public_marker"
    if PAGE_NUMBER_RE.fullmatch(text):
        return "page_number"
    if SECTION_TOC_RE.fullmatch(text) or TOC_LINE_RE.search(text):
        return "toc"
    if recurrent_key(text) in recurrent:
        return "recurrent_header_footer"
    for name, pattern in POLLUTION_PATTERNS.items():
        if pattern.search(text):
            return name
    # Layout tables typically expose at least three numeric cells separated by columns.
    if len(re.findall(r"\s{2,}\S+", item.text)) >= 3 and len(re.findall(r"\b\d+(?:\.\d+)?\b", text)) >= 3:
        return "table_row"
    return None


def locate_summary(lines: list[Line]) -> tuple[int, int, str | None]:
    starts = [idx for idx, item in enumerate(lines) if START_RE.fullmatch(normalize_space(item.text))]
    if not starts:
        return -1, -1, "missing_executive_summary_heading"
    start = starts[0]
    for idx in range(start + 1, len(lines)):
        heading = normalize_space(lines[idx].text)
        if len(heading) <= 140 and END_RE.fullmatch(heading):
            body_chars = sum(len(normalize_space(x.text)) for x in lines[start + 1 : idx])
            # A body boundary must start on a later PDF page.  This provides a
            # conservative, directly auditable page-interval separation.
            if body_chars >= 500 and lines[idx].page > lines[start].page:
                return start, idx, None
    return start, -1, "missing_executive_summary_end"


def merge_lines(lines: list[Line]) -> str:
    merged: list[str] = []
    for item in lines:
        text = normalize_space(item.text)
        if not text:
            continue
        if merged and merged[-1].endswith("-") and text[:1].islower():
            merged[-1] = merged[-1][:-1] + text
        else:
            merged.append(text)
    return normalize_space(" ".join(merged))


def split_candidates(lines: list[Line], recurrent: set[str]) -> tuple[list[dict], Counter]:
    by_page: dict[int, list[Line]] = {}
    drops: Counter = Counter()
    for item in lines:
        reason = line_drop_reason(item, recurrent)
        if reason:
            drops[reason] += 1
            continue
        by_page.setdefault(item.page, []).append(item)

    candidates: list[dict] = []
    ordinal = 0
    for page in sorted(by_page):
        text = merge_lines(by_page[page])
        for sentence in SENTENCE_SPLIT_RE.split(text):
            sentence = normalize_space(sentence)
            if len(sentence) < 35 or len(WORD_RE.findall(sentence)) < 6:
                drops["short_fragment"] += 1
                continue
            reason = next((name for name, pat in POLLUTION_PATTERNS.items() if pat.search(sentence)), None)
            if reason:
                drops[reason] += 1
                continue
            ordinal += 1
            candidates.append({"sid": f"s{ordinal:05d}", "page": page, "text": sentence})
    return candidates, drops


def longest_common_substring_at_least(a: str, b: str, threshold: int = 50) -> int:
    if min(len(a), len(b)) < threshold:
        return 0
    # Fast exact threshold gate before computing a diagnostic maximum.
    if not any(a[i : i + threshold] in b for i in range(len(a) - threshold + 1)):
        return 0
    return SequenceMatcher(None, a, b, autojunk=False).find_longest_match().size


def remove_reference_leakage(candidates: list[dict], reference: str) -> tuple[list[dict], list[dict]]:
    ref_norm = normalize_match(reference)
    kept, removed = [], []
    for row in candidates:
        candidate_norm = normalize_match(row["text"])
        common = longest_common_substring_at_least(candidate_norm, ref_norm, 50)
        if common >= 50:
            removed.append({"sid": row["sid"], "page": row["page"], "common_chars": common})
        else:
            kept.append(row)
    for index, row in enumerate(kept, start=1):
        row["sid"] = f"s{index:05d}"
    return kept, removed


def deduplicate_candidates(candidates: list[dict]) -> tuple[list[dict], list[dict]]:
    """Keep the first page-anchored occurrence of each normalized sentence."""
    seen: dict[str, dict] = {}
    kept, removed = [], []
    for row in candidates:
        key = normalize_match(row["text"])
        if key in seen:
            removed.append(
                {
                    "sid": row["sid"],
                    "page": row["page"],
                    "first_sid": seen[key]["sid"],
                    "first_page": seen[key]["page"],
                }
            )
            continue
        seen[key] = row
        kept.append(row)
    for index, row in enumerate(kept, start=1):
        row["sid"] = f"s{index:05d}"
    return kept, removed


def remaining_leak_count(candidates: list[dict], reference: str) -> int:
    ref_norm = normalize_match(reference)
    return sum(
        longest_common_substring_at_least(normalize_match(row["text"]), ref_norm, 50) >= 50
        for row in candidates
    )


def pollution_counts(candidates: list[dict]) -> dict[str, int]:
    return {
        name: sum(bool(pattern.search(row["text"])) for row in candidates)
        for name, pattern in POLLUTION_PATTERNS.items()
    }


def report_series(doc_id: str, title: str) -> str:
    lower = title.lower()
    rules = (
        ("state of reliability", "series_state_of_reliability"),
        ("odessa", "series_odessa"),
        ("ems", "series_ems"),
        ("hurricane", "series_hurricane"),
        ("winter storm elliott", "series_winter_storm_elliott"),
    )
    for marker, group in rules:
        if marker in lower:
            return group
    if "solar photovoltaic" in lower or "solar pv" in lower:
        return "series_solar_pv"
    return doc_id


def split_name(series_id: str) -> str:
    bucket = int(hashlib.sha256(series_id.encode("utf-8")).hexdigest()[:8], 16) % 10
    return "dev" if bucket < 3 else "test"


def jsonl_write(path: Path, rows: Iterable[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def build(output: Path) -> dict:
    if output.exists():
        raise FileExistsError(f"Refusing existing output directory: {output}")
    output.mkdir(parents=True)
    manifest_rows = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    if len(manifest_rows) != 40:
        raise RuntimeError(f"Expected 40 manifest rows, found {len(manifest_rows)}")

    dataset: list[dict] = []
    audits: list[dict] = []
    rights: list[dict] = []
    missing: list[dict] = []

    for source in manifest_rows:
        doc_id = source["doc_id"]
        pdf = SOURCE_ROOT / source["local_pdf"]
        if FORBIDDEN_FRAGMENT in str(pdf):
            raise RuntimeError("Forbidden excerpt input detected")
        if not pdf.exists():
            missing.append({"doc_id": doc_id, "expected_path": str(pdf)})
            audits.append({"doc_id": doc_id, "status": "missing_pdf"})
            continue

        pdf_hash = sha256(pdf)
        rights.append(
            {
                "doc_id": doc_id,
                "source_url": source.get("url", ""),
                "local_pdf": source["local_pdf"],
                "pdf_sha256": pdf_hash,
                "access_date": "not_recorded_in_source_manifest",
                "rights_holder": "not_verified",
                "license_or_terms_locator": "not_recorded_in_source_manifest",
                "local_computational_use_status": "performed_for_research; legal determination pending responsible human/institution",
                "pdf_redistribution_status": "not_authorized_pending_human_rights_review",
                "verbatim_text_redistribution_status": "not_authorized_pending_human_rights_review",
                "reviewer_access_status": "by_corresponding_author_subject_to_third_party_terms",
            }
        )

        try:
            pages = pdf_pages(pdf)
        except subprocess.CalledProcessError as exc:
            audits.append({"doc_id": doc_id, "status": "pdftotext_failed", "returncode": exc.returncode, "pdf_sha256": pdf_hash})
            continue
        lines = flatten_pages(pages)
        start, end, boundary_error = locate_summary(lines)
        if boundary_error:
            audits.append(
                {
                    "doc_id": doc_id,
                    "status": boundary_error,
                    "page_count": len(pages),
                    "pdf_sha256": pdf_hash,
                }
            )
            continue

        recurrent = recurrent_line_keys(lines, len(pages))
        reference_lines = [item for item in lines[start + 1 : end] if line_drop_reason(item, recurrent) is None]
        reference = merge_lines(reference_lines)
        reference_words = len(WORD_RE.findall(reference))
        if reference_words < 80:
            audits.append({"doc_id": doc_id, "status": "reference_too_short", "reference_words": reference_words, "pdf_sha256": pdf_hash})
            continue

        reference_page_max = max(item.page for item in reference_lines)
        body_page = lines[end].page
        if reference_page_max >= body_page:
            audits.append(
                {
                    "doc_id": doc_id,
                    "status": "summary_body_page_interval_overlap",
                    "summary_last_page": reference_page_max,
                    "body_heading_page": body_page,
                    "pdf_sha256": pdf_hash,
                }
            )
            continue

        raw_candidates, drops = split_candidates(lines[end + 1 :], recurrent)
        leakage_clean, leak_removed = remove_reference_leakage(raw_candidates, reference)
        candidates, duplicate_removed = deduplicate_candidates(leakage_clean)
        residual_leaks = remaining_leak_count(candidates, reference)
        pollution = pollution_counts(candidates)
        if residual_leaks != 0 or any(pollution.values()):
            raise RuntimeError(f"Post-clean gate failed for {doc_id}: leaks={residual_leaks}, pollution={pollution}")
        if len(candidates) < 12:
            audits.append(
                {
                    "doc_id": doc_id,
                    "status": "too_few_clean_candidates",
                    "candidate_count": len(candidates),
                    "leak_removed_count": len(leak_removed),
                    "pdf_sha256": pdf_hash,
                }
            )
            continue
        candidate_min_page = min(row["page"] for row in candidates)
        page_interval_overlap = int(candidate_min_page <= reference_page_max)
        if page_interval_overlap:
            raise RuntimeError(
                f"Page-interval leakage gate failed for {doc_id}: "
                f"reference<=p{reference_page_max}, candidate starts p{candidate_min_page}"
            )

        series_id = report_series(doc_id, source.get("title", ""))
        row = {
            "doc_id": doc_id,
            "title": source.get("title", ""),
            "report_series_id": series_id,
            "split": split_name(series_id),
            "source_url": source.get("url", ""),
            "source_pdf_sha256": pdf_hash,
            "source_page_count": len(pages),
            "reference_summary": reference,
            "reference_provenance": "official_executive_summary_extracted_from_complete_manifest_pdf",
            "reference_start": asdict(lines[start]),
            "body_start": asdict(lines[end]),
            "reference_page_max": reference_page_max,
            "candidate_min_page": candidate_min_page,
            "candidate_sentences": candidates,
            "candidate_count": len(candidates),
            "candidate_truncation": "none",
            "silver_role_evidence": {},
            "silver_label_provenance": "none_in_v0.3_builder",
            "rights_status": "not_authorized_for_text_redistribution_pending_human_review",
        }
        dataset.append(row)
        audits.append(
            {
                "doc_id": doc_id,
                "status": "included",
                "split": row["split"],
                "pdf_sha256": pdf_hash,
                "page_count": len(pages),
                "reference_words": reference_words,
                "summary_heading_page": lines[start].page,
                "body_heading_page": lines[end].page,
                "summary_last_page": reference_page_max,
                "candidate_min_page": candidate_min_page,
                "page_interval_overlap": page_interval_overlap,
                "raw_candidate_count": len(raw_candidates),
                "candidate_count": len(candidates),
                "candidate_truncation": "none",
                "leak_removed_count": len(leak_removed),
                "duplicate_removed_count": len(duplicate_removed),
                "residual_reference_substring_ge_50": residual_leaks,
                "pollution_counts": pollution,
                "drop_counts": dict(sorted(drops.items())),
            }
        )

    dataset.sort(key=lambda row: row["doc_id"])
    audits.sort(key=lambda row: row["doc_id"])
    rights.sort(key=lambda row: row["doc_id"])
    missing.sort(key=lambda row: row["doc_id"])
    dataset_path = output / "nerc_full_pdf_benchmark_v0_3.jsonl"
    jsonl_write(dataset_path, dataset)
    dev_path = output / "nerc_full_pdf_dev_v0_3.jsonl"
    test_path = output / "nerc_full_pdf_test_v0_3.jsonl"
    jsonl_write(dev_path, (row for row in dataset if row["split"] == "dev"))
    jsonl_write(test_path, (row for row in dataset if row["split"] == "test"))
    jsonl_write(output / "per_report_extraction_audit.jsonl", audits)
    jsonl_write(output / "rights_ledger.jsonl", rights)
    jsonl_write(output / "missing_inputs.jsonl", missing)

    with (output / "rights_ledger.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rights[0]) if rights else ["doc_id"])
        writer.writeheader()
        writer.writerows(rights)

    included_audits = [row for row in audits if row["status"] == "included"]
    build_manifest = {
        "protocol": "C2GES-NERC-FULL-PDF-v0.3-diagnostic",
        "source_manifest": str(SOURCE_MANIFEST),
        "source_manifest_sha256": sha256(SOURCE_MANIFEST),
        "source_pdf_manifest_rows": len(manifest_rows),
        "source_pdf_missing": len(missing),
        "included": len(dataset),
        "dev": sum(row["split"] == "dev" for row in dataset),
        "test": sum(row["split"] == "test" for row in dataset),
        "excluded": len(audits) - len(dataset),
        "dataset_sha256": sha256(dataset_path),
        "dev_dataset_sha256": sha256(dev_path),
        "test_dataset_sha256": sha256(test_path),
        "builder_sha256": sha256(Path(__file__)),
        "candidate_source": "complete_manifest_pdfs_only",
        "forbidden_excerpt_asset_used": False,
        "candidate_fixed_cap": None,
        "total_candidates": sum(row["candidate_count"] for row in dataset),
        "max_candidates_per_report": max((row["candidate_count"] for row in dataset), default=0),
        "reports_over_80_candidates": sum(row["candidate_count"] > 80 for row in dataset),
        "residual_reference_substring_ge_50": sum(row["residual_reference_substring_ge_50"] for row in included_audits),
        "pollution_totals": {
            name: sum(row["pollution_counts"][name] for row in included_audits)
            for name in POLLUTION_PATTERNS
        },
        "rights_policy": "fail_closed_no_redistribution_without_responsible_human_or_institutional_approval",
        "note": "Diagnostic until boundary and extraction audits are independently accepted; do not use for test evaluation.",
    }
    (output / "build_manifest.json").write_text(
        json.dumps(build_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return build_manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.output.resolve()), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
