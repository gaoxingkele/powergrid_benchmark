# Cover Letter Notes: SHIELD-MOEA (p4) Submission to MDPI Energies

Purpose: material for the cover letter, addressing the editor directly on the
relationship between this manuscript (SHIELD-MOEA, "p4") and its companion
manuscript (CARS-MODE, "p3"). The two papers share one versioned public
artifact -- the SimBench-derived candidate-pool generation code -- and nothing
else. Disclosing the relationship proactively, with a differentiation table,
pre-empts the "salami-slicing" reading and converts the shared benchmark into
a comparability feature.

## Suggested cover-letter paragraph (draft)

> We wish to disclose that a companion manuscript from the same research
> program (CARS-MODE, currently under review) uses the same public
> SimBench-derived candidate-generation pipeline. The shared component is
> limited to candidate-pool generation, which is a versioned public artifact;
> the two papers study methodologically independent algorithms, different
> problem framings, disjoint mechanism contributions, and share no
> experimental claims. Both manuscripts declare the shared artifact in their
> Related Work, benchmark, and Data Availability sections. A differentiation
> summary is provided below for the editor's convenience.

## Companion-differentiation table (p3 vs. p4)

| Dimension | p3: CARS-MODE (companion) | p4: SHIELD-MOEA (this manuscript) |
|---|---|---|
| Evolutionary kernel | Strategy-adaptive binary multi-objective differential evolution (MODE); adaptation acts on mutation/crossover/repair intensity from population feedback | NSGA-II core (constraint-dominated sorting + crowding) with fixed operators: hybrid GA/DE variation + greedy feasibility repair |
| Where the novelty lives | Parameter/strategy self-adaptation inside the operators | Scenario-set adaptation at the optimizer-uncertainty interface (worst-K screening) + leakage-proof evaluation protocol |
| Problem framing | Economic DER-and-storage integration planning under conventional operating conditions; characteristic output is DER-heavy plans | Resilience-oriented planning under load/DER/outage uncertainty, incl. an unseen-stress generalization experiment |
| Evaluation protocol | Standard front evaluation; headline discussion centers on the HV-vs-AC trade-off its plans exhibit | Strict leakage-proof protocol: final fronts scored only on disjoint-seed (and, in one experiment, disjoint-range) scenario sets; mean plus worst-case hypervolume readouts |
| AC power-flow layer finding | Documents an HV-vs-AC trade-off (proxy-strong plans are not automatically AC-strong) | Plans tied for the top AC-feasible rate (0.708); AC layer isolates outage-aware search as the physically load-bearing component (0.708 -> 0.625, loading 68.8% -> 82.3% when removed) |
| Shared artifact | Candidate-pool generation code only (public, versioned) | Same -- everything downstream (scenario model, experiments, methods, analyses) is paper-specific |
| Mechanism overlap | None: parameter self-adaptation (p3) and scenario-set adaptation (p4) are orthogonal; neither method contains the other's mechanism | -- |
| Experimental claims overlap | None | None |

## Additional submission notes

- The manuscript's Sections 2.4 and 3.4 and the Data Availability statement
  each declare the shared pipeline explicitly; reference [42] cites the
  companion manuscript as "under review".
- If the editor prefers, the two submissions can be handled by disjoint
  reviewer pools; the papers are self-contained and cross-reference only for
  the shared candidate-generation artifact.
- Remaining pre-submission mechanical items tracked separately: author
  list/affiliations/correspondence, funding statement, repository URL/DOI in
  Data Availability (all currently [TODO] placeholders in MANUSCRIPT.md).
