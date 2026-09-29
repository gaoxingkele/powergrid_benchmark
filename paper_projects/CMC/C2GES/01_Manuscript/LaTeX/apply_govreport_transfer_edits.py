"""Write the GovReport transfer layer (G2) into the manuscript and supplement."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
TEX = ROOT / "paper_information.tex"
SUPP = PROJECT / "01_Manuscript" / "Supplementary" / "supplementary_materials.tex"

INTRO_OLD = (
    "The internal evidence is presented in four explicitly separated layers (Table~\\ref{tab:evidence-layers}), "
    "followed by two bounded layers that are not pooled with them: an adjacent-corpus construct audit of the "
    "role and edge cues (Section~\\ref{sec:construct-audit}) and a prospective frozen external evaluation on a "
    "new report family (Section~\\ref{sec:external-prospective})."
)
INTRO_NEW = (
    "The internal evidence is presented in four explicitly separated layers (Table~\\ref{tab:evidence-layers}), "
    "followed by three bounded layers that are not pooled with them: an adjacent-corpus construct audit of the "
    "role and edge cues (Section~\\ref{sec:construct-audit}), a prospective frozen external evaluation on a "
    "new report family (Section~\\ref{sec:external-prospective}), and an out-of-domain transfer check on "
    "government research reports."
)

TABLE_OLD = (
    "L6 Adjacent-corpus construct audit & 7{,}285 relation pairs; 2{,}139 sentences & n/a & Role and edge cues "
    "vs human annotation & Adjacent-domain construct audit: cues are precise when they fire and sparse and "
    "genre-bound. Not domain expert gold.\\\\\n\\bottomrule"
)
TABLE_NEW = (
    "L6 Adjacent-corpus construct audit & 7{,}285 relation pairs; 2{,}139 sentences & n/a & Role and edge cues "
    "vs human annotation & Adjacent-domain construct audit: cues are precise when they fire and sparse and "
    "genre-bound. Not domain expert gold.\\\\\n"
    "L7 Out-of-domain transfer check & 100 reports & 110/260 words; $K=5/10$ & Frozen arms on GovReport "
    "(CRS and GAO reports, human-written summaries) & Out-of-domain robustness transfer: the path channel is "
    "negative in every budget with a one-sided upper limit below zero, but the role and edge constructs are "
    "not valid outside the power domain, so this layer bounds a risk rather than supporting the mechanism.\\\\\n"
    "\\bottomrule"
)

CAPTION_OLD = "\\caption{The six evidence layers, their resources and claim bounds."
CAPTION_NEW = "\\caption{The seven evidence layers, their resources and claim bounds."

TRANSFER_SECTION = r"""
\subsection{Out-of-Domain Transfer Check on Government Reports}
\label{sec:govreport-transfer}

The path-layer null and the budget dependence were re-examined outside the power domain on a large, human-referenced corpus. The GovReport test split (973 reports from the Congressional Research Service and the Government Accountability Office, CC BY 4.0) was sampled in five length strata to 100 documents before any outcome was computed, and the same frozen arms and budgets were applied without tuning against each report's own human-written summary. Two limits fix how this layer may be read: the role cue lexicon is power-domain specific, so the role contrasts here measure cue mismatch rather than the construct, and the references are abstractive. The path channel was negative at all four budgets ($-0.00305$, $-0.00259$, $-0.00515$ and $-0.00277$ at 110 words, 260 words, five units and ten units), with a one-sided 95\% bootstrap upper limit below zero in every budget ($-0.00105$ to $-0.00071$) and a family-corrected five-unit contrast (Holm $p=0.0017$); the bound therefore excludes a positive path effect instead of merely failing to detect one. The role-conditioned arms were significantly worse than their lexical baseline at both word budgets ($-0.02124$ and $-0.02043$, Holm $p=0.0002$), as expected when a domain lexicon is applied outside its domain, and TextRank again exceeded no-path at equal word budgets ($+0.02149$ and $+0.02728$, Holm $p=0.0002$). Supplementary Table~S18 reports these contrasts with intervals, discordant splits and leave-one-out envelopes.

"""

ANCHOR = "\\subsection{Held-Out Matched-Budget Path Revision}"

SUPP_INTRO_OLD = "It contains seventeen tables and two figures referenced by the main manuscript."
SUPP_INTRO_NEW = "It contains eighteen tables and two figures referenced by the main manuscript."

SUPP_DECL_OLD = "\\supplementary{The supplementary PDF contains Tables~S1--S17 and Figures~S4--S5."
SUPP_DECL_NEW = "\\supplementary{The supplementary PDF contains Tables~S1--S18 and Figures~S4--S5."

SUPP_TAIL_OLD = (
    "Tables~S14--S17 and Figure~S5 record the reviewer-requested second addendum round: the exact "
    "reservation--path factorial estimates, the external corpus stratified by publisher family, "
    "per-report cost and coverage, one-sided bounds on the layer contrasts, and the budget-efficiency "
    "curves."
)
SUPP_TAIL_NEW = (
    "Tables~S14--S17 and Figure~S5 record the reviewer-requested second addendum round: the exact "
    "reservation--path factorial estimates, the external corpus stratified by publisher family, "
    "per-report cost and coverage, one-sided bounds on the layer contrasts, and the budget-efficiency "
    "curves. Table~S18 reports the out-of-domain transfer check on GovReport."
)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"{label}: anchor occurs {count} times")
    return text.replace(old, new)


def main() -> None:
    tex = TEX.read_text(encoding="utf-8")
    if "sec:govreport-transfer" in tex:
        raise AssertionError("transfer section already present")
    tex = replace_once(tex, INTRO_OLD, INTRO_NEW, "layer intro")
    tex = replace_once(tex, TABLE_OLD, TABLE_NEW, "layer table")
    tex = replace_once(tex, CAPTION_OLD, CAPTION_NEW, "layer caption")
    tex = replace_once(tex, ANCHOR, TRANSFER_SECTION.lstrip("\n") + ANCHOR, "transfer section")
    tex = replace_once(tex, SUPP_DECL_OLD, SUPP_DECL_NEW, "supplementary declaration")
    tex = replace_once(tex, SUPP_TAIL_OLD, SUPP_TAIL_NEW, "supplementary tail")
    TEX.write_text(tex, encoding="utf-8")

    supp = SUPP.read_text(encoding="utf-8")
    supp = replace_once(supp, SUPP_INTRO_OLD, SUPP_INTRO_NEW, "supplement intro")
    SUPP.write_text(supp, encoding="utf-8")
    print("GovReport transfer layer written into manuscript and supplement")


if __name__ == "__main__":
    main()
