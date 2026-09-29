"""Apply the G1 (bounded negative result) and reviewer-addenda edits.

Four anchored edits, each asserted to occur exactly once:

  1. main text, external section: turn the "not significant" path-layer result
     into a one-sided bound, record the family composition behind the pooled mean,
     and point at Figure S5 for the budget-efficiency curve;
  2. main text, component-factorial section: point at Tables S14 and S16;
  3. main text, supplementary declaration: S1--S17, Figures S4--S5;
  4. supplement: marker region for the generated Tables S14--S17 / Figure S5.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
TEX = ROOT / "paper_information.tex"
SUPP = PROJECT / "01_Manuscript" / "Supplementary" / "supplementary_materials.tex"

BOUND_PARAGRAPH = (
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

ADDENDA_POINTERS = (
    " Supplementary Table~S14 gives the exact reservation, path and interaction estimates with their "
    "cluster-bootstrap intervals, exact sign-flip values, Holm adjustments and per-series deltas, and "
    "Supplementary Table~S16 records per-report cost against candidate-set size together with role and "
    "typed-edge coverage."
)

SUPPLEMENTARY_OLD = (
    "\\supplementary{The supplementary PDF contains Tables~S1--S13 and Figure~S4. Main-text "
    "Table~\\ref{tab:evidence-layers} states the four evidence layers and their claim bounds."
)

SUPPLEMENTARY_NEW = (
    "\\supplementary{The supplementary PDF contains Tables~S1--S17 and Figures~S4--S5. Main-text "
    "Table~\\ref{tab:evidence-layers} states the four evidence layers and their claim bounds."
)

SUPPLEMENTARY_TAIL_OLD = (
    "Tables~S11--S13 are descriptive addenda: the error profile of path-driven selection changes, "
    "per-role token alignment between extracts and references, and the long-block audit detail."
)

SUPPLEMENTARY_TAIL_NEW = (
    "Tables~S11--S13 are descriptive addenda: the error profile of path-driven selection changes, "
    "per-role token alignment between extracts and references, and the long-block audit detail. "
    "Tables~S14--S17 and Figure~S5 record the reviewer-requested second addendum round: the exact "
    "reservation--path factorial estimates, the external corpus stratified by publisher family, "
    "per-report cost and coverage, one-sided bounds on the layer contrasts, and the budget-efficiency "
    "curves."
)

SUPP_INTRO_OLD = "It contains thirteen tables and one figure referenced by the main manuscript."
SUPP_INTRO_NEW = "It contains seventeen tables and two figures referenced by the main manuscript."

MARKERS = (
    "% ==== BEGIN ADDENDA V2 TABLES (generated) ====\n"
    "% ==== END ADDENDA V2 TABLES ====\n"
)


def replace_once(text: str, old: str, new: str, *, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"{label}: anchor occurs {count} times")
    return text.replace(old, new)


def main() -> None:
    tex = TEX.read_text(encoding="utf-8")
    tex = replace_once(
        tex,
        "and the external corpus supports the negative component result rather than a general "
        "role-layer advantage.",
        "and the external corpus supports the negative component result rather than a general "
        "role-layer advantage. " + BOUND_PARAGRAPH,
        label="external-bound paragraph",
    )
    tex = replace_once(
        tex,
        "Supplementary Table~S12 reports per-role token alignment between extracts and reference "
        "sentences under the same lexical cues.",
        "Supplementary Table~S12 reports per-role token alignment between extracts and reference "
        "sentences under the same lexical cues." + ADDENDA_POINTERS,
        label="addenda pointers",
    )
    tex = replace_once(tex, SUPPLEMENTARY_OLD, SUPPLEMENTARY_NEW, label="supplementary declaration")
    tex = replace_once(tex, SUPPLEMENTARY_TAIL_OLD, SUPPLEMENTARY_TAIL_NEW, label="supplementary tail")
    TEX.write_text(tex, encoding="utf-8")

    supp = SUPP.read_text(encoding="utf-8")
    supp = replace_once(supp, SUPP_INTRO_OLD, SUPP_INTRO_NEW, label="supplement intro")
    if "% ==== BEGIN ADDENDA V2 TABLES" not in supp:
        supp = replace_once(
            supp,
            "\\section*{Exploratory Development-Only Calibration}",
            MARKERS + "\n\\section*{Exploratory Development-Only Calibration}",
            label="addenda marker",
        )
    SUPP.write_text(supp, encoding="utf-8")
    print("G1 + addenda edits applied")


if __name__ == "__main__":
    main()
