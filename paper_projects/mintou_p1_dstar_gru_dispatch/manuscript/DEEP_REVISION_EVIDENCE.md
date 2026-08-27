# Title-to-Evidence Map

## Stage-3 binding

The current title is **A Reproducible Retrospective Curtailment-Risk Benchmark
and Fair Evaluation of GRU Learned-Space Retrieval on RTS-GMLC**. The title
names the evaluated method; it does not assert that learned-space retrieval is
uniformly superior. All new numerical statements in this matrix are bound to
the completed, protocol-valid `p1_ieee_access_upgrade_v2` execution accepted at
Stage 2 and independently rederived at Stage 3.

| Title/contribution term | Evidence-supported meaning | Boundary that travels with the claim |
|---|---|---|
| Reproducible | The sealed manifest hashes the contract, executed script, source files, and nine outputs. Stage 3 independently reproduced all 30 paired rows and all 36 moving-block rows before writing paper tables. | This is deterministic rederivation from the accepted execution, not a new experiment, independent replication, or cross-hardware reproduction. |
| Retrospective | A 48-row query ending at benchmark index $s$ predicts the proxy at delivery row $s+h$, for $h\in\{1,24\}$. | Issue timestamps, as-of mappings, release identifiers, and vintages are absent; no operational forecast or dispatch claim is licensed. |
| Curtailment-risk | A fixed SNSP-type rule maps load, wind, and PV to a method-independent proxy rate. | The target is not observed curtailment, an operator action, OPF/UC output, or an economic outcome. |
| Benchmark | The task, temporal gate, comparison budget, failures, metrics, inference, and sensitivities are prospectively frozen and executable. | One RTS-GMLC system and the first 8760 of 8784 rows identify every result; the sequence ends December 30 and is not a complete calendar year. |
| Fair evaluation | Fit, selection, calibration, and test target sets are disjoint; four architecture heads use the same 20-epoch/checkpoint budget; retrieval controls share the head-selected GRU checkpoint. | Architectures are not parameter-count matched. The result is conditional on the specified budget and single sequence. |
| GRU learned-space retrieval | Learned k=8 retrieval is compared with matched head, raw-feature kNN, and randomized-encoder retrieval. | At 1 h it has lower MAE than both named attribution controls after within-family Holm adjustment. At 24 h it is worse than raw-feature retrieval and unresolved versus randomized retrieval; no general learned-space advantage is licensed. |

The bounded benchmark contribution does not require a favorable method result.
The method contribution is contrast- and horizon-specific. The clear-advance
claim remains unverified until the separately required Stage-4 literature
positioning is completed.

# Primary Estimand and Analysis Unit

The primary estimand is the cap-0.70 mean paired within-seed
treatment-minus-control difference, conditional on the ten frozen seeds, fixed
8760-row sequence, temporal gate, cap, horizon, selection objective, metric,
model budget, retrieval bank, and contrast. The analysis unit is one paired
method-seed run. The 2627 test targets at 1 h and 2604 at 24 h are reused across
seeds and are not independent replicates.

Three families are frozen separately within each horizon:

| Family | Objective / metric | Contrasts per horizon | Interpretation |
|---|---|---:|---|
| `primary_mae_mechanism_attribution` | MAE / continuous MAE | 6 | Primary mechanism and learned-space attribution |
| `architecture_head_mae` | MAE / continuous MAE | 3 | Named head-to-head comparisons only; no overall architecture winner |
| `onset_f1_diagnostic` | onset F1 / onset F1 | 6 | Diagnostic because pre-test onset support is absent |

For every contrast, the paper table reports the mean and median paired
difference, sample SD, paired standardized mean difference $d_z$ when variance
is nonzero, win/tie/loss counts, the two-sided exact sign-flip p-value over all
$2^{10}=1024$ sign assignments, and Holm adjustment within the frozen family
and horizon. The sign-flip interpretation assumes sign-exchangeability under a
no-effect null; the common algorithmic seeds are not randomized experimental
assignments.

The predeclared 95% seed interval is

$$
\bar d \pm 2.2621571627409915\,s_d/\sqrt{10}.
$$

It describes training-seed variability conditional on this sequence and
protocol. It is not uncertainty over hours, blocks, events, years, systems,
policies, vintages, operators, or deployments.

