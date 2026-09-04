# Related Work — mintou_p5 (TRACE-MOEA, target: MDPI Energies)

Working literature file for the Related Work section of the TRACE-MOEA manuscript.
The current item-level audit, claim bindings, search record, and comparator decisions are in
`reconstruction_v2/literature/`; that record supersedes the unavailable historical scratchpad.
Phrasing is written independently of the sibling p6 (BiLo-NSGA) manuscript to keep the
two texts CrossCheck-safe; only unavoidable classic references overlap.

**Status notice.** This is an internal historical literature worksheet. The
claim-authoritative synthesis is Section 2 of `MANUSCRIPT.md`, and scientific
closure is recorded in `THREE_ROUND_SCIENTIFIC_CLOSURE.md`. Planning language
below is bounded by those files and is not evidence for lineage, replay,
explanation quality, human preference validity, deployment, or novelty by
exhaustive absence.

---

## Unresolved problem A — From network planning to auditable project-queue selection

**Scope of the thread.** How utilities decide which grid investments to fund: expansion-planning
optimization, portfolio-level project selection, and the multi-criteria scoring tradition that
review boards actually use when they certify project feasibility.

1. **Hemmati, R.; Hooshmand, R.-A.; Khodabakhshian, A.** State-of-the-art of transmission expansion planning: Comprehensive review. *Renewable and Sustainable Energy Reviews* **2013**, *23*, 312–319. https://doi.org/10.1016/j.rser.2013.03.015
   - Canonical review of transmission expansion planning (TEP) models; documents that TEP research optimizes network topology or capacity, not the selection among heterogeneous, already-specified candidate projects.
2. **Munoz, F.D.; Hobbs, B.F.; Ho, J.L.; Kasina, S.** An Engineering-Economic Approach to Transmission Planning Under Market and Regulatory Uncertainties: WECC Case Study. *IEEE Transactions on Power Systems* **2014**, *29*(1), 307–317. https://doi.org/10.1109/TPWRS.2013.2279654
   - Shows how regulatory and market uncertainty enters real planning economics; motivates why review verdicts need recorded justifications that survive regulatory scrutiny.
3. **Lumbreras, S.; Ramos, A.** The new challenges to transmission expansion planning. Survey of recent practice and literature review. *Electric Power Systems Research* **2016**, *134*, 19–29. https://doi.org/10.1016/j.epsr.2015.10.013
   - Contrasts academic TEP with utility practice; notes practitioners screen discrete project lists — exactly the review setting this paper formalizes.
4. **Wang, J.-J.; Jing, Y.-Y.; Zhang, C.-F.; Zhao, J.-H.** Review on multi-criteria decision analysis aid in sustainable energy decision-making. *Renewable and Sustainable Energy Reviews* **2009**, *13*(9), 2263–2278. https://doi.org/10.1016/j.rser.2009.06.021
   - Establishes MCDA (AHP/TOPSIS families) as the default instrument for energy investment appraisal; criteria weighting is the central methodological lever.
5. **Kumar, A.; Sah, B.; Singh, A.R.; Deng, Y.; He, X.; Kumar, P.; Bansal, R.C.** A review of multi criteria decision making (MCDM) towards sustainable renewable energy development. *Renewable and Sustainable Energy Reviews* **2017**, *69*, 596–609. https://doi.org/10.1016/j.rser.2016.11.191
   - Updated MCDM survey; confirms per-alternative scoring remains dominant and that portfolio-level interactions are outside standard MCDM scope.
6. **Liesiö, J.; Mild, P.; Salo, A.** Preference programming for robust portfolio modeling and project selection. *European Journal of Operational Research* **2007**, *181*(3), 1488–1505. https://doi.org/10.1016/j.ejor.2005.12.041
   - Robust Portfolio Modeling: project selection under incomplete preference information; exact, but restricted to additive value models and modest pool sizes.
7. **Mild, P.; Liesiö, J.; Salo, A.** Selecting infrastructure maintenance projects with Robust Portfolio Modeling. *Decision Support Systems* **2015**, *77*, 21–30. https://doi.org/10.1016/j.dss.2015.05.001
   - Real infrastructure deployment of RPM (bridge maintenance programming); evidence that boards demand decision-support artifacts they can defend, not just optima.
