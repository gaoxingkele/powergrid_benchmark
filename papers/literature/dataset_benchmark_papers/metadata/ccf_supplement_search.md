# CCF Supplement Search Notes

Date: 2026-07-09

Scope: recent papers from 2023-07-09 to 2026-07-09 that mention local dataset
aliases and appear in CCF-list computer-science conferences.

Automated Result:

- No confirmed CCF main-conference record was identified by the OpenAlex venue
  classifier for the current dataset pool.
- The strongest computer-science crossover cluster is `grid2op_datasets`
  / `L2RPN`, but the recent records found by OpenAlex are journals, arXiv,
  OpenReview-style pages, challenge reports, or surveys rather than confirmed
  AAAI/IJCAI/KDD/ICML/ICLR/NeurIPS main-conference papers.
- `State and Action Factorization in Power Grids` was added as a Grid2Op/L2RPN
  OA supplement because it is a recent RL-oriented power-grid paper with an
  arXiv PDF, but it is not marked as a confirmed CCF paper.

Verification Policy:

- `venue_bucket=ccf_conference_candidate` should be assigned only when a record
  source name or proceedings venue clearly matches a CCF-list conference.
- Workshop, arXiv, OpenReview, and challenge papers are useful background but
  should not be counted as CCF main-conference evidence without manual venue
  confirmation.

Next Manual Checks:

- Search CCF A/B venues directly for `Grid2Op`, `L2RPN`, `Learning to Run a
  Power Network`, and `power grid topology reinforcement learning`.
- If a confirmed CCF paper is found, add it to
  `dataset_paper_candidates_filtered.csv` with:
  `venue_bucket=ccf_conference_candidate`.
