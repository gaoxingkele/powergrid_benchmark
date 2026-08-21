# Independent Pre-Test Integrity Audit: C2GES v0.3

## Material Passport

- Artifact type: independent pre-test integrity audit
- Audit date: 2026-08-08 (Asia/Shanghai)
- Audited freeze: `C2GES-NERC-FORMAL-v0.3-PRETEST-20260808`
- Freeze-manifest SHA-256 at audit: `F70387B4605ACE3CB1219A6628A7025C220FBEC2296F541A68C0AEBAE0525BAE`
- Verification mode: read-only mechanical verification plus static code/protocol review
- Test-data boundary: the build08 test JSONL was not decoded or parsed; only its SHA-256, byte size, and binary LF count were obtained
- Formal-execution boundary: `run_test_v0_3.py` was not executed
- Verdict: **FAIL — DO NOT AUTHORIZE THE FORMAL TEST YET**

## 1. Scope and decision rule

This audit independently checked the manifest and its bound assets, the local
runtime and semantic-model snapshot, the development-selection ledger, the
registered conditions and statistical family, the strict counterfactual
ablation, baseline strength, incident isolation, failure preservation, relative
path semantics, and unbound execution dependencies. A PASS requires both
mechanical hash integrity and a closed, internally consistent scientific
protocol. Mechanical integrity alone is insufficient.

The freeze is correctly labelled a **post-audit corrective evaluation**, not a
fresh confirmatory or outcome-unseen test. The R1 test outcomes had already been
inspected. Nothing in a later execution may upgrade this evidence class.

## 2. Checks that passed

| Check | Independent result | Status |
|---|---:|---|
| Manifest itself | SHA-256 `F70387...25BAE` | PASS |
| Registered config | Actual `5E96EC...C95D4` equals manifest | PASS |
| Seven bound files | All present; all SHA-256 values equal manifest | PASS |
| Seven code files | All present; all SHA-256 values equal manifest | PASS |
| Test-only dataset | Actual `A9342B...D127` equals manifest; 2,354,058 bytes; 15 binary LF records | PASS |
| Combined/dev datasets | Actual hashes equal `87F7F7...AA15` / `27CE41...7F79` | PASS |
| Semantic model snapshot | Tree hash `62FFD0...DDF7`, 11 files, 91,578,415 bytes | PASS |
| Registered direct runtime | Python 3.12.10; NetworkX 3.6.1; NumPy 2.4.6; rouge-score 0.1.2; sentence-transformers 5.6.0; torch 2.13.0+cpu | PASS |
| Unit/regression tests | `python -m unittest discover -s R2_v0_3 -p test_*.py -q`: 22 run, 22 passed | PASS |
| Development grid size | 144 ledger rows; 144 unique indices; contiguous 0--143 | PASS |
| Grid reconstruction | Independent Cartesian-product reconstruction produced 144 candidates in the same order | PASS |
| Winner reconstruction | Registered rule independently selects index 60; byte-level selected object equals decision | PASS |
| Formal config vs winner | Weights, penalty, distance, and path lengths all equal run04 winner | PASS |
| Development boundary record | run04 is COMPLETE 144/144 and records `test_input_accessed=false` | PASS, with evidence limitation below |
| run03 isolation | Only `run_state.json`; retained RUNNING 120/144; no ledger/decision; distinct directory and timestamps | PASS |
| Conditions | Seven registered conditions appear in identical order in config and runner | PASS |
| Primary family | Three ROUGE-L contrasts x two budgets = six tests | PASS |
| Holm implementation | Deterministic step-down adjustment across the six-record list | PASS |
| Strict no-CF implementation | Only the CF coefficient changes from 0.15 to 0.0; other coefficients and redundancy penalty remain unchanged; no renormalization | PASS |
| Output collision guard | Runner refuses an already-existing output directory | PASS |
| Failure materialization | After output creation, exceptions produce retained `failure.json` and failed `run_state.json` | PASS |

The selected development statistics were also reproduced from the ledger:
ROUGE-L@5 `0.11951259817416543`, ROUGE-1@5
`0.2713870157276585`, negative redundancy
`-0.07882377312696708`, and full-minus-strict-no-CF ROUGE-L@5
`-0.005665215823945863`. The negative CF contrast remains evidence against a
development-set benefit and must be reported without reinterpretation.

## 3. Blocking findings

### B1. The promised strong semantic baseline is not implemented

The R1 revision-response matrix registers primary comparison against
**Semantic-MMR** and says to add Semantic-MMR if local model support passes.
Local MiniLM support does pass, but the frozen condition is instead
`semantic_centroid`, which independently ranks sentences by centroid similarity
and has no MMR diversity term. This is not a naming difference. It gives the
full method a redundancy-aware selection mechanism while the semantic comparator
lacks the corresponding diversity control, weakening and confounding the main
semantic comparison.

