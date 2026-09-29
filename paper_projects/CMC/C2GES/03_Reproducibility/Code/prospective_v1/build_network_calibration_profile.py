#!/usr/bin/env python3
"""Build a non-verbatim structural profile from private calibration PDFs.

The script never writes extracted report text. It emits only counts, length
statistics, hashes, and coarse layout categories suitable for local synthetic
fixture calibration.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import statistics
from collections import Counter
from pathlib import Path

import fitz

UNIT_TYPES = ("body", "heading", "list_item", "table_unit", "caption", "footnote")
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*")
LIST_RE = re.compile(r"^\s*(?:[•‣▪◦*-]|\(?\d{1,2}[.)]|[A-Za-z][.)])\s+")
HEADING_RE = re.compile(r"^\s*(?:\d+(?:\.\d+)*\s+)?[A-Z][A-Z0-9 &/():,.-]{4,}\s*$")
CAPTION_RE = re.compile(r"^\s*(?:figure|fig\.?|table|chart)\s+\d+", re.I)


def words(text: str) -> int:
    return len(WORD_RE.findall(text))


def quantile(values: list[float], p: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    position = (len(ordered) - 1) * p
    lo, hi = math.floor(position), math.ceil(position)
    if lo == hi:
        return ordered[lo]
    return ordered[lo] * (hi - position) + ordered[hi] * (position - lo)


def describe(values: list[float]) -> dict[str, float]:
    if not values:
        return {"n": 0, "mean": 0.0, "median": 0.0, "q25": 0.0, "q75": 0.0,
                "min": 0.0, "max": 0.0}
    return {"n": len(values), "mean": statistics.mean(values),
            "median": statistics.median(values), "q25": quantile(values, .25),
            "q75": quantile(values, .75), "min": min(values), "max": max(values)}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def block_text_and_size(block: dict) -> tuple[str, float]:
    fragments: list[str] = []
    sizes: list[float] = []
    for line in block.get("lines", []):
        line_text = "".join(span.get("text", "") for span in line.get("spans", []))
        if line_text.strip():
            fragments.append(line_text.strip())
        sizes.extend(float(span.get("size", 0)) for span in line.get("spans", []) if span.get("text", "").strip())
    return " ".join(fragments), statistics.median(sizes) if sizes else 0.0


def classify(text: str, font_size: float, page_height: float, y0: float,
             body_font: float) -> str:
    count = words(text)
    numeric = sum(character.isdigit() for character in text)
    nonspace = sum(not character.isspace() for character in text)
    if CAPTION_RE.match(text):
        return "caption"
    if y0 >= page_height * .9 or (font_size and body_font and font_size <= body_font * .72):
        return "footnote"
    if LIST_RE.match(text):
        return "list_item"
    if count <= 22 and ((font_size and body_font and font_size >= body_font * 1.14) or HEADING_RE.match(text)):
        return "heading"
    if count >= 4 and nonspace and numeric / nonspace >= .28:
        return "table_unit"
    return "body"


def analyze_pdf(path: Path) -> dict:
    document = fitz.open(path)
    page_word_counts: list[int] = []
    unit_word_counts: list[int] = []
    token_over_256 = 0
    counts: Counter[str] = Counter()
    for page in document:
        blocks = [block for block in page.get_text("dict").get("blocks", []) if block.get("type") == 0]
        parsed = [(*block_text_and_size(block), float(block.get("bbox", [0, 0, 0, 0])[1])) for block in blocks]
        fonts = [font for text, font, _ in parsed if text and font > 0]
        body_font = statistics.median(fonts) if fonts else 10.0
        page_words = 0
        for text, font_size, y0 in parsed:
            count = words(text)
            if count == 0:
                continue
            page_words += count
            unit_word_counts.append(count)
            token_over_256 += int(count > 190)
            counts[classify(text, font_size, float(page.rect.height), y0, body_font)] += 1
        page_word_counts.append(page_words)
    return {
        "source_id": path.stem,
        "file_name": path.name,
        "sha256": sha256(path),
        "file_bytes": path.stat().st_size,
        "page_count": len(document),
        "candidate_count": sum(counts.values()),
        "units_over_256_tokens": token_over_256,
        "page_words": describe(page_word_counts),
        "unit_words": describe(unit_word_counts),
        "unit_counts": {kind: counts[kind] for kind in UNIT_TYPES},
    }


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    profiles = [analyze_pdf(path) for path in sorted(args.pdf_dir.glob("*.pdf"))]
    if not profiles:
        raise SystemExit("no PDF files found")

    metadata_rows = [{"doc_id": row["source_id"], "inclusion_status": "included",
                      "page_count": row["page_count"], "reference_words": 145}
                     for row in profiles]
    layout_rows = []
    for row in profiles:
        layout = {"doc_id": row["source_id"], "source_pages": row["page_count"],
                  "candidate_count": row["candidate_count"],
                  "units_over_256_tokens": row["units_over_256_tokens"]}
        layout.update({f"units_{kind}": row["unit_counts"][kind] for kind in UNIT_TYPES})
        layout_rows.append(layout)
    write_csv(args.output_dir / "network_metadata_profile.csv",
              ["doc_id", "inclusion_status", "page_count", "reference_words"], metadata_rows)
    write_csv(args.output_dir / "network_layout_profile.csv",
              ["doc_id", "source_pages", "candidate_count", "units_over_256_tokens",
               *(f"units_{kind}" for kind in UNIT_TYPES)], layout_rows)
    write_csv(args.output_dir / "NETWORK_PDF_HASHES.csv",
              ["source_id", "file_name", "sha256", "file_bytes"],
              [{key: row[key] for key in ("source_id", "file_name", "sha256", "file_bytes")}
               for row in profiles])
    aggregate = {
        "schema": "c2ges-network-calibration-profile-v1",
        "contains_report_text": False,
        "confirmatory_e1_eligible": False,
        "report_count": len(profiles),
        "page_count": describe([row["page_count"] for row in profiles]),
        "candidate_count": describe([row["candidate_count"] for row in profiles]),
        "page_words": describe([value for row in profiles for value in [row["page_words"]["median"]]]),
        "unit_words": describe([value for row in profiles for value in [row["unit_words"]["median"]]]),
        "unit_type_totals": {kind: sum(row["unit_counts"][kind] for row in profiles) for kind in UNIT_TYPES},
        "reports": profiles,
        "interpretation_boundary": "Coarse automated PDF-layout statistics only; not semantic ground truth and not a confirmatory external test.",
    }
    (args.output_dir / "CALIBRATION_DISTRIBUTION_PROFILE.json").write_text(
        json.dumps(aggregate, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "reports": len(profiles),
                      "profile": str(args.output_dir / "CALIBRATION_DISTRIBUTION_PROFILE.json")}))


if __name__ == "__main__":
    main()
