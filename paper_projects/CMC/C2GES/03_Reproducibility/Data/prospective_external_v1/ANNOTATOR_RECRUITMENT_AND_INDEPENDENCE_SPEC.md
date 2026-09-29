# E2 annotator recruitment and independence specification

Status: action required from the authors/institution

## Minimum staffing

- Annotator A: documented experience in power-system operation, protection, reliability-event analysis, or technical incident investigation.
- Annotator B: an independent technical-document researcher or second domain expert trained on the frozen annotation guide.
- Neither annotator may be an LLM, the benchmark generator, or the person who produced the system predictions being scored.
- Both annotators work independently until the pre-adjudication agreement statistics are frozen.

## Required records

- Name or coded personnel identifier held privately by the institution.
- Qualification basis and relevant years or projects of experience.
- Conflict-of-interest declaration.
- Training date, guide version, and calibration-only examples used.
- Signed confidentiality/data-handling acknowledgement if restricted source text is shown.
- Independent annotation timestamps and immutable output hashes.

## Separation of duties

Annotators must not see condition names, model scores, the other annotator's labels, or the intended hypothesis during independent labeling. Adjudication starts only after raw agreement and confusion statistics have been generated. Adjudicated labels do not replace the pre-adjudication files.

## Acceptance gate

E2 cannot start until two named and authorized humans are assigned and the institution's ethics decision has been issued. Synthetic examples may support training, but labels on synthetic examples do not count toward the human-validity sample.
