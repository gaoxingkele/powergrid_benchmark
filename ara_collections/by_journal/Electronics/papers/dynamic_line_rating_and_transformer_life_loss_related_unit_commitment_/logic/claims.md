# Claims

## C01: A thermal-balance dynamic rating recovers transfer capability that worst-case static rating discards under heat
- **Statement**: Because conductor ampacity is set by the current at which resistive heating
  balances convective and radiative cooling minus solar gain, and that balance degrades as ambient
  temperature rises, computing the rating from real-time thermal balance (rather than from a fixed
  worst-case assumption) exposes transfer capability that static rating conservatively hides —
  so replacing SLR with a temperature-dependent DLR limit raises usable line utilization in hot
  regions without violating the conductor's permissible temperature.
- **Conditions**: Holds for the modeled overhead conductors under an extreme high-temperature
  typical day on the IEEE 39-bus system, with wind speed and solar irradiance treated as constant
  over each period and the steady-state (long-time-scale) temperature governing (Eq. 9). Untested:
  transient/gust-dominated ratings, forecast error in the meteorological inputs, and conductors
  whose thermal-stability parameters drift outside the fitted regime.
- **Sources**: ["12% ← Abstract «improves transmission capacity utilization in high-temperature conditions by 12%» [result]", "12% ← §6 conclusion 1 «a 12% improvement in transmission capacity utilization in high-temperature regions compared to conventional static line rating methods» [result]"]
- **Status**: supported
- **Falsification criteria**: If, under the same weather inputs, the DLR-derived ampacity from
  Eq. 10 were equal to or below the SLR limit (i.e., real-time thermal balance yielded no extra
  capacity), or if operating a line at the DLR limit drove conductor temperature above θmax, the
  mechanism would be refuted.
- **Proof**: [E01]
- **Evidence basis**: The DLR formulation (Eqs. 1-10) and the reported 12% utilization improvement
  in high-temperature regions; see evidence/figures/figure5.md (interface flows stay within limits).
  Numbers are recorded in evidence, not restated here.
- **Tags**: dynamic-line-rating, ampacity, thermal-balance, transmission

## C02: Pricing thermal aging into dispatch caps hot-spot temperature near its rated bound by steering load off hot transformers
- **Statement**: Since transformer insulation aging rises Arrhenius-fast with hot-spot temperature,
  and hot-spot temperature is driven jointly by ambient temperature and load ratio, attaching a
  monetary life-loss cost to loading makes the optimizer shift load away from transformers in hot
  regions, holding hot-spot temperature near the rated (98 C) bound instead of letting it run away
  — converting an otherwise-ignored degradation into a controllable dispatch outcome.
- **Conditions**: Holds for an OA/ONAN oil-immersed transformer (FT = 1.4, n = 0.9, m = 0.8,
  θQC = 22 C, rated top-oil rise 56.3 C at 20 C ambient) under the extreme high-temperature typical
  day; aging follows Arrhenius kinetics with the IEC 98 C / +6 C-doubling rule and 30-year nominal
  life. Untested: multi-day cumulative aging, non-OA/ONAN cooling, and parameter drift under
  abnormal heat noted as a failure mode of prior dynamic-rating models.
- **Sources**: ["69% ← Abstract «reduces transformer life loss costs by 69%» [result]", "98 ← §3.2 «a continuous maximum hot-spot temperature of 98 °C ensures the rated lifetime of a transformer, whereas each additional 6 °C above this threshold doubles the aging rate» [input]", "0.04 ← Table 2 «TL-TF model 7.01 0.5 0.21 0.04 7.76» [result]", "0.13 ← Table 2 «Con- Model 7.12 0.67 0.24 0.13 8.16» [result]"]
- **Status**: supported
- **Falsification criteria**: If the aging-aware model's transformer hot-spot profile exceeded the
  conventional model's under the same ambient trajectory, or if adding the life-loss cost term did
  not lower transformer loss cost relative to the conventional model, the mechanism would be refuted.
- **Proof**: [E02]
- **Evidence basis**: Figure 6 shows the conventional model's hot-spot temperature exceeding 98 C
  and rising with ambient temperature while the TL-TF profile stays near 98 C; Table 2 records the
  transformer-loss-cost reduction (0.13 → 0.04, ×10^4 CNY ≈ 69%). See evidence/figures/figure6.md,
  evidence/tables/table2.md.
- **Dependencies**: C01
- **Tags**: transformer-life-loss, hot-spot-temperature, Arrhenius, dispatch

## C03: Co-optimizing DLR and transformer life loss redistributes generation from hot bottlenecked regions and improves total operating economy
- **Statement**: Embedding both the temperature-dependent line limit and the transformer life-loss
  cost in one UC objective couples ambient temperature to power-flow paths and to asset
  degradation, so the optimum moves generation from hot, transmission-constrained regions to cooler
  or spare-capacity units; because this simultaneously relieves curtailment and avoids expensive
  aging, the combined objective lowers total operating cost rather than trading security against
  economy.
- **Conditions**: Holds on the IEEE 39-bus system (10 thermal units, wind at buses 17 and 21) for
  the extreme high-temperature typical day with wind-curtailment penalty 500 CNY/(MW·h) and DC power
  flow via GSDF. Untested: AC power flow, networks with different regional temperature spreads, and
  penalty/investment settings far from the base case.
