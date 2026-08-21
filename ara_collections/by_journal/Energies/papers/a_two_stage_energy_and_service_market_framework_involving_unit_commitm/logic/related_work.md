# Related Work

## Market Coordination and Multi-Stage Models

### RW01: Dominguez et al., 2019 (Ref. [6])
- **DOI**: 10.1016/j.ijepes.2019.05.064
- **Type**: baseline
- **Delta**: Three market configurations for reserve procurement in renewable-dominated systems: DAM-only, ASM-only, joined co-optimized; compared market designs but without bid adjustment mechanism.
- **Claims affected**: C01
- **Adopted elements**: Framework for market design comparison; RES-dominated system context.

### RW02: Goudarzi et al., 2021 (Ref. [23])
- **DOI**: 10.1016/j.ijepes.2021.106817
- **Type**: extends
- **Delta**: Two-stage day-ahead clearing for energy and RT markets in American framework with fast-start generators as non-spinning reserve.
- **Claims affected**: C01
- **Adopted elements**: Two-stage sequential market model; fast-start generator behavior.

### RW03: Garcia-Gonzalez et al., 2007 (Ref. [19])
- **DOI**: 10.1109/TPWRS.2007.907584
- **Type**: extends
- **Delta**: Three optimization problems modeling consecutive intraday, reserve, and real-time markets; unit-state constraints from already-committed units.
- **Claims affected**: C01, C02
- **Adopted elements**: Sequential market optimization; unit-state constraints; fixed-commitment limitation.

### RW04: Nycander et al., 2022 (Ref. [22])
- **DOI**: 10.1109/TSTE.2022.3160842
- **Type**: bounds
- **Delta**: Capacity and intra-hour ramp reserves for wind integration; treats unit status as fixed by DAM.
- **Claims affected**: C02
- **Adopted elements**: Demonstrates limitation of fixed-commitment redispatch that motivates the work.

## Redispatch and Congestion Management

### RW05: Pitto et al., 2020 (Ref. [10])
- **DOI**: 10.23919/AEIT50178.2020.9241188
- **Type**: bounds
- **Delta**: Probabilistic security-constrained preventive redispatch with correlated uncertainties.
- **Claims affected**: C06
- **Adopted elements**: Redispatch optimization with uncertainty.

### RW06: Klabunde & Wolter, 2020 (Ref. [14])
- **DOI**: 10.1109/ISGT-Europe47291.2020.9248954
- **Type**: baseline
- **Delta**: MILP time-series redispatch optimization; uses integer variables for unit start-up/shut-down.
- **Claims affected**: C01
- **Adopted elements**: MILP formulation for redispatch; start-up/shut-down modeling.

## SCUC and ED Foundations

### RW07: Conejo & Baringo, 2017 (Ref. [32])
- **DOI**: — (Book chapter)
- **Type**: baseline
- **Delta**: Standard UC and ED formulation used as benchmark reference.
- **Claims affected**: C03
- **Adopted elements**: UC formulation with reserve constraints for benchmark model (Appendix A).

### RW08: Morales-Espana & Tejada-Arango, 2019 (Ref. [33])
- **DOI**: 10.1109/TPWRS.2019.2896905
- **Type**: baseline
- **Delta**: Modeling of hidden flexibility in clustered unit commitment; MUT/MDT formulation.
- **Claims affected**: C03
- **Adopted elements**: MUT/MDT constraint formulation for benchmark model.

## Test System References

### RW09: Pena et al., 2017 (Ref. [31])
- **DOI**: 10.1109/TPWRS.2017.2695963
- **Type**: baseline
- **Delta**: Extended IEEE 118-Bus test system with high renewable penetration datasets (load, wind, solar, costs, availabilities, hydro data).
- **Claims affected**: C01
- **Adopted elements**: Full NREL-118 dataset for case study.

### RW10: Tricarico et al., 2022 (Ref. [35])
- **DOI**: 10.1109/ISGTAsia54193.2022.10003588
- **Type**: baseline
- **Delta**: Zonal day-ahead energy market model on modified IEEE 39-bus; basis for the DAM formulation.
- **Claims affected**: C01
- **Adopted elements**: DAM zonal market LP formulation (Eqs. 2–9).

## Technical References

### RW11: GME (Italian Market Operator)
- **DOI**: — (Online data source)
- **Type**: baseline
- **Delta**: Public market data on DAM/ASM bids; source for time-varying bid factors.
- **Claims affected**: C02
- **Adopted elements**: Hourly ASM/DAM bid price ratios for bid factor construction.

### RW12: Ronellenfitsch et al., 2017 (Ref. [37])
- **DOI**: 10.1109/TPWRS.2016.2589464
- **Type**: baseline
- **Delta**: Dual method for computing PTDFs.
- **Claims affected**: C01
- **Adopted elements**: PTDF computation method for redispatch modeling.

### RW13: Tricarico et al., 2022 (Ref. [44])
- **DOI**: 10.1109/EEM54602.2022.9921066
- **Type**: baseline
- **Delta**: Tertiary reserve requirement determination method.
- **Claims affected**: C05
- **Adopted elements**: SRR calculation formula.

## Review and Context

### RW14: Yang et al., 2022 (Ref. [8])
- **DOI**: 10.35833/MPCE.2021.000255
- **Type**: baseline
- **Delta**: Comprehensive review of SCUC from deterministic to stochastic/robust.
- **Claims affected**: C01
- **Adopted elements**: SCUC evolution context.

### RW15: IEEE PES, 2022 (Ref. [20])
- **DOI**: 10.17023/1j99-wn34
- **Type**: baseline
- **Delta**: Technical report on SCUC for electricity markets.
- **Claims affected**: C01
- **Adopted elements**: MILP SCUC reference.

### RW16: Charbonnier et al., 2022 (Ref. [27])
- **DOI**: 10.1016/j.apenergy.2022.119188
- **Type**: baseline
- **Delta**: Systematic review of resource coordination at grid edge.
- **Claims affected**: C01
- **Adopted elements**: Market coordination taxonomy.

### RW17: Rancilio et al., 2022 (Ref. [28])
- **DOI**: 10.1016/j.rser.2021.111850
- **Type**: baseline
- **Delta**: Meta-analysis of ASM evolution and regulatory trade-offs.
- **Claims affected**: C02
- **Adopted elements**: ASM context and service classification.
