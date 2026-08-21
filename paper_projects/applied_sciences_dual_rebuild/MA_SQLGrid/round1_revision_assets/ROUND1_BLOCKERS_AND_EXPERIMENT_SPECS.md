# Round-1 blockers and executable experiment specifications

## Human/external blockers

| Blocker | Current state | Completion evidence required |
|---|---|---|
| External semantic review | 0/91 completed; RTS-GMLC 55 and SimBench 36 remain `AUTO_CANDIDATE` and unsealed | two independent complete forms, frozen hashes, agreement report, third-person adjudication, re-executed final SQL/result hashes |
| Genuinely sealed external test | current 91 were visible during development | newly authored/deeply rewritten, family-isolated access-controlled set; access log; frozen method before one no-drop run |
| GridDB redistribution | permission/license unresolved | author/license-owner decision plus explicit license/permission or lawful regeneration route |
| Public artifact access | local hashes only | permission-filtered archive with permanent DOI/URL and environment lock |
| Semantic validity audit | no blinded human/test-suite audit | adjudicated sample or discriminating perturbed database states |
| MDPI front matter | author/affiliation/CRediT/funding/COI/acknowledgment/AI statement placeholders | real author confirmations; never agent-inferred |

## E1 — value-grounding ablation

**Question.** What changes when value and normalization grounding is removed while schema serialization and the composite hint are held fixed?

**Registered arms.** Extend to a `2 context packages × 2 composite hints × 2 grounding states` design. For the controlled estimand, construct paired packages in which the exact same schema serialization is used with (a) grounding fields present and (b) all value dictionaries, exact matched values, and handcrafted normalization/predicate hints removed. Do not call the old full-versus-compact difference a value ablation.

**Execution.** Use a new formal run directory; both backbones; one frozen generation per item/arm; same database/model/runtime; no retries after a valid response; all 180 attempts retained. Freeze prompts before serving.

**Outcomes.** Primary frozen-snapshot execution equality. Secondary safe-executable rate, common-target projection-count diagnostic, missing/invalid-column/value error taxonomy, prompt tokens. Estimate paired grounding main effects and interactions with template-cluster bootstrap; report question-level discordances descriptively.

**Gate.** Claim only a GridDB-local package effect. Because rules were corpus-exposed, replication on the sealed external set is required for generality.

## E2 — candidate replay validator experiment

**Question.** Does deterministic validation/selection improve choice among identical raw candidates?

**Freeze.** Generate `K` candidates once for every item using a fixed prompt/model/seed schedule and archive raw candidates before any selector is evaluated. Candidate generation must be identical for all validator arms.

**Arms.** (1) first parsed candidate; (2) safety+executability selector; (3) safety+execution+reference-free structural/value selector; optionally (4) the historical rule-weight ranker reproduced exactly. No arm may see gold SQL, gold result, or correctness feedback.

**Primary contrast.** Paired selected-candidate execution equality on all attempts. Also report oracle-in-candidate-set as a conditional diagnostic, selection regret, abstention, unsafe rate, and candidate-set diversity. Use cluster-aware paired intervals/permutation. A repair model call is a separate intervention and must not be mixed into replay.

## E3 — BIRD/DKA-style competitive baseline

**Dataset.** Register a permission-compatible, schema-stratified BIRD validation subset before model execution, plus the final human-reviewed grid set. Do not tune on evaluation items.

**Same-environment arms.** Plain direct full-schema prompt; explicit CoT/decomposition prompt; schema-selection/retrieval baseline; verification/candidate-replay baseline; released DKASQL if reproducible, otherwise clearly named “DKASQL-style reimplementation.” Hold model snapshot, quantization, max context/output, decoding, evaluator, and hardware fixed.

**Reporting.** Per-database all-attempt execution accuracy, safe-executable rate, prompt/output tokens, latency, and failure taxonomy. Do not import DKASQL version-of-record scores into a same-environment table. Publish configuration and implementation deviations.

## E4 — efficiency experiment

**Design.** Re-run the frozen four prompt cells for both backbones on one machine, randomized/interleaved by cell to reduce drift. Perform separately logged cold-start and warmed runs; at least 10 repeated timed passes per cell for stable latency summaries if deterministic caching is disabled or declared.

**Measurements.** Actual tokenizer input/output tokens; prompt bytes; model generation wall time and tokens/s; SQL execution time; end-to-end latency; peak host RAM; peak accelerator memory; failure/retry count; optional energy using a named meter/software method. Record hardware, drivers, llama.cpp revision, thread/GPU-layer/batch/context settings, and background-load policy.

**Analysis.** Report full-versus-compact resource differences jointly with execution differences; use paired question-level summaries and cluster-aware uncertainty. No post-hoc “Pareto” claim without a prospectively defined decision rule.

## E5 — sealed external confirmatory experiment

**Construction.** After prompt/schema repair is frozen, create 50–100 newly authored or deeply rewritten items spanning RTS-GMLC and multiple SimBench networks; target at least 15–20% genuinely human-authored items. Two reviewers independently assess semantics, SQL, units, projection, ordering, NULL/tie behavior, and difficulty; a third adjudicates.

**Sealing.** Isolate families/intents from development data, freeze databases/SQL/results/hashes, store access-controlled with an access log, and prohibit the modeling team from viewing contents before the final configuration hash is signed.

**Execution.** One no-drop run of both backbones and all four packages; preserve every provider, parse, safety, and execution failure in the denominator. Report RTS-GMLC and each SimBench network separately as well as a predeclared aggregate.

**Promotion gate.** 100% critical-field coverage, recorded agreement/adjudication, license clearance, independent artifact audit, and no post-unsealing method changes. The existing 91 visible candidates may become human-reviewed **unsealed** evidence only.