- **Sources**: ["4.9% ← Abstract «lowers total operating costs by 4.9%» [result]", "12.5% ← §6 conclusion 3 «this approach reduces wind curtailment by 12.5% and decreases total operating costs by 4.9%» [result]", "7.76 ← Table 2 «TL-TF model 7.01 0.5 0.21 0.04 7.76» [result]", "8.16 ← Table 2 «Con- Model 7.12 0.67 0.24 0.13 8.16» [result]", "14.21 ← §5 «the proposed model reduces wind power curtailment by 14.21 MW» [result]"]
- **Status**: supported
- **Falsification criteria**: If the TL-TF model's total operating cost were higher than the
  conventional model's on the same scenario, or if its dispatch did not reduce output of the
  hot-region economic unit (Unit 2) relative to the conventional dispatch, the mechanism would be
  refuted.
- **Proof**: [E03]
- **Evidence basis**: Figure 4a vs 4b shows the dispatch reallocation (Unit 2 output suppressed in
  the temperature-aware case); Table 2 records total cost 8.16 → 7.76 (×10^4 CNY, ≈4.9%) and wind
  curtailment reduced by 14.21 MW. See evidence/figures/figure4.md, evidence/tables/table2.md.
- **Dependencies**: C01, C02
- **Tags**: unit-commitment, co-optimization, wind-curtailment, economic-dispatch

## C04: Transformer life-loss cost is strongly temperature-sensitive, and the aging-aware model's relative benefit widens with hotter conditions
- **Statement**: Because insulation aging is Arrhenius-exponential in hot-spot temperature, life-loss
  cost climbs steeply as the ambient temperature scaling factor increases in both conventional and
  aging-aware dispatch; but because the aging-aware model can re-route generation, power flow, and
  transformer loading to shed the hottest loading, the fraction of life-loss cost it avoids grows as
  conditions get hotter — i.e., the value of aging-aware scheduling increases precisely when heat
  stress is most severe.
- **Conditions**: Holds across temperature scaling factors λ ∈ {0.9, 1.0, 1.1, 1.2} applied to all
  regional 24 h temperature curves with all other parameters fixed. Untested: λ beyond 1.2,
  compounding multi-day exposure, and whether the reported λ = 1.2 TL-TF value is consistent (see
  evidence/tables/table4.md note on an apparent transcription anomaly).
- **Sources**: ["63.4% ← Table 4 «0.9 0.082 0.030 63.4%» [result]", "69.2% ← Table 4 «1.0 0.130 0.040 69.2%» [result]", "73.0% ← Table 4 «1.1 0.189 0.051 73.0%» [result]", "76.1% ← Table 4 «1.2 0.285 0.680 76.1%» [result]"]
- **Status**: supported
- **Falsification criteria**: If life-loss cost did not rise monotonically with λ, or if the
  cost-reduction ratio of the aging-aware model did not increase with λ, the claimed
  temperature-sensitivity/widening-benefit relationship would be refuted.
- **Proof**: [E04]
- **Evidence basis**: Table 4 reports life-loss cost rising with λ in both models and cost-reduction
  ratio increasing from 63.4% (λ=0.9) to 76.1% (λ=1.2). See evidence/tables/table4.md.
- **Dependencies**: C02
- **Tags**: sensitivity-analysis, temperature-scaling, robustness, transformer-aging

## C05: The wind-curtailment penalty coefficient drives a U-shaped total-cost response across curtailment-tolerant and full-absorption regimes
- **Statement**: As the wind-curtailment penalty rises, the system passes through three regimes —
  a low-penalty regime where curtailment is economically tolerated and thermal units stay at stable
  efficient set-points, a cost-balancing regime where committing flexible units and peak-shaving
  absorbs more wind, and a high-penalty regime where near-complete wind absorption forces costly
  thermal cycling — so total operating cost first falls then rises, tracing a U-shape rather than
  decreasing monotonically with stricter penalties.
- **Conditions**: Holds for penalty coefficients {100, 300, 500, 1000} CNY/(MW·h) at fixed
  transformer investment cost on the studied system; the minimum lies near the mid-range penalty.
  Untested: finer penalty grids, interaction with very high/low transformer investment cost, and
  other load/wind profiles.
- **Sources**: ["7.93 ← Table 3 «100 230 7.15 0.30 0.45 0.03 7.93» [result]", "7.76 ← Table 3 «500 230 7.01 0.50 0.21 0.04 7.76» [result]", "7.87 ← Table 3 «1000 230 6.97 0.72 0.13 0.05 7.87» [result]"]
- **Status**: supported
- **Falsification criteria**: If total cost decreased monotonically (or increased monotonically)
  with the penalty coefficient rather than reaching an interior minimum, the U-shaped-regime
  mechanism would be refuted.
- **Proof**: [E05]
- **Evidence basis**: Table 3 total cost across penalties: 7.93 (100) → 7.78 (300) → 7.76 (500) →
  7.87 (1000) (×10^4 CNY), an interior minimum near 500. See evidence/tables/table3.md.
- **Tags**: wind-curtailment, penalty-sensitivity, U-shape, dispatch-economics
