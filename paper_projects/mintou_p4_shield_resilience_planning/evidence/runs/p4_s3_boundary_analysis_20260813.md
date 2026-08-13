# P4 Boundary Experiment Analysis

Run: `p4_s3_boundary_20260813`. This is a predeclared exploratory boundary study and does not replace the main archive.

## Hypervolume Audit

All settings use one bounds vector computed before method execution from the declared reference-plan sample. Across 1050 run fronts, 441 required clipping (960 objective components).
The primary score clips affine values to [0,1] at reference point 1.1. The same raw fronts were also scored without clipping and with the predeclared alternative reference point 1.2.

## SHIELD minus NSGA-II+Repair

| Setting | Primary mean gap | Relative gap | 95% bootstrap interval | Gap sign stable across clipping/reference audits? |
|---|---:|---:|---:|---|
| reference | 0.01383 | 5.38% | [0.00963, 0.01809] | True |
| budget_tight_0p82 | 0.01090 | 4.39% | [0.00765, 0.01441] | True |
| budget_loose_1p20 | 0.01013 | 3.46% | [0.00557, 0.01457] | True |
| scenarios_8 | 0.01677 | 6.63% | [0.01288, 0.02047] | True |
| scenarios_32 | 0.01598 | 6.23% | [0.01082, 0.02083] | True |
| resilience_scale_0p75 | 0.01885 | 7.20% | [0.01385, 0.02473] | True |
| resilience_scale_1p25 | 0.01390 | 5.37% | [0.00993, 0.01793] | True |

## Mechanism Gaps

Positive values favor the full hybrid/dynamic SHIELD configuration. Intervals are pointwise and multiplicity-unadjusted; overlap with zero is not an equivalence result.

| Setting | Opponent | Primary mean gap | 95% bootstrap interval |
|---|---|---:|---:|
| reference | Control-GAOnly | 0.00179 | [-0.00267, 0.00624] |
| reference | Control-DEOnly | -0.00247 | [-0.00610, 0.00117] |
| reference | Control-FixedWorstK | 0.00053 | [-0.00345, 0.00459] |
| budget_tight_0p82 | Control-GAOnly | -0.00326 | [-0.00582, -0.00061] |
| budget_tight_0p82 | Control-DEOnly | -0.00278 | [-0.00561, 0.00018] |
| budget_tight_0p82 | Control-FixedWorstK | -0.00138 | [-0.00428, 0.00161] |
| budget_loose_1p20 | Control-GAOnly | 0.00136 | [-0.00313, 0.00588] |
| budget_loose_1p20 | Control-DEOnly | -0.00322 | [-0.00769, 0.00133] |
| budget_loose_1p20 | Control-FixedWorstK | -0.00121 | [-0.00569, 0.00352] |
| scenarios_8 | Control-GAOnly | 0.00049 | [-0.00362, 0.00490] |
| scenarios_8 | Control-DEOnly | -0.00281 | [-0.00633, 0.00074] |
| scenarios_8 | Control-FixedWorstK | 0.00059 | [-0.00267, 0.00382] |
| scenarios_32 | Control-GAOnly | 0.00290 | [-0.00243, 0.00785] |
| scenarios_32 | Control-DEOnly | -0.00076 | [-0.00542, 0.00338] |
| scenarios_32 | Control-FixedWorstK | -0.00086 | [-0.00582, 0.00370] |
| resilience_scale_0p75 | Control-GAOnly | 0.00079 | [-0.00290, 0.00449] |
| resilience_scale_0p75 | Control-DEOnly | -0.00061 | [-0.00393, 0.00276] |
| resilience_scale_0p75 | Control-FixedWorstK | 0.00223 | [-0.00187, 0.00621] |
| resilience_scale_1p25 | Control-GAOnly | 0.00444 | [-0.00007, 0.00916] |
| resilience_scale_1p25 | Control-DEOnly | -0.00160 | [-0.00565, 0.00254] |
| resilience_scale_1p25 | Control-FixedWorstK | -0.00080 | [-0.00515, 0.00348] |

## Interpretation Boundary

Budget factor, scenario count, and the action-gain coefficient in the survivability equation are varied one at a time. The DER-output multiplier remains inactive. Scenario-count settings scale K at one quarter of the search draw and change both the search and disjoint evaluation sample sizes. The resilience coefficient changes the proxy formulation and its method-independent bounds, but not the fixed repair heuristic. These are proxy-benchmark reruns, not AC, deployment, tail-bound, or monetary-calibration evidence.
