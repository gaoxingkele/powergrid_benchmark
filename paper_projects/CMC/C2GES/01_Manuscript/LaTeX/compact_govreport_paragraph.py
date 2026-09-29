"""Fold the transfer check into the external subsection and tighten it (length control)."""

from __future__ import annotations

from pathlib import Path

TEX = Path(__file__).resolve().parent / "paper_information.tex"

HEADING = "\\subsection{Out-of-Domain Transfer Check on Government Reports}\n\\label{sec:govreport-transfer}\n\n"

LONG = (
    "The path-layer null and the budget dependence were re-examined outside the power domain on a large, "
    "human-referenced corpus. The GovReport test split (973 reports from the Congressional Research Service "
    "and the Government Accountability Office, CC BY 4.0) was sampled in five length strata to 100 documents "
    "before any outcome was computed, and the same frozen arms and budgets were applied without tuning "
    "against each report's own human-written summary. Two limits fix how this layer may be read: the role cue "
    "lexicon is power-domain specific, so the role contrasts here measure cue mismatch rather than the "
    "construct, and the references are abstractive. The path channel was negative at all four budgets "
    "($-0.00305$, $-0.00259$, $-0.00515$ and $-0.00277$ at 110 words, 260 words, five units and ten units), "
    "with a one-sided 95\\% bootstrap upper limit below zero in every budget ($-0.00105$ to $-0.00071$) and a "
    "family-corrected five-unit contrast (Holm $p=0.0017$); the bound therefore excludes a positive path "
    "effect instead of merely failing to detect one. The role-conditioned arms were significantly worse than "
    "their lexical baseline at both word budgets ($-0.02124$ and $-0.02043$, Holm $p=0.0002$), as expected "
    "when a domain lexicon is applied outside its domain, and TextRank again exceeded no-path at equal word "
    "budgets ($+0.02149$ and $+0.02728$, Holm $p=0.0002$). Supplementary Table~S18 reports these contrasts "
    "with intervals, discordant splits and leave-one-out envelopes."
)

SHORT = (
    "The path-layer null was then re-examined outside the power domain. The GovReport test split (973 "
    "Congressional Research Service and Government Accountability Office reports with human-written "
    "summaries, CC BY 4.0) was sampled in five length strata to 100 documents before any outcome was "
    "computed, and the same frozen arms and budgets were applied without tuning. The role cue lexicon is "
    "power-domain specific, so the role contrasts here measure cue mismatch rather than the construct. The "
    "path channel was negative at all four budgets ($-0.00305$, $-0.00259$, $-0.00515$ and $-0.00277$), with "
    "a one-sided 95\\% bootstrap upper limit below zero in every budget ($-0.00105$ to $-0.00071$) and a "
    "family-corrected five-unit contrast (Holm $p=0.0017$), so the bound excludes a positive path effect "
    "rather than merely failing to detect one. The role-conditioned arms were significantly worse than their "
    "lexical baseline at both word budgets ($-0.02124$ and $-0.02043$, Holm $p=0.0002$), and TextRank again "
    "exceeded no-path at equal word budgets ($+0.02149$ and $+0.02728$, Holm $p=0.0002$); Supplementary "
    "Table~S18 gives intervals, discordant splits and leave-one-out envelopes."
)


def main() -> None:
    text = TEX.read_text(encoding="utf-8")
    for label, old, new in (("heading", HEADING, ""), ("paragraph", LONG, SHORT)):
        count = text.count(old)
        if count != 1:
            raise AssertionError(f"{label}: anchor occurs {count} times")
        text = text.replace(old, new)
    TEX.write_text(text, encoding="utf-8")
    print("transfer paragraph folded into the external subsection")


if __name__ == "__main__":
    main()