8. **Gao, C.; Wang, X.; Li, D.; Han, C.; You, W.; Zhao, Y.** A Novel Hybrid Power-Grid Investment Optimization Model with Collaborative Consideration of Risk and Benefit. *Energies* **2023**, *16*(20), 7215. https://doi.org/10.3390/en16207215
   - Target-venue example of grid investment optimization coupling risk and benefit; alternatives are aggregate investment directions rather than reviewable project portfolios.
9. **Rodkumnerd, P.; Pothinun, T.; Phumpho, S.; Watson, N.; Siritaratiwat, A.; Srirattanawichaikul, W.; Khunkitti, S.** Fuzzy Analytical Hierarchy Process-Based Multi-Criteria Decision Framework for Risk-Informed Maintenance Prioritization of Distribution Transformers. *Energies* **2026**, *19*(2), 460. https://doi.org/10.3390/en19020460
   - Current target-venue MCDM practice: fuzzy AHP prioritization of grid assets — auditable weighting, but each asset is still scored in isolation.

**What Thread A leaves open.** Expansion planning optimizes network variables, not candidate
subsets; MCDM appraisal scores candidates one at a time and cannot represent budget crowding-out
or cross-project trade-offs; RPM-style exact portfolio methods handle small pools with additive
value only. These differences motivate the present portfolio-level proxy search, but the released
event fields expose only run-level count and pool-position co-occurrence rather than individually
inspectable intermediate decisions.

---

## Unresolved problem B — Preference guidance under hard constraints

**Scope of the thread.** Multi-objective evolutionary algorithms that inject decision-maker
preference structure into the search: reference points, preference relations, reference vectors,
and adaptive preference articulation.

1. **Deb, K.; Pratap, A.; Agarwal, S.; Meyarivan, T.** A fast and elitist multiobjective genetic algorithm: NSGA-II. *IEEE Transactions on Evolutionary Computation* **2002**, *6*(2), 182–197. https://doi.org/10.1109/4235.996017
   - Baseline dominance-based framework; preference-neutral by design, which is what preference-guided variants amend.
2. **Zhang, Q.; Li, H.** MOEA/D: A Multiobjective Evolutionary Algorithm Based on Decomposition. *IEEE Transactions on Evolutionary Computation* **2007**, *11*(6), 712–731. https://doi.org/10.1109/TEVC.2007.892759
   - Decomposition into scalar subproblems via a fixed weight-vector set; weights are static and problem-agnostic — the design choice our adaptive weight population revisits.
3. **Deb, K.; Jain, H.** An Evolutionary Many-Objective Optimization Algorithm Using Reference-Point-Based Nondominated Sorting Approach, Part I. *IEEE Transactions on Evolutionary Computation* **2014**, *18*(4), 577–601. https://doi.org/10.1109/TEVC.2013.2281535
   - NSGA-III: structured reference points sustain selection pressure in many-objective spaces; reference set is again fixed a priori.
4. **Deb, K.; Sundar, J.** Reference point based multi-objective optimization using evolutionary algorithms. In *Proceedings of GECCO 2006*; pp. 635–642. https://doi.org/10.1145/1143997.1144112
   - R-NSGA-II: the seminal reference-point-guided variant focusing search near decision-maker aspiration levels.
5. **Thiele, L.; Miettinen, K.; Korhonen, P.J.; Molina, J.** A Preference-Based Evolutionary Algorithm for Multi-Objective Optimization. *Evolutionary Computation* **2009**, *17*(3), 411–436. https://doi.org/10.1162/evco.2009.17.3.411
   - PBEA: achievement scalarizing functions inside an indicator-based EA; formal bridge between interactive MCDM and EMO.
6. **Ben Said, L.; Bechikh, S.; Ghedira, K.** The r-Dominance: A New Dominance Relation for Interactive Evolutionary Multicriteria Decision Making. *IEEE Transactions on Evolutionary Computation* **2010**, *14*(5), 801–818. https://doi.org/10.1109/TEVC.2010.2041060
   - Preference expressed as a modified dominance relation; interactive updating during the run.
