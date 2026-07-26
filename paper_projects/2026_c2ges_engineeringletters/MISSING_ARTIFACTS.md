# MISSING_ARTIFACTS — files to supply from the original experiment machine

The original C2GES experiment workspace
(`.../paper_workspace/workspaces/c2ges-causal-mechanism-ieeeaccess/`, previously at
`/media/lenovo/data2/cja/GridMind/references/AutoResearchClaw/paper_workspace/workspaces/c2ges-causal-mechanism-ieeeaccess`)
is **not in this repository**. Without it, no new baseline results can be produced.
This is the exact request list; each item says what it unlocks and where to put it.

Exact original-machine paths recorded inside the in-package supplement
(`source/supplement/bm25_k_sensitivity/summary.json`, run 2026-06-26T16:01:35Z,
git sha `08fd42f972b2a8c3cca254aadb5c2d8a7259c807`):

- Run workspace: `/media/lenovo/data2/cja/GridMind/references/AutoResearchClaw/paper_workspace/workspaces/c2ges-causal-mechanism-ieeeaccess`
- Dataset used by the run: `<workspace>/verification_pilot/agent_audit_40doc`
- Raw dataset asset root (`dataset.source_asset_root` — note this is a **different
  workspace**, the evidence-audit one): `/media/lenovo/data2/cja/GridMind/references/AutoResearchClaw/paper_workspace/workspaces/c2ges-evidence-audit-krill/datasets/gridmaint_causalsum_pilot/processed`
- Executor artifact dir: `<workspace>/post_freeze_revisions/role_selective_graph_gate/experiment_outputs/c2ges_role_selective_graph`

## 0. Already evidenced IN-PACKAGE — do NOT re-request

`source/supplement/bm25_k_sensitivity/summary.json` is the paper's main K=3 run for
seven conditions (verified programmatically by
`source/code/analyze_supplement_evidence.py`, output
`source/supplement/bm25_k_sensitivity/derived_tables.{json,md}`; 105/109 manuscript
cross-checks match exactly). It already evidences:

- Table 3 rows for TF-IDF query, BM25 query, SBERT query, full C2GES (all mean ± std
  cells for F1/precision/recall/ROUGE-L).
- Section 6.2 ablation aggregates (query-only 0.2152, no-role 0.2295, no-graph 0.2923)
  and therefore the mean differences of Table 4's ablation rows.
- Table 4's three baseline rows (vs TF-IDF / BM25 / SBERT): mean diffs exactly; the
  supplement's independently seeded bootstrap (seed 20260626) reproduces the TF-IDF and
  SBERT CI endpoints to within 0.002 (the 4 non-matching cross-checks, all seed-level).
- The full K∈{1,3,5} sensitivity table and all nine baseline paired comparisons.
- All role-stratified tables (per-role full metrics, per-role BM25/NoRole comparison,
  role-wise graph-gate deltas) — the deltas recompute exactly.
- Dataset lineage/verification counts now cited in §3 of the paper (25→40 docs, 15 new
  docs verified 6 pass / 8 minor-repair / 1 answer-narrowed, 5 verifier batches failed
  with HTTP 429 then rerun sequentially, 0 schema errors, 1 low-diversity flag).

Base drop location in this repo:
`paper_projects/2026_c2ges_engineeringletters/workspace/` (create it; referred to as `<workspace>/` below).
After copying, run everything with `--workspace <workspace>` or `export C2GES_WORKSPACE=<workspace>`.

## 1. Benchmark dataset (highest priority — blocks everything)

| Supply | Put at |
|---|---|
| `verification_pilot/agent_audit_40doc/` — all `nerc_*.json` (40 docs, 200 questions, 608 evidence IDs) plus `manifest.json` if present | `<workspace>/verification_pilot/agent_audit_40doc/` |

Unlocks: running ALL prepared baselines (P1-7/G3), the human-gold subset sampling
(P1-8/G4), public dataset release (P1-6/G1), and any reproduction of the paper's numbers.

## 2. Validated pilot scripts + config (blocks `source/code/main.py`)

| Supply | Put at |
|---|---|
| `verification_pilot/scripts/run_baselines.py` | `<workspace>/verification_pilot/scripts/run_baselines.py` |
| `verification_pilot/scripts/run_c2ges.py` | `<workspace>/verification_pilot/scripts/run_c2ges.py` |
| `three-pack/config.yaml` | `<workspace>/three-pack/config.yaml` |

Unlocks: full reproduction run of `source/code/main.py` (all conditions, ablations,
CV protocol, bootstrap statistics) — reviewer-facing reproducibility (P0/G2).
Note: the prepared baselines in `source/code/prepared_baselines/` need only item 1,
not item 2.

