# C2GES diagnostic submission route decision

Date: 2026-09-12

## Decision

The submission is bounded to a diagnostic, non-confirmatory study. The title,
abstract, research questions, contribution claims, conclusions, ethics
statement, and data-availability statement must consistently reflect that
route.

## Evidence boundary

- The seven-series external pilot is post-access and exploratory. It is not an
  untouched external test and must never be relabeled as one.
- DeepSeek and Codex supplied machine labels for error discovery. They are not
  human participants, independent annotators, domain experts, or adjudicators.
- No human subjects were recruited and no human annotations were collected for
  the reported study. Institutional review is therefore not claimed for a
  nonexistent human study. A future human study requires its own institutional
  determination before recruitment.
- The controlled AB/RP/G experiment is reported as exploratory mechanism
  diagnosis. It supports negative or uncertain component findings, not a
  confirmatory performance claim.

## Submission consequence

The original 42-item gate was written exclusively for the stronger
confirmatory route. Its missing E1/E2 files and frozen-state requirements are
not silently waived or populated with synthetic substitutes. They are marked
not applicable to this diagnostic route in an item-level disposition ledger.
The confirmatory checker remains fail-closed and should continue to reject the
current package.

The diagnostic route is submission-ready only if its separate checker reports
zero findings, the public verifier passes in diagnostic mode, and all cited
evidence is hash-locked with the compiled manuscript.

## Final requirement resolution

For the current title and bounded claims, E1 is satisfied as explicitly
post-access exploratory evidence, E3 is complete exploratory mechanism diagnosis,
and E2/E4/E5 are not applicable because the manuscript makes no human-validation,
operational-benefit, or maintenance-generalization claim. No human participants
were recruited, so the current computational study reports institutional review
as not applicable; an institutional determination becomes mandatory before any
future human recruitment. The former confirmatory findings are future claim-upgrade
requirements, not current submission blockers. This resolution is machine-checked
in `CURRENT_SUBMISSION_REQUIREMENTS_RESOLUTION.json`.
