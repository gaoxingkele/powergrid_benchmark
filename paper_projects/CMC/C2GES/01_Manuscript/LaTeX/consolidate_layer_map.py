"""N-4 + N-5: one six-layer map, and the corrected internal win named in the abstract."""

from __future__ import annotations

import re
from pathlib import Path

TEX = Path(__file__).resolve().parent / "paper_information.tex"

NEW_ROWS = [
    "L1 Historical retained test & 15 reports & $K=5/10$ units & Full vs Semantic-MMR, TextRank, unrenormalized removal & Corrected wins for Full against both baselines at $K=5$, qualified by 54--63\\% longer outputs; descriptive ranking, not a fair-tuning comparison. Unrenormalized removal is scale-coupled.\\\\",
    "L2 Seven-series pilot and component factorial & 7 series & 110/260 words & Role evidence, reservation, typed path, and typed vs untyped graph; system contrasts vs three baselines & Exploratory length-controlled component diagnosis and system contrast; the role components are the measured effects and the path layer is not. Not unseen confirmatory and not expert gold.\\\\",
    "L3 External prospective evaluation & 19 reports, two organisations & 110/260 words & Full vs no-path; TextRank vs no-path & Prospective frozen external evaluation; the corrected contrasts favour the untyped ranking and put the path channel below no-path at the larger budget. Not author-attested unseen.\\\\",
    "L4 Held-out path revision (RSI) & 15 reports & 110/260 words & Redesigned path vs no-path and TextRank & Held-out-for-this-revision freeze-before-eval on already-used reports; it did not meet its bounded win. Not unseen confirmatory.\\\\",
    "L5 Synthetic stress set & 8 fictional reports, 4 series & 110/260 words & Full vs no-path on planted role-chain references & Software and endpoint alignment on fictional fixtures; no Holm-adjusted path contrast is nonzero. Not real incident data.\\\\",
    "L6 Adjacent-corpus construct audit & 7{,}285 relation pairs; 2{,}139 sentences & n/a & Role and edge cues vs human annotation & Adjacent-domain construct audit: cues are precise when they fire and sparse and genre-bound. Not domain expert gold.\\\\",
    "",
]

EDITS = [
    (
        "\\caption{Evidence layers and claim bounds. No layer supports confirmatory superiority, unseen confirmatory evaluation, or expert-gold construct validity.}",
        "\\caption{The six evidence layers, their resources and claim bounds. No layer supports confirmatory superiority, author-attested unseen evaluation, or expert-gold construct validity, and no two layers are pooled.}",
    ),
    (
        "On 15 North American Electric Reliability Corporation (NERC) reports, Full exceeded Semantic-MMR and TextRank at equal unit counts but produced 54--63\\% longer outputs; the unrenormalized removal comparison is scale-coupled.",
        "On 15 North American Electric Reliability Corporation (NERC) reports, Full exceeded Semantic-MMR and TextRank at equal unit counts, the only corrected internal win, but produced 54--63\\% longer outputs; the unrenormalized removal comparison is scale-coupled.",
    ),
    (
        "On a prospectively frozen external corpus of 19 reports from two organisations it fell below no-path at 260 words after correction, while an untyped baseline exceeded it.",
        "On a prospectively frozen external corpus of 19 reports it fell below no-path at 260 words after correction, while an untyped baseline exceeded it.",
    ),
    ("The eight fictional fixtures are not real data.", "Eight fictional fixtures are not real data."),
]


def replace_rows(text: str) -> str:
    """Rewrite the body rows of the evidence-layer table between midrule and bottomrule."""
    anchor = "\\label{tab:evidence-layers}"
    start = text.index(anchor)
    mid = text.index("\\midrule", start) + len("\\midrule") + 1
    bottom = text.index("\\bottomrule", start)
    return text[:mid] + "\n".join(NEW_ROWS) + text[bottom:]


def main() -> None:
    text = TEX.read_text(encoding="utf-8")
    for old, new in EDITS:
        count = text.count(old)
        if count != 1:
            raise AssertionError(f"anchor occurs {count} times: {old[:70]!r}")
        text = text.replace(old, new)
    text = replace_rows(text)
    match = re.search(r"\\abstract\{(.*?)\}\s*\\keyword", text, flags=re.DOTALL)
    words = re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*",
                       match.group(1).replace("\\cges{}", "C2GES").replace("\\%", "%"))
    if not 1 <= len(words) <= 200:
        raise AssertionError(f"abstract is {len(words)} words")
    TEX.write_text(text, encoding="utf-8")
    print(f"layer map consolidated; abstract {len(words)} words")


if __name__ == "__main__":
    main()