The supplementary moving-block analysis uses the chronological series of the
mean across the ten seeds of paired hourly absolute-loss differences. It uses
ordinary overlapping, non-circular blocks of 24 and 168 rows, 5000 PCG64
replicates, and the four frozen RNG seeds. Its percentile intervals are a
conditional, descriptive dependence sensitivity on the single observed test
sequence. They do not enter Holm decisions, do not override the seed-paired
analysis, and are not confidence intervals across years or systems.

# Comparison Budget and Data Visibility

| Item | Frozen Stage-2 execution | Stage-3 interpretation |
|---|---|---|
| Source | First 8760 of 8784 aligned, hashed RTS-GMLC load/wind/PV rows plus static branch data | One truncated sequence and one system |
| Grid | Caps 0.60/0.70/0.80; 1 h/24 h; MAE/onset-F1 objectives; ten seeds | Cap 0.70 is primary; other caps and cross-cap findings are descriptive |
| Temporal gate | Fit, selection, calibration, and test delivery targets with horizon-length embargoes | Delivery-row retrospective lags; not an issue-time gate |
| Training | GRU, LSTM, DLinear, and TCN; 240 total trajectories; common 20-epoch/checkpoint budget | Architectures are not parameter-count matched |
| Retrieval | learned, raw, and randomized spaces; k=4/8/16/32; k=8 primary | k=4/16/32 are descriptive and never selected from test outcomes |
| Seeded rows | 2280 | Every expected key completed; no seed replacement or imputation |
| Deterministic rows | Persistence, Seasonal-24h, Ridge, privileged direct transform | Descriptive references; privileged transform is not rank eligible |
| Total rows | 2310 completed, 0 failed | Effect direction is not a protocol-validity gate |

The source loader has delivery calendar keys but lacks issue times, as-of
mappings, release identifiers, and vintage fields. The privileged target-hour
transform is a construction/visibility audit and is never a forecaster.
Persistence, Seasonal-24h, and Ridge receive no seed-based p-value. Cross-cap
and k-sensitivity comparisons reuse the same sequence and remain descriptive.

# Negative and Null Results

1. **Persistence remains the lower-MAE primary-cap reference.** Selected
   learned retrieval minus Persistence is +0.000865971 at 1 h and +0.000222061
   at 24 h. These comparisons are descriptive because Persistence has one
   deterministic row.
2. **Learned-space attribution is horizon dependent.** At 1 h, learned k=8
   retrieval is favorable versus raw and randomized retrieval, with paired
   mean differences -0.00498575 and -0.000268116 and Holm p=0.01171875 for
   both. At 24 h it is adverse versus raw retrieval (+0.00126543,
   Holm p=0.01171875) and has a small favorable but Holm-unresolved mean versus
   randomized retrieval (-0.0000482585, Holm p=0.36328125). A general learned-
   space advantage is therefore not supported.
3. **Architecture results are method specific.** At 1 h, the GRU head is
   adverse versus LSTM and TCN and favorable versus DLinear after the separate
   three-contrast Holm adjustment. At 24 h, GRU is favorable versus DLinear;
   its adverse mean differences versus LSTM and TCN are not Holm-resolved. No
   overall architecture winner is licensed.
4. **Onset-targeted selection remains inapplicable.** Every cap/horizon cell
   has zero positive onsets in both selection and calibration. All onset-family
   exact and Holm results are diagnostics and cannot cure that absent support.
   The selected onset condition equals the head at both primary-cap horizons,
   with ten ties and Holm p=1; this fallback identity is not proof of no onset
   effect.
5. **Non-significance is not converted to a supported null.** For example, the
   24 h learned-versus-randomized MAE contrast and GRU-versus-LSTM/TCN head
   contrasts retain their observed directions, intervals, and adjusted
   p-values without a no-effect conclusion.
6. **Moving-block results are conditional/descriptive.** In particular, the
   24 h learned-versus-raw block intervals include zero at both block lengths,
   even though the seed-paired family is adverse after Holm adjustment. This
   sensitivity neither cancels nor replaces the paired-seed result; the two
   analyses condition on different axes of variation.
7. **Cap ordering crosses.** Selected learned retrieval is descriptively
   lower-MAE than Persistence only at cap 0.60/1 h and cap 0.80/24 h;
   Persistence is lower in the other four cells. These are same-sequence
   crossings, not evidence of transport across policies, years, or systems.
8. No result supports observed-curtailment accuracy, probabilistic calibration,
   operator usefulness, network feasibility, deployment safety, economic
   benefit, another system, or another complete year.

