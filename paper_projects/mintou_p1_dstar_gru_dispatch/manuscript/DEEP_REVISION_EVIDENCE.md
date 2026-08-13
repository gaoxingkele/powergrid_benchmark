# Title-to-Evidence Map

## Binding conservative paper story

This is a fixed-policy, single-system **retrospective lag-forecasting** benchmark and a matched retrieval-mechanism study. It constructs a curtailment-risk proxy from one RTS-GMLC weather year under a fixed SNSP-type acceptance rule and evaluates learned-space analogue retrieval at 1 h and 24 h lags. The source rows have `Year`, `Month`, `Day`, and `Period`, but no forecast issue timestamp, as-of mapping, or data-vintage identifier. The evidence does not support an operational day-ahead claim.

The paper-facing name is **GRU learned-space retrieval (GRU-LSR)**. `DSTAR-GRU` remains the immutable v5/v6 archive label. No digital twin, contrastive loss, or pairwise Siamese objective is implemented; bank and query windows use a shared frozen GRU encoder.

The frozen v6 full-leaderboard contract remains intact:

- At 1 h, Persistence has the lowest v6 MAE: 0.00690531.
- At 24 h, Ablation-SmallBank has the lowest v6 MAE: 0.01534389, but event F1 is 0.000000. It is a degenerate low-MAE outcome, not a recommended winner.
- At 24 h, kNN-RawFeature is the strongest non-degenerate v6 MAE reference: 0.01946336 with event F1 0.131737. It ties Ablation-NoSiamese on both metrics.
- Persistence and Seasonal-24h both have v6 24 h MAE 0.02035887 and event F1 0.340000. Neither is the v6 24 h MAE leader.

The append-only fair-data rerun is stored at `../experiments/p1_s3_fair_v1/`. It reruns a mechanism subset rather than the complete 14-method suite. At cap 0.70, the privileged direct policy transform has zero MAE by construction. Among non-privileged rerun methods, Persistence remains lower-MAE than MAE-selected GRU-LSR at 1 h (0.00690794 versus 0.00777391) and 24 h (0.02054651 versus 0.02076857). MAE selection chooses retrieval-only (`alpha_head=0`) for every seed at both lags. Onset-targeted selection is unsupported because every disjoint selection and calibration phase contains zero positive onsets; the frozen tie fallback chooses the first checkpoint and no-retrieval head.

## Title terms

| Title term | Supported meaning | Direct evidence | Boundary or blocker |
|---|---|---|---|
| **Reproducible** | Fixed code paths, configurations, source/output hashes, seeds, environment, and result tables are recorded. | v6 archive; `TABLE_TO_CONFIG_MANIFEST.md`; fair-v1 `run_manifest.json`. | Computational traceability is not independent reproduction. The fair run used deterministic cuDNN settings, but PyTorch's global deterministic-algorithm switch was unavailable because the preserved environment lacked `sympy`; the manifest records this. |
| **Retrospective** | A query window ends at row $s$ and predicts the proxy at delivery row $s+h$, $h\in\{1,24\}$. | v6 and fair-v1 task builders. | No operational issuance time or source vintage is recorded. |
| **Curtailment-risk** | Fraction of available renewable generation rejected by a fixed load-relative acceptance rule. | Label equation; fair-v1 `build_targets`; v6 `build_series`. | Policy-derived proxy, not measured curtailment, operator action, AC-OPF output, or unit-commitment result. |
| **Benchmark** | Common targets, temporal gates, metrics, baselines, and controls at two lags. | v6 14-method archive; fair-v1 three-cap mechanism subset. | One system and weather year identify every result. Caps 0.60/0.80 do not have a full 14-method rerun. |
| **GRU learned-space retrieval** | A GRU head/embedding, fit-only $k=8$ target bank, and selected or fixed blend controls. | fair-v1 `run_results.csv` logs checkpoint and alpha per seed. | Fair-v1 MAE selection chooses retrieval-only. Onset selection cannot be estimated because its selection phase has no positive onsets. |
| **RTS-GMLC** | Delivery-indexed aggregate load, wind, PV, and branch ratings. | Hashed source files in fair-v1 manifest. | Filenames say `DAY_AHEAD`, but issue/vintage metadata are absent. |

