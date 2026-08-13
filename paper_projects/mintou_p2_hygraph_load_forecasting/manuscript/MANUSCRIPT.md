<!-- MDPI Electronics submission draft (Markdown master).
     Paper: mintou_p2 / CSA-LoadNet (route A claim downgrade, v7 evidence).
     Section suggestion: Artificial Intelligence / Computational Intelligence in Electronics.
     All numbers verified against:
       papers/mintou/mintou_p2_hygraph_load_forecasting/evidence/tables/real_opsd_v7_leaderboard.csv
       papers/mintou/mintou_p2_hygraph_load_forecasting/evidence/tables/real_simbench_v7_leaderboard.csv
       papers/mintou/mintou_p2_hygraph_load_forecasting/evidence/tables/real_ausgrid_v7_leaderboard.csv
       papers/mintou/mintou_p2_hygraph_load_forecasting/evidence/tables/real_p2_v7_significance.csv
       papers/mintou/mintou_p2_hygraph_load_forecasting/src/configs/real_hyg_neural_config.json
       papers/mintou/mintou_p2_hygraph_load_forecasting/src/configs/real_p2_v7_config.json
       papers/mintou/mintou_p2_hygraph_load_forecasting/evidence/source/real_{opsd,simbench}_source_profile.csv
     Binding claim boundary: logic/claims.md (Route A). Prohibited: any hyperbolic-geometry
     advantage claim, any 1h-horizon advantage claim, any hierarchical-scenario advantage
     claim, any "smart dispatch" narrative.
     Figures live in ./figures/ (print-resolution PNG plus PDF/SVG evidence figures;
     regenerate the core figures with figures/make_figures.py and the exact-
     hierarchy enhancement figures with scripts/mintou/make_above_mean_enhancement_figures.py).
     AUTHOR INPUT REQUIRED markers must be resolved before submission. -->

# Cross-Series Attention Neural Forecasting for Day-Ahead Multi-Region Power Load Prediction

**Authors:** Jieyun Zheng (郑洁云), Linyao Zhang (张林垚), Zhanghuang Zhang (张章煌), Zhuolin Chen (陈卓琳), Ying Shi (施莹)
**Affiliations:** Economic and Technological Research Institute of State Grid Fujian Electric Power Co., Ltd., Fuzhou 350000, Fujian, China
**Correspondence:** zjy_0701@163.com (J. Zheng)

## Abstract

Cross-correlated regional load series motivate graph and attention mechanisms, but single-run accuracy tables rarely isolate whether cross-series aggregation itself contributes. CSA-LoadNet combines a shared temporal encoder, cross-series attention, and a compact prediction head for day-ahead multi-region load forecasting. Ten seeded runs under a leakage-free temporal protocol show that, on the six-country Open Power System Data benchmark, the full model improves 24-hour mean absolute percentage error over a multilayer perceptron (0.0323 versus 0.0337; Holm-adjusted p = 0.0085) and over the no-aggregation ablation (0.0323 versus 0.0346; p = 0.0011). No difference among Poincaré, Euclidean, and equal-weight parameterizations is resolved at the available precision. We additionally rebuild Ausgrid as an exact 12-leaf, four-region, one-root hierarchy and evaluate independent, bottom-up, top-down, and OLS reconciliation with ten seeds for every method. DLinear with bottom-up reconciliation is best (hierarchy-weighted sMAPE 0.2802); CSA-LoadNet with OLS reaches 0.2895, while both coherent methods have zero structural violation. The results locate the resolved OPSD day-ahead gain in cross-series aggregation rather than in a particular weighting geometry, while distinguishing forecast accuracy from hierarchical coherence.

**Keywords:** short-term load forecasting; day-ahead forecasting; multi-region load; cross-series attention; ablation study; statistical significance testing; negative results; open power system data

---

## 1. Introduction

Day-ahead load forecasts inform unit commitment, cross-border exchange scheduling, reserve dimensioning, and distribution-level flexibility procurement. In multi-region forecasting, such as countries in an interconnection or profile classes in a distribution network, the individual series share weather regimes, calendar structure, and economic rhythms. This raises a practical question: does cross-series information improve on forecasts constructed independently for each series?

Recent applied studies address this question with increasingly elaborate architectures. Graph convolutions, learned adjacency matrices, spatio-temporal attention stacks, and tensor decompositions have been combined with recurrent or transformer backbones, commonly with the complete architecture leading the reported accuracy table [1–4].

A parallel line of evidence cautions against equating architectural complexity with forecast accuracy. Linear models outperform several transformer variants on standard long-horizon benchmarks [5], statistical methods remain competitive in the M-competitions [6,7], and methodological audits show that some reported gains shrink under stricter protocols [8].

These findings leave a component-level question unresolved. Cross-series models are often evaluated as complete architectures, making it difficult to determine whether aggregation itself helps, whether a particular weighting geometry matters, and whether any gain persists across horizons and aggregation structures.

CSA-LoadNet is a compact neural forecaster in which a shared encoder processes each region's load history and cross-series attention aggregates the other encodings. Attention weights can use Poincaré distance with fixed or learned curvature, Euclidean distance, or equal averaging. Each mechanism is an independent switch.

The primary component comparison contains the full model and five single-switch ablations. A targeted ten-seed comparison with MLP is conducted on OPSD and SimBench after a preliminary three-seed architecture screen; the screen is reported separately and is not treated as equal-strength confirmatory evidence. Ausgrid solar-home data provide an exact hierarchical test against ten models under common reconciliation. Pairwise comparisons use two-sided Mann–Whitney U tests with Holm correction within each dataset–horizon block and its primary metric.

The paper makes three contributions:

1. **A component-identifiable cross-series forecaster.** CSA-LoadNet separates the shared temporal encoder, cross-series aggregation, distance weighting, and curvature choice into independently testable switches. This design distinguishes the value of pooling other series from the value of a particular weighting geometry.
2. **A multi-setting evaluation of aggregation, horizon, and hierarchy.** Strict temporal splits are used on OPSD and SimBench at 1 h and 24 h horizons. An exact 12-leaf, four-region, one-root Ausgrid hierarchy then compares independent forecasts with bottom-up, top-down, and OLS reconciliation under a common summing structure.
3. **An empirical map of where aggregation helps.** On OPSD at 24 h, CSA-LoadNet improves over the targeted MLP comparator and the no-aggregation ablation. The tested weight forms remain unresolved, and the method does not lead at OPSD 1 h or on the exact Ausgrid hierarchy. The result identifies a day-ahead aggregation effect while separating forecast accuracy from structural coherence.

The paper is organized as follows. Section 2 reviews the three research threads the study draws on. Section 3 describes the datasets, tasks, and split protocol. Section 4 specifies CSA-LoadNet and its ablation switches. Section 5 details baselines, training, and statistics. Section 6 reports results, Section 7 interprets the setting-dependent component evidence, Section 8 states limitations, and Section 9 concludes.

---

## 2. Related Work

Three threads frame this study: the deep-architecture lineage of short-term load forecasting, cross-series and graph-structured forecasting, and rigorous evaluations that compare complex forecasters with simple baselines. An extended review with full citation context accompanies the released evidence package.

