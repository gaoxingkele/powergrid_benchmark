# Remaining Validation Gaps

These are not failures of the ARA package; they are boundaries that must be disclosed or closed before stronger claims.

| Paper | Signal | Remaining Validation Gap |
| --- | --- | --- |
| mintou_p1 | narrow_promising_public_signal | Add DC-OPF/UC or Grid2Op validation. |
| mintou_p2 | day_ahead_promising_public_signal | Add stronger neural short-horizon baselines only if 1h claims are needed. |
| mintou_p3 | narrow_promising_public_signal | Add pandapower/AC load-flow and repeated DER-hosting scenario variance. |
| mintou_p4 | promising_public_signal | Add AC/pandapower feasibility and repeated scenario variance. |
| mintou_p5 | promising_public_signal | Add expert-labeled feasibility-review outcomes and cost calibration. |
| mintou_p6 | promising_public_signal | Add expert-labeled review outcomes, dependency labels, and calibrated budget cases. |

## Upgrade Policy

These gaps should now be treated as experiment gates rather than optional notes. The concrete upgrade matrix is maintained in `experiment_strength_upgrade_plan.md`.