7. **Bechikh, S.; Kessentini, M.; Ben Said, L.; Ghédira, K.** Preference Incorporation in Evolutionary Multiobjective Optimization. *Advances in Computers* **2015**, *98*, 141–207. https://doi.org/10.1016/bs.adcom.2015.03.001
   - Survey and taxonomy of preference incorporation (a priori / interactive / a posteriori); notes validation is almost always on continuous test suites.
8. **Cheng, R.; Jin, Y.; Olhofer, M.; Sendhoff, B.** A Reference Vector Guided Evolutionary Algorithm for Many-Objective Optimization. *IEEE Transactions on Evolutionary Computation* **2016**, *20*(5), 773–791. https://doi.org/10.1109/TEVC.2016.2519378
   - RVEA: reference vectors *adapted* during the run to the objective-space geometry — the closest precedent for run-time preference adaptation, still on continuous benchmarks.
9. **Li, K.; Deb, K.; Yao, X.** R-Metric: Evaluating the Performance of Preference-Based Evolutionary Multiobjective Optimization Using Reference Points. *IEEE Transactions on Evolutionary Computation* **2018**, *22*(6), 821–835. https://doi.org/10.1109/TEVC.2017.2737781
   - Measurement problem of preference-based EMO; quality assessment must respect the preference region, foreshadowing our fixed-bounds evaluation discipline.
10. **Li, K.; Liao, M.; Deb, K.; Min, G.; Yao, X.** Does Preference Always Help? A Holistic Study on Preference-Based Evolutionary Multiobjective Optimization Using Reference Points. *IEEE Transactions on Evolutionary Computation* **2020**, *24*(6), 1078–1096. https://doi.org/10.1109/TEVC.2020.2987559
    - Empirical caution: preference guidance is not uniformly beneficial and can mislead search — directly anticipates the weak/negative component attribution we report for our own preference layer.

**What Thread B leaves open.** Preference-guided EMO overwhelmingly assumes (i) an explicit
decision maker who supplies reference points or aspiration levels, and (ii) continuous benchmark
geometry. Adaptive-preference mechanisms (RVEA-style) tune vectors to objective-space shape, not
to a combinatorial review task; and the literature's own audit (Li et al. 2020) warns that
preference layers may contribute little — consistent with the unresolved direct preference-layer
effect in this constrained binary portfolio benchmark. The paper evaluates a combination of
adaptive preference elitism, deterministic repair, and bounded event summaries; it does not claim
that this combination establishes isolated component novelty or a decision archive.

---

## Unresolved problem C — Run summaries are not decision provenance

**Scope of the thread.** Making algorithmic decisions inspectable: XAI foundations, explainability
for optimization/metaheuristics, provenance models, and algorithmic audit practice.

1. **Miller, T.** Explanation in artificial intelligence: Insights from the social sciences. *Artificial Intelligence* **2019**, *267*, 1–38. https://doi.org/10.1016/j.artint.2018.07.007
   - What humans accept as explanations (contrastive, selected, social); grounds why a move-level decision record is a better explanation substrate than post-hoc summaries.
2. **Barredo Arrieta, A.; Díaz-Rodríguez, N.; Del Ser, J.; et al.** Explainable Artificial Intelligence (XAI): Concepts, taxonomies, opportunities and challenges toward responsible AI. *Information Fusion* **2020**, *58*, 82–115. https://doi.org/10.1016/j.inffus.2019.12.012
   - Standard XAI taxonomy (transparent models vs. post-hoc explanation); optimization algorithms are barely covered, exposing the gap this thread addresses.
3. **Machlev, R.; Heistrene, L.; Perl, M.; et al.** Explainable Artificial Intelligence (XAI) techniques for energy and power systems: Review, challenges and opportunities. *Energy and AI* **2022**, *9*, 100169. https://doi.org/10.1016/j.egyai.2022.100169
   - XAI in the power domain concentrates on ML predictors (forecasting, security assessment); decision/optimization pipelines for investment are absent from the reviewed corpus.
4. **Bacardit, J.; Brownlee, A.E.I.; Cagnoni, S.; Iacca, G.; McCall, J.; Walker, D.** The intersection of evolutionary computation and explainable AI. In *Proceedings of GECCO 2022 Companion*; pp. 1757–1762. https://doi.org/10.1145/3520304.3533974
   - Position paper defining "explainable metaheuristics"; explicitly lists search-trajectory explanation as an open research direction rather than an available technique.
