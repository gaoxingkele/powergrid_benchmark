"""Report the arm-level external result: role layer is budget-specific, path layer is stable."""

from __future__ import annotations

import re
from pathlib import Path

TEX = Path(__file__).resolve().parent / "paper_information.tex"

ARMS = (
    "An arm-level extension separates the two layers instead of testing them jointly, and it shows a "
    "budget dependence rather than a hidden role-layer gain. Adding role evidence and role-group "
    "reservation to a lexical-and-position baseline moves ROUGE-L by $-0.03510$ at the 110-word budget, "
    "with 18 of 22 discordant documents negative ($p=0.0039$, Holm-adjusted $0.0774$), while the same "
    "contrast is $+0.01079$ under a ten-unit budget and never reaches family-wise correction; the path "
    "channel stays at or below zero in all four budgets. The role layer's apparent benefit is therefore "
    "specific to the equal-unit-count protocol, and the external corpus supports the negative component "
    "result rather than a general role-layer advantage."
)

EDITS = [
    (
        "The role layer carries measurable effects: on a seven-series pilot, role evidence raised ROUGE-L by 0.0186 at 260 words (interval [0.0078, 0.0320]), and its cues matched professionally annotated spans at precision 0.610 and 0.807, with recall near 6\\%.",
        "The role layer raised ROUGE-L by 0.0186 at 260 words in the seven-series pilot (interval [0.0078, 0.0320]) but not under matched word budgets externally; its cues matched expert-annotated spans at precision 0.610 and 0.807, with recall near 6\\%.",
    ),
    (
        "The extension is reported as a sensitivity rather than as a pre-registered test: on this corpus the sign direction is stable while mean-based inference is not.",
        "The extension is reported as a sensitivity rather than as a pre-registered test: on this corpus the sign direction is stable while mean-based inference is not. "
        + ARMS,
    ),
]


def main() -> None:
    text = TEX.read_text(encoding="utf-8")
    for old, new in EDITS:
        count = text.count(old)
        if count != 1:
            raise AssertionError(f"anchor occurs {count} times: {old[:70]!r}")
        text = text.replace(old, new)
    match = re.search(r"\\abstract\{(.*?)\}\s*\\keyword", text, flags=re.DOTALL)
    words = re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*",
                       match.group(1).replace("\\cges{}", "C2GES").replace("\\%", "%"))
    if not 1 <= len(words) <= 200:
        raise AssertionError(f"abstract is {len(words)} words")
    TEX.write_text(text, encoding="utf-8")
    print(f"arm-level result added; abstract {len(words)} words")


if __name__ == "__main__":
    main()