### 2.1. Deep Architectures for Short-Term and Day-Ahead Load Forecasting

Recurrent networks were among the first deep models to displace classical load forecasters. Building on the LSTM cell [9], Kong et al. demonstrate short-term forecasting at the residential scale [10]. DeepAR extends shared training to large panels of related series [11], an idea reflected in CSA-LoadNet's shared encoder. Temporal convolutional networks offer a lower-cost alternative [12], while the Temporal Fusion Transformer [13] and Informer [14] extend attention-based forecasting.

Applied load forecasting increasingly uses hybrid models, including LSTM–CNN fusion [15], BiLSTM–Transformer combinations [16], decomposition pipelines [17], and LSTM–XGBoost ensembles [18]. Evidence for the added component, however, is commonly limited to one accuracy table. Multi-seed distributions and component-level tests remain uncommon.

### 2.2. Cross-Series and Graph-Structured Load Forecasting

A second thread exploits correlation among regional or nodal series. LSTNet models dependence through joint convolutional–recurrent channels [19]. Graph formulations emerged in traffic forecasting [20], and MTGNN learns adjacency end to end [21]. Power-load examples include LoadSeer [4], GCN–BiLSTM–Adaboost [1], spatio-temporal graph transformers [2], and GCN–Transformer integration [3]. A parallel literature treats multiple series as a hierarchy requiring reconciliation [22,23], with Ausgrid as a common testbed [24].

These graph-based studies propose increasingly elaborate weighting mechanisms. Their comparisons rarely test the selected weighting against equal averaging under an identical seeded protocol. Consequently, the contribution of aggregation can be conflated with that of its parameterization.

### 2.3. Simple Baselines and Honest Evaluation

The third thread concerns evaluation discipline. Sound out-of-sample practice was codified early [25], and temporal leakage from naive cross-validation is well documented [26]. Common metrics also have known failure modes; MAPE becomes unstable near zero loads [27], directly motivating the SimBench and Ausgrid choices. Diebold–Mariano testing [28] made statistical comparison a standard forecasting question. The M competitions [6,7], DLinear [5], and later best-practice guides [8] further emphasize strong simple baselines.

This evaluation literature mainly operates at whole-model granularity. The present study extends it to individual forecaster components, using multiplicity-corrected tests to determine which component claims survive. Section 6.3 applies that logic to the aggregation weight forms.

---

## 3. Datasets, Tasks, and Split Protocol

### 3.1. Datasets and Forecast Tasks

We evaluate on three public datasets chosen to span three distinct multi-series regimes: country-level national loads, distribution-system load profiles, and a customer/region/system hierarchy (Table 1).

**Table 1.** Datasets, series pools, and temporal splits (from `evidence/source/real_opsd_source_profile.csv`, `evidence/source/real_simbench_source_profile.csv`, and `src/configs/real_ausgrid_exact_hierarchy_v8_config.json`).

| Property | OPSD | SimBench | Ausgrid |
|---|---|---|---|
| Source | Open Power System Data, 60 min single-index time series [29] | SimBench complete mixed dataset, `LoadProfile.csv` [30] | Ausgrid solar-home half-hourly data [24] |
| Series pool | 6 country loads: DE, FR, IT, ES, NL, PL | 8 load profiles: BL-H, G0-A, G0-M, G1-A, G1-B, G1-C, G2-A, G3-A (hourly aggregation) | Exact 17-node hierarchy: 12 highest-energy complete customers + four deterministic postcode groups formed only from those leaves + their exact system sum (hourly GC) |
| Period used | 2015-01-01 to 2018-12-31 (35,000 hourly rows) | full year 2016 (8760 h) | 2010-07 to 2013-06 (3 years) |
| Train/test boundary | index 24,500 = 2017-10-19 03:00 (70% train) | index 6132 = 2016-09-12 13:45 (70% train) | 70% chronological train |
| Horizons | 1 h and 24 h | 1 h and 24 h | 24 h |
| Primary metric | MAPE | normalized MAE | sMAPE |

Each horizon-h task predicts each series' load h hours beyond the forecast origin from the preceding 168 h of that pool's history; sliding the origin hourly across the test segment produces the full evaluation trajectory. The 24 h task is the day-ahead task around which this paper's claims are organized.

### 3.2. Primary Metrics and Why They Differ per Dataset

The primary metric is chosen per dataset to avoid known metric pathologies [27]. For a fixed dataset–horizon test set of $N$ targets, the implementation computes

$$
\operatorname{MAPE}=\frac{1}{N}\sum_{j=1}^{N}\frac{|y_j-\hat y_j|}{\max(\epsilon,|y_j|)},
$$

$$
\operatorname{nMAE}=\frac{N^{-1}\sum_{j=1}^{N}|y_j-\hat y_j|}
{\max\!\left(\epsilon,\max_j y_j-\min_j y_j\right)},
$$

and


$$
\operatorname{sMAPE}=\frac{1}{N}\sum_{j=1}^{N}
\frac{2|y_j-\hat y_j|}{\max(\epsilon,|y_j|+|\hat y_j|)},
$$

with $\epsilon=10^{-6}$. The normalization range in nMAE is computed once from the common test targets; it is an evaluation scale and is identical for all methods, not a training input. Country-level OPSD loads are strictly positive and far from zero, so MAPE is interpretable there. SimBench profile values approach zero at many timestamps, where MAPE denominators become unstable; SimBench methods are therefore ranked by nMAE and MAPE is retained descriptively.

For the exact Ausgrid hierarchy, let $\bar s_L$, $\bar s_R$, and $s_T$ be the mean node sMAPE over the 12 leaves, the four regions, and the root. The predeclared primary metric gives each level equal weight rather than letting 12 leaves dominate:

$$
\operatorname{HWSMAPE}=\frac{\bar s_L+\bar s_R+s_T}{3}.
$$

With bottom-level forecast matrix $\hat{B}$ and summing matrix $S\in\{0,1\}^{17\times12}$, structural coherence requires $\hat{Y}=S\hat{B}$. We report the scale-normalized violation

$$
C(\hat Y)=\frac{1}{5T}\sum_{i=13}^{17}\sum_{t=1}^{T}
\frac{|\hat y_{it}-(S\hat B)_{it}|}{\max(\epsilon,T^{-1}\sum_t|y_{it}|)}.
$$

Bottom-up, top-down, and OLS projection reconciliation are evaluated separately from forecasting accuracy. All significance tests in Section 6 use the primary metric of the respective dataset; secondary metrics, including MAE, RMSE, level-specific sMAPE, peak-load error, and coherence violation, are preserved in the evidence tables.

### 3.3. Leakage-Free Temporal Protocol

Forecasting comparisons are sensitive to temporal leakage [8,26], so every preprocessing and selection step follows the chronological boundary in Table 1. The data are not shuffled, and no test-period observation enters training or model selection. Per-series z-normalization statistics are fitted on the training segment. Early stopping uses its final 15% as a temporally later validation slice. Training samples are strided to fit the CPU budget (Section 5.2), whereas every test trajectory is evaluated in full. The released source profiles record the files, row counts, and boundary timestamps needed to reconstruct each split.

---

