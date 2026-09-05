# Modern unsupervised baseline identity and license audit

Date: 2026-09-06  
Status: `METHOD_IDENTITY_VERIFIED / IMPLEMENTATION_TESTED / TUNING_PENDING_LAYOUT_AUDIT`

## Selected method

- Published method: **PacSum (Position-Augmented Centrality-based
  Summarization)**.
- Paper: Hao Zheng and Mirella Lapata, “Sentence Centrality Revisited for
  Unsupervised Summarization,” *Proceedings of ACL 2019*, pp. 6236–6247.
- Stable paper ID: ACL Anthology `P19-1628`.
- Paper locator: `https://aclanthology.org/P19-1628/`.
- Published implementation locator: `https://github.com/mswellhao/PacSum`.
- Repository revision inspected: `67cc8ad370eac160ede997b7c32eb74907728bf8`.

## License decision

The inspected GitHub tree contained 11 entries and no top-level or nested
`LICENSE`, `LICENCE`, `COPYING`, or `NOTICE` file. Public visibility is not treated
as permission to copy, modify, or redistribute code. Therefore the upstream
implementation is **not imported, vendored, or adapted** for C2GES.

The project instead supplies an independent implementation of the published
equations in `03_Reproducibility/Code/prospective_v1/pacsum_minilm.py`. It uses no
source text or code from the upstream repository. Distribution of this local
implementation follows the C2GES package's own author-controlled licensing
decision.

## Controlled implementation identity

The prospective comparator is named **PacSum-MiniLM (clean-room)**, not unqualified
PacSum. It retains the paper's thresholded pairwise-similarity matrix and
position-weighted directed degree centrality, while replacing the paper's
task-fine-tuned BERT encoder with the same frozen
`sentence-transformers/all-MiniLM-L6-v2` representation and long-unit policy used
by the prospective Semantic-MMR comparator. This replacement must be disclosed in
Methods and table labels.

The nine-configuration development grid is fixed as the Cartesian product:

- preceding-sentence coefficient: `-2.0`, `-1.0`, `0.0`;
- following-sentence coefficient: `1.0` in every configuration;
- similarity threshold fraction beta: `0.0`, `0.3`, `0.6`.

These ranges are anchored to the paper's reported sensitivity analysis; selection
uses the complete ranking and the same 110/260-word non-truncating budget function
as every other system. Development tuning must not begin until the selected
layout-builder version passes its independent boundary audit. External outcomes
must remain inaccessible during tuning.

## Current gate

Algorithmic unit tests pass, but no performance estimate has been generated from
the new layout candidates. The method may enter balanced development tuning only
after `LAYOUT_BOUNDARY_AUDIT_PROTOCOL.md` passes. It is not yet eligible to appear
as an executed baseline in the manuscript Results section.
