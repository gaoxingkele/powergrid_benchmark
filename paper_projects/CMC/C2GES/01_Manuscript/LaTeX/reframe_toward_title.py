"""Reframe the manuscript so its headline follows its title (writing only).

Title object = role-conditioned extractive summarization. The revision therefore
leads with the component diagnosis (which layer carries information), keeps the
evaluation-boundary protocol in second position as the instrument, and reports the
system comparison as budget- and corpus-dependent. No number changes.
"""

from __future__ import annotations

import re
from pathlib import Path

TEX = Path(__file__).resolve().parent / "paper_information.tex"

EDITS = [
    # 1. Expand the framework name in the abbreviation table (naming option 1).
    (
        "C\\textsuperscript{2}GES & role-conditioned extractive selector described in this paper\\\\",
        "C\\textsuperscript{2}GES & Causal-Chain Graph Extractive Summarization; the term causal refers only to the condition--event--impact--mitigation role progression\\\\",
    ),
    # 2. Abstract opening: lead with the object of the evaluation.
    (
        "Does added structure supply what lexical relevance and dense similarity do not? Structural additions can add complexity without improving quality; this study measures that. \\cges{} is a deterministic selector with lexical relevance, role heuristics, a typed proxy graph, path participation, redundancy control, and page traceability.",
        "Role-conditioned extraction adds role evidence, a typed proxy graph, and a path-deletion term to lexical relevance; this diagnostic evaluation asks which layer carries measurable information for long power-system reports. \\cges{} is a deterministic, source-linked selector with inspectable channels.",
    ),
    # 3. Abstract body: role layer first, path layer second.
    (
        "The primary evidence is the length-controlled normalized Full versus no-path contrast: on a post-access seven-series pilot at 110/260 words, Full-minus-no-path was -0.00799/-0.00718.",
        "The role layer carries measurable effects: on a seven-series pilot, role evidence raised ROUGE-L by 0.0186 at 260 words (interval [0.0078, 0.0320]), and its cues matched professionally annotated spans at precision 0.610 and 0.807 against base rates near 0.52, with recall near 6\\%. The typed path layer is the layer that failed: Full-minus-no-path was -0.00799/-0.00718 in the pilot.",
    ),
    # 4-6. Abstract compressions to stay inside the 200-word limit.
    (
        "On 15 North American Electric Reliability Corporation (NERC) reports, Full had higher ROUGE-L than Semantic-MMR and TextRank at equal unit counts, but outputs were 54--63\\% longer; the unrenormalized removal comparison is scale-coupled, not a component estimate.",
        "On 15 North American Electric Reliability Corporation (NERC) reports, Full exceeded Semantic-MMR and TextRank at equal unit counts but produced 54--63\\% longer outputs; the unrenormalized removal comparison is scale-coupled.",
    ),
    (
        "A freeze-before-eval redesign scored 0.0652/0.1044 against no-path 0.0654/0.1020 on the same reports (held-out, not unseen confirmatory).",
        "A freeze-before-eval redesign scored 0.0652/0.1044 against 0.0654/0.1020 (held-out, not unseen).",
    ),
    (
        "On a prospectively frozen external corpus of 19 reports from two organisations the path term again did not help and fell below no-path at 260 words, while an untyped baseline exceeded it.",
        "On a prospectively frozen external corpus of 19 reports from two organisations it fell below no-path at 260 words after correction, while an untyped baseline exceeded it.",
    ),
    (
        "The evidence supports a negative real-summary diagnosis and no-path as the provisional default, not superiority, proxy validity, or operational benefit.",
        "The evidence supports this component-level diagnosis, not superiority, proxy validity, or operational benefit.",
    ),
    # 7. Contributions reordered to match the title's object.
    (
        "The paper makes three current contributions. First, it provides a deterministic, source-linked role-conditioned selector whose scoring channels can be inspected and removed under controlled configurations. Second, it reports a layered evaluation that separates the 15-report retained test, a seven-series post-access pilot, a freeze-before-evaluation path revision on held-out reports, and a synthetic stress set, and explicitly diagnoses length, clustering, layout, embedding, and multiplicity effects. Third, it reports a reproducible negative component result:",
        "The paper makes three current contributions. First, it diagnoses which layer of the role-conditioned design carries measurable information: role evidence and role-group reservation show the largest component effects measured here, whereas the typed path-deletion layer does not improve the predefined endpoint and is detectably below no-path on a frozen external corpus at the larger budget. Second, it supplies the deterministic, source-linked selector and the evaluation boundary that make that diagnosis admissible, namely length-controlled budgets, series-level clustering, exact enumeration, and a freeze-before-evaluation revision. Third, it reports the resulting system comparison as budget- and corpus-dependent rather than uniform. The negative component result is:",
    ),
    # 8. Conclusions: name the two layers instead of "two clear findings".
    (
        "Its diagnostic evaluation yields two clear findings.",
        "Its diagnostic evaluation separates a role layer that carries measurable effects from a typed path layer that does not.",
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
    print(f"applied {len(EDITS)} edits; abstract now {len(words)} words")


if __name__ == "__main__":
    main()