## 4. CSA-LoadNet

Figure 1 gives the complete forecasting path. Load histories and calendar variables enter a shared temporal encoder; target and context series are related only inside the cross-series attention block; and the fused representation enters the horizon-specific forecasting head. The three weight forms shown under the attention block are controlled alternatives evaluated with the same downstream network.

![Figure 1. End-to-end CSA-LoadNet architecture and evaluation assets.](figures/fig_architecture.png)

**Figure 1.** CSA-LoadNet data and model flow. The lower strip identifies independent evaluation datasets; it is not an input path. Poincare, Euclidean, and equal-weight attention share the same encoder, fusion, head, and training protocol.

CSA-LoadNet (Cross-Series Attention Load Forecasting Network) is intentionally small: a shared temporal encoder, one cross-series attention block, and a compact prediction head. The design goal is not architectural novelty for its own sake but a testbed in which every mechanism is an independent switch, so that the component analysis of Section 6.2–6.3 attributes effects cleanly.

**Formal definitions.** For series \(i\), the 168-hour history is standardized with fit-split statistics only,

$$
\tilde x_{i,t-\ell}=\frac{x_{i,t-\ell}-\mu_i^{\mathrm{fit}}}{\sigma_i^{\mathrm{fit}}+\epsilon},
\qquad \ell=0,\ldots,167.
$$

The shared two-layer encoder is

$$
h_i=W_2\,\phi(W_1\tilde X_{i,t}+b_1)+b_2,\qquad
W_1\in\mathbb R^{96\times168},\; W_2\in\mathbb R^{48\times96},
$$

where \(\phi\) is ReLU. When hyperbolic weighting is enabled, embeddings are projected inside the unit ball and their Poincare distance is

$$
\bar e_i=\frac{\tanh(\|e_i\|_2)}{\|e_i\|_2+\epsilon}e_i,\qquad
d_{\mathbb B}(\bar e_i,\bar e_j)=
\operatorname{arcosh}\!\left(1+
2\frac{\|\bar e_i-\bar e_j\|_2^2}
{(1-\|\bar e_i\|_2^2)(1-\|\bar e_j\|_2^2)}\right).
$$

The Euclidean control replaces \(d_{\mathbb B}\) by \(\|e_i-e_j\|_2\), and the equal-neighbor control fixes \(\alpha_{ij}=1/(m-1)\). For any weight form, context fusion is

$$
g_i=\sum_{j\ne i}\alpha_{ij}W_vh_j,\qquad
u_i=[h_i\|g_i\|\operatorname{cal}(t+h)] .
$$

The prediction head and empirical training risk are

$$
\hat y_{i,t+h}=w_o^\top\phi(W_ou_i+b_o)+b_y,
$$

$$
\mathcal L_h(\Theta)=\frac{1}{|\mathcal T_{\mathrm{fit}}|m}
\sum_{t\in\mathcal T_{\mathrm{fit}}}\sum_{i=1}^{m}
\left(\tilde y_{i,t+h}-\hat y_{i,t+h}\right)^2 .
$$

With \(m\) series, embedding width \(d_e\), and temporal width \(d_h\), the cross-series block costs \(O(m^2d_e+m^2d_h)\) per batch item; the TemporalOnly ablation removes the quadratic terms. This complexity statement concerns the implemented dense pool, not sparse graph attention.

### 4.1. Shared Temporal Encoder

For each series $i$ in the pool, the past 168 hours of per-series z-normalized load are passed through a shared multilayer perceptron $168 \to 96 \to 48$, yielding a temporal encoding $h_i \in \mathbb{R}^{48}$. Sharing one encoder across all series follows the cross-learning principle established by panel forecasters such as DeepAR [11]: every series' history contributes gradient signal to the same temporal features, which matters when pools are small (6–17 series here).

### 4.2. Cross-Series Attention Aggregation

Each series additionally owns a learned embedding $e_i \in \mathbb{R}^{8}$. To forecast target series $i$, the module computes attention weights over the other series in the pool,

$$
\alpha_{ij} = \frac{\exp\!\big(-c_i \, d(e_i, e_j)\big)}{\sum_{k \neq i} \exp\!\big(-c_i \, d(e_i, e_k)\big)},
$$

and aggregates their value-mapped temporal encodings into a context vector $g_i = \sum_{j \neq i} \alpha_{ij} \, W_v h_j$. In the default configuration, $d(\cdot,\cdot)$ is the geodesic distance in a Poincaré ball and $c_i = \mathrm{softplus}(\kappa_i) + 0.1$ is a per-target learnable inverse-temperature/curvature parameter. The Poincaré parameterization is one interchangeable option for producing $\alpha_{ij}$. Section 6.3 shows that it is statistically inseparable from Euclidean-distance and equal weights; accordingly, no geometric property is claimed as a contribution. The component under test is the aggregation step itself: whether $g_i$ should exist at all.

### 4.3. Prediction Head and Calendar Features

The prediction head concatenates the target encoding, aggregated context, and a calendar vector derived from the forecast timestamp. A hidden layer of width 64 maps this vector to the scalar h-step-ahead prediction: $\hat{y}_{i,t+h} = \mathrm{MLP}_{64}\big([\,h_i \,\|\, g_i \,\|\, \mathrm{cal}(t+h)\,]\big)$. The parameter count is held in the same budget class as the MLP baseline (Section 5.1), reducing capacity as an alternative explanation for accuracy differences.

### 4.4. Ablation Switches

Five single-switch variants isolate each mechanism (configuration keys from `src/configs/real_hyg_neural_config.json`):

- **TemporalOnly** (`no_graph`): removes the aggregation module entirely; the head sees only $h_i$ and calendar features. This is the switch that tests whether cross-series aggregation contributes at all.
- **Euclidean weights** (`euclidean`): replaces the Poincaré distance with Euclidean distance in the same weight formula.
- **Equal-weight neighbors** (`equal_neighbors`): replaces learned attention with uniform averaging over the pool.
- **Fixed curvature** (`fixed_curvature`): freezes $c_i$ instead of learning it.
- **No calendar** (`no_calendar`): removes the calendar feature vector from the head.

The middle three switches jointly probe the *form* of the aggregation weights; TemporalOnly probes the *existence* of aggregation; NoCalendar probes an orthogonal feature channel.

### 4.5. Weighting Variants and Artifact Labels

The implementation exposes Poincaré, Euclidean, equal-weight, fixed-curvature, and learnable-curvature weighting variants through the ablation switches defined above. The empirical question is whether cross-series aggregation contributes and, separately, whether any tested weighting form is distinguishable. Some archived result tables use the earlier implementation label `HyG-LoadFormer (neural)` for the full configuration; the evidence README maps this label one-to-one to CSA-LoadNet. All manuscript claims use the component definitions rather than the historical name.

---

## 5. Experimental Setup

### 5.1. Methods Compared

Table 2 lists the methods. The five external baselines are compact PyTorch implementations spanning the standard neural-forecasting families: MLP, LSTM [9,10], TCN [12], DLinear [5], and a lightweight PatchTST variant (patch-based transformer, reduced depth to fit the shared CPU budget). All models — proposed, ablations, baselines — consume the same 168 h z-normalized inputs, the same splits, and the same full test sets.

