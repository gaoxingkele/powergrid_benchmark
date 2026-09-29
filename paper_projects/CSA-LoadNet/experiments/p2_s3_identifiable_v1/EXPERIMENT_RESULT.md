## Material Passport

- Origin Skill: experiment-agent
- Origin Mode: run
- Origin Date: 2026-08-13T10:09:59.004216+00:00
- Verification Status: UNVERIFIED
- Version Label: p2_s3_identifiable_v1_exp_result_v1
- Upstream Dependencies: hashed OPSD source; frozen local configuration and driver

# Experiment Result

- **ID:** `p2_s3_identifiable_v1`
- **Type:** neural training and rolling-origin component controls
- **Status:** COMPLETED
- **Run rows:** 240
- **Forecast-day audit rows:** 6750
- **Outer analysis unit:** eight rolling temporal origins; five seed runs averaged within each origin
- **Metrics:** MAPE primary, WAPE secondary; MAE, RMSE, and sMAPE descriptive

## Capacity-matched cross-series result

`CSA-Poincare-Shared` has mean origin-level MAPE 0.0366404835;
`TargetSelfContext-Matched` has 0.0368937083.
The proposed-minus-control MAPE difference is -0.0002532248
(pointwise origin bootstrap 95% interval [-0.0006688492,
0.0002315019], exact sign-flip p=0.3281250000,
Holm p=0.9843750000). Negative differences favor the proposed arm.
Both arms have 29,815 instantiated parameters, the same 100-to-64-to-1 head,
the same optimizer, batches, epochs, seeds, and the same executed attention path.

## Informative context and weighting-form controls

The uniform cross-series control has mean MAPE 0.0367062364.
Its proposed-minus-control difference is -0.0000657529
(Holm p=0.9843750000). No frozen weighting-form contrast separated after Holm correction. This is not an equivalence result because no equivalence margin was specified.

The weighting block is combined evidence only for that bounded joint statement;
it does not identify a best form when contrasts do not separate and it does not
upgrade non-significance to equivalence.

## Shared-versus-independent encoder control

The capacity-matched independent-encoder arm has mean MAPE
0.0420346194; its proposed-minus-control
difference is -0.0053941359
(Holm p=0.0390625000). Although total parameters
and the downstream head are matched, independent encoders use narrower hidden
layers and less encoder arithmetic. This result cannot isolate sharing from
width allocation and does not license a general claim that sharing helps or hurts.

## Evidence boundary

This run narrows confirmation to OPSD lead 24 and does not equalize or rerun the
historical external architecture roster. It does not broaden claims to OPSD
lead 1, SimBench, Ausgrid, other years, exogenous weather, hierarchical
coherence, dispatch, or deployment. Processed positions can skip UTC hours
because the frozen parser drops a row when any selected series is missing.
No independent rerun was performed, so the artifact remains `UNVERIFIED`.