## Contribution terms

| Contribution | Supported statement | Negative/null result that travels with it | Blocker |
|---|---|---|---|
| **C1: retrospective proxy benchmark** | The target is method-independent; fair-v1 gives fitted methods a symmetric phase gate. | Labels are proxies and rankings are conditional on one system/year/policy. | Operational language needs an issuance-to-delivery vintage archive. |
| **C1: onset/transition slice** | Onset remains `y_t >= 0.02` and `y_{t-h} < 0.02`; fair-v1 reserves a separate threshold-calibration phase. | Cap-0.70 test onsets number 57 and 172, but selection and calibration have zero at both lags. The same zero-support condition holds at caps 0.60/0.80. | The frozen threshold fallback is not successful calibration. A new frozen temporal design or additional years are required. |
| **C1: seeded statistics** | Fair-v1 makes common-seed, two-sided exact sign-flip tests primary for six frozen GRU contrasts and applies Holm within each horizon. | Deterministic and cross-cap comparisons are descriptive. Seed pairing covers training randomness only. | No dated preregistration and no independent rerun support stronger language. |
| **C2: learned-space retrieval with matched controls** | Fair-v1 holds the checkpoint fixed across selected/fixed retrieval blends within each objective and logs weights. | MAE-selected `alpha_head=0` means the selected condition is retrieval-only, not a successful mixture. Combined legacy ablations retain their joint scope. | The fair subset does not rerun every v6 baseline or ablation. |
| **C3: conditional retrieval utility** | Under MAE selection, retrieval-only improves GRU-head MAE at both lags over all ten paired seeds (mean deltas -0.00496069 and -0.00220055; Holm p=0.01171875 at each lag). | Persistence remains lower-MAE than the selected GRU condition at both lags. Onset-targeted selection is inapplicable and cannot validate the legacy onset sign reversal under the fair gate. | Mechanistic persistence-prior language remains a hypothesis. |

# Primary Estimand and Analysis Unit

For fair-v1, the primary inferential estimand is the mean **paired within-seed treatment-minus-control** difference over GRU training randomness at cap 0.70, conditional on the fixed RTS-GMLC year, temporal gate, feature/metric definitions, checkpoint budget, retrieval bank, and lag. Six frozen contrasts per horizon compare selected retrieval, fixed 0.5 blending, and the no-retrieval head under matching MAE or onset-F1 selection arms. Lower differences favor treatment for MAE; higher differences favor treatment for onset F1.

The analysis unit is one paired method-seed run, not an hour, onset, network, year, forecast vintage, or deployment. Horizon embargoes leave 2627 test targets at 1 h and 2604 at 24 h, including 57 and 172 cap-0.70 onsets. Reusing the same targets across seeds means uncertainty covers training randomness only.

Fair-v1 uses exact two-sided sign-flip tests and Holm adjustment within the frozen six-contrast horizon family. Persistence, Seasonal-24h, each target-selected Ridge condition, and the direct policy transform have one deterministic row per cap/lag and no seed-based p-value. The direct transform is a privileged construction control, not a competing lag forecaster. The legacy v6 Mann-Whitney/Holm table remains historical evidence for the old run and is not relabeled as fair-v1 inference.

# Comparison Budget and Data Visibility

## Fair-v1 information gate

| Phase | Delivery-row rule | Information use |
|---|---|---|
| Fit | targets below 4380 | Feature normalization, Ridge coefficients, GRU parameters, retrieval bank. |
| Selection | targets `4380+h` through 5255 | Ridge penalty, GRU checkpoint, and blend alpha. |
| Calibration | targets `5256+h` through 6131 | Detection threshold only. |
| Test | targets at or after `6132+h` | Scoring only. |

The horizon gaps ensure each downstream query index is no earlier than the end of the preceding artifact-building phase. Ridge and GRU conditions receive the same visibility. This repairs the v6 delivery-row boundary asymmetry for the rerun subset but cannot establish operational as-of validity because source issuance/vintage fields do not exist.

