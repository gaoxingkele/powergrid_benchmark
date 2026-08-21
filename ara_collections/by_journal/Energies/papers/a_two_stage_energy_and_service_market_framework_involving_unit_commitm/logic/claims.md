# Claims

## C01: Sequential zonal-DAM-then-nodal-ASM with bid adjustment resolves network, forecast, and UC constraints
- **Statement**: A sequential market framework in which the zonal DAM clears without UC constraints (merit-order only) and the subsequent nodal ASM re-evaluates unit commitment through a bid adjustment mechanism can simultaneously resolve DAM-induced branch overloads, RES/load forecast deviations, and secondary reserve requirements, while keeping unit commitment (MUT/MDT) feasible and continuous across days.
- **Conditions**: Holds for European-style market structures with zonal DAM and nodal ASM with pay-as-bid settlement; demonstrated on the NREL-118 system with 89 DT units and 15 DH units over a full leap year. The bid adjustment mechanism assumes ASM bids are derived from DAM schedules through the five operational cases of Figure 3.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Show that for any day of the year the NCUCER ASM optimization yields an infeasible solution (unresolved overload, unmet SRR, or MUT/MDT violation), or that the total yearly TSO disbursement exceeds the benchmark's by a factor less than 5.
- **Proof**: [E01, E02, E03]
- **Evidence basis**: §2 methodology (Figures 2–3, Section 2.3); §4.2 shows all branch overloads resolved, SRR always met, zero RES curtailment/load shedding, feasible unit states across 366 days.
- **Tags**: sequential market, DAM, ASM, NCUCER, feasibility

## C02: The bid adjustment process correctly enforces DT unit technical limits through case-dependent ordering
- **Statement**: The five-case bid adjustment logic (Figure 3) — encoding whether a DT unit's DAM schedule is below technical minimum, at minimum, between limits, at rated power, or zero — correctly maps DAM outcomes to ASM-compatible bids by forcing mandatory SU or SD bids when the unit is dispatched below its technical minimum and preventing simultaneous SU and SD or SR bids that violate the unit's physical state.
- **Conditions**: Verified for the five operational cases defined by the DAM schedule P^D_i,t relative to P^min_i,t and zero; the constraints (30)–(34) enforce the case-dependent logic. SU/SD costs are based on DAM bid prices with time-varying factors.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Show a DT unit ASM state that violates any of: (a) SU bid cleared when P^D >= P^min, (b) SD bid cleared when P^D = 0, (c) both SU and SD cleared simultaneously for a unit below P^min, or (d) SR bids accepted for a unit that is not online.
- **Proof**: [E02, E03]
- **Evidence basis**: §2.2, Figure 3 (five cases); constraints (17)–(34) enforcing the logic; §4.2 Table 5 reporting yearly SU/SD occurrences per technology.
- **Tags**: bid adjustment, DT unit, technical minimum, SU/SD, operational case

## C03: The sequential approach is substantially cheaper than co-optimized DAM-with-UC benchmark
- **Statement**: The proposed sequential DAM-ASM approach yields total yearly energy plus service costs 5.6 times lower than a benchmark DAM model with UC and reserve constraints ([32,33]), because the sequential framework allows the DAM to clear at marginal cost without reserve obligations, while the benchmark must keep expensive units online just to satisfy SR provision, inflating zonal prices by factors of 2–6.
- **Conditions**: Based on comparison with the benchmark model detailed in Appendix A; both models use the same NREL-118 system, generation mix, and yearly horizon. The benchmark DAM includes MUT/MDT and SR constraints, yielding zonal prices of $45–242/MWh vs $27–55/MWh in the proposed DAM.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Show a scenario on the same test system where the proposed approach yields total costs within a factor of 3 of the benchmark, or where the benchmark yields lower total costs (including the cost of unresolved network overloads).
- **Proof**: [E06]
- **Evidence basis**: §4.5, Table 8 (benchmark prices), Figure 17 (dispatched energy variation), Figure 18 (service cost variation): proposed $3.49B vs benchmark $19.50B.
- **Tags**: cost comparison, benchmark, co-optimization, zonal prices

