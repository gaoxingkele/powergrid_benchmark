# Claims

## C01: C4 Compact Domain Context Accuracy

- Statement: MA-SQLGrid C4 compact domain context reaches execution accuracy 0.7000 on the 180-question test split.
- Status: Imported from verified package; not locally rerun.
- Scope: GridDB-Maintenance-v2 v0.1 only.
- Falsification: A rerun on the same test split does not reproduce the C4 score within expected deterministic behavior.
- Proof: `paper_projects/2026_ma_sqlgrid_cmc/source/evidence/validator_diagnostics/validator_diagnostics.json`

## C02: C5 Validated Variant Gain

- Statement: MA-SQLGrid C5 validated variant reaches execution accuracy 0.7278 and reduces execution errors relative to C4.
- Status: Imported from verified package; not locally rerun.
- Scope: GridDB-Maintenance-v2 v0.1 only.
- Falsification: Same-artifact rerun fails to show the reported C5 score or execution-error reduction.
- Proof: `paper_projects/2026_ma_sqlgrid_cmc/source/evidence/validator_diagnostics/validator_diagnostics.json`

## C03: Citation Verification Complete

- Statement: Stage 23 citation verification has 45 cited keys, 0 missing cited keys, and decision `proceed`.
- Status: Imported from final package.
- Scope: Uploaded package state.
- Falsification: Local citation sync finds missing or extra verified keys.
- Proof: `paper_projects/2026_ma_sqlgrid_cmc/source/verification/verification_report.json`; `paper_projects/2026_ma_sqlgrid_cmc/source/verification/stage23_decision.json`
