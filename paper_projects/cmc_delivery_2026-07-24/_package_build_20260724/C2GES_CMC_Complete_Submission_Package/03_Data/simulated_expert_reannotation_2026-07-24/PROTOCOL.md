# Simulated-Expert Reannotation Protocol (75 Questions)

## Status and disclosure

This study uses three AI agents configured to simulate complementary expert
review perspectives. They are not human annotators and must never be described
as human experts or as producing human-gold labels. The resulting labels are
`simulated_expert_adjudicated` labels.

## Frozen subset

The subset contains all five role-conditioned questions from the 15 documents
listed as `new_documents` in the 40-document manifest (75 questions total).
This subset is frozen before annotation and is not selected using model scores.

## Blinding

Annotators receive only:

- document identifier, title, and source URL;
- the sentence-ID/text sequence;
- question identifier, causal role, and question text.

They must not inspect the original `answer`, `evidence_sentence_ids`, notes,
role-cue lexicons, manuscript results, or another annotator's output.

## Role definitions

- `trigger_event`: the initiating action, fault, trip, outage, or condition
  that starts the event described by the question.
- `root_cause`: the underlying equipment, protection, planning, procedural,
  organizational, or environmental cause that explains why the event occurred.
- `propagation_or_response`: how the disturbance spread or how protection,
  operators, controls, or the grid responded after initiation.
- `impact`: measurable or concrete consequences for load, generation,
  customers, equipment, reliability, or service.
- `mitigation`: restoration, corrective action, recommendation, repair,
  prevention, training, operating adjustment, or other risk-reduction action.

## Evidence-selection rules

1. Select the smallest set of sentences that directly and jointly answers the
   question for the specified role.
2. Select 1--4 sentence IDs. Prefer 1--3; use 4 only when the answer genuinely
   requires a multi-step chain.
3. Do not select a sentence merely because it shares topic words.
4. Prefer explicit statements over inferred or neighboring context.
5. Do not import facts absent from the provided sentence sequence.
6. If the question is not answerable from the provided text, return an empty
   evidence list and set `answerable` to `false`.
7. Treat sentence boundaries as fixed; select the exact IDs that contain the
   support.
8. Do not force agreement with the question's presupposition. Note ambiguity
   or an invalid premise in the rationale.

## Required output

Write one UTF-8 JSON object per line with these fields:

```json
{
  "qid": "document::role",
  "role": "impact",
  "evidence_sentence_ids": ["s001", "s010"],
  "answerable": true,
  "answer_summary": "Concise evidence-grounded answer.",
  "confidence": 0.90,
  "rationale": "Why these exact sentences are necessary and sufficient.",
  "annotator_id": "simexpert_A"
}
```

Confidence must be between 0 and 1. Preserve the packet order and produce
exactly 75 records.