**Table 2.** Methods and roles.

| Method | Role | Note |
|---|---|---|
| CSA-LoadNet | proposed | Section 4; evidence label `HyG-LoadFormer (neural)` |
| TemporalOnly | ablation | aggregation removed |
| Euclidean weights | ablation | weight-form switch |
| Equal-weight neighbors | ablation | weight-form switch |
| Fixed curvature | ablation | weight-form switch |
| No calendar | ablation | calendar channel removed |
| MLP | targeted baseline | selected from the preliminary compact-model screen for ten-seed confirmation |
| LSTM | baseline | recurrent |
| TCN | baseline | dilated causal convolutions |
| DLinear | baseline | linear decomposition model [5] |
| PatchTST-lite | baseline | patch transformer, reduced depth |

### 5.2. Training Protocol and Hyperparameter Disclosure

Table 3 discloses every training-relevant setting; none was tuned on test data, and the configuration is held fixed across datasets rather than optimized per benchmark. The only per-dataset deviations are the documented Ausgrid budget reductions (10 epochs, stride 6) required by the larger 17-series pool.

**Table 3.** Full hyperparameter disclosure (from `src/configs/real_hyg_neural_config.json` and `src/configs/real_p2_v7_config.json`).

| Setting | Value |
|---|---|
| Lookback window | 168 h |
| Temporal encoder | shared MLP 168 → 96 → 48 |
| Series embedding dimension | 8 |
| Curvature/temperature | $\mathrm{softplus}(\kappa_i) + 0.1$, learnable per target (frozen in the FixedCurvature ablation) |
| Head | concat[target encoding, aggregated context, calendar] → 64 → 1 |
| Optimizer / loss | Adam, lr $10^{-3}$ / MSE on per-series z-normalized targets |
| Batch size | 512 |
| Epochs | 15 (OPSD, SimBench); 10 (Ausgrid) |
| Training-sample stride | 3 (OPSD, SimBench); 6 (Ausgrid); test sets never strided |
| Early stopping | validation = final 15% of training window by time; best-validation state restored |
| Seeds (decision set) | 10: {11, 23, 47, 59, 71, 83, 97, 109, 127, 139} |
| Seeds (exact Ausgrid hierarchy) | same 10 seeds for every proposed, ablation, and baseline model |
| Reconciliation | Base, Bottom-Up, Top-Down, OLS projection; parameters estimated without test targets |
| Hardware / framework | CPU for OPSD/SimBench; RTX 3090 with PyTorch 2.13.0+cu130 for the v8 Ausgrid rerun |

**Fairness statement.** Every model in a comparison shares the training regime, normalization, split boundaries, early-stopping rule, and computational budget class; the proposed model is held at the MLP baseline's parameter budget. The exact Ausgrid rerun moves all eleven models to the same GPU execution path and gives all of them the same ten seeds. Hardware changes between dataset blocks but never within a comparison block; runtime values are interpreted only within datasets.

### 5.3. Statistical Methodology

The primary model set, CSA-LoadNet, its five ablations, and MLP, was run for ten seeds per dataset/horizon on OPSD and SimBench. Each block contains six proposed-versus-opponent comparisons. On the corrected Ausgrid hierarchy, all eleven models use the same ten seeds under four reconciliation regimes. Primary OLS model tests use two declared five-comparison role families. A paired sensitivity analysis contains all ten opponents. The prespecified primary analysis uses two-sided Mann--Whitney U tests with Holm correction. The complete table reports rank-biserial effects and pointwise, multiplicity-unadjusted 5000-resample mean-difference intervals (`real_p2_primary_inference_v2.csv`). Exact paired sign-flip tests use the common seeds as a sensitivity analysis; Holm-adjusted p-values determine significance in each declared family.

For reproducibility, let $e_{a,s}$ be the primary error of method $a$ at seed $s$. The reported mean and dispersion are

$$
\bar e_a=\frac{1}{n_a}\sum_{s=1}^{n_a}e_{a,s},\qquad
s_a=\sqrt{\frac{1}{n_a-1}\sum_{s=1}^{n_a}(e_{a,s}-\bar e_a)^2}.
$$

For a proposed--baseline comparison with rank sum $R_1$, the Mann--Whitney statistic is

$$
U_1=n_1n_2+\frac{n_1(n_1+1)}{2}-R_1,\qquad
U=\min(U_1,n_1n_2-U_1).
$$

If $p_{(1)}\leq\cdots\leq p_{(m)}$ are the ordered raw p-values within one dataset--horizon family, the monotone Holm-adjusted values used in Figure 3 are

$$
p^{\mathrm{Holm}}_{(i)}=
\max_{1\leq j\leq i}\min\!\left(1,(m-j+1)p_{(j)}\right).
$$

The seed-paired descriptive effect in Figure 6 is computed only when the same seeds exist for both methods,

$$
\Delta_s=100\,\frac{e_{b,s}-e_{a,s}}{e_{b,s}},
$$

so positive values favor CSA-LoadNet. This percentage is an effect display, not the test statistic. No pair with unequal seed support is promoted to a paired inferential comparison.

---

## 6. Results

### 6.1. Day-Ahead Main Result on OPSD

Figure 2a and Table 4 present the OPSD 24 h leaderboard over ten seeds. CSA-LoadNet attains mean MAPE 0.032345 (std 0.000817), compared with 0.033715 (std 0.000587) for MLP, a 4.1% relative improvement that is Holm-significant (p = 0.0085). MLP was the strongest observed external model in the preliminary three-seed OPSD screen; the exact-hierarchy Ausgrid study yields a different ordering led by DLinear. The no-aggregation TemporalOnly ablation reaches 0.034591, 6.5% above the full model (p = 0.0011, U = 0). In the paired sensitivity analysis, CSA-minus-MLP MAPE is -0.001371 (pointwise 95% bootstrap CI [-0.001826, -0.000927]) and CSA-minus-TemporalOnly is -0.002246 ([-0.002813, -0.001741]); both paired Holm p = 0.0117.

**Table 4.** OPSD day-ahead (24 h) leaderboard: mean ± std MAPE over 10 seeds, with the Holm-adjusted p of the comparison against CSA-LoadNet (from `real_opsd_v7_leaderboard.csv` and `real_p2_v7_significance.csv`).

| Method | Mean MAPE | Std | Holm p vs. proposed | Verdict |
|---|---|---|---|---|
| No calendar | 0.031873 | 0.000563 | 0.485 | not separable |
| Euclidean weights | 0.032257 | 0.000738 | 1 | not separable |
| Fixed curvature | 0.032302 | 0.000717 | 1 | not separable |
| **CSA-LoadNet (proposed)** | **0.032345** | **0.000817** | — | — |
| Equal-weight neighbors | 0.032469 | 0.000506 | 1 | not separable |
| MLP | 0.033715 | 0.000587 | 0.0085 | **significant win** |
| TemporalOnly (no aggregation) | 0.034591 | 0.000251 | 0.0011 | **significant win** |

![Figure 2. Merged day-ahead leaderboards: (a) OPSD 24 h MAPE, (b) SimBench 24 h normalized MAE, mean ± std over 10 seeds.](figures/fig_leaderboard.png)

