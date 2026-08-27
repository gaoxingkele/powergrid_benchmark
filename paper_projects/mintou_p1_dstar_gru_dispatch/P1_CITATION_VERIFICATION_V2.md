# P1 Citation Verification V2

Audit date: **2026-08-28**. Scope: the 30 numbered references in `manuscript/MANUSCRIPT.md`, checked at proposition level. This report verifies identity and limits what the inspected evidence can support; it does not authorize a manuscript rewrite. `IDENTITY-VERIFIED` means the cited work's bibliographic identity was matched to its DOI/venue record. `FULL` and `PARTIAL` refer only to the stated manuscript proposition. Claim-bearing content that could not be inspected is labeled `UNVERIFIED` and is excluded from support.

## Search order and local provenance

The approved host stores were searched first, on 2026-08-28:

1. `D:/aicoding/powergrid_benchmark/papers/literature` — 1,762 files.
2. `D:/aicoding/mylib/powergrid_paper` — 1,238 files.

The sparse worktree was not used to infer host-store absence. Exact DOI/title searches and relevant task/method terms were applied to text-indexable content; PDFs were inventoried separately. Terms included every manuscript DOI, exact titles for references [5], [13], [28]–[30], and `curtailment`, `System Non-Synchronous Penetration`, `SNSP forecasting`, `analog ensemble`, `analogue`, `similar days approach`, `learned retrieval`, `time-series benchmark`, `forecast evaluation`, `persistence`, and `linear baseline`. The following inspected local indexes anchor the search:

| Local file | SHA-256 | Use |
|---|---|---|
| `D:/aicoding/powergrid_benchmark/papers/literature/dataset_benchmark_papers/algorithm_task_map.md` | `85fab064661f740a096f12b7e82df0e4455ccba54e26e875aeabf96ef1c18fdc` | algorithm/task discovery |
| `D:/aicoding/powergrid_benchmark/papers/literature/dataset_benchmark_papers/metadata/dataset_direction_sci_papers_2021_2026.csv` | `150383007faca4c61b58953875863868a972d84904eb897e1cc6d8e983badd79` | dataset/direction discovery |
| `D:/aicoding/powergrid_benchmark/papers/literature/dataset_benchmark_papers/metadata/curated_extension_papers.csv` | `2a57e02daf24ae5ca0ac890cf65cca5f5dcc1124ec5f90d06ad44f107c0c73f7` | extension-paper discovery |
| `D:/aicoding/powergrid_benchmark/papers/literature/target_journal_related/metadata/target_journal_related_candidates.csv` | `4fc6574ef453d644fcba8d82be3bb8874816394ccdd86f9861d234a7b4824929` | target-journal candidates |
| `D:/aicoding/mylib/powergrid_paper/metadata/target_journal_related_candidates.csv` | `4fc6574ef453d644fcba8d82be3bb8874816394ccdd86f9861d234a7b4824929` | mirrored target-journal candidates |
| `D:/aicoding/powergrid_benchmark/papers/literature/target_journal_related/comparison_analysis.md` | `007e61d9e960bcaa29f7132707c1af23306c97213f0ef86a3bfaf290b73f32ea` | comparison notes |
| `D:/aicoding/powergrid_benchmark/papers/literature/target_journal_related/pdfs/p2_hyperbolic_gcn_smart_dispatch/p2_hyperbolic_gcn_smart_dispatch__11__loadseer_exploiting_tensor_graph_convolutional_network_for__3cba22d20b.pdf` | `5908282d0c137859cefa5bdd77472662e9969e67e5805623543b2a459b767396` | reference [29] full-text support |
| `D:/aicoding/powergrid_benchmark/papers/literature/target_journal_related/pdfs/p1_ieee_access_extension/ieee_access_2024_timesnet_crossformer_lstm.pdf` | `9054a62c1e9b25b46ea044e981f8ff89c68d2f706aebb5db8cfcdc72392f4e01` | reference [30] full-text support |

The mirrored candidate CSV contains 12 rows tagged `p1_twin_gru_dispatch`; their recorded relevance score is 0 and their subjects are dispatch, economic dispatch, or unit commitment. They were retained as discovery-adjacent entries, not promoted to curtailment-forecasting or retrieval comparators. Primary publisher or venue records were consulted only after the two host-store passes. Crossref bibliographic responses were processed in memory and were not saved.

