# -*- coding: utf-8 -*-
"""Extract structural statistics from author-owned publication PDFs."""
import fitz
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
PDF_DIR = BASE / "pdf"
OUT_DIR = BASE / "analysis"
TXT_DIR = OUT_DIR / "fulltext"
TXT_DIR.mkdir(parents=True, exist_ok=True)

PDFS = [
    ("sci_rep_2025_19440", "sci_rep_2025_19440.pdf"),
    ("atmosphere_2024_1429", "atmosphere_2024_1429.pdf"),
    ("discover_computing_2026_173", "discover_computing_2026_173.pdf"),
]

# Journal-specific reference-section markers
REF_PATTERNS = [
    r"(?m)^\s*References\s*$",
    r"(?m)^\s*REFERENCES\s*$",
]

CAPTION_FIG = re.compile(r"(?m)^\s*(?:Fig\.?|Figure)\s*\d+", re.I)
CAPTION_TAB = re.compile(r"(?m)^\s*Table\s*\d+", re.I)


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9\-']*", text))


def find_abstract(full: str):
    """Return (abstract_text, abstract_end_char_offset)."""
    m = re.search(r"(?is)\bAbstract\b[:\s]*(.*?)(?:\n\s*(?:Keywords?|Index Terms|1\.\s|1\s+Introduction|I\.\s|©|\n\s*1\s*\n))", full)
    if not m:
        return None, None
    return m.group(1), m.end(1)


def count_numbered_equations(text: str) -> int:
    """Count display-equation numbers like (1) .. (99) at line ends."""
    nums = set()
    for m in re.finditer(r"\((\d{1,2})\)\s*$", text, re.M):
        n = int(m.group(1))
        if 1 <= n <= 99:
            nums.add(n)
    return len(nums)


def main():
    stats = {}
    for key, fname in PDFS:
        doc = fitz.open(PDF_DIR / fname)
        full = "\n".join(p.get_text() for p in doc)
        (TXT_DIR / f"{key}.txt").write_text(full, encoding="utf-8")

        n_pages = doc.page_count
        abs_text, abs_end = find_abstract(full)
        abs_words = word_count(abs_text) if abs_text else None

        # locate references section
        ref_start = None
        for pat in REF_PATTERNS:
            ms = list(re.finditer(pat, full))
            if ms:
                ref_start = ms[-1].start()  # last occurrence = actual section
                break
        body_end = ref_start if ref_start else len(full)
        body_text = full[:body_end]
        ref_text = full[ref_start:] if ref_start else ""

        # body word count: strip figure/table caption lines
        body_lines = [
            ln for ln in body_text.splitlines()
            if not (CAPTION_FIG.match(ln) or CAPTION_TAB.match(ln))
        ]
        body_words = word_count("\n".join(body_lines))

        # references count: numbered entries like "1. " or "[1]" at line start
        n_refs_bracket = len(re.findall(r"(?m)^\s*\[\d+\]", ref_text))
        n_refs_dot = len(re.findall(r"(?m)^\s*\d+\.\s+[A-Z(]", ref_text))
        n_refs = max(n_refs_bracket, n_refs_dot)

        # figures / tables: count distinct caption numbers
        fig_nums = set(re.findall(r"(?im)^\s*(?:Fig\.?|Figure)\s*(\d+)", body_text))
        tab_nums = set(re.findall(r"(?im)^\s*Table\s*(\d+)", body_text))

        # numbered equations: search body only
        eq_nums = count_numbered_equations(body_text)

        # section headings: try numbered pattern "N. Title" / "N Title" / "N.N"
        heads = []
        for ln in full.splitlines():
            s = ln.strip()
            if re.match(r"^\d+(\.\d+)*\.?\s+[A-Z][A-Za-z]", s) and 4 < len(s) < 90:
                heads.append(s)
            elif re.match(r"^\d+(\.\d+)*\.?\s*$", s):
                # number alone on a line (Sci Rep style: number on its own line? unlikely) skip
                pass
        # also unnumbered standard headings
        for std in ["Introduction", "Methods", "Results", "Discussion", "Conclusion",
                    "Conclusions", "Materials and methods", "Data availability"]:
            for ln in full.splitlines():
                if ln.strip() == std:
                    heads.append(ln.strip())
                    break

        stats[key] = {
            "pdf_file": fname,
            "pages": n_pages,
            "abstract_words": abs_words,
            "body_words_excl_refs_captions": body_words,
            "numbered_equations": eq_nums,
            "figure_captions": len(fig_nums),
            "figure_numbers_seen": sorted(int(x) for x in fig_nums),
            "table_captions": len(tab_nums),
            "table_numbers_seen": sorted(int(x) for x in tab_nums),
            "references_count_auto": n_refs,
            "ref_count_bracket": n_refs_bracket,
            "ref_count_dot": n_refs_dot,
            "heading_candidates": heads[:80],
        }
        print(key, json.dumps(stats[key], ensure_ascii=False)[:200])

    (OUT_DIR / "auto_stats_raw.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", OUT_DIR / "auto_stats_raw.json")


if __name__ == "__main__":
    main()