**Figure 2.** Day-ahead (24 h) leaderboards on (**a**) OPSD (MAPE) and (**b**) SimBench (normalized MAE), mean ± std over 10 seeds. On OPSD the proposed model separates significantly from the MLP baseline and the no-aggregation ablation; on SimBench no separation from the MLP is established and the MLP mean is ahead.

Two features of Table 4 constrain interpretation. NoCalendar has the best nominal mean at this horizon (0.031873), but its difference from the full model is not significant ($p=0.485$) and does not recur significantly elsewhere. The result suggests that the calendar channel may add little at 24 h, but it is not treated as a supported component finding. The three weight-form ablations also remain within ±0.4% of the full model, foreshadowing Section 6.3.

For context, in the preliminary 3-seed v6 screen on the same OPSD 24 h split, TCN, PatchTST-lite, DLinear, and LSTM trail MLP (MAPE 0.0361, 0.0378, 0.0408, and 0.0527, respectively, versus 0.0339). This screen motivated selecting MLP for the ten-seed decision set, but its four-method ordering is supporting evidence rather than equal-strength confirmatory inference.

### 6.2. Component Significance Across All Settings

Figure 3 condenses the complete decision analysis: every proposed-versus-opponent comparison in all five dataset/horizon settings, with its Holm-adjusted p-value and verdict.

![Figure 3. Component significance matrix: CSA-LoadNet vs each opponent across five dataset/horizon settings, Mann–Whitney U with Holm correction, 10 seeds per cell.](figures/fig_component.png)

**Figure 3.** Component-level significance summary (Mann–Whitney U, Holm-corrected, 10 seeds per cell). Exactly two non-hierarchical comparisons are significant wins--OPSD 24 h against MLP and against the no-aggregation ablation--and OPSD 1 h contains a significant loss to MLP. The corrected hierarchy and its DLinear loss are reported separately in Figures 4--5. The entire weight-form block remains inseparable in every setting.

The matrix summarizes the paper's central result. At OPSD 24 h, both the external comparison and the aggregation-existence comparison separate significantly. At the 1 h settings, TemporalOnly is nominally worse than the full model but the differences are not significant (OPSD, p = 0.188; SimBench, p = 0.271). The aggregation signal is also absent at SimBench 24 h and Ausgrid (p = 1 in both), with TemporalOnly nominally ahead at SimBench 24 h. No weight-form comparison approaches significance; every Holm-adjusted p in that comparison family equals 1.

### 6.3. Aggregation Helps, but the Tested Weight Forms Do Not Separate

Cross-series aggregation and aggregation-weight form produce different empirical conclusions. The no-aggregation comparison separates on OPSD at 24 h, whereas the ten-seed comparisons among Poincaré, Euclidean, equal-weight, and curvature variants do not resolve a difference:

- **Poincaré vs. Euclidean distance weights:** not separable in any of the five settings (Holm p = 1 in all five; largest observed mean gap below 0.5% relative).
- **Poincaré vs. equal-weight averaging:** not separable in any setting (Holm p = 1 in all five). Learned attention coefficients, whatever their geometry, do not demonstrably beat uniform pooling of the neighbor encodings at these pool sizes.
- **Learnable vs. fixed curvature:** not separable in any setting (Holm p = 1 in all five). The adaptive-curvature parameter, the most distinctive ingredient of the original design, has no measurable effect.

Together with the TemporalOnly separation in Section 6.1, the evidence supports a narrower attribution: cross-series aggregation is useful in the OPSD day-ahead setting, whereas no difference among the tested weighting schemes is resolved at the available statistical precision. Equal-weight neighbor averaging is therefore a simpler empirically competitive option, not a demonstrated equivalent of the learned weight forms. For graph-based load forecasting, the result shows why single-run point estimates are insufficient for component attribution. For this paper, it determines the claim structure: the Poincaré embedding is treated as an implementation option, and the contribution centers on the aggregation-existence comparison that survived testing.

The weight-form result is specific to the tested pools, horizons, and training budget. Larger pools, sparser cross-correlations, or genuinely tree-structured populations might separate the variants (Section 8). The protocol detected the observed 4.1% OPSD MAPE difference, but no weighting-form difference was resolved after multiplicity correction. Because an equivalence margin was not specified, the simpler variants are empirically competitive rather than proven equivalent.

### 6.4. The Hierarchical Setting: Where the Method Loses

The Ausgrid experiment uses an exact hierarchy built from the 12 selected complete customers: four deterministic postcode-sorted groups each sum three leaves, and the root sums all 12. Figure 4 makes the 17-by-12 summing structure explicit; the identity $Y=SB$ holds at every hour. Earlier non-exact aggregates are excluded from every result reported here.

![Figure 4. Exact Ausgrid hierarchy used by the corrected experiment.](figures/fig_exact_hierarchy_design.png)

**Figure 4.** Corrected Ausgrid hierarchy. The four intermediate series and the system total are deterministic sums of the same 12 leaves used by every forecasting method; no outside customer enters an aggregate.

Each model first forecasts all 17 nodes independently. Base forecasts are then compared with bottom-up aggregation, top-down allocation using training-period leaf proportions, and the OLS projection $S(S^{\mathsf T}S)^{-1}S^{\mathsf T}\hat Y$. Bottom-up and OLS are exactly coherent; the mean base-forecast coherence violation across the displayed methods is 0.035. Accuracy and coherence are not interchangeable. DLinear with bottom-up reconciliation is best at hierarchy-weighted sMAPE 0.28017, followed by DLinear with OLS at 0.28047. CSA-LoadNet with OLS reaches 0.28949. Under the same OLS transformation, CSA-LoadNet significantly loses to DLinear (Holm $p=0.000985$), significantly beats LSTM ($p=0.000913$), and is unresolved against MLP, TCN, and PatchTST-lite. The paired CSA-minus-DLinear difference is 0.00902 (pointwise 95% bootstrap CI [0.00606, 0.01215], paired Holm p = 0.0195).

![Figure 5. Accuracy and structural coherence on the corrected Ausgrid hierarchy.](figures/fig_exact_hierarchy_reconciliation.png)

**Figure 5.** (a) Hierarchy-weighted sMAPE under independent, bottom-up, and OLS-reconciled forecasts (ten seeds per model). (b) Mean structural violation. Bottom-up and OLS enforce exact coherence, but DLinear remains more accurate than CSA-LoadNet; reconciliation does not rescue the architectural ranking.

The corrected result strengthens the boundary claim rather than the method claim. Cross-series aggregation helps on the six-country OPSD pool at 24 h, where national loads supply mutually informative context. On the exact customer hierarchy, a strong linear decomposition with deterministic aggregation is better. The experiment therefore supports using coherence constraints where accounting identities matter and reserving CSA-LoadNet for settings in which cross-series context, rather than hierarchy alone, carries predictive information.

### 6.5. Short-Horizon and SimBench Boundaries