## 3. Main Executor artifacts (P0-4 — evidence completeness for numbers already in the paper)

From `post_freeze_revisions/role_selective_graph_gate/experiment_outputs/c2ges_role_selective_graph/`
(or `experiment_outputs/c2ges_executor_iterated/`, whichever the manuscript run used):

Narrowed scope (see §0): the BM25 supplement now in-package-evidences the four
query-retrieval rows of Table 3, all ablation aggregates/mean-diffs, the K-sensitivity
table, and all role-stratified numbers. What §3 below still uniquely evidences:

- Table 3's five weak-baseline rows (Lead 0.0545, TF-IDF centroid 0.0688, TextRank
  0.0700, LexRank 0.0167, Causal trigger 0.1071).
- Table 4's CI/p values for the four ablation/legacy rows (query-only, no-role,
  no-graph +0.0060 [0.0014, 0.0119] p=0.0254, fixed-legacy +0.0403) — mean diffs of the
  first three are derivable in-package, CIs and p-values are not.
- The fixed-legacy condition entirely (not present in the supplement).
- The exact Executor-seed CI endpoints of Table 4's TF-IDF/SBERT rows (supplement
  reproduces them only to within 0.002 under its own seed).
- cv_protocol.json's 5-fold selection record and the qualitative case studies.

| Supply | Put at | What it evidences |
|---|---|---|
| `summary.json` | `source/supplement/c2ges_role_selective_graph/summary.json` | Table 3's five weak-baseline rows, Table 4's four ablation/legacy paired CIs/p-values, the fixed-legacy condition, and the Executor-seed CI endpoints of Table 4's TF-IDF/SBERT rows |
| `details.jsonl` | `source/supplement/c2ges_role_selective_graph/details.jsonl` | All four qualitative case studies in Section 7 (nerc_014 impact F1 0.667, nerc_009 root_cause, nerc_012 trigger, nerc_001 impact); also serves as `--reference-details` for paired comparisons in the prepared baselines |
| `cv_protocol.json` | `source/supplement/c2ges_role_selective_graph/cv_protocol.json` | The document-level 5-fold selection of w=(0.52, 0.40, 0.08) and the role_gated_chain family |
| `heldout_predictions.jsonl` | `source/supplement/c2ges_role_selective_graph/heldout_predictions.jsonl` | Held-out full and fixed-legacy predictions cited in Sections 3 and 5 |
| `metadata.json` (if present) | `source/supplement/c2ges_role_selective_graph/metadata.json` | Command lines, dependency status, label-provenance record |

Unlocks: closes the remaining P0-4 evidence-completeness gap flagged in
PUBLICATION_ASSESSMENT.md §2 items 13/17/18. After the 2026-07 supplement analysis
(§0 above), the classes of published numbers resting only on REVISION_NOTE.md
cross-references are reduced to: weak-baseline rows, ablation/legacy CIs and
p-values, the fixed-legacy condition, and the §7 qualitative cases.

## 4. What each unlock enables next (run order once files arrive)

1. **P0-4** — drop item 3 into `source/supplement/` (no code needed; pure evidence packaging).
2. **P1-7 baselines** — with item 1 (+ optionally item 3's `details.jsonl` for paired stats):
   ```
   cd source/code/prepared_baselines
   python run_crossencoder_baseline.py --workspace <workspace> --out-dir out/crossencoder --reference-details ../../supplement/c2ges_role_selective_graph/details.jsonl
   python run_bge_reranker.py         --workspace <workspace> --out-dir out/bge          --reference-details ../../supplement/c2ges_role_selective_graph/details.jsonl
   python run_llm_zeroshot_baseline.py --model <model> --base-url <url> --api-key-env <VAR> --workspace <workspace> --out-dir out/llm_zeroshot --reference-details ../../supplement/c2ges_role_selective_graph/details.jsonl
   ```
3. **P1-8 gold subset** — with item 1, sample 50–100 questions for dual expert annotation
   (Cohen's kappa + agent-label agreement), as pre-announced in the manuscript's new
   Section 4 circularity subsection and Limitations.
4. **P1-6 release** — with item 1 (and ideally item 3), publish dataset + artifacts to
   GitHub/Zenodo and fill the `[TODO]` in the manuscript's Data Availability section.

## Not needed

- The frozen `deliverables/` package (superseded by the post-freeze revision).
- `pipeline/runs/` intermediate stages other than the artifacts named above.
- GPU hardware: the prepared cross-encoder/BGE baselines run on CPU; the LLM baseline
  needs only an OpenAI-compatible endpoint.
