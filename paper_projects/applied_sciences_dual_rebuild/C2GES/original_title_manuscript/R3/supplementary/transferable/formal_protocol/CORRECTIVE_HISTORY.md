# C2GES v0.3 Corrective History

- `diagnostic_build_06` and its builder-team audit are superseded and failed by
  `INDEPENDENT_STAGE1_AUDIT.md`. They must not be used as evidence of a clean
  dataset or as an input to development selection.
- `dev_selection_run01` is a retained timeout incident.
- `dev_selection_run02` is a retained interrupted incident (84/144 grid
  configurations recorded in its unchanged running state). It was stopped when
  the Stage-1 audit failed and is excluded from every result.
- The next permissible artifact is the immutable `diagnostic_build_07` produced
  after the page-count, summary-boundary, running-head, ambiguous-role, and
  typed-path work-limit corrections. Passing the builder-team structural audit
  does not replace the required fresh independent audit.
- `diagnostic_build_07` is retained as a failed diagnostic: its first
  implementation of the page-interval gate counted filtered page markers and
  running heads as reference content, excluding two otherwise valid reports.
  Its structural audit is preserved under
  `audits/diagnostic_build_07_structural_audit` with status `FAIL`.
- The corrected successor and final diagnostic candidate is
  `diagnostic_build_08`; no prior diagnostic directory is overwritten. It
  conservatively excludes `nerc_034` because the report transitions from its
  Executive Summary to an unnumbered report-specific title not accepted by the
  registered general chapter-heading rule. The retained set is therefore 27
  reports (12 development, 15 test), rather than reintroducing a document-level
  exception to recover one report.
- `dev_selection_run03` is a retained execution-window/orphan-process incident.
  The outer command timed out after its state first showed 12/144, but the
  child Python process remained alive contrary to the initial process check.
  The coordinating root independently verified that the orphan command line
  pointed only to run03 and terminated it; its last state then showed 120/144,
  `test_input_accessed=false`, and no ledger or decision. This directory and
  every partial computation associated with it are permanently excluded; it
  is not resumed, overwritten, or used for a decision. Incident classification:
  `orphan_process_detected_and_terminated_by_root`.
- The registered development grid contains **144**, as shown consistently by
  `candidates()` and the prior development run records. A coordinating oral
  instruction that said 192 was explicitly corrected before the new run; no
  grid point was added or removed. `dev_selection_run04` is authorized as a
  fresh complete execution of the same 144 records.