The remaining cells of Figure 3 complete the boundary map. On OPSD 1 h, the MLP significantly beats CSA-LoadNet (0.010155 versus 0.010689 mean MAPE; primary Holm $p=0.0348$). The supplementary paired sensitivity agrees: CSA-minus-MLP MAPE is 0.000534 (pointwise 95% CI [0.000248, 0.000826], paired Holm $p=0.0469$). At this lead time, recent target history may dominate the aggregation context. On SimBench, neither horizon separates from the MLP. The proposed mean is only trivially lower at 1 h (0.033349 versus 0.033385 nMAE; $p=1$), whereas the MLP mean is lower at 24 h (0.058591 versus 0.060662; $p=0.084$). We therefore make no SimBench superiority or parity claim.

Figure 6 expresses the five primary comparisons as seed-paired relative error changes. Positive values favor CSA-LoadNet. Only OPSD 24 h combines a positive mean effect with corrected significance. OPSD 1 h and the corrected Ausgrid hierarchy favor their strongest named comparators; SimBench 1 h is effectively zero, and SimBench 24 h trends against the proposed model. This cross-dataset view prevents the single favorable cell from being mistaken for general superiority.

![Figure 6. Cross-dataset seed-paired relative primary-error changes for CSA-LoadNet.](figures/fig_cross_dataset_effects.png)

**Figure 6.** Seed-paired relative reduction in each dataset's primary error for CSA-LoadNet against the named comparator. Bars show the mean and error bars show the standard deviation across matched seeds; positive values favor CSA-LoadNet. The historical evidence label `HyG-LoadFormer (neural)` maps one-to-one to CSA-LoadNet. Inferential decisions use the Holm-adjusted tests and the corrected hierarchy table, not visual overlap.

### 6.6. Cross-Setting Rank and Compute Profiles

Figure 7 replaces selective pairwise reading with a complete current rank profile. Every available model is ranked by the prespecified primary metric in each of the five dataset--horizon settings; the Ausgrid column uses the exact hierarchy under common OLS reconciliation. CSA-LoadNet ranks in the middle of the OPSD 1 h field, first on OPSD 24 h, near the front but unresolved against several methods on SimBench, and below DLinear on Ausgrid. Missing cells indicate methods not run in a setting and are not imputed. We do not form a cross-dataset average rank because MAPE, normalized MAE, and hierarchy-weighted sMAPE answer different scale questions.

![Figure 7. Model ranks where reported over the five primary forecasting settings.](figures/fig_cross_setting_ranks.png)

**Figure 7.** Ranks by dataset-specific primary error. Rank 1 is the lowest mean error within a column. Dashes mark methods absent from an experiment. Non-hierarchical cells use the ten-seed OPSD and SimBench leaderboards; the Ausgrid column uses the exact hierarchy with OLS reconciliation.

The run-time profile in Figure 8 supplies the computational counterpart. The same compact architecture is inexpensive on OPSD and SimBench and slower on the 17-series Ausgrid hierarchy. The y-axis intentionally retains each dataset's primary metric, so vertical locations must not be compared across datasets; the panel asks whether a reported accuracy cell is accompanied by an exceptional computational burden, not whether the error scales are interchangeable.

![Figure 8. Dataset-specific compute and error profile of CSA-LoadNet.](figures/fig_compute_error_profile.png)

**Figure 8.** Mean wall-clock time and dataset-specific primary error for CSA-LoadNet at each evaluated horizon. The x-axis is logarithmic. Timings are interpreted within dataset and execution environment, not across CPU and GPU blocks.

**Table 5.** Stability summary across the complete primary-metric comparisons. "Supported" requires Holm-adjusted (p<0.05); a nominal mean ordering without corrected separation is not counted.

| Setting | Proposed mean position | Corrected decision against strongest named baseline | Interpretation |
|---|---|---|---|
| OPSD, 1 h | Behind MLP | Significant loss | Short-horizon boundary |
| OPSD, 24 h | Ahead of MLP | Significant win | Supported day-ahead result |
| SimBench, 1 h | Approximately tied | Not separable | No superiority claim |
| SimBench, 24 h | Behind MLP | Not separable | Adverse nominal trend |
| Ausgrid, 24 h | Behind DLinear under OLS | Significant loss | Coherence achieved; no accuracy-superiority claim |

The table and rank profile locate the observed effect. Cross-series aggregation is supported in the OPSD day-ahead setting, accompanied by two adverse settings and two unresolved settings. The tested attention geometries do not extend this result to the other settings.

---

## 7. Discussion

### 7.1. Aggregation, Weighting, and Hierarchical Coherence

The ten-seed component comparison supports cross-series aggregation over the no-aggregation control on OPSD at 24 h. The targeted MLP comparison separates in the same setting. By contrast, the analysis does not distinguish Poincaré, Euclidean, equal-weight, or curvature variants, so the observed benefit concerns aggregation rather than the geometry used to weight neighbors. The preliminary three-seed architecture screen explains the choice of MLP for confirmation but does not carry the same evidential weight.

The exact Ausgrid experiment answers a different question. It constructs all four regional aggregates and the root from the same 12 leaves and applies common reconciliation transformations to every method. Bottom-up and OLS reconciliation remove structural violations, yet DLinear remains more accurate than CSA-LoadNet. Coherence is therefore a constraint that can be enforced after forecasting; it is not evidence that the underlying forecaster is accurate.

Taken together, the experiments locate rather than generalize the benefit. Pool context is useful in the OPSD day-ahead setting, whereas additional weighting complexity is unsupported at the evaluated pool sizes. Multiple temporal origins and independently repeated weather years would test whether this pattern persists beyond the selected splits.

### 7.2. Why Aggregation Helps at 24 h and Not at 1 h

The horizon asymmetry in Figure 3 admits a simple reading. At one-hour lead, each country's own most recent observations carry nearly all recoverable information, and any capacity spent on pool context competes with capacity spent on the target's own dynamics — hence a plain MLP on the target window wins outright. At day-ahead lead, the target's terminal observations are 24 h stale; what generalizes across that gap is shared structure — synchronized daily and weekly shapes, common weather-driven regimes — which is exactly what a pooled context vector over five neighboring national loads can supply. The TemporalOnly column supports this reading quantitatively: its deficit against the full model is decisive at OPSD 24 h (p = 0.0011), directionally present but non-significant at the 1 h settings, and absent on Ausgrid where the pool is uninformative. We offer this as an interpretation consistent with the evidence, not as a tested mechanism.

### 7.3. Implications for the Cross-Series Forecasting Literature

Our results neither reject cross-series modeling nor support additional weighting complexity. In the OPSD multi-region day-ahead setting, aggregation improves MAPE by 6.5% and survives both the prespecified test and paired sensitivity analysis. By contrast, no difference among the tested weight forms is resolved in any setting; equivalence within a prespecified tolerance was not tested. This contrast shows why mechanism claims require repeated component-level evaluation. In this study, the OPSD and SimBench decision sets were feasible on CPU, while the larger exact-hierarchy rerun used a single RTX 3090.

---

## 8. Limitations

