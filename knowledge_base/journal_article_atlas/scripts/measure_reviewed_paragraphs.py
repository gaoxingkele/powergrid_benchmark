"""Compute auditable lengths from explicitly reviewed PDF paragraph spans.

No semantic labels are guessed here. Source prose is not exported: only locators,
hashes, counts and reviewer-written paraphrases are retained. This is not a
general-purpose paragraph detector or a certificate of human calibration.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import fitz


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    # A line-end hyphen followed by a lower-case continuation is treated as PDF
    # word wrapping. This declared convention may merge genuine compounds.
    text = re.sub(r"(?<=[A-Za-z])-\s*\n\s*(?=[a-z])", "", text)
    return re.sub(r"\s+", " ", text).strip()


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*", text)


def percentile(values: list[int], p: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * p
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def measure(map_path: Path) -> dict:
    mapping = json.loads(map_path.read_text(encoding="utf-8"))
    source = (map_path.parent / mapping["source_path"]).resolve()
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if digest != mapping["source_sha256"]:
        raise ValueError("Source SHA mismatch; paragraph map must be re-reviewed")
    doc = fitz.open(source)
    items, used = [], set()
    by_section = defaultdict(list)
    for index, row in enumerate(mapping["paragraphs"], 1):
        section, role, paraphrase, specs = row[:4]
        kind = row[4] if len(row) > 4 else "prose"
        fragments, locators = [], []
        for spec in specs:
            page, block_index = spec[:2]
            block = doc[page - 1].get_text("blocks")[block_index]
            if block[6] != 0:
                raise ValueError(f"Not text: {spec}")
            lines = block[4].splitlines(keepends=True)
            start, end = spec[2:4] if len(spec) == 4 else (0, len(lines))
            if not 0 <= start < end <= len(lines):
                raise ValueError(f"Invalid line range: {spec}")
            for line in range(start, end):
                key = (page, block_index, line)
                if key in used:
                    raise ValueError(f"Duplicate paragraph span: {key}")
                used.add(key)
            fragment = "".join(lines[start:end])
            if kind == "list_item":
                fragment = re.sub(r"^\s*\d+\.\s*", "", fragment)
            fragments.append(fragment)
            locators.append({"page": page, "block_index": block_index,
                             "line_range_half_open": [start, end],
                             "block_bbox": [round(v, 3) for v in block[:4]]})
        cleaned = normalize("\n".join(fragments))
        count = len(words(cleaned))
        if not count:
            raise ValueError("Empty paragraph")
        record = {"id": f"P{index:03}", "section_id": section, "kind": kind,
                  "role_primary": role, "functional_paraphrase": paraphrase,
                  "spans": locators, "words": count,
                  "normalized_text_sha256": hashlib.sha256(cleaned.encode()).hexdigest(),
                  "sentences": None, "tense": "not_assessed", "voice": "not_assessed"}
        items.append(record)
        by_section[section].append(record)
    lengths = [p["words"] for p in items]
    prose = [p["words"] for p in items if p["kind"] == "prose"]
    section_counts = {s: {"units_exclusive": len(ps), "words_exclusive": sum(p["words"] for p in ps),
                          "role_counts": dict(Counter(p["role_primary"] for p in ps))}
                      for s, ps in by_section.items()}
    return {"schema": "atlas_paragraph_measurements/1", "paper_id": mapping["paper_id"],
            "source_sha256": digest, "map_sha256": hashlib.sha256(map_path.read_bytes()).hexdigest(),
            "parser": f"PyMuPDF {fitz.VersionBind}",
            "status": "single_assistant_reviewed_spans_computed_lengths_pending_independent_review",
            "human_calibrated": False,
            "tokenizer": "NFKC; join line-end hyphen before lowercase; ASCII alphanumeric words with internal apostrophe/hyphen; includes citation numbers and inline math tokens; excludes list numbering",
            "scope": "Introduction through Conclusions including future work; no headings/captions/table cells/declarations/references",
            "summary": {"prose_paragraphs": len(prose), "list_items": len(items) - len(prose),
                        "total_units": len(items), "body_words": sum(lengths),
                        "prose_words": sum(prose), "prose_mean_words": statistics.mean(prose),
                        "all_units_mean_words": statistics.mean(lengths),
                        "all_units_median_words": statistics.median(lengths),
                        "all_units_p10_words": percentile(lengths, .1),
                        "all_units_p90_words": percentile(lengths, .9),
                        "quantile_method": "linear interpolation at (n-1)*p"},
            "sections": section_counts, "paragraphs": items}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("map", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    expected = args.map.with_name(args.map.name.replace(".paragraph_map.json", ".paragraphs.json"))
    if not args.map.name.endswith(".paragraph_map.json") or args.output.resolve() != expected.resolve():
        raise ValueError("Output must be the sibling paper_id.paragraphs.json, never a source or map")
    result = measure(args.map)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False))


if __name__ == "__main__":
    main()
