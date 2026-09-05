#!/usr/bin/env python3
"""Build layout-aware C2GES candidates on development reports only.

Verbatim text is written exclusively to a caller-provided private directory.
The public audit directory contains locators, hashes, counts, and blank review
fields but no title, URL, source text, candidate text, or reference text.
"""

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
from typing import Any, Iterable

import fitz
from transformers import AutoTokenizer


WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])")
LIST_RE = re.compile(r"^\s*(?:[•●▪◦‣\-–—]|\(?[A-Za-z0-9]{1,3}[.)])\s+")
CAPTION_RE = re.compile(r"^\s*(?:figure|fig\.?|table)\s+[A-Za-z0-9]+(?:[.:]|\s)", re.I)
TERMINAL_RE = re.compile(r"[.!?][\"')\]]?$")
FORBIDDEN_PUBLIC_KEYS = {"text", "reference", "summary", "title", "url", "source_url"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest().upper()


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def normalize_match(text: str) -> str:
    return normalize_space(re.sub(r"[^A-Za-z0-9]+", " ", text)).lower()


def recurrent_key(text: str) -> str:
    return normalize_space(re.sub(r"\b\d+\b", " ", normalize_match(text)))


def word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def bbox_overlap_fraction(left: tuple[float, float, float, float], right: tuple[float, float, float, float]) -> float:
    x0, y0 = max(left[0], right[0]), max(left[1], right[1])
    x1, y1 = min(left[2], right[2]), min(left[3], right[3])
    intersection = max(0.0, x1 - x0) * max(0.0, y1 - y0)
    area = max(1e-9, (left[2] - left[0]) * (left[3] - left[1]))
    return intersection / area


def join_lines(lines: Iterable[str]) -> str:
    merged: list[str] = []
    for raw in lines:
        value = normalize_space(raw)
        if not value:
            continue
        if merged and merged[-1].endswith("-") and value[:1].islower():
            merged[-1] = merged[-1][:-1] + value
        else:
            merged.append(value)
    return normalize_space(" ".join(merged))


def classify_unit(text: str, median_font: float, max_font: float, bold: bool, y0_ratio: float) -> str:
    words = word_count(text)
    if CAPTION_RE.match(text):
        return "caption"
    if LIST_RE.match(text):
        return "list_item"
    if words <= 24 and (max_font >= median_font * 1.15 or (bold and not TERMINAL_RE.search(text))):
        return "heading"
    if y0_ratio >= 0.82 and max_font <= median_font * 0.90:
        return "footnote"
    return "body"


def split_block(text: str, unit_type: str) -> list[str]:
    if unit_type != "body":
        return [text]
    return [normalize_space(value) for value in SENTENCE_SPLIT_RE.split(text) if normalize_space(value)]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_public_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    keys = {key.lower() for row in rows for key in row}
    forbidden = keys & FORBIDDEN_PUBLIC_KEYS
    if forbidden:
        raise AssertionError(f"verbatim-capable public fields forbidden: {sorted(forbidden)}")
    fields = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(({key: row.get(key, "") for key in fields} for row in rows))


def extract_blocks(page: fitz.Page) -> tuple[list[dict[str, Any]], list[Any], int]:
    try:
        tables = list(page.find_tables().tables)
        table_failures = 0
    except Exception:
        tables, table_failures = [], 1
    table_boxes = [tuple(float(value) for value in table.bbox) for table in tables]
    blocks: list[dict[str, Any]] = []
    page_dict = page.get_text("dict", sort=True)
    for block_index, block in enumerate(page_dict.get("blocks", [])):
        if block.get("type") != 0:
            continue
        line_texts: list[str] = []
        fonts: list[float] = []
        bold = False
        for line in block.get("lines", []):
            spans = line.get("spans", [])
            line_texts.append("".join(span.get("text", "") for span in spans))
            for span in spans:
                fonts.append(float(span.get("size", 0.0)))
                bold = bold or "bold" in str(span.get("font", "")).lower()
        text = join_lines(line_texts)
        bbox = tuple(float(value) for value in block["bbox"])
        blocks.append({
            "block_index": block_index,
            "bbox": bbox,
            "text": text,
            "fonts": fonts,
            "max_font": max(fonts, default=0.0),
            "bold": bold,
            "table_overlap": max((bbox_overlap_fraction(bbox, table_box) for table_box in table_boxes), default=0.0),
        })
    return blocks, tables, table_failures


def build_report(pdf: Path, report: dict[str, Any], tokenizer: Any) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    document = fitz.open(pdf)
    page_count = document.page_count
    start_page = int(report["candidate_min_page"])
    raw_pages: dict[int, dict[str, Any]] = {}
    recurrence: dict[str, set[int]] = defaultdict(set)
    font_sizes: list[float] = []
    table_failures = 0
    detected_tables = 0
    for page_number in range(start_page, document.page_count + 1):
        page = document[page_number - 1]
        blocks, tables, failures = extract_blocks(page)
        table_failures += failures
        detected_tables += len(tables)
        raw_pages[page_number] = {"width": float(page.rect.width), "height": float(page.rect.height), "blocks": blocks, "tables": tables}
        for block in blocks:
            key = recurrent_key(block["text"])
            if key:
                recurrence[key].add(page_number)
            if block["table_overlap"] < 0.25:
                font_sizes.extend(size for size in block["fonts"] if size > 0)
    median_font = statistics.median(font_sizes) if font_sizes else 10.0
    recurrence_threshold = max(3, math.ceil(len(raw_pages) * 0.20))
    recurrent = {key for key, pages in recurrence.items() if len(pages) >= recurrence_threshold}
    drops: Counter[str] = Counter()
    provisional: list[dict[str, Any]] = []
    source_order = 0

    for page_number, page_data in raw_pages.items():
        width, height = page_data["width"], page_data["height"]
        page_elements: list[dict[str, Any]] = []
        for table_index, table in enumerate(page_data["tables"]):
            extracted = table.extract() or []
            for row_index, cells in enumerate(extracted):
                row_text = join_lines(str(cell or "") for cell in cells)
                if word_count(row_text) < 3:
                    drops["short_table_row"] += 1
                    continue
                bbox = tuple(float(value) for value in table.bbox)
                page_elements.append({
                    "kind": "table", "text": row_text, "bbox": bbox,
                    "table_index": table_index, "row_index": row_index,
                })
        page_elements.extend({"kind": "block", **block} for block in page_data["blocks"])
        page_elements.sort(key=lambda value: (
            value["bbox"][1], value["bbox"][0],
            0 if value["kind"] == "block" else 1,
            value.get("block_index", value.get("table_index", 0)), value.get("row_index", 0),
        ))
        for element in page_elements:
            if element["kind"] == "table":
                source_order += 1
                bbox = element["bbox"]
                provisional.append({
                    "text": element["text"], "unit_type": "table_unit", "page_start": page_number,
                    "page_end": page_number,
                    "block_ids": [f"t{element['table_index']}:r{element['row_index']}"],
                    "bbox": bbox, "source_order": source_order, "boundary_status": "table_row",
                    "x0_ratio": bbox[0] / width, "y0_ratio": bbox[1] / height,
                    "x1_ratio": bbox[2] / width, "y1_ratio": bbox[3] / height,
                })
                continue
            block = element
            text = block["text"]
            bbox = block["bbox"]
            if not text:
                drops["blank_block"] += 1
                continue
            if bbox[3] <= 0.06 * height or bbox[1] >= 0.94 * height:
                drops["margin_block"] += 1
                continue
            if recurrent_key(text) in recurrent:
                drops["recurrent_header_footer"] += 1
                continue
            if block["table_overlap"] >= 0.25:
                drops["table_source_block_isolated"] += 1
                continue
            unit_type = classify_unit(text, median_font, block["max_font"], block["bold"], bbox[1] / height)
            for segment in split_block(text, unit_type):
                if word_count(segment) < (3 if unit_type in {"heading", "caption", "footnote", "list_item"} else 6):
                    drops[f"short_{unit_type}"] += 1
                    continue
                source_order += 1
                provisional.append({
                    "text": segment, "unit_type": unit_type, "page_start": page_number,
                    "page_end": page_number, "block_ids": [f"b{block['block_index']}"],
                    "bbox": bbox, "source_order": source_order,
                    "boundary_status": "complete" if TERMINAL_RE.search(segment) or unit_type != "body" else "possible_fragment",
                    "x0_ratio": bbox[0] / width, "y0_ratio": bbox[1] / height,
                    "x1_ratio": bbox[2] / width, "y1_ratio": bbox[3] / height,
                })

    # Repair a conservative cross-block/page continuation only when the previous
    # body fragment lacks punctuation and the following body unit starts lower-case.
    repaired: list[dict[str, Any]] = []
    for unit in sorted(provisional, key=lambda value: (value["page_start"], value["source_order"])):
        if (repaired and repaired[-1]["unit_type"] == unit["unit_type"] == "body"
                and repaired[-1]["boundary_status"] == "possible_fragment"
                and unit["text"][:1].islower()
                and unit["page_start"] - repaired[-1]["page_end"] <= 1):
            previous = repaired[-1]
            previous["text"] = join_lines([previous["text"], unit["text"]])
            previous["page_end"] = unit["page_end"]
            previous["block_ids"].extend(unit["block_ids"])
            previous["boundary_status"] = "repaired_cross_boundary" if TERMINAL_RE.search(previous["text"]) else "possible_fragment"
            drops["repaired_cross_boundary"] += 1
        else:
            repaired.append(unit)

    reference_norm = normalize_match(report["reference_summary"])
    seen: set[str] = set()
    units: list[dict[str, Any]] = []
    for unit in repaired:
        normalized = normalize_match(unit["text"])
        if not normalized:
            drops["empty_normalized"] += 1
            continue
        if normalized in seen:
            drops["duplicate_unit"] += 1
            continue
        if len(normalized) >= 50 and normalized[:50] in reference_norm:
            drops["reference_overlap"] += 1
            continue
        seen.add(normalized)
        token_count = len(tokenizer(unit["text"], add_special_tokens=True, truncation=False)["input_ids"])
        unit_id = f"u{len(units) + 1:05d}"
        units.append({
            "sid": unit_id, "text": unit["text"], "page": unit["page_start"],
            "page_start": unit["page_start"], "page_end": unit["page_end"],
            "unit_type": unit["unit_type"], "block_ids": unit["block_ids"],
            "source_order": len(units) + 1, "word_count": word_count(unit["text"]),
            "tokenizer_length": token_count, "boundary_status": unit["boundary_status"],
            "normalized_sha256": sha256_text(normalized),
            "x0_ratio": unit["x0_ratio"], "y0_ratio": unit["y0_ratio"],
            "x1_ratio": unit["x1_ratio"], "y1_ratio": unit["y1_ratio"],
        })
    document.close()
    private_row = dict(report)
    private_row["candidate_sentences"] = units
    private_row["candidate_count"] = len(units)
    private_row["candidate_builder"] = "layout_candidate_builder_dev_pilot_v2"
    types = Counter(unit["unit_type"] for unit in units)
    audit = {
        "doc_id": report["doc_id"], "report_series_id": report["report_series_id"],
        "source_pdf_sha256": sha256_file(pdf), "source_pages": page_count,
        "candidate_min_page": start_page, "candidate_count": len(units),
        "detected_tables": detected_tables, "table_detection_failures": table_failures,
        "possible_fragments": sum(unit["boundary_status"] == "possible_fragment" for unit in units),
        "repaired_boundaries": sum(unit["boundary_status"] == "repaired_cross_boundary" for unit in units),
        "units_over_256_tokens": sum(unit["tokenizer_length"] > 256 for unit in units),
        "max_words": max((unit["word_count"] for unit in units), default=0),
        "max_tokenizer_length": max((unit["tokenizer_length"] for unit in units), default=0),
        **{f"units_{name}": types.get(name, 0) for name in ("body", "heading", "list_item", "table_unit", "caption", "footnote")},
        **{f"dropped_{name}": count for name, count in sorted(drops.items())},
    }
    sample_rows = [{
        "doc_id": report["doc_id"], "candidate_id": unit["sid"],
        "page_start": unit["page_start"], "page_end": unit["page_end"],
        "unit_type": unit["unit_type"], "normalized_sha256": unit["normalized_sha256"],
        "word_count": unit["word_count"], "tokenizer_length": unit["tokenizer_length"],
        "boundary_status": unit["boundary_status"], "x0_ratio": round(unit["x0_ratio"], 6),
        "y0_ratio": round(unit["y0_ratio"], 6), "x1_ratio": round(unit["x1_ratio"], 6),
        "y1_ratio": round(unit["y1_ratio"], 6), "reviewer_a_validity": "",
        "reviewer_b_validity": "", "contamination_type": "", "adjudication": "", "notes_nonverbatim": "",
    } for unit in units]
    return private_row, audit, sample_rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--dev", type=Path, required=True)
    parser.add_argument("--tokenizer-snapshot", type=Path, required=True)
    parser.add_argument("--private-output", type=Path, required=True)
    parser.add_argument("--public-audit-output", type=Path, required=True)
    args = parser.parse_args()
    for output in (args.private_output, args.public_audit_output):
        if output.exists():
            raise FileExistsError(f"refusing existing output: {output}")
        output.mkdir(parents=True)

    manifest_rows = json.loads(args.manifest.read_text(encoding="utf-8"))
    manifest = {row["doc_id"]: row for row in manifest_rows}
    reports = load_jsonl(args.dev)
    if not reports or any(row.get("split") != "dev" for row in reports):
        raise AssertionError("development-only input required")
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer_snapshot, local_files_only=True)
    private_rows: list[dict[str, Any]] = []
    audit_rows: list[dict[str, Any]] = []
    sample_pool: list[dict[str, Any]] = []
    for index, report in enumerate(reports, 1):
        print(f"[{index}/{len(reports)}] layout candidates for {report['doc_id']}")
        source = manifest[report["doc_id"]]
        pdf = args.source_root / source["local_pdf"]
        if sha256_file(pdf) != report["source_pdf_sha256"].upper():
            raise AssertionError(f"source hash mismatch: {report['doc_id']}")
        private, audit, samples = build_report(pdf, report, tokenizer)
        private_rows.append(private)
        audit_rows.append(audit)
        sample_pool.extend(samples)

    # Deterministic stratified sample by unit type plus risk-enriched boundary
    # and long-token strata. A row can belong to more than one stratum.
    selected_by_key: dict[tuple[str, str], dict[str, Any]] = {}

    def add_sample(row: dict[str, Any], stratum: str) -> None:
        key = (row["doc_id"], row["candidate_id"])
        if key not in selected_by_key:
            selected_by_key[key] = {**row, "sampling_strata": stratum}
        else:
            current = set(selected_by_key[key]["sampling_strata"].split("|"))
            current.add(stratum)
            selected_by_key[key]["sampling_strata"] = "|".join(sorted(current))

    for unit_type in ("body", "heading", "list_item", "table_unit", "caption", "footnote"):
        candidates = [row for row in sample_pool if row["unit_type"] == unit_type]
        candidates.sort(key=lambda row: sha256_text(f"{row['doc_id']}|{row['candidate_id']}|20260906"))
        for row in candidates[:30]:
            add_sample(row, f"unit_type:{unit_type}")
    for status, limit in (("possible_fragment", 40), ("repaired_cross_boundary", 40)):
        candidates = [row for row in sample_pool if row["boundary_status"] == status]
        candidates.sort(key=lambda row: sha256_text(f"{row['doc_id']}|{row['candidate_id']}|{status}|20260906"))
        for row in candidates[:limit]:
            add_sample(row, f"boundary:{status}")
    long_candidates = [row for row in sample_pool if int(row["tokenizer_length"]) > 256]
    long_candidates.sort(key=lambda row: sha256_text(f"{row['doc_id']}|{row['candidate_id']}|long|20260906"))
    for row in long_candidates[:30]:
        add_sample(row, "tokenizer_length:gt256")
    selected_samples = list(selected_by_key.values())
    selected_samples.sort(key=lambda row: (row["doc_id"], row["page_start"], row["candidate_id"]))

    private_dataset = args.private_output / "layout_dev_candidates_v1.jsonl"
    write_jsonl(private_dataset, private_rows)
    write_public_csv(args.public_audit_output / "layout_candidate_audit.csv", audit_rows)
    write_public_csv(args.public_audit_output / "layout_boundary_sample_blank.csv", selected_samples)
    manifest_value = {
        "schema": "c2ges-layout-dev-pilot-v2", "status": "DEVELOPMENT_ONLY_PENDING_HUMAN_BOUNDARY_AUDIT",
        "external_test_accessed": False, "confirmatory_claims_allowed": False,
        "reports": len(reports), "series": len({row["report_series_id"] for row in reports}),
        "total_candidates": sum(row["candidate_count"] for row in audit_rows),
        "sample_rows": len(selected_samples), "sample_types": dict(Counter(row["unit_type"] for row in selected_samples)),
        "sample_strata": dict(Counter(stratum for row in selected_samples for stratum in row["sampling_strata"].split("|"))),
        "tokenizer": {"name": "sentence-transformers/all-MiniLM-L6-v2", "revision": args.tokenizer_snapshot.name,
                      "class": tokenizer.__class__.__name__, "vocab_size": tokenizer.vocab_size, "production_max_length": 256},
        "inputs": {"source_manifest_sha256": sha256_file(args.manifest), "dev_sha256": sha256_file(args.dev),
                   "source_pdf_sha256": {row["doc_id"]: row["source_pdf_sha256"] for row in audit_rows}},
        "outputs": {"private_dataset_sha256": sha256_file(private_dataset),
                    "public_audit_sha256": sha256_file(args.public_audit_output / "layout_candidate_audit.csv"),
                    "blank_sample_sha256": sha256_file(args.public_audit_output / "layout_boundary_sample_blank.csv")},
        "privacy": "Verbatim candidate/reference text is confined to the caller-provided private output outside the release scope.",
        "runtime": {"python": platform.python_version(), "pymupdf": fitz.__version__},
    }
    write_json(args.public_audit_output / "LAYOUT_DEV_PILOT_MANIFEST.json", manifest_value)
    print(json.dumps({"status": "PASS", "reports": len(reports), "candidates": manifest_value["total_candidates"],
                      "sample_rows": len(selected_samples), "external_test_accessed": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
