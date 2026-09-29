"""Insert the external-prospective-evaluation findings into the manuscript.

Each replacement is asserted to occur exactly once so a silent mismatch cannot
corrupt the text. Run once, then rebuild the manuscript.
"""

from __future__ import annotations

from pathlib import Path

TEX = Path(__file__).resolve().parent / "paper_information.tex"

EDITS = [
    (
        "leading at 260 words but not at 110 (held-out, not unseen confirmatory).",
        "leading at 260 words but not at 110 (held-out, not unseen confirmatory). "
        "On a prospectively frozen external corpus of 19 incident reports from two organisations, the path term was again no better than no-path and was detectably worse at 260 words after correction, while an untyped graph baseline exceeded no-path at that budget.",
    ),
    (
        "Taken together, these results do not establish a system-level advantage and instead favor no-path \\cges{} as the simpler provisional configuration.",
        "Taken together, these results do not establish a system-level advantage and instead favor no-path \\cges{} as the simpler provisional configuration. "
        "The external prospective evaluation points the same way and adds one contrast the internal studies never produced: on the new corpus the typed path channel fell below no-path at 260 words after family-wise correction, while TextRank exceeded it, so the only corrected system-level evidence in this study favours the untyped ranking over the typed path.",
    ),
    (
        "Tables~S1--S9 and Figure~S4",
        "Tables~S1--S10 and Figure~S4",
    ),
    (
        "Table~S9 records the adjacent-corpus construct audit of the role and edge cues against human-annotated public corpora.",
        "Table~S9 records the adjacent-corpus construct audit of the role and edge cues against human-annotated public corpora, and Table~S10 reports the external prospective evaluation on a new report family.",
    ),
    (
        "The GUM and EBM-NLP corpora are not redistributed and must be obtained from their original distributors under their own terms.",
        "The external prospective evaluation is distributed as \\nolinkurl{03_Reproducibility/Data/external_prospective_v1/}: the frozen protocol and amendments, the inventory with per-file hashes, the extraction and evaluation scripts, the aggregate result records for every build iteration, and the acquisition and findings reports. "
        "The GUM and EBM-NLP corpora, and the third-party incident-report PDFs and their verbatim text, are not redistributed and must be obtained from their original distributors under their own terms.",
    ),
]


def main() -> None:
    text = TEX.read_text(encoding="utf-8")
    for old, new in EDITS:
        count = text.count(old)
        if count != 1:
            raise AssertionError(f"anchor occurs {count} times: {old[:70]!r}")
        text = text.replace(old, new)
    TEX.write_text(text, encoding="utf-8")
    print(f"applied {len(EDITS)} edits to {TEX.name}")


if __name__ == "__main__":
    main()
