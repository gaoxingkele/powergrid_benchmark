# Cover Letter Notes: SHIELD-MOEA (p4) Submission to MDPI Energies

Purpose: material for the cover letter, addressing the editor directly on the
relationship between this manuscript (SHIELD-MOEA, "p4") and its companion
manuscript (CARS-MODE, "p3"). The two papers share public benchmark and
evaluation infrastructure: the planning runner, SimBench extraction and
candidate builder, binary-plan/budget structures, evaluation/statistics
utilities, seeded archive machinery, and AC composition mapper. Their research
questions, method-specific configurations, run archives, comparisons, and
conclusions are independent. Disclosing the relationship proactively, with a differentiation table,
pre-empts the "salami-slicing" reading and converts the shared benchmark into
a comparability feature.

## Suggested cover-letter paragraph (draft)

> We wish to disclose that a companion manuscript from the same research
> program (CARS-MODE, an unpublished companion manuscript whose final status
> requires author confirmation) uses the same public
> SimBench-derived planning and evaluation infrastructure, including source
> extraction, candidate construction, binary budget representation, common
> evaluation utilities, seeded archive machinery, and the AC composition
> mapper. The two papers study methodologically independent algorithms,
> different problem framings, disjoint mechanism contributions, and share no
> experimental claims or run archives. Both manuscripts declare the shared infrastructure in their
> Related Work, benchmark, and Data Availability sections. A differentiation
> summary is provided below for the editor's convenience.

## Companion-differentiation table (p3 vs. p4)

| Dimension | p3: CARS-MODE (companion) | p4: SHIELD-MOEA (this manuscript) |
|---|---|---|
| Evolutionary kernel | Strategy-adaptive binary multi-objective differential evolution (MODE); adaptation acts on mutation/crossover/repair intensity from population feedback | NSGA-II core (constraint-dominated sorting + crowding) with fixed operators: hybrid GA/DE variation + greedy feasibility repair |
| Where the novelty lives | Parameter/strategy self-adaptation inside the operators | Scenario-set adaptation at the optimizer-uncertainty interface (worst-K screening) + direct-scenario-reuse-controlled evaluation protocol |
| Problem framing | Economic DER-and-storage integration planning under conventional operating conditions; characteristic output is DER-heavy plans | Resilience-oriented planning under load/DER/outage uncertainty, incl. an unseen-stress generalization experiment |
| Evaluation protocol | Standard front evaluation; headline discussion centers on the HV-vs-AC trade-off its plans exhibit | Final fronts scored only on disjoint-seed (and, in one experiment, active-coordinate disjoint-range) scenario sets; mean plus sampled worst-envelope hypervolume readouts; a 1050-run boundary supplement audits clipping and reference geometry |
| AC power-flow layer finding | Documents an HV-vs-AC trade-off (proxy-strong plans are not automatically AC-strong) | Mapped compositions reach 0.685 AC feasibility versus 0.389 without planning and 0.694 for NSGA-II+Repair; removing outage-aware search reaches 0.574 under the same fixed mapping |
| Shared infrastructure | Planning runner, source extraction, candidate builder, binary-plan/budget representation, evaluation/statistics utilities, seeded archives, and AC mapper | Same infrastructure; paper-specific method branch, scenario question, configurations, archives, comparisons, and conclusions |
| Mechanism overlap | None: parameter self-adaptation (p3) and scenario-set adaptation (p4) are orthogonal; neither method contains the other's mechanism | -- |
| Experimental claims overlap | None | None |

## Additional submission notes

- The manuscript's Sections 2.4 and 3.4 and the Data Availability statement
  each declare the shared pipeline explicitly; reference [42] cites the
  companion as an unpublished manuscript. Its final bibliographic identity and
  submission status require author confirmation.
- If the editor prefers, the two submissions can be handled by disjoint
  reviewer pools; the papers are self-contained and cross-reference only for
  the shared benchmark/evaluation infrastructure.
- Remaining pre-submission mechanical items tracked separately: author
  list/affiliations/correspondence, funding statement, repository URL/DOI in
  Data Availability (all currently [TODO] placeholders in MANUSCRIPT.md).
