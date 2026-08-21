# C2GES Round-3 response matrix

| ID | Response | Evidence / status |
|---|---|---|
| R3-M01 | Created a timestamped, hash-bound add-on protocol before execution. The add-on is separate from canonical v2 and exploratory v3, uses the unchanged label-blind test contract, retrains true no-floor and structurally role-free variants for all five seeds, and prospectively reruns the frozen cached cross-encoder. All eight arms, four K values, seven primary contrasts, cluster bootstrap, sign-flip rules, Holm family, tie/truncation rules, snapshot files, and runtime boundaries were frozen. Label-blind alone is justified because the new estimands concern structural floor/head removal; repeating role provenance would answer the already-bounded canonical question. | `addon_round3/ADDON_PROTOCOL_FREEZE.{md,json}`; execution/aggregation/validation artifacts in the same directory. Canonical W6 gates unchanged. |
| R3-M02 | Changed exploratory-v3 intervals to resample documents and pool every claim plus its complete five-seed bundle, preserving claim counts and repeated sampled clusters. Added a fully independent recomputation of every stored cell interval. | `exploratory_v3/build_exploratory_v3.py`, `validate_exploratory_v3.py`, regenerated tables/figures/manifest; validation PASS with zero interval discrepancy. |
| R3-m01 | Removed the non-dominated-envelope line and legend from the canonical compute renderer and regenerated canonical-v2 vector/raster figures and manifest. The prose continues to prohibit a Pareto interpretation. | `build_c2_canonical_artifacts.py`; regenerated `w6_c2_canonical_v2`; manuscript compute PDF replaced. |
| R3-m02 | Removed leading “Proceedings of” from cited-only BibTeX booktitles for the MDPI style, changed `month = jan` to `{January}`, and made the undated NERC program page explicitly undated with its access date. | `manuscript_applsci/references_cited_verified.bib`; no fabricated publication year. |
| R3-m03 | Enlarged and simplified framework Figure 3; made implementation-table columns ragged-right to remove known underfull boxes; removed math shifts from abstract metadata; rebuilt and checked warnings. | Framework config/rendered PDF, canonical TeX generator, manuscript TeX/build log. |

## Execution incidents retained without substitution

The first orchestration call timed out while its launcher/children survived; PID-level inspection prevented a duplicate launch. All ten learned runs subsequently completed with success records. The orphaned launcher exited before cross-encoder execution. A first isolated cross-encoder attempt then failed before model loading because its wrapper pre-created a directory that the frozen runner required to be absent. That failed directory and status remain preserved. The unchanged frozen scorer was launched once in a fresh runner-owned output directory with logs stored separately. See `addon_round3/LAUNCH_INCIDENT.md`.

## External blockers deliberately preserved

Author identities, affiliations, correspondence, CRediT roles, funding, conflicts, acknowledgments, ethics/consent confirmation, and final AI-use wording remain author actions. Public artifact license review, upload authority, and DOI/URL minting remain human/institutional actions. The unrecorded historical Hugging Face revision and absence of human NERC labels are not fabricated.
