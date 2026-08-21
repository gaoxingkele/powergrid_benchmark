# Related Work (typed dependency graph)

## RW01: Dehghani et al., 2023 — Coati Optimization Algorithm (COA)
- **DOI**: 10.1016/j.knosys.2022.110011 (Knowl.-Based Syst., vol. 259) [32]
- **Type**: extends
- **Delta**:
  - What changed: This paper takes COA as the base optimizer and enhances it with FDB selection and OBL seeding.
  - Why: COA is accurate but unstable/poorly scalable; needs diversity/selection guidance.
- **Claims affected**: C01, C02, C04, C07
- **Adopted elements**: full two-stage (hunting/escaping) update structure, Eqs. 16–23.

## RW02: Kahraman et al., 2020 — Fitness-Distance Balance (FDB)
- **DOI**: 10.1016/j.knosys.2020.105169 (Knowl.-Based Syst., vol. 190) [33]
- **Type**: imports
- **Delta**:
  - What changed: FDB selection method is injected into COA's position-update steps (Eqs. 24–28).
  - Why: to select candidates that are both fit and far from the best, preventing local-optimum traps.
- **Claims affected**: C01, C02
- **Adopted elements**: FDB score SP_i = ω·normF + (1−ω)·normD and the distance vector.

## RW03: Zhou et al., 2012 — Elite Opposition-Based Learning (EOBL)
- **DOI**: (Proc. 13th Int. Conf. Parallel Distrib. Comput., Appl. Technol., Dec. 2012) [47]
- **Type**: imports
- **Delta**:
  - What changed: Elite OBL (Eqs. 34–35) seeds FDBCOA1's initial population; identified as the best of 8 OBL schemes (variant OBL5).
  - Why: forming opposites from elite incumbents balances exploration/exploitation.
- **Claims affected**: C03, C04
- **Adopted elements**: elite opposite generation and out-of-bounds reset rule.

## RW04: Wolpert & Macready, 1997 — No Free Lunch theorem
- **DOI**: 10.1109/4235.585893 (IEEE Trans. Evol. Comput., vol. 1, no. 1) [62]
- **Type**: bounds
- **Delta**:
  - What changed: used to explain why the enhanced variants cannot dominate on every problem.
  - Why: frames the residual losses/ties as expected, not a defect.
- **Claims affected**: C06
- **Adopted elements**: the NFL argument.

## RW05: Garver, 1970 — TNEP via linear programming
- **DOI**: 10.1109/TPAS.1970.292825 (IEEE Trans. Power App. Syst., PAS-89, no. 7) [3]
- **Type**: imports
- **Delta**:
  - What changed: originator of the TNEP problem and the Garver 6-bus test system used here.
  - Why: canonical small-scale benchmark for TNEP methods.
- **Claims affected**: C04, C08
- **Adopted elements**: Garver 6-bus system definition (760 MW load, +545 MW sixth bus).

## RW06: Zimmerman et al. — MATPOWER 6.0
- **DOI**: (software; http://www.pserc.cornell.edu/matpower) [56]
- **Type**: imports
- **Delta**:
  - What changed: provides the DC power-flow solutions for constraint evaluation.
  - Why: fast, standard DC load-flow tooling.
- **Claims affected**: C04, C05
- **Adopted elements**: DC power flow computation.

## RW07: TNEP comparison baselines (inline-comparison references)
These are compared against FDBCOA1-OBL5 in the cost tables (14–19):
- **El-Bages & Elsayed, 2017 — Social Spider Algorithm (SS)** [7] — Garver & IEEE-25 baseline; affects C04. (Electric Power Syst. Res., vol. 143)
- **Mehroliya et al., 2023 — hybrid GA-PSO (GAPSO)** [2] — Garver baseline; affects C04. (Social Netw. Comput. Sci., vol. 4, no. 5)
- **Torres & Castro, 2014 — PLPSO / smart-grid AC expansion (PLPSO)** [25] — Garver-with-resizing baseline; affects C04, C08. (IET Gener., Transmiss. Distrib., vol. 8, no. 5)
- **Rathore & Roy, 2014 — modified GBMO** [65] — IEEE-25 baseline; affects C04. (Int. J. Electr. Power Energy Syst., vol. 62)
- **Rathore et al., 2013 — Mosquitoes-behaviour (MOX)** [66] — IEEE-25 baseline; affects C04. (Proc. Int. Conf. Energy Efficient Technol. Sustainability)
- **Sum-Im et al., 2009 — Differential Evolution (CGA)** [67] — IEEE-25 & Colombian baseline; affects C04. (IET Gener., Transmiss. Distrib., vol. 3, no. 4)
- **Sum-Im, 2009 — DE approach (DEA)** [58] — data source for all systems & baseline; affects C04, C05, C08. (Ph.D. thesis, Brunel Univ.)
- **Gallego et al., 2017 — High-performance Hybrid GA (HGA)** [68] — Colombian baseline (ranks above proposed on cost); affects C04, C06. (IET Gener., Transmiss. Distrib., vol. 11, no. 5)
- **Escobar et al., 2004 — Enhanced Genetic Algorithm (EGA)** [23] — Colombian baseline; affects C04. (IEEE Trans. Power Syst., vol. 19, no. 2)

## RW08: OBL scheme family (imports for the OBL ablation)
Eight OBL schemes seeded FDBCOA1: Classical OBL (Tizhoosh 2005) [43], Quasi-Reflection OBL (Ergezer et al. 2009) [45], Quasi OBL (Rahnamayan et al. 2007) [44], Super OBL (Kaucic 2013) [46], Elite OBL (Zhou et al. 2012) [47] (=RW03), Random OBL (Long et al. 2019) [48], Dynamic OBL (Xu et al. 2020) [49], Probabilistic OBL (Kuang et al. 2022) [50]. Type: imports; affect C03. Eqs. 29–38.

## RW09: FDB-enhanced algorithm precedents (background/inline)
FDB previously improved SFS, AGDE, LSHADE, TLABC, LFD, SDO, PPSO (FDB-SFS/AGDE/LSHADE/TLABC/LFD/SDO/PPSO) [34]–[40], and dynamic FDB (dFDB) improved MRFO [41] and ARO [42]. Type: baseline/background; motivate C01 (FDB transfers across optimizers).

## RW10: TNEP method history (background)
DC vs AC power flow: Rider et al. 2007 AC model [4]. TNEP history: SA & parallel SA (1996–97) [18],[19]; GA (2000) [20]; TS (2001) [21]; ANN+GA+TS (2002) [22]; EGA/DTNEP (2004) [23]; DPSO (2010) [24]; LPSO (2014) [25]; MGPSO (2017) [26]; ACO (2019) [27]; ASSO (2020) [28]; DABC (2021) [29]; LSHADE-SPACMA with N-1 (2021) [30]; IBBA (2022) [31]; GA-PSO (2023) [2]. Dodu & Merlin 1981 first DTNEP [10]. Heuristic methods: fuzzy fault-tree [15], fuzzy logic heuristic [16], sensitivity analysis [17]. Type: background; establish gap G3.
