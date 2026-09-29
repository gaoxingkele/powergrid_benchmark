"""Keep the transfer result in the main text as a bounded pointer; move detail to Table S18."""

from __future__ import annotations

from pathlib import Path

TEX = Path(__file__).resolve().parent / "paper_information.tex"

OLD = (
    "The same frozen arms were applied out of domain to 100 length-stratified GovReport documents "
    "(Congressional Research Service and Government Accountability Office reports with human-written "
    "summaries), where the path channel was negative at all four budgets and its one-sided 95\\% bootstrap "
    "upper limit stayed below zero, excluding a positive path effect; the role-conditioned arms were instead "
    "significantly worse than their lexical baseline at both word budgets, as expected when a power-domain cue "
    "lexicon is applied outside its domain. TextRank again exceeded no-path at equal word budgets. This layer "
    "therefore bounds a transfer risk rather than supporting the mechanism; Supplementary Table~S18 gives the "
    "contrasts, intervals, discordant splits and leave-one-out envelopes."
)

NEW = (
    "The frozen arms were also applied out of domain to 100 length-stratified GovReport documents "
    "(human-written summaries of Congressional Research Service and Government Accountability Office "
    "reports). The path channel was negative at all four budgets with a one-sided 95\\% bootstrap upper limit "
    "below zero, excluding a positive path effect, whereas the role-conditioned arms were significantly worse "
    "than their lexical baseline at both word budgets; because the cue lexicon is power-domain specific, this "
    "layer bounds a transfer risk rather than supporting the mechanism (Supplementary Table~S18)."
)

TABLE_ROW_OLD = (
    "L7 Out-of-domain transfer check & 100 reports & 110/260 words; $K=5/10$ & Frozen arms on GovReport "
    "(CRS and GAO reports, human-written summaries) & Out-of-domain robustness transfer: the path channel is "
    "negative in every budget with a one-sided upper limit below zero, but the role and edge constructs are "
    "not valid outside the power domain, so this layer bounds a risk rather than supporting the mechanism.\\\\"
)

TABLE_ROW_NEW = (
    "L7 Out-of-domain transfer check & 100 reports & 110/260 words; $K=5/10$ & Frozen arms on GovReport "
    "& Out-of-domain robustness transfer: the path channel is negative in every budget with a one-sided upper "
    "limit below zero, but the role and edge constructs are not valid outside the power domain, so this bounds "
    "a risk.\\\\"
)


def main() -> None:
    text = TEX.read_text(encoding="utf-8")
    count = text.count(OLD)
    if count != 1:
        raise AssertionError(f"transfer paragraph anchor occurs {count} times")
    text = text.replace(OLD, NEW)
    row_count = text.count(TABLE_ROW_OLD)
    if row_count != 1:
        raise AssertionError(f"L7 table row anchor occurs {row_count} times")
    text = text.replace(TABLE_ROW_OLD, TABLE_ROW_NEW)
    TEX.write_text(text, encoding="utf-8")
    print("transfer detail moved to Table S18 and shortened")


if __name__ == "__main__":
    main()
