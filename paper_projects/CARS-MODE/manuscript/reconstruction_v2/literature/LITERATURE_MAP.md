# Verified Literature Map

## Scope and audit result

All 32 references in the frozen manuscript bibliography are inventoried in `REFERENCE_VERIFICATION.csv`. The inventory separates existence, metadata consistency, and sentence-level support. No source is promoted beyond its demonstrated scope. In particular, references 18 and 19 are respectively transmission-expansion and economic-dispatch analogues; references 1--4, 20--31 are algorithm, constraint, indicator, software, or benchmarking sources and do not validate the engineering interpretation of this study.

The historical manuscript note records a Crossref author-list audit on 2026-07-17. This stage checked consistency between the two manuscript forms, exact identifiers, visible publisher/discovery metadata, and every in-text use. Where automated publisher access was blocked or rate-limited, the verification row says so indirectly through the named evidence route and does not claim a new Crossref retrieval.

## Claim map

### Action-aligned distribution expansion, DER, and storage

References 8--17 establish the topic space, but their exact roles differ. References 10--12 concern expansion or reinforcement; references 15--17 concern explicit storage, EV, DG, capacitor, or resilience applications. The newly mapped `SRC-A1` is the strongest action-alignment comparator found in this pass because its formulation names substations, transformers, MV/LV branches, RES, BESS, upgrades, and investment/operating costs. `SRC-A2` adds an explicit storage location/capacity decision with an AC-OPF formulation.

These sources reveal the present manuscript's boundary rather than cure it: the current decision vector remains a portfolio proxy and is not a bus/line/project investment encoding. Literature relevance cannot substitute for missing action, cost, and network-parameter mappings.

### AC validation

References 5 and 7 support the identities and intended roles of SimBench and pandapower. They do not establish that the archived optimizer outputs are AC feasible. `SRC-A2` and `SRC-A1` show stronger forms of electrical coupling in which location/capacity or network investments enter a power-flow/OPF model. The current study's 72 fixed-case outcomes share three selected compositions and remain an illustrative composition-level diagnostic.

### Self-adaptive DE

Reference 2 supports jDE-style adaptation of `F` and `CR`; reference 3 supports success-driven strategy adaptation; references 24 and 25 support success-history and composite extensions. Their benchmark evidence is algorithmic and mostly continuous-domain. It is not evidence that self-adaptation improves this binary distribution-planning proxy. Because the implemented `FixedDE` contrast changes parameter and strategy adaptation together, only a joint-controller conclusion is identifiable, and the current evidence does not show a positive joint effect.

### Constraint handling

References 29 and 30 support the taxonomy and feasibility-based selection rationale. They do not demonstrate the efficacy of this manuscript's greedy budget repair. Any repair conclusion must come from the manuscript's own repair ablation, with its exact configuration and metric qualifiers.

### Multi-objective evaluation

Reference 20 supports hypervolume's indicator lineage; `SRC-M1` supplies direct IGD+ evaluation evidence; reference 32 supports Holm's sequential multiple-testing procedure. The manuscript's sampled/clipped hypervolume, analytic-envelope hypervolume, and common-reference IGD+ are different analysis constructions. Their observed ranking reversal must remain visible; none may be treated as a cosmetic robustness check.

## Citation-context corrections and use rules

- Reference 1 supports the original DE method but is only indirect support for the broad statement that DE is sensitive to both control parameters and mutation strategy. References 2, 3, 23--26 are the stronger mechanism sources.
- Reference 4 supports comparative benchmarking across test suites; it does not itself validate the power-engineering protocol.
- Reference 6 supports the `pymoo` platform. Exact implementation/version behavior still depends on the archived environment and code, not the paper alone.
- Reference 21 supports a multi-objective optimization platform, not the manuscript's general reproducibility-risk claim by itself; reference 22 is the direct benchmarking-risk source.
- References 18 and 19 remain clearly labelled analogues.
- Generic optimizer, software, metric, and statistics papers must never be cited as proof of action alignment, AC feasibility, deployment readiness, or distribution-system benefit.

## Unresolved evidence boundaries

No literature source can resolve the study-specific gaps identified in P3-C04--P3-C06. Separate parameter-versus-strategy attribution needs a four-arm experiment. Candidate-level AC validity needs end-to-end mapping of every relevant plan and operating case. Engineering planning claims need explicit buses, lines/projects, capacities, monetary calibration, and network constraints. Until then, the allowed description is a distribution-planning portfolio proxy with an illustrative AC diagnostic.