## C04: CC NG is the primary ASM service provider; ST NG provides mainly SU/SD due to cost structure
- **Statement**: Among DT technologies in the ASM, CC NG units provide the majority of UR, DR, SU, and SR services thanks to their economic viability and flexibility; CT NG units are marginally cleared, mainly providing SRU; ST NG units are mostly cleared for SU and SD due to higher costs and large MUT/MDT values that make sustained operation uneconomic.
- **Conditions**: Based on yearly ASM results on the NREL-118 system with 28 CC NG, 52 CT NG/Oil, 8 ST NG, and 1 Geo units. The cost structure and MUT/MDT parameters are given in Table 1.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Show an alternative technology providing a larger share of ASM services than CC NG in UR, or ST NG providing more UR than SU/SD, using the same NREL-118 data.
- **Proof**: [E03, E04]
- **Evidence basis**: §4.2, Figure 9 (services per technology), Table 5 (SU/SD occurrences): CC NG: 28,206 SU, 1718 SD; CT NG: 6176 SU, 1200 SD; ST NG: 1448 SU, 962 SD.
- **Tags**: technology contribution, CC NG, ST NG, ancillary services, economic dispatch

## C05: USM is the binding constraint for SR provision, requiring SU or DR clearance for 741 hours yearly
- **Statement**: While DSM is sufficient to cover SRR year-round, USM is insufficient for 741 time steps per year, requiring the ASM to clear SU or DR bids to create additional upward margin. This confirms that asymmetric SR provision (upward margin harder to satisfy) is a structural constraint of the generation mix.
- **Conditions**: USM/DSM computed as sum of SRH-limited upward/downward margin of cleared DT units after DAM. SRR ranges from 94.4 MW to 302.5 MW per [44].
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Show that for all 741 USM-deficient hours, an alternative re-dispatch exists that does not require SU or DR while still meeting SRR, or that the USM deficiency can be resolved by DH units.
- **Proof**: [E03]
- **Evidence basis**: §4.1, Figure 10 (SRR and USM/DSM difference): "DSM is sufficient to cover the SRR, whereas for 741 time steps the USM is lower than the SRR."
- **Tags**: secondary reserve, USM, DSM, SRR, asymmetry

## C06: UR service is price-inelastic (driven by overload mitigation); other services respond to price
- **Statement**: UR cleared amount is almost unaffected by price variation in the sensitivity analysis (±0.5–0.6% change for ±10% price factor variation), indicating UR is mainly cleared to mitigate line overloads rather than for economic optimization. In contrast, DR, SU, SD, and SR services show elastic responses: DR quantity changes by +10.5%/−8.5%, SU by +13.7%/−10.9% under narrower/larger prices.
- **Conditions**: Sensitivity analysis varies time-varying bid factors: narrower prices (selling +10%, buying −10%) and larger prices (selling −10%, buying +10%) relative to base case. SRU/SRD quantities fixed at SRR (unaffected by price).
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Show UR cleared amount varying by more than 2% under the same price factor variations, or show that removing overload constraints eliminates the price-inelasticity of UR.
- **Proof**: [E05]
- **Evidence basis**: §4.4, Table 6: UR base 2.315 TWh vs narrower 2.301 TWh (−0.6%) vs larger 2.304 TWh (−0.5%), while DR varies +10.5%/−8.5%.
- **Tags**: price elasticity, UR, sensitivity analysis, overload mitigation

## C07: DH bidding strategy significantly impacts ASM outcomes
- **Statement**: Changing the DH bidding strategy from 90% to 85% DAM allocation reduces DH DAM production by ~0.94 TWh/year, increases CC NG generation by ~72.7% of that reduction, raises zonal prices by ~1%, increases overload occurrences from 4517 to 4537, and increases TSO expense by ~$1.72M/year, mainly from more expensive UR provision. SU energy decreases as more units are already committed in DAM.
- **Conditions**: Tested as a sensitivity on the base case with 15 DH units; only the DAM allocation percentage changes, keeping all other parameters fixed.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Show that for any alternate DH allocation percentage between 80% and 95%, the resulting TSO expense change is less than $0.5M, or that the overload occurrence count decreases with lower DH DAM allocation.
- **Proof**: [E05]
- **Evidence basis**: §4.4, Table 7 (zonal prices for 85% allocation), Figure 15 (energy and cost variation), Figure 16 (service provision variation).
- **Tags**: DH bidding strategy, sensitivity, zonal prices, overloads
