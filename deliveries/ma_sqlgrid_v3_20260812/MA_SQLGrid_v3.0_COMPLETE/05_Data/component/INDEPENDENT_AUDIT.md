# Independent Audit of Prospective Component Experiments

## Verdict

**PASS with a mandatory latency boundary.** The frozen prompt/call-order ledgers, two 350-call formal runs, sealed reference-free selections, scored ledgers, and registered aggregate numbers were independently checked. No source freeze, run, scoring, or analysis artifact was changed.

## Recomputed evidence

- Each backbone has exactly 350 unique formal calls: 170 paired V0/V1 questions plus 10 additional V1-only questions, giving 180 V1 questions. Both runs contain 350 successes, zero provider failures, and 350 zero-retry calls.
- The intervention-eligible set independently reconstructs to 170 questions in 61 frozen template clusters. Question text, selected-table hash, selected-column hash, and inferred-shape hash are invariant within every V0/V1 pair.
- Prediction and candidate-selection ledgers contain no gold/reference fields. The selection seals bind their ledgers, and scoring manifests bind the same selection hashes. This is strong ledger-level evidence for selection-before-gold, but it is not an external timestamp or notarial proof.
- All 700 scored rows and every parsed candidate were independently re-executed against the frozen SQLite state; the execution-equality flags match the sealed scored ledgers exactly.
- For the frozen-state execution-equality outcome, Qwen E1 is +0.1059 (95% cluster bootstrap CI +0.0282 to +0.2013; Holm p=0.0310), satisfying the preregistered positive-efficacy rule. Granite E1 is 0.0000 (CI -0.1902 to +0.1705; Holm p=1.0000).
- For the same outcome, Qwen E2 is +0.0389 (CI -0.0081 to +0.1071; Holm p=0.5008). Granite E2 is +0.0556 (CI +0.0075 to +0.1232; Holm p=0.1285). Neither E2 result is promoted because the complete preregistered rule includes Holm-adjusted p<0.05.
- The backbones are sensitivity analyses on the same 180-question benchmark, not independent replications. Replication is false for E1 and E2.
- Zero retries preserve token accounting. Latency remains **diagnostic only** because the required exclusive-GPU/thermal/competing-process efficiency attestation is absent.

## Publication use

Use `table_primary_effects` for confirmatory frozen-state execution-equality results, `table_selection_descriptives` for E2 mechanism diagnostics, and `table_efficiency_diagnostic` only with the explicit diagnostic label. Figures use the same separation. Do not state that E2 improved either model, do not call the two backbones replications, and do not make a controlled latency claim.
