# Independent Pre-Test Integrity Audit: C2GES v0.3.1

## Material Passport

- Artifact type: fresh independent pre-test integrity audit
- Audit date: 2026-08-08 (Asia/Shanghai)
- Audited freeze: `C2GES-NERC-FORMAL-v0.3.1-PRETEST-20260808`
- Freeze-manifest SHA-256: `DE3205B0BC8DF65706B40B696F7313953E5905AA875128B569EECB685DAB19B5`
- Predecessor freeze SHA-256: `F70387B4605ACE3CB1219A6628A7025C220FBEC2296F541A68C0AEBAE0525BAE`
- Verification mode: independent hash/metadata verification, static source review, isolated helper checks, and the complete frozen unit/regression suite
- Test-data boundary: the test JSONL was never decoded or parsed; only SHA-256, byte size, and binary LF count were read
- Formal-execution boundary: `run_test_v0_3_1.py` was not executed as a formal run, and no prediction was generated
- Verdict: **PASS — eligible for one hash-bound author authorization**

## 1. Decision

All five blockers in `INDEPENDENT_PRETEST_AUDIT_v0_3.md` are closed in the
successor freeze. The frozen assets, runtime closure, formal runner, test suite,
and current filesystem state support issuing exactly one authorization that
binds this freeze hash, a machine-readable PASS decision for this hash, one
valid run id, and its canonical output path.

This PASS does not authorize execution by itself. The evidence class remains
`post_audit_corrective_descriptive_not_fresh_confirmatory`; the earlier R1 test
inspection cannot be reversed by this repair or by the later run.

## 2. Independent mechanical verification

| Check | Independent result | Status |
|---|---:|---|
| Successor manifest | 14,332 bytes; SHA-256 `DE3205...19B5` | PASS |
| Bound files | 14/14 present; paths remain below repository root; byte sizes and SHA-256 values match | PASS |
| Code files | 9/9 present; paths remain below repository root; byte sizes and SHA-256 values match | PASS |
| Test files | 5/5 present; full repository-relative paths; byte sizes and SHA-256 values match | PASS |
| Opaque test dataset | 2,354,058 bytes; SHA-256 `A9342B...D127`; 15 binary LF records | PASS |
| Frozen semantic model | SHA-256 tree `62FFD0...DDF7`; 11 files; 91,578,415 bytes | PASS |
| Dependency lock | 46 packages; Python 3.12.10; every installed version matches | PASS |
| Independently reconstructed dependency closure | Exact equality with the 46-package lock; no active required dependency missing | PASS |
| Runner's own freeze verification | 77 checks passed; model file count 11 | PASS |
| Frozen regression command | 29 tests run; 29 passed; 0 failures/errors | PASS |
| Predecessor v0.3 freeze | SHA-256 still `F70387...25BAE`; all predecessor bound/code/test entries remain unchanged | PASS |
| Current authorization artifact | Absent | PASS |
| Current durable registry | Absent | PASS |
| Current canonical output root | Absent | PASS |
| Formal runner process | No `run_test_v0_3_1.py` process found | PASS |

The unit suite was executed from the manifest directory with the registered
command:

```text
python -m unittest discover -s . -p test_*.py -q
Ran 29 tests in 1.144s
OK
```

No test invoked the formal runner entry point or decoded the frozen test input.

## 3. Closure of the five predecessor blockers

### B1 — Semantic-MMR: closed

The seven frozen conditions are, in order, `lead`, `centroid`, `textrank`,
`semantic_mmr`, `role`, `graph_no_cf_strict`, and `c2ges_full`.
`semantic_mmr_select()` implements greedy MMR as

```text
0.5 * cosine(sentence, normalized document centroid)
- 0.5 * max cosine(sentence, already selected sentence)
```

Both relevance and redundancy use the same normalized, frozen MiniLM embedding
matrix. The lambda is fixed at 0.5 and is neither a development-grid parameter
nor a test-informed selection. The semantic comparator therefore has an
explicit semantic diversity control rather than the former centroid-only
ranking. Budget truncation and the tie order (adjusted score, earlier document
position, then lexicographically larger sentence id) are deterministic. A
synthetic regression independently selects the non-duplicate second sentence,
confirming that the redundancy term is operative.

### B2 — complete test-file paths and runtime verification: closed

All five test entries use repository-relative paths. `resolve_repo()` resolves
and rejects paths outside the repository. `verify_freeze()` iterates over
`bound_files`, `code_files`, and `test_files`; a changed test hash therefore
stops the run before authorization or test decoding. The corresponding
mutation regression passed.

### B3 — explicit counterfactual work limits: closed