1. **Claims are confined to day-ahead, pool-level multi-region forecasting.** The single significance-backed superiority result is OPSD 24 h (vs. MLP and vs. the no-aggregation ablation). We make no claim at the 1 h horizon — on OPSD 1 h the method significantly loses to the MLP (Holm p = 0.0348) — and no claim on SimBench, where both horizons are inseparable from the MLP (24 h: p = 0.084 with the MLP mean ahead; 1 h: p = 1 with means nearly identical).
2. **The method does not transfer to the exact customer/region/system hierarchy as implemented.** Under the common OLS reconciliation, CSA-LoadNet significantly loses to DLinear (Holm $p<0.001$), while its contrasts against MLP, TCN, and PatchTST-lite remain unresolved under the primary family. Bottom-up, top-down, and OLS reconciliation are included and the coherent variants satisfy the accounting identities exactly, but reconciliation does not make the proposed forecaster more accurate than the strongest linear baseline. MinT with covariance shrinkage and end-to-end coherence-constrained training remain untested.
3. **The weight-form inseparability is a bounded negative.** It holds for pools of 6–17 series on these three public benchmarks under our training budget; larger pools, sparser correlation structure, or genuinely tree-structured populations could separate the weight parameterizations. Our finding licenses skepticism, not a universal impossibility statement.
4. **Bounded training budgets.** All models, baselines included, use compact configurations with bounded epochs and strided training samples. OPSD and SimBench were trained on CPU and the exact Ausgrid experiment on one RTX 3090. Budgets are matched within each comparison block, but absolute errors and even rankings could change under architecture-specific large-scale tuning.
5. **One fixed hierarchy and one temporal split.** The corrected Ausgrid study removes the leaf/aggregate inconsistency and uses ten seeds for every model, but it still tests one deterministic 12-leaf grouping and one chronological split. Alternative geographic groupings, rolling origins, and larger customer populations could yield different reconciliation rankings.
6. **No exogenous weather inputs.** All models forecast from load history and calendar information alone; weather-aware extensions remain untested on real data in this study, and no claim about them is made.
7. **Weather-year sensitivity is untested.** The OPSD conclusions rest on a single chronological split of the 2015–2018 period, whose test segment (October 2017 through December 2018, Table 1) spans essentially one weather-year. Because all inputs are load history and calendar features, an unusually mild or extreme weather-year could shift both absolute errors and the size of the cross-series aggregation benefit — synchronized weather regimes are precisely the shared structure we conjecture the pooled context exploits (Section 7.2). The findings have not been replicated across alternative multi-year split positions, and we make no claim of weather-year robustness.

---

## 9. Conclusions

This study determines which components of a cross-series attention forecaster earn empirical support. On the public six-country OPSD benchmark, CSA-LoadNet significantly outperforms the ten-seed MLP comparator at 24 h (mean MAPE 0.0323 versus 0.0337; Holm $p=0.0085$). It also outperforms its no-aggregation ablation (Holm $p=0.0011$) over ten seeded runs under a leakage-free temporal protocol. The remaining four compact neural families were screened with three seeds and do not carry the same confirmatory weight. Cross-series aggregation is therefore supported only for the stated day-ahead multi-region setting.

The form of the aggregation weights is not supported as a differentiator. No difference among hyperbolic, Euclidean, equal-weight, and fixed-curvature variants is resolved in the tested non-hierarchical settings; equivalence was not tested. Outside the OPSD day-ahead setting, the method loses at 1 h on OPSD, does not separate from MLP on SimBench, and loses to DLinear on the exact Ausgrid hierarchy. Bottom-up and OLS reconciliation make forecasts coherent but do not change that ranking. The resulting contribution is a setting-specific aggregation effect, a clear separation between accuracy and coherence, and an empirical limit on additional weighting complexity. The public datasets, full configurations, per-seed results, and hierarchy construction are released to support reproduction and extension.

---

## Author Contributions

[AUTHOR INPUT REQUIRED: assign the CRediT roles to Jieyun Zheng, Linyao Zhang, Zhanghuang Zhang, Zhuolin Chen, and Ying Shi, and obtain approval from every author.] All authors have read and agreed to the published version of the manuscript.

## Funding

[AUTHOR INPUT REQUIRED: insert the verified funder, grant number, and APC funder, or state "This research received no external funding."]

## Institutional Review Board Statement

Not applicable.

## Informed Consent Statement

Not applicable.

## Data Availability Statement

