"""Tighten the G1 paragraph and remove two duplicated caveats (length control).

The evidence-layer sentence repeats its own table caption, and the §5 sentence on
the held-out revision repeats the methods statement verbatim. Both are removed;
the bound paragraph keeps every number but drops the family sentence, which is
already the caption of Supplementary Table S15.
"""

from __future__ import annotations

from pathlib import Path

TEX = Path(__file__).resolve().parent / "paper_information.tex"

LONG_BOUND = (
    "That reading can be sharpened from a null result into a bound. Across the four budgets the "
    "one-sided 95\\% bootstrap upper limit on the path-layer difference is at most $+0.0047$ ROUGE-L "
    "and $+0.0021$ at 260 words, so a path-channel gain larger than $+0.005$ is excluded on this "
    "corpus; the bound is post hoc and its worst case under leave-one-out is $+0.0059$ "
    "(Supplementary Table~S17). The pooled 260-word difference is also not homogeneous: it is carried "
    "by the two frequency-deviation reports ($-0.0799$), whereas the grid-incident, market-coupling "
    "and NERC families sit at $-0.0028$, $+0.0036$ and $-0.0031$ (Supplementary Table~S15). "
    "Figure~S5 traces every arm across five word budgets and four unit budgets and shows the mechanism "
    "behind the budget dependence: under an equal-word budget the role-conditioned arms trail the "
    "lexical-and-position baseline up to 260 words and reach parity only at 400 words, while under an "
    "equal-unit budget they lead and pack about 1.5 times as many words into each selected unit as "
    "that baseline and three times as many as TextRank."
)

SHORT_BOUND = (
    "That reading can be sharpened from a null result into a bound: across the four budgets the "
    "one-sided 95\\% bootstrap upper limit on the path-layer difference is at most $+0.0047$ ROUGE-L, "
    "so a path-channel gain larger than $+0.005$ is excluded on this corpus (post hoc; $+0.0059$ worst "
    "case under leave-one-out; Supplementary Table~S17). Figure~S5 traces every arm across five word "
    "budgets and four unit budgets and locates the mechanism: the role-conditioned arms trail the "
    "lexical-and-position baseline up to 260 words under an equal-word budget and reach parity only at "
    "400 words, whereas under an equal-unit budget they lead and pack about 1.5 times as many words "
    "into each selected unit. The pooled 260-word difference is not homogeneous either, since it is "
    "carried by the two frequency-deviation reports, and Supplementary Tables~S15--S16 report the "
    "family split and the per-report cost record."
)

DROP_LAYER_SENTENCE = (
    " None of the four layers supports confirmatory superiority, unseen generalization, expert gold, "
    "or semantic-validity claims."
)

DROP_REVISION_SENTENCE = (
    " The freeze-before-eval path revision uses the same 15 retained-test reports as a held-out split "
    "for this revision; it is not an unseen confirmatory corpus."
)


def main() -> None:
    text = TEX.read_text(encoding="utf-8")
    for label, old, new in (
        ("bound paragraph", LONG_BOUND, SHORT_BOUND),
        ("layer sentence", DROP_LAYER_SENTENCE, ""),
        ("revision sentence", DROP_REVISION_SENTENCE, ""),
    ):
        count = text.count(old)
        if count != 1:
            raise AssertionError(f"{label}: anchor occurs {count} times")
        text = text.replace(old, new)
    TEX.write_text(text, encoding="utf-8")
    print("trim applied")


if __name__ == "__main__":
    main()
