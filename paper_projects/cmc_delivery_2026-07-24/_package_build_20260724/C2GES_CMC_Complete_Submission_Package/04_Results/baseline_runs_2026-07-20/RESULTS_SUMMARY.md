# Baseline Runs 2026-07-20 — Results Summary

Runs executed on the newly placed original workspace
(`paper_projects/2026_c2ges_engineeringletters/workspace/`, dataset
`verification_pilot/agent_audit_40doc/`: 40 docs / 2940 sentences / 200
questions / 608 evidence IDs, `manifest.json` present). All three prepared
baselines (`source/code/prepared_baselines/`) ran end-to-end with the paper's
protocol: K=3 budget, same metrics imported from `main.py`, document-cluster
bootstrap (seed 202502, 10000 samples), paired comparisons vs the Executor
`details.jsonl` (`source/supplement/c2ges_role_selective_graph/details.jsonl`).

- Interpreter: `C:\Users\10175\AppData\Local\Programs\Python\Python312\python.exe`
  (torch 2.13.0+cpu; sentence-transformers 5.6.0 installed for this run). CPU only.
- Outputs: `crossencoder/`, `bge_reranker/`, `llm_zeroshot_deepseek/` (each with
  `summary.json` + `details.jsonl`; run logs `*_run.log` alongside).
- All 200 questions scored `ok` in every run; every prediction respected K=3.

## 1. New baseline results vs paper conditions (K=3, evidence metrics, mean over 200 questions)

| Method | Evidence F1 | Precision | Recall | ROUGE-L | Source |
|---|---|---|---|---|---|
| Lead sentence selector | 0.0545 | 0.0533 | 0.0592 | 0.1822 | Executor artifact |
| SBERT query retrieval | 0.1972 | 0.1883 | 0.2329 | 0.3067 | Executor artifact |
| TF-IDF query retrieval | 0.2122 | 0.2050 | 0.2471 | 0.3224 | Executor artifact |
| BM25 query retrieval | 0.2273 | 0.2217 | 0.2575 | 0.3247 | BM25 supplement |
| **BGE reranker (BAAI/bge-reranker-base)** | **0.2604** | 0.2517 | 0.3013 | 0.3490 | this run |
| **Cross-encoder (ms-marco-MiniLM-L-6-v2)** | **0.2787** | 0.2717 | 0.3188 | 0.3667 | this run |
| Full C2GES reranker | 0.2983 | 0.2950 | 0.3325 | 0.3732 | Executor artifact |
| **LLM zero-shot (deepseek-chat, temp 0)** | **0.5887** | 0.5950 | 0.6342 | 0.5942 | this run |

Document-level bootstrap 95% CIs on own evidence F1 (10000 samples):
cross-encoder [0.2492, 0.3095]; BGE [0.2278, 0.2946]; LLM [0.5569, 0.6182].

## 2. Paired document-cluster bootstrap vs c2ges_full (delta = baseline − c2ges_full, evidence F1)

| Baseline | Mean diff | 95% CI | p | Verdict |
|---|---|---|---|---|
| Cross-encoder MiniLM | −0.0196 | [−0.0539, +0.0140] | 0.2464 | C2GES ahead, **not statistically significant** |
| BGE reranker base | −0.0379 | [−0.0739, −0.0010] | 0.0448 | C2GES ahead, **significant at 0.05 (borderline)** |
| LLM zero-shot deepseek-chat | +0.2905 | [+0.2533, +0.3255] | <0.001 | **LLM decisively ahead of C2GES** |

Paired vs the lexical/semantic query baselines (both neural rerankers beat them
significantly): cross-encoder vs TF-IDF +0.0665 [0.0389, 0.0941] p<0.001, vs
SBERT +0.0815 [0.0544, 0.1069] p<0.001; BGE vs TF-IDF +0.0482 [0.0210, 0.0747]
p<0.001, vs SBERT +0.0632 [0.0260, 0.0995] p=0.0006. LLM vs TF-IDF +0.3765, vs
SBERT +0.3915, both p<0.001.

Magnitude sanity check: both neural rerankers land between BM25 (0.2273) and
c2ges_full (0.2983), as anticipated; nothing pathological (no 0.0, nothing >0.9;
the LLM's 0.5887 is a genuine large gain, verified per-question — e.g. it
recovers 3/4 gold IDs on the first root-cause question).

## 3. Analysis notes (mandatory)

**(a) Deployment-class tradeoff.** Full C2GES beats both same-deployment-class
neural cross-encoder rerankers (one comparison significant, one not), so within
the transparent/CPU-light/deterministic reranker class the paper's method
remains the best of the tested options. The zero-shot LLM roughly doubles
C2GES's F1 (0.5887 vs 0.2983). The pre-positioned narrative applies: C2GES
offers an auditable, deterministic, fully inspectable scoring rule with
negligible inference cost, whereas the LLM baseline requires a remote
proprietary endpoint, per-call cost/latency, and offers no per-term score
decomposition. The manuscript must report the LLM number honestly and reframe
C2GES's claim around the transparent-reranker class, not overall SOTA.