## Retraction and correction check

Provider: **Crossref / Retraction Watch**. Documentation URL: `https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/`. Snapshot source URL: `https://gitlab.com/crossref/retraction-watch-data`. Snapshot date: **2026-08-26**; commit: `d624b4ae1f19a47b6cbcb0f8d548f7048e4f3d71`; CSV SHA-256: `2962f61f31cfa29efd644cb8b8b60f59456cff225af8bf909dc0be611632a9d9`; size: 66,134,396 bytes. Exact normalized DOI matching against both `OriginalPaperDOI` and `RetractionDOI` produced zero matches for the 30 references. Current Crossref relation/update fields were also checked on 2026-08-28.

Codes: `RW0` = no exact DOI match in that dated Retraction Watch snapshot; `C0` = no correction/update relation in the inspected Crossref record; `C1` = a correction relation exists. These are bounded registry checks, not proof that no unregistered notice exists. Reference [24] has erratum DOI `10.1016/j.ijforecast.2021.01.013`, which adds omitted competing-interest declarations; the inspected notice did not identify a result correction.

## Proposition-level audit

| Ref. | DOI | Identity | Proposition support | Correction status | Support boundary |
|---:|---|---|---|---|---|
| [1] | `10.1016/j.rser.2016.06.082` | IDENTITY-VERIFIED | FULL | RW0/C0 | Supports international curtailment levels, causes, and mitigation. |
| [2] | `10.1016/j.rser.2015.09.075` | IDENTITY-VERIFIED | PARTIAL | RW0/C0 | Supports China wind-curtailment drivers and solutions; the narrower Three-North wording is not established by the inspected record. |
| [3] | `10.1016/j.joule.2021.03.021` | IDENTITY-VERIFIED | PARTIAL | RW0/C0 | Supports the curtailment paradox and planning trade-offs; the exact phrase “economically optimal marginal curtailment” is not established by inspected content. |
| [4] | `10.1109/TPWRS.2014.2316974` | IDENTITY-VERIFIED | FULL | RW0/C0 | Supports the Irish SNSP/frequency-stability mechanism. |
| [5] | `10.1016/j.apenergy.2024.123006` | IDENTITY-VERIFIED | FULL | RW0/C0 | Supports day-ahead SNSP forecasting with a continuous penetration target. |
| [6] | `10.1109/TPWRS.2019.2925557` | IDENTITY-VERIFIED | FULL | RW0/C0 | Supports RTS-GMLC assets; it does not remove the manuscript's missing issue-time/vintage limitation. |
| [7] | `10.1371/journal.pone.0194889` | IDENTITY-VERIFIED | PARTIAL | RW0/C0 | Supports the value of simple forecasting references; the compound sparse/persistent-series qualifier is not directly supported. |
| [8] | `10.1016/j.patter.2023.100804` | IDENTITY-VERIFIED | PARTIAL | RW0/C0 | Supports leakage and reproducibility concerns; the compound sparse/persistent-series qualifier is not directly supported. |
| [9] | `10.1175/MWR-D-12-00281.1` | IDENTITY-VERIFIED | FULL | RW0/C0 | Supports the analog-ensemble retrieval and predictive-distribution mechanism. |
| [10] | `10.1016/j.epsr.2011.08.005` | IDENTITY-VERIFIED | PARTIAL | RW0/C0 | Supports case-based voltage-control reasoning; the exact retrieve–reuse–revise–retain wording remains UNVERIFIED. |
| [11] | `10.1016/j.rser.2022.112212` | IDENTITY-VERIFIED | FULL | RW0/C0 | Supports the curtailment-rate/renewable-share map. |
| [12] | `10.1016/j.enpol.2021.112513` | IDENTITY-VERIFIED | FULL | RW0/C0 | Supports the Irish wind, interconnection, and storage planning comparison. |
| [13] | `10.11159/ehst23.120` | IDENTITY-VERIFIED | FULL | RW0/C0 | Supports a one-hour-ahead CAISO wind/solar-curtailment comparison and GRU's within-study ranking only; it does not support external superiority. |
| [14] | `10.1016/j.energy.2016.08.067` | IDENTITY-VERIFIED | FULL | RW0/C0 | Supports adjacent net-load forecasting, not the manuscript's curtailment-onset task. |
| [15] | `10.1109/59.192889` | IDENTITY-VERIFIED | PARTIAL | RW0/C0 | Supports an expert-system load forecaster; the exact similar-day operator-heuristic formulation is UNVERIFIED. |
| [16] | `10.1016/j.ijepes.2005.12.007` | IDENTITY-VERIFIED | PARTIAL | RW0/C0 | Supports neural similar-day load forecasting across several hours; the asserted Euclidean metric is UNVERIFIED. |
| [17] | `10.1109/TPWRS.2007.901670` | IDENTITY-VERIFIED | FULL | RW0/C0 | Supports weighted-nearest-neighbor next-day price forecasting. |
| [18] | `10.1016/j.renene.2014.11.061` | IDENTITY-VERIFIED | FULL | RW0/C0 | Supports an analog-ensemble application to wind-power forecasting. |
| [19] | `10.1016/j.apenergy.2015.08.011` | IDENTITY-VERIFIED | FULL | RW0/C0 | Supports probabilistic analog-ensemble solar-power forecasting. |
| [20] | `10.1016/j.ijepes.2018.07.026` | IDENTITY-VERIFIED | FULL | RW0/C0 | Supports Siamese appliance identification as adjacent learned-similarity work. |
| [21] | `10.3390/en12244732` | IDENTITY-VERIFIED | FULL | RW0/C0 | Supports Siamese representation plus k-NN for power-quality classification. |
| [22] | `10.1016/S0169-2070(00)00057-1` | IDENTITY-VERIFIED | FULL | RW0/C0 | Supports M3's comparison of sophisticated and simple forecasting methods. |
| [23] | `10.1016/j.ijforecast.2006.03.001` | IDENTITY-VERIFIED | FULL | RW0/C0 | Supports failures of common accuracy measures and the MASE proposal. |
| [24] | `10.1016/j.ijforecast.2019.04.014` | IDENTITY-VERIFIED | FULL | RW0/C1 | Supports the M4 evaluation; erratum `10.1016/j.ijforecast.2021.01.013` concerns omitted competing-interest declarations, not an inspected result change. |
| [25] | `10.1016/j.ijforecast.2021.11.013` | IDENTITY-VERIFIED | FULL | RW0/C0 | Supports the M5 competition/evaluation context. |
| [26] | `10.1016/j.ijforecast.2016.02.001` | IDENTITY-VERIFIED | FULL | RW0/C0 | Supports GEFCom2014's competition-grade forecasting protocol. |
| [27] | `10.1016/j.solener.2020.04.019` | IDENTITY-VERIFIED | FULL | RW0/C0 | Supports standardized persistence/climatology reference forecasts for solar verification. |
| [28] | `10.1007/s10618-022-00894-5` | IDENTITY-VERIFIED | FULL | RW0/C0 | Supports leakage, naive-baseline, and metric guidance for time-series forecasting. |
| [29] | `10.1109/ACCESS.2024.3514174` | IDENTITY-VERIFIED | PARTIAL / UNSUPPORTED COMPOUND CLAIM | RW0/C0 | Full text supports the LoadSeer architecture; it does not establish a requirement that learned methods be tested against naive and linear references. |
| [30] | `10.1109/ACCESS.2024.3383912` | IDENTITY-VERIFIED | PARTIAL / UNSUPPORTED COMPOUND CLAIM | RW0/C0 | Full text supports the TimesNet–Crossformer–LSTM architecture; its baselines are learned models and do not establish the asserted naive/linear-reference requirement. |

## Claim boundary and disposition

All 30 reference identities are verified. That does not make every compound sentence fully supported. In particular, [7]–[8] do not directly establish the sparse/persistent-series qualifier, and [29]–[30] do not support the naive-and-linear-reference requirement attributed to them. These limitations are preserved rather than silently repaired. Any later manuscript edit should split the compound propositions, narrow their wording, or add separately verified evidence under a new approved stage.

No manuscript file was changed in this stage. Databases, API responses, publisher files, extracted text, caches, and temporary directories are not committed; only this compact report, the comparator report, and validator changes belong in version control.