The runner reads and passes all four registered fields:
`path_min_edges`, `path_max_edges`, `path_max_paths`, and
`path_max_expansions`. `score_channels()` passes all four explicitly to
`path_counterfactual_sensitivity()`, which passes them explicitly to
`qualified_typed_paths()`. The v0.3.1 call chain has no hidden work-limit
defaults. Independent AST inspection found exactly these four keyword arguments
at the formal runner call site. Behavioral tests demonstrated that both edge
limits change accepted path lengths and that path-count and expansion-count
excesses raise `PathEnumerationLimitError` fail-closed.

### B4 — output-relevant dependency closure: closed

`OUTPUT_DEPENDENCY_LOCK_v0_3_1.json` binds Python plus the recursive installed
`Requires-Dist` closure of NetworkX, NumPy, rouge-score,
sentence-transformers, and torch with environment markers evaluated and extras
disabled. Independent reconstruction produced exactly the same 46 package/name
versions and found no missing active requirement. The runner verifies every
locked package version, the lock-file hash, and the frozen model tree before
authorization.

### B5 — one-shot execution enforcement: closed

The formal control sequence is, in source order:

1. `verify_freeze()` (line 408);
2. exact config/test path checks and config validation;
3. `verify_authorization()` (line 416);
4. `reserve_attempt()` (line 419);
5. canonical output collision handling and retained state creation;
6. test decoding through `jsonl()` (line 430).

Authorization must bind the exact current freeze hash, PASS decision path and
hash, run id, canonical output path, approver, approval timestamp, and
`authorized: true`. The fixed registry directory is created atomically before
test decoding. An existing directory blocks every later reservation, including
an empty crash placeholder and attempts that choose another CLI output.
CLAIMED/FAILED/COMPLETE states are therefore all terminal under this freeze.

The bundled authorization test had a combined name and exercised the bad-audit
path before its output mismatch could be isolated. To rule out that potential
false positive, this audit independently constructed a temporary, otherwise
valid authorization: a wrong output was rejected specifically with `CLI output
is not the authorized canonical output`; the correct canonical output was
accepted; the first reservation recorded `CLAIMED` with
`test_content_decoded=false`; and a second reservation was rejected. No formal
data were involved in this helper check.

## 4. Seven conditions and six-test Holm family

The config, manifest, runner constant, dispatch code, and statistical loop agree
on seven conditions and two budgets (K=5 and K=10). The primary family contains
exactly six ROUGE-L comparisons:

- full minus strict no-CF, at K=5 and K=10;
- full minus Semantic-MMR, at K=5 and K=10;
- full minus TextRank, at K=5 and K=10.

`holm_adjust()` applies a deterministic step-down maximum across all six raw
bootstrap p-values and records `holm_family_size=6`. An independent known-vector
check produced adjusted values 0.006, 0.05, 0.12, 0.12, 0.40, and 0.80 in raw-p
order, consistent with Holm adjustment. No condition or comparison is selected
after test access.

## 5. Bypass and false-positive review

- No alternative output argument bypasses the authorization because both the
  authorized relative output and resolved CLI output must equal the canonical
  `root/run_id` path.
- No alternative authorization path is accepted; it must equal the one frozen
  artifact path.
- No substitute PASS file is accepted without both its current SHA-256 and this
  freeze hash matching the authorization and decision contents.
- No second directory can obtain a physical attempt because the durable
  registry path is independent of output path and fixed by the freeze.
- A crash after registry-directory creation but before `attempt.json` creation
  still leaves the directory present and therefore consumes the single attempt.
- Test mutation, code mutation, config mutation, lock mutation, package-version
  drift, or model-tree drift fails before reservation and decoding.
- The regression suite contains helper-level mocks, so it is not taken alone as
  proof. The PASS rests additionally on direct hash reconstruction, independent
  dependency-closure reconstruction, static call-chain inspection, and isolated
  authorization/registry checks.

No runner bypass or blocking test false positive was found within the frozen
execution interface.

## 6. Authorization recommendation

**Recommendation: the root agent may now prepare one explicit author
authorization for successor freeze SHA-256
`DE3205B0BC8DF65706B40B696F7313953E5905AA875128B569EECB685DAB19B5`.**

Before execution, create a machine-readable independent decision containing at
minimum:

```json
{
  "verdict": "PASS",
  "freeze_sha256": "DE3205B0BC8DF65706B40B696F7313953E5905AA875128B569EECB685DAB19B5"
}
```

The later author authorization must bind that decision file's exact path and
SHA-256 and every other field required by the freeze. Only the canonical output
for the authorized run id may be passed. If a registry or output appears before
authorization, if any frozen hash changes, or if the runtime check fails, do not
execute; create and independently audit a new freeze instead. Preserve all
failed or completed artifacts without retry, overwrite, deletion, or resume.

