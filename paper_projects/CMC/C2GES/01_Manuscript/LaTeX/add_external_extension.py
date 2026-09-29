"""Report the post-freeze corpus extension (n=24) without disturbing the frozen n=19 result."""

from __future__ import annotations

import re
from pathlib import Path

TEX = Path(__file__).resolve().parent / "paper_information.tex"

EXTENSION = (
    "An extension acquired after that freeze adds five documents (three grid incidents and two "
    "frequency-deviation reports), raising the corpus to 24 documents. The direction is unchanged and "
    "slightly larger: Full minus no-path is $-0.006908$ at 260 words with ten negative, one positive and "
    "thirteen exactly tied documents, but the mean-based sign-flip test is no longer significant "
    "($p=0.444$) because a single document with a large positive difference dominates the mean, and the "
    "TextRank contrast falls to $p=0.130$ as well. The extension is reported as a sensitivity rather than "
    "as a pre-registered test: on this corpus the sign direction is stable while mean-based inference is not."
)

EDITS = [
    # 1. Abstract: drop the now-fragile "after correction" claim and name the extension.
    (
        "On a prospectively frozen external corpus of 19 reports it fell below no-path at 260 words after correction, while an untyped baseline exceeded it.",
        "On the frozen external corpus it fell below no-path at 260 words and extending it from 19 to 24 documents kept that direction; an untyped baseline exceeded no-path.",
    ),
    ("On 15 North American Electric Reliability Corporation (NERC) reports,", "On 15 NERC reports,"),
    (
        "at precision 0.610 and 0.807 against base rates near 0.52, with recall near 6\\%.",
        "at precision 0.610 and 0.807, with recall near 6\\%.",
    ),
    ("Eight fictional fixtures are not real data.", "Fictional fixtures are not real data."),
    # 2. Results: report the extension after the frozen contrasts.
    (
        "Supplementary Table~S10 reports the means and intervals.",
        "Supplementary Table~S10 reports the means and intervals. " + EXTENSION,
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
    print(f"extension reported; abstract {len(words)} words")


if __name__ == "__main__":
    main()
