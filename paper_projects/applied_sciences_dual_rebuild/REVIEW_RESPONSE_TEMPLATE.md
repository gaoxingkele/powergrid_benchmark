# Three-Round Review and Response Template

## Review metadata

- Paper: `MA-SQLGrid | C2GES`
- Round: `1 Scientific validity | 2 Applied/venue fit | 3 Rejection stress test`
- Reviewer agent role:
- Frozen manuscript hash:
- Frozen canonical-results hash:
- Recommendation: `Reject as-is | Major revision | Minor revision | Ready`

## Overall assessment

One paragraph covering contribution, strongest evidence, principal validity risk, and the exact condition for a positive recommendation.

## Review comments

| ID | Severity | Location | Evidence inspected | Problem | Requested action | Acceptance test |
|---|---|---|---|---|---|---|
| R1-METHOD-001 | Critical/Major/Minor | Section/Table/Figure/line | file + run_id |  |  | binary/verifiable test |

Severity rules:

- **Critical**: leakage, fabricated/missing evidence, invalid task definition, license/ethics issue, unreproducible headline result.
- **Major**: claim not supported, missing strong baseline, unfair comparison, wrong statistics, applied-value gap.
- **Minor**: clarity, organization, terminology, figure/readability or formatting issue that does not change conclusions.

## Author/agent response matrix

| Comment ID | Response | Changed artifact | Before → after evidence | Validator | Status |
|---|---|---|---|---|---|
| R1-METHOD-001 | Agree/partly agree/disagree with evidence | file/path | run/table/figure | command or manual check | Open/Resolved/Accepted risk |

Disagreement is allowed only with concrete evidence. “Reworded” is not a sufficient response to a request for missing validation.

## Round closure

- Critical open:
- Major open:
- Minor open:
- New experiments introduced:
- Claims strengthened:
- Claims weakened/removed:
- PI-Integrator decision: `Close round | Reopen targeted work`

Round closure requires Critical=0 and Major=0. Round 3 may not introduce a new unsupported headline contribution.
