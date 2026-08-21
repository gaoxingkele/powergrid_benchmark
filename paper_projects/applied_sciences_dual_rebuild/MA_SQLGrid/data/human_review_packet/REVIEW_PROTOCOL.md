# Two-person blind review, adjudication, and promotion protocol

## Independence and sequence

1. Freeze `packet_hashes.json`; assign one real reviewer to A and another to B.
2. Each reviewer receives only their own form, field definitions, schemas/dictionaries and read-only databases.
3. Reviewers complete all required fields without communicating or reading machine flags/other decisions.
4. Freeze and hash both completed forms before running `agreement.py`.
5. A third real person adjudicates every disagreement and every missing critical field. Revised SQL is re-executed and its result hash recorded.
6. A reviewer must not be described as a power-system expert unless their real qualification supports that description.

## Full-review and sampling rules

- **Promotion path:** all 91 items receive two independent reviews. Every `REVISE` item is reviewed again after correction; every conflict is adjudicated. Sampling is not sufficient for gold/sealed promotion.
- **Exploratory triage only:** if resources are temporarily constrained, review 100% of machine-high-risk items plus a deterministic stratified 25% of the remainder by dataset × family × class × difficulty. Such a sample can refine instructions but cannot support benchmark-quality or agreement claims for all 91 items.
- Machine risk is not a substitute for random/stratified coverage; low-risk items can contain semantic defects.

## Agreement and quality gates

Run:

```powershell
python agreement.py --reviewer-a reviewer_A_completed.csv --reviewer-b reviewer_B_completed.csv `
  --json-out agreement.json --markdown-out agreement.md --conflicts-out conflicts.csv
```

Report field-level coverage, raw agreement and Cohen's kappa. Kappa measures consistency, not correctness. Suggested project targets before benchmark promotion are 100% critical-field coverage, raw decision agreement ≥0.85, and κ ≥0.75 for decision/semantic/SQL judgments. Missing those targets triggers instruction refinement and a second independent pass; it does not license selective deletion.

## Sealed-test gate

Human review alone cannot retroactively make development-visible data sealed. The current 91 questions are visibly stored in the workspace and must remain `AUTO_CANDIDATE`/unsealed unless access history proves an item was never used for prompt, method, repair-rule, threshold, baseline or model selection.

For any future subset to become sealed, all conditions are required:

1. two-person full review and conflict adjudication are complete;
2. final NL, SQL and results are independently re-executed and frozen by hash;
3. template families and semantic intents are isolated from development data;
4. duplicate/paraphrase leakage checks pass;
5. source/license and redistribution decisions are recorded;
6. the subset is selected before modeling, stored access-controlled, and has an access log;
7. method/configuration/thresholds are frozen before a single sealed run;
8. no failed item is silently dropped after unsealing;
9. the experiment reaches E4 independent evidence audit.

Items already used during development may be promoted only to a human-reviewed **unsealed** evaluation or development set. A genuinely sealed test should preferably contain newly authored/deeply rewritten questions unavailable to the model-building team.