The target-hour `DAY_AHEAD_*` rows make `DirectPolicyTransform-Privileged` executable. It applies the label rule to target-hour load, wind, and PV and therefore has zero point error. It diagnoses what happens if those rows are admitted; it is not an operational forecast.

## Frozen comparison budget

| Contract item | Budget | Boundary |
|---|---|---|
| Data | First 8760 aligned rows of 8784-row RTS-GMLC files; one weather year. | Same hashed files at all caps; no extra system/year unit. |
| Tasks | Lags 1 h and 24 h; cap 0.70 primary; caps 0.60/0.80 sensitivity. | Cross-cap differences are descriptive same-series reruns. |
| Methods | Direct transform, Persistence, Seasonal-24h, two Ridge selection arms, and two GRU objective arms crossed with selected/fixed blends. | 510 rows total; not a full 14-method leaderboard. |
| GRU budget | 20 epochs; checkpoints 5/10/15/20; hidden size 48; ten common seeds. | Manual eager Adam matches stated equations because packaged `torch.optim` required unavailable `sympy`. |
| Retrieval | Fit-only bank, $k=8$, selected alpha grid plus fixed 0/0.5/1 controls. | Same selected checkpoint across retrieval controls within an objective. |
| Inference | Six paired GRU contrasts per horizon at cap 0.70. | Exact sign-flip plus Holm; deterministic and cap contrasts descriptive. |

# Negative and Null Results

1. The privileged direct policy transform has zero MAE and onset MAE by construction at every cap and lag. This exposes the consequence of admitting target-hour inputs; it is not evidence of forecasting skill.
2. Its onset F1 is below one despite exact continuous predictions because the inherited classifier flags ongoing high-curtailment hours as well as transitions. Predicted positives are not conditioned on the observed quiet-state prerequisite. This is a metric-definition limitation.
3. Every fair-v1 selection and calibration phase has zero onset positives at both lags and all three caps. Onset-targeted checkpoint/blend selection and threshold calibration use frozen fallbacks.
4. Consequently, onset-selected GRU-LSR equals the no-retrieval head in all ten cap-0.70 pairs at each lag (paired p=1). This is inapplicability evidence, not proof of no retrieval effect.
5. MAE selection chooses retrieval-only (`alpha_head=0`) for all ten cap-0.70 seeds at both lags. The result does not show that a head/retrieval mixture is beneficial.
6. Persistence remains descriptively lower-MAE than fair-v1 MAE-selected GRU-LSR at cap 0.70: 0.00690794 versus 0.00777391 at 1 h and 0.02054651 versus 0.02076857 at 24 h.
7. Fixed 0.5 blending improves GRU-head MAE in all ten cap-0.70 pairs at both lags (Holm p=0.01171875), but the selected retrieval-only condition is still lower-MAE than fixed 0.5 in all pairs.
8. Under the unsupported onset-selection fallback, fixed 0.5 improves 1 h test onset F1 over the head in all ten seeds (mean delta 0.02441871; Holm p=0.01171875), while the 24 h difference is null (five wins/five losses; Holm p=1). Because no selection/calibration onsets exist, neither is evidence of successful target-matched selection.
9. Method ordering changes descriptively with the cap: MAE-selected GRU-LSR is slightly below Persistence only at cap 0.60/1 h and cap 0.80/24 h; Persistence is lower in the other four cap/lag cells. These are same-series crossings, not generalization.
10. The fair subset does not rerun legacy SmallBank, raw-kNN, MLP, LSTM, DLinear, TCN, NoTopology, or other full-leaderboard methods. No overall fair-v1 winner is identified.
11. Legacy adverse results remain: v6 GRU-LSR is not the overall MAE leader; its 24 h event/onset performance is weak; NoTopology and TCN contrasts are unresolved in stated cells; and the high-renewable stress subset shows no GRU-LSR advantage.
12. NREL-118 at the frozen cap has zero positive targets and remains a task-transport boundary, not external validation.
13. No result covers another weather year, observed curtailment, forecast vintages, OPF/UC feasibility, probabilistic forecasts, operators, deployment, or economic outcomes.

# Shared Assets and Independent Contribution

