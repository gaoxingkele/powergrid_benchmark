"""Compress the abstract back under 200 words after adding the external result."""

from __future__ import annotations

import re
from pathlib import Path

TEX = Path(__file__).resolve().parent / "paper_information.tex"

EDITS = [
    (
        "Structural additions to an extractive selector can increase complexity without improving quality, and this study measures that possibility directly.",
        "Structural additions can add complexity without improving quality; this study measures that.",
    ),
    (
        "semantic maximal-marginal-relevance (Semantic-MMR) and TextRank at equal unit counts",
        "Semantic-MMR and TextRank at equal unit counts",
    ),
    (
        "On a prospectively frozen external corpus of 19 incident reports from two organisations, the path term was again no better than no-path and was detectably worse at 260 words after correction, while an untyped graph baseline exceeded no-path at that budget.",
        "On a prospectively frozen external corpus of 19 reports from two organisations the path term again did not help and fell below no-path at 260 words, while an untyped baseline exceeded it.",
    ),
    (
        "Eight fictional fixtures are not real incident data. The evidence supports a negative real-summary diagnosis and no-path as the simpler provisional default, but not system superiority, structural-proxy validity, or operational benefit.",
        "The eight fictional fixtures are not real data. The evidence supports a negative real-summary diagnosis and no-path as the provisional default, not superiority, proxy validity, or operational benefit.",
    ),
    (
        "A freeze-before-eval redesign scored 0.0652/0.1044 against no-path 0.0654/0.1020 on those 15 reports, leading at 260 words but not at 110 (held-out, not unseen confirmatory).",
        "A freeze-before-eval redesign scored 0.0652/0.1044 against no-path 0.0654/0.1020 on the same reports (held-out, not unseen confirmatory).",
    ),
    (
        "We present \\cges{}, a deterministic selector with lexical relevance, role heuristics, a typed proxy graph, path participation, redundancy control, and page traceability.",
        "\\cges{} is a deterministic selector with lexical relevance, role heuristics, a typed proxy graph, path participation, redundancy control, and page traceability.",
    ),
    (
        "TextRank ranked first at 110 words (0.1690) and no-path \\cges{} at 260 words (0.1844).",
        "TextRank ranked first at 110 words and no-path \\cges{} at 260 (0.1690 and 0.1844).",
    ),
    (
        "Does added structure supply what lexical relevance and dense similarity do not already carry?",
        "Does added structure supply what lexical relevance and dense similarity do not?",
    ),
    (
        "The primary path-component evidence is the length-controlled normalized Full versus no-path contrast: on a post-access seven-series pilot at 110/260-word budgets, Full-minus-no-path was -0.00799/-0.00718.",
        "The primary evidence is the length-controlled normalized Full versus no-path contrast: on a post-access seven-series pilot at 110/260 words, Full-minus-no-path was -0.00799/-0.00718.",
    ),
    (
        "Full had higher ROUGE-L (lexical overlap) than Semantic-MMR and TextRank at equal unit counts, but outputs were 54--63\\% longer; the unrenormalized coefficient-removal comparison is a scale-coupled historical diagnostic.",
        "Full had higher ROUGE-L than Semantic-MMR and TextRank at equal unit counts, but outputs were 54--63\\% longer; the unrenormalized removal comparison is scale-coupled, not a component estimate.",
    ),
    (
        "TextRank ranked first at 110 words and no-path \\cges{} at 260 (0.1690 and 0.1844). ",
        "",
    ),
]


def main() -> None:
    text = TEX.read_text(encoding="utf-8")
    for old, new in EDITS:
        count = text.count(old)
        if count != 1:
            raise AssertionError(f"anchor occurs {count} times: {old[:60]!r}")
        text = text.replace(old, new)
    match = re.search(r"\\abstract\{(.*?)\}\s*\\keyword", text, flags=re.DOTALL)
    words = re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*",
                       match.group(1).replace("\\cges{}", "C2GES").replace("\\%", "%"))
    if len(words) > 200:
        raise AssertionError(f"abstract still {len(words)} words")
    TEX.write_text(text, encoding="utf-8")
    print(f"abstract words now {len(words)}")


if __name__ == "__main__":
    main()