5. **Herschel, M.; Diestelkämper, R.; Ben Lahmar, H.** A survey on provenance: What for? What form? What from? *The VLDB Journal* **2017**, *26*(6), 881–906. https://doi.org/10.1007/s00778-017-0486-1
   - Provenance taxonomy (why/how/where); the present count-and-overlap summaries fall short of process provenance because stable identifiers, ordered payloads, and state transitions are absent.
6. **Moreau, L.; Groth, P.; Cheney, J.; Lebo, T.; Miles, S.** The rationale of PROV. *Journal of Web Semantics* **2015**, *35*, 235–257. https://doi.org/10.1016/j.websem.2015.04.001
   - The W3C PROV design rationale: standardized, machine-readable derivation records; the conceptual template for evidence-linked review trails.
7. **Raji, I.D.; Smart, A.; White, R.N.; et al.** Closing the AI accountability gap: defining an end-to-end framework for internal algorithmic auditing. In *Proceedings of FAT\* 2020*; pp. 33–44. https://doi.org/10.1145/3351095.3372873
   - Institutional audit framing motivates artifacts produced during a process. The present release does not satisfy an end-to-end audit framework because it retains only aggregate run-level fields.

**What Thread C leaves open.** XAI concentrates on learned predictors; explainable-metaheuristics
work is programmatic, with search-trajectory explanation named as open; provenance standards say
*how* to record derivations but are silent on *what* an evolutionary review search should record.
The present implementation quarantines its run-level event summaries from the performance metric;
stable-ID ordered records, state snapshots, lineage, and replay remain open requirements.

---

## Gap statement

Across the three threads, the bounded opening evaluated here is a budget-constrained portfolio
proxy that combines adaptive preference elitism, explicit repair, and performance-quarantined
run-level event summaries under a method-independent metric. NERC and MISO MTEP16 checks provide
descriptive external-consistency views rather than expert validation. Thread A motivates portfolio
selection, Thread B supplies preference machinery and cautions about weak preference effects, and
Thread C identifies provenance requirements that the current aggregate event fields do not meet.
TRACE-MOEA evaluates their integration; it does not establish isolated component novelty, an
auditable decision path, or a validated model of reviewer preference.

## Distinction from the sibling method BiLo-NSGA [sibling]

The companion paper in our research program, BiLo-NSGA, works on the same public candidate-derivation
pipeline, and we separate the two studies on both axes so that neither text nor claims overlap:

- **Mechanism.** TRACE-MOEA augments a constrained non-dominated sorting kernel with three
  components that act at *selection and event-generation* level: a **preference-adaptive**
  weight-vector population (periodically perturbed and re-selected by best-response dispersion;
  an absent best-response row can replace a seeded-random selected slot), a proxy-score **budget
  repair** operator, and an in-memory event list that generates repair-drop and
  preference-best-response records and releases only run-level count and pool-position
  co-occurrence. BiLo-NSGA
  instead concentrates its contribution at *variation* level: a bidirectional local search
  (forward insertion under budget slack, backward deletion of weak selections) with
  dependency-aware move bonuses. Neither method contains the other's core operator.
- **Problem lens.** TRACE-MOEA targets **investment-effectiveness review with traceability**: a
  five-objective formulation that includes a compliance/evidence quality objective, scenarios
  organized around review preferences (reliability-driven, renewable-accommodation,
  preference-aware, traceability evaluation), and a two-rung external-validity ladder against NERC
  reliability reports and MISO MTEP16 historical project outcomes. BiLo-NSGA poses a
  four-objective problem where the **hard budget envelope** is the organizing question (budget
  multiplier scans, loose-budget stress tests) and no external-outcome backtest is attempted.
- **Shared artifact, declared.** Candidate-generation code, source corpora, common benchmark and
  evaluation utilities, and public-record backtest infrastructure are shared. Problem formulation,
  configurations, executions, run outputs, selected portfolios, comparisons, and claims are
  paper-specific. The shared infrastructure is disclosed and is not claimed as TRACE-MOEA's
  independent contribution.