- Public substrate: RTS-GMLC and cited NREL-118 assets are external. Public data do not by themselves make this code/evidence package publicly released.
- Legacy v5 source state is commit `3f0371eb5d775f5967ad59120e937d4804bd5a21`; v6 source state is `a728800bd48b11bc8f07647f82e4c9c2841a3e45`. v5/v6 archives remain untouched.
- Claim-specific source order: fair-v1 manifest/results govern fair-gate and crossed retrieval-control claims; v6 governs only the legacy complete leaderboard; manuscript tables/figures still reflect v6 until the separately approved S4 integration.
- Fair-v1 is under `../experiments/p1_s3_fair_v1/` with hashed config, script, source files, outputs, environment, and preserved smoke/failure logs. It did not write to `../../papers/.../evidence`.
- The independent scientific contribution supported here is the P1 retrospective proxy/onset benchmark plus a within-pipeline retrieval evaluation. No independent authorship, external reproduction, deployment, or companion-paper fact is inferred.
- No companion paper is named by this project's acceptance contract. Authors must disclose overlap rather than relying on repository inference.

# New or Rerun Experiments

The append-only `p1_s3_fair_v1` namespace completed on 2026-08-13 with 510 method-seed rows. It verified SHA-256 hashes for load, wind, PV, and branch inputs, evaluated the first 8760 aligned rows, and ran with Python 3.12.13, NumPy 2.3.5, PyTorch 2.13.0/CUDA 13.0, and an RTX 3090. The run manifest records the exact command, configuration/script/output hashes, device, and determinism boundary.

Executed components were:

1. A symmetric fit/selection/calibration/test gate with horizon embargoes for Ridge and GRU conditions.
2. MAE- and onset-F1-targeted checkpoint/hyperparameter arms.
3. Retrieval-on/off, selected-blend, and fixed head-weight 0/0.5/1 controls sharing the selected checkpoint.
4. Ten common seeds with paired exact sign-flip analysis primary at cap 0.70.
5. The privileged target-hour direct policy transform.
6. Method-level sensitivity reruns at caps 0.60 and 0.80 for the stated subset.

The run has not been independently repeated; its Material Passport remains `UNVERIFIED`. Stronger claims still require an issue-time/vintage-aware archive, a frozen design with positive pre-test onset support, a full 14-method fair-gate rerun if a complete leaderboard is needed, another system/year or event-block unit, independent reproduction, and physical/user/deployment validation as appropriate.

# Unresolved Human Blockers

- **AUTHOR INPUT REQUIRED:** final author list and public ORCIDs.
- **AUTHOR INPUT REQUIRED:** complete affiliations and corresponding-author name/e-mail.
- **AUTHOR INPUT REQUIRED:** funder and grant number, or an explicit no-external-funding statement. Funding status may not be inferred.
- **AUTHOR INPUT REQUIRED:** IEEE Access biography and photograph for every author.
- **AUTHOR INPUT REQUIRED:** public repository URL and/or archival DOI if the package is to be called publicly released. Until then, use “benchmark on public RTS-GMLC data.”
- **AUTHOR INPUT REQUIRED:** author-contribution/CRediT statement. Contributions cannot be assigned from repository history.
- **AUTHOR INPUT REQUIRED:** confirm conflicts-of-interest and generative-AI disclosures.
- **AUTHOR INPUT REQUIRED:** identify the exact RTS-GMLC release/vintage and provide issue timestamps or an issue-to-delivery archive if operational language is desired.
- **AUTHOR INPUT REQUIRED:** provide dated support for any “prespecified” or “predeclared” claim; otherwise retain “matched,” “primary,” and “scope check.”
- **AUTHOR INPUT REQUIRED:** disclose shared code, text, figures, data preparation, or evidence tables with another manuscript and state the P1-specific contribution.

Scientific blockers that wording alone cannot resolve are absent issue/vintage metadata, absent observed-curtailment labels, zero positive onset support in all fair-v1 selection/calibration phases, independent reproduction, cross-year/system evidence, physical-feasibility evaluation, and deployment/user evidence. Moving boundaries after inspecting test performance merely to obtain positive onsets or a favorable result is not permitted.
