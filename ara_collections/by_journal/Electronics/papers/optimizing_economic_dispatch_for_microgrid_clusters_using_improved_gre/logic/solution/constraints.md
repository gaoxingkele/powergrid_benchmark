# Constraints, Assumptions, and Limitations

## Boundary conditions (model constraints, §2.2)
- **Power balance** (Eq. 1): Σ_i P_gen,i(t) + P_import(t) = P_load(t) at every interval t.
- **Per-MG load composition** (Eq. 2): P_loadi = P_WTi + P_PVi + P_MTi + P_ESSi + P_buyi − P_selli
  + inter-MG exchange terms (symbols in Table 1).
- **MT/DG output limits** (Eq. 3): P_min ≤ P_MT/DG(t) ≤ P_max.
- **MT/DG ramp limits** (Eq. 4): P(t) − P(t−1) ≤ r_MT / r_DG.
- **ESS charge/discharge power** (Eq. 5): 0 ≤ P_ch(t) ≤ P_ch,max ; 0 ≤ P_dis(t) ≤ P_dis,max.
- **ESS capacity** (Eq. 6): E_min ≤ E(t) ≤ E_max.
- **ESS SOC** (Eq. 7): SOC_min ≤ SOC(t) ≤ SOC_max; **set to [30%, 90%] in this study**.

## Assumptions
- A1: MGC = exactly 3 microgrids; MG1/MG3 use DGs, MG2 uses an MT; central EMC coordination.
- A2: Daily horizon, 1-hour resolution, 24 intervals.
- A3: WT and PV are emission-free; ESS pollutants are neglected in the pollution-control cost.
- A4: Forecast wind/solar/load for a typical day (from ECMWF meteorology + local historical data) are
  the nominal deterministic inputs.
- A5: Operational revenue uses TOU pricing; inter-MG trading price is flat across the day.
- A6: ESS modelled as supercapacitor storage with a SOC-dependent loss function f(SOC).
- A7: Robustness assessed with a single ±10% random disturbance on MG1 wind, MG2 PV, MG3 load.

## Known limitations
- **Single test instance / single day**: results come from one MGC configuration on one typical day;
  no cross-day, cross-season, or cross-topology validation.
- **Unspecified parameters**: penalty coefficients δ, γ; emission coefficients λ_i; unit pollution
  costs c_DG/c_MT; m_ESS; ramp and capacity bounds are not given numerically — only SOC ∈ [30%,90%].
  This limits exact reproduction.
- **No penalty-coefficient sensitivity study**: the weighting between cost and penalty terms is fixed
  and its effect on solution quality is not analysed.
- **Chaos-vs-DOBL contributions not fully ablated**: chaos-only is tested (Table 4), but DOBL-only is
  not; the two enhancements' separate late-stage contributions are argued, not independently measured.
- **Disturbance model is narrow**: only bounded (±10%) independent random disturbance on three
  quantities; correlated, larger, or adversarial uncertainty is untested.
- **Scale**: authors note applicability to "larger and more complex microgrid systems" as future work
  — the demonstrated cluster is small (3 MGs).
- **Reproducibility of the solver**: no code or run logs are released (Data Availability: "included in
  the article; further inquiries to the corresponding author").
