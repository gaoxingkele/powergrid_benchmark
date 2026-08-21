# Response to Independent Pre-Test Audit: v0.3 to v0.3.1

## Material Passport

- Artifact: prediction-test repair response
- Predecessor audit: `INDEPENDENT_PRETEST_AUDIT_v0_3.md`
- Predecessor verdict: FAIL; permanently unauthorized and excluded
- Successor: `C2GES-NERC-FORMAL-v0.3.1-PRETEST-20260808`
- Test-data boundary: the 15-report test file was not decoded or parsed during
  repair; only its already registered pathname, byte-level hash, and metadata
  are carried forward
- Formal execution: not performed
- Current gate: **AWAITING FRESH INDEPENDENT PRE-TEST AUDIT; UNAUTHORIZED**

## Point-by-point response

| Audit blocker | Repair | Verification evidence |
|---|---|---|
| B1: semantic comparator lacked MMR diversity | `semantic_mmr` replaces `semantic_centroid`. It greedily maximizes `lambda*cos(sentence, centroid) - (1-lambda)*max_cos(sentence, selected)` with lambda 0.5. Both terms use the same normalized frozen MiniLM vectors. Tie-breaking and budget behavior are deterministic. | `test_semantic_mmr_uses_minilm_space_for_relevance_and_redundancy`; config retains seven conditions and primary family size six. |
| B2: ambiguous test paths and no test-file runtime verification | Every test path is repository-relative. `verify_freeze()` resolves only below repository root and hashes every entry in `bound_files`, `code_files`, and `test_files`. | `test_verify_freeze_checks_test_files_as_repo_relative_paths` mutates a temporary test file and proves verification fails. |
| B3: three registered CF work settings were not consumed | All four fields are explicit parameters from config through runner, `score_channels`, counterfactual sensitivity, and path enumeration. No work-limit defaults remain in the v0.3.1 path module. | Mock-based end-to-end argument test plus behavioral tests for min edges, max edges, maximum path count, and maximum expansion count. Limit excess raises `PathEnumerationLimitError`. |
| B4: output-relevant transitive packages were unbound | `OUTPUT_DEPENDENCY_LOCK_v0_3_1.json` recursively records installed `Requires-Dist` closure for the five direct output roots with active environment markers, including transformers, tokenizers, NLTK, SciPy, scikit-learn, Hugging Face Hub, and safetensors. Runner checks every locked version and the lock-file hash. | Freeze verification binds the lock, Python version, semantic-model tree, and every locked package version. |
| B5: documentary one-shot rule | Authorization must bind exact freeze hash, independent PASS decision hash, unique run id, canonical output, approver, and time. An atomic registry directory is claimed before test decoding. Existing CLAIMED, FAILED, or COMPLETE registry state forbids another attempt, even with a different output CLI argument. | Temporary-directory regression tests verify authorization/output/audit mismatches fail and a second reservation fails. Runner durably updates the registry on success or failure. |

## Protocol continuity and discretion control

The full-method development choice was not reopened. Semantic-MMR lambda was
not optimized on development or test data: 0.5 is frozen as a symmetric fixed
balance required to implement the comparator already promised in the R1
response. Conditions remain seven; primary contrasts remain three at K=5 and
K=10; Holm family size remains six. The semantic primary contrast alone changes
from the non-MMR centroid comparator to the promised Semantic-MMR comparator.

## Required next action

A fresh agent must independently audit the successor manifest, source and test
hash closure, dependency lock, path-parameter operability, Semantic-MMR formula,
authorization schema, and durable registry behavior without decoding the test
JSONL or executing the formal runner. Only a PASS decision file binding the
successor freeze SHA-256 can be referenced by a later author authorization.

