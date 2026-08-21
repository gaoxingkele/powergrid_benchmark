# MA-SQLGrid Narrative Revision Summary

## Outcome

The manuscript has been restructured as an Applied Sciences research article
rather than a software-acceptance report. Its central result is now the
validation-aware historical-pool comparison (80/180, 100/180, and 101/180),
with the 130/180 top-score ties and 117--118/180 reverse-order sensitivity used
to explain the remaining semantic-ranking bottleneck.

The revised title is:

> MA-SQLGrid: A Robust and Auditable Multi-Agent Framework for Power-Grid
> Text-to-SQL

This positioning is consistent with the journal's applied computing and
electrical-engineering scope: <https://www.mdpi.com/journal/applsci/about> and
<https://www.mdpi.com/journal/applsci/sections/computing_artificial_intelligence>.

## Main changes

- Rewrote the abstract to 168 English words and retained only the primary
  number group plus one scope boundary.
- Rebuilt the Introduction around the power-grid semantic problem, the
  workflow gap, three research questions, and three contributions.
- Consolidated Related Work into schema/context, multi-role validation and
  selection, and power-grid Text-to-SQL.
- Moved the five-role architecture and read-only adjudication mechanism ahead
  of version and provenance detail.
- Replaced the claim-licence table with an experimental-design table organized
  by study unit, generation design, endpoint, inference, and research role.
- Centralized the statistical estimand, dependence proxies, exchangeability,
  exact sign enumeration, zero-difference handling, and Holm families.
- Reordered Results so that context/component behavior leads to portability,
  historical-pool selection, and then tie/order stability.
- Rewrote Discussion around mechanisms and engineering significance rather
  than repeated disclaimers.
- Consolidated limitations into data/external validity, experimental design,
  semantic validity, and ranking stability.
- Compressed Conclusions around one take-home result and one next-step problem.
- Replaced the audit-style Figure 6 with a reproducible scientific evidence
  flow diagram. All six manuscript figures remain code-native PDF/SVG assets.
- Materialized a rights-safe supplement containing executor tests, independent
  audits, supersession records, complete R3 numerical tables, and the rights
  inventory.

## Preserved scientific facts

No experiment, dataset, baseline, prediction, endpoint, or statistical result
was changed. In particular:

- fixed-order, validation-only, and complete-witness reference matches remain
  80/180, 100/180, and 101/180;
- both evidence-aware selectors remain tied at the top score on 130/180
  questions;
- reverse-order sensitivity remains 117--118/180;
- the BIRD v1.1 formal runs, excluded incidents, GridDB factorial results,
  component results, and constructed-state results retain their prior status;
- the historical-pool comparison remains descriptive and is not presented as
  a causal estimate of five-role superiority.

## Verification

- MDPI LaTeX build: PASS
- Pages: 26
- Figures: 6
- Tables: 11
- Undefined references/citations: 0
- Overfull boxes: 0
- Visual inspection: PASS, 26/26 pages and 6/6 figures
- PDF SHA-256:
  `5A8EDD49E13F49850484A8E6B903CEB07FF1C479034EBB660C14EA9FA9DBD596`

File-level hashes are recorded in `RELEASE_MANIFEST.json`; figure provenance is
recorded in `MA_SQLGrid/figures/FIGURE_LINEAGE.json`.

## Human checks before submission

1. Confirm that `liubijing@outlook.com` is the intended correspondence address
   for corresponding author Yang Yong, or replace it with the final independent
   correspondence mailbox.
2. Confirm author order, affiliation markers, author-contribution roles, and
   the funding acknowledgement with all authors.
3. Replace template-only journal metadata (received/accepted/DOI fields) only
   if the MDPI submission system or editorial office requests it; do not invent
   these values in the manuscript.
4. Decide which rights-safe supplementary files will be uploaded with the
   initial submission and which restricted records will be provided only on
   editor/reviewer request.
