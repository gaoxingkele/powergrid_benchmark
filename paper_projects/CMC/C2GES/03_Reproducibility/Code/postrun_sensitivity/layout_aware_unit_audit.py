#!/usr/bin/env python3
"""Nonverbatim PyMuPDF block-preserving extraction-unit audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import fitz


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
DEFAULT_OUTPUT = PROJECT / "03_Reproducibility" / "Data" / "postrun_layout_audit" / "pymupdf_blocks_v1"
WORD_RE = re.compile(r"[A-Za-z0-9]+")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"“‘(])")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--dev", type=Path, required=True)
    parser.add_argument("--test", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest().upper()


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def normalize_match(text: str) -> str:
    return normalize_space(re.sub(r"[^A-Za-z0-9]+", " ", text)).lower()


def recurrent_key(text: str) -> str:
    return normalize_space(re.sub(r"\b\d+\b", " ", normalize_match(text)))


def intersection_fraction(block: tuple[float, float, float, float], table: tuple[float, float, float, float]) -> float:
    x0 = max(block[0], table[0])
    y0 = max(block[1], table[1])
    x1 = min(block[2], table[2])
    y1 = min(block[3], table[3])
    intersection = max(0.0, x1 - x0) * max(0.0, y1 - y0)
    area = max(1e-9, (block[2] - block[0]) * (block[3] - block[1]))
    return intersection / area


def public_schema_check(rows: list[dict[str, Any]]) -> None:
    forbidden = {"text", "reference", "summary", "title", "url", "source_url"}
    for row in rows:
        overlap = forbidden & {key.lower() for key in row}
        if overlap:
            raise AssertionError(f"Forbidden public output fields: {sorted(overlap)}")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    public_schema_check(rows)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    if args.output.exists():
        raise FileExistsError(f"Refusing to overwrite output: {args.output}")
    manifest_rows = json.loads(args.manifest.read_text(encoding="utf-8"))
    manifest = {row["doc_id"]: row for row in manifest_rows}
    frozen_rows = load_jsonl(args.dev) + load_jsonl(args.test)
    if len(manifest_rows) != 40 or len(frozen_rows) != 27 or len({row["doc_id"] for row in frozen_rows}) != 27:
        raise AssertionError("Expected 40 manifest rows and 27 unique included reports")

    report_rows: list[dict[str, Any]] = []
    sample_rows: list[dict[str, Any]] = []
    aggregate_drops: Counter[str] = Counter()
    pdf_hashes: dict[str, str] = {}

    for frozen in sorted(frozen_rows, key=lambda row: row["doc_id"]):
        doc_id = frozen["doc_id"]
        pdf = args.source_root / manifest[doc_id]["local_pdf"]
        observed_hash = sha256_file(pdf)
        if observed_hash != frozen["source_pdf_sha256"].upper():
            raise AssertionError(f"{doc_id}: source PDF hash mismatch")
        pdf_hashes[doc_id] = observed_hash
        legacy_hashes = {sha256_text(normalize_match(item["text"])) for item in frozen["candidate_sentences"]}
        start_page = int(frozen["candidate_min_page"])

        document = fitz.open(pdf)
        page_blocks: dict[int, list[dict[str, Any]]] = defaultdict(list)
        recurrent_pages: dict[str, set[int]] = defaultdict(set)
        table_failures = 0
        detected_tables = 0
        source_blocks = 0
        narrow_blocks = 0

        for page_number in range(start_page, document.page_count + 1):
            page = document[page_number - 1]
            width, height = float(page.rect.width), float(page.rect.height)
            try:
                tables = [tuple(table.bbox) for table in page.find_tables().tables]
            except Exception:
                tables = []
                table_failures += 1
            detected_tables += len(tables)
            for raw in page.get_text("blocks", sort=False):
                x0, y0, x1, y1, text, block_number, block_type = raw[:7]
                source_blocks += 1
                normalized = normalize_space(text)
                key = recurrent_key(normalized)
                if key:
                    recurrent_pages[key].add(page_number)
                if (x1 - x0) / max(width, 1.0) < 0.55:
                    narrow_blocks += 1
                page_blocks[page_number].append(
                    {
                        "bbox": (float(x0), float(y0), float(x1), float(y1)),
                        "block_number": int(block_number),
                        "block_type": int(block_type),
                        "raw": normalized,
                        "key": key,
                        "width": width,
                        "height": height,
                        "tables": tables,
                    }
                )

        recurrence_threshold = max(3, math.ceil(document.page_count * 0.20))
        recurrent = {key for key, pages in recurrent_pages.items() if len(pages) >= recurrence_threshold}
        drops: Counter[str] = Counter()
        units: list[dict[str, Any]] = []
        seen: set[str] = set()

        for page_number in sorted(page_blocks):
            for block in sorted(page_blocks[page_number], key=lambda item: (item["bbox"][1], item["bbox"][0], item["block_number"])):
                x0, y0, x1, y1 = block["bbox"]
                if block["block_type"] != 0:
                    drops["non_text_block"] += 1
                    continue
                if not block["raw"]:
                    drops["blank_block"] += 1
                    continue
                if y1 <= 0.08 * block["height"] or y0 >= 0.92 * block["height"]:
                    drops["margin_block"] += 1
                    continue
                if block["key"] in recurrent:
                    drops["recurrent_block"] += 1
                    continue
                if any(intersection_fraction(block["bbox"], table) >= 0.25 for table in block["tables"]):
                    drops["table_overlap_block"] += 1
                    continue
                for sentence in SENTENCE_SPLIT_RE.split(block["raw"]):
                    sentence = normalize_space(sentence)
                    if len(sentence) < 35 or len(WORD_RE.findall(sentence)) < 6:
                        drops["short_unit"] += 1
                        continue
                    normalized = normalize_match(sentence)
                    digest = sha256_text(normalized)
                    if digest in seen:
                        drops["duplicate_unit"] += 1
                        continue
                    seen.add(digest)
                    units.append(
                        {
                            "page": page_number,
                            "block_number": block["block_number"],
                            "x0_ratio": x0 / block["width"],
                            "y0_ratio": y0 / block["height"],
                            "x1_ratio": x1 / block["width"],
                            "y1_ratio": y1 / block["height"],
                            "word_count": len(WORD_RE.findall(sentence)),
                            "character_count": len(sentence),
                            "normalized_sha256": digest,
                            "legacy_exact_match": int(digest in legacy_hashes),
                        }
                    )
        document.close()
        aggregate_drops.update(drops)
        exact_overlap = sum(unit["legacy_exact_match"] for unit in units)
        long_units = sum(unit["word_count"] > 100 for unit in units)
        report_rows.append(
            {
                "doc_id": doc_id,
                "split": frozen["split"],
                "source_pdf_sha256": observed_hash,
                "source_pages": int(frozen["source_page_count"]),
                "candidate_min_page": start_page,
                "processed_pages": int(frozen["source_page_count"]) - start_page + 1,
                "source_blocks": source_blocks,
                "narrow_blocks": narrow_blocks,
                "detected_tables": detected_tables,
                "table_detection_failures": table_failures,
                "legacy_units": len(frozen["candidate_sentences"]),
                "layout_units": len(units),
                "layout_exact_legacy_overlap": exact_overlap,
                "layout_exact_legacy_overlap_fraction": exact_overlap / len(units) if units else 0.0,
                "layout_units_over_100_words": long_units,
                "layout_units_over_100_fraction": long_units / len(units) if units else 0.0,
                "maximum_layout_unit_words": max((unit["word_count"] for unit in units), default=0),
                **{f"dropped_{reason}": count for reason, count in sorted(drops.items())},
            }
        )

        if units:
            selected_indexes = {0, len(units) // 2, max(range(len(units)), key=lambda index: units[index]["word_count"])}
            for sample_index in sorted(selected_indexes):
                sample_rows.append({"doc_id": doc_id, "sample_ordinal": sample_index + 1, **units[sample_index]})

    public_schema_check(report_rows)
    public_schema_check(sample_rows)
    args.output.mkdir(parents=True)
    all_fields = sorted({key for row in report_rows for key in row})
    normalized_report_rows = [{key: row.get(key, 0) for key in all_fields} for row in report_rows]
    with (args.output / "layout_unit_per_report.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=all_fields)
        writer.writeheader()
        writer.writerows(normalized_report_rows)
    write_csv(args.output / "layout_unit_sample_audit.csv", sample_rows)

    summary = {
        "analysis_id": "C2GES-postrun-layout-aware-block-unit-audit-v1",
        "status": "post_result_extraction_diagnostic_not_confirmatory",
        "runtime": {"python": platform.python_version(), "pymupdf": fitz.__version__, "platform": platform.platform()},
        "inputs": {
            "manifest_sha256": sha256_file(args.manifest),
            "dev_sha256": sha256_file(args.dev),
            "test_sha256": sha256_file(args.test),
        },
        "reports": len(report_rows),
        "source_pdf_hashes": pdf_hashes,
        "legacy_units": sum(row["legacy_units"] for row in report_rows),
        "layout_units": sum(row["layout_units"] for row in report_rows),
        "layout_exact_legacy_overlap": sum(row["layout_exact_legacy_overlap"] for row in report_rows),
        "layout_units_over_100_words": sum(row["layout_units_over_100_words"] for row in report_rows),
        "detected_tables": sum(row["detected_tables"] for row in report_rows),
        "table_detection_failures": sum(row["table_detection_failures"] for row in report_rows),
        "drop_counts": dict(sorted(aggregate_drops.items())),
        "privacy": "Public outputs contain no source, candidate, reference, title, or URL text.",
        "limitations": [
            "post-result diagnostic on already selected reports",
            "block and table detection are heuristic",
            "no ranking, ROUGE, or human-validity claim",
        ],
    }
    (args.output / "layout_unit_audit.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# C2GES layout-aware extraction-unit audit",
        "",
        "Status: post-result, nonverbatim extraction diagnostic. No model ranking or reference scoring was performed.",
        "",
        f"Across {summary['reports']} included reports, the frozen page-wide pipeline contained {summary['legacy_units']:,} units. The block-preserving PyMuPDF audit produced {summary['layout_units']:,} units; {summary['layout_exact_legacy_overlap']:,} were exact normalized matches to legacy units. It detected {summary['detected_tables']:,} table regions and recorded {summary['table_detection_failures']} page-level table-detection failures. {summary['layout_units_over_100_words']} retained block-preserving units exceeded 100 words.",
        "",
        "The lower or higher unit count is not a quality score. The audit demonstrates a reproducible block/page boundary and supplies hashed samples for manual checking without redistributing report text. Prospective ranking and independent human review remain required.",
        "",
    ]
    (args.output / "LAYOUT_UNIT_AUDIT_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"status": "PASS", "reports": len(report_rows), "layout_units": summary["layout_units"], "output": str(args.output)}))


if __name__ == "__main__":
    main()
