# Design changelog: v1 freeze to v2 re-audit draft

The v1 frozen states and artifacts remain intact under `states/` and
`PROTOCOL_FREEZE_DRAFT.json`. No unfavorable v1 operator family was removed.
The v2 Stage A reproduces all six v1 perturbation families and adds the whole
schema-risk families required by the independent NO-GO audit.

The first v2 gold-only coverage pass reached 176/180 and is preserved under
`pre_score_v2/`. A versioned, whole-family revision added a lifecycle-state
sentinel, a uniform half-day calendar grid over the schema-derived date
envelope, and an independent all-category isolated-parent state. It did not
inspect or respond to any model SQL or collision flag. The resulting v2b design
reached 180/180 gold-denotation change coverage and broke all five snapshot-empty
denotations in at least two states.

Gold coverage was used only to decide GO/hold status for the general design.
It was not used to remove a state, select favorable model results, or construct
candidate-specific counterexamples. The experiment remains a retrospective
robustness reanalysis because the archived predictions predate this protocol.

