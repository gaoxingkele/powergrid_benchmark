"""External prospective evaluation v2: Markdown-based extraction.

v1/v1.3 extracted candidate and reference text from raw PyMuPDF text blocks and
failed on large ENTSO-E reports for three layout reasons: a section number before
the summary title, table-of-contents dot leaders, and — decisively — a
"Management Summary" whose content lives in *subsections* (`# 1 MANAGEMENT
SUMMARY` followed by `### 1.1 Introduction`). Cutting at the next heading of any
level therefore returned a three-word "reference".

This version converts each PDF to structured Markdown with pymupdf4llm (layout
analysis emits heading levels, lists and tables) and cuts the reference from the
summary heading to the next heading of the *same or higher* level. Candidates are
the paragraph blocks after that section. Selectors, budgets, endpoints and
statistics are the frozen ones (`rsi_common`, protocol v1 + amendments v1.1-v1.4).

Usage:
    python -B run_external_prospective_v2.py --json external_prospective_v2.json
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import re
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _code_dir() -> Path:
    """Locate the shared analysis code from either the release layout or a working copy.

    The script ships inside `03_Reproducibility/Data/external_prospective_v1/`, so
    walking up from HERE finds `03_Reproducibility/Code/rsi_path_v1`; the same
    helper also works when the file is executed from the working copy under
    `05_External_Prospective_20260922/`.
    """
    for parent in (HERE, *HERE.parents):
        candidate = parent / "03_Reproducibility" / "Code" / "rsi_path_v1"
        if candidate.is_dir():
            return candidate
    raise RuntimeError("cannot locate 03_Reproducibility/Code/rsi_path_v1")


sys.path.insert(0, str(_code_dir()))
import rsi_common as R  # noqa: E402

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*")
HEADING_RE = re.compile(r"^(#{1,6})\s+(\S.*)$")
SUMMARY_RE = re.compile(r"^[\d.\s]*(?:executive\s+|management\s+)?summary\b", re.I)
MIN_REFERENCE_WORDS = 100
MIN_UNIT_WORDS = 6
MAX_CANDIDATES = 2000
FAMILY_RULES = (
    ("entsoe_market", r"(SDAC|SIDC|decoupling)"),
    ("entsoe_grid", r"(grid.incident|incident.report|factual.report|disturbance.statistics|South-East|MEPSO|Spain)"),
    ("nerc", r"^(blackstart|incident[_-]review)"),
)


def family_of(name: str) -> str:
    for family, pattern in FAMILY_RULES:
        if re.search(pattern, name, re.I):
            return family
    return "other"


GENERIC_STEM_WORDS = {
    "entso", "e", "grid", "incident", "incidents", "report", "factual", "final", "interim",
    "clean", "version", "pdf", "the", "of", "on", "in", "and", "to", "for", "from", "public",
    "update", "sdac", "sidc", "ida", "idct", "note", "coms",
}


def stem_tokens(stem: str) -> set[str]:
    words = {w for w in re.split(r"[^a-z0-9]+", stem.lower()) if w and not w.isdigit()}
    return words - GENERIC_STEM_WORDS


def is_same_incident(left: str, right: str) -> bool:
    """Same-incident test (protocol v2.1).

    Documents that cite the same event date (a 6+ digit token such as 240621 or
    20200204) are versions of one incident; annual statistics series keep their
    four-digit years and are therefore not merged. Without a date token, fall back
    to heavy overlap of the specific stem words.
    """
    dates_left = {t for t in re.split(r"[^0-9]+", left) if len(t) >= 6}
    dates_right = {t for t in re.split(r"[^0-9]+", right) if len(t) >= 6}
    if dates_left and dates_right:
        return bool(dates_left & dates_right)
    a, b = stem_tokens(left), stem_tokens(right)
    if not a or not b:
        return left.lower() == right.lower()
    return len(a & b) / len(a | b) >= 0.6


def headings(lines: list[str]) -> list[tuple[int, int, str]]:
    out = []
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line.strip())
        if match:
            clean = re.sub(r"[*_`]", "", match.group(2))
            out.append((index, len(match.group(1)), re.sub(r"\s+", " ", clean).strip()))
    return out


def build_report(md_path: Path) -> dict | None:
    lines = md_path.read_text(encoding="utf-8").splitlines()
    heads = headings(lines)
    if not heads:
        return None
    summary = next((h for h in heads if SUMMARY_RE.match(h[2]) and h[1] <= 3), None)
    if summary is None:
        return None
    start_index, level, _ = summary
    end_index = next((h[0] for h in heads if h[0] > start_index and h[1] <= level), len(lines))
    reference = "\n".join(lines[start_index + 1 : end_index])
    reference_words = len(WORD_RE.findall(reference))
    if reference_words < MIN_REFERENCE_WORDS:
        return None

    blocks: list[str] = []
    buffer: list[str] = []
    for line in lines[end_index:]:
        stripped = line.strip()
        if not stripped:
            if buffer:
                blocks.append(" ".join(buffer))
                buffer = []
            continue
        if HEADING_RE.match(stripped) or stripped.startswith(("|", "![", "[^")):
            if buffer:
                blocks.append(" ".join(buffer))
                buffer = []
            continue
        buffer.append(stripped)
    if buffer:
        blocks.append(" ".join(buffer))

    candidates = [b for b in blocks if len(WORD_RE.findall(b)) >= MIN_UNIT_WORDS][:MAX_CANDIDATES]
    if len(candidates) < 20:
        return None
    return {
        "doc_id": md_path.stem,
        "report_series_id": family_of(md_path.stem),
        "reference_summary": reference,
        "candidate_sentences": [
            {"sid": f"{md_path.stem}_u{index:04d}", "text": text} for index, text in enumerate(candidates)
        ],
    }


def bootstrap_interval(values: list[float], draws: int = 10000, seed: int = 20260923) -> list[float]:
    rng = random.Random(seed)
    n = len(values)
    means = sorted(statistics.fmean(rng.choice(values) for _ in range(n)) for _ in range(draws))
    return [means[int(0.025 * draws)], means[int(0.975 * draws) - 1]]


def exact_signflip(values: list[float]) -> float | None:
    n = len(values)
    if n > 20:
        return None
    observed = abs(statistics.fmean(values))
    hits = total = 0
    for signs in itertools.product((1, -1), repeat=n):
        total += 1
        if abs(statistics.fmean(s * v for s, v in zip(signs, values))) >= observed - 1e-12:
            hits += 1
    return hits / total


def randomized_signflip(values: list[float], draws: int = 100000, seed: int = 20260926) -> float:
    """Two-sided sign-flip p by Monte Carlo (protocol v2.1, used when n > 20)."""
    rng = random.Random(seed)
    n = len(values)
    observed = abs(statistics.fmean(values))
    hits = 0
    for _ in range(draws):
        shifted = abs(statistics.fmean(v if rng.random() < 0.5 else -v for v in values))
        if shifted >= observed - 1e-12:
            hits += 1
    return (hits + 1) / (draws + 1)


def holm(pvalues: list[float]) -> list[float]:
    order = sorted(range(len(pvalues)), key=lambda i: pvalues[i])
    adjusted = [0.0] * len(pvalues)
    running = 0.0
    for rank, index in enumerate(order):
        running = max(running, (len(pvalues) - rank) * pvalues[index])
        adjusted[index] = min(1.0, running)
    return adjusted


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", required=True)
    args = parser.parse_args()

    settings = R.load_protocol()["textrank"]
    budgets = [110, 260]
    reports, skipped = [], []
    built = []
    for md in sorted((HERE / "markdown").glob("*.md")):
        row = build_report(md)
        if row is None:
            skipped.append({"file": md.name, "reason": "no usable summary reference or candidates"})
            continue
        built.append(row)
    # Keep the fullest version of each incident; ties resolved by larger reference.
    built.sort(key=lambda r: (-len(r["candidate_sentences"]), -len(r["reference_summary"].split()), r["doc_id"]))
    for row in built:
        if any(is_same_incident(row["doc_id"], kept["doc_id"]) for kept in reports):
            skipped.append({"file": row["doc_id"], "reason": "same incident as a kept, fuller version"})
            continue
        reports.append(row)

    rows = []
    for row in reports:
        prepared = R.prepare_report(row)
        for budget in budgets:
            results = {
                "no_path": R.c2ges_select(prepared, utility=None, path_weight=0.0, word_budget=budget),
                "full_path_0.10": R.c2ges_select(prepared, utility="historical", path_weight=0.10, word_budget=budget),
                "textrank": R.textrank_select(prepared, budget, settings),
            }
            for condition, result in results.items():
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

    by_condition, contrasts = {}, []
    for budget in budgets:
        for condition in ("no_path", "full_path_0.10", "textrank"):
            values = [r["rougeL_f1"] for r in rows if r["word_budget"] == budget and r["condition"] == condition]
            by_condition[f"{condition}@{budget}"] = {"n": len(values), "mean": round(statistics.fmean(values), 6) if values else None}
        for condition in ("full_path_0.10", "textrank"):
            pairs = []
            for doc in sorted({r["doc_id"] for r in rows}):
                a = next((r for r in rows if r["doc_id"] == doc and r["word_budget"] == budget and r["condition"] == condition), None)
                b = next((r for r in rows if r["doc_id"] == doc and r["word_budget"] == budget and r["condition"] == "no_path"), None)
                if a and b:
                    pairs.append(a["rougeL_f1"] - b["rougeL_f1"])
            if pairs:
                p = exact_signflip(pairs)
                if p is None:
                    p = randomized_signflip(pairs)
                contrasts.append({
                    "contrast": f"{condition} - no_path",
                    "budget": budget,
                    "n": len(pairs),
                    "mean_difference": round(statistics.fmean(pairs), 6),
                    "bootstrap_95": [round(x, 6) for x in bootstrap_interval(pairs)],
                    "exact_signflip_p": round(p, 6) if p is not None else None,
                    "negative_documents": sum(1 for x in pairs if x < 0),
                    "positive_documents": sum(1 for x in pairs if x > 0),
                })
    pvalues = [c["exact_signflip_p"] for c in contrasts if c["exact_signflip_p"] is not None]
    if pvalues:
        for contrast, value in zip([c for c in contrasts if c["exact_signflip_p"] is not None], holm(pvalues)):
            contrast["holm_p"] = round(value, 6)

    payload = {
        "schema": "c2ges-external-prospective-v2-markdown",
        "extraction": "pymupdf4llm markdown; reference = summary heading to next same-or-higher-level heading",
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
