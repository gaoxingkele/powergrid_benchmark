"""N-1..N-3: reorder the Results narrative and let the Discussion lead with the role layer.

1. Label the two bounded subsections and replace hard-coded section numbers with refs.
2. Move the external prospective evaluation next to the component factorial.
3. Open Discussion 5.1 with the role-layer evidence and carry the cue-precision result
   into the Discussion and the Conclusions.
"""

from __future__ import annotations

from pathlib import Path

TEX = Path(__file__).resolve().parent / "paper_information.tex"

EXTERNAL_HEAD = "\\subsection{External Prospective Evaluation on a New Report Family}"
CONSTRUCT_HEAD = "\\subsection{Adjacent-Corpus Construct Audit of Role and Edge Evidence}"
INSERT_BEFORE = "\\subsection{Held-Out Matched-Budget Path Revision}"
AFTER_WHICH = "\\subsection{Implementation Reliability}"

EDITS = [
    (
        CONSTRUCT_HEAD,
        CONSTRUCT_HEAD + "\n\\label{sec:construct-audit}",
    ),
    (
        EXTERNAL_HEAD,
        EXTERNAL_HEAD + "\n\\label{sec:external-prospective}",
    ),
    ("Section~4.10", "Section~\\ref{sec:construct-audit}"),
    ("Section~4.11", "Section~\\ref{sec:external-prospective}"),
    (
        "The primary path-component evidence is the length-controlled, normalized Full versus no-path contrast. In the seven-series factorial, AB-5 (normalized Full) remained below AB-6 (no-path)",
        "The role-conditioned layers are not uniformly informative. Role evidence and role-group reservation are the components with measurable effects, and the cues behind them matched professionally annotated intervention and outcome spans at precision 0.610 and 0.807 against base rates near 0.52; the length-controlled, normalized Full versus no-path contrast shows where the same design does not pay. In the seven-series factorial, AB-5 (normalized Full) remained below AB-6 (no-path)",
    ),
    (
        "Its diagnostic evaluation separates a role layer that carries measurable effects from a typed path layer that does not. First,",
        "Its diagnostic evaluation separates a role layer that carries measurable effects from a typed path layer that does not. Role evidence raised ROUGE-L by 0.0186 at 260 words in the pilot, and its cues matched expert-annotated spans at precision 0.610 and 0.807, while no path configuration improved the endpoint. First,",
    ),
]


def main() -> None:
    text = TEX.read_text(encoding="utf-8")
    multi = {"Section~4.10", "Section~4.11"}  # every occurrence refers to the same section
    for old, new in EDITS:
        count = text.count(old)
        if old in multi:
            if count < 1:
                raise AssertionError(f"anchor missing: {old!r}")
        elif count != 1:
            raise AssertionError(f"anchor occurs {count} times: {old[:60]!r}")
        text = text.replace(old, new)

    start = text.index(EXTERNAL_HEAD)
    end = text.index(AFTER_WHICH)
    block = text[start:end].rstrip() + "\n\n"
    text = text[:start] + text[end:]
    target = text.index(INSERT_BEFORE)
    text = text[:target] + block + text[target:]
    TEX.write_text(text, encoding="utf-8")
    print("external subsection moved; narrative edits applied")


if __name__ == "__main__":
    main()
