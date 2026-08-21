# Constraints — Boundary Conditions, Assumptions, Limitations

## Boundary conditions (model scope)
- Test network: IEEE 39-bus system, 10 thermal units, wind (DFIG) at buses 17 and 21, five regional
  temperature zones; bus 31 slack. Results are specific to this topology and the southwest-China
  typical-day forecasts.
- Horizon: one day, 24 hourly time steps.
- Power flow: DC approximation via GSDF (Eq. 28) — lossless, linearized; no AC voltage/reactive
  modeling.
- DLR validity: steady-state conductor temperature governs (long time scale); wind speed v and solar
  irradiance G assumed constant over each period (Eq. 9 assumption).
- Transformer cooling: OA/ONAN mode fixes FT = 1.4, n = 0.9, m = 0.8, θQC = 22 C, ∆θTM-R = 56.3 C at
  20 C reference ambient; aging follows the IEC 98 C / +6 C-doubling rule with 30-year nominal life.

## Assumptions
- A1: Meteorological inputs (temperature, wind, solar) and load/wind forecasts are known day-ahead
  and are deterministic within each period.
- A2: Transformer thermal aging obeys Arrhenius kinetics and linear (Miner's-rule) damage
  accumulation (Eqs. 20-21).
- A3: Transformer loading is the dominant driver of hot-spot temperature (adopted premise, ref [14]).
- A4: Empirical loss/temperature-rise constants (ES ∈ [1.3,1.5]; 0.8/3.5/0.7 regression constants;
  Ka ∈ [0.05,0.15]; Kh ∈ [0.5,0.9]) are taken from cited sources, not re-derived.
- A5: Spinning-reserve margin factor α = 0.02 (per GB/T 38969-2020).

## Known limitations (stated or implied by the paper)
- Single test system and a single typical day; generalization to other networks/climates is argued
  only via the λ-scaling sensitivity (Table 4), not via multiple real systems.
- Deterministic forecasts: wind/temperature/load uncertainty is represented only through the wind
  decomposition (curtailment) variable, not through stochastic/robust optimization.
- DC power flow ignores losses and voltage/reactive constraints; interface security is checked only
  via section flow limits.
- Prior dynamic-rating transformer models are noted to become invalid under abnormal high temperature
  (parameter drift); this paper fixes OA/ONAN parameters and does not model such drift explicitly.
- Data-consistency caveat: Table 4 at λ = 1.2 reports a TL-TF life-loss cost (0.680) that is
  inconsistent with its own 76.1% cost-reduction column (which implies ≈0.068); treated as a likely
  transcription/typo in the source (see evidence/tables/table4.md).
- Nomenclature/typographic ambiguities in the transcribed equations (e.g., Eq. 5-7 exponent
  formatting) are carried as-printed; where the paper is silent on a value it is marked "Not
  specified in paper".
