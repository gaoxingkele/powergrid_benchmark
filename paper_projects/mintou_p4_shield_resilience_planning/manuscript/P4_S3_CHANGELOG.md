# P4 Stage-3 Boundary Experiment Changelog

Date: 2026-08-13. Stage: `p4_s3_boundary_experiments`.

## Scientific changes

- Reconciled the boundary axes to implemented quantities: budget factor,
  scenario count with `K/|S|=1/4`, and the selected-action coefficient in the
  survivability equation. The inactive DER-output multiplier was not used.
- Wrote `experiments/p4_s3_boundary_predeclared.json` before execution and ran
  7 settings × 5 methods × 30 independent method-specific seeds (1050 complete
  invocations) on new disjoint search/evaluation scenario draws.
- Scored every raw held-out front with primary clipped fixed-bound HV at 1.1,
  an unclipped audit at 1.1, and clipped HV at the predeclared alternative
  reference point 1.2.
- Preserved all results. The runner refuses to overwrite the run files, and the
  manifest hashes eight controlling/generated assets.

## Evidence outcome

- SHIELD-minus-NSGA-II+Repair is positive in all seven settings under the
  primary score (0.01013--0.01885; 3.46--7.20%); all seven pointwise bootstrap
  intervals are above zero. The sign remains positive under both HV audits.
- Clipping is not benign: 441/1050 fronts contain 960 low-side out-of-bound
  components. It changes gap magnitude, especially for tight budget and the
  0.75 survivability-action scale.
- Method-independent bounds include infeasible singletons. The cost bound is
  approximately -32,195 to 676,102 against budgets 754.4--1104, so feasible
  cost differences occupy a narrow normalized band.
- Mechanism attribution remains null/adverse. DE-only has a higher primary mean
  in 7/7 settings but all pointwise intervals span zero; fixed worst-K is
  unresolved in 7/7. Under tight budget, full-minus-GA-only is -0.00326 with a
  pointwise interval [-0.00582, -0.00061]. No equivalence or confirmatory
  GA-only superiority claim is made.

## Scope and implementation

- No shared p3/p4 planning source or p3 claim was changed.
- The local boundary runner reconstructs the 72 candidates from a frozen,
  hash-traced 18-subnet profile. Its NSGA-II+Repair path uses installed pymoo
  0.4.1 with a NumPy Euclidean-distance compatibility shim for duplicate
  elimination because the environment's SciPy binary cannot import. No SciPy
  statistical routine is used; uncertainty intervals are fixed-seed bootstrap
  calculations declared in advance.
- The boundary archive supplements and does not replace or pool with the main
  historical archive.

## Remaining human blockers

- Author identities, affiliations, CRediT roles, funding, APC responsibility,
  and the persistent public archive URL/DOI remain author inputs.
- A complete historical executable supplement remains to be assembled; this
  stage adds only the self-contained boundary package.
