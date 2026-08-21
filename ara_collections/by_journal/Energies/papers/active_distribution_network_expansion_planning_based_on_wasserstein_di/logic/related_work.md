# Related Work

Typed dependency graph. Full `RW` blocks for works with a specific technical delta to this paper;
briefer entries preserve the paper's full citation footprint.

## RW01: SOP planning for distribution networks — [5][6][7][8]
- **Type**: extends
- **Delta**:
  - What changed: Prior work [5–8] studies SOP-only expansion planning (siting and sizing) under deterministic or stochastic DG/load scenarios. This paper extends to collaborative planning with lines and interconnection switches under distributional ambiguity.
  - Why: Earlier SOP planning models ignore the option of using cheaper mechanical switches at tie positions, potentially over-investing in power-electronic devices.
- **Claims affected**: C01
- **Adopted elements**: SOP mathematical model (converter loss characteristics, power flow capability); SOP planning formulation framework.

## RW02: Interconnection switch / tie switch planning — [9][10][11][12]
- **Type**: baseline
- **Delta**:
  - What changed: [9–12] study optimal placement and operation of interconnection switches or tie switches for network reconfiguration. This paper treats switches as a binary interconnection option alongside SOPs rather than as reconfiguration-only devices.
  - Why: Prior switch planning does not compare against or combine with power-electronic alternatives.
- **Claims affected**: C01
- **Adopted elements**: Switch operational model (binary on/off state); capital cost parameter ranges.

## RW03: Distribution network expansion planning with lines — [15][16][17][18][19][20]
- **Type**: extends
- **Delta**:
  - What changed: [15–20] study line/feeder expansion planning with various DG integration strategies but without considering SOP or interconnection switch options for flexible interconnection. This paper adds device-type selection to line expansion.
  - Why: Siloed line-only expansion may over-invest in new feeders where existing feeders could be coupled at lower cost.
- **Claims affected**: C01
- **Adopted elements**: Line investment cost model; annualized cost calculation framework.

## RW04: Robust optimization for ADN — [22][23][24][25]
- **Type**: baseline
- **Delta**:
  - What changed: [22–25] apply traditional robust optimization (box/polyhedral uncertainty sets) to ADN problems. This paper uses Wasserstein-distance DRO instead, which is less conservative (the inner problem hedges against distributional ambiguity rather than the worst-case scenario).
  - Why: Traditional robust optimization is "too conservative" (Table 6 net profit: robust 4770 vs DRO 4928).
- **Claims affected**: C02
- **Adopted elements**: Robust optimization formulation language (min-max); conservativeness-vs-performance trade-off framing.

## RW05: Wasserstein distance DRO in power systems — [26][27][28][29]
- **Type**: extends
- **Delta**:
  - What changed: [26–29] apply Wasserstein DRO to power system operations (e.g., unit commitment, economic dispatch). This paper applies it to expansion planning (investment decisions with SOP/switch selection), a longer-horizon problem.
  - Why: Extends the Wasserstein DRO tool from operational to planning timescales.
- **Claims affected**: C02
- **Adopted elements**: Wasserstein ambiguity set formulation; dual reformulation of the inner worst-case expectation.

## RW06: SOCP relaxation for distribution network optimization — [19][20][21]
- **Type**: imports
- **Delta**:
  - What changed: [19–21] establish the exactness of SOCP relaxation for radial distribution networks with OPF. This paper uses the same relaxation for the ADN expansion planning context.
  - Why: Core mathematical dependency enabling the MISOCP reformulation.
- **Claims affected**: C05
- **Adopted elements**: SOCP relaxation of DistFlow equations; exactness conditions.

## RW07: Bilinear term relaxation methods — [30]
- **Type**: baseline
- **Delta**:
  - What changed: [30] proposes a "bilinear-removed" method for eliminating bilinear terms. This paper compares against it (Table 7) and shows that McCormick relaxation achieves 24% better solution quality.
  - Why: Used as a performance baseline for the proposed McCormick approach.
- **Claims affected**: C03, C05
- **Adopted elements**: Used as a comparison method in Section 5.6.

## RW08: Portugal 54-node test system — [31]
- **Type**: imports
- **Delta**:
  - What changed: [31] (Miranda, Ranito, Proenca, IEEE Trans. Power Syst. 1994) defines the Portugal 54-node distribution system used as the test network in this paper.
  - Why: Source of all topological, line, and substation parameters.
- **Claims affected**: C01, C02, C03
- **Adopted elements**: Full test system.

## Additional citations (brief footprint)
- [1] Bilil, B.; Assali, R.; Amamra, S.A. — Review of active distribution network planning (2021) — background.
- [2] DG integration impact survey (2017) — background.
- [3] Wang et al. — SOP development and VSC control (2015) — SOP technology background.
- [4] Cao et al. — SOP operation optimization in ADN (2016) — SOP modeling.
- [13] Optimal feeder configuration (2011) — background.
- [14] Switch operation cost survey — background.
- [32] H. Wu et al. — DRO for economic dispatch with wind (2017) — Wasserstein DRO background.
- [33] P. M. Castro — MISOCP for process networks (2015) — McCormick relaxation reference.
- [34] CPLEX solver reference — solution engine.