**(b) Label-provenance caveat / circularity.** The benchmark labels are
agent-generated and agent-verified (`label_provenance:
"agent_rewritten_and_agent_verified_candidate; not human gold"`). Part of the
LLM baseline's advantage may reflect LLM-LLM agreement — a modern instruction
LLM selecting evidence the way another LLM wrote/verified the labels — rather
than pure task superiority. This ties directly to the paper's existing Section 4
circularity subsection and the pre-announced human-gold subset plan (P1-8):
until dual expert annotation exists, the 0.5887 should be read as an upper bound
under agent-verified candidate labels. Conversely, the LLM score demonstrates
the benchmark has substantial headroom and discriminative power: it separates
methods across a 0.05–0.59 range and is not saturated by any tested approach.

## 4. LLM run cost/latency

- 200 API calls (one per question), model `deepseek-chat`, temperature 0.0,
  max_tokens 200, zero-shot, response cache at
  `llm_zeroshot_deepseek/llm_response_cache.jsonl` (200 entries, resume-safe).
- Wall clock: ~8.5 minutes (launched ~21:36:50 local, `summary.json` written
  21:45:20), i.e. ~2.5 s/call average including one full-document prompt per call.
- Token usage: the stdlib client does not record API `usage`; reconstructed from
  prompt text: ~3.19 M prompt characters total ≈ **~0.8 M input tokens** and
  ~4.8 k response characters ≈ **~1.2 k output tokens** across the 200 calls
  (≈4 k input tokens per call — each prompt embeds the full report sentence
  list). At DeepSeek's published cache-miss rates this is on the order of
  **US$0.2–0.3 for the full benchmark**, versus zero marginal cost for C2GES.
- No API key was written to any file (scanned outputs; only the env-var name is
  recorded in metadata).

## 5. Phase 2 — Executor evidence verification (all ✓, 108/108 checks)

Verified `source/supplement/c2ges_role_selective_graph/summary.json` against
`source/paper.tex`, with independent recomputation of Table 3 means/stds from
`details.jsonl` (2400 rows = 12 conditions × 200 questions):

| Manuscript claim | Executor artifact | Status |
|---|---|---|
| Table 3 Lead 0.0545±0.1426 (F1/P/R/ROUGE-L row) | matches, recomputed from details | ✓ |
| Table 3 TF-IDF centroid 0.0688±0.1556 row | matches, recomputed | ✓ |
| Table 3 TextRank 0.0700±0.1549 row | matches, recomputed | ✓ |
| Table 3 LexRank 0.0167±0.0946 row | matches, recomputed | ✓ |
| Table 3 Causal trigger 0.1071±0.1986 row | matches, recomputed | ✓ |
| Headline full C2GES 0.2983±0.2409 (all 4 metrics) | matches, recomputed | ✓ |
| Table 4 vs TF-IDF +0.0861 [0.0581, 0.1145] p<0.001 | matches (p=0.0000) | ✓ |
| Table 4 vs SBERT +0.1010 [0.0629, 0.1388] p<0.001 | matches (p=0.0000) | ✓ |
| Table 4 vs query-only +0.0831 [0.0541, 0.1120] p<0.001 | matches | ✓ |
| Table 4 vs no-role +0.0688 [0.0416, 0.0972] p<0.001 | matches | ✓ |
| Table 4 vs no-graph +0.0060 [0.0014, 0.0119] p=0.0254 | matches exactly | ✓ |
| Table 4 vs fixed-legacy +0.0403 [0.0178, 0.0621] p<0.001 | matches (p=0.0006) | ✓ |
| Headline +0.0710 vs BM25, CI [0.0423, 0.1000] | from in-package `bm25_k_sensitivity/summary.json` `k3_c2ges_full_vs_bm25_query` (0.0710, [0.04226, 0.09998], p=0.0) | ✓ |
| §7 cases: nerc_014 impact F1 0.667; nerc_009 root_cause; nerc_012 trigger; nerc_001 impact | present in details.jsonl (0.6667 / 0.4000 / 0.3333 / 0.6667) | ✓ |
| cv_protocol.json documents fold selection | 5 folds, `sha256(doc_id) mod 5`, whole-document assignment, 7-candidate grid incl. w=(0.52,0.40,0.08) and role_gated_chain family, purpose "non-leaky family/weight selection" | ✓ |

Fixed-legacy condition (`c2ges_full_fixed_legacy`) is fully present in the
Executor artifact (aggregate 0.2580, paired row above) — the last
previously-unevidenced condition is now closed.

Dataset integrity: 40 `nerc_*.json`, 2940 sentence records, 200 questions,
608 evidence assignments, `manifest.json` present — exact match to the
manuscript's stated counts.

## 6. Protocol notes / issues hit

- No protocol mismatches: the prepared baselines resolved the placed workspace
  directly (`--workspace .../2026_c2ges_engineeringletters/workspace`), no path
  adjustment needed beyond following MISSING_ARTIFACTS.md's drop location.
- The executor artifact contains no `bm25_query` condition (BM25 lives in the
  separate `bm25_k_sensitivity` supplement, as documented); paired baselines vs
  BM25 would need that supplement's details if desired later.
- The LLM client does not capture the API `usage` block — token numbers above
  are character-based estimates. If exact accounting is needed, re-run with a
  patched client (cache makes this cheap) or read provider-side billing.
- p-values of 0.0000 mean "below bootstrap resolution at 10000 samples", i.e.
  <0.001 as stated in the paper.