All datasets used in this study are public: the Open Power System Data 60 min package (https://open-power-system-data.org) [29], SimBench load profiles (https://simbench.de) [30], and Ausgrid solar-home electricity data (https://www.ausgrid.com.au) [24]. The CSA-LoadNet implementation, configurations, 420 non-hierarchical decision-set records, 440 exact-hierarchy model--reconciliation records, effect and interval tables, paired-sensitivity results, split/source profiles, and figure scripts are included in the supplementary package and are available from the corresponding author. A persistent public archive can be supplied before publication, subject to source-data terms. Archived CSV files use the historical full-configuration label `HyG-LoadFormer (neural)`, whose one-to-one mapping to CSA-LoadNet is documented in the evidence README.

## Acknowledgments

During the preparation of this manuscript, the authors used Claude (Anthropic) for language drafting and editing and for assistance in preparing analysis and figure-generation code. All experimental designs, data processing steps, numerical results, statistical analyses, and conclusions were specified, executed, and verified by the authors. The authors reviewed and revised all assisted content and take full responsibility for the publication.

## Conflicts of Interest

The authors declare no conflicts of interest.

---

## References

<!-- MDPI numbered style, ordered by first appearance in the text.
     All DOIs verified against the Crossref API on 2026-07-16. -->

1. Li, J.; Li, J.; Li, J.; Zhang, G. Bayesian-Optimized GCN-BiLSTM-Adaboost Model for Power-Load Forecasting. *Electronics* **2025**, *14*(16), 3332. https://doi.org/10.3390/electronics14163332
2. Zhou, H.; Ai, Q.; Li, R. Short-Term Multi-Energy Load Forecasting Method Based on Transformer Spatio-Temporal Graph Neural Network. *Energies* **2025**, *18*(17), 4466. https://doi.org/10.3390/en18174466
3. Wu, M.; Feng, W.; Li, X.; Liu, Y.; Cao, C. Short-Term Power Load Forecasting Using an Improved Model Integrating GCN and Transformer. *Applied Sciences* **2025**, *15*(13), 7003. https://doi.org/10.3390/app15137003
4. Zhang, J.; Yu, B.; Lai, H.; Liu, L.; Zhou, J.; Lou, F.; Ni, Y.; Peng, Y.; Yu, Z. LoadSeer: Exploiting Tensor Graph Convolutional Network for Power Load Forecasting With Spatio-Temporal Characteristics. *IEEE Access* **2024**, *12*, 190337–190346. https://doi.org/10.1109/ACCESS.2024.3514174
5. Zeng, A.; Chen, M.; Zhang, L.; Xu, Q. Are Transformers Effective for Time Series Forecasting? *Proceedings of the AAAI Conference on Artificial Intelligence* **2023**, *37*(9), 11121–11128. https://doi.org/10.1609/aaai.v37i9.26317
6. Makridakis, S.; Spiliotis, E.; Assimakopoulos, V. Statistical and Machine Learning forecasting methods: Concerns and ways forward. *PLOS ONE* **2018**, *13*(3), e0194889. https://doi.org/10.1371/journal.pone.0194889
7. Makridakis, S.; Spiliotis, E.; Assimakopoulos, V. The M4 Competition: 100,000 time series and 61 forecasting methods. *International Journal of Forecasting* **2020**, *36*(1), 54–74. https://doi.org/10.1016/j.ijforecast.2019.04.014
8. Hewamalage, H.; Ackermann, K.; Bergmeir, C. Forecast evaluation for data scientists: common pitfalls and best practices. *Data Mining and Knowledge Discovery* **2023**, *37*(2), 788–832. https://doi.org/10.1007/s10618-022-00894-5
9. Hochreiter, S.; Schmidhuber, J. Long Short-Term Memory. *Neural Computation* **1997**, *9*(8), 1735–1780. https://doi.org/10.1162/neco.1997.9.8.1735
10. Kong, W.; Dong, Z.Y.; Jia, Y.; Hill, D.J.; Xu, Y.; Zhang, Y. Short-Term Residential Load Forecasting Based on LSTM Recurrent Neural Network. *IEEE Transactions on Smart Grid* **2019**, *10*(1), 841–851. https://doi.org/10.1109/TSG.2017.2753802
11. Salinas, D.; Flunkert, V.; Gasthaus, J.; Januschowski, T. DeepAR: Probabilistic forecasting with autoregressive recurrent networks. *International Journal of Forecasting* **2020**, *36*(3), 1181–1191. https://doi.org/10.1016/j.ijforecast.2019.07.001
12. Lara-Benítez, P.; Carranza-García, M.; Luna-Romera, J.M.; Riquelme, J.C. Temporal Convolutional Networks Applied to Energy-Related Time Series Forecasting. *Applied Sciences* **2020**, *10*(7), 2322. https://doi.org/10.3390/app10072322
13. Lim, B.; Arık, S.Ö.; Loeff, N.; Pfister, T. Temporal Fusion Transformers for interpretable multi-horizon time series forecasting. *International Journal of Forecasting* **2021**, *37*(4), 1748–1764. https://doi.org/10.1016/j.ijforecast.2021.03.012
14. Zhou, H.; Zhang, S.; Peng, J.; Zhang, S.; Li, J.; Xiong, H.; Zhang, W. Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting. *Proceedings of the AAAI Conference on Artificial Intelligence* **2021**, *35*(12), 11106–11115. https://doi.org/10.1609/aaai.v35i12.17325
15. Zhao, X.; Peng, H.; Zhang, L.; Ma, H. Research on a Short-Term Power Load Forecasting Method Based on a Three-Channel LSTM-CNN. *Electronics* **2025**, *14*(11), 2262. https://doi.org/10.3390/electronics14112262
16. Xu, J.; Zhang, L.; Zhang, Z. Research on BiLSTM–Transformer Power Load Forecasting Method Based on Dynamic Adaptive Fusion. *Energies* **2026**, *19*(6), 1473. https://doi.org/10.3390/en19061473
17. Yang, M.; Chen, Y.; Fang, G.; Ma, C.; Liu, Y.; Wang, J. A Short-Term Power Load Forecasting Method Based on SBOA–SVMD-TCN–BiLSTM. *Electronics* **2024**, *13*(17), 3441. https://doi.org/10.3390/electronics13173441
18. Dakheel, F.; Çevik, M. Optimizing Smart Grid Load Forecasting via a Hybrid Long Short-Term Memory-XGBoost Framework: Enhancing Accuracy, Robustness, and Energy Management. *Energies* **2025**, *18*(11), 2842. https://doi.org/10.3390/en18112842
19. Lai, G.; Chang, W.-C.; Yang, Y.; Liu, H. Modeling Long- and Short-Term Temporal Patterns with Deep Neural Networks. In Proceedings of the 41st International ACM SIGIR Conference on Research & Development in Information Retrieval, 2018; pp. 95–104. https://doi.org/10.1145/3209978.3210006
20. Yu, B.; Yin, H.; Zhu, Z. Spatio-Temporal Graph Convolutional Networks: A Deep Learning Framework for Traffic Forecasting. In Proceedings of the Twenty-Seventh International Joint Conference on Artificial Intelligence (IJCAI-18), 2018; pp. 3634–3640. https://doi.org/10.24963/ijcai.2018/505
21. Wu, Z.; Pan, S.; Long, G.; Jiang, J.; Chang, X.; Zhang, C. Connecting the Dots: Multivariate Time Series Forecasting with Graph Neural Networks. In Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, 2020; pp. 753–763. https://doi.org/10.1145/3394486.3403118
22. Hyndman, R.J.; Ahmed, R.A.; Athanasopoulos, G.; Shang, H.L. Optimal combination forecasts for hierarchical time series. *Computational Statistics & Data Analysis* **2011**, *55*(9), 2579–2589. https://doi.org/10.1016/j.csda.2011.03.006
23. Wickramasuriya, S.L.; Athanasopoulos, G.; Hyndman, R.J. Optimal Forecast Reconciliation for Hierarchical and Grouped Time Series Through Trace Minimization. *Journal of the American Statistical Association* **2019**, *114*(526), 804–819. https://doi.org/10.1080/01621459.2018.1448825
24. Ratnam, E.L.; Weller, S.R.; Kellett, C.M.; Murray, A.T. Residential load and rooftop PV generation: an Australian distribution network dataset. *International Journal of Sustainable Energy* **2017**, *36*(8), 787–806. https://doi.org/10.1080/14786451.2015.1100196
25. Tashman, L.J. Out-of-sample tests of forecasting accuracy: an analysis and review. *International Journal of Forecasting* **2000**, *16*(4), 437–450. https://doi.org/10.1016/S0169-2070(00)00065-0
26. Bergmeir, C.; Benítez, J.M. On the use of cross-validation for time series predictor evaluation. *Information Sciences* **2012**, *191*, 192–213. https://doi.org/10.1016/j.ins.2011.12.028
27. Hyndman, R.J.; Koehler, A.B. Another look at measures of forecast accuracy. *International Journal of Forecasting* **2006**, *22*(4), 679–688. https://doi.org/10.1016/j.ijforecast.2006.03.001
28. Diebold, F.X.; Mariano, R.S. Comparing Predictive Accuracy. *Journal of Business & Economic Statistics* **1995**, *13*(3), 253–263. https://doi.org/10.1080/07350015.1995.10524599
29. Wiese, F.; Schlecht, I.; Bunke, W.-D.; Gerbaulet, C.; Hirth, L.; Jahn, M.; Kunz, F.; Lorenz, C.; Mühlenpfordt, J.; Reimann, J.; Schill, W.-P. Open Power System Data — Frictionless data for electricity system modelling. *Applied Energy* **2019**, *236*, 401–409. https://doi.org/10.1016/j.apenergy.2018.11.097
30. Meinecke, S.; Sarajlić, D.; Drauz, S.R.; Klettke, A.; Lauven, L.-P.; Rehtanz, C.; Moser, A.; Braun, M. SimBench—A Benchmark Dataset of Electric Power Systems to Compare Innovative Solutions Based on Power Flow Analysis. *Energies* **2020**, *13*(12), 3290. https://doi.org/10.3390/en13123290