Required correction: implement and test a frozen Semantic-MMR comparator,
preferably replacing `semantic_centroid` so the seven-condition design and the
six-test primary family remain unchanged. Register its relevance/diversity
formula, lambda, deterministic tie-breaking, and budget handling before any
formal test. Update the response matrix or satisfy it; do not silently treat
semantic centroid as Semantic-MMR.

### B2. `test_files` have ambiguous paths and are outside runtime verification

The four `test_files` paths are bare filenames. They resolve successfully only
when the manifest directory is used as the implicit base; they are missing when
resolved from the repository root, unlike every `bound_files` and `code_files`
entry. The manifest does not declare that base. More importantly,
`verify_freeze()` never iterates over `test_files`, so a test file can change
without formal-run freeze verification failing.

Required correction: use repository-relative paths (or declare and enforce a
single manifest-relative base), and make a pre-run verifier check all four test
hashes. The formal runner need not execute tests, but the audited freeze closure
must not silently ignore them.

### B3. Registered CF work-limit settings are not consumed by the runner

`formal_config_v0_3.json` registers `path_min_edges`, `path_max_paths`, and
`path_max_expansions`. The runner passes only `path_max_edges` to
`score_channels`; `score_channels` hard-codes `min_edges=2`, and the CF function
uses its source-code defaults of 250,000 paths and 2,000,000 expansions. Those
defaults currently equal the config, so present behavior happens to match, but
the claimed configuration-to-runner binding is not real and cannot be validated
by changing a config field.

Required correction: thread all four registered path parameters through
`run_test_v0_3.py` -> `score_channels()` ->
`path_counterfactual_sensitivity()` -> `qualified_typed_paths()`, and add a
regression test proving each work limit is operative and fails closed.

### B4. The runtime closure omits output-relevant transitive packages

The direct package versions match, but transformer inference and stemming also
depend on unregistered packages. The current environment includes at least
`transformers 5.14.1`, `tokenizers 0.22.2`, `nltk 3.10.0`, `scipy 1.18.0`,
`scikit-learn 1.9.0`, `huggingface-hub 1.24.0`, and `safetensors 0.8.0`.
Changes to tokenization, model loading, numerical operations, or stemming can
change sentence embeddings or ROUGE values while every presently registered
runtime check still passes.

Required correction: bind and verify an output-relevant dependency lock/snapshot
(at minimum the listed packages), or bind a complete environment lock with a
hash. Retain the model tree hash.

### B5. The one-shot rule is documentary, not enforced across output directories

The runner refuses reuse of one output path and preserves a failure after that
directory is created. It does not prevent a second physical execution using a
different new output directory, and it does not inspect a run registry or
authorization artifact. Thus `permitted_runs: 1` and `rerun_after_success:
forbidden` cannot be inferred from runner behavior.

Required correction: bind a canonical output root and a durable run-attempt
registry/lock outside the attempt directory, recording the attempt before test
content is decoded. Any existing attempt, whether COMPLETE or FAILED, must stop
a new call pending a new freeze and explicit authorization. A separate signed or
hashed authorization record may remain an operational prerequisite.

## 4. Evidence limitations and leakage assessment

- `test_input_accessed=false` is supported by the run04 state and decision, by
  the dev-only input path/hash, and by static inspection of the development
  selector. It is still a self-recorded process fact, not an operating-system
  access trace. The audit therefore does not elevate it to cryptographic proof.
- The development winner is independently reproducible from the 144-row ledger.
  This audit did not rerun development selection or read the test JSONL.
- The formal test JSONL was treated as opaque bytes. Its 15 binary LF records
  corroborate the registered physical row count without exposing row content.
- Earlier R1 test reports and results were already inspected by the project.
  Consequently, the v0.3 evaluation can only be reported as post-audit
  corrective/descriptive evidence even after all blockers are repaired.
- The semantic baseline choice is especially sensitive to prior knowledge.
  Replacing centroid with the comparator already promised in the pre-existing
  R1 response matrix reduces discretion; it does not restore confirmatory
  status.

## 5. Authorization recommendation

**Do not authorize or execute `run_test_v0_3.py` under manifest SHA-256
`F70387B4605ACE3CB1219A6628A7025C220FBEC2296F541A68C0AEBAE0525BAE`.**

A successor freeze may be eligible for a new independent pre-test audit only
after B1--B5 are corrected, all affected code/config/test hashes are regenerated,
the full regression suite passes, and the successor manifest binds the complete
closure. The old manifest and this FAIL report must remain preserved. No formal
test execution occurred during this audit.
