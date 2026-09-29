#!/usr/bin/env python3
"""Build a non-confirmatory external corpus from official public PDF reports.

The builder deliberately separates an official summary section from extraction
candidates.  Its output is exploratory because source metadata was inspected
before this protocol existed and because the reference extraction is automated.
No manuscript-confirmatory flag can be emitted by this script.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import fitz


WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")

# One-indexed pages, fixed from contents/headings before metric computation.
REFERENCE_PAGES = {
    "ext_001_entsoe_see_2024": (6, 10),
    "ext_002_entsoe_mepso_2025": (4, 8),
    "ext_003_entsoe_czech_2025": (4, 6),
    "ext_004_nerc_gmd_2024": (1, 1),
    "ext_005_nerc_low_wind": (1, 1),
    "ext_006_nerc_large_load_loss": (1, 1),
    "ext_008_transpower_tower_130": (4, 8),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def clean(text: str) -> str:
    text = text.replace("\u00ad", "").replace("ﬁ", "fi").replace("ﬂ", "fl")
    text = re.sub(r"(?<=\w)-\s+(?=[a-z])", "", text)
    return re.sub(r"\s+", " ", text).strip()


def normalized_recurrent(text: str) -> str:
    return re.sub(r"\d+", "#", clean(text).lower())


def page_blocks(doc: fitz.Document) -> list[list[dict[str, Any]]]:
    pages: list[list[dict[str, Any]]] = []
    for page_index, page in enumerate(doc):
        height = page.rect.height
        items: list[dict[str, Any]] = []
        for block in page.get_text("dict").get("blocks", []):
            if block.get("type") != 0:
                continue
            raw_lines = block.get("lines", [])
            spans = [span for line in raw_lines for span in line.get("spans", [])]
            line_records = []
            for line in raw_lines:
                line_spans = line.get("spans", [])
                line_text = clean(" ".join(str(span.get("text", "")) for span in line_spans))
                if line_text:
                    line_records.append({"text": line_text,
                                         "bold": any("bold" in str(span.get("font", "")).lower() for span in line_spans),
                                         "max_font": max((float(span.get("size", 0.0)) for span in line_spans), default=0.0)})
            line_texts = [value["text"] for value in line_records]
            text = clean(" ".join(str(span.get("text", "")) for span in spans))
            if not text:
                continue
            x0, y0, x1, y1 = block["bbox"]
            items.append({
                "page": page_index + 1,
                "text": text,
                "x0": float(x0), "y0": float(y0), "x1": float(x1), "y1": float(y1),
                "page_height": float(height),
                "max_font": max((float(span.get("size", 0.0)) for span in spans), default=0.0),
                "bold": any("bold" in str(span.get("font", "")).lower() for span in spans),
                "line_texts": line_texts,
                "line_records": line_records,
            })
        pages.append(items)
    return pages


def recurrent_margin_texts(pages: list[list[dict[str, Any]]]) -> set[str]:
    counts: Counter[str] = Counter()
    for blocks in pages:
        seen: set[str] = set()
        for block in blocks:
            margin = block["y0"] < 0.09 * block["page_height"] or block["y1"] > 0.91 * block["page_height"]
            key = normalized_recurrent(block["text"])
            if margin and 2 <= len(words(key)) <= 24:
                seen.add(key)
        counts.update(seen)
    threshold = max(3, int(len(pages) * 0.15))
    return {key for key, count in counts.items() if count >= threshold}


def unit_type(block: dict[str, Any], sentence: str) -> str:
    wc = len(words(sentence))
    numeric = sum(ch.isdigit() for ch in sentence) / max(1, len(sentence))
    if block["y1"] > 0.90 * block["page_height"] and wc <= 35:
        return "footnote"
    if re.match(r"^(figure|fig\.|table)\s*\d*", sentence, re.I):
        return "caption"
    if numeric > 0.16 or sentence.count("  ") >= 2 or (sentence.count(";") >= 3 and wc < 80):
        return "table_unit"
    if re.match(r"^(?:[•▪»–-]|\(?[a-z0-9]+[.)])\s+", sentence, re.I):
        return "list_item"
    if (block["bold"] or block["max_font"] >= 13.0) and wc <= 18 and not sentence.endswith((".", "?", "!")):
        return "heading"
    return "body"


def looks_like_heading(line: str, block: dict[str, Any]) -> bool:
    tokens = words(line)
    if not 2 <= len(tokens) <= 18 or line.endswith((".", "?", "!", ";")):
        return False
    title_ratio = sum(token[:1].isupper() for token in tokens) / len(tokens)
    return block["bold"] or block["max_font"] >= 13.0 or title_ratio >= 0.65


def sentences_from_block(block: dict[str, Any]) -> list[str]:
    line_records = list(block.get("line_records") or [{"text": block["text"], "bold": block["bold"], "max_font": block["max_font"]}])
    chunks: list[str] = []
    body_lines: list[str] = []
    for record in line_records:
        line = record["text"]
        line_style = {**block, "bold": record["bold"], "max_font": record["max_font"]}
        boundary = looks_like_heading(line, line_style) or re.match(r"^(figure|fig\.|table)\s*\d+", line, re.I)
        if boundary:
            if body_lines:
                chunks.append(clean(" ".join(body_lines))); body_lines = []
            chunks.append(line)
        else:
            body_lines.append(line)
    if body_lines:
        chunks.append(clean(" ".join(body_lines)))
    parts: list[str] = []
    for chunk in chunks:
        for bullet_part in re.split(r"\s+[»•▪]\s+", clean(chunk)):
            parts.extend(SENTENCE_RE.split(bullet_part))
    accepted: list[str] = []
    for part in parts:
        part = clean(part)
        count = len(words(part))
        if not 5 <= count <= 190:
            continue
        if part[:1].islower():
            continue
        if re.search(r"\b(?:and|or|of|to|from|with|versus|vs\.)$", part, re.I):
            continue
        accepted.append(part)
    return accepted


def reference_summary(pages: list[list[dict[str, Any]]], start: int, end: int) -> str:
    text = clean(" ".join(block["text"] for page in pages[start - 1:end] for block in page))
    text = re.sub(r"^.*?(?:management summary|executive summary|summary and objective|primary takeaways)\s*", "", text, flags=re.I)
    selected: list[str] = []
    total = 0
    for sentence in SENTENCE_RE.split(text):
        sentence = clean(sentence)
        count = len(words(sentence))
        if count < 5:
            continue
        if total + count > 260 and selected:
            break
        selected.append(sentence)
        total += count
        if total >= 180:
            break
    return " ".join(selected)


def build_row(meta: dict[str, str], pdf: Path) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    doc_id = meta["doc_id"]
    doc = fitz.open(pdf)
    pages = page_blocks(doc)
    recurrent = recurrent_margin_texts(pages)
    start, end = REFERENCE_PAGES[doc_id]
    reference = reference_summary(pages, start, end)
    candidates: list[dict[str, Any]] = []
    type_counts: Counter[str] = Counter()
    seen_units: set[str] = set()
    excluded_table_units = 0
    sid = 0
    for blocks in pages:
        for block in blocks:
            if start <= block["page"] <= end:
                continue
            if normalized_recurrent(block["text"]) in recurrent:
                continue
            for sentence in sentences_from_block(block):
                kind = unit_type(block, sentence)
                if kind == "footnote" or len(words(sentence)) < 6:
                    continue
                if kind == "table_unit":
                    excluded_table_units += 1
                    continue
                if kind == "body" and not re.search(r"[.!?][\"')\]]?$", sentence):
                    continue
                if kind == "body" and re.match(r"^(?:MW|kV|Hz|kA|MVA|%)\b", sentence):
                    continue
                normalized = re.sub(r"\W+", " ", sentence.lower()).strip()
                if normalized in seen_units:
                    continue
                seen_units.add(normalized)
                sid += 1
                candidates.append({"sid": f"u{sid:05d}", "page": block["page"], "unit_type": kind, "text": sentence})
                type_counts[kind] += 1
    ref_words = len(words(reference))
    reason = ""
    accepted = 110 <= ref_words <= 260 and len(candidates) >= 40
    if not accepted:
        reason = f"reference_words={ref_words};candidates={len(candidates)}"
    audit = {
        "doc_id": doc_id,
        "report_series_id": meta["report_series_id"],
        "organization": meta["organization"],
        "pdf_sha256": sha256(pdf),
        "pdf_bytes": pdf.stat().st_size,
        "page_count": len(doc),
        "reference_page_start": start,
        "reference_page_end": end,
        "reference_words": ref_words,
        "candidate_count": len(candidates),
        "recurrent_margin_strings_removed": len(recurrent),
        "excluded_table_units": excluded_table_units,
        "accepted": accepted,
        "rejection_reason": reason,
        **{f"units_{kind}": type_counts.get(kind, 0) for kind in ("body", "heading", "list_item", "table_unit", "caption")},
    }
    if not accepted:
        return None, audit
    row = {
        "doc_id": doc_id,
        "report_series_id": meta["report_series_id"],
        "title": meta["title"],
        "split": "exploratory_external",
        "synthetic": False,
        "confirmatory_claims_allowed": False,
        "reference_provenance": "automatically extracted official summary section; not human adjudicated",
        "reference_summary": reference,
        "candidate_sentences": candidates,
    }
    return row, audit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--pdf-dir", type=Path, required=True)
    parser.add_argument("--private-jsonl", type=Path, required=True)
    parser.add_argument("--audit-csv", type=Path, required=True)
    parser.add_argument("--manifest-json", type=Path, required=True)
    args = parser.parse_args()
    rows = list(csv.DictReader(args.inventory.open(encoding="utf-8-sig", newline="")))
    unknown = sorted(set(REFERENCE_PAGES) - {row["doc_id"] for row in rows})
    if unknown:
        raise RuntimeError(f"reference-page registry has unknown inventory rows: {unknown}")
    dataset: list[dict[str, Any]] = []
    audits: list[dict[str, Any]] = []
    missing: list[str] = []
    for meta in rows:
        pdf = args.pdf_dir / meta["local_pdf"]
        if not pdf.is_file():
            missing.append(meta["doc_id"])
            continue
        row, audit = build_row(meta, pdf)
        audits.append(audit)
        if row is not None:
            dataset.append(row)
    args.private_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with args.private_jsonl.open("w", encoding="utf-8", newline="\n") as stream:
        for row in dataset:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    args.audit_csv.parent.mkdir(parents=True, exist_ok=True)
    fields = list(audits[0]) if audits else ["doc_id"]
    with args.audit_csv.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader(); writer.writerows(audits)
    manifest = {
        "schema": "c2ges-exploratory-external-v0",
        "evidence_class": "EXPLORATORY_ONLY",
        "confirmatory_claims_allowed": False,
        "reference_method": "automatic official-summary extraction without human adjudication",
        "inventory_rows": len(rows),
        "downloaded_pdfs": len(audits),
        "accepted_reports": len(dataset),
        "accepted_series": len({row["report_series_id"] for row in dataset}),
        "missing_doc_ids": missing,
        "dataset_sha256": sha256(args.private_jsonl),
        "inventory_sha256": sha256(args.inventory),
        "builder_sha256": sha256(Path(__file__)),
    }
    args.manifest_json.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