# Shared Assets and Independent Contribution

- RTS-GMLC is an external public substrate. The source-file hashes identify the
  evaluated bytes but do not establish a release/vintage identifier or public
  release of this manuscript's evidence package.
- `p1_ieee_access_upgrade_v2/run_manifest.json` and its nine sealed outputs are
  the sole numerical source for the Stage-3 paper tables. Older v1, legacy, and
  independent-rerun records retain their historical scopes and are not mixed
  into these tables.
- `derive_statistics.py` verifies every sealed output hash, independently
  recomputes paired and moving-block results, and applies the claim router.
  `statistics_provenance.json` records the derivation and table hashes.
- The execution-manifest runner hash
  `d4f0e14dd010e4f429e2d61771d781b169a673b73156dac5236113f0e3f34e28`
  exactly matches the committed Git blob and the canonical-LF working content.
  The Windows checkout is separately recorded as CRLF with raw hash
  `da2e1f1ec024d2493e776a1b63b23bfee99b05971752a1ec59f74a2a4dabb225`;
  this line-ending rendering is not a scientific source mismatch.
- The existing manuscript narrative, figures, TeX, and PDFs remain the frozen
  pre-v2 record in this statistics stage. They must not be represented as
  already incorporating these v2 tables. A later evidence-validated narrative
  stage must remove stale claims that the attribution controls, architecture
  heads, seed intervals, or block sensitivity were absent.
- Stage-4 literature positioning remains required before an IEEE Access clear-
  advance statement. No systematic-review, exhaustive-SOTA, or external-domain-
  expert claim is licensed here.
- No authorship, affiliation, funding, contribution, conflict, or companion-
  paper fact is inferred from repository history.

# New or Rerun Experiments

No experiment was newly run or rerun in Stage 3. The accepted Stage-2 execution
already contained 2310 completed result rows, 240 training trajectories, 30
paired-effect rows, 36 moving-block rows, 258 cap/k aggregate rows, and a sealed
primary-cap prediction archive.

Stage 3 performed deterministic rederivation only:

1. verified the accepted manifest, normative contract, and all nine sealed
   output hashes;
2. independently recomputed all paired effects, exact sign-flip p-values,
   within-family/horizon Holm values, and predeclared seed intervals;
3. independently recomputed the 36 frozen moving-block cells from paired hourly
   loss differences and the sealed prediction archive;
4. generated five paper-facing CSV tables for paired inference, moving-block
   sensitivity, deterministic references, cross-cap findings, and wording
   routing; and
5. recorded committed-blob, canonical-LF, and CRLF checkout provenance without
   reclassifying line-ending conversion as a scientific mismatch.

# Unresolved Human Blockers

- **AUTHOR INPUT REQUIRED:** final author list and public ORCIDs.
- **AUTHOR INPUT REQUIRED:** complete affiliations and corresponding-author
  name/e-mail.
- **AUTHOR INPUT REQUIRED:** funder/grant information or an explicit
  no-external-funding statement.
- **AUTHOR INPUT REQUIRED:** CRediT contribution statement; contributions may
  not be inferred from repository history.
- **AUTHOR INPUT REQUIRED:** conflicts-of-interest and generative-AI disclosure.
- **AUTHOR INPUT REQUIRED:** IEEE Access biography and photograph for every
  author.
- **AUTHOR INPUT REQUIRED:** public repository URL and/or archival DOI before
  claiming that the evidence package is publicly released.
- **AUTHOR INPUT REQUIRED:** exact RTS-GMLC release/vintage beyond the hashed
  files, and an issue-to-delivery archive if operational wording is desired.
- **AUTHOR INPUT REQUIRED:** disclose any shared code, text, figures, data
  preparation, or evidence tables with another manuscript.
- **AUTHOR INPUT REQUIRED:** run or commission a final similarity/plagiarism
  screen and external domain-expert review if required; both remain unverified.

Scientific limitations that wording cannot resolve are the proxy rather than
observed-curtailment target, missing issue/vintage metadata, zero positive
onsets in all selection/calibration cells, one truncated system sequence,
absence of cross-system/complete-year units, and absence of physical, operator,
deployment, safety, and economic validation. The block analysis does not create
those missing units. Changing the protocol, temporal boundaries, families,
block lengths, RNG seeds, or wording gates after seeing the results is not
permitted.
