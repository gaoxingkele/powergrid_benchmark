# GovReport transfer layer — protocol v1 (frozen 2026-09-26, before any outcome)

Purpose: test whether the **frozen** C²GES arm set produces a measurable gain on a
large, human-referenced, long-report corpus outside the power domain. This layer is
a **robustness transfer test**, not domain evidence and not a construct-validity test.

## 0. What this layer cannot show (fixed before running)

1. The role cue lexicon is power-domain specific (`fault`, `relay`, `load shed`,
   `voltage`, `MW`, …). On GovReport it fires on incidental words, so the role
   layer is **not** semantically interpretable here and is reported only as an
   exploratory contrast.
2. Any path-layer result is a property of the frozen, power-domain-tuned pipeline
   applied out of domain. A null here does not strengthen the domain claim, and a
   positive here does not rescue the mechanism.
3. GovReport references are **human-written abstractive summaries**; the standing
   ROUGE caveat of the main text applies unchanged.

## 1. Corpus and provenance

| Item | Value |
|---|---|
| Source | `ccdv/govreport-summarization` (HuggingFace), test split |
| Original | GovReport (Huang et al., NAACL 2021), CRS + GAO reports, CC BY 4.0 |
| Access | `datasets-server` rows API, 2026-09-26; 973 test rows fetched in 10 pages |
| Local raw copy | `05_External_Prospective_20260922/govreport/govreport_test_full.jsonl` (**outside the release scope**) |
| Shipped | derived numbers only |

Observed test-split shape: report characters min 2,650 / median 43,145 / max 193,646;
approximate candidate units min 24 / median 248 / max 1,529, so **no candidate cap is
applied** (unlike the 2,000-unit cap of the external prospective protocol).

## 2. Sampling (fixed now)

Five strata by report character length (quintiles of the 973 test rows), 20 rows per
stratum, drawn with `random.Random(20260926)` → **n = 100**. The full test split is a
later sensitivity, not part of this frozen test.

## 3. Unit construction

Deterministic sentence segmentation of the report text: split on paragraph
boundaries, then on sentence-final punctuation; drop units shorter than three words;
`sid = u%05d` in reading order; `unit_type = body`. Reference = the dataset summary,
untruncated.

## 4. Arms and budgets (identical to the frozen external arm set)

Arms: AB0 (lexical + position), AB1 (AB0 + role evidence), AB2 (AB1 + role-group
reservation), no_path (AB2 + typed graph salience), Full (no_path + path deletion at
weight 0.10), TextRank, Lead. Budgets: word 110/260 and unit K=5/10. No tuning.

## 5. Endpoints and criteria (fixed now)

- Primary endpoint: ROUGE-L F1, paired per document.
- **H1** (exploratory, role layer): AB2 − AB0 positive sign share ≥ 65 %.
- **H2** (primary, path layer): Full − no_path mean ≤ 0 **and** positive share of
  discordant documents ≤ 50 %.
- **H3** (primary): one-sided 95 % bootstrap upper limit on Full − no_path < +0.005.
- Statistics: exact sign-flip when n ≤ 20, otherwise 10⁵ randomised sign flips; Holm
  inside each contrast family; zero mass and discordant counts reported next to every
  mean.
- Diagnostics reported alongside: role-cue coverage (share of units with a dominant
  role), realised words per selected unit, and the number of exactly tied documents.

## 6. Decision rule (fixed now)

| Outcome | Reading |
|---|---|
| H2 and H3 hold | the path-layer null survives an out-of-domain, large-n transfer test |
| H2 or H3 fails | the null is domain-specific; report as a boundary condition, do not generalise |
| H1 holds here | cannot be used as role-layer evidence (see §0.1); report as a cue-lexicon artefact check |

## 7. Red lines

No tuning on outcomes, no pooling with the power-domain layers, no claim of domain
validity, and no verbatim GovReport text inside the release scope.
