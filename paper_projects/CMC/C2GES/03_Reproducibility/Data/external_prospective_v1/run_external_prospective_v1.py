"""External prospective evaluation v1 for C2GES (protocol frozen before scoring).

Builds candidate units and official-summary references from the frozen corpus of
ENTSO-E and NERC incident reports, then runs the shipped selectors
(no-path C2GES, Full C2GES at the frozen path weight 0.10, TextRank) at 110 and
260 words, and reports paired differences with bootstrap intervals and exact
sign-flip enumeration.

Extraction implementation (frozen with this script): PyMuPDF text blocks per
page; a block is the reference-summary start when its stripped text matches
`^(executive\\s+)?summary\\b` in the first 12 pages; the reference continues to
the next heading-like block (no terminal period, <= 12 words) or 2000 words;
candidates are the blocks after the reference with at least six word tokens.

Usage:
    python -B run_external_prospective_v1.py --json external_prospective_v1.json
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
import re
import statistics
import sys
from pathlib import Path

import fitz

HERE = Path(__file__).resolve().parent
RUN_CODE = HERE.parent / "03_Reproducibility" / "Code" / "rsi_path_v1"
sys.path.insert(0, str(RUN_CODE))
import rsi_common as R  # noqa: E402

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*")
SUMMARY_RE = re.compile(r"^\s*(?:\d+(?:\.\d+)*\.?\s+)?(?:executive\s+|management\s+)?summary\b", re.I)  # v1.3
HEADING_MAX_WORDS = 12
SUMMARY_PAGE_WINDOW = 25  # protocol amendment v1.1 (was 12)
SUMMARY_TITLE_MAX_WORDS = 8  # protocol amendment v1.1 (was 6)
MIN_UNIT_WORDS = 6
MAX_REFERENCE_WORDS = 2000
MIN_REFERENCE_WORDS = 100  # protocol amendment v1.4: a 10-14 word stub is not a reference
MAX_CANDIDATES = 2000  # largest retained NERC report had 1898 units; keeps the O(n^2) graph bounded
FAMILY_RULES = (
    ("entsoe_grid", r"(grid.incident|incident.report|factual.report|disturbance.statistics|South-East|MEPSO|Spain)"),
    ("entsoe_market", r"(SDAC|SIDC|decoupling)"),
    ("nerc", r"^(blackstart|incident[_-]review)"),
)


def family_of(name: str) -> str:
    for family, pattern in FAMILY_RULES:
        if re.search(pattern, name, re.I):
            return family
    return "other"


def blocks_of(pdf: Path) -> list[tuple[int, str]]:
    doc = fitz.open(pdf)
    out = []
    for page_index, page in enumerate(doc, 1):
        for block in page.get_text("blocks"):
            text = re.sub(r"\s+", " ", block[4] or "").strip()
            if text:
                out.append((page_index, text))
    doc.close()
    return out


def looks_like_heading(text: str) -> bool:
    words = WORD_RE.findall(text)
    if not words or len(words) > HEADING_MAX_WORDS:
        return False
    return not text.rstrip().endswith((".", ":", ";", ",", "?"))


def running_headers(blocks: list[tuple[int, str]]) -> set[str]:
    """Blocks appearing on three or more pages are running headers or footers."""
    pages: dict[str, set[int]] = {}
    for page, text in blocks:
        pages.setdefault(text, set()).add(page)
    return {text for text, seen in pages.items() if len(seen) >= 3}


def is_layout_noise(text: str, headers: set[str]) -> bool:
    """Dot-leading table-of-contents rows, page numbers, running heads, fragments."""
    if re.search(r"\.{3,}", text):
        return True
    if text in headers:
        return True
    return len(WORD_RE.findall(text)) < 4


def reference_noise(text: str, headers: set[str]) -> bool:
    """Inside a summary section only running heads and dot-leaders are dropped.

    Bulleted summary items are often three to five words long, so the general
    fragment filter must not be applied while collecting the reference text
    (protocol amendment v1.4).
    """
    if re.search(r"\.{3,}", text):
        return True
    if text in headers:
        return True
    return len(WORD_RE.findall(text)) == 0


def build_report(pdf: Path) -> dict | None:
    blocks = blocks_of(pdf)
    if not blocks:
        return None
    start = None
    for index, (page, text) in enumerate(blocks):
        if page > SUMMARY_PAGE_WINDOW:
            break
        if SUMMARY_RE.match(text) and len(WORD_RE.findall(text)) <= SUMMARY_TITLE_MAX_WORDS:
            start = index
            break
    if start is None:
        return None
    headers = running_headers(blocks)
    reference_blocks: list[str] = []
    reference_words = 0
    cursor = start + 1
    while cursor < len(blocks):
        text = blocks[cursor][1]
        words = len(WORD_RE.findall(text))
        if reference_noise(text, headers):
            cursor += 1
            continue
        if looks_like_heading(text) and len(reference_blocks) >= 2:
            break
        if reference_words + words > MAX_REFERENCE_WORDS:
            break
        reference_blocks.append(text)
        reference_words += words
        cursor += 1
    candidates = []
    for page, text in blocks[cursor:]:
        if len(WORD_RE.findall(text)) < MIN_UNIT_WORDS:
            continue
        if re.fullmatch(r"\d+", text):
            continue
        if is_layout_noise(text, headers):
            continue
        candidates.append(text)
        if len(candidates) >= MAX_CANDIDATES:
            break
    if len(reference_blocks) < 2 or len(candidates) < 20:
        return None
    if reference_words < MIN_REFERENCE_WORDS:
        return None
    return {
        "doc_id": pdf.stem,
        "report_series_id": family_of(pdf.stem),
        "reference_summary": " ".join(reference_blocks),
        "candidate_sentences": [
            {"sid": f"{pdf.stem}_u{index:04d}", "text": text} for index, text in enumerate(candidates)
        ],
    }


def bootstrap_interval(values: list[float], draws: int = 10000, seed: int = 20260922) -> list[float]:
    rng = random.Random(seed)
    n = len(values)
    means = []
    for _ in range(draws):
        means.append(statistics.fmean(rng.choice(values) for _ in range(n)))
    means.sort()
    return [means[int(0.025 * draws)], means[int(0.975 * draws) - 1]]


def exact_signflip(values: list[float]) -> float:
    """Two-sided exact sign-flip p over all 2^n assignments (n <= 18)."""
    n = len(values)
    observed = abs(statistics.fmean(values))
    total = 0
    hits = 0
    for signs in itertools.product((1, -1), repeat=n):
        total += 1
        shifted = abs(statistics.fmean(s * v for s, v in zip(signs, values)))
        if shifted >= observed - 1e-12:
            hits += 1
    return hits / total


def holm(pvalues: list[float]) -> list[float]:
    order = sorted(range(len(pvalues)), key=lambda i: pvalues[i])
    adjusted = [0.0] * len(pvalues)
    running = 0.0
    for rank, index in enumerate(order):
        value = (len(pvalues) - rank) * pvalues[index]
        running = max(running, value)
        adjusted[index] = min(1.0, running)
    return adjusted


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", required=True)
    args = parser.parse_args()

    protocol = R.load_protocol()
    settings = protocol["textrank"]
    budgets = [110, 260]

    pdfs = sorted((HERE / "source_pdfs_entsoe").glob("*.pdf")) + sorted((HERE / "source_pdfs").glob("*.pdf"))
    reports = []
    skipped = []
    seen_titles = set()
    for pdf in pdfs:
        row = build_report(pdf)
        if row is None:
            skipped.append({"file": pdf.name, "reason": "no usable summary/candidates"})
            continue
        key = (row["report_series_id"], len(row["candidate_sentences"]) // 50)
        if key in seen_titles:
            skipped.append({"file": pdf.name, "reason": "near-duplicate of a kept report"})
            continue
        seen_titles.add(key)
        reports.append(row)

    rows = []
    for row in reports:
        prepared = R.prepare_report(row)
        for budget in budgets:
            nopath = R.c2ges_select(prepared, utility=None, path_weight=0.0, word_budget=budget)
            full = R.c2ges_select(prepared, utility="historical", path_weight=0.10, word_budget=budget)
            textrank = R.textrank_select(prepared, budget, settings)
            for condition, result in (("no_path", nopath), ("full_path_0.10", full), ("textrank", textrank)):
                rows.append(
                    {
                        "doc_id": row["doc_id"],
                        "report_series_id": row["report_series_id"],
                        "condition": condition,
                        "word_budget": budget,
                        "candidate_units": len(row["candidate_sentences"]),
                        "reference_words": R.word_count(row["reference_summary"]),
                        "actual_words": result["actual_words"],
                        "rougeL_f1": result["rougeL_f1"],
                    }
                )

    by_condition = {}
    contrasts = []
    for budget in budgets:
        for condition in ("no_path", "full_path_0.10", "textrank"):
            values = [r["rougeL_f1"] for r in rows if r["word_budget"] == budget and r["condition"] == condition]
            by_condition[f"{condition}@{budget}"] = {
                "n": len(values),
                "mean": round(statistics.fmean(values), 6) if values else None,
            }
        for condition in ("full_path_0.10", "textrank"):
            pairs = []
            for doc in sorted({r["doc_id"] for r in rows}):
                a = next((r for r in rows if r["doc_id"] == doc and r["word_budget"] == budget and r["condition"] == condition), None)
                b = next((r for r in rows if r["doc_id"] == doc and r["word_budget"] == budget and r["condition"] == "no_path"), None)
                if a and b:
                    pairs.append(a["rougeL_f1"] - b["rougeL_f1"])
            if pairs:
                contrasts.append(
                    {
                        "contrast": f"{condition} - no_path",
                        "budget": budget,
                        "n": len(pairs),
                        "mean_difference": round(statistics.fmean(pairs), 6),
                        "bootstrap_95": [round(x, 6) for x in bootstrap_interval(pairs)],
                        "exact_signflip_p": round(exact_signflip(pairs), 6) if len(pairs) <= 18 else None,
                        "negative_documents": sum(1 for p in pairs if p < 0),
                        "positive_documents": sum(1 for p in pairs if p > 0),
                    }
                )
    pvalues = [c["exact_signflip_p"] for c in contrasts if c["exact_signflip_p"] is not None]
    if pvalues:
        adjusted = holm(pvalues)
        for contrast, value in zip([c for c in contrasts if c["exact_signflip_p"] is not None], adjusted):
            contrast["holm_p"] = round(value, 6)

    payload = {
        "schema": "c2ges-external-prospective-v1",
        "protocol": "PROTOCOL_external_prospective_v1.md",
        "claim_class": "prospective frozen external evaluation; not author-attested unseen",
        "reports_kept": len(reports),
        "reports_skipped": skipped,
        "kept_documents": [
            {"doc_id": r["doc_id"], "family": r["report_series_id"],
             "candidate_units": len(r["candidate_sentences"]),
             "reference_words": R.word_count(r["reference_summary"])}
            for r in reports
        ],
        "by_condition": by_condition,
        "contrasts": contrasts,
        "rows": rows,
    }
    Path(args.json).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: payload[k] for k in ("reports_kept", "by_condition", "contrasts")}, indent=2))


if __name__ == "__main__":
    main()
