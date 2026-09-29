# E2 human validation — costed execution plan

Status: `PLAN_ONLY / NO HUMAN LABELS COLLECTED / NO ETHICS DETERMINATION YET`
Companion documents: `ANNOTATION_PROTOCOL.md` (rubric, `DRAFT_NOT_FROZEN`),
`ETHICS_REVIEW_REQUEST_PACKET.md`, `E2_ANNOTATOR_INFORMATION_AND_CONSENT.md`,
`E2_DATA_MANAGEMENT_PLAN.md`, `E2_RECRUITMENT_TEXT.md`, `annotation_schema.json`,
`annotation_form_blank.csv`, `adjudication_log_template.csv`,
`HUMAN_VALIDATION_EXECUTION.md` (commands).

This plan exists because the paper's remaining gap is a **human-judged** one, and because
the cost of closing it has to be visible before anyone commits. All rates are placeholders
for the authors to fill; nothing here is a quote.

## 1. What the spend buys (claim-for-claim)

| Claim currently | Status | After a passing E2 |
|---|---|---|
| Role cues match expert spans at precision 0.610 / 0.807 (adjacent corpora) | adjacent-domain only | in-domain role precision/recall with confidence intervals |
| Typed edges/paths are formal structure proxies | construct validity explicitly **not** claimed | supported or refuted per edge type, with an error taxonomy |
| No-path C²GES is the provisional simpler default | internal evidence only | same recommendation with an independent human check of omission harm |
| "No path benefit" | statistical null + bound | null **plus** a human-judged taxonomy of what the path term changes |

Nothing in this plan upgrades a claim on its own: the gates in `ANNOTATION_PROTOCOL.md`
decide, and a failed gate forces a downgrade.

## 2. Sample design (arithmetic, not taste)

Half-width of a 95 % proportion interval at proportion `p`:

`n ≤ z²·p(1−p)/w²`, with `z = 1.96`:

| p | w = 0.05 | w = 0.08 | w = 0.10 | w = 0.12 |
|---|---|---|---|---|
| 0.5 | 385 | 151 | 97 | 67 |
| 0.6 | 369 | 145 | 93 | 65 |
| 0.7 | 323 | 127 | 81 | 57 |
| 0.8 | 246 | 97 | 62 | 43 |

Design decision: **150 units per role family** (“propagation”, “impact”, “mitigation”) was
**not** chosen; the affordable and defensible target is:

* **Tier A — minimum viable (recommended first):** 120 randomly sampled units from the frozen
  15-report test set, stratified across roles; expected half-width ≈ 0.09 at p = 0.7.
* **Tier B — publication grade:** 320 units (half-width ≈ 0.05), plus 60 typed edges/paths and
  40 omission decisions, which is the version that can carry a construct-validity sentence.

The schema already carries unit validity, role, edge direction, path plausibility, source
faithfulness and critical omission, so both tiers use the same form.

## 3. Effort model

Labelling rate assumption for long technical reports: **8–12 units/hour** per annotator
(each unit needs surrounding context; captions and table markers cost more).

| Work item | Tier A | Tier B |
|---|---|---|
| Training + calibration pilot (2 annotators) | 3 h × 2 = 6 h | 4 h × 2 = 8 h |
| Unit labelling (120 / 320 units at 10 units/h) | 12 h × 2 = 24 h | 32 h × 2 = 64 h |
| Edge/path and omission items (0 / 100 items at 15 items/h) | — | 6 h × 2 = 12 h |
| Adjudication (senior, domain-experienced) | 4 h | 8 h |
| Coordinator: sampling manifest, secure packets, script runs, QA | 6 h | 10 h |
| **Total person-hours** | **≈ 40 h** | **≈ 102 h** |

## 4. Cost lines (fill the rates)

| Line | Unit | Tier A | Tier B | Rate (author to fill) |
|---|---|---|---|---|
| Domain expert annotator | person-hours | 21 | 44 | ____ /h |
| Second annotator (may be non-expert) | person-hours | 18 | 42 | ____ /h |
| Adjudicator (≥ 5 y domain experience) | person-hours | 4 | 8 | ____ /h |
| Coordination + QA | person-hours | 6 | 10 | ____ /h |
| Participant compensation / honorarium | lump | 1 | 1 | ____ |
| Ethics review fee (if charged) | lump | 1 | 1 | ____ |
| **Total** | | | | ____ |

If the budget is zero, the honest alternative is **not** to relabel with an LLM: it is to keep
the current adjacent-corpus audit and the explicit “not expert gold” caveat, which the paper
already does.

## 5. Calendar (Tier A, ~6 weeks from a standing start)

| Week | Action | Gate |
|---|---|---|
| 1 | Submit ethics packet; confirm both annotators; freeze the sampling manifest (hash it) | ethics determination recorded |
| 2 | Training + calibration pilot on 20 units; freeze the rubric after any wording fix | pilot κ ≥ 0.6, else fix rubric and re-pilot |
| 3–4 | Independent blinded labelling of the 120 units | both annotation files complete, schema-valid |
| 5 | Pre-adjudication agreement; adjudication log; run `human_validation.py pre/final` | κ and per-role metrics produced |
| 6 | Claim-gate decisions; update the manuscript | gates in `claim_gate_decisions.json` |

## 6. Gates and downgrade rules

Reused verbatim from `ANNOTATION_PROTOCOL.md`; a miss downgrades the matching claim rather
than being written up as a partial success. The manuscript sentence to edit on a miss is
named in the layer table (L6 row) and in the Limitations paragraph.

## 7. Red lines

1. No LLM or author labels may be presented as independent human annotation; the authors may
   not serve as the two annotators.
2. No recruitment or data collection before the institutional ethics determination.
3. No freezing of the sampling manifest after outcomes are seen.
4. No “partial pass” language: each gate either holds or the claim is downgraded.
5. Annotator identity stays pseudonymous; consent and data-management documents travel with
   the packet, never into the release scope.
